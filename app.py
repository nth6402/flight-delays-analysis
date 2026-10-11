import os
import sys

os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "1000"

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Flight Delays Analysis", layout="wide")

st.title("Flight Delays Analysis Dashboard")


@st.cache_data
def load_data():
  file_name = "flights_sample_3m.csv"
  df = pd.read_csv(file_name, nrows=100000)
  return df


try:
  with st.spinner("Loading flight data automatically..."):
    df_sample = load_data()

  st.subheader("Data Overview")
  st.write(f"Sample Records Loaded: {len(df_sample):,}")

  df_sample.columns = df_sample.columns.str.upper().str.strip()

  delay_col = next(
      (c for c in df_sample.columns if "DEL" in c or "DEP_DEL" in c), None
  )
  airline_col = next(
      (
          c
          for c in df_sample.columns
          if "AIRLINE" in c or "CARRIER" in c or "OP_CARRIER" in c
      ),
      None,
  )
  origin_col = next(
      (c for c in df_sample.columns if "ORIGIN" in c or "DEST" in c), None
  )

  if airline_col:
    st.subheader(f"Delays by Airline ({airline_col})")
    if delay_col:
      airline_data = (
          df_sample.groupby(airline_col)[delay_col]
          .sum()
          .reset_index()
          .sort_values(by=delay_col, ascending=False)
