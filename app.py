import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Nassau Dashboard", layout="wide")

# -----------------------------
# PREMIUM UI CSS
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
}

.kpi-card {
    background-color: #1C1F26;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
}

.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: #4CAF50;
}

section[data-testid="stSidebar"] {
    background-color: #161A23;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("data/product_summary.csv")

df["start_date"] = pd.to_datetime(df["start_date"])
df["end_date"] = pd.to_datetime(df["end_date"])

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filters")

division = st.sidebar.multiselect(
    "Division",
    df["division"].unique(),
    default=df["division"].unique()
)

threshold = st.sidebar.slider("Margin Threshold", 0.0, 1.0, 0.30)

search_product = st.sidebar.text_input("Search Product")

date_range = st.sidebar.date_input(
    "Date Range",
    [df["start_date"].min(), df["end_date"].max()]
)

# ==============================
# APPLY FILTERS
# ==============================

filtered_df = df.copy()

# Division filter
filtered_df = filtered_df[filtered_df["division"].isin(division)]

# ✅ Margin filter (THIS WAS MISSING)
filtered_df = filtered_df[filtered_df["margin"] > threshold]

# Search filter
if search_product:
    filtered_df = filtered_df[
        filtered_df["product_name"].str.contains(search_product, case=False, na=False)
    ]

# Date filter
if len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_df = filtered_df[
        (filtered_df["start_date"] >= start) &
        (filtered_df["end_date"] <= end)
    ]

# Empty check
if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()
st.session_state.filtered_df = filtered_df
# -----------------------------
# TITLE
# -----------------------------
st.title("🍬 Nassau Candy Profitability Dashboard")

# -----------------------------
# KPI CARDS
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.markdown(f"""
<div class="kpi-card">
    <h3>Total Revenue</h3>
    <div class="metric-value">{int(filtered_df['sales'].sum()):,}</div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="kpi-card">
    <h3>Total Profit</h3>
    <div class="metric-value">{int(filtered_df['gross_profit'].sum()):,}</div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="kpi-card">
    <h3>Avg Margin</h3>
    <div class="metric-value">{filtered_df['margin'].mean():.2f}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# TOP PRODUCTS
# -----------------------------
st.subheader("🏆 Top Products by Margin")

top_products = filtered_df.sort_values("margin", ascending=False).head(10)

fig1 = px.bar(
    top_products,
    x="product_name",
    y="margin",
    color="margin",
    color_continuous_scale="Blues"
)

fig1.update_layout(xaxis_tickangle=-30)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

# -----------------------------
# DIVISION PERFORMANCE
# -----------------------------
st.subheader("🏢 Division Performance")

division_df = filtered_df.groupby("division")[["sales", "gross_profit"]].sum().reset_index()

fig2 = px.bar(
    division_df,
    x="division",
    y=["sales", "gross_profit"],
    barmode="group"
)

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# -----------------------------
# COST VS MARGIN
# -----------------------------
st.subheader("⚠️ Cost vs Margin Diagnostics")

fig3 = px.scatter(
    filtered_df,
    x="cost",
    y="margin",
    size="sales",
    color="division",
    hover_name="product_name"
)

st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# -----------------------------
# PARETO ANALYSIS
# -----------------------------
st.subheader("📈 Pareto Analysis")

pareto_df = filtered_df.sort_values(by="gross_profit", ascending=False).head(15)

pareto_df["cum_pct"] = pareto_df["gross_profit"].cumsum() / pareto_df["gross_profit"].sum()

fig4 = go.Figure()

fig4.add_trace(go.Bar(
    x=pareto_df["product_name"],
    y=pareto_df["gross_profit"],
    name="Profit"
))

fig4.add_trace(go.Scatter(
    x=pareto_df["product_name"],
    y=pareto_df["cum_pct"],
    yaxis="y2",
    mode="lines+markers",
    name="Cumulative %"
))

fig4.update_layout(
    xaxis=dict(tickangle=-40),
    yaxis=dict(title="Profit"),
    yaxis2=dict(overlaying="y", side="right", tickformat=".0%"),
    height=500
)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------------
# TOP CONTRIBUTORS
# -----------------------------
st.subheader("🏆 Top Contributors (80%)")

top_contributors = pareto_df[pareto_df["cum_pct"] <= 0.8]

st.dataframe(
    top_contributors[["product_name", "gross_profit", "cum_pct"]],
    use_container_width=True
)