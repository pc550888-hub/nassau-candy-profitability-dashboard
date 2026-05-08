import streamlit as st
import plotly.express as px

st.title("🏢 Division Performance")

# ✅ GET DATA
if "filtered_df" not in st.session_state:
    st.warning("⚠️ Please go to main dashboard first")
    st.stop()

df = st.session_state.filtered_df

# ================= DATA =================
division_df = df.groupby("division")[["sales", "gross_profit"]].sum().reset_index()

# ================= KPI =================
col1, col2 = st.columns(2)

top_div = division_df.sort_values("gross_profit", ascending=False).iloc[0]["division"]

col1.metric("Top Division", top_div)
col2.metric("Total Divisions", division_df.shape[0])

st.markdown("---")

# ================= BAR =================
st.subheader("💰 Sales vs Profit")

fig = px.bar(
    division_df,
    x="division",
    y=["sales", "gross_profit"],
    barmode="group",
    color_discrete_sequence=["#4CAF50", "#2196F3"]
)

fig.update_layout(
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)

# ================= DONUT =================
st.subheader("📊 Profit Contribution")

fig2 = px.pie(
    division_df,
    names="division",
    values="gross_profit",
    hole=0.5
)

fig2.update_layout(
    plot_bgcolor="#0E1117",
    paper_bgcolor="#0E1117",
    font_color="white"
)

st.plotly_chart(fig2, use_container_width=True)