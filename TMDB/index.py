import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

from ingestion.fetch_movie import fetch_movie
from processing.clean_movies import clean_movies
from visualization.plots import (
    plot_revenue_vs_budget,
    plot_popularity_vs_rating,
    plot_yearly_revenue_trends,
    plot_franchise_vs_standalone
)

def run_pipeline():
    logging.info("Starting TMDB data pipeline...")
    
    # Step 1: Fetch data
    logging.info("Fetching movie data...")
    raw_data = fetch_movie()
    
    # Step 2: Clean data
    logging.info("Cleaning movie data...")
    cleaned_data = clean_movies(raw_data)
    
    # Step 3: Generate visualizations
    logging.info("Generating visualizations...")
    plot_revenue_vs_budget(cleaned_data)
    plot_popularity_vs_rating(cleaned_data)
    plot_yearly_revenue_trends(cleaned_data)
    plot_franchise_vs_standalone(cleaned_data)
    
    logging.info("TMDB data pipeline completed successfully.")
    
if __name__ == "__main__":
    run_pipeline()