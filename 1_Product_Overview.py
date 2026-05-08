import streamlit as st
import plotly.express as px

st.title("📊 Product Profitability Overview")

# ✅ GET DATA
if "filtered_df" not in st.session_state:
    st.warning("⚠️ Please go to main dashboard first")
    st.stop()

df = st.session_state.filtered_df

# ================= KPI =================
col1, col2, col3 = st.columns(3)

col1.metric("Products", df["product_name"].nunique())
col2.metric("Avg Margin", f"{df['margin'].mean():.2f}")
col3.metric("Top Product", df.sort_values("margin", ascending=False)["product_name"].iloc[0])

st.markdown("---")

# ================= TOP PRODUCTS =================
st.subheader("🏆 Top Products by Margin")

top_products = df.sort_values("margin", ascending=False).head(10)

fig = px.bar(
    top_products,
    x="product_name",
    y="margin",
    color="margin",
    color_continuous_scale="Blues",
    text="margin"
)

fig.update_layout(
    xaxis_tickangle=-30,
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)

# ================= SCATTER =================
st.subheader("📈 Profit vs Sales")

fig2 = px.scatter(
    df,
    x="sales",
    y="gross_profit",
    size="margin",
    color="division",
    hover_name="product_name",
    size_max=40
)

fig2.update_layout(
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
)

st.plotly_chart(fig2, use_container_width=True)