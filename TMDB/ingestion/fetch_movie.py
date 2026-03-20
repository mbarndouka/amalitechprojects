import pandas as pd
from api.api import TMDB
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

movie_ids = [0, 299534, 19995, 140607, 299536, 597, 135397, 420818, 24428, 168259, 99861, 284054, 12445, 181808, 330457, 351286, 109445, 321612, 260513]

RAW_DATA_PATH = "data/raw/raw_movies.parquet"


def _normalize_movies(movies):
    """Normalize top-level keys while preserving nested payloads like credits."""
    if not movies:
        return pd.DataFrame()
    return pd.json_normalize(movies, max_level=0)

async def fetch_movie():
    """Fetch movies using async batch processing for better performance."""
    client = TMDB()

    # Small fixed input; modest concurrency is enough and friendlier to the API.
    movies = await client.get_movies_batch_async(movie_ids, max_concurrent=4)

    logging.info(f"Successfully fetched {len(movies)} out of {len(movie_ids)} movies")

    df = _normalize_movies(movies)
    os.makedirs(os.path.dirname(RAW_DATA_PATH), exist_ok=True)
    df.to_parquet(RAW_DATA_PATH, index=False)
    return df