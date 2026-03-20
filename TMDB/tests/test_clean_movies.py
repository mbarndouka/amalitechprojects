import pandas as pd

import processing.clean_movies as clean_module
from processing.clean_movies import FINAL_COLUMNS, clean_movies


def test_clean_movies_extracts_cast_and_director_fields(tmp_path, monkeypatch):
    out_path = tmp_path / "clean_movies.parquet"
    monkeypatch.setattr(clean_module, "PROCESS_DATA_PATH", str(out_path))

    raw_df = pd.DataFrame(
        {
            "id": [100],
            "title": ["Sample Movie"],
            "tagline": ["Test"],
            "release_date": ["2024-01-01"],
            "genres": [[{"name": "Action"}, {"name": "Science Fiction"}]],
            "belongs_to_collection": [{"name": "Sample Saga"}],
            "original_language": ["en"],
            "budget": [50000000],
            "revenue": [150000000],
            "production_companies": [[{"name": "Studio A"}]],
            "production_countries": [[{"name": "USA"}]],
            "vote_count": [100],
            "vote_average": [7.5],
            "popularity": [90.0],
            "runtime": [120],
            "overview": ["Overview"],
            "spoken_languages": [[{"name": "English"}]],
            "poster_path": ["/poster.jpg"],
            "status": ["Released"],
            "credits": [
                {
                    "cast": [
                        {"name": "Actor One"},
                        {"name": "Actor Two"},
                    ],
                    "crew": [
                        {"name": "Crew One", "job": "Producer"},
                        {"name": "Director Name", "job": "Director"},
                    ],
                }
            ],
        }
    )

    cleaned = clean_movies(raw_df)

    assert list(cleaned.columns) == FINAL_COLUMNS
    row = cleaned.iloc[0]
    assert row["cast"] == "Actor One|Actor Two"
    assert row["cast_size"] == 2
    assert row["director"] == "Director Name"
    assert row["crew_size"] == 2
    assert out_path.exists()


def test_clean_movies_is_resilient_to_missing_optional_columns(tmp_path, monkeypatch):
    out_path = tmp_path / "clean_movies_missing.parquet"
    monkeypatch.setattr(clean_module, "PROCESS_DATA_PATH", str(out_path))

    raw_df = pd.DataFrame(
        {
            "id": [1],
            "title": ["Only Required"],
            "status": ["Released"],
        }
    )

    cleaned = clean_movies(raw_df)

    assert "cast" in cleaned.columns
    assert "director" in cleaned.columns
    assert len(cleaned) == 1
    assert out_path.exists()
