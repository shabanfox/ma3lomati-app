import streamlit as st
import pandas as pd
import requests
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- الروابط (رابط الـ Apps Script الخاص بك) ---
# ملاحظة: هذا الرابط هو المسؤول عن جلب المستخدمين وتسجيلهم
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 2. إدارة الجلسة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None

# --- 3. وظائف الربط (Backend) ---
def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        return response.text == "Success"
    except: return False

def login_user(user_input, pwd_input):
    try:
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

# --- 4. تصميم الـ CSS (السنترة المطلقة + الشكل المصغر) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding: 0px !important; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), url('{BG_IMG}');
        background-size: cover; background-position: center;
        display: flex !important; align-items: center !important; justify-content: center !important;
        height: 100vh; direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}

    /* الحاوية الممركزة */
    .auth-container {{
        width: 100%; max-width: 320px; text-align: center;
    }}

    .brand-logo {{
        color: #f59e0b; font-size: 35px; font-weight: 900; margin-bottom: 5px;
        text-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
    }}
    
    .brand-tagline {{ color: #ffffff; font-size: 13px; opacity: 0.5; margin-bottom: 20px; }}

    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] {{ background: transparent !important; gap: 10px; justify-content: center !important; }}
    .stTabs [data-baseweb="tab"] {{ font-size: 14px !important; color: #777 !important; padding: 5px 12px !important; }}
    .stTabs [aria-selected="true"] {{ color: #f59e0b !important; border-bottom: 2px solid #f59e0b !important; }}

    /* الحقول */
    div.stTextInput input {{
        background: rgba(255, 255, 255, 0.04) !important; color: #fff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 10px !important;
        height: 40px !important; font-size: 14px !important; text-align: center !important;
    }}

    /* الأزرار */
    .stButton button {{
        background: linear-gradient(90deg, #f59e0b, #d97706) !important;
        color: #000 !important; font-weight: 700 !important;
        border-radius: 10px !important; height: 42px !important; border: none !important; margin-top: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. واجهة تسجيل الدخول والاشتراك ---
if not st.session_state.auth:
    st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
    st.markdown("<p class='brand-logo'>MA3LOMATI PRO</p>", unsafe_allow_html=True)
    st.markdown("<p class='brand-tagline'>الجيل القادم من المعلومات العقارية</p>", unsafe_allow_html=True)
    
    t_login, t_reg = st.tabs(["🔐 دخول", "📝 اشتراك"])
    
    with t_login:
        u_log = st.text_input("User", placeholder="الاسم أو الإيميل", label_visibility="collapsed", key="u_l")
        p_log = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="p_l")
        
        if st.button("دخول للمنصة", use_container_width=True):
            if p_log == "2026": # الدخول السريع للإدارة
                st.session_state.auth = True
                st.session_state.current_user = "مدير المنصة"
                st.rerun()
            else:
                with st.spinner("جاري التحقق..."):
                    user_name = login_user(u_log, p_log)
                    if user_name:
                        st.session_state.auth = True
                        st.session_state.current_user = user_name
                        st.rerun()
                    else:
                        st.error("البيانات غير صحيحة")

    with t_reg:
        r_name = st.text_input("Name", placeholder="الاسم بالكامل", label_visibility="collapsed", key="r_n")
        r_email = st.text_input("Email", placeholder="البريد الإلكتروني", label_visibility="collapsed", key="r_e")
        r_pass = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="r_p")
        r_wa = st.text_input("WA", placeholder="رقم الواتساب", label_visibility="collapsed", key="r_w")
        r_co = st.text_input("CO", placeholder="اسم الشركة", label_visibility="collapsed", key="r_c")
        
        if st.button("تأكيد طلب الاشتراك", use_container_width=True):
            if r_name and r_pass and r_email:
                with st.spinner("جاري التسجيل..."):
                    if signup_user(r_name, r_pass, r_email, r_wa, r_co):
                        st.success("تم تسجيلك بنجاح! يمكنك الدخول الآن.")
                    else: st.error("فشل الاتصال بالسيرفر")
            else: st.warning("يرجى ملء البيانات الأساسية")
            
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. الواجهة الداخلية بعد الدخول ---
else:
    st.markdown(f"<h2 style='text-align:center; color:#f59e0b; padding-top:100px;'>مرحباً بك {st.session_state.current_user}</h2>", unsafe_allow_html=True)
    # هنا تضع بقية كود المنصة (المشاريع، المساعد الذكي، إلخ)
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
