import streamlit as st
import pandas as pd
import requests
import feedparser
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu
from streamlit_autorefresh import st_autorefresh

# 1. الإعدادات الأساسية
st.set_page_config(page_title="KMT PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# تحديث الساعة تلقائياً كل ثانية
st_autorefresh(interval=1000, key="clock_sync")

# 2. روابط الربط (تأكد من صحتها)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"

# 3. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 4. تنسيق الواجهة (أسود وذهبي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Orbitron:wght@500&display=swap');
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    
    /* شاشة الدخول */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 40px; }
    .stTabs [data-baseweb="tab"] { font-size: 28px !important; font-weight: 900 !important; color: #444 !important; }
    .stTabs [aria-selected="true"] { color: #f59e0b !important; border-bottom: 4px solid #f59e0b !important; }
    
    label { font-size: 20px !important; color: #f59e0b !important; font-weight: bold !important; text-align: right !important; display: block; }
    input { font-size: 18px !important; text-align: right !important; background-color: #111 !important; color: white !important; border: 1px solid #333 !important; border-radius: 10px !important; height: 45px !important; }

    /* الأزرار */
    div.stButton > button { border-radius: 10px !important; font-weight: 900 !important; width: 100% !important; transition: 0.3s; }
    .login-btn button { height: 60px !important; font-size: 24px !important; background-color: #f59e0b !important; color: black !important; border: none !important; }
    .logout-btn button { background-color: #ff4b4b !important; color: white !important; font-size: 12px !important; height: 35px !important; }

    /* الكروت */
    div.stButton > button[key*="card_"] {
        background-color: #111 !important; color: #f59e0b !important;
        min-height: 120px !important; text-align: right !important;
        border: 1px solid #222 !important; border-right: 8px solid #f59e0b !important;
    }

    /* شريط الأخبار */
    .ticker-wrap { width: 100%; background: #000; padding: 10px 0; overflow: hidden; border-bottom: 1px solid #222; margin: 10px 0; }
    .ticker { display: inline-block; animation: ticker 150s linear infinite; color: #f59e0b; font-size: 15px; font-weight: bold; white-space: nowrap; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    </style>
""", unsafe_allow_html=True)

# 5. دوال الربط والتحقق
def verify_login(u, p):
    # خيار المطور السريع (2026) لضمان الدخول في حال فشل السيرفر
    if p == "2026":
        return "المطور"
    try:
        # جلب البيانات من الجوجل شيت
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=8)
        if response.status_code == 200:
            users = response.json()
            for user in users:
                # التحقق من الاسم أو الإيميل مع تجاهل المسافات وحالة الأحرف
                db_name = str(user.get('Name', '')).strip().lower()
                db_email = str(user.get('Email', '')).strip().lower()
                db_pass = str(user.get('Password', '')).strip()
                
                input_u = u.strip().lower()
                if (input_u == db_name or input_u == db_email) and p.strip() == db_pass:
                    return user.get('Name')
        return None
    except:
        return None

# 6. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#f59e0b; font-size:70px; font-weight:900;'>KMT PRO</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["SIGN IN", "CREATE ACCOUNT"])
    with t1:
        _, c2, _ = st.columns([1, 1.5, 1])
        with c2:
            u = st.text_input("Username / Email", key="user_field")
            p = st.text_input("Password", type="password", key="pass_field")
            st.markdown('<div class="login-btn">', unsafe_allow_html=True)
            if st.button("LOGIN NOW 🚀"):
                user_name = verify_login(u, p)
                if user_name:
                    st.session_state.auth = True
                    st.session_state.current_user = user_name
                    st.rerun()
                else:
                    st.error("خطأ في البيانات أو في الاتصال بالسيرفر. (استخدم 2026 للدخول الطارئ)")
            st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 7. الهيدر العلوي (الساعة واليوزر)
egypt_now = datetime.now(pytz.timezone('Africa/Cairo'))
c_h1, c_h2, c_h3 = st.columns([0.4, 0.45, 0.15])
with c_h1:
    st.markdown(f"<div style='color:#f59e0b; font-weight:bold; padding-top:10px;'>👤 {st.session_state.current_user}</div>", unsafe_allow_html=True)
with c_h2:
    st.markdown(f"""<div style='text-align: left; padding-top: 8px;'>
        <span style='color: #f59e0b; font-size: 22px; font-weight: bold; font-family: "Orbitron";'>{egypt_now.strftime('%I:%M:%S %p')}</span>
        <span style='color: #444; margin: 0 10px;'>|</span>
        <span style='color: #888; font-size: 14px;'>{egypt_now.strftime('%Y-%m-%d')}</span>
    </div>""", unsafe_allow_html=True)
with c_h3:
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("Logout"): 
        st.session_state.auth = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# الهيدر الصوري
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 160px; background-size: cover; background-position: center; border-radius: 20px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b;">
        <h1 style="color: white; margin: 0; font-size: 50px; font-weight:900;">KMT PRO</h1>
        <p style="color: #f59e0b; font-weight: bold;">EGYPTIAN REAL ESTATE HUB</p>
    </div>
""", unsafe_allow_html=True)

# 8. المنيو والبيانات
@st.cache_data(ttl=600)
def get_data():
    p = pd.read_csv(URL_PROJECTS).fillna("---")
    d = pd.read_csv(URL_DEVELOPERS).fillna("---")
    p.rename(columns={'Area': 'Location', 'Project Name': 'ProjectName'}, inplace=True, errors='ignore')
    return p, d

df_p, df_d = get_data()

menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "حقيبة البروكر"], 
    icons=["robot", "search", "building", "briefcase"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# 9. الصفحات
if menu == "المشاريع":
    search = st.text_input("🔍 ابحث عن مشروع...")
    dff = df_p[df_p.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)] if search else df_p
    for i in range(0, len(dff.head(6)), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(dff.head(6)):
                row = dff.iloc[i+j]
                cols[j].button(f"🏢 {row.get('ProjectName','---')}\n📍 {row.get('Location','---')}", key=f"card_{i+j}")

elif menu == "حقيبة البروكر":
    st.title("🛠️ أدوات البروكر")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("💳 حساب القسط")
        price = st.number_input("السعر", 1000000)
        st.write(f"القسط الشهري (8 سنوات): {price/(8*12):,.0f}")
    with c2:
        st.subheader("💰 العمولة")
        val = st.number_input("قيمة الصفقة", 1000000)
        st.write(f"العمولة (1.5%): {val*0.015:,.0f}")

st.markdown("<p style='text-align:center; color:#333; margin-top:50px;'>KMT PRO © 2026</p>", unsafe_allow_html=True)
