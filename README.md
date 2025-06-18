# Belgium Real Estate Scraper

A Python project that scrapes real estate property listings from Zimmo.be to build a comprehensive dataset covering properties all over Belgium.

---

## General Info

This scraper collects extensive property data by navigating through multiple pages and extracting detailed information such as property type, price, rooms, area, and additional features. The resulting dataset is saved as a CSV file.

## Feature

- Scrapes property listings across Belgium, covering many cities and localities.
- Collects over 10,000 unique property entries without duplicates.
- Data columns include locality, property type, price, rooms, living area and more.
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

While scraping, the program keeps the user informed after each page loop:

```
📦 Total properties scraped so far: 10065
```

This will start scraping property data from Zimmo.be, collecting pages and property details concurrently, and save the final cleaned dataset as `properties{MMDDHHMM}.csv`

This program will save data into `leaders.json` inside the `data/` folder

### 📊 Sample Output in CSV

```csv
zimmo code,type,price,street,number,postcode,city,living area(m²),ground area(m²),bedroom,bathroom,garage,garden,EPC(kWh/m²),renovation obligation,year built,mobiscore,url
L97O9,Vakantiewoning (Huis),,,,8670,Oostduinkerke,40.0,105.0,2,1,,False,,False,,7.4,https://www.zimmo.be/nl/oostduinkerke-8670/te-koop/huis/L97O9/?search=eyJmaWx0ZXIiOiB7InN0YXR1cyI6IHsiaW4iOiBbIkZPUl9TQUxFIiwgIlRBS0VfT1ZFUiJdfSwgImNhdGVnb3J5IjogeyJpbiI6IFsiSE9VU0UiLCAiQVBBUlRNRU5UIl19LCAicHJpY
```

---

### 📊 Sample Output in terminal

The program will also ask user if they want to see preview in their terminal:

```bash

📖 Do you want preview results? ('y' to confirm):

```

The program will then show output in the terminal

```

📖 Reading

```

The program ends by displaying the total runtime to fetch the data.
(In the `nice-to-have` branch, this feature is replaced by a progress bar.)

```
⌛️ Total
```

## What Went Well / Challenges

- Originally intended to scrape data from `Immoweb.be`, but encountered strong anti-scraping measures that made it impractical.
- Use `Zimmo.be` as the data source, which allowed for smoother scraping.
- Removed Selenium from requests, speeding up scraping with requests.Session.
- Implemented multithreading for concurrency, reducing total runtime.
- 📊 Handled Zimmo pagination limits:
  - Zimmo only allows up to 100 pages per query
  - Resolved by manually created multiple base URLs targeting different price ranges:
    - Started from €0 up to €1,499,999
    - In increments of €50,000 per query range
    - For the final group (starting from €1,499,999), the max limit was left open to capture all remaining properties
    - **For future improvement** Use a script to automatically create these links by decoding the search filters from the `base64` string.
