import pandas as pd
import numpy as np
import re

def compute_profit(df):
    df = df.copy()
    df["profit_musd"] = df["revenue_musd"] -df["budget_musd"]
    
    df["roi"] = df["profit_musd"] / df["budget_musd"]
    # Keep ROI only when the production budget is at least $10M.
    df.loc[df["budget_musd"] < 10, "roi"] = np.nan
    return df

def rank_movies(df, column: str, top_n=10, ascending=False):
    df = df.copy()
    if ascending:
        return df.nsmallest(top_n, columns=column)
    return df.nlargest(top_n, columns=column)

def filter_votes(df, min_votes=10):
    df = df.copy()
    return df[df["vote_count"] >= min_votes]

# specific KPIs

def top_revenue(df, top_n=10):
    return rank_movies(df, "revenue_musd", top_n=top_n)

def top_budget(df, top_n=10):
    return rank_movies(df, "budget_musd", top_n=top_n)

def top_profit(df, top_n=10):
    return rank_movies(df, "profit_musd", top_n=top_n)

def top_roi(df, top_n=10):
    return rank_movies(df, "roi", top_n=top_n)

def lowest_budget(df, top_n=10):
    return rank_movies(df, "budget_musd", top_n=top_n, ascending=True)

def top_voted(df, top_n=10):
    return rank_movies(df, "vote_count", top_n=top_n)

def highest_rated(df, top_n=10):
    return rank_movies(df, "vote_average", top_n=top_n, ascending=False)

def lowest_rated(df, top_n=10):
    return rank_movies(df, "vote_average", top_n=top_n, ascending=True)

def most_popular(df, top_n=10):
    return rank_movies(df, "popularity", top_n=top_n)


# Advanced Filtering Functions
def search_movies(df, genre=None, actors=None, director=None, sort_by="vote_average", ascending=False):
    """
    Generic search for movies.
    
    genre: string or list of genres (pipe-separated)
    actors: string or list of actors (must appear in 'cast' column)
    director: string
    sort_by: column to sort
    ascending: sort order
    """
    
    required_columns = {sort_by}
    if genre:
        required_columns.add("genres")
    if actors:
        required_columns.add("cast")
    if director:
        required_columns.add("director")

    missing_columns = [col for col in sorted(required_columns) if col not in df.columns]
    if missing_columns:
        raise ValueError(
            "search_movies requires missing columns: " + ", ".join(missing_columns)
        )

    df_filtered = df.copy()
    
    if genre:
        if isinstance(genre, str):
            genre = [genre]
        escaped_genres = [re.escape(g) for g in genre]
        genre_pattern = rf"(?:^|\|)(?:{'|'.join(escaped_genres)})(?:\||$)"
        df_filtered = df_filtered[
            df_filtered["genres"].str.contains(genre_pattern, na=False, regex=True)
        ]
        
    if actors:
        if isinstance(actors, str):
            actors = [actors]
        escaped_actors = [re.escape(a) for a in actors]
        actor_pattern = rf"(?:^|\|)(?:{'|'.join(escaped_actors)})(?:\||$)"
        df_filtered = df_filtered[
            df_filtered["cast"].str.contains(actor_pattern, na=False, regex=True)
        ]
        
    if director:
        escaped_director = re.escape(director)
        df_filtered = df_filtered[
            df_filtered["director"].str.contains(escaped_director, na=False, regex=True)
        ]

    return df_filtered.sort_values(by=sort_by, ascending=ascending)

# Franchise vs Standalone Analysis

def franchise_vs_standalone(df):
    df = df.copy()
    df["franchise"] = df["belongs_to_collection"].notna()
    stats = df.groupby("franchise").agg(
        mean_revenue=("revenue_musd", "mean"),
        median_roi=("roi", "median"),
        mean_budget=("budget_musd", "mean"),
        mean_rating=("vote_average", "mean"),
        count_movies=("id", "count")
    ).reset_index()
    return stats

# Most Successful Franchises
def top_franchises(df, top_n=10):
    df = df.copy()
    df["franchise"] = df["belongs_to_collection"].notna()
    return df[df["franchise"]].groupby("belongs_to_collection").agg(
        total_movies=("id", "count"),
        total_budget=("budget_musd", "sum"),
        mean_budget=("budget_musd", "mean"),
        total_revenue=("revenue_musd", "sum"),
        mean_revenue=("revenue_musd", "mean"),
        mean_rating=("vote_average", "mean")
    ).sort_values(by="total_revenue", ascending=False).head(top_n)
    
