import streamlit as st
import pandas as pd 
df= pd.read_csv("dataset.csv")
st.write("Rows:", len(df))
st.write("Columns:", df.columns.tolist())
st.dataframe(df.head(10))
