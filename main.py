import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الجلسة (الريفريش)
if "u" in st.query_params:
    st.session_state.auth = True
    st.session_state.current_user = st.query_params["u"]

if 'auth' not in st.session_state: st.session_state.auth = False
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_now = datetime.now(pytz.timezone('Africa/Cairo'))

# 3. التنسيق الجمالي (تصميم الهيدر بالصورة والأسود والذهبي)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* خلفية سوداء وحذف الأيقونات العلوية */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: #000000 !important;
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }}
    header, [data-testid="stHeader"], [data-testid="stToolbar"] {{ visibility: hidden !important; display: none !important; }}
    .block-container {{ padding: 0rem !important; }}

    /* الهيدر بصورة الشركات العقارية */
    .mobile-header {{
        background-image: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.6)), url('https://i.ibb.co/LzNfDq9/real-estate-logos-header.jpg');
        background-size: cover;
        background-position: center;
        border-bottom: 3px solid #D4AF37;
        padding: 25px 10px;
        text-align: center;
        border-radius: 0 0 25px 25px;
        margin-bottom: 15px;
        box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3);
    }}
    .mobile-header h1 {{ color: #D4AF37 !important; font-size: 26px !important; margin: 0; text-shadow: 3px 3px 6px #000; font-weight: 900; }}
    
    /* زر الخروج فوق على الشمال تماماً */
    .stButton > button[key="exit_top_left"] {{
        position: fixed;
        top: 10px;
        left: 10px;
        background-color: #800 !important;
        color: white !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 8px !important;
        padding: 0px 10px !important;
        font-size: 13px !important;
        z-index: 999999;
    }}

    /* نصوص بيضاء وفريمات ذهبية */
    p, span, div, label {{ color: #FFFFFF !important; font-weight: 700 !important; }}
    
    div.stButton > button {{
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 12px !important;
        width: 100% !important;
        font-weight: 900 !important;
        margin-bottom: 8px !important;
    }}
    
    /* المنيو المضغوط للهواتف */
    .nav-link {{ padding: 8px !important; font-size: 12px !important; }}
    
    .smart-box {{ border: 2px solid #D4AF37; padding: 15px; border-radius: 20px; background: #0a0a0a; }}
    </style>
""", unsafe_allow_html=True)

# 4. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#D4AF37;'>MA3LOMATI</h1></div>", unsafe_allow_html=True)
    u = st.text_input("الأسم")
    p = st.text_input("كلمة السر", type="password")
    if st.button("دخول ✅"):
        if p == "2026": 
            st.session_state.auth = True; st.session_state.current_user = u
            st.query_params["u"] = u; st.rerun()
    st.stop()

# 5. زر الخروج الثابت (أقصى أعلى اليسار)
if st.button("🚪 خروج", key="exit_top_left"):
    st.session_state.auth = False; st.query_params.clear(); st.rerun()

# 6. الهيدر بالصورة والساعة
st.markdown(f"""
    <div class='mobile-header'>
        <h1>MA3LOMATI PRO</h1>
        <div style='margin-top:10px;'>
            <span style='color:#D4AF37; font-size:16px; font-weight:900;'>🕒 <span id="clock">{egypt_now.strftime('%I:%M %p')}</span></span>
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

# 7. المنيو الرئيسي
menu = option_menu(None, ["المشاريع", "المساعد", "المطورين", "الأدوات"], 
    icons=["building", "robot", "people", "calculator"], 
    orientation="horizontal",
    styles={
        "container": {"background-color": "#000", "border": "1px solid #D4AF37", "padding": "0px"},
        "nav-link": {"font-size": "11px", "color": "#FFF", "padding": "10px"},
        "nav-link-selected": {"background-color": "#D4AF37", "color": "#000", "font-weight": "bold"}
    })

# 8. محتوى الصفحات
if menu == "المشاريع":
    st.text_input("🔍 ابحث عن مشروع...", label_visibility="collapsed")
    for i in range(3):
        if st.button(f"🏢 مشروع فخم {i+1} | التجمع", key=f"card_p_{i}"):
            st.session_state.selected_item = f"مشروع {i+1}"

elif menu == "الأدوات":
    st.markdown("<div class='smart-box'><h4>💳 حاسبة العقار</h4>", unsafe_allow_html=True)
    val = st.number_input("السعر", value=1000000)
    st.write(f"القسط الشهري: {val/96:,.0f} ج.م")
    st.markdown("</div>", unsafe_allow_html=True)

# عرض تفاصيل مختارة
if st.session_state.selected_item:
    st.markdown(f"<div class='smart-box'>📂 تفاصيل: {st.session_state.selected_item}</div>", unsafe_allow_html=True)
    if st.button("إغلاق ❌"): st.session_state.selected_item = None; st.rerun()

st.markdown("<p style='text-align:center; color:#333; font-size:10px; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)

