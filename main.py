import threading
from itertools import count
from utils.scraper import Scraper
from utils.scrapethread import ScrapeThread

def get_properties_each_page(properties_url, id_counter):
    threads = []
    results = {}
    lock = threading.Lock()

    for url in properties_url:
        t = ScrapeThread(url, results, id_counter, lock)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return results

def main():
   print("\n🔍 Getting data...")
   scraper = Scraper()
   id_counter = count(1)
   page = 1
   while True:
       current_url = scraper.update_page_number(page)
       soup = scraper.open_page(current_url)
       if not soup:
           break
       properties_url = scraper.get_links(soup)
       if not properties_url:
           print("No more properties found.")
           break
       
       results = get_properties_each_page(properties_url, id_counter)
       scraper.properties_data.update(results)
       print(f"✅ Page {page} done.")
       break
   scraper.close()
    #    page += 1

   print(scraper.properties_data)
   
if __name__ == "__main__":
    main()
