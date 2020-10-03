from dotenv import load_dotenv
import numpy as np
import os
import pandas as pd
import requests


load_dotenv()
APIKEY = os.getenv("APIKEY") # api key neccessary for goodreads API
REVIEW_COLS = ["Average Rating", "Ratings Count", "Text Reviews Count"]
REVIEW_COLS_SNAKE = [
    "_".join([s.lower() for s in col.split(" ")]) for col in REVIEW_COLS
]

def parse_oreilly(res):
    """
    Parse a response returned by the O'Reilly Platform Search API.

    Args:
        res (requests.models.Response): Response to parse.

    Returns:
        data (pd.DataFrame): Parsed data.
    """
    # Create DataFrame from HTTP response
    res = res.json()
    data = pd.DataFrame(res["results"])
    data = data.dropna(subset=["isbn"]).drop(columns="id")

    # Fix DataFrame
    data = data[data["isbn"].str.match(r"\d{13}")] # check valid ISBNs
    data.set_index("isbn", inplace=True)
    data.index = data.index.astype(int, copy=False)
    data.index.name = "ISBN"
    data.columns = ["Authors", "Language Code", "Title", "Num Pages"]
    data["Authors"] = data["Authors"].str.join(", ")
    data["Language Code"] = data["Language Code"].replace("en", "eng")
    data["Num Pages"] = data["Num Pages"].astype(int)

    # Fill missing columns to avoid NaNs when appending to original DataFrame
    for col in REVIEW_COLS:
        data[col] = 0

    return data


def add_by_title(data, containing, limit=200):
    """
    Add books by title from the O'Reilly Platform Search API.

    Args:
        data (pd.DataFrame): Dataset containing the books data.
        containing (str): Books whose title contains this word will be added to the data.

    Returns:
        data (pd.DataFrame): Updated dataset.
    """
    # API setup
    base_url = "https://learning.oreilly.com"
    endpoint = "/api/v2/search"
    params = {
    "query": {" AND ".join(containing.split(" "))},
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

    return data


def parse_stats(data, isbn, res):
    """
    Parse a response returned by the Goodreads API with the endpoint "/book/review_counts" and add the info to the corresponding book.

    Args:
        data (pd.DataFrame): Dataset containing the books data.   
        isbn (int): ISBN of the target book.
        res (requests.models.Response): Response to parse.

    Returns:
        None.
    """
    res = res.json()
    for col, col_snake in zip(REVIEW_COLS, REVIEW_COLS_SNAKE):
        data.loc[isbn, col] = res["books"][0][col_snake]


def add_review_stats(data):
    """
    Add review stats ("Average Rating", "Ratings Count" and "Text Reviews Count") from the Goodreads API.

    Args:
        data (pd.DataFrame): Dataset containing the books data.

    Returns:
        None.
    """
    # Search dataset for books with missing review stats
    mask = (data[REVIEW_COLS] == 0).all(axis="columns")
    isbns = data[mask].index.to_list()

    # API setup
    base_url = "https://www.goodreads.com"
    endpoint = "/book/review_counts"
    params = {
        "key": APIKEY,
        "format": "json",
    }
    
    # Perform HTTP GET for each ISBN
    for isbn in isbns:
        params["isbns"] = str(isbn)
        res = requests.get(f"{base_url}{endpoint}", params=params)
        if res.status_code == 404:
            # drop rows without review stats, for better summary statistics
            data.drop(index=isbn, inplace=True) 
            continue
        parse_stats(data, isbn, res)
