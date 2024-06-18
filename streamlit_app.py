import streamlit as st
from openai import OpenAI
from utils import get_roadmap, get_stage_tag, PHASE, save_roadmap, reset_roadmap
import config.prompt as prompt
import os

# 获取查询参数
query_params = st.query_params

# 获取 "knowledge" 参数的值
selected_knowledge = query_params.get("knowledge", None)
        
# Initialization
st.set_page_config(page_title="EduGame", page_icon="🏫")

data = get_roadmap()

if 'selected_knowledge' not in st.session_state:
    if selected_knowledge:
        st.session_state['selected_knowledge'] = selected_knowledge
    else: 
        st.session_state['selected_knowledge'] = None

if 'selected_knowledge_stage' not in st.session_state:
    if selected_knowledge:
        st.session_state['selected_knowledge_stage'] = data["三年级数学上册"][selected_knowledge]["stage"]
    else: 
        st.session_state['selected_knowledge_stage']  = None

if 'pic_url' not in st.session_state:
    st.session_state['pic_url']  = None

# 重置对话窗口
@st.experimental_dialog("⚠️注意！")
def reset():
    st.markdown("请确定是否要重置！所有的记录都会被:red[**删除**]")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("确定", type="primary", use_container_width=True):
            reset_roadmap()
            st.rerun()  # 重新运行应用，关闭对话框
    with col2:
        if st.button("取消", use_container_width=True):
            st.rerun()  # 重新运行应用，关闭对话框

# Sidebar  
st.sidebar.write(
    """
    # Edu:blue[Game]'s 知识点
    """
)

# 🏠 主页 Button
if st.sidebar.button("🏠 主页",  use_container_width=True):
    st.query_params.clear()

# 重置 Button
if "reset" not in st.session_state:
    if st.sidebar.button('⚠️ 重置', type="primary", use_container_width=True):
        reset()

# 知识点目录
with st.sidebar.container():
    for index in data:
        st.sidebar.subheader(index)
        for idx, (key, value) in enumerate(data[index].items()):
            if "questions" not in value or not value["questions"]:
                stage = "Lock"
            else:
                stage = data[index][key]["stage"]
            stage_tag = get_stage_tag(stage)
            description = f"<br /><small style='color: #808495'>{value['description']}</small>"
            a, b = st.sidebar.columns([0.04, 0.96])
            phase = PHASE[idx % len(PHASE)]
            a.markdown(phase)
            if stage == "Lock":
                b.markdown(f":grey[<strong>{key}</strong>] {stage_tag}{description}", unsafe_allow_html=True)
            else:
                b.markdown(f"<strong>[{key}](?knowledge={key})</strong> {stage_tag}{description}", unsafe_allow_html=True)
        
# 主界面
if st.session_state['selected_knowledge'] == None:                  # 未选择知识点时
    st.write(
    """
    # Edu:blue[Game] 🏫

    欢迎来到面向小学数学学科的生成式人工智能故事化教育游戏! 👋 

    一起通过游戏来学习小学1-3年级的数学知识点吧！✨
    """
    )
    st.info('左侧栏可以看到当前学习状态，请点击你要开始的知识点吧！', icon="ℹ️")

elif st.session_state['selected_knowledge_stage'] == "Done":        # 知识点状态为完成
    st.header(f" {st.session_state['selected_knowledge']}的:blue[完成结果]")
    
    # 评语
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "assistant",
            "content": [
                {
                "type": "text",
                "text": prompt.history_prompt + str(data["三年级数学上册"][selected_knowledge]["history"])
                }
            ]
            }
        ],
        temperature=1,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    msg = response.choices[0].message.content
    st.markdown(msg)

    # 历史聊天记录
    st.markdown("## 对话记录如下：")
    for msg in data["三年级数学上册"][selected_knowledge]["history"]:
        if msg["role"] in ["user", "assistant"]:
            st.chat_message(msg["role"]).write(msg["content"])

else:                                                               # 选择可选知识点
    st.header(f":blue[知识点] {st.session_state['selected_knowledge']}")

    # 生成故事背景
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    if "messages" not in st.session_state:
        # 生成第一句提示
        st.session_state["messages"] = [
            {
                "role": "system",
                "content": [
                    {
                    "type": "text",
                    "text": prompt.instruction + str(data["三年级数学上册"][st.session_state['selected_knowledge']]["questions"])
                    }
                ]
            },
        ]
        response = client.chat.completions.create(
            model="gpt-4-turbo", 
            messages=st.session_state.messages,
            temperature=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})

        # 生成故事背景图
        response = client.images.generate(
            model="dall-e-3",
            prompt=msg,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        st.session_state['pic_url'] = response.data[0].url
        
    st.image(st.session_state['pic_url'], use_column_width=True)

    # 输出聊天消息
    for msg in st.session_state["messages"]:
        if msg["role"] in ["user", "assistant"]:
            st.chat_message(msg["role"]).write(msg["content"])

    # 输入框
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(
            model="gpt-4-turbo", 
            messages=st.session_state.messages,
            temperature=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

    # 完成知识点
    if "你已经成功地解开了我们所有的谜题。" in msg:
            st.session_state['selected_knowledge_stage'] = "Done"
            data["三年级数学上册"][selected_knowledge]["stage"] = "Done"
            data["三年级数学上册"][selected_knowledge]["history"] = st.session_state.messages
            save_roadmap(data)
            st.balloons()
            st.info('输入任意信息结束当前游戏', icon="ℹ️")
            