# 🗞️ CoinDesk Scraper

A robust Python-based web scraping toolkit for extracting headlines, articles, and downloadable content from [CoinDesk](https://www.coindesk.com/). Built with modular architecture, retry logic, logging, and config management — ready for extension.

---

## ✨ Features

| Feature                | Status         | Description                                                                                                                           |
| ---------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **HTTP Client**        | ✅ Implemented | Reusable `HTTPClient` class with automatic retry (3 attempts), exponential backoff, custom user-agent, and streaming download support |
| **Headline Scraper**   | ✅ Implemented | Parses CoinDesk homepage using BeautifulSoup, extracts `<h2>` headlines, saves raw HTML and structured JSON                           |
| **PDF Downloader**     | ✅ Implemented | Downloads binary files (PDFs, etc.) using streaming chunked writes                                                                    |
| **Logging**            | ✅ Implemented | Per-request logging with timestamps to `logs/app.log`                                                                                 |
| **Environment Config** | ⚠️ Partial     | `.env` file support via `python-dotenv`; `API_KEY` defined but not yet wired to any endpoint                                          |
| **Orchestrator**       | ✅ Implemented | `main.py` entry point runs all scrapers sequentially                                                                                  |

---

## 📁 Project Architecture

```
CoinDesk Scraper/
├── main.py                      # 🚀 Entry point — runs everything
├── requirements.txt             # 📦 Python dependencies
├── .gitignore                   # 🙈 Ignored: logs/, downloads/, output/, .env, __pycache__
├── .env                         # 🔐 Secret API keys (you create this)
│
├── http_client/                 # 🌐 Reusable HTTP layer
│   ├── __init__.py
│   └── client.py                # HTTPClient: retry, timeout, streaming, logging
│
├── scrapers/                    # 🕷️ Scraper modules
│   ├── __init__.py
│   ├── coindesk_html.py         # Scrapes CoinDesk homepage headlines → HTML + JSON
│   └── downloader.py            # Downloads binary files (PDFs, etc.)
│
├── utils/                       # 🛠️ Utilities
│   ├── config.py                # Loads .env → exposes API_KEY
│
├── output/                      # 📄 Generated output
│   ├── homepage.html            # Raw saved HTML of CoinDesk homepage
│   └── articles.json            # Extracted headlines as JSON
│
├── downloads/                   # ⬇️ Downloaded files
│   └── sample.pdf               # Example downloaded PDF
│
└── logs/                        # 📋 Application logs
    └── app.log                  # Structured log with timestamps & levels
```

### Module Responsibilities

| Module               | File                        | Role                                                                                        |
| -------------------- | --------------------------- | ------------------------------------------------------------------------------------------- |
| **Entry Point**      | `main.py`                   | Calls `scrape_homepage()` then `download_pdf()` in sequence                                 |
| **HTTP Client**      | `http_client/client.py`     | Wraps `requests.Session` with retry adapter, configurable timeout, custom headers, logging  |
| **Headline Scraper** | `scrapers/coindesk_html.py` | Fetches `https://www.coindesk.com/` via `HTTPClient`, parses `<h2>` tags, saves HTML + JSON |
| **PDF Downloader**   | `scrapers/downloader.py`    | Uses `HTTPClient.download()` to stream-save a PDF from w3.org                               |
| **Config**           | `utils/config.py`           | Calls `load_dotenv()`, exposes `API_KEY` for future API integration                         |
| **Output**           | `output/`                   | `homepage.html` (raw page), `articles.json` (parsed headlines)                              |
| **Logs**             | `logs/`                     | `app.log` — info/error logs with timestamps                                                 |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/your-username/coindesk-scraper.git
cd coindesk-scraper
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # macOS / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables (optional)

Create a `.env` file in the project root:

```env
COINDESK_API_KEY=your_api_key_here
```

> **Note:** The API key is loaded but not yet consumed. This is ready for future CoinDesk API integration.

### 5. Run the scraper

```bash
python main.py
```

---

## 🧪 Usage

Running `python main.py` will:

1. **Scrape CoinDesk homepage** — fetches `https://www.coindesk.com/`, extracts top 10 `<h2>` headlines, prints them to console, saves:
   - `output/homepage.html` (full raw HTML)
   - `output/articles.json` (parsed headlines as JSON)
2. **Download a sample PDF** — downloads `dummy.pdf` from w3.org and saves it to `downloads/sample.pdf`

### Sample Console Output

```
==================================================
CoinDesk Scraper Started
==================================================

Latest Headlines

Bitcoin Rallies Past $70,000
Crypto Regulation Update
...

Download Finished

Finished Successfully!
```

### Sample Output (`output/articles.json`)

```json
[
  "Bitcoin Rallies Past $70,000",
  "Crypto Regulation Update",
  "DeFi TVL Hits New High"
]
```

---

## ⚙️ Configuration

All configuration is managed via `.env` in the project root:

| Variable           | Required | Default | Description                           |
| ------------------ | -------- | ------- | ------------------------------------- |
| `COINDESK_API_KEY` | ❌ No    | None    | API key for CoinDesk API (future use) |

Settings hardcoded in `HTTPClient` (can be customized in `http_client/client.py`):

| Setting            | Value                                     | Description                      |
| ------------------ | ----------------------------------------- | -------------------------------- |
| `timeout`          | 15 seconds                                | Request timeout                  |
| `retries`          | 3                                         | Max retry attempts               |
| `backoff_factor`   | 1                                         | Exponential backoff (1s, 2s, 4s) |
| `status_forcelist` | 429, 500, 502, 503, 504                   | Retry on these status codes      |
| `User-Agent`       | Mozilla/5.0 (Windows NT 10.0; Win64; x64) | Browser user-agent header        |

---

## 📋 Logging

All HTTP requests and errors are logged to `logs/app.log` with the format:

```
2024-01-15 10:30:45,123 | INFO | GET https://www.coindesk.com/
2024-01-15 10:30:47,456 | ERROR | ConnectionTimeout(…)
```

| Log Level | When                                      |
| --------- | ----------------------------------------- |
| `INFO`    | Every GET/DOWNLOAD request                |
| `ERROR`   | Request failures, timeouts, status errors |

---

## 🔮 Future Enhancements

- [ ] **API Integration** — Wire `API_KEY` to CoinDesk's public API for richer data (prices, articles, news)
- [ ] **Multiple Scrapers** — Add scrapers for specific CoinDesk sections (Markets, Tech, Opinion)
- [ ] **Scheduling** — Add `schedule` or `APScheduler` for periodic scraping
- [ ] **Database Storage** — Store scraped articles in SQLite / PostgreSQL instead of JSON
- [ ] **Email/Notification** — Send alerts when keywords appear in headlines
- [ ] **Docker Support** — Containerized deployment with `Dockerfile` + `docker-compose.yml`
- [ ] **CLI Interface** — Add `argparse` for running specific scrapers, custom URLs, etc.
- [ ] **Tests** — Unit tests for `HTTPClient`, scrapers, and downloader

---

## 📄 License

MIT
