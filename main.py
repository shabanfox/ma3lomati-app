import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الرابط الصحيح الخاص بك ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# --- 3. إدارة حالة الجلسة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- 4. وظائف الربط (Backend) ---
def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        return response.text == "Success"
    except: return False

def login_user(user_input, pwd_input):
    try:
        # جلب البيانات من الشيت
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}")
        if response.status_code == 200:
            users_list = response.json()
            for user_data in users_list:
                # التأكد من مطابقة أسماء الأعمدة في الشيت (Name, Password, Email)
                # ملاحظة: البرمجة حساسة لحالة الأحرف (Name تبدأ بحرف كبير)
                name_s = str(user_data.get('Name', user_data.get('name', ''))).strip()
                pass_s = str(user_data.get('Password', user_data.get('password', ''))).strip()
                email_s = str(user_data.get('Email', user_data.get('email', ''))).strip()
                
                if (user_input.strip() == name_s or user_input.strip() == email_s) and str(pwd_input).strip() == pass_s:
                    return name_s
        return None
    except Exception as e:
        st.error(f"خطأ في قراءة البيانات: {e}")
        return None

# --- 5. التنسيق الجمالي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    
    div.stButton > button { border-radius: 12px !important; background-color: #f59e0b !important; color: black !important; font-weight: bold !important; width: 100%; height: 50px; }
    .stTextInput label { color: #f59e0b !important; font-weight: bold !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [aria-selected="true"] { background-color: #f59e0b !important; color: black !important; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 6. نظام الدخول والاشتراك ---
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:50px;'><h1 style='color:#f59e0b; font-size:60px;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 تسجيل دخول", "📝 اشتراك جديد"])
    
    with tab1:
        _, col, _ = st.columns([1,1.5,1])
        with col:
            u_log = st.text_input("الأسم أو الجيميل", key="log_u")
            p_log = st.text_input("كلمة السر", type="password", key="log_p")
            if st.button("دخول للمنصة 🚀"):
                with st.spinner("جاري التحقق..."):
                    user_name = login_user(u_log, p_log)
                    if user_name:
                        st.session_state.auth = True
                        st.session_state.current_user = user_name
                        st.success(f"مرحباً بك يا {user_name}")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("بيانات الدخول غير صحيحة أو الحساب غير مفعل")

    with tab2:
        _, col, _ = st.columns([1,1.5,1])
        with col:
            r_name = st.text_input("الأسم بالكامل")
            r_pass = st.text_input("كلمة السر")
            r_mail = st.text_input("الجيميل")
            r_wa = st.text_input("رقم الواتساب")
            r_co = st.text_input("الشركة")
            if st.button("تأكيد التسجيل ✅"):
                if r_name and r_pass and r_mail:
                    if signup_user(r_name, r_pass, r_mail, r_wa, r_co):
                        st.success("تم تسجيل بياناتك بنجاح! اذهب الآن لتبويب تسجيل الدخول.")
                    else: st.error("حدث خطأ، تأكد من اتصال الإنترنت")
                else: st.warning("يرجى ملء البيانات الأساسية")
    st.stop()

# --- 7. واجهة المنصة بعد الدخول ---
st.markdown(f"""
    <div style="background: #111; padding: 20px; border-radius: 0 0 20px 20px; border-bottom: 3px solid #f59e0b; text-align: center;">
        <h2 style="color: white; margin: 0;">MA3LOMATI PRO</h2>
        <p style="color: #f59e0b;">مرحباً {st.session_state.current_user} | {egypt_now.strftime('%I:%M %p')}</p>
    </div>
""", unsafe_allow_html=True)

menu = option_menu(None, ["المشاريع", "المساعد الذكي", "أدوات البروكر"], 
    icons=["building", "robot", "briefcase"], default_index=0, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if menu == "أدوات البروكر":
    if st.button("🚪 تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
else:
    st.info("هذا القسم قيد التحديث لعام 2026")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
