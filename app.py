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
  file_name = "flag1.csv"
  df = pd.read_csv(file_name, nrows=30000)
  return df


try:
  with st.spinner("Loading flight data automatically..."):
    df_sample = load_data()

  st.subheader("Data Overview")
  st.write(f"Sample Records Loaded: {len(df_sample):,}")

  df_sample.columns = df_sample.columns.str.upper().str.strip()

  if "AIRLINE" in df_sample.columns and "DEVELAY" in df_sample.columns:
    st.subheader("Top 10 Delayed Airlines")
    airline_data = (
        df_sample.groupby("AIRLINE")["DEVELAY"]
        .sum()
        .reset_index()
        .sort_values(by="DEVELAY", ascending=False)
        .head(10)
    )
    fig1 = px.bar(
        airline_data,
        x="AIRLINE",
        y="DEVELAY",
        title="Top 10 Delayed Airlines",
    )
    st.plotly_chart(fig1, use_container_width=True)
  else:
    st.subheader("Data Preview")
    st.dataframe(df_sample.head())

except Exception as e:
  st.error(
      f"Error loading data automatically. Please make sure the file name in"
      f" GitHub matches the code. Details: {e}"
  )
