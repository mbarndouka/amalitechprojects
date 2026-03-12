import pandas as pd
import numpy as np
import os

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
    df = df.copy()
    
    df = df.drop(columns=DROP_COLS, errors='ignore')
    
    # Extract names from list of dictionaries
    df["belongs_to_collection"] = df["belongs_to_collection"].apply(extract_collection)
    df["genres"] = df["genres"].apply(extract_names)
    df["production_companies"] = df["production_companies"].apply(extract_names)
    df["production_countries"] = df["production_countries"].apply(extract_names)
    df["spoken_languages"] = df["spoken_languages"].apply(extract_names)
    
    # Inspect anomalies
    print(df["genres"].value_counts().head())
    
    # convert datatypes
    numeric_cols = ['budget', 'id', 'popularity']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    df["release_date"] = pd.to_datetime(df['release_date'])
    
    # Replace unrealistic values with NaN
    df["budget"] = df["budget"].replace(0, np.nan)
    df["revenue"] = df["revenue"].replace(0, np.nan)
    df["runtime"] = df["runtime"].replace(0, np.nan)
    
    # convert budget and revenue to millions
    df["budget_musd"] = df["budget"] / 1_000_000
    df["revenue_musd"] = df["revenue"] / 1_000_000
    
    df.drop(columns=["budget", "revenue"], inplace=True)
    
    # handles anomalies in the data
    df.loc[df["vote_count"] == 0, "vote_count"] = np.nan

    df["overview"] = df["overview"].replace("", np.nan)
    df["tagline"] = df["tagline"].replace("", np.nan)
    
    df = df.drop(columns=["origin_country"], errors='ignore')
    #remove duplicates
    df = df.drop_duplicates()
    
    #remove rows with unknown id or title
    df = df.dropna(subset=["id", "title"])
    
    # Keep only rows where at least 10 columns have non-NaN values
    df = df[df.count(axis=1) >= 10]
    
    # filter released movies
    if "status" in df.columns:
        df = df[df["status"] == "Released"]
        df = df.drop(columns=["status"])
    
    # Reorder columns
    existing_cols = [col for col in FINAL_COLUMNS if col in df.columns]
    df = df.reindex(columns=existing_cols)

    # Reset index
    df = df.reset_index(drop=True)
    
    # save cleaned DataFrame
    os.makedirs(os.path.dirname(PROCESS_DATA_PATH), exist_ok=True)
    df.to_parquet(PROCESS_DATA_PATH, index=False)

    return df