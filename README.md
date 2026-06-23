📖 项目简介
MediVision 是一个基于 Streamlit 构建的全球健康智能分析平台，集成了数据可视化、AI预测、风险评估和资源优化等核心功能。平台以直观的交互方式展示全球健康数据，帮助用户洞察健康趋势，辅助决策。

✨ 核心亮点
🏥 8大功能模块：从数据驾驶舱到报告中心，覆盖健康分析全流程

🌍 全球数据覆盖：195个国家/地区，20+健康风险因素，24年历史数据

🤖 AI智能分析：集成机器学习预测、聚类分析和智能评估

📊 丰富的可视化：地图、图表、雷达图、热力图等多种展示形式

📱 响应式设计：适配桌面和移动设备，交互流畅

🎯 功能模块
模块	功能描述	核心能力
🏠 数据驾驶舱	全局健康数据概览	关键指标、健康评估、趋势展示
📊 医疗资源分析	全球医疗资源分布	地理分布、数据对比、年度趋势
✏️ 智能计算引擎	自定义健康评估	多维度计算、资源评级、雷达图
🌍 全球风险监测	实时风险预警	风险地图、阈值预警、排名分析
📊 国家聚类分析	健康水平分组	K-Means聚类、治理类型识别
📈 趋势预测	AI智能预测	线性回归、置信区间、趋势分析
📊 资源优化	资源配置方案	预算优化、效果预估、策略建议
📋 报告中心	智能报告生成	一键生成、历史记录、导出下载
🚀 快速开始
环境要求
Python 3.9+

pip 包管理器

安装步骤
bash
# 1. 克隆仓库
git clone [https://github.com/yourusername/medivision.git](https://github.com/xllyiiiii/health_platform)
cd medivision

# 2. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行应用
streamlit run main.py
数据准备
将数据文件放在 data/ 目录下：

bash
data/
├── sim_data.csv       # 模拟数据示例
└── your_data.csv      # 自定义数据
数据格式要求：

csv
年份,地理位置,风险因素,数值
2022,中国,空气质量指数,72
2022,美国,医疗可及性,85
📊 数据源
世界卫生组织 (WHO) - 全球健康统计数据

世界银行 (World Bank) - 经济发展与健康指标

美国疾控中心 (CDC) - 疾病预防与控制数据

综合模拟数据 - 用于演示和测试

🛠️ 技术栈
前端
Streamlit - 应用框架

Plotly - 交互式可视化

Custom CSS - 自定义样式

后端
Python - 核心语言

Pandas - 数据处理

NumPy - 数值计算

AI/ML
Scikit-learn - 机器学习

K-Means 聚类

线性回归预测

StandardScaler 标准化

