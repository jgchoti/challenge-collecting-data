import pandas as pd
import numpy as np
import os
from utils.config import ALL_KEYS
class Output:
    def __init__(self):
        self.columns = ["zimmo code"] + ALL_KEYS

    def save_to_csv(self, filename, data, overwrite=False):
        df = pd.DataFrame.from_dict(data, orient="index")
        path = os.path.abspath("")
        data_folder = os.path.join(path, "data")
        access_file = os.path.join(data_folder, filename)
    
        os.makedirs(os.path.dirname(access_file), exist_ok=True)
        for col in self.columns[1:]:  
            if col not in df.columns:
                df[col] = pd.NA
        df = df[self.columns[1:]] 
        df.index.name = "zimmo code" 
        
        if overwrite:
            df.to_csv(access_file, index=True)
        else:
            df.to_csv(access_file, mode="a", index=True, header=False)

    def read_csv(self, filename):
        path = os.path.abspath("")
        data_folder = os.path.join(path, "data")
        access_file = os.path.join(data_folder, filename)
        print(f"🔎 Preview data from {filename}")
        df = pd.read_csv(access_file)
        
        if "year built" in df.columns:
            df["year built"] = pd.to_numeric(df["year built"], errors="coerce").astype("Int64")

        print(df.head())

    def output_info(self,filename):
        path = os.path.abspath("")
        data_folder = os.path.join(path, "data")
        access_file = os.path.join(data_folder, filename)
        df = pd.read_csv(access_file)
        print(f"\n🏡 Zimmo.be scraping complete — total properties: {len(df)}")
        print("📌 Columns:", list(df.columns))
        
