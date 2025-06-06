import os
import sys
import logging
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
import uvicorn
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv

from playwright.async_api import async_playwright
import openai

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# -------------------------------------------------
# Setup logging
# -------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------------------------
# FastAPI app
# -------------------------------------------------
app = FastAPI(
    title="Orchids Challenge API",
    description="FastAPI backend for the Website Cloning challenge with Playwright scraping and LLM cloning",
    version="1.4.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend dev URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Pydantic models
# -------------------------------------------------
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CloneRequest(BaseModel):
    url: HttpUrl

# -------------------------------------------------
# Dummy in-memory data
# -------------------------------------------------
items_db: List[Item] = [
    Item(id=1, name="Sample Item", description="This is a sample item"),
    Item(id=2, name="Another Item", description="This is another sample item"),
]

# -------------------------------------------------
# Utility: check same domain
# -------------------------------------------------
def is_same_domain(url1: str, url2: str) -> bool:
    """Check if two URLs share the same domain."""
    return urlparse(url1).netloc == urlparse(url2).netloc

# -------------------------------------------------
# Utility: rewrite URLs in HTML to absolute URLs
# -------------------------------------------------
def rewrite_resource_urls(soup: BeautifulSoup, base_url: str):
    """Rewrite href/src URLs to absolute URLs for proper loading."""
    for tag in soup.find_all(['a', 'link', 'script', 'img']):
        attr = 'href' if tag.name in ['a', 'link'] else 'src' if tag.name in ['script', 'img'] else None
        if attr and tag.has_attr(attr):
            original = tag[attr]
            if original.startswith('javascript:') or original.startswith('#') or original.startswith('mailto:'):
                continue
            absolute = urljoin(base_url, original)
            tag[attr] = absolute

# -------------------------------------------------
# Legacy fetch_page function (requests + BeautifulSoup)
# Kept for download endpoint or fallback
# -------------------------------------------------
def fetch_page(url: str) -> dict:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    rewrite_resource_urls(soup, url)

    title = soup.title.string.strip() if soup.title and soup.title.string else "No title found"

    desc_tag = soup.find("meta", attrs={"name": "description"})
    description = (
        desc_tag.get("content", "").strip()
        if desc_tag and desc_tag.get("content")
        else "No description found"
    )

    fav_tag = soup.find("link", rel=lambda v: v and "icon" in v.lower())
    favicon_url = None
    if fav_tag and fav_tag.get("href"):
        favicon_url = urljoin(url, fav_tag["href"].strip())

    clean_html = str(soup)[:200000]  # Larger size limit for full page

    return {
        "url": url,
        "html": clean_html,
        "title": title,
        "description": description,
        "favicon": favicon_url,
    }

# -------------------------------------------------
# Async Playwright scraper to get fully rendered page HTML
# -------------------------------------------------
async def scrape_site_with_playwright(url: str) -> dict:
    logger.info(f"Starting Playwright scraping for {url}")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until='networkidle')
        content = await page.content()
        await browser.close()
        logger.info(f"Scraping done for {url}, length: {len(content)} chars")
        return {
            "url": url,
            "html": content,
        }

# -------------------------------------------------
# LLM generation function calling OpenAI's API
# -------------------------------------------------
async def generate_clone_html(design_context: dict) -> str:
    """
    Input: design_context dict with 'html' key (raw HTML from scraper)
    Output: string of cloned HTML generated by LLM
    """
    logger.info("Generating cloned HTML from design context with OpenAI LLM")

    design_html = design_context.get("html", "")
    if not design_html:
        raise ValueError("Empty design context HTML")

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that converts website design context into clean, semantic, and functional HTML code."
        },
        {
            "role": "user",
            "content": (
                "Generate a complete HTML website clone based on the following design context:\n\n"
                f"{design_html}\n\n"
                "Focus on preserving the layout and styles as much as possible. Return only the HTML code."
            )
        }
    ]

    try:
        response = await asyncio.to_thread(
            lambda: openai.ChatCompletion.create(
                model="gpt-4o-mini",  # You can use other models like "gpt-4", "gpt-4o", "gpt-4o-mini"
                messages=messages,
                max_tokens=1500,
                temperature=0.3,
            )
        )
        html_code = response['choices'][0]['message']['content']
        logger.info("Received cloned HTML from LLM")
        return html_code

    except Exception as e:
        logger.error(f"Error generating clone HTML: {e}")
        raise

# -------------------------------------------------
# Basic routes
# -------------------------------------------------
@app.get("/")
async def root():
    return {"message": "Hello from FastAPI backend!", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "orchids-challenge-api"}

# -------------------------------------------------
# CRUD routes (unchanged)
# -------------------------------------------------
@app.get("/items", response_model=List[Item])
async def get_items():
    return items_db

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items", response_model=Item)
async def create_item(item: ItemCreate):
    new_id = max((itm.id for itm in items_db), default=0) + 1
    new_item = Item(id=new_id, **item.dict())
    items_db.append(new_item)
    return new_item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemCreate):
    for i, current in enumerate(items_db):
        if current.id == item_id:
            updated_item = Item(id=item_id, **item.dict())
            items_db[i] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    for i, itm in enumerate(items_db):
        if itm.id == item_id:
            deleted = items_db.pop(i)
            return {"message": f"Item {item_id} deleted", "deleted_item": deleted}
    raise HTTPException(status_code=404, detail="Item not found")

# -------------------------------------------------
# POST /clone endpoint using Playwright + LLM workflow
# -------------------------------------------------
@app.post("/clone")
async def clone_website(data: CloneRequest):
    start_url = str(data.url)
    logger.info(f"Received URL to clone: {start_url}")

    try:
        # Step 1: Scrape site fully rendered HTML using Playwright
        design_context = await scrape_site_with_playwright(start_url)

        # Step 2: Generate cloned HTML using LLM workflow (OpenAI API)
        cloned_html = await generate_clone_html(design_context)

        # Return cloned HTML in JSON response
        return {"html": cloned_html, "source_url": start_url}

    except Exception as e:
        logger.exception(f"Error cloning site {start_url}")
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------------------------
# Keep your existing /clone/download endpoint using legacy requests scrape
# -------------------------------------------------
@app.get("/clone/download")
async def download_cloned_html(url: HttpUrl):
    logger.info(f"Download requested for: {url}")
    try:
        data = fetch_page(str(url))
        headers = {
            "Content-Disposition": 'attachment; filename="cloned_page.html"',
            "Content-Type": "text/html; charset=utf-8",
        }
        return Response(content=data["html"], headers=headers, media_type="text/html")

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="Request timed out")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Request failed: {e}")
    except Exception as e:
        logger.exception("Unexpected error during download")
        raise HTTPException(status_code=500, detail="Internal server error")

# -------------------------------------------------
# Run if executed directly
# -------------------------------------------------
def main():
    uvicorn.run("hello:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
