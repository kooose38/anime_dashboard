import pandas as pd 
import numpy as np 
import requests 

def request_api(config) -> pd.DataFrame:
    df = pd.DataFrame(columns=["id", "year", "season", "title", "title_short1", "twitter_account", "public_url", "sex", "sequel"])
    for year in config["YEAR"]:
        for season in [1, 2, 3, 4]:
            res = requests.get(config["ROOT_URL"] + str(year) + "/" + str(season))
            for r in res.json():
                df = df.append(
                        {
                            "id": r["id"], 
                            "year": year, 
                            "season": season, 
                            "title": r["title"], 
                            "title_short1": r["title_short1"], 
                            "twitter_account": r["twitter_account"], 
                            "public_url": r["public_url"], 
                            "sex": r["sex"], 
                            "sequel": r["sequel"]
                        }, 
                        ignore_index=True
                )
        print(f"complete {year} years\n")
        
    return df 