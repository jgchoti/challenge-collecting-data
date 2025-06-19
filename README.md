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

- Language: Python 3
- Libraries: requests, BeautifulSoup4, threading, pandas, re
- Concurrency: Python threading module

## ▶️ Usage

Run the main scraper script:

```bash
python main.py
```

While scraping, the program keeps the user informed after each page loop:

```
🔎 Done scraping listings in price range:650000 - 699999 - Page: 57
🗃️ Total properties scraped so far: 20772
🏷️ Done scraping listings in price range :650000 - 699999

```

This will start scraping property data from Zimmo.be, collecting pages and property details concurrently, and save the final cleaned dataset as `properties{MMDDHHMM}.csv`

This program will save data into `leaders.json` inside the `data/` folder

### 📊 Sample Output in CSV

```csv
zimmo code,type,price,street,number,postcode,city,living area(m²),ground area(m²),bedroom,bathroom,garage,garden,EPC(kWh/m²),renovation obligation,year built,mobiscore,url
L9M5W,Chalet (Huis),49000.0,Patrijzenpad,,2275,Gierle,,2607.0,1,,,False,,False,1986,5.9,/nl/gierle-2275/te-koop/huis/L9M5W/?search=eyJmaWx0ZXIiOiB7InN0YXR1cyI6IHsiaW4iOiBbIkZPUl9TQUxFIiwgIlRBS0VfT1ZFUiJdfSwgImNhdGVnb3J5IjogeyJpbiI6IFsiSE9VU0UiLCAiQVBBUlRNRU5UIl19LCAicHJpY2UiOiB7InVua25vd24iOiBmYWxzZSwgInJhbmdlIjogeyJtaW4iOiAwLCAibWF4IjogNDk5OTl9fX19

```

---

### 📊 Sample Output in terminal

The program will also ask user if they want to see preview in their terminal:

```

📖 Do you want preview results? ('y' to confirm):y
🔎 Preview data from properties06181030.csv
  zimmo code                    type    price  ... year built mobiscore                                                url
0      L9M5W           Chalet (Huis)  49000.0  ...       1986       5.9  /nl/gierle-2275/te-koop/huis/L9M5W/?search=eyJ...
1      L9W3V           Woning (Huis)  40000.0  ...       <NA>       NaN  /nl/quaregnon-7390/te-koop/huis/L9W3V/?search=...
2      L5Q5T           Andere (Huis)  45000.0  ...       1850       7.7  /nl/maaseik-3680/te-koop/huis/L5Q5T/?search=ey...
3      L9KJ7  Eengezinswoning (Huis)  49900.0  ...       <NA>       NaN  /nl/ivoz-ramet-4400/te-koop/huis/L9KJ7/?search...
4      L9X2H   Vakantiewoning (Huis)  39000.0  ...       1970       5.1  /nl/wechelderzande-2275/te-koop/huis/L9X2H/?se...

[5 rows x 18 columns]

🏡 Zimmo.be scraping complete — total properties: 25403
📌 Columns: ['zimmo code', 'type', 'price', 'street', 'number', 'postcode', 'city', 'living area(m²)', 'ground area(m²)', 'bedroom', 'bathroom', 'garage', 'garden', 'EPC(kWh/m²)', 'renovation obligation', 'year built', 'mobiscore', 'url']
```

The program ends by displaying the total runtime to fetch the data.

```
==============⏰ Total web scraping is 8.4e+03 seconds=============
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
    - **For future improvement** Use a script to automatically create these links by decoding the search filters from the `base64`.
