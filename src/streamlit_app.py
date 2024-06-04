import streamlit as st
from utils import get_roadmap, get_stage_tag, PHASE, STAGE

# 配置 Streamlit 页面
st.set_page_config("EduGame", "https://streamlit.io/favicon.svg")

# 显示欢迎信息
st.write(
    """
    # Edu:blue[Game] 🏫

    欢迎来到面向小学数学学科的生成式人工智能故事化教育游戏! 👋 

    一起通过游戏来学习小学1-3年级的数学知识点吧！✨

    """
)

st.divider()

# 获取路线图数据
data = get_roadmap()

# 显示每个知识点
for index in data:
    st.subheader(index)
    for idx, (key, value) in enumerate(data[index].items()):
        stage = get_stage_tag(STAGE[idx % len(STAGE)])
        description = f"<br /><small style='color: #808495'>{value}</small>"
        a, b = st.columns([0.03, 0.97])
        phase = PHASE[idx % len(PHASE)]
        a.markdown(phase)
        b.markdown(f"<strong>[{key}](chat?knowledge={key})</strong> {stage}{description}", unsafe_allow_html=True)
