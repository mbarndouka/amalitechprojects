# Final Report: TMDB Analysis

## 1. Objective

This report summarizes the end-to-end TMDB analysis workflow and presents the main findings from the processed movie dataset. The focus is on financial performance, audience response, franchise behavior, and trend patterns.

## 2. Methodology

### 2.1 Data Pipeline

1. Ingestion:

- Movie records were fetched from TMDB API endpoints (including credits payload).

2. Cleaning and standardization:

- Dropped irrelevant columns.
- Parsed nested fields (genres, production details, cast, crew, director).
- Converted numeric and date fields to appropriate types.
- Replaced unrealistic zero values for budget, revenue, and runtime with nulls.
- Converted budget and revenue to millions (budget_musd, revenue_musd).
- Removed duplicates and filtered to released movies.

3. Feature engineering:

- profit_musd = revenue_musd - budget_musd
- roi = profit_musd / budget_musd
- ROI was set to null for movies with budget below 10M to avoid unstable ratios.

4. KPI and visualization stage:

- Ranking functions were used for revenue, budget, profit, ROI, rating, votes, and popularity.
- Search filters were applied for genre, actors, and directors.
- Visualizations were generated for:
  - Median ROI by genre
  - Revenue vs budget
  - Popularity vs rating
  - Yearly box office trend
  - Franchise vs standalone comparison

### 2.2 Scope and Sample Size

- clean_df shape: (18, 22)
- kpi_df shape: (18, 24)
- voted_df shape (vote_count >= 100): (18, 24)

The dataset is intentionally small and focused on blockbuster-style titles, so conclusions should be interpreted as directional rather than universal.

## 3. Key Insights

### 3.1 Revenue, Budget, Profit Leaders

Top revenue titles (M USD):

- Avatar: 2923.706
- Avengers: Endgame: 2799.439
- Titanic: 2264.162
- Star Wars: The Force Awakens: 2068.224
- Avengers: Infinity War: 2052.415

Top budget titles (M USD):

- Avengers: Endgame: 356
- Avengers: Infinity War: 300
- Star Wars: The Last Jedi: 300
- The Lion King: 260
- Star Wars: The Force Awakens: 245

Top profit titles (M USD):

- Avatar: 2686.706
- Avengers: Endgame: 2443.439
- Titanic: 2064.162
- Star Wars: The Force Awakens: 1823.224
- Avengers: Infinity War: 1752.415

Interpretation:

- The same titles dominate revenue and profit, showing scale effects.
- Very high budgets can still produce exceptional returns when paired with strong demand.

### 3.2 ROI Patterns

Top ROI titles:

- Avatar: 11.336
- Titanic: 10.321
- Jurassic World: 10.144
- Harry Potter and the Deathly Hallows: Part 2: 9.732
- Frozen II: 8.691

Median ROI by genre:

- Highest: Comedy (8.691), Romance (8.617), Fantasy (8.093)
- Lower in sample: Action (6.306), Science Fiction (6.306)

Interpretation:

- High-ROI performance is not restricted to the largest-budget titles.
- In this sample, some genres convert spend into returns more efficiently than action/sci-fi.

### 3.3 Audience Response: Ratings, Votes, Popularity

Highest rated:

- Avengers: Endgame (8.235)
- Avengers: Infinity War (8.234)
- Harry Potter and the Deathly Hallows: Part 2 (8.081)

Most voted:

- The Avengers (36551)
- Avatar (33625)
- Avengers: Infinity War (31616)

Most popular (TMDB popularity):

- The Avengers (49.1925)
- Avengers: Infinity War (34.2807)
- Titanic (28.7289)

Interpretation:

- Audience scale (votes/popularity) and quality signal (rating) are positively related for top titles, but not perfectly aligned.

### 3.4 Search and Filtering Findings

- Action top by rating includes Endgame, Infinity War, and The Avengers.
- Science Fiction + Action + Bruce Willis returned no matches.

Interpretation:

- The filter logic is working and strict.
- Empty result is expected from dataset coverage, not a pipeline failure.

### 3.5 Franchise vs Standalone

Aggregate comparison:

- Standalone (2 titles):
  - mean_revenue: 1765.139
  - median_roi: 8.617
  - mean_budget: 180
  - mean_rating: 7.436
- Franchise (16 titles):
  - mean_revenue: 1682.668
  - median_roi: 6.786
  - mean_budget: 218
  - mean_rating: 7.391

Top franchise collections by total revenue:

- The Avengers Collection: 7776.073
- Star Wars Collection: 3400.922
- Jurassic Park Collection: 2982.006
- Avatar Collection: 2923.706
- Frozen Collection: 2727.902

Interpretation:

- Franchises dominate aggregate market footprint, but in this sample standalone titles show higher average ROI/revenue due to composition effects and small standalone count.

### 3.6 Yearly Revenue Trend

Yearly total revenue (M USD) shows strong volatility:

- 2015: 6660.565 (peak)
- 2018: 5956.036
- 2019: 5915.143

Interpretation:

- Revenue concentration by release year is significant for this title mix.
- Trend should not be generalized without broader catalog coverage.

## 4. Conclusions

1. Financial concentration is strong:
   A small set of major titles contributes a disproportionate share of revenue and profit.

2. Budget alone does not guarantee efficiency:
   ROI reveals meaningful differences in capital effectiveness across titles and genres.

3. Franchise strategy remains powerful but nuanced:
   Franchises deliver scale and recurring demand, while selected standalone titles can outperform on ROI.

4. Audience and financial outcomes are related but distinct:
   Highly rated movies are often popular, but popularity and votes do not map one-to-one with ROI.

5. Insights are reliable for this sampled portfolio, not the full market:
   Findings are actionable for this curated blockbuster subset and should be validated on a larger TMDB sample for wider inference.
