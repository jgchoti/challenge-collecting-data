import pandas as pd
import numpy as np
import os
from utils.config import ALL_KEYS


class Output:
    def __init__(self):
        self.base_name = "properties"
        self.columns = ["zimmo code"] + ALL_KEYS
        
    def get_filename(self):
        path = os.path.abspath("")
        data_path = os.path.join(path, "data")
        os.makedirs(data_path, exist_ok=True)
        index = 1
        while True:
            access_file = os.path.join(data_path, f"{self.base_name}{index}.csv")
            if not os.path.exists(access_file):
                return access_file
            index += 1

    def save_to_csv(self, data, overwrite=False):
        df = pd.DataFrame.from_dict(data, orient="index")
        
        path = os.path.abspath("")
        access_file = self.get_filename()
        
        os.makedirs(os.path.dirname(access_file), exist_ok=True)

        # df["year built"] = pd.to_numeric(df["year built"], errors="coerce").astype(
        #     "Int64"
        # )
        for col in self.columns[1:]:  
            if col not in df.columns:
                df[col] = pd.NA
        df = df[self.columns[1:]] 
        df.index.name = "zimmo code" 
        
        if overwrite:
            df.to_csv(access_file, index=True)
        else:
            df.to_csv(access_file, mode="a", index=True, header=False)

    def read_csv(self):
        latest_filename = self.get_latest_filename()
        print(f"🔎 Preview data from {os.path.basename(latest_filename)}")
        df = pd.read_csv(latest_filename)
        
        if "year built" in df.columns:
            df["year built"] = pd.to_numeric(df["year built"], errors="coerce").astype("Int64")

        print(df.head())
        print(f"\n📊 Total properties in database: {len(df)}")
        print("📌 Columns:", list(df.columns))

    def output_info(self):
        latest_filename = self.get_latest_filename()
        df = pd.read_csv(latest_filename)
        print(f"\n📊 Total properties in database: {len(df)}")
        print("📌 Columns:", list(df.columns))
        
    def get_latest_filename(self):
        path = os.path.abspath("")
        data_folder = os.path.join(path, "data")
        filenames_list = os.listdir(data_folder)
        filenames_list.sort(key=os.path.getmtime)
        
        return filenames_list[-1]
