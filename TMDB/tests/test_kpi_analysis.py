import pandas as pd
import pytest

from analysis.kpi_analysis import (
    compute_profit,
    top_revenue,
    top_budget,
    top_profit,
    top_roi,
    lowest_budget,
    top_voted,
    highest_rated,
    lowest_rated,
    most_popular,
    search_movies,
)


def _sample_df():
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "title": ["A", "B", "C", "D"],
            "revenue_musd": [200.0, 120.0, 80.0, 50.0],
            "budget_musd": [100.0, 20.0, 8.0, 12.0],
            "vote_count": [500, 250, 50, 300],
            "vote_average": [8.5, 7.1, 6.4, 8.0],
            "popularity": [95.0, 60.0, 45.0, 75.0],
            "genres": [
                "Action|Science Fiction",
                "Drama|Crime",
                "Science Fiction",
                "Action",
            ],
            "cast": [
                "Bruce Willis|Actor X",
                "Uma Thurman|Actor Y",
                "Actor Z",
                "Bruce Willis|Uma Thurman",
            ],
            "director": [
                "Director One",
                "Quentin Tarantino",
                "Director Three",
                "Director Four",
            ],
            "runtime": [120, 110, 90, 130],
        }
    )


def test_top_helpers_return_expected_count_and_order():
    df = compute_profit(_sample_df())

    helper_specs = [
        (top_revenue, "revenue_musd", False),
        (top_budget, "budget_musd", False),
        (top_profit, "profit_musd", False),
        (top_roi, "roi", False),
        (lowest_budget, "budget_musd", True),
        (top_voted, "vote_count", False),
        (most_popular, "popularity", False),
    ]

    for helper, column, ascending in helper_specs:
        result = helper(df, top_n=3)
        assert len(result) == 3
        expected = (
            df.sort_values(by=column, ascending=ascending)
            .head(3)["id"]
            .tolist()
        )
        assert result["id"].tolist() == expected


def test_highest_and_lowest_rated_are_oppositely_sorted():
    df = compute_profit(_sample_df())

    high = highest_rated(df, top_n=4)
    low = lowest_rated(df, top_n=4)

    assert high["vote_average"].tolist() == sorted(df["vote_average"], reverse=True)
    assert low["vote_average"].tolist() == sorted(df["vote_average"])


def test_search_movies_filters_and_sorts():
    df = compute_profit(_sample_df())

    result = search_movies(
        df,
        genre=["Action"],
        actors=["Bruce Willis"],
        director="Director",
        sort_by="runtime",
        ascending=True,
    )

    assert isinstance(result, pd.DataFrame)
    assert result["id"].tolist() == [1, 4]
    assert result["runtime"].tolist() == [120, 130]


def test_search_movies_raises_for_missing_required_columns():
    df = pd.DataFrame({"title": ["A"], "vote_average": [7.0]})

    with pytest.raises(ValueError, match="search_movies requires missing columns"):
        search_movies(df, actors="Any Actor")


def test_compute_profit_blanks_roi_for_budget_below_10():
    df = compute_profit(_sample_df())

    low_budget_row = df.loc[df["budget_musd"] == 8.0].iloc[0]
    assert pd.isna(low_budget_row["roi"])

    high_budget_row = df.loc[df["budget_musd"] == 20.0].iloc[0]
    assert pd.notna(high_budget_row["roi"])
