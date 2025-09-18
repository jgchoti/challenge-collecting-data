# Belgium Real Estate Scraper

A Python project that scrapes real estate property listings from Zimmo.be to build a comprehensive dataset covering properties all over Belgium.

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.0+-FF6B35?style=for-the-badge&logo=python&logoColor=white)](https://www.crummy.com/software/BeautifulSoup/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Requests](https://img.shields.io/badge/Requests-2CA5E0?style=for-the-badge&logo=python&logoColor=white)](https://requests.readthedocs.io)
[![Threading](https://img.shields.io/badge/Multithreading-Enabled-green?style=for-the-badge)](https://docs.python.org/3/library/threading.html)

## The Story Behind This Project

### Because Data Patterns Tell the Real Story

A Python web scraper that systematically collects property listings from **Zimmo.be** to build comprehensive datasets covering the entire Belgian real estate landscape.

---

## Table of Contents

- [Belgium Real Estate Scraper](#belgium-real-estate-scraper)
  - [The Story Behind This Project](#the-story-behind-this-project)
    - [Because Data Patterns Tell the Real Story](#because-data-patterns-tell-the-real-story)
  - [Table of Contents](#table-of-contents)
  - [What Makes This Special](#what-makes-this-special)
  - [Technical Architecture](#technical-architecture)
  - [Features That Matter](#features-that-matter)
    - [Data Collection Capabilities](#data-collection-capabilities)
    - [Performance \& Reliability](#performance--reliability)
    - [Data Quality Assurance](#data-quality-assurance)
  - [Installation \& Setup](#installation--setup)
  - [Usage](#usage)
    - [Basic Execution](#basic-execution)
    - [Real-time Monitoring](#real-time-monitoring)
    - [Data Preview](#data-preview)
  - [Data Pipeline](#data-pipeline)
    - [Output Schema](#output-schema)
    - [Data Validation Pipeline](#data-validation-pipeline)
  - [Performance Optimizations](#performance-optimizations)
    - [Threading Architecture](#threading-architecture)
    - [Session Management](#session-management)
    - [Memory Optimization](#memory-optimization)
  - [Challenges \& Solutions](#challenges--solutions)
    - [Platform Limitations](#platform-limitations)
    - [Performance Bottlenecks](#performance-bottlenecks)
    - [Data Quality Issues](#data-quality-issues)
  - [Future Roadmap](#future-roadmap)
    - [Technical Enhancements](#technical-enhancements)

## What Makes This Special

**Scale That Delivers**: Successfully collected **25,000+ unique property listings** across all Belgian regions, creating one of the most comprehensive datasets available.

**Smart Problem Solving**: When Zimmo's 100-page limit threatened data completeness, implemented price range segmentation (€50k intervals) to capture the full market spectrum up to €1.5M+.

**Performance Engineering**: Migrated from Selenium to `requests.Session` + multithreading architecture, achieving **3x faster collection speeds** while maintaining data integrity.

**Production-Ready Data Quality**: Implements comprehensive deduplication, missing value handling, and data validation to ensure clean, analysis-ready outputs.

## Technical Architecture

```
Data Collection Pipeline:
├── Request Session Pool (threading)
├── Price Range Segmentation (€50k intervals)
├── Pagination Handler (100 pages max per range)
├── HTML Parser (BeautifulSoup4)
├── Data Normalizer & Validator
├── Deduplication Engine
└── CSV Export with Terminal Preview
```

**Core Technologies:**

- **Language**: Python 3.8+
- **HTTP Client**: `requests.Session` for connection pooling
- **HTML Parsing**: `BeautifulSoup4` for robust DOM extraction
- **Data Processing**: `pandas` for ETL operations
- **Concurrency**: Python `threading` for I/O parallelization
- **Data Validation**: Custom regex patterns for field standardization

## Features That Matter

### Data Collection Capabilities

- **Comprehensive Coverage**: Scrapes across all Belgian provinces and municipalities
- **Rich Attribute Extraction**: Captures 15+ property fields including type, price, dimensions, energy ratings, and location data
- **Smart Missing Value Handling**: Graceful degradation with `None` fills rather than failed records

### Performance & Reliability

- **Multithreaded Architecture**: Concurrent request processing for optimal throughput
- **Pagination Mastery**: Handles Zimmo's complex pagination system with automatic page discovery
- **Rate Limiting Respect**: Built-in delays to maintain server courtesy
- **Progress Monitoring**: Real-time collection statistics and completion estimates

### Data Quality Assurance

- **Automatic Deduplication**: Removes duplicate listings based on Zimmo codes
- **Data Type Validation**: Ensures numerical fields are properly typed
- **Export Flexibility**: CSV output with optional terminal data preview

## Installation & Setup

**Prerequisites**: Python 3.8+ with pip package manager

```bash
# Clone the repository
git clone https://github.com/jgchoti/challenge-collecting-data.git
cd challenge-collecting-data

# Install dependencies
pip install -r requirements.txt

# Verify installation
python --version  # Should show Python 3.8+
```

**Required Dependencies:**

```txt
requests>=2.28.0
beautifulsoup4>=4.11.0
pandas>=1.5.0
lxml>=4.9.0
```

## Usage

### Basic Execution

```bash
python main.py
```

### Real-time Monitoring

During execution, the scraper provides comprehensive progress tracking:

```
🔎 Done scraping listings in price range: 650000 - 699999 - Page: 57
🗃️ Total properties scraped so far: 20,772
🏷️ Done scraping listings in price range: 650000 - 699999
📈 Progress: 78% complete (13/18 price ranges)
⏱️ Estimated time remaining: 12 minutes
```

### Data Preview

The system offers optional terminal data preview:

```bash
📖 Do you want preview results? ('y' to confirm): y

🔎 Preview data from properties06181030.csv
  zimmo_code                    type    price  street  postcode      city  living_area
0      L9M5W           Chalet (Huis)  49000.0    ...      2275     Gierle         85.0
1      L9W3V           Woning (Huis)  40000.0    ...      3945  Ham-sur-Heure       120.0

✅ Total properties scraped: 25,403
📊 Data quality: 98.2% complete records
```

## Data Pipeline

### Output Schema

The scraper generates structured CSV files with standardized columns:

```csv
zimmo_code,type,price,street,number,postcode,city,province,living_area_m2,ground_area_m2,bedrooms,bathrooms,garage,garden,epc_kwh_m2,renovation_obligation,year_built,mobiscore,property_url
L9M5W,Chalet (Huis),49000.0,Patrijzenpad,,2275,Gierle,Antwerpen,85,2607,1,1,False,True,245,False,1986,5.9,/nl/gierle-2275/...
```

### Data Validation Pipeline

1. **Field Extraction**: HTML parsing with fallback handling
2. **Type Conversion**: String to numeric conversion with error handling
3. **Geographic Standardization**: Postcode validation and province mapping
4. **Deduplication**: Based on unique `zimmo_code` identifiers

## Performance Optimizations

### Threading Architecture

```python
# Concurrent request processing
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(scrape_price_range, range_params)
               for range_params in price_ranges]
```

### Session Management

```python
# Connection pooling for efficiency
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (compatible real estate research)'
})
```

### Memory Optimization

- **Streaming CSV writes** to handle large datasets
- **Batch processing** for memory-efficient data cleaning
- **Generator patterns** for lazy evaluation of large result sets

## Challenges & Solutions

### Platform Limitations

**Challenge**: Zimmo restricts queries to 100 pages maximum
**Solution**: Price range segmentation strategy covering €0-€1.5M+ in €50k intervals

**Challenge**: Anti-scraping measures on competing platforms
**Solution**: Strategic platform selection - Zimmo offered better accessibility than Immoweb

### Performance Bottlenecks

**Challenge**: Selenium webdriver causing slow collection speeds
**Solution**: Complete rewrite using `requests.Session` + threading, achieving 3x performance improvement

### Data Quality Issues

**Challenge**: Inconsistent missing value handling across different property types
**Solution**: Comprehensive null value standardization with `None` fills and data type validation

## Future Roadmap

### Technical Enhancements

- **Async Implementation**: Migrate to `asyncio` for even better concurrency performance
- **URL Pattern Analysis**: Reverse-engineer Zimmo's Base64 filter encoding for dynamic query generation
- **Database Integration**: PostgreSQL backend with spatial indexing for geographic queries

---

**Note**: This scraper is designed for research and analysis purposes. Please review Zimmo.be's robots.txt and terms of service before use, and implement appropriate rate limiting to be respectful of their infrastructure.
