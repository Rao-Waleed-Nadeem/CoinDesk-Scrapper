# 🗞️ CoinDesk Scraper

A robust Python-based web scraping and parsing toolkit for extracting headlines, articles, and downloadable content from [CoinDesk](https://www.coindesk.com/). Built with modular architecture — HTTP client layer, scrapers, structured parsers, retry logic, logging, and config management — ready for extension.

---

## ✨ Features

| Feature                | Status         | Description                                                                                                                           |
| ---------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **HTTP Client**        | ✅ Implemented | Reusable `HTTPClient` class with automatic retry (3 attempts), exponential backoff, custom user-agent, and streaming download support |
| **Headline Scraper**   | ✅ Implemented | Fetches CoinDesk homepage, saves raw + pretty HTML, and returns structured article data using `HomepageParser`                        |
| **PDF Downloader**     | ✅ Implemented | Downloads binary files (PDFs, etc.) using streaming chunked writes                                                                    |
| **Logging**            | ✅ Implemented | Per-request logging with timestamps to `logs/app.log`                                                                                 |
| **Environment Config** | ⚠️ Partial     | `.env` file support via `python-dotenv`; `API_KEY` defined but not yet wired to any endpoint                                          |
| **Parsers**            | ✅ Implemented | Structured parsing layer with abstract base, homepage, category, and full-article parsers using BeautifulSoup + `lxml`                |
| **Orchestrator**       | ✅ Implemented | `main.py` entry point runs all scrapers and parsers sequentially, outputs structured article titles                                   |

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
│   ├── coindesk_html.py         # Scrapes CoinDesk homepage → saves HTML + invokes HomepageParser
│   └── downloader.py            # Downloads binary files (PDFs, etc.)
│
├── parsers/                     # 🧠 Structured parsing layer
│   ├── __init__.py
│   ├── base_parser.py           # Abstract BaseParser (ABC) with select, get_text, validate helpers
│   ├── utils.py                 # Shared parsing utilities: clean_text, normalize_url, safe_select, etc.
│   ├── homepage_parser.py       # Parses homepage <article> cards → title, url, category, image
│   ├── category_parser.py       # Parses category pages (e.g. /markets) → title, url, category, summary, image
│   └── article_parser.py        # Parses full article page → title, author, date, body, tags, images, metadata
│
├── utils/                       # 🛠️ Utilities
│   ├── config.py                # Loads .env → exposes API_KEY
│
├── output/                      # 📄 Generated output
│   ├── homepage.html            # Raw saved HTML of CoinDesk homepage
│   ├── homepage_pretty.html     # Pretty-printed (BeautifulSoup prettify) version of homepage HTML
│   └── articles.json            # Extracted headlines as JSON (legacy)
│
├── downloads/                   # ⬇️ Downloaded files
│   └── sample.pdf               # Example downloaded PDF
│
└── logs/                        # 📋 Application logs
    └── app.log                  # Structured log with timestamps & levels
```

### Module Responsibilities

| Module                | File                         | Role                                                                                             |
| --------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------ |
| **Entry Point**       | `main.py`                    | Calls `scrape_homepage()` → prints structured article titles → calls `download_pdf()`            |
| **HTTP Client**       | `http_client/client.py`      | Wraps `requests.Session` with retry adapter, configurable timeout, custom headers, logging       |
| **Headline Scraper**  | `scrapers/coindesk_html.py`  | Fetches `https://www.coindesk.com/`, saves raw + pretty HTML, invokes `HomepageParser`           |
| **PDF Downloader**    | `scrapers/downloader.py`     | Uses `HTTPClient.download()` to stream-save a PDF from w3.org                                    |
| **Base Parser**       | `parsers/base_parser.py`     | Abstract class (`ABC`) with `select()`, `select_all()`, `get_text()`, `get_attr()`, `validate()` |
| **Parsing Utilities** | `parsers/utils.py`           | Shared helpers: `extract_text()`, `extract_attr()`, `normalize_url()`, `safe_select()`, etc.     |
| **Homepage Parser**   | `parsers/homepage_parser.py` | Parses homepage `<article>` cards → title, url, category, image                                  |
| **Category Parser**   | `parsers/category_parser.py` | Parses category pages → title, url, category, summary, image                                     |
| **Article Parser**    | `parsers/article_parser.py`  | Parses full article page → title, author, date, body (paragraphs), tags, images, SEO metadata    |
| **Config**            | `utils/config.py`            | Calls `load_dotenv()`, exposes `API_KEY` for future API integration                              |
| **Output**            | `output/`                    | `homepage.html`, `homepage_pretty.html`, `articles.json`                                         |
| **Logs**              | `logs/`                      | `app.log` — info/error logs with timestamps                                                      |

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

1. **Scrape CoinDesk homepage** — fetches `https://www.coindesk.com/`, saves:
   - `output/homepage.html` (full raw HTML)
   - `output/homepage_pretty.html` (pretty-printed HTML via BeautifulSoup)
2. **Parse homepage articles** — uses `HomepageParser` to extract structured data from each `<article>` card:
   - `title` — article headline
   - `url` — absolute URL to the article
   - `category` — article category/section (e.g. Markets, Tech)
   - `image` — absolute URL to the featured image
3. **Print headlines** — displays top 10 article titles in the console
4. **Download a sample PDF** — downloads `dummy.pdf` from w3.org to `downloads/sample.pdf`

### Sample Console Output

```
==================================================
CoinDesk Scraper Started
==================================================

Latest Headlines

Bitcoin Rallies Past $70,000
Crypto Regulation Update
DeFi TVL Hits New High
...

Download Finished

Finished Successfully!
```

### Sample Structured Output (from `HomepageParser`)

```json
[
  {
    "title": "Bitcoin Rallies Past $70,000",
    "url": "https://www.coindesk.com/markets/2025/bitcoin-rallies",
    "category": "Markets",
    "image": "https://www.coindesk.com/resizer/example.jpg"
  }
]
```

---

## 🧠 Parser Layer

The `parsers/` module provides a structured, object-oriented approach to extracting data from CoinDesk pages.

### Architecture

```
BaseParser (abstract)
├── HomepageParser   — homepage <article> cards (title, url, category, image)
├── CategoryParser   — category pages; multiple <article> cards (title, url, category, summary, image)
└── ArticleParser    — full article page (title, author, date, body paragraphs, tags, images, metadata)
```

### How to Use a Parser

```python
from parsers.homepage_parser import HomepageParser

html = "<html>...</html>"       # raw HTML from HTTPClient
parser = HomepageParser(html)   # automatically parses with lxml
articles = parser.parse()       # returns list of dicts

for article in articles:
    print(article["title"], article["url"])
```

### Shared Utilities (`parsers/utils.py`)

| Function              | Description                                 |
| --------------------- | ------------------------------------------- |
| `clean_text()`        | Normalize whitespace                        |
| `extract_text()`      | Safely extract cleaned text from an element |
| `extract_attr()`      | Safely extract an HTML attribute            |
| `normalize_url()`     | Convert relative URLs to absolute           |
| `validate_required()` | Check required fields exist in a dict       |
| `safe_select()`       | Safe `select_one()` wrapper                 |
| `safe_select_all()`   | Safe `select()` wrapper                     |
| `extract_list_text()` | Extract text from multiple elements         |

### BaseParser Helper Methods

| Method                     | Returns     | Description                               |
| -------------------------- | ----------- | ----------------------------------------- |
| `select(selector)`         | Tag or None | Wraps `soup.select_one()`                 |
| `select_all(selector)`     | List[Tag]   | Wraps `soup.select()`                     |
| `get_text(selector)`       | str or None | Extract cleaned text via CSS selector     |
| `get_attr(selector, attr)` | str or None | Extract HTML attribute                    |
| `get_list_text(selector)`  | List[str]   | Extract text from multiple elements       |
| `validate(data, fields)`   | dict        | Raises `ValueError` if fields are missing |

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

## 📦 Dependencies

| Package             | Version | Purpose                      |
| ------------------- | ------- | ---------------------------- |
| `requests`          | 2.34.2  | HTTP client                  |
| `beautifulsoup4`    | 4.15.0  | HTML parsing                 |
| `lxml`              | 5.3.1   | Fast XML/HTML parser for BS4 |
| `python-dotenv`     | 1.2.2   | `.env` file loading          |
| `certifi`           | 2026.7  | SSL certificate bundle       |
| `soupsieve`         | 2.9.1   | CSS selector engine for BS4  |
| `typing_extensions` | 4.16.0  | Type hint backports          |
| `urllib3`           | 2.7.0   | HTTP connection pooling      |

---

## 🔮 Future Enhancements

- [ ] **API Integration** — Wire `API_KEY` to CoinDesk's public API for richer data (prices, articles, news)
- [ ] **Scheduling** — Add `schedule` or `APScheduler` for periodic scraping
- [ ] **Database Storage** — Store parsed articles in SQLite / PostgreSQL
- [ ] **Email/Notification** — Send alerts when keywords appear in headlines
- [ ] **Docker Support** — Containerized deployment with `Dockerfile` + `docker-compose.yml`
- [ ] **CLI Interface** — Add `argparse` for running specific scrapers/parsers, custom URLs, etc.
- [ ] **Tests** — Unit tests for `HTTPClient`, scrapers, all parsers

---

## 📄 License

MIT
