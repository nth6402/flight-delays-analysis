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
  data_url = (
      "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/flights.csv"
  )
  df = pd.read_csv(data_url)
  return df


try:
  with st.spinner("Loading flight data automatically..."):
    df_sample = load_data()

  st.subheader("Data Overview")
  st.write(f"Sample Records Loaded: {len(df_sample):,}")

  df_sample.columns = df_sample.columns.str.upper().str.strip()

  if "YEAR" in df_sample.columns and "PASSENGERS" in df_sample.columns:
    st.subheader("Passengers Trend by Year")
    yearly_data = (
        df_sample.groupby("YEAR")["PASSENGERS"].sum().reset_index()
    )
    fig1 = px.line(
        yearly_data,
        x="YEAR",
        y="PASSENGERS",
        markers=True,
        title="Total Passengers Over Years",
    )
    st.plotly_chart(fig1, use_container_width=True)

  if "MONTH" in df_sample.columns and "PASSENGERS" in df_sample.columns:
    st.subheader("Passengers Distribution by Month")
    monthly_data = (
        df_sample.groupby("MONTH")["PASSENGERS"].sum().reset_index()
    )
    fig2 = px.bar(
        monthly_data,
        x="MONTH",
        y="PASSENGERS",
        title="Total Passengers by Month",
    )
    st.plotly_chart(fig2, use_container_width=True)

  st.subheader("Data Table Preview")
  st.dataframe(df_sample)

except Exception as e:
  st.error(f"Error loading data automatically. Details: {e}")
