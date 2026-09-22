import streamlit as st
import pandas as pd
import plotly.express as px

# =============================================================================
# Page Config
# =============================================================================
st.set_page_config(
    page_title="LBP/USD Exchange Rate Dashboard",
    page_icon=":material/monitoring:",
    layout="wide",
)

# =============================================================================
# Load Data
# =============================================================================
@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")  # Replace with your actual file name

    df = df.rename(columns={
        "StartDate": "date",
        "Value": "lbp_usd",
        "refArea": "region",
        "Currency": "currency",
        "Item Code": "item_code",
        "Month": "month_name",
        "Publisher": "publisher",
        "Year": "year",
        "Item": "item",
        "Dataset": "dataset",
    })

    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month_num"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%B")

    return df

df = load_data()

# =============================================================================
# Page Header
# =============================================================================
with st.container(
    horizontal=True,
    horizontal_alignment="distribute",
    vertical_alignment="center",
):
    st.markdown("# :material/monitoring: LBP/USD Exchange Rate Dashboard")
    if st.button(":material/restart_alt: Reset Filters", type="tertiary"):
        st.session_state.clear()
        st.rerun()

st.markdown("""
Lebanon has experienced one of the **worst currency collapses** in modern
history. The Lebanese Pound (LBP) was pegged at ~1,507 LBP/USD for decades
before collapsing after the 2019 financial crisis, losing over **90% of its
value**. This dashboard explores two key insights:

- **Insight 1:** The exchange rate was stable for decades then collapsed
  sharply after 2019.
- **Insight 2:** Monthly fluctuations became increasingly volatile year
  over year, with the highest instability between 2020 and 2023.
""")

st.divider()

# =============================================================================
# LINKED Filters
# Feature 1: Year Multiselect — drives Feature 2 month options
# =============================================================================
st.subheader(":material/tune: Filters")

st.info(
    ":material/link: **Linked filters:** Selecting a year updates the "
    "months available below — use both to drill down progressively."
)

col_f1, col_f2 = st.columns(2)

with col_f1:
    all_years = sorted(df["year"].unique().tolist())
    selected_years = st.multiselect(
        "**Step 1 — Select Years**",
        options=all_years,
        default=all_years,
        help="Select years to explore. Updates the months available below.",
    )

# Apply year filter first
year_filtered_df = (
    df[df["year"].isin(selected_years)] if selected_years else df.copy()
)

with col_f2:
    # Feature 2: Month options DRIVEN by selected years (linked behavior)
    available_months = sorted(year_filtered_df["month_name"].unique().tolist())
    selected_months = st.multiselect(
        "**Step 2 — Select Months** *(updates based on years above)*",
        options=available_months,
        default=available_months,
        help="Only months available in the selected years are shown.",
    )

# Apply month filter on top of year filter
filtered_df = (
    year_filtered_df[year_filtered_df["month_name"].isin(selected_months)]
    if selected_months
    else year_filtered_df.copy()
)

st.divider()

# =============================================================================
# Design Justification
# =============================================================================
with st.expander(
    ":material/info: Design Justification — Feature 1: Year Multiselect"
):
    st.markdown("""
    **Which user question does this answer?**
    "How did the LBP/USD exchange rate behave in specific years,
    particularly before and after the 2019 financial crisis?"

    **Why a multiselect rather than a slider or dropdown?**
    A multiselect allows the user to compare **multiple specific years
    side by side** (e.g. 2018 vs 2022), which a single-value dropdown
    cannot do. A slider would only allow a continuous range, making it
    harder to isolate and compare non-consecutive years.

    **Course concept:**
    This feature provides **context** by letting users isolate the
    pre-crisis period from the post-crisis period, helping them
    **focus attention** on the most relevant time window rather than
    being overwhelmed by the full dataset.
    """)

with st.expander(
    ":material/info: Design Justification — Feature 2: Month Multiselect (Linked)"
):
    st.markdown("""
    **Which user question does this answer?**
    "Within the years I selected, which specific months show the
    highest exchange rate fluctuations?"

    **Why a multiselect rather than a date range picker?**
    A date range picker selects a continuous period, but a month
    multiselect allows the user to compare **the same months across
    different years** (e.g. January across 2020, 2021, 2022),
    enabling seasonal comparison which a date range cannot do.

    **Course concept — Linked interaction:**
    The month options are **dynamically driven by the year selection**
    above. This means the user drills down progressively rather than
    filtering two things independently. This **reduces clutter** by
    only showing months that exist in the selected years, and
    **focuses attention** on the most relevant subset of data.
    """)

st.divider()

# =============================================================================
# KPI Cards + Status Badge + Progress Bar
# =============================================================================
st.subheader(":material/analytics: Key Metrics")

if not filtered_df.empty:
    current_rate = float(filtered_df["lbp_usd"].iloc[-1])
    previous_rate = float(filtered_df["lbp_usd"].iloc[-2])
    rate_change_pct = round(
        ((current_rate - previous_rate) / previous_rate) * 100, 2
    )
    highest_rate = float(filtered_df["lbp_usd"].max())
    lowest_rate = float(filtered_df["lbp_usd"].min())
    avg_rate = round(float(filtered_df["lbp_usd"].mean()), 2)
    volatility = round(float(filtered_df["lbp_usd"].std()), 2)
    total_records = len(filtered_df)

    # Status Badge
    if current_rate > 50000:
        st.badge(
            "Critical Depreciation",
            color="red",
            icon=":material/warning:",
        )
    elif current_rate > 10000:
        st.badge(
            "High Depreciation",
            color="orange",
            icon=":material/trending_down:",
        )
    else:
        st.badge(
            "Stable",
            color="green",
            icon=":material/check_circle:",
        )

    # KPI Cards
    with st.container(horizontal=True):
        st.metric(
            label=":material/currency_exchange: Current Rate",
            value=f"{current_rate:,.0f} LBP",
            delta=f"{rate_change_pct}%",
            border=True,
        )
        st.metric(
            label=":material/trending_up: Highest Rate",
            value=f"{highest_rate:,.0f} LBP",
            border=True,
        )
        st.metric(
            label=":material/trending_down: Lowest Rate",
            value=f"{lowest_rate:,.0f} LBP",
            border=True,
        )
        st.metric(
            label=":material/bar_chart: Average Rate",
            value=f"{avg_rate:,.0f} LBP",
            border=True,
        )
        st.metric(
            label=":material/ssid_chart: Volatility (Std Dev)",
            value=f"{volatility:,.0f}",
            border=True,
        )
        st.metric(
            label=":material/dataset: Total Records",
            value=f"{total_records:,}",
            border=True,
        )

    # Depreciation Progress Bar
    with st.container(border=True):
        st.markdown("**Depreciation from Peg Rate (1,507 LBP/USD)**")
        peg_rate = 1507
        max_rate = float(df["lbp_usd"].max())
        depreciation_pct = min(
            (current_rate - peg_rate) / (max_rate - peg_rate), 1.0
        )
        st.progress(
            depreciation_pct,
            text=f"Depreciated {depreciation_pct * 100:.1f}% from peg rate"
        )

else:
    st.warning("No data available for the selected filters.")

st.divider()

# =============================================================================
# Summary Statistics
# =============================================================================
with st.expander(":material/query_stats: Summary Statistics"):
    if not filtered_df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(
                filtered_df["lbp_usd"].describe().reset_index(),
                hide_index=True,
            )
        with col2:
            st.markdown(f"""
            - **Median Rate:** {filtered_df['lbp_usd'].median():,.0f} LBP
            - **Variance:** {filtered_df['lbp_usd'].var():,.0f}
            - **Range:** {filtered_df['lbp_usd'].max() - filtered_df['lbp_usd'].min():,.0f} LBP
            - **Total Years:** {filtered_df['year'].nunique()}
            - **Total Months:** {filtered_df['month_name'].nunique()}
            """)

st.divider()

# =============================================================================
# Charts
# =============================================================================
st.subheader(":material/insert_chart: Visualizations")

tab1, tab2, tab3, tab4 = st.tabs([
    ":material/show_chart: Rate Over Time",
    ":material/scatter_plot: Monthly Fluctuations",
    ":material/bar_chart: Yearly Average",
    ":material/percent: Year over Year Change",
])

# --- Tab 1: Line Chart with Annotations ---
with tab1:
    with st.container(border=True):
        st.subheader("LBP/USD Exchange Rate Over Time")
        st.caption(
            "Insight: The rate was stable at ~1,507 LBP/USD for decades "
            "before collapsing sharply after 2019."
        )

        # Chart type toggle
        chart_type = st.segmented_control(
            "Chart type",
            options=["Line", "Area"],
            default="Line",
            key="line_chart_type",
        )

        if not filtered_df.empty:
            if chart_type == "Area":
                fig_line = px.area(
                    filtered_df,
                    x="date",
                    y="lbp_usd",
                    title="LBP/USD Exchange Rate Over Time",
                    labels={"date": "Date", "lbp_usd": "LBP per 1 USD"},
                )
            else:
                fig_line = px.line(
                    filtered_df,
                    x="date",
                    y="lbp_usd",
                    title="LBP/USD Exchange Rate Over Time",
                    labels={"date": "Date", "lbp_usd": "LBP per 1 USD"},
                )

            # Crisis annotations
            fig_line.add_vline(
                x="2019-10-17",
                line_dash="dash",
                line_color="red",
                annotation_text="Crisis Start Oct 2019",
                annotation_position="top right",
            )
            fig_line.add_vrect(
                x0="2019-10-17",
                x1="2020-12-31",
                fillcolor="red",
                opacity=0.1,
                annotation_text="Crisis Period",
            )
            fig_line.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                hovermode="x unified",
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.warning("No data available for the selected filters.")

# --- Tab 2: Scatter Chart ---
with tab2:
    with st.container(border=True):
        st.subheader("Monthly Exchange Rate Fluctuations by Year")
        st.caption(
            "Insight: Monthly volatility increased dramatically from 2020 "
            "onwards, with large gaps between months showing rapid depreciation."
        )
        if not filtered_df.empty:
            monthly_df = (
                filtered_df.groupby(["year", "month_num", "month_name"])["lbp_usd"]
                .mean()
                .reset_index()
            )
            monthly_df["year"] = monthly_df["year"].astype(str)

            fig_scatter = px.scatter(
                monthly_df,
                x="month_num",
                y="lbp_usd",
                color="year",
                hover_data=["month_name"],
                title="Monthly Exchange Rate Fluctuations by Year",
                labels={
                    "month_num": "Month",
                    "lbp_usd": "Avg LBP per 1 USD",
                    "year": "Year",
                },
            )
            fig_scatter.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning("No data available for the selected filters.")

# --- Tab 3: Yearly Average Bar Chart ---
with tab3:
    with st.container(border=True):
        st.subheader("Average LBP/USD Rate by Year")
        st.caption(
            "Insight: The yearly average shows a clear acceleration of "
            "depreciation, with the steepest increases between 2020 and 2022."
        )
        if not filtered_df.empty:
            yearly_df = (
                filtered_df.groupby("year")["lbp_usd"]
                .mean()
                .reset_index()
            )
            yearly_df["year"] = yearly_df["year"].astype(str)

            fig_bar = px.bar(
                yearly_df,
                x="year",
                y="lbp_usd",
                title="Average LBP/USD Rate by Year",
                labels={"year": "Year", "lbp_usd": "Avg LBP per 1 USD"},
                color="lbp_usd",
                color_continuous_scale="Reds",
            )
            fig_bar.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("No data available for the selected filters.")

# --- Tab 4: Year over Year Change ---
with tab4:
    with st.container(border=True):
        st.subheader("Year over Year % Change in LBP/USD Rate")
        st.caption(
            "Insight: The steepest year over year increases occurred between "
            "2019 and 2021, reflecting the peak of Lebanon's financial crisis."
        )
        if not filtered_df.empty:
            yoy_df = (
                filtered_df.groupby("year")["lbp_usd"]
                .mean()
                .pct_change()
                .reset_index()
            )
            yoy_df.columns = ["year", "pct_change"]
            yoy_df["pct_change"] = yoy_df["pct_change"] * 100
            yoy_df["year"] = yoy_df["year"].astype(str)
            yoy_df = yoy_df.dropna()

            fig_yoy = px.bar(
                yoy_df,
                x="year",
                y="pct_change",
                title="Year over Year % Change in LBP/USD Rate",
                labels={"year": "Year", "pct_change": "% Change"},
                color="pct_change",
                color_continuous_scale="Reds",
            )
            fig_yoy.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_yoy, use_container_width=True)
        else:
            st.warning("No data available for the selected filters.")

st.divider()

# =============================================================================
# Raw Data Table
# =============================================================================
with st.expander(":material/table: View Raw Data"):
    col1, col2 = st.columns([3, 1])
    with col2:
        st.download_button(
            label=":material/download: Download Filtered CSV",
            data=filtered_df.to_csv(index=False),
            file_name="lbp_usd_filtered.csv",
            mime="text/csv",
        )
    st.dataframe(filtered_df, hide_index=True)

