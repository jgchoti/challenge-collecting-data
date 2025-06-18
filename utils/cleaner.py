import re

class Cleaner:
    @staticmethod
    def clean_address(full_address):
        cleaned = re.sub(r"\n+|\s+", " ", full_address).strip()
        street_part, city_part = cleaned.split(",", 1)
        street_parts = street_part.strip().split()
        street_name_parts = []
        number_parts = []
        for i, part in enumerate(street_parts):
            if re.search(r"\d", part):
                street_name_parts = street_parts[:i]
                number_parts = street_parts[i:]
                break
            else:
                street_name_parts = street_parts
                number_parts = []

        street_name = " ".join(street_name_parts).strip() if street_name_parts else None
        number = " ".join(number_parts).strip() if number_parts else None
        if number is not None:
            number = re.sub(r"\s", "", number)
        postcode, city = city_part.strip().split(" ", 1)
        if street_name == "Straat niet gekend":
            street_name = None
        return {
            "street": street_name,
            "number": number,
            "postcode": postcode,
            "city": city,
        }

    @staticmethod
    def clean_zimmo_code(code):
        cleaned = code.replace(r"Zimmo-code: ", "").strip()
        cleaned = re.sub(r"\s", "", cleaned)
        return cleaned

    @staticmethod
    def clean_text(text):
        cleaned = text.strip()
        return cleaned

    @staticmethod
    def remove_non_digits(text):
        cleaned = re.sub(r"[^0-9]", "", str(text))
        if cleaned == "":
            return None
        return int(cleaned)

    @staticmethod
    def cleaned_price(price):
        cleaned_price = re.sub(r"[€\.]", "", price)
        if cleaned_price.isdigit():
            cleaned_price = cleaned_price.replace(",", ".")
            return int(cleaned_price)
        else:
            return None

    @staticmethod
    def cleaned_renovation_obligation(text):
        return text.strip().lower() == "van toepassing"

    @staticmethod
    def cleaned_data(data):
        for key, value in data.items():
            if isinstance(value, str) and "op aanvraag »" in value:
                data[key] = None
        return data 
