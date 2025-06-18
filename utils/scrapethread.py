import threading
from utils.scraper import Scraper
import pandas as pd
class ScrapeThread(threading.Thread):
    def __init__(self, url, results, lock):
        super().__init__()
        self.url = url
        self.results = results
        self.lock = lock

    def run(self):
        scraper = Scraper()
        soup = scraper.scrape_property(self.url)
        results = scraper.process_soup(soup, self.url)
        if results is not None:
            zimmo_code, data = results
            if zimmo_code is not None and data is not None:
                with self.lock:
                    self.results[zimmo_code] = data
