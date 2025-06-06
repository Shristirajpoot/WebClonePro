# 🌐 WebClonePro — Dynamic Webpage Scraper & Recreator

[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95-green)](https://fastapi.tiangolo.com/)
[![Playwright](https://img.shields.io/badge/Playwright-1.36.0-purple)](https://playwright.dev/python/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## 🚀 Project Overview

This project is a **Website Cloning Tool** that takes any publicly accessible URL, scrapes the page content and structure with full browser automation, and returns a close replica of the website’s HTML and metadata.

It demonstrates proficiency in asynchronous programming with Python, modern API development with FastAPI, and advanced scraping using Playwright for dynamic content.

---

## ⚙️ Technology Stack

- 🐍 **Backend**: Python, FastAPI, Playwright
- ⚛️ **Frontend**: Next.js, React, TypeScript
- 🕷️ **Scraping**: Playwright for dynamic and modern web content rendering
- ☁️ **Deployment**: (Optional) Docker, Vercel, or any cloud provider


---

## 📝 Key Features

- 🔗 **URL input to clone**: Provide any public website URL to initiate cloning.
- 🎭 **Playwright scraping**: Uses Playwright for headless browser scraping to capture HTML, CSS, and assets.
- 🖥️ **Next.js frontend**: Interactive UI for entering URLs and viewing the cloned design preview.
- ⚡ **FastAPI backend**: Robust API server handling scraping requests asynchronously.
- 📄 **Metadata extraction**: Extracts essential metadata and styles from the target website.
- 🚨 **Error handling**: Gracefully handles scraping errors and invalid URLs.
- 🚀 **Caching and optimization**: (If implemented) Improves response times for repeated requests.

- 
## 📸 Screenshots

![Example1](./Screenshot%202025-06-07%20013644.png)

![Example2](./Screenshot%202025-06-07%20013711.png)

![Example3](./Screenshot%202025-06-07%20013739.png)


![Example4](./Screenshot%202025-06-07%20013807.png)


![Example5](./Screenshot%202025-06-07%20013826.png)


![Example6](./Screenshot%202025-06-07%20013912.png)


## 🎥 Demo Video

[![Watch the demo](https://img.youtube.com/vi/jfMwgjjgFoE/hqdefault.jpg)](https://youtu.be/jfMwgjjgFoE)

---
## 🛠️ Getting Started

### 📋 Prerequisites

- 🐍Python 3.9+
- 🔧Node.js 16+
- 🎭Playwright browsers installed (`playwright install`)


## 📥 Installation & Setup


1. Clone the repository:


git clone https://github.com/Shristirajpoot/WebClonePro.git
cd WebClonePro/backend

2.Backend setup
Create and activate a virtual environment:
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
Install required Python packages:

pip install --upgrade pip
pip install -r requirements.txt
Install Playwright browsers:

python -m playwright install
Launch the FastAPI server:

uvicorn hello:app --reload
Server runs at http://localhost:8000

3.Frontend setup
cd ../frontend
npm install
npm run dev

🔍 Usage

- Open your browser and go to http://localhost:3000.

- Enter the website URL you want to clone.

- Submit and wait for the backend to scrape and return the cloned content.

- View the preview on the frontend.

### 📂 Project Structure
/backend       # FastAPI backend code and scraping logic
/frontend      # Next.js frontend code and UI components
README.md      # Project overview and instructions

### 🔧 Challenges & Solutions
- ⚙️Overcame Windows-specific async subprocess limitations by configuring event loop policies.

- 🕸️Managed dynamic content loading with Playwright’s network idle wait.

- 🛡️Implemented comprehensive error handling and logging for reliability.

- ⏳Designed asynchronous scraping to improve performance and scalability.

### 🚀 Future Enhancements
- 📄 Add multi-page site cloning with navigation support.

- 🎨 Implement a user-friendly frontend interface.

- 📦 Enable downloadable static site packages (HTML/CSS/JS).

- ⚡Introduce caching to reduce redundant scraping and improve speed.

🙏 Acknowledgements
This project leveraged open-source tools and frameworks like FastAPI and Playwright, which enabled rapid development and powerful scraping capabilities.

📞 Contact
- Shristi Rajpoot
- 🔗LinkedIn: www.linkedin.com/in/shristi-rajpoot-36774b281

📄License
MIT License. See LICENSE for details.
