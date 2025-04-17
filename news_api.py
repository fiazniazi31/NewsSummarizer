import requests
import os
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_news(category="business", max_items=10):
    url = f"https://www.api.thefreenewsapi.com/api/news/v1"
    params = {
        "apiKey": NEWS_API_KEY,
        "category": category,
        "sort": "DESC",
        "language": "English",
        "sourceCountry": "UnitedStates",
        "max": max_items
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get("member", [])
