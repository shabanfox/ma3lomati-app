import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة الفخمة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. الرابط الخاص بك لربط الجوجل شيت
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# 3. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- وظائف الربط ---
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

@st.cache_data(ttl=3600)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "MA3LOMATI PRO 2026: السوق العقاري في أمان."
    except: return "مرحباً بك في النسخة الاحترافية من معلوماتي برو."

news_text = get_real_news()

# 4. التنسيق الجمالي الشامل (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}

    /* شاشة الدخول - English & Big */
    .stTabs [data-baseweb="tab-list"] {{ justify-content: center; gap: 40px; }}
    .stTabs [data-baseweb="tab"] {{ font-size: 28px !important; font-weight: 900 !important; color: #888 !important; }}
    .stTabs [aria-selected="true"] {{ color: #f59e0b !important; border-bottom: 4px solid #f59e0b !important; }}
    label {{ font-size: 24px !important; color: #f59e0b !important; font-weight: bold !important; }}
    input {{ font-size: 24px !important; background-color: #111 !important; color: white !important; border: 1px solid #333 !important; border-radius: 12px !important; }}

    /* أزرار الدخول والخروج */
    div.stButton > button {{ border-radius: 15px !important; transition: 0.3s !important; font-weight: 900 !important; }}
    .login-btn button {{ height: 70px !important; font-size: 26px !important; background-color: #f59e0b !important; color: black !important; }}
    .logout-btn button {{ background-color: transparent !important; color: #ff4b4b !important; border: 1px solid #ff4b4b !important; font-size: 14px !important; padding: 5px 15px !important; }}

    /* شريط الأخبار البطئ */
    .ticker-wrap {{ width: 100%; background: #0a0a0a; padding: 8px 0; overflow: hidden; border-bottom: 1px solid #222; margin-bottom: 15px; }}
    .ticker {{ display: inline-block; animation: ticker 120s linear infinite; color: #f59e0b; font-size: 16px; font-weight: bold; white-space: nowrap; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* كروت المشاريع (أسود فخم + كتابة ذهبية) */
    div.stButton > button[key*="card_"] {{
        background-color: #111 !important; 
        color: #f59e0b !important;
        min-height: 140px !important; 
        text-align: right !important;
        font-weight: bold !important; 
        font-size: 17px !important;
        border: 1px solid #222 !important; 
        border-right: 8px solid #f59e0b !important;
        display: block !important; 
        width: 100% !important;
    }}
    div.stButton > button[key*="card_"]:hover {{ background-color: #1a1a1a !important; border-color: #f59e0b !important; }}
    
    .smart-box {{ background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; }}
    .side-card {{ background: #161616; padding: 15px; border-radius: 12px; border: 1px solid #222; margin-bottom: 8px; color: #f59e0b; }}
    .tool-card {{ background: #1a1a1a; padding: 20px; border-radius: 15px; border-top: 4px solid #f59e0b; text-align: center; }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:60px;'><h1 style='color:#f59e0b; font-size:80px;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    tab_login, tab_signup = st.tabs(["SIGN IN", "CREATE ACCOUNT"])
    with tab_login:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            u_input = st.text_input("Username or Email", key="log_user")
            p_input = st.text_input("Password", type="password", key="log_pass")
            st.markdown('<div class="login-btn">', unsafe_allow_html=True)
            if st.button("LOGIN NOW 🚀"):
                if p_input == "2026":
                    st.session_state.auth, st.session_state.current_user = True, "Admin"
                    st.rerun()
                else:
                    user_verified = login_user(u_input, p_input)
                    if user_verified:
                        st.session_state.auth, st.session_state.current_user = True, user_verified
                        st.rerun()
                    else: st.error("Access Denied")
            st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 6. جلب البيانات
@st.cache_data(ttl=600)
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

# 7. الهيدر وزر الخروج
c_h1, c_h2 = st.columns([0.85, 0.15])
with c_h2:
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("🚪 Logout"): 
        st.session_state.auth = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 200px; background-size: cover; background-position: center; border-radius: 25px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 5px solid #f59e0b;">
        <h1 style="color: white; margin: 0; font-size: 50px;">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-size: 18px;">Welcome, {st.session_state.current_user}</p>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

# 8. المنيو الرئيسي
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "حقيبة البروكر"], 
    icons=["robot", "search", "building", "briefcase"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# 9. المحتوى
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"<div class='smart-box'><h2>{item.get('ProjectName', item.get('Developer'))}</h2><p>📍 {item.get('Location', '---')}</p><hr>{item.get('Payment Plan', '---')}</div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    m_col, s_col = st.columns([0.7, 0.3])
    with s_col:
        st.markdown("<h4 style='color:#10b981; text-align:center;'>🔑 استلام فوري</h4>", unsafe_allow_html=True)
        ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(8)
        for i, r in ready.iterrows():
            if st.button(f"✅ {r['ProjectName']}", key=f"ready_{i}"):
                st.session_state.selected_item = r; st.rerun()

    with m_col:
        search = st.text_input("🔍 ابحث عن مشروع...")
        dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
        start = st.session_state.p_idx * 6
        page = dff.iloc[start:start+6]
        for i in range(0, len(page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page):
                    row = page.iloc[i+j]
                    if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}", key=f"card_p_{start+i+j}"):
                        st.session_state.selected_item = row; st.rerun()

elif menu == "المطورين":
    m_col, s_col = st.columns([0.7, 0.3])
    with s_col:
        st.markdown("<h4 style='color:#f59e0b; text-align:center;'>🏆 أفضل المطورين</h4>", unsafe_allow_html=True)
        for i, r in df_d.head(10).iterrows():
            st.markdown(f"<div class='side-card'><b>{i+1}. {r['Developer']}</b></div>", unsafe_allow_html=True)
    with m_col:
        search_d = st.text_input("🔍 ابحث عن مطور...")
        dfd_f = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
        for i in range(0, len(dfd_f.head(6)), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(dfd_f):
                    row = dfd_f.iloc[i+j]
                    if cols[j].button(f"🏗️ {row['Developer']}\n⭐ الفئة: {row.get('Developer Category','A')}", key=f"card_d_{i+j}"):
                        st.session_state.selected_item = row; st.rerun()

elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 المساعد الذكي")
    c1, c2 = st.columns(2)
    loc = c1.selectbox("📍 المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    client = st.text_input("رقم واتساب العميل")
    if st.button("🎯 ترشيح أفضل الوحدات"):
        st.success("جاري البحث في قاعدة البيانات...")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "حقيبة البروكر":
    st.title("🛠️ أدوات البروكر")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='tool-card'><h3>💳 القسط</h3>", unsafe_allow_html=True)
        v = st.number_input("السعر", 1000000)
        st.metric("شهرياً (8 سنوات)", f"{v/(8*12):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='tool-card'><h3>💰 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("الصفقة", 1000000)
        st.metric("العمولة (1.5%)", f"{deal*0.015:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='tool-card'><h3>📈 ROI</h3>", unsafe_allow_html=True)
        buy = st.number_input("الشراء", 1000000)
        rent = st.number_input("الإيجار", 100000)
        st.metric("العائد", f"{(rent/buy)*100:,.1f}%")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
