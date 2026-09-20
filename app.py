import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Lebanon Exchange Rate", layout="wide")

st.title("Lebanon Exchange Rate Analysis")
st.write(
    "This interactive app explores changes in Lebanon's exchange-rate data over time."
)

# Load the dataset
df = pd.read_csv("dataset.csv")

# Show the dataset
st.subheader("Dataset")
st.dataframe(df)

# Select numeric columns
numeric_columns = df.select_dtypes(include="number").columns.tolist()

if len(numeric_columns) >= 1:

    # Graph 1
    st.subheader("Exchange Rate Trend")

    column1 = st.selectbox(
        "Choose an exchange-rate variable:",
        numeric_columns
    )

    fig1 = px.line(
        df,
        y=column1,
        title=f"{column1} Over Time"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Graph 2
    st.subheader("Exchange Rate Distribution")

    fig2 = px.histogram(
        df,
        x=column1,
        title=f"Distribution of {column1}"
    )

    st.plotly_chart(fig2, use_container_width=True)

else:
    st.error("No numeric columns were found in the dataset.")




