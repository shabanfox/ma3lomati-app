import streamlit as st
import pandas as pd
import feedparser
import time
import random
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'cache_key' not in st.session_state: st.session_state.cache_key = random.randint(1, 999999)

# 3. جلب الأخبار
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "جاري تحديث الأخبار العقارية..."
    except: return "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."

news_text = get_real_news()

# 4. التنسيق الجمالي (UI/UX)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    /* الهيدر الذهبي */
    .luxury-header {{
        background: rgba(15, 15, 15, 0.95); backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b; padding: 15px 30px;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; border-radius: 0 0 25px 25px; margin-bottom: 15px;
    }}
    .logo-text {{ color: #f59e0b; font-weight: 900; font-size: 26px; letter-spacing: 1px; }}
    
    /* شريط الأخبار */
    .ticker-wrap {{ width: 100%; background: transparent; padding: 8px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 15px; }}
    .ticker {{ display: inline-block; animation: ticker 120s linear infinite; color: #aaa; font-size: 14px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* الكروت الاحترافية (تصميم نوي) */
    div.stButton > button[key*="card_"] {{
        background: white !important;
        color: #1a1a1a !important;
        border: none !important;
        border-radius: 20px !important;
        width: 100% !important;
        min-height: 240px !important;
        padding: 25px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        text-align: right !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
        white-space: pre-wrap !important;
        line-height: 1.7 !important;
    }}
    div.stButton > button[key*="card_"]:hover {{
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 15px 30px rgba(245, 158, 11, 0.3) !important;
        background: #fdfdfd !important;
    }}

    /* الاستلام الفوري الجانبي */
    .ready-sidebar-container {{
        background: #0d0d0d; border: 1px solid #222; border-radius: 20px; padding: 15px;
        max-height: 75vh; overflow-y: auto; border-top: 4px solid #10b981;
    }}
    .ready-card {{ background: #161616; border-right: 4px solid #10b981; padding: 12px; border-radius: 10px; margin-bottom: 10px; transition: 0.3s; }}
    .ready-card:hover {{ background: #222; }}
    .ready-title {{ color: #f59e0b; font-size: 15px; font-weight: bold; margin-bottom: 4px; }}
    
    .info-label {{ color: #f59e0b; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# 5. نظام الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:120px;'><h1 style='color:#f59e0b; font-size:50px;'>MA3LOMATI <span style='color:white'>PRO</span></h1>", unsafe_allow_html=True)
