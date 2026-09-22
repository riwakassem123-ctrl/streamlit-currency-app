import streamlit as st
import pandas as pd

st.title("LBP/USD Exchange Rate Analysis")

# =============================================================================
# Load Your CSV
# =============================================================================
@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")  
    # Rename all your columns
    df = df.rename(columns={
        "StartDate": "date",
        "EndDate": "end_date",
        "Value": "lbp_usd",
        "refArea": "region",
        "Currency": "currency",
        "Item Code": "item_code",
        "Observation URI": "obs_uri",
        "Month": "month_name",      # NEW
        "Publisher": "publisher",   # NEW
        "Year": "year",             # NEW
        "Item": "item",             # NEW
        "Dataset": "dataset",       # NEW
    })

    # Parse dates
    df["date"] = pd.to_datetime(df["date"])

    # Extract year and month if not already columns
    if "year" not in df.columns:
        df["year"] = df["date"].dt.year
    if "month_name" not in df.columns:
        df["month_name"] = df["date"].dt.strftime("%B")

    df["month_num"] = df["date"].dt.month

    return df

df = load_data()

# =============================================================================
# Sidebar Filters
# =============================================================================
with st.sidebar:
    st.header("Filters")

    # 1. Date Range
    st.subheader("Date Range")
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    date_range = st.date_input(
        "Select date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # 2. Year Multiselect
    st.subheader("Year")
    all_years = sorted(df["year"].unique().tolist())
    selected_years = st.multiselect(
        "Select years",
        options=all_years,
        default=all_years,
    )

    # 3. Month Multiselect
    st.subheader("Month")
    all_months = df["month_name"].unique().tolist()
    selected_months = st.multiselect(
        "Select months",
        options=all_months,
        default=all_months,
    )

    # 4. Publisher Dropdown
    st.subheader("Publisher")
    all_publishers = df["publisher"].unique().tolist()
    selected_publisher = st.selectbox(
        "Select publisher",
        options=["All"] + all_publishers,
    )

    # 5. Item Multiselect
    st.subheader("Item")
    all_items = df["item"].unique().tolist()
    selected_items = st.multiselect(
        "Select items",
        options=all_items,
        default=all_items,
    )

    # 6. Dataset Dropdown
    st.subheader("Dataset")
    all_datasets = df["dataset"].unique().tolist()
    selected_dataset = st.selectbox(
        "Select dataset",
        options=["All"] + all_datasets,
    )

    # 7. Region Multiselect
    st.subheader("Region")
    all_regions = df["region"].unique().tolist()
    selected_regions = st.multiselect(
        "Select regions",
        options=all_regions,
        default=all_regions,
    )

    # 8. Currency Dropdown
    st.subheader("Currency")
    all_currencies = df["currency"].unique().tolist()
    selected_currency = st.selectbox(
        "Select currency",
        options=["All"] + all_currencies,
    )

    # 9. Rate Range Slider
    st.subheader("Rate Range")
    min_rate = float(df["lbp_usd"].min())
    max_rate = float(df["lbp_usd"].max())
    rate_range = st.slider(
        "LBP/USD rate range",
        min_value=min_rate,
        max_value=max_rate,
        value=(min_rate, max_rate),
        step=100.0,
    )

    # 10. Checkboxes
    st.subheader("Display Options")
    show_line_chart = st.checkbox("Show line chart", value=True)
    show_scatter_chart = st.checkbox("Show scatter chart", value=True)
    show_raw_data = st.checkbox("Show raw data table", value=False)

# =============================================================================
# Apply Filters
# =============================================================================
filtered_df = df.copy()

# Date range
if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["date"].dt.date >= date_range[0]) &
        (filtered_df["date"].dt.date <= date_range[1])
    ]

# Year
if selected_years:
    filtered_df = filtered_df[filtered_df["year"].isin(selected_years)]

# Month
if selected_months:
    filtered_df = filtered_df[filtered_df["month_name"].isin(selected_months)]

# Publisher
if selected_publisher != "All":
    filtered_df = filtered_df[filtered_df["publisher"] == selected_publisher]

# Item
if selected_items:
    filtered_df = filtered_df[filtered_df["item"].isin(selected_items)]

# Dataset
if selected_dataset != "All":
    filtered_df = filtered_df[filtered_df["dataset"] == selected_dataset]

# Region
if selected_regions:
    filtered_df = filtered_df[filtered_df["region"].isin(selected_regions)]

# Currency
if selected_currency != "All":
    filtered_df = filtered_df[filtered_df["currency"] == selected_currency]

# Rate slider
filtered_df = filtered_df[
    (filtered_df["lbp_usd"] >= rate_range[0]) &
    (filtered_df["lbp_usd"] <= rate_range[1])
]

# =============================================================================
# Charts
# =============================================================================

# Line Chart
if show_line_chart:
    st.subheader("LBP/USD Exchange Rate Over Time")
    st.line_chart(
        filtered_df,
        x="date",
        y="lbp_usd",
        x_label="Date",
        y_label="LBP per 1 USD",
    )

# Scatter Chart
if show_scatter_chart:
    st.subheader("Monthly Exchange Rate Fluctuations by Year")
    monthly_df = (
        filtered_df.groupby(["year", "month_num"])["lbp_usd"]
        .mean()
        .reset_index()
    )
    monthly_df["year"] = monthly_df["year"].astype(str)

    st.scatter_chart(
        monthly_df,
        x="month_num",
        y="lbp_usd",
        color="year",
        x_label="Month",
        y_label="Avg LBP per 1 USD",
    )

# Raw Data Table
if show_raw_data:
    st.subheader("Raw Data")
    st.dataframe(filtered_df, hide_index=True)

