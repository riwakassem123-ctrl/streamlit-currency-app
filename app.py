import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Lebanon Exchange Rate Analysis",
    layout="wide"
)

st.title("Lebanon Exchange Rate Analysis")

st.write(
    "This interactive app explores changes in Lebanon's "
    "exchange-rate data over time."
)

# Load the dataset
df = pd.read_csv("dataset.csv")

# Show the data
st.subheader("Dataset")
st.dataframe(df)

# Find numeric columns
numeric_columns = df.select_dtypes(include="number").columns.tolist()

if numeric_columns:

    selected_column = st.selectbox(
        "Choose an exchange-rate variable:",
        numeric_columns
    )

    # Visualization 1
    st.subheader("Exchange Rate Trend")

    fig1 = px.line(
        df,
        x="EndDate",
        y="Value",
        title="Exchange rate value over time",
        
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Visualization 2
    st.subheader("Exchange Rate Distribution")

    fig2 = px.histogram(
        df,
        x=selected_column,
        title=f"Distribution of {selected_column}"
    )

    st.plotly_chart(fig2, use_container_width=True)

else:
    st.error("No numeric columns were found in the dataset.")




