from dotenv import load_dotenv
import os
import pandas as pd
import requests

load_dotenv()
APIKEY = os.getenv("APIKEY") # api key neccessary for goodreads API

def parse_oreilly_page(res):
    res = res.json()
    data = pd.DataFrame(res["results"]).set_index("isbn").drop(columns="id")
    data.columns = ["Authors", "Language Code", "Title", "Num Pages"]
    data["Language Code"] = data["Language Code"].replace("en", "eng")
    return data


def add_by_title(data, containing, limit=200):
    """
    Add books by title.

    Args:
        data (DataFrame): DataFrame containing the book data.
        containing (str): Books whose title contains this string will be added to the data.

    Returns:
        None.
    """
    # Perform HTTP GET for first page
    base_url = "https://learning.oreilly.com"
    endpoint = "/api/v2/search"
    params = {
    "query": {containing},
    "field": "title", 
    "formats": "book",
    "page": 0,
    "limit": limit,
    "fields": ["isbn", "title", "authors", "language", "virtual_pages"]
    }
    res = requests.get(f"{base_url}{endpoint}", params=params)
    if res.status_code != 200:
        raise Exception("HTTP GET to O'Reilly Search API failed.")

    # Parse and append first page
    parse_oreilly_page(res)]

    # Parse extra pages if they exist
    num_pages = res["total"] // limit
    for i in range(num_pages):
        params["page"] = i + 1
        res = requests.get(f"{base_url}{endpoint}", params=params)
        df_list.append(parse_oreilly_page(res))

        
