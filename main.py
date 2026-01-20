import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الجلسة (الريفريش) - يقرأ اليوزر من الرابط لو موجود
if "u" in st.query_params:
    st.session_state.auth = True
    st.session_state.current_user = st.query_params["u"]

if 'auth' not in st.session_state: st.session_state.auth = False
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_now = datetime.now(pytz.timezone('Africa/Cairo'))

# 3. التنسيق الجمالي (تصميم الهواتف النحيف - Slim Mobile Design)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* سواد كامل */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: #000000 !important;
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }}
    .block-container {{ padding: 0.2rem !important; }}

    /* الهيدر المصغر جداً Slim Header */
    .slim-header {{
        background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.8)), url('https://img.freepik.com/premium-photo/luxury-gold-abstract-architecture-background_1012-1234.jpg');
        background-size: cover;
        background-position: center;
        border-bottom: 2px solid #D4AF37;
        padding: 15px 10px; /* تصغير المساحة الداخلية */
        text-align: center;
        border-radius: 0 0 20px 20px;
        margin-bottom: 10px;
    }}
    .slim-header h1 {{ color: #D4AF37 !important; font-size: 22px !important; margin: 0; }}
    
    /* زر الخروج الدائري الصغير */
    .stButton > button[key="exit_btn"] {{
        position: fixed;
        top: 10px;
        left: 10px;
        background-color: #600 !important;
        color: white !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 50% !important;
        width: 35px !important;
        height: 35px !important;
        z-index: 9999;
        font-size: 14px !important;
        padding: 0 !important;
    }}

    p, span, div, label {{ color: #FFFFFF !important; font-weight: 700 !important; }}
    
    /* الأزرار: فريم ذهبي وخلفية سوداء */
    div.stButton > button {{
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 1.5px solid #D4AF37 !important;
        border-radius: 10px !important;
        width: 100% !important;
        font-weight: 700 !important;
        margin-bottom: 5px !important;
        font-size: 14px !important;
    }}
    
    /* المنيو المضغوط جداً للموبايل */
    .nav-link {{ padding: 5px !important; font-size: 11px !important; }}
    
    .smart-box {{ border: 1.5px solid #D4AF37; padding: 12px; border-radius: 15px; background: #000; margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# 4. شاشة الدخول (تظهر فقط لو مش مسجل)
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:50px;'><h1 style='color:#D4AF37;'>MA3LOMATI</h1></div>", unsafe_allow_html=True)
    u = st.text_input("اسم المستخدم")
    p = st.text_input("كلمة السر", type="password")
    if st.button("فتح النظام"):
        if p == "2026": 
            st.session_state.auth = True; st.session_state.current_user = u
            st.query_params["u"] = u; st.rerun()
    st.stop()

# 5. زر الخروج الثابت (أعلى اليسار)
if st.button("🚪", key="exit_btn"):
    st.session_state.auth = False; st.query_params.clear(); st.rerun()

# 6. الهيدر المصغر (Slim Header) مع الساعة
st.markdown(f"""
    <div class='slim-header'>
        <h1>MA3LOMATI PRO</h1>
        <div style='margin-top:5px;'>
            <span style='color:#D4AF37; font-size:14px; font-weight:900;'>🕒 <span id="clock">{egypt_now.strftime('%I:%M %p')}</span></span>
        </div>
    </div>
    <script>
        setInterval(() => {{
            let d = new Date();
            let opt = {{timeZone: 'Africa/Cairo', hour: '2-digit', minute: '2-digit', hour12: true}};
            document.getElementById("clock").innerHTML = d.toLocaleTimeString("en-US", opt);
        }}, 60000);
    </script>
""", unsafe_allow_html=True)

# 7. المنيو الرئيسي (الأكثر توافقاً مع عرض الموبايل)
menu = option_menu(None, ["المشاريع", "المساعد", "المطورين", "الأدوات"], 
    icons=["building", "robot", "people", "calculator"], 
    orientation="horizontal",
    styles={
        "container": {"background-color": "#000", "border": "1px solid #D4AF37", "padding": "0px"},
        "nav-link": {"font-size": "11px", "color": "#FFF", "padding": "7px"},
        "nav-link-selected": {"background-color": "#D4AF37", "color": "#000", "font-weight": "bold"}
    })

# 8. محتوى الصفحات
if menu == "المشاريع":
    st.text_input("🔍 بحث...", label_visibility="collapsed")
    # عرض الكروت بشكل مضغوط
    for i in range(3):
        if st.button(f"🏢 مشروع {i+1} | التجمع", key=f"card_p_{i}"):
            st.session_state.selected_item = f"مشروع {i+1}"

elif menu == "الأدوات":
    st.markdown("<div class='smart-box'><h4>💳 الحاسبة</h4>", unsafe_allow_html=True)
    val = st.number_input("السعر", value=1000000)
    st.write(f"القسط: {val/96:,.0f} ج.م")
    st.markdown("</div>", unsafe_allow_html=True)

# عرض التفاصيل المختارة
if st.session_state.selected_item:
    st.markdown(f"<div class='smart-box'>📂 {st.session_state.selected_item}</div>", unsafe_allow_html=True)
    if st.button("إغلاق ❌"): st.session_state.selected_item = None; st.rerun()

st.markdown("<p style='text-align:center; color:#333; font-size:10px; margin-top:20px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
