import logging
import os

import numpy as np
import pandas as pd

# Set up logging for this module
logger = logging.getLogger(__name__)

DROP_COLS = [
    "adult",
    "imdb_id",
    "original_title",
    "video",
    "homepage"
]

FINAL_COLUMNS = ['id', 'title', 'tagline', 'release_date', 'genres', 'belongs_to_collection', 'original_language', 'budget_musd', 'revenue_musd', 'production_companies', 'production_countries', 'vote_count', 'vote_average', 'popularity', 'runtime', 'overview', 'spoken_languages', 'poster_path', 'cast', 'cast_size', 'director', 'crew_size'
]

PROCESS_DATA_PATH = "data/processed/clean_movies.parquet"


def _extract_credits_fields(credits):
    if not isinstance(credits, dict):
        return pd.Series({
            "cast": np.nan,
            "cast_size": np.nan,
            "director": np.nan,
            "crew_size": np.nan,
        })

    cast = credits.get("cast") if isinstance(credits.get("cast"), list) else []
    crew = credits.get("crew") if isinstance(credits.get("crew"), list) else []

    cast_names = [member.get("name") for member in cast if isinstance(member, dict) and member.get("name")]
    director = next(
        (
            member.get("name")
            for member in crew
            if isinstance(member, dict) and member.get("job") == "Director" and member.get("name")
        ),
        np.nan,
    )

    return pd.Series({
        "cast": "|".join(cast_names) if cast_names else np.nan,
        "cast_size": len(cast),
        "director": director,
        "crew_size": len(crew),
    })

def extract_names(item):
    if isinstance(item, list) and len(item) > 0:
        return "|".join([i['name'] for i in item])
    return np.nan

def extract_collection(item):
    if isinstance(item, dict):
        return item.get('name')
    return np.nan

# Drop irrelevant columns
def clean_movies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the raw movies DataFrame by:
    - Dropping irrelevant columns
    - Extracting relevant information from nested structures (e.g. genres, credits)
    - Converting datatypes and handling anomalies
    - Removing duplicates and rows with insufficient data
    - Filtering to only include released movies
    - Reordering columns to a consistent schema
    """
    logger.info("Starting data cleaning process...")
    df = df.copy()
    
    initial_rows = len(df)
    df = df.drop(columns=DROP_COLS, errors='ignore')
    
    # Extract names from list/dict payloads where available.
    if "belongs_to_collection" in df.columns:
        df["belongs_to_collection"] = df["belongs_to_collection"].apply(extract_collection)
    if "genres" in df.columns:
        df["genres"] = df["genres"].apply(extract_names)
    if "production_companies" in df.columns:
        df["production_companies"] = df["production_companies"].apply(extract_names)
    if "production_countries" in df.columns:
        df["production_countries"] = df["production_countries"].apply(extract_names)
    if "spoken_languages" in df.columns:
        df["spoken_languages"] = df["spoken_languages"].apply(extract_names)

    if "credits" in df.columns:
        credit_fields = df["credits"].apply(_extract_credits_fields)
        df[["cast", "cast_size", "director", "crew_size"]] = credit_fields
    
    # convert datatypes
    numeric_cols = ['budget', 'id', 'popularity']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
    if "release_date" in df.columns:
        df["release_date"] = pd.to_datetime(df['release_date'], errors="coerce")
    
    # Replace unrealistic values with NaN
    if "budget" in df.columns:
        df["budget"] = df["budget"].replace(0, np.nan)
    if "revenue" in df.columns:
        df["revenue"] = df["revenue"].replace(0, np.nan)
    if "runtime" in df.columns:
        df["runtime"] = df["runtime"].replace(0, np.nan)
    
    # convert budget and revenue to millions
    df["budget_musd"] = df["budget"] / 1_000_000 if "budget" in df.columns else np.nan
    df["revenue_musd"] = df["revenue"] / 1_000_000 if "revenue" in df.columns else np.nan
    
    df.drop(columns=["budget", "revenue"], inplace=True, errors="ignore")
    
    # handles anomalies in the data
    if "vote_count" in df.columns:
        df.loc[df["vote_count"] == 0, "vote_count"] = np.nan

    if "overview" in df.columns:
        df["overview"] = df["overview"].replace("", np.nan)
    if "tagline" in df.columns:
        df["tagline"] = df["tagline"].replace("", np.nan)
    
    df = df.drop(columns=["origin_country"], errors='ignore')
    # Remove duplicates in a hash-safe way even when rows contain nested lists/dicts.
    df = df.loc[~df.astype(str).duplicated()]
    
    #remove rows with unknown id or title
    required_identity_cols = [col for col in ["id", "title"] if col in df.columns]
    if required_identity_cols:
        before_drop = len(df)
        df = df.dropna(subset=required_identity_cols)
        dropped = before_drop - len(df)
        if dropped > 0:
            logger.warning(f"Dropped {dropped} rows due to missing id/title")

    # Keep rows with sufficient populated values relative to available schema.
    if len(df.columns) >= 10:
        df = df[df.count(axis=1) >= 10]
    
    # filter released movies
    if "status" in df.columns:
        df = df[df["status"] == "Released"]
        logger.info(f"Filtered for Released movies only. Rows remaining: {len(df)}")
        df = df.drop(columns=["status"])
    
    # Reorder columns
    df = df.reindex(columns=FINAL_COLUMNS)

    # Reset index
    df = df.reset_index(drop=True)
    
    # save cleaned DataFrame
    os.makedirs(os.path.dirname(PROCESS_DATA_PATH), exist_ok=True)
    df.to_parquet(PROCESS_DATA_PATH, index=False)
    logger.info(f"Cleaning complete. Processed {len(df)} movies (from initial {initial_rows}). Saved to {PROCESS_DATA_PATH}")

    return df