import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
base_url = os.getenv("URL")
api_key = os.getenv("TMDB_API_KEY")
access_token = os.getenv("access_token")

class TMDB:
    def __init__(self, access_token):
        self.url = base_url
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {access_token}"
        }


    def get_movies(self, movie_ids):
        url = f"{self.url}/{{movie_id}}"
        response = requests.get(url, headers=self.headers)
        # Check if the request was successful
        response.raise_for_status()
        return response.json()        