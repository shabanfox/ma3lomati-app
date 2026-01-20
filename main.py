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
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (الريفريش)
query_params = st.query_params
if 'auth' not in st.session_state:
    if "u" in query_params:
        st.session_state.auth = True
        st.session_state.current_user = query_params["u"]
    else:
        st.session_state.auth = False

# 3. روابط البيانات والتوقيت
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# 4. التنسيق الجمالي المطور (Elite CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    [data-testid="stAppViewContainer"] {{ background-color: #000000; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; padding-left: 0.5rem !important; padding-right: 0.5rem !important; }}

    /* الهيدر الفخم */
    .elite-header {{
        background: linear-gradient(135deg, #1a1a1a 0%, #000000 100%);
        padding: 30px 20px;
        border-bottom: 2px solid #D4AF37;
        text-align: center;
        border-radius: 0 0 40px 40px;
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.15);
        margin-bottom: 20px;
    }}
    
    .elite-header h1 {{
        color: #D4AF37 !important;
        font-size: 35px !important;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 2px;
    }}

    /* نصوص واضحة جداً */
    p, span, div, label {{ color: #FFFFFF !important; font-weight: 600 !important; }}
    
    /* زر الخروج العلوي */
    .stButton > button[key="logout_top"] {{
        background-color: #8b0000 !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 5px 20px !important;
        font-size: 14px !important;
        position: fixed;
        top: 15px;
        left: 15px;
        z-index: 1000;
    }}

    /* المنيو المضغوط للموبايل */
    .nav-link {{ padding: 8px !important; font-size: 13px !important; }}
    
    /* الكروت الذهبية */
    div.stButton > button[key*="card_"] {{
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 15px !important;
        min-height: 110px !important;
        font-size: 17px !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.1) !important;
    }}
    
    div.stButton > button[key*="card_"]:hover {{
        background-color: #D4AF37 !important;
        color: #000000 !important;
    }}

    .smart-box {{ 
        border: 1px solid #D4AF37; 
        padding: 20px; 
        border-radius: 20px; 
        background: #0a0a0a;
        margin-bottom: 15px; 
    }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:80px;'><h1 style='color:#D4AF37; font-size:50px;'>MA3LOMATI</h1><p style='color:white;'>Elite Broker System</p></div>", unsafe_allow_html=True)
    _, login_col, _ = st.columns([1, 2, 1])
    with login_col:
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة المرور", type="password")
        if st.button("فتح النظام 🔓"):
            if p == "2026": # دخول سريع
                st.session_state.auth = True; st.session_state.current_user = u
                st.query_params["u"] = u; st.rerun()
    st.stop()

# 6. زر الخروج العلوي (الثابت)
if st.button("🚪 خروج", key="logout_top"):
    st.session_state.auth = False; st.query_params.clear(); st.rerun()

# 7. الهيدر المطور
st.markdown(f"""
    <div class="elite-header">
        <h1>MA3LOMATI PRO</h1>
        <p style="color: #D4AF37 !important; margin-top: 5px;">مرحباً، {st.session_state.current_user}</p>
        <div style="font-size: 14px; color: #FFFFFF;">
            📅 {egypt_now.strftime('%Y-%m-%d')} | <span id="clock">{egypt_now.strftime('%I:%M %p')}</span>
        </div>
    </div>
    <script>
        function updateClock() {{
            const now = new Date();
            const opt = {{ timeZone: 'Africa/Cairo', hour: '2-digit', minute: '2-digit', hour12: true }};
            document.getElementById('clock').innerHTML = now.toLocaleTimeString('en-US', opt);
        }}
        setInterval(updateClock, 60000);
    </script>
""", unsafe_allow_html=True)

# 8. المنيو الرئيسي المطور (Responsive Menu)
menu = option_menu(None, ["المشاريع", "المساعد", "المطورين", "الأدوات"], 
    icons=["building", "robot", "people", "calculator"], 
    orientation="horizontal",
    styles={
        "container": {"background-color": "#000", "border": "1px solid #D4AF37", "padding": "0px"},
        "nav-link": {"font-size": "13px", "text-align": "center", "color": "#FFF", "padding": "10px"},
        "nav-link-selected": {"background-color": "#D4AF37", "color": "#000", "font-weight": "bold"}
    })

# 9. محتوى الصفحات
if menu == "المشاريع":
    st.markdown("<h3 style='text-align:center;'>🗂️ قاعدة بيانات المشاريع</h3>", unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    with f1: st.text_input("🔍 اسم المشروع")
    with f2: st.selectbox("📍 المنطقة", ["القاهرة الجديدة", "العاصمة الإدارية", "الشيخ زايد"])
    
    # عرض الكروت
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢 زد التجمع - ZED East\n📍 القاهرة الجديدة", key="card_p_1"):
            st.toast("جاري تحميل تفاصيل زد...")
    with c2:
        if st.button("🏢 أورا الشيخ زايد\n📍 6 أكتوبر", key="card_p_2"):
            st.toast("جاري تحميل تفاصيل أورا...")

elif menu == "الأدوات":
    st.markdown("<div class='smart-box'><h3>💳 الحاسبة العقارية</h3>", unsafe_allow_html=True)
    v = st.number_input("إجمالي السعر", 1000000)
    st.info(f"القسط الشهري على 8 سنوات: {v/96:,.0f} ج.م")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#333; font-size:12px; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
