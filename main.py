import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. الرابط الخاص بك (اللي أنت بعته)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzT_YOHvummf-xi8iWzmdVeJSK-TKcvkHLtt5F91MoahqH-d-F2BOvvLF4D8Pjmzww-Ag/exec"

# 3. إدارة حالة الجلسة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None

# 4. وظائف الربط مع جوجل شيت (تسجيل ودخول)
def signup_user(name, pwd, email, wa, comp):
    data = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=data)
        return response.text == "Success"
    except: return False

def login_user(user_input, pwd_input):
    try:
        # قراءة البيانات من الشيت
        response = requests.get(SCRIPT_URL)
        users = response.json() # مصفوفة البيانات
        for row in users[1:]: # نتخطى أول صف (العناوين)
            # row[0]=Name, row[1]=Password, row[2]=Email
            if (user_input == row[0] or user_input == row[2]) and str(pwd_input) == str(row[1]):
                return row[0] # نرجع اسم المستخدم
        return None
    except: return None

# 5. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    .stTextInput label { color: #f59e0b !important; font-weight: bold !important; }
    div.stButton > button { border-radius: 12px !important; background-color: #f59e0b !important; color: black !important; font-weight: bold !important; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# 6. شاشة الدخول والتسجيل
if not st.session_state.auth:
    st.markdown("<h1 style='color:#f59e0b; text-align:center; padding-top:50px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    
    choice = st.radio("القائمة", ["تسجيل دخول", "إنشاء حساب جديد"], horizontal=True)
    
    _, col, _ = st.columns([1,2,1])
    with col:
        if choice == "تسجيل دخول":
            u = st.text_input("الأسم أو الجيميل")
            p = st.text_input("كلمة السر", type="password")
            if st.button("دخول 🚀"):
                user_name = login_user(u, p)
                if user_name:
                    st.session_state.auth = True
                    st.session_state.current_user = user_name
                    st.success(f"أهلاً بك يا {user_name}")
                    st.rerun()
                else:
                    st.error("بيانات الدخول خطأ أو الحساب غير موجود")
        
        else:
            st.markdown("### 📝 اشتراك بروكر جديد")
            r_name = st.text_input("الأسم بالكامل")
            r_pass = st.text_input("كلمة السر")
            r_mail = st.text_input("الجيميل")
            r_wa = st.text_input("رقم الواتساب")
            r_co = st.text_input("الشركة")
            
            if st.button("تأكيد التسجيل ✅"):
                if r_name and r_pass and r_mail:
                    if signup_user(r_name, r_pass, r_mail, r_wa, r_co):
                        st.success("تم تسجيلك في الشيت بنجاح! روح دلوقتي لـ 'تسجيل دخول'")
                    else: st.error("حدث خطأ في الاتصال")
                else: st.warning("املأ الخانات الأساسية")
    st.stop()

# --- من هنا يبدأ كود موقعك الأصلي (المشاريع والمساعد الذكي) ---
st.success(f"تم تسجيل الدخول باسم: {st.session_state.current_user}")
if st.button("تسجيل خروج"):
    st.session_state.auth = False
    st.rerun()

# أضف هنا باقي كود المنيو والمشاريع اللي عملناه قبل كدة...
