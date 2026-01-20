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

# 3. روابط البيانات
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# 4. التنسيق الجمالي المخصص للهواتف (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    [data-testid="stAppViewContainer"] {{ background-color: #000000; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; padding-left: 0.5rem !important; padding-right: 0.5rem !important; }}

    /* الكتابة والفريمات */
    p, span, div, label {{ color: #FFFFFF !important; font-weight: 700 !important; }}
    h1, h2, h3 {{ color: #D4AF37 !important; font-weight: 900 !important; }}

    /* تعديل حجم المنيو ليناسب الموبايل */
    .nav-link {{
        padding: 5px !important;
        font-size: 12px !important; /* تصغير الخط قليلاً */
        margin: 0px !important;
    }}
    .nav-link svg {{
        width: 16px !important; /* تصغير الأيقونات */
        height: 16px !important;
    }}
    
    /* الأزرار الذهبية */
    div.stButton > button {{
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 10px !important;
        width: 100% !important;
    }}
    
    div.stButton > button[key*="card_"] {{
        min-height: 100px !important;
        font-size: 16px !important;
    }}

    .smart-box {{ border: 2px solid #D4AF37; padding: 15px; border-radius: 15px; margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:30px;'><h1>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    u = st.text_input("الأسم")
    p = st.text_input("كلمة السر", type="password")
    if st.button("دخول ✅"):
        if p == "2026" or u == "Admin": # تبسيط للدخول
            st.session_state.auth = True; st.session_state.current_user = u
            st.query_params["u"] = u; st.rerun()
    st.stop()

# 6. الهيدر والساعة الحية (بدون ثواني)
st.markdown(f"<div class='smart-box' style='text-align:center;'><h3>MA3LOMATI PRO</h3><p>مرحباً، {st.session_state.current_user}</p></div>", unsafe_allow_html=True)

c1, c2 = st.columns([0.6, 0.4])
with c2:
    st.markdown(f"""
        <div style='text-align: left; color: #D4AF37; font-size: 13px; font-weight:900;'>
            🕒 <span id="clock">{egypt_now.strftime('%I:%M %p')}</span>
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
    if st.button("🚪 خروج"): st.session_state.auth = False; st.query_params.clear(); st.rerun()

# 7. المنيو الرئيسي المطور للموبايل
# تصغير الـ Index والمساحات
menu = option_menu(None, ["المشاريع", "المساعد", "المطورين", "الأدوات"], 
    icons=["building", "robot", "people", "calculator"], 
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#000", "border": "1px solid #D4AF37"},
        "icon": {"font-size": "14px"}, 
        "nav-link": {"font-size": "12px", "text-align": "center", "margin": "0px", "padding": "5px"},
        "nav-link-selected": {"background-color": "#D4AF37", "color": "#000"}
    })

# 8. محتوى الصفحات (مثال)
if menu == "المشاريع":
    st.markdown("🔍 **ابحث عن مشروعك**")
    st.text_input("اسم المشروع", label_visibility="collapsed")
    # عرض الكروت بشكل طولي للموبايل
    for i in range(3):
        if st.button(f"🏢 مشروع رقم {i+1} | التجمع", key=f"card_p_{i}"):
            st.info("تم اختيار المشروع")

elif menu == "الأدوات":
    st.markdown("<div class='smart-box'><h4>💳 حاسبة القسط</h4>", unsafe_allow_html=True)
    v = st.number_input("السعر", 1000000)
    st.write(f"القسط الشهري: {v/96:,.0f} ج.م")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#333; font-size:10px;'>MA3LOMATI PRO 2026</p>", unsafe_allow_html=True)
