# Prius Price Predictor

An end-to-end machine-learning project: scrape used-car listings, clean them, fit a
pricing model and serve it as a small web app.

1. **Collect** – a Selenium scraper walked CarGurus search results for the Toyota Prius
   and pulled year, trim, mileage, accident history, usage type, number of owners,
   state and asking price from each listing.
2. **Model** – a scikit-learn pipeline (median imputation + scaling for numeric
   features, one-hot encoding for trim, accident history, usage type and state)
   feeding a linear regression.
3. **Serve** – a Streamlit app where you pick a car's features and get an estimated
   price.

## Results

Trained on 1,424 listings with an 80/20 train/test split (`random_state=0`):

| Metric (test set) | Value |
|---|---|
| R² | 0.96 |
| Mean absolute error | ≈ $1,100 (median asking price ≈ $12,000) |

## Run it

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Layout

```
streamlit_app.py            price estimator app
data/prius_listings.csv     cleaned listings used for training
scraper/cargurus_scraper.py the original 2022 Selenium scraper
```

The scraper is kept for reference: it targets the CarGurus page layout and Selenium API
of early 2022 and would need updating before it can collect fresh data.
