import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import time
import random
from utils.cleaner import Cleaner
from utils.retriever import Retriever
from utils.config import ALL_KEYS
import random
import certifi
from http.client import RemoteDisconnected
from fake_useragent import UserAgent
class Scraper:
    def __init__(self, page: int = 1):
        self.page = page
        # self.base_url = 'https://www.immoweb.be/en/search/for-sale?countries=BE'
        self.session = requests.Session()
        self.properties_data = {}
        self.page_urls = []
        self.seen_url = set()
        
    def close(self):
        self.session.close()
        
    def get_user_agent(self):
        ua = UserAgent(platforms='desktop')
        return ua.random
        
    def open_page(self, url):
        try:
            headers = {
        'User-Agent': (
          self.get_user_agent()
        ),
        'Accept': (
            'text/html,application/xhtml+xml,application/xml;q=0.9,'
            'image/avif,image/webp,*/*;q=0.8'
        ),
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Connection': 'keep-alive',
        }
            response = self.session.get(url, headers=headers)
            time.sleep(random.uniform(1, 3))
            if response.status_code != 200:
                print(f"❌ Failed to reach {url}")
                return False
            else:
                print(f"✅ Accessed {url}")
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup
        except RemoteDisconnected:
            print(f"🔌 RemoteDisconnected: Server closed connection for {url}")
            return False
     
    def update_page_number(self, page_number, url):
        if page_number == 1:
            return url
        else:
            return f"{url}&p={page_number}"
            # return f"{self.base_url}&page={page_number}"
        
    def get_links(self, soup):
        properties_url = []
        properties = soup.find_all("div", class_="property-item")
        for listing in properties:
            a_elem = listing.find("a", href=True)
            if a_elem and a_elem.get('href'):
                properties_url.append(a_elem['href'])
        return properties_url
    
    def scrape_property(self, link):
        full_link = urljoin("https://www.zimmo.be", link)
        if full_link in self.seen_url:
            print(f"❌ Skipped {full_link} ")
            return
        
        self.seen_url.add(full_link )
        
        headers = {
            'User-Agent': (
            self.get_user_agent()
        ),
        'Accept': (
            'text/html,application/xhtml+xml,application/xml;q=0.9,'
            'image/avif,image/webp,*/*;q=0.8'
        ),
   "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Connection': 'keep-alive',

}
        response = self.session.get(full_link, headers = headers, verify=certifi.where())
        time.sleep(random.uniform(1, 3))
        
        if response.status_code != 200:
            print(f"❌ Failed to fetch {full_link }")
            return None
        
        soup = BeautifulSoup(response.content, "html.parser")
   
        time.sleep(random.uniform(1, 3))
        retrieve = Retriever(soup)
        
        # get zimmo code
        zimmo_code = retrieve.get_zimmo_code()
        cleaned_zimmo_code = Cleaner.clean_zimmo_code(zimmo_code) if zimmo_code else None

        feature = retrieve.get_feature_info()
        # print("Extracted keys from feature:", feature.keys())
        feature["prijs"] = Cleaner.cleaned_price(feature["prijs"]) if feature.get("prijs") else None
        address = Cleaner.clean_address(feature.get("adres")) if feature.get("adres") else {}
        feature["woonopp."] = Cleaner.remove_non_digits(feature["woonopp."]) if feature.get("woonopp.") else None
        feature["grondopp."] = Cleaner.remove_non_digits(feature["grondopp."]) if feature.get("grondopp.") else None
        feature["epc"]  = Cleaner.remove_non_digits(feature["epc"]) if feature.get("epc") else None
        feature['renovatieplicht'] = Cleaner.cleaned_renovation_obligation(feature['renovatieplicht']) if feature.get('renovatieplicht') else None
        feature['ki'] = Cleaner.cleaned_price(feature['ki']) if feature.get('ki') else None
        feature['bouwjaar'] = Cleaner.clean_year(feature['bouwjaar']) if feature.get('bouwjaar') else None
        
        mobiscore = retrieve.get_mobiscore() 

        data = {
            "type": feature.get("type"),
            "price": feature.get("prijs"),
            "street": address.get("street") if isinstance(address, dict) else None,
            "number": address.get("number") if isinstance(address, dict) else None,
            "postcode": address.get("postcode") if isinstance(address, dict) else None,
            "city": address.get("city") if isinstance(address, dict) else None,
            "living area(m²)": feature.get("woonopp."),
            "ground area(m²)": feature.get("grondopp."),
            "bedroom": feature.get("slaapkamers"),
            "bathroom": feature.get("badkamers"),
            "garage": feature.get("garages"),
            "garden": True if feature.get("tuin") else False,
            "EPC(kWh/m²)": feature.get("epc"),
            "renovation obligation": feature.get("renovatieplicht"),
            "year built" : feature.get('bouwjaar'),
            "mobiscore" : mobiscore, 
            "url": full_link,
        }
        
        for key in ALL_KEYS:
            data.setdefault(key, None)
        
        data = Cleaner.cleaned_data(data)
        return cleaned_zimmo_code, data