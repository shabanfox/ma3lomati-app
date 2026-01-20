import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- منع الخروج بالخطأ عند الضغط على Back في الموبايل ---
st.components.v1.html("""
<script>
    window.onbeforeunload = function() { return "هل تريد المغادرة؟"; };
    history.pushState(null, null, location.href);
    window.onpopstate = function () { history.go(1); };
</script>
""", height=0)

# 2. التنسيق الجمالي (CSS) - ألوان فائقة الوضوح
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container { padding-top: 1rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    
    /* الخلفية الملكية */
    [data-testid="stAppViewContainer"] { 
        background-color: #0a192f; 
        direction: rtl !important; 
        text-align: right !important; 
        font-family: 'Cairo', sans-serif; 
    }
    
    /* جعل كل النصوص بيضاء وواضحة جداً */
    p, span, label, .stWrite, .stMetric div { 
        color: #ffffff !important; 
        font-weight: 600 !important; 
    }
    
    /* العناوين بالذهبي المضيء */
    h1, h2, h3, h4 { 
        color: #f59e0b !important; 
        font-weight: 900 !important; 
    }

    /* كروت المشاريع - كتابة بيضاء Bold */
    div.stButton > button {
        background: linear-gradient(145deg, #112240, #0a192f) !important;
        color: #ffffff !important;
        border: 1px solid #233554 !important;
        border-right: 6px solid #f59e0b !important;
        border-radius: 12px !important;
        min-height: 120px !important;
        width: 100% !important;
        font-size: 17px !important;
        font-weight: bold !important;
        margin-bottom: 15px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
    }
    
    div.stButton > button:hover {
        border-color: #f59e0b !important;
        color: #f59e0b !important;
        transform: translateY(-3px);
    }

    /* صناديق المحتوى */
    .smart-box { 
        background: #112240; 
        border: 1px solid #233554; 
        padding: 25px; 
        border-radius: 20px; 
        border-right: 6px solid #f59e0b; 
        margin-bottom: 20px;
    }

    /* تحسين شكل المدخلات (Inputs) */
    input { color: white !important; background-color: #0d1e36 !important; border: 1px solid #233554 !important; }
    div[data-baseweb="select"] { background-color: #0d1e36 !important; }
    div[data-baseweb="select"] * { color: white !important; }
    
    /* شريط الأخبار */
    .ticker-wrap { background: #112240; border-bottom: 2px solid #f59e0b; padding: 10px; }
    .ticker { color: #f59e0b !important; font-weight: bold; font-size: 15px; }

    /* التبويبات Tabs */
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; }
    .stTabs [aria-selected="true"] { color: #f59e0b !important; border-bottom-color: #f59e0b !important; }
</style>
""", unsafe_allow_html=True)

# 3. إدارة الحالة والبيانات
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        p = pd.read_csv
