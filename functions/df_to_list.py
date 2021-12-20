import json
import pandas as pd


def df_to_list(df):
    json = []
    for index, row in df.iterrows():
        temp = {}
        temp["id"] = index
        for col in df.columns:
            temp[col] = row[col]
        json.append(temp)
    return json
