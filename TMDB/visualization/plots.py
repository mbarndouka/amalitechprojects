import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Set seaborn theme for all plots
sns.set_theme(style="whitegrid", palette="muted")

FIGURE_DIR = "reports/figures"

def _ensure_dir():
    os.makedirs(FIGURE_DIR, exist_ok=True)

# ROI Distribution by Genre
def plot_roi_by_genre(df: pd.DataFrame):
    _ensure_dir()
    df = df.dropna(subset=["roi", "genres"])
    df = df.assign(genre=df["genres"].str.split("|")).explode("genre")

    genre_roi = df.groupby("genre")["roi"].median().sort_values(ascending=False).reset_index()

    plt.figure(figsize=(12, 6))
    sns.barplot(data=genre_roi, x="genre", y="roi", hue="genre", legend=False)

    plt.title("Median ROI by Genre", fontsize=14, fontweight='bold')
    plt.ylabel("Median ROI")
    plt.xlabel("Genre")

    plt.xticks(rotation=45)
    plt.show()

# Revenue vs budget
def plot_revenue_vs_budget(df):
    _ensure_dir()
    df = df.dropna(subset=["budget_musd", "revenue_musd", "popularity", "vote_average"])

    cmap = sns.cubehelix_palette(rot=-.2, as_cmap=True)

    g = sns.relplot(
        data=df,
        x="budget_musd", 
        y="revenue_musd", 
        hue="popularity", 
        size="vote_average",
        palette=cmap,
        sizes=(10, 200),
        height=7,
        aspect=1.2,
        alpha=0.8,
    )
    
    g.set(xscale="log", yscale="log")
    g.set_axis_labels("Budget (Millions USD, log)", "Revenue (Millions USD, log)")
    g.ax.xaxis.grid(True, "minor", linewidth=.25)
    g.ax.yaxis.grid(True, "minor", linewidth=.25)
    g.despine(left=True, bottom=True)

    plt.title("Revenue vs Budget (Log Scale)", fontsize=14, fontweight='bold', pad=20)
    plt.show()

# Popularity vs rating
def plot_popularity_vs_rating(df):
    _ensure_dir()
    df = df.dropna(subset=["popularity", "vote_average", "revenue_musd", "budget_musd"])

    cmap = sns.cubehelix_palette(start=2, rot=0, dark=0.2, light=0.8, reverse=True, as_cmap=True)

    g = sns.relplot(
        data=df,
        x="popularity", 
        y="vote_average", 
        hue="revenue_musd",
        size="budget_musd",
        palette=cmap,
        sizes=(10, 200),
        height=7,
        aspect=1.2,
        alpha=0.8,
    )
    
    g.set(xscale="log")
    g.set_axis_labels("Popularity (log)", "Rating")
    g.ax.xaxis.grid(True, "minor", linewidth=.25)
    g.ax.yaxis.grid(True, "minor", linewidth=.25)
    g.despine(left=True, bottom=True)

    plt.title("Popularity vs Rating", fontsize=14, fontweight='bold', pad=20)
    plt.show()

# Yearly Box Office Trends
def plot_yearly_revenue_trends(df):
    _ensure_dir()
    df = df.dropna(subset=["release_date", "revenue_musd"]).copy()
    
    df["year"] = pd.to_datetime(df["release_date"]).dt.year
    yearly_revenue = df.groupby("year")["revenue_musd"].sum().reset_index()

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=yearly_revenue, x="year", y="revenue_musd", marker='o')

    plt.title("Yearly Box Office Revenue Trends", fontsize=14, fontweight='bold')
    plt.xlabel("Year")
    plt.ylabel("Total Revenue (Millions USD)")
    
    plt.show()

# Franchise vs standalone performance
def plot_franchise_vs_standalone(df):
    _ensure_dir()
    df = df.copy()
    df["franchise"] = df["belongs_to_collection"].notna().map({True: "Franchise", False: "Standalone"})

    comparison = df.groupby("franchise").agg(
        mean_revenue=("revenue_musd", "mean"),
        mean_roi=("roi", "mean"),
        mean_popularity=("popularity", "mean"),
        mean_rating=("vote_average", "mean")
    ).reset_index()

    # Melting for easier seaborn plotting if needed, but for multiple metrics on one bar chart:
    comparison_melted = comparison.melt(id_vars="franchise", var_name="Metric", value_name="Value")

    plt.figure(figsize=(12, 6))
    sns.barplot(data=comparison_melted, x="Metric", y="Value", hue="franchise")

    plt.title("Franchise vs Standalone Performance", fontsize=14, fontweight='bold')
    plt.xlabel("Metric")
    plt.ylabel("Metric Value")
    
    plt.show()
