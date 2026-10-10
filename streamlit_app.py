"""Streamlit app: estimate a used Toyota Prius price from its features."""
from pathlib import Path

import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATA = Path(__file__).parent / "data" / "prius_listings.csv"
NUMERIC = ["Years", "Mileage", "Owner#"]
CATEGORICAL = ["Model", "Condition", "Usage Type", "Location"]


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA, index_col=0)


@st.cache_resource
def train_model(df: pd.DataFrame) -> Pipeline:
    preprocessor = ColumnTransformer(
        [
            ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), NUMERIC),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
        ]
    )
    model = Pipeline([("preprocessor", preprocessor), ("regressor", LinearRegression())])
    return model.fit(df[NUMERIC + CATEGORICAL], df["Price"])


df = load_data()
model = train_model(df)

st.title("Toyota Prius Price Estimator")
st.caption(f"Linear regression trained on {len(df):,} used Prius listings scraped from CarGurus.")

col1, col2 = st.columns(2)
with col1:
    trim = st.selectbox("Model", sorted(df["Model"].unique()))
    year = st.slider("Year", int(df["Years"].min()), int(df["Years"].max()), 2016)
    mileage = st.slider("Mileage", 0, 275_000, 60_000, step=1_000)
    owners = st.slider("Previous owners", 0, 10, 1)
with col2:
    state = st.selectbox("State", sorted(df["Location"].unique()))
    usage = st.selectbox("Usage type", sorted(df["Usage Type"].unique()))
    conditions = sorted(df["Condition"].unique())
    condition = st.selectbox("Accident history", conditions, format_func=lambda c: c.replace("Accident check\n", ""))

if st.button("Estimate price", type="primary"):
    row = pd.DataFrame(
        {"Years": [year], "Model": [trim], "Mileage": [mileage], "Condition": [condition],
         "Usage Type": [usage], "Owner#": [owners], "Location": [state]}
    )
    price = float(model.predict(row)[0])
    if price > 0:
        st.metric("Estimated price", f"${price:,.0f}")
    else:
        st.warning("Not enough comparable listings to estimate this combination.")
