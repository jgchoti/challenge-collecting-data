class Retriever:
    def __init__(self, soup):
        self.soup = soup
    
    # get zimmo code
    def get_zimmo_code(self):
        zimmo_code_elem = self.soup.find("p", class_="zimmo-code")
        if zimmo_code_elem:
            return zimmo_code_elem.get_text()
        else:
            return None

    def get_feature_info(self):
        main_features_section = (self.soup.find("section", id="main-features") or 
                                 self.soup.find("div", class_="features-section") or 
                                 self.soup.find("ul", class_="main-features"))
        if not main_features_section:
            print("⚠️ Could not find 'main-features'")
            return None
 
        if main_features_section:
            li_list = main_features_section.find_all("li")
            feature = {}
            for li in li_list:
                label = li.find("strong", class_="feature-label")
                value = li.find("span", class_="feature-value")
                if label:
                    key = label.text.strip().lower()
                    val = value.text.strip() if value else None
                    feature[key] = val
            return feature
        else:
            return None
   
    def get_mobiscore(self):
        mobiscore_elem = (self.soup.find("span", class_="section-mobiscore_total-score"))
        if mobiscore_elem:
            return mobiscore_elem.get_text()
        else:
            return None
    
