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

# 2. التنسيق الجمالي (تصحيح الألوان والخطوط البيضاء)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container { padding-top: 1rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    
    /* الخلفية والخطوط العامة */
    [data-testid="stAppViewContainer"] { 
        background-color: #0a192f; 
        direction: rtl !important; 
        text-align: right !important; 
        font-family: 'Cairo', sans-serif; 
    }
    
    /* جعل كل النصوص بيضاء وواضحة */
    p, span, div, label, .stWrite { 
        color: #ffffff !important; 
        font-weight: 500 !important; 
    }
    
    /* العناوين بالذهبي */
    h1, h2, h3 { 
        color: #f59e0b !important; 
        font-weight: 900 !important; 
    }

    /* كروت المشاريع (أزرار بخلفية داكنة وكتابة بيضاء) */
    div.stButton > button {
        background: linear-gradient(145deg, #112240, #0a192f) !important;
        color: #ffffff !important;
        border: 1px solid #233554 !important;
        border-right: 6px solid #f59e0b !important;
        border-radius: 12px !important;
        min-height: 100px !important;
        width: 100% !important;
        font-size: 16px !important;
        font-weight: bold !important;
    }
    
    div.stButton > button:hover {
        border-color: #f59e0b !important;
        color: #f59e0b !important;
    }

    /* الصناديق */
    .smart-box { 
        background: #112240; 
        border: 1px solid #233554; 
        padding: 25px; 
        border-radius: 20px; 
        border-right: 6px solid #f59e0b; 
    }

    /* المدخلات (Input) ليكون النص بداخلها واضح */
    input { color: white !important; }
</style>
""", unsafe_allow_html=True)

# 3. إدارة الحالة والروابط
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None

# --- وظيفة الدخول ---
def login_user(u_in, p_in):
    try:
        res = requests.get(f"{SCRIPT_URL}?nocache={time.time()}")
        if res.status_code == 200:
            for u in res.json():
                n, p = str(u.get('Name','')), str(u.get('Password',''))
                if u_in.strip().lower() == n.lower() and str(p_in) == p:
                    return n
        return None
    except: return None

# 4. واجهة الدخول
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    u_log = st.text_input("الأسم أو الجيميل")
    p_log = st.text_input("كلمة السر", type="password")
    if st.button("دخول للنظام 🚀"):
        if p_log == "2026":
            st.session_state.auth, st.session_state.current_user = True, "Admin"
            st.rerun()
        else:
            found = login_user(u_log, p_log)
            if found:
                st.session_state.auth, st.session_state.current_user = True, found
                st.rerun()
            else:
                st.error("بيانات غير صحيحة")
    st.stop()

# 5. القائمة الرئيسية
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "calculator"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# 6. مثال لصفحة المشاريع
if menu == "المشاريع":
    st.markdown("<h2 style='text-align:right;'>🏢 المشاريع المتاحة</h2>", unsafe_allow_html=True)
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.write("هنا تظهر المشاريع باللون الأبيض الواضح:")
    c1, c2 = st.columns(2)
    c1.button("🏢 مشروع العاصمة الإدارية\n📍 العاصمة الإدارية", key="p1")
    c2.button("🏢 مشروع التجمع الخامس\n📍 القاهرة الجديدة", key="p2")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "أدوات البروكر":
    st.title("🛠️ حقيبة البروكر")
    val = st.number_input("سعر الوحدة", value=1000000)
    st.write(f"القسط الشهري التقريبي: {val/96:,.0f}")

st.markdown(f"<p style='text-align:center;'>المستخدم الحالي: {st.session_state.current_user}</p>", unsafe_allow_html=True)
