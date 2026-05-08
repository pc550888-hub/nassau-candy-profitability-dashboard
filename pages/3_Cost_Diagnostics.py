import streamlit as st
import plotly.express as px

st.title("⚠️ Cost vs Margin Diagnostics")

# ✅ GET DATA
if "filtered_df" not in st.session_state:
    st.warning("⚠️ Please go to main dashboard first")
    st.stop()

df = st.session_state.filtered_df

# ================= KPI =================
col1, col2 = st.columns(2)

high_cost = df.sort_values("cost", ascending=False).iloc[0]["product_name"]
low_margin = df.sort_values("margin").iloc[0]["product_name"]

col1.metric("Highest Cost Product", high_cost)
col2.metric("Lowest Margin Product", low_margin)

st.markdown("---")

# ================= SCATTER =================
st.subheader("📉 Cost vs Margin")

fig = px.scatter(
    df,
    x="cost",
    y="margin",
    size="sales",
    color="division",
    hover_name="product_name",
    size_max=50
)

fig.update_layout(
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)

# ================= HEATMAP =================
st.subheader("🔥 Margin Density")

fig2 = px.density_heatmap(
    df,
    x="cost",
    y="margin",
    nbinsx=20,
    nbinsy=20
)

fig2.update_layout(
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
)

st.plotly_chart(fig2, use_container_width=True)
