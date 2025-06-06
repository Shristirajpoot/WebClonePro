from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
import uvicorn
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import logging
from collections import deque

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
    description="FastAPI backend for the Website Cloning challenge",
    version="1.3.0",
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
                # Skip javascript links, fragments, mailto
                continue
            absolute = urljoin(base_url, original)
            tag[attr] = absolute

# -------------------------------------------------
# Utility: fetch page and return metadata + rewritten HTML
# -------------------------------------------------
def fetch_page(url: str) -> dict:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # DO NOT remove scripts/styles/iframes to keep page functional

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
# POST /clone  (Multi-page clone preview JSON)
# -------------------------------------------------
@app.post("/clone")
async def clone_website(data: CloneRequest):
    start_url = str(data.url)
    logger.info(f"Received URL to clone (multi-page): {start_url}")

    visited = set()
    to_visit = deque([start_url])
    pages = []

    MAX_PAGES = 5  # Limit number of pages to crawl

    try:
        while to_visit and len(pages) < MAX_PAGES:
            url = to_visit.popleft()
            if url in visited:
                continue
            visited.add(url)

            page_data = fetch_page(url)
            pages.append(page_data)

            # Parse links from page HTML to queue for crawling
            soup = BeautifulSoup(page_data["html"], "html.parser")
            for a_tag in soup.find_all("a", href=True):
                link = urljoin(url, a_tag["href"])
                # Only follow links within the same domain, ignore fragments, mailto etc.
                if is_same_domain(start_url, link) and link not in visited:
                    if link.startswith("http://") or link.startswith("https://"):
                        to_visit.append(link)

        return {"pages": pages}

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="Request timed out")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Request failed: {e}")
    except Exception as e:
        logger.exception("Unexpected error")
        raise HTTPException(status_code=500, detail="Internal server error")

# -------------------------------------------------
# GET /clone/download  (Download HTML file)
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
