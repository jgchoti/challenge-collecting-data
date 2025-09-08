import base64
import json
import urllib.parse

# encoded_value = base64.b64encode(json.dumps(data))
# url = "https://www.zimmo.be/nl/zoeken/?search=eyJmaWx0ZXIiOnsic3RhdHVzIjp7ImluIjpbIkZPUl9TQUxFIiwiVEFLRV9PVkVSIl19LCJjYXRlZ29yeSI6eyJpbiI6WyJIT1VTRSIsIkFQQVJUTUVOVCJdfX19"

search_q = "eyJmaWx0ZXIiOnsic3RhdHVzIjp7ImluIjpbIkZPUl9TQUxFIiwiVEFLRV9PVkVSIl19LCJjYXRlZ29yeSI6eyJpbiI6WyJIT1VTRSIsIkFQQVJUTUVOVCJdfX19"
decoded_url = urllib.parse.unquote(search_q)
decoded_base64 = base64.b64decode(decoded_url)
print(decoded_base64.decode())

# {"filter":{"status":{"in":["FOR_SALE","TAKE_OVER"]},"category":{"in":["HOUSE","APARTMENT"]}}}

def generate_zimmo_url(min_price, max_price=None, category_type = "HOUSE"):
    query = {
        "filter": {
            "status": {
                "in": ["FOR_SALE", "TAKE_OVER"]
            },
            "category": {
                "in": [category_type]
            },
            "price": {
                "unknown": False,
                "range": {
                    "min": min_price
                }
            }
        }
    }

    if max_price is not None:
        query["filter"]["price"]["range"]["max"] = max_price
    
    
    # Convert the query to Json
    json_query = json.dumps(query)
    # Encode the JSON string to bytes
    encode = json_query.encode()
    encoded_query = base64.b64encode(encode)
    # back to a string 
    url_query = encoded_query.decode()

    url = f"https://www.zimmo.be/nl/zoeken/?search={url_query}"
    return url


def generate_price_ranges_with_open_end(start, max_limit, step):
    current = start
    while current + step - 1 <= max_limit:
        yield (current, current + step - 1)
        current += step
    yield (max_limit + 1, None)

BASE_URL = {}
for min_p, max_p in generate_price_ranges_with_open_end(0, 1499999, 50000):
    url = generate_zimmo_url(min_p, max_p)
    BASE_URL[f"{min_p} - {max_p}"] = url
    if max_p is None:
        print(f"Price range {min_p} - no max: {url}")
    else:
        print(f"Price range {min_p} - {max_p}: {url}")
        
print(BASE_URL)

# import pandas as pd
# import os

# def modify_url(url):
#     if pd.isna(url):
#         return url
#     return f"https://www.zimmo.be{url}"

# def modify():
#     path = os.path.abspath("")
#     data_folder = os.path.join(path, "data")
#     access_file = os.path.join(data_folder, "properties.csv")

#     if not os.path.exists(access_file):
#         print("❌ File not found:", access_file)
#         return

#     df = pd.read_csv(access_file)
#     print(f"\n🏡 Total properties: {len(df)}")
#     print("📌 Columns:", list(df.columns))

  
    # df.columns = df.columns.str.strip().str.lower()
    # if "url" not in df.columns:
    #     print("❌ 'url' column not found after normalization")
    #     return

    # df["url"] = df["url"].apply(modify_url)
    # print(df["url"].head())

    # df.to_csv(os.path.join(data_folder, "properties_modified.csv"), index=True)
    # print("✅ Modified CSV saved.")

