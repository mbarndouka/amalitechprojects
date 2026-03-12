import os
import matplotlib.pyplot as plt
import pandas as pd

FIGURE_DIR = "reports/figures"

def _ensure_dir():
    os.makedirs(FIGURE_DIR, exist_ok=True)

# ROI Distribution by Genre
def plot_roi_by_genre(df: pd.DataFrame):

    _ensure_dir()

    df = df.dropna(subset=["roi", "genres"])

    df = df.assign(genre=df["genres"].str.split("|")).explode("genre")

    genre_roi = df.groupby("genre")["roi"].median().sort_values(ascending=False)

    plt.figure(figsize=(12, 6))
    genre_roi.plot(kind="bar")

    plt.title("Median ROI by Genre")
    plt.ylabel("ROI")
    plt.xlabel("Genre")

    plt.xticks(rotation=45)
    plt.grid(axis="y")

    plt.savefig(f"{FIGURE_DIR}/roi_by_genre.png", bbox_inches="tight")
    plt.close()
    
# Revenue vs budget
def plot_revenue_vs_budget(df):
    _ensure_dir()
    df = df.dropna(subset=["budget_musd", "revenue_musd"])
    plt.figure(figsize=(10, 6))
    plt.scatter(df["budget_musd"], df["revenue_musd"], alpha=0.6)
    plt.xlabel("Budget (Millions USD)")
    plt.ylabel("Revenue (Millions USD)")
    plt.title("Revenue vs Budget")
    
    plt.grid(True)
    
    plt.savefig(os.path.join(FIGURE_DIR, "revenue_vs_budget.png"), bbox_inches="tight")
    plt.close()
    
    # ROI Distribution by genre
    
    def plot_roi_by_genre(df):
        _ensure_dir()
        df = df.dropna(subset=["roi", "genres"])
        
        df = df.assign(genre=df["genres"].str.split("|").explode("genre"))
        
        genre_roi = df.groupby("genre")["roi"].median().sort_values(ascending=False)
        plt.figure(figsize=(12, 6))
        genre_roi.plot(kind="bar")
        
        plt.title("Median ROI by Genre")
        plt.ylabel("ROI")
        plt.xlabel("Genre")
        
        plt.xticks(rotation=45)
        plt.grid(axis="y")
        
        plt.savefig(os.path.join(FIGURE_DIR, "roi_by_genre.png"), bbox_inches="tight")
        plt.close()
        
# Popularity vs rating
def plot_popularity_vs_rating(df):
    _ensure_dir()
    df = df.dropna(subset=["popularity", "vote_average"])
    
    plt.figure(figsize=(10, 6))
    
    plt.scatter(df["popularity"], df["vote_average"], alpha=0.6)
    
    plt.xlabel("Rating")
    plt.ylabel("Popularity")
    plt.title("Popularity vs Rating")
    
    plt.grid(True)
    
    plt.savefig(os.path.join(FIGURE_DIR, "popularity_vs_rating.png"), bbox_inches="tight")
    plt.close()
    
# Yearly Box Office Trends
def plot_yearly_revenue_trends(df):
    _ensure_dir()
    df = df.dropna(subset=["release_date", "revenue_musd"])
    
    df["year"] = pd.to_datetime(df["release_date"]).dt.year
    yearly_revenue = df.groupby("year")["revenue_musd"].sum()
    
    plt.figure(figsize=(12, 6))
    yearly_revenue.plot()
    
    plt.title("Yearly Box Office Revenue Trends")
    plt.xlabel("Year")
    plt.ylabel("Total Revenue (Millions USD)")
    
    plt.grid(True)
    
    plt.savefig(os.path.join(FIGURE_DIR, "yearly_revenue_trends.png"), bbox_inches="tight")
    plt.close()
    
# Franchise vs standalone performance 

def plot_franchise_vs_standalone(df):
    _ensure_dir()
    df = df.copy()
    df["franchise"] = df["belongs_to_collection"].notna()
    
    comparison = df.groupby("franchise").agg(
        mean_revenue=("revenue_musd", "mean"),
        mean_roi=("roi", "mean"),
        mean_popularity=("popularity", "mean"),
        mean_rating=("vote_average", "mean")
    )
    
    comparison.plot(kind="bar", figsize=(12, 6))
    
    plt.title("Franchise vs Standalone Performance")
    plt.xlabel("Franchise")
    plt.ylabel("Metric Value")
    
    plt.grid(axis="y")
    
    plt.savefig(os.path.join(FIGURE_DIR, "franchise_vs_standalone.png"), bbox_inches="tight")
    plt.close()
