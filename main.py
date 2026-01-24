import streamlit as st
import pandas as pd
import requests
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة الفخمة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- روابط البيانات (Google Sheets / Apps Script) ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 2. إدارة الحالة (Session State) ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'page_num' not in st.session_state: st.session_state.page_num = 0

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- 3. وظائف التحقق والربط ---
def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        return response.text == "Success"
    except: return False

def login_user(u, p):
    try:
        df = pd.read_csv(f"{USER_SHEET_URL}?nocache={time.time()}")
        df.columns = [c.strip() for c in df.columns]
        user_row = df[(df['Name'].astype(str) == str(u)) & (df['Password'].astype(str) == str(p))]
        if not user_row.empty:
            return user_row.iloc[0]['Name']
        return None
    except: return None

# --- 4. التنسيق الجمالي (CSS Luxury 2026) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}

    /* تصميم صفحة تسجيل الدخول */
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 50px; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 28px; font-weight: 900;
        text-align: center; z-index: 10; margin-bottom: -35px; min-width: 380px;
        box-shadow: 0 10px 30px rgba(245,158,11,0.3);
    }}
    .auth-card {{ 
        background-color: #ffffff; width: 400px; padding: 60px 35px 35px 35px; 
        border-radius: 40px; text-align: center; box-shadow: 0 25px 60px rgba(0,0,0,0.5); 
    }}
    .lock-gold {{ font-size: 50px; color: #f59e0b; margin-bottom: 10px; }}
    
    /* ستايل المدخلات داخل الكارت */
    .auth-card div.stTextInput input {{
        background-color: #f8f9fa !important; color: #000 !important;
        border: 1px solid #ddd !important; border-radius: 15px !important;
        text-align: center !important; height: 50px !important; font-weight: bold;
    }}

    /* ستايل الهيدر الداخلي */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 3px solid #f59e0b;
        padding: 40px 20px; text-align: center; border-radius: 0 0 50px 50px; margin-bottom: 30px;
    }}
    .detail-card {{ background: rgba(25, 25, 25, 0.95); padding: 25px; border-radius: 20px; border-top: 5px solid #f59e0b; border: 1px solid #333; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 15px; margin-bottom: 2px; }}
    .val-white {{ color: white; font-size: 17px; border-bottom: 1px solid #333; padding-bottom: 5px; margin-bottom: 15px; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. منطق عرض صفحة الدخول ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>MA3LOMATI PRO</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.markdown("<div class='lock-gold'>🔐</div>", unsafe_allow_html=True)
    
    tab_log, tab_reg = st.tabs(["تسجيل الدخول", "فتح حساب جديد"])
    
    with tab_log:
        u = st.text_input("اسم المستخدم / البريد", placeholder="Username", label_visibility="collapsed", key="l_user")
        p = st.text_input("كلمة المرور", type="password", placeholder="Password", label_visibility="collapsed", key="l_pass")
        if st.button("دخول للمنصة 🔥", use_container_width=True):
            if p == "2026": # كود دخول سريع للمطور
                st.session_state.auth = True
                st.session_state.current_user = "Admin"
                st.rerun()
            else:
                user_name = login_user(u, p)
                if user_name:
                    st.session_state.auth = True
                    st.session_state.current_user = user_name
                    st.rerun()
                else:
                    st.error("بيانات غير صحيحة")
                    
    with tab_reg:
        r_name = st.text_input("الاسم بالكامل", key="r1")
        r_mail = st.text_input("البريد الإلكتروني", key="r2")
        r_pass = st.text_input("كلمة السر", type="password", key="r3")
        if st.button("إنشاء حساب جديد ✅", use_container_width=True):
            if signup_user(r_name, r_pass, r_mail, "000", "Company"):
                st.success("تم التسجيل! يمكنك الدخول الآن")
            else:
                st.error("خطأ في الاتصال")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 6. المنصة من الداخل (بعد تسجيل الدخول) ---
st.markdown(f"""
    <div class="royal-header">
        <h1 style="color:#f59e0b; font-weight:900; margin:0;">MA3LOMATI PRO</h1>
        <p style="color:white;">مرحباً بك، {st.session_state.current_user} | {egypt_now.strftime('%Y-%m-%d')}</p>
    </div>
""", unsafe_allow_html=True)

# المنيو الرئيسي
menu = option_menu(None, ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي"], 
                   icons=["tools", "building", "list-task", "robot"], 
                   default_index=2, orientation="horizontal",
                   styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if st.sidebar.button("🚪 تسجيل خروج"):
    st.session_state.auth = False
    st.rerun()

# --- هنا تضع بقية كود عرض المشاريع والأدوات الخاص بك ---
if menu == "المشاريع":
    st.subheader("🏢 قاعدة بيانات المشاريع العقارية")
    # تكملة الكود...
    st.info("تم تفعيل نظام الدخول بنجاح. يمكنك الآن عرض بيانات المشاريع هنا.")

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026 | النسخة الاحترافية</p>", unsafe_allow_html=True)
