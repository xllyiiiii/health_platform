import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans

# 页面设置
st.set_page_config(
    page_title="全球健康智析平台",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 标题
st.title("🌍 全球健康智析平台")
st.caption("中国大学生计算机设计大赛 · 大数据实践赛")

# 侧边栏
st.sidebar.title("功能菜单")
menu = st.sidebar.radio(
    "选择模块",
    ["数据概览", "全球风险地图", "健康效率HEI", "国家聚类", "趋势分析"]
)

# 加载数据
@st.cache_data
def load_data():
    df = pd.read_csv("data/sim_data.csv")
    return df

df = load_data()

# ====================== 1. 数据概览 ======================
if menu == "数据概览":
    st.subheader("📊 数据概览")
    st.dataframe(df, use_container_width=True)

# ====================== 2. 全球风险地图 ======================
elif menu == "全球风险地图":
    st.subheader("🗺️ 全球健康风险分布")
    fig = px.choropleth(
        df,
        locations="Country",
        locationmode="country names",
        color="RiskValue",
        title="全球健康风险值",
        color_continuous_scale="Reds",
        range_color=(4, 10)
    )
    st.plotly_chart(fig, use_container_width=True)

# ====================== 3. 健康效率HEI ======================
elif menu == "健康效率HEI":
    st.subheader("📈 健康效率指数 HEI（核心创新）")

    # 计算HEI
    df["Output"] = (df["LifeExpectancy"] - df["LifeExpectancy"].min()) / (df["LifeExpectancy"].max() - df["LifeExpectancy"].min())
    df["Input"] = (df["HealthExpend"] - df["HealthExpend"].min()) / (df["HealthExpend"].max() - df["HealthExpend"].min())
    df["HEI"] = df["Output"] / (df["Input"] + 1e-6)

    # 展示排名
    hei_df = df[["Country", "LifeExpectancy", "HealthExpend", "HEI"]].sort_values("HEI", ascending=False)
    st.dataframe(hei_df, use_container_width=True)

    # 柱状图
    fig = px.bar(hei_df, x="Country", y="HEI", title="HEI 排名", color="HEI", color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)

# ====================== 4. 国家聚类 ======================
elif menu == "国家聚类":
    st.subheader("🔍 国家健康水平 K-Means 聚类")

    # 聚类
    X = df[["LifeExpectancy", "HealthExpend", "DoctorDensity"]]
    model = KMeans(n_clusters=4, random_state=42)
    df["Cluster"] = model.fit_predict(X)

    # 展示
    st.dataframe(df[["Country", "Cluster", "LifeExpectancy", "HealthExpend"]], use_container_width=True)

    # 散点图
    fig = px.scatter(
        df,
        x="HealthExpend",
        y="LifeExpectancy",
        color="Cluster",
        hover_name="Country",
        title="健康投入 vs 预期寿命（聚类）"
    )
    st.plotly_chart(fig, use_container_width=True)

# ====================== 5. 趋势分析 ======================
elif menu == "趋势分析":
    st.subheader("📉 全球风险趋势")
    # 模拟趋势数据
    years = [2015,2016,2017,2018,2019,2020]
    risk_trend = [5.2,5.5,5.9,6.3,6.8,7.2]
    trend_df = pd.DataFrame({"Year":years,"Risk":risk_trend})
    fig = px.line(trend_df, x="Year", y="Risk", title="2015-2020 全球风险趋势")
    st.plotly_chart(fig, use_container_width=True)

st.success("✅ 平台运行成功！")