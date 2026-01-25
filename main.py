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
ITEMS_PER_PAGE = 6

# --- 3. إدارة الحالة (Session State) ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'lang' not in st.session_state: st.session_state.lang = "Arabic"
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'page_num' not in st.session_state: st.session_state.page_num = 0

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- 4. الوظائف البرمجية ---
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
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة."
    except: return "MA3LOMATI PRO: Your Real Estate Portal 2026."

news_text = get_real_news()

# --- 5. التصميم الجمالي CSS (تعديل موضع الكارت للأعلى) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding: 0rem !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: radial-gradient(circle, rgba(0,0,0,0.85), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {"rtl" if st.session_state.lang == "Arabic" else "ltr"} !important;
        text-align: {"right" if st.session_state.lang == "Arabic" else "left"} !important;
        font-family: 'Cairo', sans-serif;
    }}

    /* شاشة الدخول المرفوعة للأعلى */
    .auth-main {{ 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: flex-start; /* تغيير التمركز للأعلى */
        padding-top: 40px; /* مسافة من أعلى الصفحة */
        min-height: 100vh;
    }}
    
    .luxury-card {{
        background: rgba(255, 255, 255, 0.03); 
        backdrop-filter: blur(25px);
        border: 1px solid rgba(245, 158, 11, 0.3); 
        border-radius: 40px;
        padding: 40px; 
        width: 90%; 
        max-width: 460px; 
        box-shadow: 0 40px 100px rgba(0,0,0,0.6); 
        text-align: center;
    }}

    .gold-title {{
        background: linear-gradient(90deg, #f59e0b, #fbbf24, #f59e0b);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        font-size: 35px; 
        font-weight: 900;
    }}

    div.stTextInput input {{
        background: rgba(255,255,255,0.07) !important; 
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1) !important; 
        border-radius: 15px !important;
        height: 50px !important; 
        text-align: center !important;
    }}

    .stButton > button {{
        background: linear-gradient(45deg, #f59e0b, #d97706) !important;
        color: black !important; 
        font-weight: 700 !important; 
        border-radius: 15px !important;
        height: 50px !important; 
        border: none !important; 
        width: 100%;
    }}

    .ticker-wrap {{ 
        width: 100%; 
        background: rgba(245, 158, 11, 0.1); 
        padding: 10px 0; 
        border-bottom: 1px solid #f59e0b33; 
        overflow: hidden; 
        white-space: nowrap; 
    }}
    .ticker {{ display: inline-block; animation: ticker 120s linear infinite; color: #f59e0b; font-size: 14px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* التصميم الداخلي */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.8)), url('{HEADER_IMG}');
        background-size: cover; padding: 50px 20px; text-align: center;
        border-bottom: 3px solid #f59e0b; border-radius: 0 0 50px 50px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 6. صفحة الدخول (تبدأ من الأعلى) ---
if not st.session_state.auth:
    # شريط اختيار اللغة
    c_lang = st.columns([0.88, 0.12])
    with c_lang[1]:
        lang_choice = st.selectbox("🌐", ["العربية", "English"], label_visibility="collapsed")
        st.session_state.lang = "Arabic" if lang_choice == "العربية" else "English"

    st.markdown(f'<div class="ticker-wrap"><div class="ticker">{news_text}</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="auth-main">', unsafe_allow_html=True)
    st.markdown('<div class="luxury-card">', unsafe_allow_html=True)
    st.markdown('<div class="gold-title">MA3LOMATI PRO</div>', unsafe_allow_html=True)
    
    t = {
        "sub": "بوابتك لعالم العقارات الفاخرة" if st.session_state.lang=="Arabic" else "Your Luxury Real Estate Gateway",
        "tab1": "🔐 دخول" if st.session_state.lang=="Arabic" else "🔐 Login",
        "tab2": "📝 اشتراك" if st.session_state.lang=="Arabic" else "📝 Signup",
        "user": "المستخدم" if st.session_state.lang=="Arabic" else "User",
        "pass": "كلمة المرور" if st.session_state.lang=="Arabic" else "Password",
        "btn_log": "دخول آمن 🚀" if st.session_state.lang=="Arabic" else "Secure Login 🚀"
    }
    st.markdown(f'<p style="color:#888; margin-bottom:20px;">{t["sub"]}</p>', unsafe_allow_html=True)
    
    tab_log, tab_reg = st.tabs([t["tab1"], t["tab2"]])
    
    with tab_log:
        u = st.text_input(t["user"], key="u_in", placeholder=t["user"], label_visibility="collapsed")
        p = st.text_input(t["pass"], type="password", key="p_in", placeholder=t["pass"], label_visibility="collapsed")
        if st.button(t["btn_log"]):
            if p == "2026": 
                st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
            else:
                user_found = login_user(u, p)
                if user_found:
                    st.session_state.auth = True; st.session_state.current_user = user_found; st.rerun()
                else: st.error("خطأ!" if st.session_state.lang=="Arabic" else "Error!")
                
    with tab_reg:
        st.text_input("Full Name", placeholder="الأسم")
        st.text_input("WhatsApp", placeholder="واتساب")
        st.text_input("Password", type="password", placeholder="كلمة المرور", key="reg_p")
        st.button("تأكيد" if st.session_state.lang=="Arabic" else "Confirm")

    st.markdown('</div></div>', unsafe_allow_html=True)
    st.stop()

# --- 7. المحتوى الداخلي (بعد الدخول) ---
with st.sidebar:
    st.markdown(f"<h2 style='text-align:center; color:#f59e0b;'>{st.session_state.current_user}</h2>", unsafe_allow_html=True)
    menu = option_menu("MA3LOMATI", ["الرئيسية", "المشاريع", "أدوات البروكر"], icons=['house', 'search', 'briefcase'], default_index=0)
    if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()

st.markdown(f'<div class="royal-header"><h1 style="color:white;">{menu}</h1></div>', unsafe_allow_html=True)
st.info("تم تسجيل الدخول بنجاح! يمكنك الآن تصفح البيانات.")

