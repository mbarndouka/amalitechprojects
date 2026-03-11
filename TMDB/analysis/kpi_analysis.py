import pandas as pd
import numpy as np

def compute_profit(df):
    df = df.copy()
    df["profit_musd"] = df["revenue_musd"] -df["budget_musd"]
    
    df["roi"] = df["profit_musd"] / df["budget_musd"]
    # Only budget over 10M
    df.loc[df["roi"] < 10, "roi"] = np.nan
    return df

def rank_movies(df, column: str, top_n=10, ascending=False):
    df = df.copy()
    return df.sort_values(by=column, ascending=ascending).head(top_n)

def filter_votes(df, min_votes=10):
    df = df.copy()
    return df[df["vote_count"] >= min_votes]

# specific KPIs

def top_revenue(df, top_n=10):
    return rank_movies(df, "revenue_musd", top=top_n)

def top_budget(df, top_n=10):
    return rank_movies(df, "budget_musd", top=top_n)

def top_profit(df, top_n=10):
    return rank_movies(df, "profit_musd", top=top_n)

def top_roi(df, top_n=10):
    return rank_movies(df, "roi", top=top_n)

def lowest_budget(df, top_n=10):
    return rank_movies(df, "budget_musd", top=top_n, ascending=True)

def top_voted(df, top_n=10):
    return rank_movies(df, "vote_count", top=top_n)

def highest_rated(df, top_n=10):
    return rank_movies(df, "vote_average", top=top_n, ascending=True)

def lowest_rated(df, top_n=10):
    return rank_movies(df, "vote_average", top=top_n, ascending=True)

def most_popular(df, top_n=10):
    return rank_movies(df, "popularity", top=top_n)


# Advanced Filtering Functions
def search_movies(df, genre=None, actors=None, director=None, sort_by=" vote_average", ascending=False):
    """
    Generic search for movies.
    
    genre: string or list of genres (pipe-separated)
    actors: string or list of actors (must appear in 'cast' column)
    director: string
    sort_by: column to sort
    ascending: sort order
    """
    
    df_filtered = df.copy()
    
    if genre:
        if isinstance(genre, str):
            genre = [genre]
        # filter movies that contain any of the specified genres
        df_filtered = df_filtered[df_filtered["genres"].apply(lambda x: any(g in x.split("|") for g in genre) if pd.notna(x) else False)]
        
    if actors:
        if isinstance(actors, str):
            actors = [actors]
        # filter movies that contain any of the specified actors
        df_filtered = df_filtered[df_filtered["cast"].apply(lambda x: any(a in x for a in actors) if pd.notna(x) else False)]
        
    if director:
        df_filtered = df_filtered[df_filtered["director"].apply(lambda x: director in x if pd.notna(x) else False)]
        
    

# Best-rated Science Fiction Action movies starring Bruce Willis
# search1 = search_movies(df, genre=["Science Fiction", "Action"], actors="Bruce Willis", sort_by="vote_average", ascending=False)

# Movies starring Uma Thurman directed by Quentin Tarantino
# search2 = search_movies(df, actors="Uma Thurman", director="Quentin Tarantino", sort_by="runtime", ascending=True)

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
    
