# TMDB Movie Data Pipeline

A comprehensive Python-based data pipeline for fetching, cleaning, analyzing, and visualizing movie data using The Movie Database (TMDB) API. The pipeline is designed with asynchronous fetching, robust data processing, and automated visualization generation.

## Features

- **Asynchronous Data Ingestion**: Efficiently fetch movie details and credits concurrently using `httpx` and `asyncio`.
- **Automated Data Cleaning**: Standardize raw API responses, handle missing values, and prepare data for analysis.
- **KPI Engineering**: Compute essential metrics including:
  - **Profit**: Revenue minus budget.
  - **ROI (Return on Investment)**: Percentage return on movie spend.
  - **Financial Scaling**: Budget and Revenue converted to millions for readability.
- **Visual Insights**: Automatically generate charts for:
  - ROI distribution by genre.
  - Correlation between Revenue and Budget.
  - Relationship between Popularity and Rating.
  - Historical Yearly Revenue trends.
  - Performance comparison: Franchises vs. Standalone movies.
- **Project Structure**: Organized architecture following clean code principles.

## Requirements

- **Python 3.14+**
- **TMDB API Key**: Obtain one from [TMDB Settings](https://www.themoviedb.org/settings/api).
- **Environment Variables**: Configure access via a `.env` file.

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd TMDB
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the `TMDB` directory with the following:
   ```env
   API_KEY=your_tmdb_api_key_here
   URL=https://api.themoviedb.org/3/movie
   ```

## Usage

The entire pipeline can be executed from the root directory using:

```bash
python TMDB/index.py
```

This will:
1. Fetch movie data from TMDB.
2. Clean and process the records.
3. Calculate financial KPIs.
4. Save visualizations to the project directory.
5. Log progress and errors to `pipeline.log`.

## Testing

Run the automated test suite using `pytest`:

```bash
pytest TMDB/tests
```

## Project Structure

- `TMDB/api/`: TMDB API client with async support.
- `TMDB/analysis/`: KPI computation and data analysis logic.
- `TMDB/visualization/`: Matplotlib/Seaborn plotting functions.
- `TMDB/utils/`: Helper functions and async wrappers.
- `TMDB/tests/`: Unit and integration tests.
- `TMDB/config.toml`: Project and logging configuration.

## License

This project is licensed under the MIT License - see the `TMDB/config.toml` for details.

