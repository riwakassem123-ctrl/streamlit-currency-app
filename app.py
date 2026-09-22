import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 1. LOAD DATA
# -----------------------------

df = pd.read_csv("dataset.csv")

st.title("Lebanese Currency Visualization")

# -----------------------------
# 2. CHECK DATA
# -----------------------------

st.write("Number of observations:", len(df))
st.write("Columns:", df.columns.tolist())

# -----------------------------
# 3. PREPARE YEAR
# -----------------------------

df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
df = df.dropna(subset=["Year"])
df["Year"] = df["Year"].astype(int)

# -----------------------------
# 4. YEAR FILTER
# -----------------------------

years = sorted(df["Year"].unique())

selected_years = st.select_slider(
    "Select year range",
    options=years,
    value=(years[0], years[-1])
)

start_year = selected_years[0]
end_year = selected_years[1]

filtered_df = df[
    (df["Year"] >= start_year) &
    (df["Year"] <= end_year)
]

# -----------------------------
# 5. CURRENCY SELECTION
# -----------------------------

selected_currencies = st.multiselect(
    "Select currency",
    ["LCU", "SLC"],
    default=["LCU", "SLC"]
)

# -----------------------------
# 6. LINE CHART
# -----------------------------

if selected_currencies:

    st.subheader("Currency Values Over Time")

    fig1 = px.line(
        filtered_df,
        x="Year",
        y=selected_currencies,
        markers=True
    )

    fig1.update_layout(
        xaxis_title="Year",
        yaxis_title="Currency Value"
    )

    st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# 7. FIRST INSIGHT
# -----------------------------

st.subheader("Insight")

st.write(
    "The line chart shows how the Lebanese currency values changed over "
    "time. Users can select a specific period to examine changes more closely."
)

# -----------------------------
# 8. BOX PLOT
# -----------------------------

if selected_currencies:

    st.subheader("Distribution of Currency Values")

    box_data = filtered_df[selected_currencies].melt(
        var_name="Currency",
        value_name="Value"
    )

    fig2 = px.box(
        box_data,
        x="Currency",
        y="Value",
        points="outliers"
    )

    fig2.update_layout(
        xaxis_title="Currency",
        yaxis_title="Value"
    )

    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# 9. SECOND INSIGHT
# -----------------------------

st.subheader("Second Insight")

st.write(
    "The box plot shows the distribution and spread of the currency values. "
    "The outliers represent observations that are unusually high or low "
    "relative to the rest of the data."
)

