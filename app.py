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
  file_name = "flights.csv"
  df = pd.read_csv(file_name, nrows=100000)
  return df


try:
  with st.spinner("جاري تحميل وتحليل بيانات الطيران تلقائياً..."):
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
          .head(10)
      )
      fig1 = px.bar(
          airline_data,
          x=airline_col,
          y=delay_col,
          title="Top 10 Delayed Airlines",
      )
    else:
      airline_data = df_sample[airline_col].value_counts().reset_index().head(10)
      airline_data.columns = [airline_col, "Count"]
      fig1 = px.bar(
          airline_data, x=airline_col, y="Count", title="Top 10 Airlines Count"
      )
    st.plotly_chart(fig1, use_container_width=True)

  if origin_col:
    st.subheader(f"Delays by Airport ({origin_col})")
    if delay_col:
      airport_data = (
          df_sample.groupby(origin_col)[delay_col]
          .sum()
          .reset_index()
          .sort_values(by=delay_col, ascending=False)
          .head(10)
      )
      fig2 = px.bar(
          airport_data,
          x=origin_col,
          y=delay_col,
          title="Top 10 Delayed Airports",
      )
    else:
      airport_data = df_sample[origin_col].value_counts().reset_index().head(10)
      airport_data.columns = [origin_col, "Count"]
      fig2 = px.bar(
          airport_data, x=origin_col, y="Count",
