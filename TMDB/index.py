import os
import logging
import argparse
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("pipeline.log")
    ]
)
logger = logging.getLogger(__name__)

from ingestion.fetch_movie import fetch_movie
from processing.clean_movies import clean_movies
from analysis.kpi_analysis import compute_profit
from utils.async_runner import _run_coroutine_sync
from visualization.plots import (
    plot_roi_by_genre,
    plot_revenue_vs_budget,
    plot_popularity_vs_rating,
    plot_yearly_revenue_trends,
    plot_franchise_vs_standalone
)

def run_pipeline():
    """Executes the complete TMDB data pipeline."""
    logger.info("Starting TMDB data pipeline...")
    
    try:
        # Step 1: Fetch data
        logger.info("Step 1: Fetching movie data from TMDB API...")
        raw_data = _run_coroutine_sync(fetch_movie())
        if raw_data is None or raw_data.empty:
            logger.error("No data fetched. Exiting pipeline.")
            return

        # Step 2: Clean and Process data
        logger.info("Step 2: Cleaning and processing movie data...")
        cleaned_data = clean_movies(raw_data)
        
        logger.info("Computing additional KPIs (Profit, ROI)...")
        cleaned_data = compute_profit(cleaned_data)
        
        # Step 3: Generate visualizations
        logger.info("Step 3: Generating visualizations...")
        
        visualizations = [
            ("ROI by Genre", plot_roi_by_genre),
            ("Revenue vs Budget", plot_revenue_vs_budget),
            ("Popularity vs Rating", plot_popularity_vs_rating),
            ("Yearly Revenue Trends", plot_yearly_revenue_trends),
            ("Franchise vs Standalone", plot_franchise_vs_standalone)
        ]
        
        for name, plot_func in visualizations:
            try:
                logger.info(f"Generating plot: {name}")
                plot_func(cleaned_data)
            except Exception as e:
                logger.error(f"Failed to generate plot '{name}': {e}")

        logger.info("TMDB data pipeline completed successfully.")
        
    except Exception as e:
        logger.critical(f"Pipeline failed with an unexpected error: {e}", exc_info=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TMDB Data Pipeline")
    # We could add arguments here, e.g., --skip-fetch, --output-dir, etc.
    args = parser.parse_args()
    
    run_pipeline()