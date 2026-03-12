import logging
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
base_url = os.getenv("URL")
api_key = os.getenv("API_KEY")


class TMDB:
    def __init__(self):
        self.url = base_url
        self.api_key = api_key
        if not api_key:
            raise ValueError("API key is required to access TMDB API.")
        if not base_url:
            raise ValueError("Base URL is required to access TMDB API.")


    def get_movies(self, movie_id):
        try:
            url = f"{self.url}/{movie_id}"
            params = {
                    "api_key": api_key,
                    "language": "en-US"
                    }
            response = requests.get(url, params=params)
            # Check if the request was successful
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Error fetching movie data for ID {movie_id}: {e}")
            return None
        