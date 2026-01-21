import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (Session State)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0

# تفعيل التحديث التلقائي (فقط إذا كان المستخدم مسجل دخول) لضمان استقرار صفحة الدخول
if st.session_state.auth:
    st_autorefresh(interval=1000, key="clock_refresh")

# 3. الرابط الخاص بك لربط الجوجل شيت
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# --- وظائف الربط ---
def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        return response.text == "Success"
    except: return False

def login_user(user_input, pwd_input):
    try:
        # إضافة بارامتر عشوائي لمنع الكاش
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}")
        if response.status_code == 200:
            users_list = response.json()
            for user_data in users_list:
                name_s = str(user_data.get('Name', user_data.get('name', ''))).strip()
                pass_s = str(user_data.get('Password', user_data.get('password', ''))).strip()
                email_s = str(user_data.get('Email', user_data.get('email', ''))).strip()
                if (user_input.strip().lower() == name_s.lower() or user_input.strip().lower() == email_s.lower()) and str(pwd_input).strip() == pass_s:
                    return name_s
        return None
    except: return None

# 4. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { background-color: #111; border-radius: 10px; padding: 10px 20px; color: white; }
    .smart-box { background: #111; border-right: 5px solid #f59e0b; padding: 20px; border-radius: 15px; color: white; margin-bottom: 20px; }
    div.stButton > button { width: 100%; border-radius: 10px; font-family: 'Cairo'; }
    </style>
""", unsafe_allow_html=True)

# 5. منطق تسجيل الدخول (English Interface)
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    tab_login, tab_signup = st.tabs(["🔐 SIGN IN", "📝 SIGN UP"])

    with tab_login:
        _, col, _ = st.columns([1, 2, 1])
        with col:
            u = st.text_input("Username / Email", key="login_u")
            p = st.text_input("Password", type="password", key="login_p")
            if st.button("LOGIN NOW"):
                if p == "2026": # كود الطوارئ
                    st.session_state.auth = True
                    st.session_state.current_user = "Admin"
                    st.rerun()
                else:
                    with st.spinner("Verifying..."):
                        user_name = login_user(u, p)
                        if user_name:
                            st.session_state.auth = True
                            st.session_state.current_user = user_name
                            st.rerun()
                        else:
                            st.error("Invalid Credentials")

    with tab_signup:
        _, col, _ = st.columns([1, 2, 1])
        with col:
            name = st.text_input("Full Name")
            mail = st.text_input("Email")
            pwd = st.text_input("Create Password", type="password")
            if st.button("REGISTER"):
                if name and mail and pwd:
                    if signup_user(name, pwd, mail, "", ""):
                        st.success("Success! Please Sign In.")
                    else: st.error("Error connecting to server.")
    st.stop()

# --- بعد تسجيل الدخول ---

# حساب الوقت المصري
egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# الهيدر
st.markdown(f"""
    <div style="background: #111; padding: 20px; border-radius: 0 0 20px 20px; border-bottom: 3px solid #f59e0b; text-align:center;">
        <h2 style="margin:0; color:white;">MA3LOMATI PRO</h2>
        <p style="color:#f59e0b;">Welcome, {st.session_state.current_user} | 🕒 {egypt_now.strftime('%I:%M:%S %p')}</p>
    </div>
""", unsafe_allow_html=True)

# المنيو
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "أدوات البروكر"], 
    icons=["robot", "search", "briefcase"], orientation="horizontal")

# تحميل البيانات (مثال مبسط)
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try: return pd.read_csv(u_p).fillna("---")
    except: return pd.DataFrame()

df = load_data()

if menu == "المشاريع":
    search = st.text_input("🔍 ابحث عن مشروع...")
    if not df.empty:
        # عرض المشاريع
        filtered = df[df.iloc[:,0].str.contains(search, case=False)] if search else df
        st.dataframe(filtered.head(20))

elif menu == "أدوات البروكر":
    st.subheader("🛠️ أدوات الحساب")
    price = st.number_input("سعر الوحدة", value=1000000)
    years = st.slider("عدد السنوات", 1, 10, 7)
    st.metric("القسط الشهري التقديري", f"{price/(years*12):,.0f} EGP")

if st.sidebar.button("Logout"):
    st.session_state.auth = False
    st.rerun()
