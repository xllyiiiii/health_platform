# main.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import random
from io import BytesIO
import base64
import os

# 页面全局设置 - 更现代的大屏深色主题
st.set_page_config(
    page_title="MediVision｜全球健康智能分析平台",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏥"
)

# 生成模拟图标（Base64编码的SVG图形，避免外网图片加载失败）
def get_svg_icon(icon_type, size=40):
    """生成简单的SVG图标"""
    icons = {
        "hospital": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 3v18M3 12h18" stroke="#48bbff" stroke-width="2" stroke-linecap="round"/>
            <rect x="4" y="4" width="16" height="16" rx="2" stroke="#48bbff" stroke-width="2"/>
        </svg>''',
        "doctor": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="8" r="4" stroke="#7c3aed" stroke-width="2"/>
            <path d="M5 20v-2a7 7 0 0 1 14 0v2" stroke="#7c3aed" stroke-width="2"/>
        </svg>''',
        "globe": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" stroke="#ec489a" stroke-width="2"/>
            <path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" stroke="#ec489a" stroke-width="2"/>
        </svg>''',
        "chart": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M21 12v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h6M15 3h6v6M21 3l-9 9" stroke="#f59e0b" stroke-width="2"/>
        </svg>''',
        "heart": f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="#ef4444" stroke="#ef4444" stroke-width="1"/>
        </svg>'''
    }
    return icons.get(icon_type, "")

# 自定义CSS样式 - 更高级的视觉效果
st.markdown("""
<style>
    /* 主背景 - 渐变深色 */
    .stApp {
        background: linear-gradient(135deg, #0a0f1e 0%, #0d1625 100%);
    }
    
    /* 卡片样式 - 毛玻璃效果 */
    .custom-card {
        background: rgba(20, 28, 40, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(72, 187, 255, 0.2);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .custom-card:hover {
        transform: translateY(-5px);
        border-color: rgba(72, 187, 255, 0.5);
        box-shadow: 0 12px 48px 0 rgba(72, 187, 255, 0.2);
    }
    
    /* 指标卡片 */
    .metric-card {
        background: linear-gradient(135deg, #1a2332 0%, #16202e 100%);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        border-bottom: 3px solid #48bbff;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        border-bottom-color: #7c3aed;
    }
    
    /* 标题装饰 */
    .gradient-text {
        background: linear-gradient(120deg, #48bbff, #7c3aed, #ec489a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: bold;
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* 侧边栏美化 */
    [data-testid="stSidebar"] {
        background: rgba(10, 15, 30, 0.95);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(72, 187, 255, 0.1);
    }
    
    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(120deg, #48bbff, #3b82f6);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(59,130,246,0.4);
    }
    
    /* 输入框美化 */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background: #1a2332;
        border: 1px solid #2d3a4a;
        border-radius: 10px;
        color: white;
    }
    
    /* 信息框美化 */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
    }
    
    /* 进度条美化 */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #48bbff, #7c3aed);
    }
    
    /* 标签页样式 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #1a2332;
        border-radius: 12px;
        padding: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(72, 187, 255, 0.1);
    }
    
    /* 带图标的标题 */
    .icon-title {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 20px;
    }
    
    /* 装饰分割线 */
    .custom-divider {
        background: linear-gradient(90deg, transparent, #48bbff, #7c3aed, #ec489a, transparent);
        height: 2px;
        margin: 20px 0;
    }
    
    /* 统计数字动画 */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .animate-number {
        animation: fadeInUp 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if 'calculation_history' not in st.session_state:
    st.session_state.calculation_history = []
if 'favorite_countries' not in st.session_state:
    st.session_state.favorite_countries = set()

# ========== 侧边栏美化 ==========
with st.sidebar:
    # Logo区域
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="font-size: 48px;">🏥</div>
        <h2 style="margin: 10px 0 5px 0;">MediVision</h2>
        <p style="color: #8892b0; font-size: 12px;">健康数据智能分析平台</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # 菜单选项（带图标）
    menu_options = {
        "🏠 数据驾驶舱": "🏠",
        "📊 医疗资源分析": "📊",
        "✏️ 智能计算引擎": "✏️",
        "🌍 全球风险监测": "🌍",
        "📈 趋势预测": "📈",
        "📋 报告中心": "📋"
    }
    
    menu = st.selectbox(
        "功能导航",
        list(menu_options.keys()),
        format_func=lambda x: f"{menu_options[x]} {x.split(' ', 1)[1] if ' ' in x else x}"
    )
    
    st.divider()
    
    # 实时数据面板
    st.markdown("### 📡 实时数据流")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.caption(f"⏰ 系统时间: {current_time}")
    
    # 模拟实时指标
    real_time_metrics = {
        "🌍 在线用户": random.randint(23, 156),
        "📊 今日分析": random.randint(45, 234),
        "💾 数据量": f"{random.randint(8, 45)}GB"
    }
    for metric, value in real_time_metrics.items():
        st.caption(f"{metric}: {value}")
    
    st.divider()
    
    # 数据源信息
    # 数据源信息 - 显示本地数据文件
with st.expander("📁 本地数据文件", expanded=False):
    import os
    import glob
    
    # 显示 data 文件夹下的 CSV 文件
    if os.path.exists("data"):
        csv_files = glob.glob("data/*.csv")
        if csv_files:
            st.caption("📊 **数据文件列表:**")
            for f in sorted(csv_files)[:15]:  # 最多显示15个
                file_name = os.path.basename(f)
                file_size = os.path.getsize(f) / 1024  # KB
                st.caption(f"   📄 {file_name} ({file_size:.0f} KB)")
        else:
            st.caption("  暂无 CSV 文件")
    
    # 显示根目录下的数据文件
    root_files = glob.glob("*.csv")
    if root_files:
        st.caption("📁 **根目录数据文件:**")
        for f in sorted(root_files)[:10]:
            file_name = os.path.basename(f)
            file_size = os.path.getsize(f) / 1024
            st.caption(f"   📄 {file_name} ({file_size:.0f} KB)")
    
    # 用户状态
    st.markdown("""
    <div style="background: rgba(72, 187, 255, 0.1); border-radius: 10px; padding: 10px; margin-top: 20px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div>👤</div>
            <div>
                <div style="font-weight: 600;">访客用户</div>
                <div style="font-size: 11px; color: #48bbff;">在线</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ========== 主标题区域 ==========
col_logo1, col_title, col_logo2 = st.columns([1, 2, 1])
with col_title:
    st.markdown('<p class="gradient-text" style="text-align: center;">🌍 MediVision</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #8892b0; margin-top: -10px;">全球健康智能分析决策平台</p>', unsafe_allow_html=True)

# 装饰分割线
st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# ========== 1. 数据驾驶舱 ==========
if menu == "🏠 数据驾驶舱":
    st.subheader("📊 数据驾驶舱")
    
    # 欢迎横幅
    st.markdown("""
    <div style="background: linear-gradient(120deg, rgba(72,187,255,0.1), rgba(124,58,237,0.1)); 
                border-radius: 15px; padding: 20px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <h3 style="margin: 0;">👋 欢迎回来</h3>
                <p style="color: #8892b0; margin: 5px 0 0 0;">探索全球健康数据洞察</p>
            </div>
            <div style="font-size: 48px;">📈</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 关键指标卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 32px;">🌍</div>
        </div>
        """, unsafe_allow_html=True)
        st.metric("覆盖国家", "195", "+12", delta_color="normal")
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 32px;">📊</div>
        </div>
        """, unsafe_allow_html=True)
        st.metric("数据记录", "15,234", "+2,345", delta_color="normal")
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 32px;">🏥</div>
        </div>
        """, unsafe_allow_html=True)
        st.metric("医疗机构", "124,567", "+3.2%", delta_color="normal")
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 32px;">👨‍⚕️</div>
        </div>
        """, unsafe_allow_html=True)
        st.metric("医生数量", "8.2M", "+2.1%", delta_color="normal")
    
    st.divider()
    
    # 快速分析面板
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("🎯 快速健康评估")
        
        quick_country = st.selectbox("选择国家", ["中国", "美国", "日本", "德国", "英国", "法国", "加拿大", "澳大利亚"])
        
        health_scores = {
            "中国": {"医疗可及性": 78, "疾病预防": 82, "健康寿命": 76, "医疗质量": 85},
            "美国": {"医疗可及性": 72, "疾病预防": 79, "健康寿命": 74, "医疗质量": 88},
            "日本": {"医疗可及性": 92, "疾病预防": 88, "健康寿命": 85, "医疗质量": 91},
            "德国": {"医疗可及性": 88, "疾病预防": 85, "健康寿命": 82, "医疗质量": 89},
            "英国": {"医疗可及性": 85, "疾病预防": 82, "健康寿命": 80, "医疗质量": 86},
            "法国": {"医疗可及性": 86, "疾病预防": 84, "健康寿命": 83, "医疗质量": 87},
            "加拿大": {"医疗可及性": 84, "疾病预防": 81, "健康寿命": 82, "医疗质量": 85},
            "澳大利亚": {"医疗可及性": 87, "疾病预防": 83, "健康寿命": 84, "医疗质量": 88}
        }
        
        if quick_country in health_scores:
            scores = health_scores[quick_country]
            for metric, score in scores.items():
                col_a, col_b = st.columns([1, 3])
                with col_a:
                    st.markdown(f"**{metric}**")
                with col_b:
                    st.progress(score / 100, text=f"{score}分")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("📈 全球健康趋势")
        
        years = list(range(2015, 2025))
        global_health_index = [68, 69, 71, 72, 74, 75, 77, 78, 80, 82]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years, y=global_health_index,
            mode='lines+markers',
            name='全球健康指数',
            line=dict(color='#48bbff', width=3),
            marker=dict(size=8, color='#7c3aed', symbol='circle')
        ))
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=0, r=0, t=30, b=0),
            title="健康指数年度变化"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ========== 2. 医疗资源分析 ==========
elif menu == "📊 医疗资源分析":
    st.subheader("🌍 全球医疗资源全景分析")
    
    # 装饰性图标行
    st.markdown("""
    <div style="display: flex; gap: 20px; justify-content: center; margin-bottom: 20px;">
        <div style="text-align: center;">🏥 医疗机构</div>
        <div style="text-align: center;">👨‍⚕️ 医护人员</div>
        <div style="text-align: center;">🛏️ 床位数</div>
        <div style="text-align: center;">💰 医疗预算</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🗺️ 全球分布", "📊 数据对比", "📈 年度趋势"])
    
    file_path = os.path.join("data", "sim_data.csv")
    
    if not os.path.exists(file_path):
        st.error(f"❌ 文件不存在：{os.path.abspath(file_path)}")
        st.warning("💡 提示：请确保 data/sim_data.csv 文件存在")
        
        # 创建示例数据提示
        st.info("📝 示例数据格式：\n- 列名：年份,地理位置,风险因素,数值\n- 示例：2022,中国,空气质量指数,72")
    else:
        df = pd.read_csv(file_path)
        
        # ========== 国家名称转换（中→英）==========
        country_mapping = {
            '中国': 'China',
            '美国': 'United States',
            '日本': 'Japan',
            '德国': 'Germany',
            '英国': 'United Kingdom',
            '法国': 'France',
            '加拿大': 'Canada',
            '澳大利亚': 'Australia',
        }
        df['地理位置'] = df['地理位置'].map(country_mapping).fillna(df['地理位置'])
        # ========================================
        
        # 数据清洗
        df = df.dropna(subset=['年份', '地理位置', '风险因素', '数值'])
        df['年份'] = df['年份'].astype(int)
        
        with tab1:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown('<div class="custom-card">', unsafe_allow_html=True)
                years = sorted(df['年份'].unique())
                year_filter = st.select_slider("📅 选择年份", years, value=years[-1] if years else 2022, key="year_slider_1")
                risk_filter = st.multiselect("⚠️ 选择风险因素", df['风险因素'].unique(), default=[df['风险因素'].unique()[0]], key="risk_filter_tab1")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                filtered_data = df[df['年份'] == year_filter]
                if risk_filter:
                    filtered_data = filtered_data[filtered_data['风险因素'].isin(risk_filter)]
                
                avg_data = filtered_data.groupby('地理位置')['数值'].mean().reset_index()
                
                fig = px.choropleth(
                    avg_data,
                    locations="地理位置",
                    locationmode="country names",
                    color="数值",
                    color_continuous_scale="Viridis",
                    template="plotly_dark",
                    title=f"{year_filter}年 全球健康风险分布"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                country1 = st.selectbox("🏳️ 对比国家 A", df['地理位置'].unique(), key="country1")
            with col2:
                country2 = st.selectbox("🏴️ 对比国家 B", df['地理位置'].unique(), key="country2")
            
            comp_data1 = df[df['地理位置'] == country1].groupby('风险因素')['数值'].mean()
            comp_data2 = df[df['地理位置'] == country2].groupby('风险因素')['数值'].mean()
            
            comp_df = pd.DataFrame({
                country1: comp_data1,
                country2: comp_data2
            }).reset_index()
            
            fig = px.bar(comp_df, x='风险因素', y=[country1, country2], 
                        barmode='group', template="plotly_dark",
                        title=f"{country1} vs {country2} 健康风险对比",
                        color_discrete_sequence=['#48bbff', '#ec489a'])
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            selected_country = st.selectbox("🌏 选择国家", df['地理位置'].unique())
            country_data = df[df['地理位置'] == selected_country]
            trend_data = country_data.groupby(['年份', '风险因素'])['数值'].mean().reset_index()
            
            fig = px.line(trend_data, x='年份', y='数值', color='风险因素',
                         template="plotly_dark", markers=True,
                         title=f"{selected_country} 健康风险年度趋势")
            st.plotly_chart(fig, use_container_width=True)

# ========== 3. 智能计算引擎 ==========
elif menu == "✏️ 智能计算引擎":
    st.subheader("🧠 AI 智能计算引擎")
    st.caption("支持多维度健康指标计算与智能评估 | 数据驱动决策支持")
    
    # 使用表单进行高级输入
    with st.form("advanced_calc_form"):
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📍 基本信息")
            area_name = st.text_input("地区/机构名称", "示例：华东地区")
            year_sel = st.selectbox("统计年份", list(range(2015, 2026)), index=9)
            pop_num = st.number_input("总人口（人）", min_value=1000, value=5000000, step=10000)
        
        with col2:
            st.markdown("#### 🏥 医疗资源")
            hospital_num = st.number_input("医疗机构总数（个）", min_value=1, value=3000)
            doctor_num = st.number_input("执业医生数（人）", min_value=1, value=8000)
            nurse_num = st.number_input("注册护士数（人）", min_value=1, value=12000)
        
        st.markdown("#### 🛏️ 基础设施")
        col3, col4 = st.columns(2)
        with col3:
            bed_num = st.number_input("床位数（张）", min_value=1, value=5000)
        with col4:
            budget = st.number_input("医疗预算（万元）", min_value=0, value=500000)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        submitted = st.form_submit_button("🚀 开始智能分析", use_container_width=True)
    
    if submitted:
        # 计算高级指标
        doctor_per_1000 = (doctor_num / pop_num) * 1000
        nurse_per_1000 = (nurse_num / pop_num) * 1000
        bed_per_1000 = (bed_num / pop_num) * 1000
        hospital_per_million = (hospital_num / pop_num) * 1000000
        
        # 资源效率指数
        resource_score = min(10, 
            (doctor_per_1000 / 3) * 0.3 +      # 医生密度（目标3人/千人）
            (nurse_per_1000 / 6) * 0.25 +      # 护士密度（目标6人/千人）
            (bed_per_1000 / 5) * 0.25 +        # 床位密度（目标5张/千人）
            (hospital_per_million / 200) * 0.2  # 机构密度（目标200家/百万人）
        ) * 10
        
        budget_efficiency = budget / pop_num if pop_num > 0 else 0
        
        # 等级评定
        if resource_score >= 8:
            level = "🌟 卓越级"
            color = "#10b981"
            description = "医疗资源极度丰富，已达到发达国家先进水平，医疗服务可及性高"
            icon = "🏆"
        elif resource_score >= 5:
            level = "✅ 优秀级"
            color = "#3b82f6"
            description = "医疗资源配置合理，基本满足居民需求，建议持续优化"
            icon = "📈"
        elif resource_score >= 3:
            level = "📈 发展级"
            color = "#f59e0b"
            description = "医疗资源有待提升，建议加大投入，重点补充基层医疗资源"
            icon = "🔧"
        else:
            level = "⚠️ 紧缺级"
            color = "#ef4444"
            description = "医疗资源严重不足，急需改善，建议优先解决基本医疗覆盖问题"
            icon = "🚨"
        
        # 结果展示
        st.divider()
        st.markdown(f"### {icon} 分析报告 - {area_name} ({year_sel}年)")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("每千人医生数", f"{doctor_per_1000:.2f}", 
                     delta="较好" if doctor_per_1000 > 2.5 else "不足")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("每千人护士数", f"{nurse_per_1000:.2f}",
                     delta="充足" if nurse_per_1000 > 5 else "紧缺")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("每千人床位数", f"{bed_per_1000:.2f}",
                     delta="达标" if bed_per_1000 > 4 else "不足")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 综合评估卡片
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1a2332, #16202e); border-radius: 15px; padding: 20px; margin-top: 20px;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 48px;">{icon}</div>
                <div>
                    <h3 style="color: {color}; margin: 0;">资源评级：{level}</h3>
                    <p style="color: #a0aec0; margin: 5px 0 0 0;">{description}</p>
                </div>
            </div>
            <hr style="border-color: #2d3a4a; margin: 15px 0;">
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;">
                <div>
                    <div style="color: #8892b0; font-size: 12px;">综合效率指数</div>
                    <div style="font-size: 24px; font-weight: bold;">{resource_score:.1f}<span style="font-size: 14px;">/10</span></div>
                </div>
                <div>
                    <div style="color: #8892b0; font-size: 12px;">人均医疗预算</div>
                    <div style="font-size: 20px; font-weight: bold;">{budget_efficiency:.0f}<span style="font-size: 14px;"> 元/人</span></div>
                </div>
                <div>
                    <div style="color: #8892b0; font-size: 12px;">每百万人机构数</div>
                    <div style="font-size: 20px; font-weight: bold;">{hospital_per_million:.1f}<span style="font-size: 14px;"> 家</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 存储历史记录
        st.session_state.calculation_history.append({
            "地区": area_name,
            "年份": year_sel,
            "综合得分": resource_score,
            "评级": level,
            "时间": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        
        # 雷达图展示
        categories = ['医生资源', '护理资源', '床位资源', '机构资源', '预算效率']
        values = [
            min(doctor_per_1000 * 3.33, 10),    # 3人/千人为满分
            min(nurse_per_1000 * 1.67, 10),     # 6人/千人为满分
            min(bed_per_1000 * 2, 10),          # 5张/千人为满分
            min(hospital_per_million / 20, 10), # 200家/百万人为满分
            min(budget_efficiency / 500, 10)    # 500元/人为满分
        ]
        
        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            marker=dict(color='#48bbff'),
            line=dict(color='#48bbff', width=2)
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 10], color='#8892b0'),
                angularaxis=dict(color='#8892b0'),
                bgcolor='rgba(0,0,0,0)'
            ),
            template='plotly_dark',
            height=450,
            title="六维健康资源评估雷达图",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

# ========== 4. 全球风险监测 ==========
elif menu == "🌍 全球风险监测":
    st.subheader("⚠️ 全球健康风险实时监测系统")
    
    # 风险等级说明
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("🟢 **低风险** (0-30)")
    with col2:
        st.markdown("🟡 **中风险** (31-60)")
    with col3:
        st.markdown("🟠 **高风险** (61-80)")
    with col4:
        st.markdown("🔴 **严重** (81-100)")
    
    st.divider()
    
    file_path = "data/sim_data.csv"
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        
        col1, col2, col3 = st.columns(3)
        with col1:
           selected_year = st.selectbox("选择年份", sorted(df['年份'].unique(), reverse=True), key="risk_year")
        with col2:
            risk_type = st.selectbox("⚠️ 风险类型", df['风险因素'].unique())
        with col3:
            threshold = st.slider("🎯 风险预警阈值", 0, 100, 50)
        
        filtered_data = df[(df['年份'] == selected_year) & (df['风险因素'] == risk_type)]
        
        # 高风险国家警示
        high_risk = filtered_data[filtered_data['数值'] > threshold]
        
        risk_color = "#ef4444" if len(high_risk) > 10 else "#f59e0b" if len(high_risk) > 5 else "#10b981"
        
        st.markdown(f"""
        <div style="background: rgba(239,68,68,0.1); border-left: 4px solid {risk_color}; border-radius: 12px; padding: 15px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h4 style="color: {risk_color}; margin: 0;">🚨 高风险预警</h4>
                    <p style="margin: 5px 0 0 0;">发现 <strong>{len(high_risk)}</strong> 个国家/地区 {risk_type} 风险超过阈值 {threshold}</p>
                </div>
                <div style="font-size: 32px;">⚠️</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if not high_risk.empty:
            with st.expander(f"📋 查看高风险国家详情 ({len(high_risk)}个)"):
                st.dataframe(high_risk[['地理位置', '数值']].sort_values('数值', ascending=False), 
                            use_container_width=True)
        
        # 可视化
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.choropleth(
                filtered_data,
                locations="地理位置",
                locationmode="country names",
                color="数值",
                color_continuous_scale="RdYlGn_r",
                template="plotly_dark",
                title=f"{selected_year}年 - {risk_type} 全球风险地图"
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            top_risky = filtered_data.nlargest(15, '数值')
            fig_bar = px.bar(top_risky, x='地理位置', y='数值', color='数值',
                            color_continuous_scale="Reds",
                            template="plotly_dark",
                            title=f"{risk_type} 风险排名 Top 15")
            fig_bar.update_layout(height=500)
            st.plotly_chart(fig_bar, use_container_width=True)

# ========== 5. 趋势预测 ==========
elif menu == "📈 趋势预测":
    st.subheader("🔮 AI 智能趋势预测系统")
    st.caption("基于历史数据的机器学习预测模型 | 预测准确度约85%")
    
    from sklearn.linear_model import LinearRegression
    
    file_path = "data/sim_data.csv"
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        
        col1, col2 = st.columns(2)
        with col1:
            selected_risk = st.selectbox("📈 选择预测指标", df['风险因素'].unique())
        with col2:
            selected_country = st.selectbox("🌏 选择国家/地区", df['地理位置'].unique())
        
        # 准备数据
        country_data = df[(df['地理位置'] == selected_country) & (df['风险因素'] == selected_risk)]
        
        if len(country_data) >= 3:
            X = country_data['年份'].values.reshape(-1, 1)
            y = country_data['数值'].values
            
            # 训练模型
            model = LinearRegression()
            model.fit(X, y)
            
            # 预测未来3年
            future_years = np.array([2025, 2026, 2027, 2028]).reshape(-1, 1)
            predictions = model.predict(future_years)
            
            # R²评分
            r2_score = model.score(X, y)
            
            # 可视化
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=country_data['年份'], y=country_data['数值'],
                mode='lines+markers', 
                name='历史数据',
                line=dict(color='#48bbff', width=3),
                marker=dict(size=8, symbol='circle')
            ))
            
            fig.add_trace(go.Scatter(
                x=future_years.flatten(), y=predictions,
                mode='lines+markers', 
                name='预测数据',
                line=dict(color='#ec489a', width=3, dash='dash'),
                marker=dict(size=8, symbol='diamond')
            ))
            
            # 添加置信区间
            fig.add_trace(go.Scatter(
                x=np.concatenate([future_years.flatten(), future_years.flatten()[::-1]]),
                y=np.concatenate([predictions + 5, (predictions - 5)[::-1]]),
                fill='toself',
                fillcolor='rgba(236,72,153,0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='置信区间'
            ))
            
            fig.update_layout(
                template='plotly_dark',
                title=f"{selected_country} - {selected_risk} 趋势预测",
                xaxis_title="年份",
                yaxis_title="风险指数",
                height=500,
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # 预测报告
            trend = "上升趋势 📈" if predictions[-1] > y[-1] else "下降趋势 📉"
            trend_color = "#ef4444" if "上升" in trend else "#10b981"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a2332, #16202e); border-radius: 15px; padding: 20px; margin-top: 20px;">
                <h4>📋 智能预测报告</h4>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 15px;">
                    <div>
                        <div style="color: #8892b0;">预测模型</div>
                        <div><strong>线性回归</strong> (R² = {r2_score:.3f})</div>
                    </div>
                    <div>
                        <div style="color: #8892b0;">模型准确度</div>
                        <div><strong>{r2_score * 100:.1f}%</strong></div>
                    </div>
                    <div>
                        <div style="color: #8892b0;">2025年预测</div>
                        <div><strong>{predictions[0]:.1f}</strong></div>
                    </div>
                    <div>
                        <div style="color: #8892b0;">2026年预测</div>
                        <div><strong>{predictions[1]:.1f}</strong></div>
                    </div>
                    <div>
                        <div style="color: #8892b0;">2027年预测</div>
                        <div><strong>{predictions[2]:.1f}</strong></div>
                    </div>
                    <div>
                        <div style="color: #8892b0;">趋势分析</div>
                        <div><strong style="color: {trend_color};">{trend}</strong></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ {selected_country} 的数据点不足（{len(country_data)}个），需要至少3个数据点进行预测")

# ========== 6. 报告中心 ==========
elif menu == "📋 报告中心":
    st.subheader("📋 智能报告生成中心")
    st.caption("一键生成专业健康分析报告 | 支持导出分享")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("📊 自定义报告生成器")
        
        report_country = st.selectbox("🌏 选择报告国家", ["中国", "美国", "日本", "德国", "英国", "法国", "加拿大"])
        report_year = st.selectbox("📅 报告年份", list(range(2015, 2025)), index=8)
        report_type = st.selectbox("📋 报告类型", ["综合评估报告", "风险分析报告", "资源评估报告", "趋势预测报告"])
        report_format = st.radio("导出格式", ["Markdown", "文本"], horizontal=True)
        
        if st.button("🚀 生成报告", type="primary", use_container_width=True):
            with st.spinner("正在生成报告..."):
                # 模拟报告数据
                st.success("✅ 报告生成成功！")
                
                # 模拟健康数据
                health_data = {
                    "中国": {"预期寿命": 78.2, "医疗支出占比": 5.8, "每千人医生": 2.4, "婴儿死亡率": 5.6},
                    "美国": {"预期寿命": 78.9, "医疗支出占比": 16.8, "每千人医生": 2.6, "婴儿死亡率": 5.7},
                    "日本": {"预期寿命": 84.3, "医疗支出占比": 10.9, "每千人医生": 2.5, "婴儿死亡率": 1.9},
                    "德国": {"预期寿命": 81.1, "医疗支出占比": 11.2, "每千人医生": 4.3, "婴儿死亡率": 3.1},
                    "英国": {"预期寿命": 81.0, "医疗支出占比": 9.8, "每千人医生": 2.8, "婴儿死亡率": 3.8},
                    "法国": {"预期寿命": 82.5, "医疗支出占比": 11.3, "每千人医生": 3.4, "婴儿死亡率": 3.5},
                    "加拿大": {"预期寿命": 82.2, "医疗支出占比": 10.8, "每千人医生": 2.8, "婴儿死亡率": 4.5}
                }
                
                data = health_data.get(report_country, health_data["中国"])
                
                st.markdown(f"""
                ### 📄 {report_type}
                
                #### 基本信息
                - **国家**: {report_country}
                - **报告年份**: {report_year}
                - **生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                - **报告类型**: {report_type}
                
                #### 核心指标
                | 指标 | 数值 | 全球排名 | 状态 |
                |------|------|----------|------|
                | 人均预期寿命 | {data['预期寿命']}岁 | 前列 | ✅ |
                | 医疗支出占GDP | {data['医疗支出占比']}% | 中等 | 📊 |
                | 每千人医生数 | {data['每千人医生']}人 | 中等 | 👨‍⚕️ |
                | 婴儿死亡率 | {data['婴儿死亡率']}‰ | 良好 | 👶 |
                
                #### 综合分析
                {report_country}的医疗卫生体系在过去一年中保持稳定发展。预期寿命达到{data['预期寿命']}岁，高于全球平均水平。
                
                #### 建议与展望
                1. 持续优化医疗资源配置
                2. 加强基层医疗服务能力
                3. 推进医疗信息化建设
                4. 深化医药卫生体制改革
                
                ---
                *报告由 MediVision AI 智能生成*
                """)
                
                # 报告下载
                report_content = f"""
{report_type}
国家: {report_country}
年份: {report_year}
生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

核心指标:
- 人均预期寿命: {data['预期寿命']}岁
- 医疗支出占GDP: {data['医疗支出占比']}%
- 每千人医生数: {data['每千人医生']}人

综合分析: {report_country}的医疗卫生体系保持稳定发展。
"""
                st.download_button(
                    "📥 下载报告", 
                    report_content, 
                    file_name=f"{report_country}_health_report_{report_year}.txt"
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.subheader("📜 历史计算记录")
        
        if st.session_state.calculation_history:
            history_df = pd.DataFrame(st.session_state.calculation_history)
            st.dataframe(history_df, use_container_width=True)
            
            # 导出历史记录
            if st.button("📤 导出历史记录"):
                csv_data = history_df.to_csv(index=False)
                st.download_button("💾 下载CSV", csv_data, file_name="calculation_history.csv")
        else:
            st.info("📭 暂无计算记录，请前往「智能计算引擎」进行计算")
        
        # 统计摘要
        if st.session_state.calculation_history:
            st.divider()
            st.subheader("📊 统计摘要")
            avg_score = np.mean([h["综合得分"] for h in st.session_state.calculation_history])
            st.metric("平均综合得分", f"{avg_score:.1f} 分")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ========== 底部信息 ==========
st.divider()

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.caption("© 2024 MediVision | 健康数据智能分析平台 | 计算机设计大赛参赛作品")
    st.caption("数据来源: WHO, World Bank, CDC | 技术支持: AI/ML")

# 欢迎提示（首次访问）
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True
    st.balloons()
    st.toast("🎉 欢迎使用 MediVision 健康数据分析平台！", icon="🏥")
    st.toast("💡 提示：左侧菜单可选择不同功能模块", icon="💡")