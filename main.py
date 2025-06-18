import threading
from utils.scraper import Scraper
from utils.scrapethread import ScrapeThread
from utils.output import Output
import time
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

def main():
    print("\n🔍 Getting data...")
    start = time.perf_counter()
    scraper = Scraper()
    output = Output()
    first_write = True
    
    for url in BASE_URL:
        page = 1
        while True:
            current_url = scraper.update_page_number(page, url)
            soup = scraper.open_page(current_url)
            if not soup:
                break
            
            properties_url = scraper.get_links(soup)
            
            if not properties_url:
                print("No more properties found. next main base url")
                break
            
            results = get_properties_each_page(properties_url)
            output.save_to_csv(results, overwrite=first_write)
            first_write = False
            
            scraper.properties_data.update(results)
            print(f"📦 Total properties scraped so far: {len(scraper.properties_data)}")
            
            page += 1

    scraper.close()
    end = time.perf_counter()
    user_input = input(f"\nDo you want preview results? ('y' to confirm):")
    if user_input.lower() == "y":
        output.read_csv()

    output.output_info()
    print(
        f"==============⏰ Total webs scraping is {end-start:.2} seconds=============\n"
    )

if __name__ == "__main__":
    main()
