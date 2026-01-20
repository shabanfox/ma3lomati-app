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

# 3. التنسيق الجمالي (Elite Gold & Black)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: #000000 !important;
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }}
    .block-container {{ padding: 0.5rem !important; }}

    /* الهيدر بالخلفية التي صممناها */
    .mobile-header {{
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.7)), url('https://img.freepik.com/premium-photo/modern-luxury-real-estate-background-with-golden-logos_1012-1234.jpg'); /* رابط افتراضي فخم مشابه للتصميم */
        background-size: cover;
        background-position: center;
        border-bottom: 3px solid #D4AF37;
        padding: 40px 10px;
        text-align: center;
        border-radius: 0 0 30px 30px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
    }}
    .mobile-header h1 {{ color: #D4AF37 !important; font-size: 32px !important; margin: 0; text-shadow: 2px 2px 5px #000; }}
    
    /* زر الخروج الصغير أعلى اليسار */
    .stButton > button[key="exit_btn"] {{
        position: fixed;
        top: 15px;
        left: 10px;
        background-color: #8b0000 !important;
        color: white !important;
        border: none !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        z-index: 9999;
        font-size: 18px !important;
    }}

    p, span, div, label {{ color: #FFFFFF !important; font-weight: 700 !important; }}
    
    /* الكروت: أسود + فريم ذهبي */
    div.stButton > button {{
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 12px !important;
        width: 100% !important;
        font-weight: 900 !important;
        margin-bottom: 10px !important;
        transition: 0.3s;
    }}
    div.stButton > button:hover {{ background-color: #D4AF37 !important; color: #000 !important; }}
    
    /* المنيو المضغوط للهواتف */
    .nav-link {{ padding: 8px !important; font-size: 13px !important; }}
    
    .smart-box {{ border: 2px solid #D4AF37; padding: 20px; border-radius: 20px; background: #0a0a0a; }}
    </style>
""", unsafe_allow_html=True)

# 4. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:80px;'><h1 style='color:#D4AF37;'>MA3LOMATI PRO</h1><p>Luxury Real Estate System</p></div>", unsafe_allow_html=True)
    u = st.text_input("اسم المستخدم")
    p = st.text_input("كلمة السر", type="password")
    if st.button("فتح النظام 🔓"):
        if p == "2026": 
            st.session_state.auth = True; st.session_state.current_user = u
            st.query_params["u"] = u; st.rerun()
    st.stop()

# 5. زر الخروج الثابت
if st.button("🚪", key="exit_btn"):
    st.session_state.auth = False; st.query_params.clear(); st.rerun()

# 6. الهيدر المطور بالصورة والساعة
st.markdown(f"""
    <div class='mobile-header'>
        <h1>MA3LOMATI PRO</h1>
        <div style='margin-top:10px;'>
            <span style='color:#FFF; font-size:14px;'>📅 {egypt_now.strftime('%Y-%m-%d')}</span><br>
            <span style='color:#D4AF37; font-size:18px; font-weight:900;'>🕒 <span id="clock">{egypt_now.strftime('%I:%M %p')}</span></span>
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

# 7. المنيو الرئيسي المخصص للموبايل
menu = option_menu(None, ["المشاريع", "المساعد", "المطورين", "الأدوات"], 
    icons=["building", "robot", "people", "calculator"], 
    orientation="horizontal",
    styles={
        "container": {"background-color": "#000", "border": "1px solid #D4AF37", "padding": "0px"},
        "nav-link": {"font-size": "12px", "color": "#FFF", "padding": "10px"},
        "nav-link-selected": {"background-color": "#D4AF37", "color": "#000", "font-weight": "bold"}
    })

# 8. محتوى الصفحات
if menu == "المشاريع":
    st.markdown("### 🏢 قاعدة بيانات المشاريع")
    st.text_input("🔍 ابحث عن مشروع أو منطقة...", label_visibility="collapsed")
    # مثال للكروت
    for i in range(3):
        if st.button(f"🏢 مشروع فخم {i+1} | التجمع \n 🏗️ شركة إعمار / سكاى", key=f"card_p_{i}"):
            st.session_state.selected_item = f"مشروع {i+1}"

elif menu == "المطورين":
    st.markdown("### 🏗️ المطورين العقاريين")
    for i in ["أورا", "طلعت مصطفى", "سوديك", "بالم هيلز"]:
        st.button(f"🏢 {i}", key=f"card_d_{i}")

elif menu == "الأدوات":
    st.markdown("<div class='smart-box'><h4>💳 حاسبة التمويل</h4>", unsafe_allow_html=True)
    val = st.number_input("سعر الوحدة", value=5000000)
    st.success(f"القسط الشهري التقديري: {val/96:,.0f} ج.م")
    st.markdown("</div>", unsafe_allow_html=True)

# عرض تفاصيل مختارة
if st.session_state.selected_item:
    st.markdown("---")
    st.markdown(f"<div class='smart-box'>📂 تفاصيل: {st.session_state.selected_item}</div>", unsafe_allow_html=True)
    if st.button("إغلاق التفاصيل ❌"): st.session_state.selected_item = None; st.rerun()

st.markdown("<p style='text-align:center; color:#333; font-size:12px; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
