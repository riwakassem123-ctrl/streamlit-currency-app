import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("dataset.csv")

st.title("Lebanese Currency Visualization")

# =========================
# FIND COLUMNS
# =========================

st.write("Number of rows:", len(df))
st.write("Number of columns:", len(df.columns))

# Show the actual column names
st.write("Column names:", list(df.columns))

# =========================
# SELECT COLUMNS
# =========================

st.subheader("Select variables")

x_column = st.selectbox(
    "Select the time/year column",
    df.columns
)

y_columns = st.multiselect(
    "Select currency/value columns",
    [col for col in df.columns if col != x_column],
    default=[]
)

# =========================
# LINE CHART
# =========================

if len(y_columns) > 0:

    st.subheader("Currency Values Over Time")

    chart_df = df[[x_column] + y_columns].copy()

    fig1 = px.line(
        chart_df,
        x=x_column,
        y=y_columns,
        markers=True
    )

    fig1.update_layout(
        xaxis_title=x_column,
        yaxis_title="Value"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # =========================
    # BOX PLOT
    # =========================

    st.subheader("Distribution of Values")

    box_df = chart_df[y_columns].melt(
        var_name="Variable",
        value_name="Value"
    )

    fig2 = px.box(
        box_df,
        x="Variable",
        y="Value",
        points="outliers"
    )

    fig2.update_layout(
        xaxis_title="Variable",
        yaxis_title="Value"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

else:

    st.info(
        "Select at least one value/currency column above to display the charts."
    )
