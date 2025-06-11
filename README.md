# 🌐 WebClonePro — Dynamic Webpage Scraper & Recreator
![GitHub Repo stars](https://img.shields.io/github/stars/Shristirajpoot/WebClonePro?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/Shristirajpoot/WebClonePro?color=brightgreen)
![Built with](https://img.shields.io/badge/Built%20with-FastAPI%20%7C%20Next.js-blue)
[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95-green)](https://fastapi.tiangolo.com/)
[![Playwright](https://img.shields.io/badge/Playwright-1.36.0-purple)](https://playwright.dev/python/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

---

## 🚀 Overview

**WebClonePro** is an advanced tool that allows users to input any public website URL and generate a clone-like HTML preview using headless browser scraping.

This project showcases dynamic content extraction using **Playwright**, fast API development with **FastAPI**, and a sleek user interface powered by **Next.js** & **TypeScript**.

---

## 🎥 Demo Video
📺 **Watch the walkthrough here:**  
[![Watch the demo](https://img.youtube.com/vi/jfMwgjjgFoE/hqdefault.jpg)](https://youtu.be/jfMwgjjgFoE)
> 🔗 *Click the image or [watch on YouTube]((https://youtu.be/jfMwgjjgFoE)*
--- 


## 🛠️ Features

- 🔗 Clone any public website URL
- 🎭 Powerful dynamic scraping using **Playwright**
- ⚡ Fast & asynchronous backend with **FastAPI**
- 📄 Metadata, styles, and HTML extraction
- 🖥️ Frontend preview of cloned content
- 🧠 Intelligent error handling and feedback
- 📦 Optional support for downloadable static sites (future)
- ⚙️ Planned caching and performance boosts

---

## 📂 Project Structure

```plaintext
WebClonePro/
├── backend/               # FastAPI backend for scraping logic
│   ├── hello.py           # Main API app
│   ├── requirements.txt   # Python dependencies
│   └── ...                # Utilities, models
│
├── frontend/              # Next.js frontend for UI
│   ├── pages/             # Main input and result pages
│   ├── components/        # Reusable React components
│   └── ...                # Static assets, config
│
├── README.md              # Project documentation
└── LICENSE                # MIT License

```
🖼️ Screenshots
📸 Real views of WebClonePro in action:
| URL Input Page                                         | Preview of Cloned Site                                 |
| ------------------------------------------------------ | ------------------------------------------------------ |
| ![Screenshot1](./Screenshot%202025-06-07%20013644.png) | ![Screenshot2](./Screenshot%202025-06-07%20013711.png) |
| Metadata Extracted                                     | Navigation Sample                                      |
| ------------------------------------------------------ | ------------------------------------------------------ |
| ![Screenshot3](./Screenshot%202025-06-07%20013739.png) | ![Screenshot4](./Screenshot%202025-06-07%20013807.png) |
| Example Cloned                                         | Responsive View                                        |
| ------------------------------------------------------ | ------------------------------------------------------ |
| ![Screenshot5](./Screenshot%202025-06-07%20013826.png) | ![Screenshot6](./Screenshot%202025-06-07%20013912.png) |

## 📋 Getting Started

- 🔧 Prerequisites

- 🐍 Python 3.9+

- 🔧 Node.js 16+

- 🎭 Install Playwright Browsers:

```bash
python -m playwright install
```
## 📥 Installation & Setup

1️⃣ Clone Repository
```bash
git clone https://github.com/Shristirajpoot/WebClonePro.git
cd WebClonePro
```
2️⃣ Backend Setup
```bash
cd backend
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
python -m playwright install

uvicorn hello:app --reload
```
Server will run at http://localhost:8000

3️⃣ Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```
Frontend available at http://localhost:3000

## 🔍 Usage
- Open your browser and go to http://localhost:3000

- Enter any public website URL

- Submit the form and wait for the scraping

- View the cloned preview and metadata



## 🚧 Challenges & Solutions
- ⚙️ Managed Playwright async subprocesses on Windows

- 🕸️ Solved dynamic loading via network idle wait strategy

- 🛡️ Implemented robust error handling and fallback messages

- 🚀 Used async def for high-performance scraping

## 🧭 Future Enhancements
- 📄 Clone multi-page sites with link traversal

- 📦 Enable download of static HTML/CSS packages

- 🎨 Add history and clone logs on UI

- ⚡ Caching for repeated URLs

## 📞 Contact
### Shristi Rajpoot
- 🔗LinkedIn: www.linkedin.com/in/shristi-rajpoot-36774b281
- 📧 Email: shristirajpoot369@gmail.com
- 🔗 GitHub: @Shristirajpoot

## 📄License
MIT License. See LICENSE for details..

### 🌟 If you found this useful, please ⭐ star the repo and share it!


