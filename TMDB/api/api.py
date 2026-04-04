import asyncio
import logging
import os

import httpx
from dotenv import load_dotenv

from utils.async_runner import _run_coroutine_sync

# Enhanced Centralized Logging Configuration
LOG_FILE = "pipeline.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
base_url = os.getenv("URL")
api_key = os.getenv("API_KEY")


class TMDB:
    def __init__(self):
        """Initialize with environment variable validation."""
        self.url = base_url
        self.api_key = api_key

        # Validation for production readiness
        errors = []
        if not self.api_key:
            errors.append("API_KEY environment variable is missing.")
        if not self.url:
            errors.append("URL environment variable is missing.")

        if errors:
            error_msg = " Configuration Error: " + " ".join(errors)
            logger.critical(error_msg)
            raise EnvironmentError(error_msg)

        logger.info("TMDB API client initialized successfully.")

    async def get_movie_with_credits_async(self, client, movie_id):
        """Fetch movie details with embedded credits in a single request."""
        try:
            movie_url = f"{self.url}/{movie_id}"
            params = {
                "api_key": self.api_key,
                "language": "en-US",
                "append_to_response": "credits",
            }

            movie_response = await client.get(movie_url, params=params)

            if movie_response.status_code == 404:
                logger.warning(f"Movie {movie_id} not found")
                return None

            movie_response.raise_for_status()
            movie_data = movie_response.json()

            logger.info(f"Fetched movie {movie_id} with credits")
            return movie_data

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP {e.response.status_code} for movie {movie_id}")
            return None
        except Exception as e:
            logger.error(f"Error fetching movie {movie_id}: {e}")
            return None

    async def get_movies_batch_async(self, movie_ids, max_concurrent=4):
        """Fetch multiple movies concurrently with simple throttling."""
        async with httpx.AsyncClient(timeout=10.0, http2=True) as client:
            # Create semaphore to limit concurrent requests
            semaphore = asyncio.Semaphore(max_concurrent)

            async def fetch_with_semaphore(movie_id):
                async with semaphore:
                    return await self.get_movie_with_credits_async(client, movie_id)

            # Fetch all movies concurrently
            tasks = [fetch_with_semaphore(movie_id) for movie_id in movie_ids]
            results = await asyncio.gather(*tasks)

            # Filter out None results
            return [r for r in results if r is not None]

    def get_movies_batch(self, movie_ids, max_concurrent=4):
        """Synchronous wrapper for batch fetching."""
        return _run_coroutine_sync(self.get_movies_batch_async(movie_ids, max_concurrent))
