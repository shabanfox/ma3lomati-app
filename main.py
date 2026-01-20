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

# --- حماية زر الرجوع في الموبايل ---
st.components.v1.html("""
<script>
    window.onbeforeunload = function() { return "هل تريد المغادرة؟"; };
    history.pushState(null, null, location.href);
    window.onpopstate = function () { history.go(1); };
</script>
""", height=0)

# 2. التنسيق الجمالي (CSS) - أبيض محاط بذهبي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container { padding-top: 0rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    
    /* الخلفية والخطوط العامة */
    [data-testid="stAppViewContainer"] { 
        background-color: #0a192f; 
        direction: rtl !important; 
        text-align: right !important; 
        font-family: 'Cairo', sans-serif; 
    }
    
    /* نصوص بيضاء واضحة جداً مع ظل ذهبي خفيف للوضوح */
    p, span, label, .stWrite, .stMetric div { 
        color: #ffffff !important; 
        font-weight: 600 !important;
        text-shadow: 0px 0px 5px rgba(245, 158, 11, 0.2);
    }
    
    /* العناوين ذهبية واضحة */
    h1, h2, h3, h4 { 
        color: #f59e0b !important; 
        font-weight: 900 !important;
        text-shadow: 1px 1px 2px #000;
    }

    /* كروت المشاريع - كتابة بيضاء داخل برواز ذهبي */
    div.stButton > button {
        background: #112240 !important;
        color: #ffffff !important;
        border: 2px solid #f59e0b !important; /* برواز ذهبي حول الكتابة */
        border-radius: 12px !important;
        min-height: 120px !important; 
        width: 100% !important;
        font-size: 16px !important;
        font-weight: bold !important;
        box-shadow: inset 0 0 10px rgba(245, 158, 11, 0.1) !important;
    }
    
    div.stButton > button:hover {
        background: #f59e0b !important;
        color: #000000 !important;
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.4) !important;
    }

    /* الصناديق والمحتوى */
    .smart-box { 
        background: #112240; 
        border: 2px solid #f59e0b; 
        padding: 25px; 
        border-radius: 20px; 
        color: #ffffff;
    }

    /* تحسين شكل المدخلات */
    input { 
        color: white !important; 
        background-color: #0d1e36 !important; 
        border: 1px solid #f59e0b !important; 
    }
    
    /* التبويبات Tabs */
    .stTabs [data-baseweb="tab"] { color: #ffffff !important; font-size: 18px !important; }
    .stTabs [aria-selected="true"] { 
        color: #f59e0b !important; 
        border-bottom: 3px solid #f59e0b !important;
    }
    </style>
""", unsafe_allow_html=True)

# (بقية الكود الخاص بالبيانات والمنطق - لم يتغير لضمان العمل)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_now = datetime.now(pytz.timezone('Africa/Cairo'))

@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p
    except: return pd.DataFrame()

df_p = load_data()

# --- واجهة الدخول ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; padding-top:50px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1.5,1])
    with c2:
        u_in = st.text_input("الأسم")
        p_in = st.text_input("كلمة السر", type="password")
        if st.button("دخول 🚀"):
            if p_in == "2026":
                st.session_state.auth, st.session_state.current_user = True, "Admin"
                st.rerun()
    st.stop()

# --- الواجهة الرئيسية ---
st.markdown(f"""<div class='smart-box' style='text-align:center; border-radius:0 0 30px 30px;'>
    <h1 style='margin:0;'>MA3LOMATI PRO</h1>
    <p style='color:#ffffff !important; border: 1px solid #f59e0b; display: inline-block; padding: 5px 15px; border-radius: 10px;'>
        مرحباً {st.session_state.current_user} | {egypt_now.strftime('%I:%M %p')}
    </p>
</div>""", unsafe_allow_html=True)

menu = option_menu(None, ["المشاريع", "المساعد الذكي", "أدوات البروكر"], 
    icons=["search", "robot", "calculator"], orientation="horizontal",
    styles={"container": {"background-color": "#0d1e36"}, "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"<div class='smart-box'><h2>{item['ProjectName']}</h2><p>الموقع: {item['Location']}</p></div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    search = st.text_input("🔍 ابحث عن اسم المشروع")
    dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
    for i in range(0, len(dff.head(6)), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(dff):
                row = dff.iloc[i+j]
                if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}", key=f"btn_{i+j}"):
                    st.session_state.selected_item = row; st.rerun()

st.markdown("<p style='text-align:center; color:#555; padding-top:30px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
