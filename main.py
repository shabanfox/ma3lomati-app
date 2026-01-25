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

# --- 2. الروابط الأساسية ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'messages' not in st.session_state: st.session_state.messages = []

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- 4. وظائف الربط ---
def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload, timeout=10)
        return response.text == "Success"
    except: return False

def login_user(user_input, pwd_input):
    try:
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=15)
        if response.status_code == 200:
            users_list = response.json()
            user_input = str(user_input).strip().lower()
            pwd_input = str(pwd_input).strip()
            for user_data in users_list:
                name_s = str(user_data.get('Name', user_data.get('name', ''))).strip()
                email_s = str(user_data.get('Email', user_data.get('email', ''))).strip()
                pass_s = str(user_data.get('Password', user_data.get('password', ''))).strip()
                if (user_input == name_s.lower() or user_input == email_s.lower()) and pwd_input == pass_s:
                    return name_s
        return None
    except: return None

@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى في مصر لعام 2026."

news_text = get_real_news()

# --- 5. التصميم الجمالي CSS (نسخة VIP المحدثة) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}

    /* تصميم شاشة الدخول الفاخرة */
    .login-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 60px 20px;
    }}

    .glass-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 40px;
        padding: 50px 40px;
        width: 100%;
        max-width: 500px;
        box-shadow: 0 40px 100px rgba(0,0,0,0.6);
        text-align: center;
        position: relative;
    }}

    .brand-logo {{
        font-size: 42px;
        font-weight: 900;
        background: linear-gradient(to bottom, #f59e0b, #92400e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    .brand-sub {{
        color: #ffffff99;
        font-size: 14px;
        margin-bottom: 40px;
        letter-spacing: 4px;
    }}

    /* تنسيق المدخلات */
    div.stTextInput input {{
        background-color: rgba(0,0,0,0.4) !important;
        color: #fff !important;
        border: 1px solid rgba(245, 158, 11, 0.2) !important;
        border-radius: 15px !important;
        height: 55px !important;
        text-align: center !important;
        font-size: 16px !important;
    }}

    div.stTextInput input:focus {{
        border-color: #f59e0b !important;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.3) !important;
    }}

    /* الأزرار */
    .stButton > button {{
        width: 100% !important;
        background: linear-gradient(90deg, #f59e0b 0%, #d97706 100%) !important;
        color: #000 !important;
        font-weight: 700 !important;
        border: none !important;
        height: 55px !important;
        border-radius: 15px !important;
        font-size: 18px !important;
        transition: 0.5s ease !important;
        margin-top: 20px !important;
    }}

    .stButton > button:hover {{
        transform: scale(1.02) !important;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.4) !important;
    }}

    /* التبويبات (Tabs) */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        justify-content: center;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent !important;
        color: #888 !important;
        font-weight: 600 !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #f59e0b !important;
        border-bottom-color: #f59e0b !important;
    }}

    /* شريط الأخبار */
    .ticker-wrap {{ width: 100%; background: rgba(0,0,0,0.5); padding: 12px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #f59e0b33; }}
    .ticker {{ display: inline-block; animation: ticker 120s linear infinite; color: #f59e0b; font-size: 14px; font-weight: 600; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* عناصر المحتوى الداخلي */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 3px solid #f59e0b;
        padding: 60px 20px; text-align: center; border-radius: 0 0 50px 50px; margin-bottom: 30px;
    }}
    .detail-card {{ background: rgba(30, 30, 30, 0.8); padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; border: 1px solid #444; margin-bottom:20px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. واجهة تسجيل الدخول (The VIP Interface) ---
if not st.session_state.auth:
    # شريط الأخبار العلوي
    st.markdown(f'<div class="ticker-wrap"><div class="ticker">{news_text}</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
            <div class="glass-card">
                <div class="brand-logo">MA3LOMATI PRO</div>
                <div class="brand-sub">LUXURY REAL ESTATE SYSTEM</div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔒 دخول المصرح لهم", "🛡️ طلب انضمام"])
        
        with tab1:
            user_in = st.text_input("اسم المستخدم أو الإيميل", placeholder="أدخل بياناتك هنا", key="l_user")
            pass_in = st.text_input("كلمة المرور", type="password", placeholder="••••••••", key="l_pass")
            if st.button("دخول آمن"):
                name = login_user(user_in, pass_in)
                if name:
                    st.session_state.auth = True
                    st.session_state.current_user = name
                    st.success(f"مرحباً بك سيد {name}")
                    st.rerun()
                else:
                    st.error("عذراً، البيانات غير صحيحة")
        
        with tab2:
            n_name = st.text_input("الأسم بالكامل")
            n_email = st.text_input("البريد الإلكتروني")
            n_wa = st.text_input("رقم الواتساب")
            n_comp = st.text_input("الشركة / المؤسسة")
            n_pass = st.text_input("كلمة المرور", type="password", key="reg_pass")
            
            if st.button("إرسال طلب العضوية"):
                if signup_user(n_name, n_pass, n_email, n_wa, n_comp):
                    st.success("تم تسجيل طلبك بنجاح! يمكنك الدخول الآن.")
                else:
                    st.error("فشل في التسجيل، حاول مرة أخرى.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 7. المحتوى الداخلي (بعد تسجيل الدخول) ---
# يوضع هنا باقي كود تطبيقك الخاص بعرض البيانات والداشبورد
st.markdown(f"""
    <div class="royal-header">
        <h1 style='color: #f59e0b; font-weight: 900; font-size: 50px; margin:0;'>MA3LOMATI PRO</h1>
        <p style='color: white; font-size: 18px; opacity: 0.8;'>مرحباً بك {st.session_state.current_user} في لوحة التحكم الفاخرة</p>
    </div>
""", unsafe_allow_html=True)

if st.button("تسجيل الخروج"):
    st.session_state.auth = False
    st.rerun()
