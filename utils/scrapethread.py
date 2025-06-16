import threading
from utils.scraper import Scraper

class ScrapeThread(threading.Thread):
    def __init__(self, url, results, id_counter, lock):
        super().__init__()
        self.url = url
        self.results = results
        self.id_counter = id_counter
        self.lock = lock

    def run(self):
        local_scraper = Scraper()
        with self.lock:
            id_property = next(self.id_counter)
        data = local_scraper.scrape_property(self.url, id_property)
        with self.lock:
            self.results[id_property] = data
