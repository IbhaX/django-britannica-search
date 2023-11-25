from requests import get
from bs4 import BeautifulSoup
from functools import lru_cache
from textwrap import shorten
import requests, os
from dotenv import load_dotenv

load_dotenv()


def detail(url, title):
    """ Get detailed query content """
    soup = BeautifulSoup(get(url).content, "html.parser")
    content = "n".join([i.text.strip() for i in soup.find_all("p", class_="topic-paragraph")])
    images = [i.a["href"] for i in soup.find_all("div", class_="card") if i.a["href"].startswith("http")]

    data = {
        "content": content,
        "summary": shorten(content, 300),
        "image": images[0] if images else get_image(title)
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
        result = {"title": k, **detail(v, k)}
        data.append(result)
    return data


def get_image(query, size="m"):
    sizes = {
        "original": "original",
        "xl": "large2x",
        "l": "large",
        "m": "medium",
        "s": "small",
        "portrait": "portrait",
        "landscape": "landscape",
        "t": "tiny",
    }
    headers = {
        "Authorization": os.getenv("PEXELS_API_KEY")
    }
    params = {
        "query": query,
        "page": 1,
        "per_page": 1
    }
    url = "https://api.pexels.com/v1/search"
    res = requests.get(url, headers=headers, params=params)
    
    if res.ok:
        res = res.json()["photos"][0]["src"][sizes[size]]
        return res
    


