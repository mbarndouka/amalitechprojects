import pandas as pd
from api import TMDB
from dotenv import load_dotenv
import os
import time

load_dotenv()
token = os.getenv("access_token")

movie_ids = [0, 299534, 19995, 140607, 299536, 597, 135397, 420818, 24428, 168259, 99861, 284054, 12445, 181808, 330457, 351286, 109445, 321612, 260513]

RAW_DATA_PATH = "data/raw/raw_movies.parquet"

def fetch_movie():
    client = TMDB(token)
    movies = []
    for movie_id in movie_ids:
        try:
            movie = client.get_movies(movie_id)
            # insert time delay here if needed to avoid hitting rate limits
            time.sleep(0.2)
            movies.append(movie)
        except Exception as e:
            print(f"Error fetching movie with ID {movie_id}: {e}")
    
    df = pd.DataFrame(movies)
    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
    # save dataFrame
    df.to_parquet(RAW_DATA_PATH, index=False)
    return df