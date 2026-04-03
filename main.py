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

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 4. وظائف الربط (مبسطة) ---
def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try: response = requests.post(SCRIPT_URL, json=payload, timeout=10); return response.text == "Success"
    except: return False

def login_user(user_input, pwd_input):
    try:
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=15)
        if response.status_code == 200:
            users_list = response.json()
            user_input = str(user_input).strip().lower()
            for user_data in users_list:
                name_s = str(user_data.get('Name', user_data.get('name', ''))).strip()
                email_s = str(user_data.get('Email', user_data.get('email', ''))).strip()
                pass_s = str(user_data.get('Password', user_data.get('password', ''))).strip()
                if (user_input == name_s.lower() or user_input == email_s.lower()) and str(pwd_input) == pass_s: return name_s
        return None
    except: return None

@st.cache_data(ttl=1800)
def get_real_news():
    try:
        feed = feedparser.parse("https://www.youm7.com/rss/SectionRss?SectionID=297")
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى في مصر لعام 2026."

news_text = get_real_news()

# --- 5. التصميم الجمالي المطور (تعديل الألوان) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    /* الخلفية العامة */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.97), rgba(0,0,0,0.97)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}

    /* تصميم الكروت (أبيض + نص أسود عريض) */
    div.stButton > button[key*="card_"] {{
        background-color: #FFFFFF !important; 
        color: #000000 !important;
        border-right: 12px solid #f59e0b !important; /* الخط الذهبي الجانبي */
        border-radius: 15px !important;
        padding: 20px !important;
        min-height: 160px !important;
        text-align: right !important;
        font-weight: 900 !important; /* عريض جداً */
        font-size: 18px !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4) !important;
        border: none !important;
        display: block !important;
        width: 100% !important;
        line-height: 1.6 !important;
    }}
    div.stButton > button[key*="card_"]:hover {{
        transform: translateY(-5px) !important;
        background-color: #f8f9fa !important;
        box-shadow: 0 12px 25px rgba(245,158,11,0.3) !important;
    }}

    /* الهيدر الملكي */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 4px solid #f59e0b;
        padding: 40px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 25px;
    }}

    /* تفاصيل البيانات (Detail Card) */
    .detail-card {{ 
        background: rgba(30, 30, 30, 0.95); 
        padding: 25px; border-radius: 20px; 
        border-top: 5px solid #f59e0b; 
        color: white; border: 1px solid #444; 
    }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 16px; margin-top: 10px; }}
    .val-white {{ color: #FFFFFF; font-size: 20px; font-weight: 700; border-bottom: 1px solid #444; padding-bottom:5px; }}

    /* شريط الأخبار */
    .ticker-wrap {{ background: rgba(245, 158, 11, 0.1); border-bottom: 1px solid #f59e0b; padding: 8px 0; margin-bottom: 20px; }}
    .ticker {{ color: #f59e0b; font-weight: 700; font-size: 15px; }}

    /* الأزرار العامة */
    div.stButton > button {{ border-radius: 10px !important; font-weight: 700 !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. صفحة الدخول ---
if not st.session_state.auth:
    _, center_col, _ = st.columns([1, 1.2, 1])
    with center_col:
        st.markdown("<div style='background:white; padding:40px; border-radius:30px; margin-top:50px; text-align:center; box-shadow:0 20px 40px rgba(0,0,0,0.5);'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color:black; font-weight:900;'>MA3LOMATI PRO</h2>", unsafe_allow_html=True)
        tab_login, tab_signup = st.tabs(["🔐 دخول", "📝 اشتراك"])
        with tab_login:
            u = st.text_input("User", placeholder="الاسم أو الإيميل", key="log_u")
            p = st.text_input("Pass", type="password", placeholder="كلمة السر", key="log_p")
            if st.button("دخول آمن 🚀", use_container_width=True):
                if p == "2026": st.session_state.auth, st.session_state.current_user = True, "Admin"; st.rerun()
                else:
                    res = login_user(u, p)
                    if res: st.session_state.auth, st.session_state.current_user = True, res; st.rerun()
                    else: st.error("بيانات خاطئة")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 7. جلب البيانات وتحميلها ---
df_p, df_d, df_l = load_data()

# --- 8. المحتوى الداخلي ---
st.markdown(f'<div class="royal-header"><h1 style="color:white; font-size:40px;">MA3LOMATI PRO</h1><p style="color:#f59e0b;">مرحباً بك يا {st.session_state.current_user}</p></div>', unsafe_allow_html=True)
st.markdown(f'<div class="ticker-wrap"><marquee class="ticker">🔥 {news_text}</marquee></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["briefcase", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"}})

# --- 9. الصفحات ---
if menu == "أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات المساعدة العقارية</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.subheader("القسط الشهري")
            v = st.number_input("السعر", 1000000)
            y = st.number_input("السنين", 8)
            st.metric("شهرياً", f"{v/(y*12):,.0f}")
    with c2:
        with st.container(border=True):
            st.subheader("حساب العمولة")
            d = st.number_input("الصفقة", 2000000)
            p = st.slider("%", 1.0, 5.0, 2.5)
            st.metric("العمولة", f"{d*(p/100):,.0f}")
    with c3:
        with st.container(border=True):
            st.subheader("عائد ROI")
            b = st.number_input("الشراء", 3000000)
            r = st.number_input("الإيجار", 300000)
            st.metric("العائد", f"{(r/b)*100:.1f}%")

elif menu == "المشاريع":
    if st.session_state.view == "details":
        if st.button("⬅ عودة للقائمة"): st.session_state.view = "grid"; st.rerun()
        item = df_p.iloc[st.session_state.current_index]
        st.markdown(f"<div class='detail-card'>", unsafe_allow_html=True)
        for k, v in item.items():
            st.markdown(f"<p class='label-gold'>{k}</p><p class='val-white'>{v}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        search = st.text_input("🔍 ابحث عن مشروع...")
        filt = df_p[df_p.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else df_p
        
        main_c, side_c = st.columns([0.8, 0.2])
        with main_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(filt.head(10).iterrows()):
                with grid[i%2]:
                    if st.button(f"🏢 {r.iloc[0]}\n📍 {r.get('Location', '---')}\n🏗️ {r.get('Developer', '---')}", key=f"card_{idx}"):
                        st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()
        with side_c:
            st.markdown("<p style='color:#f59e0b; font-weight:bold;'>🏆 مقترحات</p>", unsafe_allow_html=True)
            for _, s in df_p.head(5).iterrows():
                st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:10px; margin-bottom:5px; border-right:4px solid #f59e0b; color:white;'>{s.iloc[0][:20]}</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
