# Belgium Real Estate Scraper

A Python project that scrapes real estate property listings from Zimmo.be to build a comprehensive dataset covering properties all over Belgium.

---

## General Info

This scraper collects extensive property data by navigating through multiple pages and extracting detailed information such as property type, price, rooms, area, and additional features. The resulting dataset is saved as a CSV file.

## Feature

- Scrapes property listings across Belgium, covering many cities and localities.
- Collects over 10,000 unique property entries without duplicates.
- Data columns include locality, property type, price, rooms, living area, kitchen status, furnished status, and more.
- Handles missing data by filling with None to avoid empty rows.
- Uses threading to speed up data collection.

## 🛠 Tech Stack

Language: Python 3
Libraries: requests, BeautifulSoup4, threading, pandas, re
Concurrency: Python threading module

## ▶️ Usage

Run the main scraper script:

```bash
python main.py
```

This will start scraping property data from Zimmo.be, collecting pages and property details concurrently, and save the final cleaned dataset as `properties.csv`

## What Went Well / Challenges

- Originally intended to scrape data from Immoweb, but encountered strong access blocks and anti-scraping measures that made it impractical.
- Pivoted to use Zimmo.be as the data source, which allowed for smoother scraping.
- Removed Selenium from most requests, using it only when necessary, speeding up scraping with requests.Session.
- Implemented multithreading for concurrency, reducing total runtime.
