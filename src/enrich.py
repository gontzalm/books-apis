from dotenv import load_dotenv
import numpy as np
import os
import pandas as pd
import requests

load_dotenv()
APIKEY = os.getenv("APIKEY") # api key neccessary for goodreads API

def parse_oreilly(res):
    """
    Parse a response returned by the O'Reilly Platform Search API.

    Args:
        res (requests.models.Response): Response to parse.

    Returns:
        data (pandas.DataFrame): Parsed data.
    """
    # Create DataFrame from HTTP response
    res = res.json()
    data = pd.DataFrame(res["results"]).set_index("isbn").drop(columns="id")

    # Fix DataFrame 
    data.index.name = "ISBN"
    data.columns = ["Authors", "Language Code", "Title", "Num Pages"]
    data["Authors"] = data["Authors"].str.join(", ")
    data["Language Code"] = data["Language Code"].replace("en", "eng")
    data["Num Pages"] = data["Num Pages"].astype(int)

    # Fill missing columns to avoid NaNs when appending to original DataFrame
    for col in ["Average Rating", "Ratings Count", "Text Reviews Count"]:
        data[col] = 0

    return data


def add_by_title(data, containing, limit=200):
    """
    Add books by title from the O'Reilly Platform Search API.

    Args:
        data (DataFrame): Dataset containing the books data.
        containing (str): Books whose title contains this string will be added to the data.

    Returns:
        data (DataFrame): Updated dataset.
    """
    # API setup
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

    # Perform HTTP GET for the first page
    res = requests.get(f"{base_url}{endpoint}", params=params)
    if res.status_code != 200:
        raise Exception("HTTP GET to O'Reilly Platform Search API failed.")

    # Parse and append first page
    data = data.append(parse_oreilly(res), sort=True)

    # Parse and append extra pages if they exist
    num_pages = res.json()["total"] // limit
    for i in range(num_pages):
        params["page"] = i + 1
        res = requests.get(f"{base_url}{endpoint}", params=params)
        if res.status_code != 200:
            raise Exception("HTTP GET to O'Reilly Platform Search API failed.")
        data = data.append(parse_oreilly(res), sort=True)

    # Drop duplicate books
    data.drop_duplicates(inplace=True)

    # Sort columns
    data = data[data.columns]

    return data


def add_review_stats(data):
    """
    Add review stats ("Average Rating", "Ratings Count" and "Text Reviews Count") from the Goodreads API.

    Args:
        data (DataFrame): Dataset containing the books data.

    Returns:
        data (DataFrame): Updated dataset.
    """
    # Search dataset for books with missing review stats
    isbns =data[data["Average Rating"] == 0].index.to_list()

    # API setup
    base_url = "https://www.goodreads.com"
    endpoint = "/book/review_counts"
    params = {
        "key": APIKEY,
        "isbns": isbns,
        "format": "json",
    }
    
    # Perform HTTP GET
    