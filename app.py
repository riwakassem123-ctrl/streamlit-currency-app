import streamlit as st
import pandas as pd
import plotly.express as px

# Page title
st.title("Lebanese Currency Exchange Rate Visualization")

st.write(
    "This interactive dashboard explores changes in Lebanese currency "
    "values over time and compares the distributions of LCU and SLC."
)

# Load the dataset
df = pd.read_csv("your_file.csv")

# Make sure Year is numeric
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

# Remove rows without a year
df = df.dropna(subset=["Year"])

# Convert Year to integer
df["Year"] = df["Year"].astype(int)

# -----------------------------
# INTERACTION 1: YEAR RANGE
# -----------------------------

min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

year_range = st.slider(
    "Select year range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# Filter the data
filtered_df = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

# -----------------------------
# INTERACTION 2: CURRENCY
# -----------------------------

currency_options = ["LCU", "SLC"]

selected_currencies = st.multiselect(
    "Select currency",
    currency_options,
    default=currency_options
)

# -----------------------------
# VISUALIZATION 1
# Currency trend over time
# -----------------------------

st.subheader("Currency Values Over Time")

if len(selected_currencies) > 0:

    fig1 = px.line(
        filtered_df,
        x="Year",
        y=selected_currencies,
        markers=True,
        title="Lebanese Currency Values Over Time"
    )

    fig1.update_layout(
        xaxis_title="Year",
        yaxis_title="Currency Value",
        legend_title="Currency"
    )

    st.plotly_chart(fig1, use_container_width=True)

else:
    st.warning("Please select at least one currency.")

# -----------------------------
# INSIGHT 1
# -----------------------------

st.subheader("Insight 1")

st.write(
    "The line chart shows how Lebanese currency values changed over time. "
    "The interactive year range allows the user to focus on a specific "
    "period and observe changes more clearly."
)

# -----------------------------
# VISUALIZATION 2
# Distribution / Box Plot
# -----------------------------

st.subheader("Distribution of Currency Values")

if len(selected_currencies) > 0:

    melted_df = filtered_df[selected_currencies].melt(
        var_name="Currency",
        value_name="Value"
    )

    fig2 = px.box(
        melted_df,
        x="Currency",
        y="Value",
        points="outliers",
        title="Distribution of Currency Values"
    )

    fig2.update_layout(
        xaxis_title="Currency",
        yaxis_title="Currency Value"
    )

    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# INSIGHT 2
# -----------------------------

st.subheader("Insight 2")

st.write(
    "The box plot highlights the distribution and spread of the currency "
    "values. Extreme observations appear as outliers and reflect periods "
    "of substantial changes in currency values."
)
