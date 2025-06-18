import threading
from utils.scraper import Scraper
from utils.scrapethread import ScrapeThread
from utils.output import Output
import time
from datetime import datetime
from utils.config import BASE_URL

def get_properties_each_page(properties_url):
    threads = []
    results = {}
    lock = threading.Lock()

    for url in properties_url:
        thread = ScrapeThread(url, results, lock)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return results

def scrap_price_ranges(scraper, output, filename):
    first_write = True
    for key, val in BASE_URL.items():
        page = 1
        while True:
            
            current_url = scraper.update_page_number(page, val)
            soup = scraper.open_page(current_url)
            if not soup:
                break
            
            properties_url = scraper.get_links(soup)
            
            if not properties_url:
                print(f"🏷️ Done scraping listings in price range :{key}")
                break
            
            results = get_properties_each_page(properties_url)
            output.save_to_csv(filename,results, overwrite=first_write)
            first_write = False
            
            scraper.properties_data.update(results)
            print(f"\n🔎 Done scraping listings in price range:{key} - Page: {page}")
            print(f"🗃️ Total properties scraped so far: {len(scraper.properties_data)}")
            page += 1

def main():
    print("\n🔍 Getting data...")
    date = datetime.now()
    fd = date.strftime("%m%d%I%M")
    filename = f"properties{fd}.csv"
    start = time.perf_counter()
    scraper = Scraper()
    output = Output()
    try: 
        scrap_price_ranges(scraper, output, filename)
    finally: 
        scraper.close()
    end = time.perf_counter()
    user_input = input(f"\n📖 Do you want preview results? ('y' to confirm):")
    if user_input.lower() == "y":
        output.read_csv()

    output.output_info()
    print(
        f"==============⏰ Total webs scraping is {end-start:.2} seconds=============\n"
    )

if __name__ == "__main__":
    main()
