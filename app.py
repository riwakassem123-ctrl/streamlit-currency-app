import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Lebanon Exchange Rate Analysis",
    layout="wide"
)

st.title("Lebanon Exchange Rate Analysis")

st.write(
    """
    This interactive app examines changes in Lebanon's exchange-rate data
    over time. The dataset contains exchange-rate observations identified
    by currency, dates, and recorded values.
    """
)

# Load dataset
df = pd.read_csv("dataset.csv")

# Prepare dates
df["Enddate"] = pd.to_datetime(df["Enddate"], errors="coerce")

# Remove rows with missing information
df = df.dropna(subset=["Enddate", "Value", "Currency"])

# Sort by date
df = df.sort_values("Enddate")


# -----------------------------
# INTERACTION 1: Currency
# -----------------------------

st.subheader("Explore the data")

currencies = sorted(df["Currency"].unique())

selected_currency = st.selectbox(
    "Choose a currency:",
    currencies
)

# Filter according to currency
currency_df = df[df["Currency"] == selected_currency].copy()


# -----------------------------
# INTERACTION 2: Date range
# -----------------------------

min_date = currency_df["Enddate"].min().date()
max_date = currency_df["Enddate"].max().date()

selected_dates = st.slider(
    "Choose a date range:",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

# Apply the selected date range
filtered_df = currency_df[
    (currency_df["Enddate"].dt.date >= selected_dates[0]) &
    (currency_df["Enddate"].dt.date <= selected_dates[1])
]


# -----------------------------
# VISUALIZATION 1
# -----------------------------

st.subheader("Exchange Rate Value Over Time")

fig1 = px.line(
    filtered_df,
    x="Enddate",
    y="Value",
    title=f"{selected_currency} Exchange Rate Value Over Time",
    markers=True
)

fig1.update_layout(
    xaxis_title="End date",
    yaxis_title="Value"
)

st.plotly_chart(fig1, use_container_width=True)


# -----------------------------
# VISUALIZATION 2
# -----------------------------

st.subheader("Distribution of Exchange Rate Values")

fig2 = px.histogram(
    filtered_df,
    x="Value",
    title=f"Distribution of {selected_currency} Exchange Rate Values",
    nbins=30
)

fig2.update_layout(
    xaxis_title="Value",
    yaxis_title="Number of observations"
)

st.plotly_chart(fig2, use_container_width=True)


# -----------------------------
# INSIGHTS
# -----------------------------

st.subheader("Key Insights")

if len(filtered_df) > 0:

    highest_value = filtered_df["Value"].max()
    lowest_value = filtered_df["Value"].min()

    st.write(
        f"• The selected period has exchange-rate values ranging "
        f"from {lowest_value:,.2f} to {highest_value:,.2f}."
    )

    st.write(
        f"• The distribution shows how frequently different exchange-rate "
        f"values occur within the selected {selected_currency} period."
    )

else:
    st.warning("No observations are available for the selected period.")




