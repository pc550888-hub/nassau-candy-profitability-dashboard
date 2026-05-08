import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------
# PAGE TITLE
# -----------------------------
st.title("📈 Pareto Analysis (Profit Concentration)")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("data/product_summary.csv")

df["start_date"] = pd.to_datetime(df["start_date"])
df["end_date"] = pd.to_datetime(df["end_date"])

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

division = st.sidebar.multiselect(
    "Select Division",
    df["division"].unique(),
    default=df["division"].unique()
)

threshold = st.sidebar.slider(
    "Margin Threshold",
    0.0, 1.0, 0.30
)

search_product = st.sidebar.text_input("Search Product")

min_date = df["start_date"].min()
max_date = df["end_date"].max()

date_range = st.sidebar.date_input(
    "Date Range",
    [min_date, max_date]
)

# -----------------------------
# APPLY FILTERS
# -----------------------------
filtered_df = df.copy()

filtered_df = filtered_df[filtered_df["division"].isin(division)]

if search_product:
    filtered_df = filtered_df[
        filtered_df["product_name"].str.contains(search_product, case=False, na=False)
    ]

if len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_df = filtered_df[
        (filtered_df["start_date"] >= start) &
        (filtered_df["end_date"] <= end)
    ]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# -----------------------------
# PARETO CALCULATION
# -----------------------------
pareto_df = filtered_df.sort_values(by="gross_profit", ascending=False)

# ✅ Limit for readability
pareto_df = pareto_df.head(15)

pareto_df["cum_pct"] = pareto_df["gross_profit"].cumsum() / pareto_df["gross_profit"].sum()

# -----------------------------
# PLOTLY CHART (PRO LOOK)
# -----------------------------
fig = go.Figure()

# Bars (profit)
fig.add_trace(
    go.Bar(
        x=pareto_df["product_name"],
        y=pareto_df["gross_profit"],
        name="Gross Profit",
        marker=dict(color="#4C78A8"),
        hovertemplate="Product: %{x}<br>Profit: %{y}<extra></extra>"
    )
)

# Line (cumulative %)
fig.add_trace(
    go.Scatter(
        x=pareto_df["product_name"],
        y=pareto_df["cum_pct"],
        name="Cumulative %",
        yaxis="y2",
        mode="lines+markers",
        line=dict(color="red"),
        hovertemplate="Cumulative: %{y:.2%}<extra></extra>"
    )
)

# Layout
fig.update_layout(
    xaxis=dict(title="Product", tickangle=-40),
    yaxis=dict(title="Gross Profit"),
    yaxis2=dict(
        title="Cumulative %",
        overlaying="y",
        side="right",
        tickformat=".0%"
    ),
    legend=dict(x=0.01, y=0.99),
    margin=dict(l=40, r=40, t=40, b=120),
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# TOP CONTRIBUTORS
# -----------------------------
st.subheader("🏆 Top Contributors (80%)")

top_contributors = pareto_df[pareto_df["cum_pct"] <= 0.8]

st.dataframe(
    top_contributors[["product_name", "gross_profit", "cum_pct"]],
    use_container_width=True
)