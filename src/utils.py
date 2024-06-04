import yaml
import streamlit as st

def get_api_key():
    with open('config/api_key.txt', 'r') as file:
        return file.read().strip()

def get_roadmap():
    with open('config/roadmap.yaml', 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)
    
STAGE_COLORS = {
    "Lock": "rgba(206, 205, 202, 0.5)",
    "Ready": "rgba(221, 0, 129, 0.2)",
    "working": "rgba(0, 135, 107, 0.2)",
    "Done": "rgba(140, 46, 0, 0.2)",
}
STAGE_SHORT_NAMES = {
    "Lock" : "🔒Lock",
    "Ready": "🔓 Ready",
    "Studying": "👷 Studying",
    "Done": "✅ Launched",
}

STAGE = [
    "Lock", "Ready", "Studying", "Done"
]

PHASE = [
    "🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"
]

def get_stage_tag(stage):
    color = STAGE_COLORS.get(stage, "rgba(206, 205, 202, 0.5)")
    short_name = STAGE_SHORT_NAMES.get(stage, stage)
    return (
        f'<span style="background-color: {color}; padding: 1px 6px; '
        "margin: 0 5px; display: inline; vertical-align: middle; "
        f"border-radius: 0.25rem; font-size: 0.75rem; font-weight: 400; "
        f'white-space: nowrap">{short_name}'
        "</span>"
    )

def get_from_url_param(param_name):
    """
    从 URL 参数中获取值并设置为页面标题
    :param param_name: URL 参数的名称
    """
    query_params = st.query_params
    param_value = query_params.get(param_name, [''])
    return param_value
       
