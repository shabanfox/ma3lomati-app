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

# 3. التنسيق الجمالي (Ultra Mobile Design)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* الخلفية سوداء تماماً */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: #000000 !important;
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }}
    .block-container {{ padding: 0.5rem !important; }}

    /* الهيدر البسيط والجذاب */
    .mobile-header {{
        background-color: #000000;
        border-bottom: 2px solid #D4AF37;
        padding: 15px 10px;
        text-align: center;
        margin-bottom: 15px;
    }}
    .mobile-header h1 {{ color: #D4AF37 !important; font-size: 28px !important; margin: 0; }}
    
    /* زر الخروج الصغير فوق */
    .logout-btn {{
        position: absolute;
        top: 15px;
        left: 10px;
    }}

    /* خطوط بيضاء واضحة وفريمات ذهبية */
    p, span, div, label {{ color: #FFFFFF !important; font-weight: 700 !important; font-size: 15px !important; }}
    
    /* الكروت: أسود + برواز ذهبي صريح */
    div.stButton > button {{
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 12px !important;
        width: 100% !important;
        font-weight: 900 !important;
        margin-bottom: 8px !important;
    }}
    div.stButton > button[key*="card_"] {{ min-height: 90px !important; font-size: 16px !important; }}
    
    /* المنيو المضغوط */
    .nav-link {{ padding: 5px !important; font-size: 12px !important; }}
    
    .smart-box {{ border: 2px solid #D4AF37; padding: 15px; border-radius: 15px; background: #000; }}
    </style>
""", unsafe_allow_html=True)

# 4. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#D4AF37;'>MA3LOMATI</h1><p>نظام الوسطاء المحترفين</p></div>", unsafe_allow_html=True)
    u = st.text_input("الأسم")
    p = st.text_input("كلمة السر", type="password")
    if st.button("دخول ✅"):
        if p == "2026": 
            st.session_state.auth = True; st.session_state.current_user = u
            st.query_params["u"] = u; st.rerun()
    st.stop()

# 5. الهيدر وزر الخروج
col_header, col_logout = st.columns([0.8, 0.2])
with col_header:
    st.markdown(f"""
        <div class='mobile-header'>
            <h1>MA3LOMATI PRO</h1>
            <span style='color:#aaa; font-size:12px;'>🕒 <span id="clock">{egypt_now.strftime('%I:%M %p')}</span></span>
        </div>
        <script>
            setInterval(() => {{
                let d = new Date();
                document.getElementById("clock").innerHTML = d.toLocaleTimeString("en-US", {{hour12:true, hour:"2-digit", minute:"2-digit", timeZone:"Africa/Cairo"}});
            }}, 60000);
        </script>
    """, unsafe_allow_html=True)
with col_logout:
    if st.button("🚪"): 
        st.session_state.auth = False; st.query_params.clear(); st.rerun()

# 6. المنيو الرئيسي المخصص للهاتف
menu = option_menu(None, ["المشاريع", "المساعد", "المطورين", "الأدوات"], 
    icons=["building", "robot", "people", "calculator"], 
    orientation="horizontal",
    styles={
        "container": {"background-color": "#000", "border": "1px solid #D4AF37", "padding": "0px"},
        "nav-link": {"font-size": "11px", "color": "#FFF", "padding": "8px"},
        "nav-link-selected": {"background-color": "#D4AF37", "color": "#000"}
    })

# 7. الصفحات
if menu == "المشاريع":
    st.markdown("### 🏢 المشاريع المتاحة")
    st.text_input("🔍 بحث سريح...", label_visibility="collapsed")
    # عرض الكروت
    for i in range(5):
        if st.button(f"مشروع {i+1} | القاهرة الجديدة \n 🏗️ مطور العقارية", key=f"card_p_{i}"):
            st.session_state.selected_item = f"مشروع {i+1}"

elif menu == "الأدوات":
    st.markdown("<div class='smart-box'><h4>💳 حاسبة الأقساط</h4>", unsafe_allow_html=True)
    val = st.number_input("السعر", value=1000000)
    st.write(f"القسط: {val/96:,.0f} ج.م")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "المطورين":
    st.markdown("### 🏗️ كبار المطورين")
    for i in range(5):
        st.button(f"شركة مطور رقم {i+1}", key=f"card_d_{i}")

elif menu == "المساعد":
    st.markdown("<div class='smart-box'>🤖 اطلب أي معلومة عن أي مشروع...</div>", unsafe_allow_html=True)

# عرض التفاصيل
if st.session_state.selected_item:
    st.markdown("---")
    st.info(f"تفاصيل: {st.session_state.selected_item}")
    if st.button("إغلاق ❌"): st.session_state.selected_item = None; st.rerun()

st.markdown("<p style='text-align:center; color:#444; font-size:10px; margin-top:30px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
