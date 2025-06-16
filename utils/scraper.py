import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

class Scraper:
    def __init__(self, page: int = 1):
        self.page = page
        self.base_url = "https://www.zimmo.be/nl/zoeken/?search=eyJmaWx0ZXIiOnsic3RhdHVzIjp7ImluIjpbIkZPUl9TQUxFIiwiVEFLRV9PVkVSIl19LCJ6aW1tb0NvZGUiOnsibm90SW4iOlsiTDRNVVYiLCJMOUY4SCIsIjEwMDRPMDQiLCJLWVFQMSJdfX0sInBhZ2luZyI6eyJmcm9tIjowLCJzaXplIjoxN30sInNvcnRpbmciOlt7InR5cGUiOiJSQU5LSU5HX1NDT1JFIiwib3JkZXIiOiJERVNDIn1dfQ%3D%3D"
        self.session = requests.Session()
        self.properties_data = {}
        self.page_urls = []
        
    def close(self):
        self.session.close()
            
    def open_page(self, url):
        if not url:
            url = self.base_url
        response = self.session.get(url, headers = {'User-Agent': 'Popular browser\'s user-agent',})
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    
    def update_page_number(self, page_number):
        if page_number == 1:
            return self.base_url
        else:
            return f"{self.base_url}&p={page_number}"


    def get_links(self, soup):
        properties = soup.find_all("div", class_="property-item")
        properties_url = []
        for listing in properties:
            a_elem = listing.find("a", href=True)
            if a_elem and a_elem.get('href'):
                properties_url.append(a_elem['href'])
        return properties_url
    
    def scrape_property(self, link, id_property):
        full_link = urljoin("https://www.zimmo.be", link)
        response = self.session.get(full_link, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)","Accept-Language": "en-US,en;q=0.9"})
        print(full_link)
        if response.status_code != 200:
            print(f"❌ Failed to fetch {id_property}")
            return None
        soup = BeautifulSoup(response.text, "html.parser")
        
        # get address
        h2_elem = soup.find("h2", class_ = "section-title")
        full_address_elem = h2_elem.find("span") if h2_elem else None
        full_address = full_address_elem.get_text() if full_address_elem else None
        cleaned_full_address = self.clean_address(full_address) if full_address else None
        
        # get price
        
        # get type
        
        # Living area.
        
        # Ground area.
        
        # get no. bedroom
        
        # get no. bathrooms
        
        # get no. toliets
        
        # get no. parking spaces
        
        # mobi score
        
        
        # Garden
        
        # EPC value
        
        # Renovation year
        
        
        
        
        
        data = {
                "street": cleaned_full_address.get("street", ""),
                "number": cleaned_full_address.get("number", ""),
                "postcode": cleaned_full_address.get("postcode", ""),
                "city": cleaned_full_address.get("city", ""),
                "url": full_link
            }
        
        return data
            
    def clean_address(self, full_address):
        cleaned = re.sub(r"\n+|\s+", " ", full_address).strip()
        street_part, city_part = cleaned.split(",", 1)
        street_parts = street_part.strip().split()
        street_name_parts = []
        number_parts = []
        for i, part in enumerate(street_parts):
            if re.search(r'\d', part):
                street_name_parts = street_parts[:i]
                number_parts = street_parts[i:]
                break
            else:
                street_name_parts = street_parts
                number_parts = []

        street_name = " ".join(street_name_parts).strip() if street_name_parts else None
        number = " ".join(number_parts).strip() if number_parts else None
        postcode, city = city_part.strip().split(" ", 1)
        if street_name == "Straat niet gekend":
            street_name = None
        return {
            "street": street_name,
            "number": number,
            "postcode": postcode,
            "city": city
        }
    
    