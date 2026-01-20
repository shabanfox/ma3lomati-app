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

# 4. التنسيق الجمالي (تصحيح خطأ المسافات + تعديل الألوان للأبيض والذهبي)
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    [data-testid="stAppViewContainer"] {{ 
        background-color: #0a192f; 
        direction: rtl !important; 
        text-align: right !important; 
        font-family: 'Cairo', sans-serif; 
    }}
    
    /* نصوص بيضاء واضحة جداً */
    p, span, label, .stWrite, .stMetric div, .stMarkdown {{ 
        color: #ffffff !important; 
        font-weight: 600 !important; 
    }}
    
    h1, h2, h3, h4 {{ color: #f59e0b !important; font-weight: 900 !important; }}

    /* الأزرار العادية */
    div.stButton > button {{ 
        border-radius: 12px !important; 
        background: #112240 !important;
        color: #ffffff !important;
        border: 1px solid #f59e0b !important;
    }}

    /* كروت المشاريع (تصحيح المسافات هنا) */
    div.stButton > button[key*="card_"], div.stButton > button[key*="ready_"] {{
        background: linear-gradient(145deg, #112240, #0a192f) !important;
        color: #ffffff !important;
        min-height: 140px !important; 
        text-align: right !important;
        font-weight: bold !important; 
        border-right: 8px solid #f59e0b !important;
        width: 100% !important;
    }}
    
    div.stButton > button[key*="card_"]:hover {{ 
        transform: translateY(-5px) !important; 
        border-color: #ffffff !important;
    }}
    
    .smart-box {{ 
        background: #112240; 
        border: 1px solid #233554; 
        padding: 25px; 
        border-radius: 20px; 
        border-right: 6px solid #f59e0b; 
        color: #ffffff !important; 
    }}

    /* شريط الأخبار */
    .ticker-wrap {{ background: #112240; border-bottom: 2px solid #f59e0b; padding: 10px; }}
    .ticker {{ color: #f59e0b !important; font-weight: bold; }}
</style>
""", unsafe_allow_html=True)

# 5. نظام الدخول
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; padding-top:50px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    tab_login, tab_signup = st.tabs(["🔐 دخول", "📝 اشتراك"])
    with tab_login:
        u_input = st.text_input("الأسم أو الجيميل", key="log_user")
        p_input = st.text_input("كلمة السر", type="password", key="log_pass")
        if st.button("دخول 🚀"):
            if p_input == "2026" or login_user(u_input, p_input):
                st.session_state.auth = True
                st.session_state.current_user = u_input if u_input else "Admin"
                st.rerun()
    st.stop()

# 6. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p
    except: return pd.DataFrame()

df_p = load_data()

# 7. المنيو والواجهة
st.markdown(f"<div class='ticker-wrap'><div class='ticker'>🔥 {news_text}</div></div>", unsafe_allow_html=True)

menu = option_menu(None, ["المساعد الذكي", "المشاريع", "أدوات البروكر"], 
    icons=["robot", "search", "briefcase"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"<div class='smart-box'><h2>{item['ProjectName']}</h2><p>📍 الموقع: {item['Location']}</p></div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    search = st.text_input("🔍 ابحث هنا")
    dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
    for i in range(0, len(dff.head(6)), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(dff):
                row = dff.iloc[i+j]
                if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}", key=f"card_p_{i+j}"):
                    st.session_state.selected_item = row; st.rerun()

st.markdown("<p style='text-align:center; color:#555;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)

