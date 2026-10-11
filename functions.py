import pandas as pd
import requests
import asyncio


# Loops through the file making an API request about each row.
def API_request_bulk(api_key,base_url,file):
    df = pd.read_csv(file)
    
    for i, row in df.iterrows():
        base_url = "https://opencellid.org/cell/get"
        response = requests.get(f"{base_url}?key={api_key}&mcc={row['mcc']}&mnc={row['mnc']}&lac={row['lac/tac']}&cellid={row['cellid']}&format=json")
        data = response.json()
        print(data)


def API_request_single(api_key,base_url,mcc,mnc,lac,cellid):
    base_url = "https://opencellid.org/cell/get"
    response = requests.get(f"{base_url}?key={api_key}&mcc={mcc}&mnc={mnc}&lac={lac}&cellid={cellid}&format=json")
    data = response.json()
    print(data)



