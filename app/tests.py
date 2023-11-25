from requests import get
from bs4 import BeautifulSoup
from functools import lru_cache
from textwrap import shorten
from string import  ascii_letters
import json


def detail(url):
    """ Get detailed query content """
    soup = BeautifulSoup(get(url).content, "html.parser")
    content = "n".join([i.text.strip() for i in soup.find_all("p", class_="topic-paragraph")])
    images = [i.a["href"] for i in soup.find_all("div", class_="card") if i.a["href"].startswith("http")]

    data = {
        "content": content,
        "summary": shorten(content, 200),
        "images": images if images else None
    }
    return data

@lru_cache()
def search(query):
    """ function for searching and fetching query """
    url = f"https://www.britannica.com/search?query={'+'.join(query.split())}"
    base_url = "https://www.britannica.com"
    soup = BeautifulSoup(get(url).content, "html.parser")
    response = soup.find("div", class_="search-results")
    response = {i.a.text.strip(): base_url + i.a["href"] for \
                i in response.find_all("li")}  
    data = []
    for k,v in response.items():
        result = {"title": k, **detail(v)}
        data.append(result)
    return data


  
