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

# 2. الرابط الخاص بك
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# 3. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- وظائف الربط ---
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

@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."
    except: return "MA3LOMATI PRO 2026"

news_text = get_real_news()

# 4. التنسيق الجمالي (كل شيء من اليمين RTL)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* جعل الصفحة بالكامل من اليمين */
    [data-testid="stAppViewContainer"], .main {{ 
        direction: rtl !important; 
        text-align: right !important; 
        background-color: #050505; 
        font-family: 'Cairo', sans-serif; 
    }}
    
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    /* تنسيق نصوص شاشة الدخول */
    .stTabs [data-baseweb="tab-list"] {{ direction: rtl !important; gap: 30px; }}
    .stTabs [data-baseweb="tab"] {{ 
        font-size: 26px !important; 
        font-weight: 900 !important; 
        color: #888 !important;
    }}
    .stTabs [aria-selected="true"] {{ color: #f59e0b !important; }}

    /* تسميات المدخلات بخط كبير */
    label {{ 
        font-size: 22px !important; 
        color: #f59e0b !important; 
        font-weight: bold !important; 
        display: block !important;
        text-align: right !important;
    }}

    input {{ 
        font-size: 22px !important; 
        text-align: right !important;
        background-color: #111 !important; 
        color: white !important; 
    }}

    /* الأزرار الكبيرة */
    div.stButton > button {{ 
        width: 100% !important;
        height: 65px !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        border-radius: 15px !important;
        background-color: #f59e0b !important;
        color: black !important;
        border: none !important;
    }}

    /* شريط الأخبار */
    .ticker-wrap {{ width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 20px; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #f59e0b; font-size: 14px; font-weight: bold; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* كروت المشاريع */
    div.stButton > button[key*="card_"] {{
        background-color: white !important; color: #111 !important;
        min-height: 140px !important; text-align: right !important;
        font-weight: bold !important; font-size: 16px !important;
        border-right: 8px solid #f59e0b !important;
    }}
    .smart-box {{ background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول (نصوص إنجليزية - اتجاه يمين)
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:50px;'><h1 style='color:#f59e0b; font-size:70px; font-weight:900;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["SIGN IN", "CREATE ACCOUNT"])
    
    with tab_login:
        _, c2, _ = st.columns([1,2,1])
        with c2:
            u_input = st.text_input("Username / Email", key="log_user")
            p_input = st.text_input("Password", type="password", key="log_pass")
            if st.button("LOGIN 🚀"):
                if p_input == "2026": 
                    st.session_state.auth, st.session_state.current_user = True, "Admin"
                    st.rerun()
                else:
                    user_verified = login_user(u_input, p_input)
                    if user_verified:
                        st.session_state.auth, st.session_state.current_user = True, user_verified
                        st.rerun()
                    else: st.error("Invalid Login Details")

    with tab_signup:
        _, c2, _ = st.columns([1,2,1])
        with c2:
            reg_name = st.text_input("Full Name")
            reg_pass = st.text_input("Password", type="password")
            reg_email = st.text_input("Gmail Address")
            reg_wa = st.text_input("WhatsApp Number")
            reg_co = st.text_input("Company Name")
            if st.button("SIGN UP ✅"):
                if reg_name and reg_pass and reg_email:
                    if signup_user(reg_name, reg_pass, reg_email, reg_wa, reg_co):
                        st.success("Success! Please Sign In.")
                    else: st.error("Connection Error")
    st.stop()

# 6. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 7. الهيدر والمنيو (كل شيء يمين)
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 180px; background-size: cover; background-position: center; border-radius: 0 0 30px 30px; 
                display: flex; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b;">
        <h1 style="color: white; font-size: 40px;">أهلاً بك يا {st.session_state.current_user}</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

menu = option_menu(None, ["المساعد الذكي", "المشاريع", "أدوات البروكر"], 
    icons=["robot", "search", "briefcase"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# (تكملة الأقسام البرمجية المعتادة...)
if menu == "المشاريع":
    search = st.text_input("🔍 ابحث عن مشروع")
    dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
    for i in range(0, len(dff.head(6)), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(dff):
                row = dff.iloc[i+j]
                if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}", key=f"card_p_{i+j}"):
                    st.session_state.selected_item = row; st.rerun()

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
