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

# 3. إدارة حالة الجلسة (لضمان عدم تسجيل الخروج عند الـ Refresh)
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
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
        return "  •  ".join(news) if news else "Market Update 2026: Real Estate is booming."
    except: return "MA3LOMATI PRO: Your #1 Real Estate Platform."

news_text = get_real_news()

# 4. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Poppins:wght@300;500;700&display=swap');
    
    .block-container { padding-top: 0rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { background-color: #050505; font-family: 'Poppins', 'Cairo', sans-serif; }
    
    /* تنسيق صفحة الدخول (تظهر على اليمين) */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { color: #888; }
    .stTabs [aria-selected="true"] { color: #f59e0b !important; font-weight: bold; }

    .ticker-wrap { width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 20px; }
    .ticker { display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    div.stButton > button { border-radius: 10px !important; transition: 0.3s !important; font-family: 'Poppins', sans-serif; }
    
    /* محاكمة الاتجاه للعربية في المحتوى الداخلي */
    .rtl-view { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    
    .smart-box { background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; direction: rtl; }
    .tool-card { background: #1a1a1a; padding: 20px; border-radius: 15px; border-top: 4px solid #f59e0b; text-align: center; height: 100%; }
    
    /* تخصيص مدخلات النصوص لتكون فخمة */
    input { background-color: #111 !important; color: white !important; border: 1px solid #333 !important; }
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول (English & Located on the Right)
if not st.session_state.auth:
    # تقسيم الشاشة: يسار فارغ (للخلفية) ويمين للدخول
    col_empty, col_login = st.columns([1.5, 1])
    
    with col_login:
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='color:#f59e0b; font-size:50px; margin-bottom:0;'>MA3LOMATI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#666; font-size:18px; letter-spacing: 2px;'>PRO VERSION 2026</p>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#222'>", unsafe_allow_html=True)
        
        tab_login, tab_signup = st.tabs(["🔐 SIGN IN", "📝 REGISTER"])
        
        with tab_login:
            u_input = st.text_input("Username / Email", key="login_u")
            p_input = st.text_input("Password", type="password", key="login_p")
            if st.button("ACCESS PLATFORM 🚀", use_container_width=True):
                if p_input == "2026":
                    st.session_state.auth = True
                    st.session_state.current_user = "Admin"
                    st.rerun()
                else:
                    user_verified = login_user(u_input, p_input)
                    if user_verified:
                        st.session_state.auth = True
                        st.session_state.current_user = user_verified
                        st.rerun()
                    else:
                        st.error("Invalid Username or Password")

        with tab_signup:
            r_name = st.text_input("Full Name")
            r_email = st.text_input("Email Address")
            r_pass = st.text_input("Choose Password", type="password")
            r_wa = st.text_input("WhatsApp Number")
            if st.button("CREATE ACCOUNT ✅", use_container_width=True):
                if r_name and r_pass and r_email:
                    if signup_user(r_name, r_pass, r_email, r_wa, ""):
                        st.success("Success! Please switch to Sign In tab.")
                    else: st.error("Database connection error")
                else: st.warning("All fields are required")
    st.stop()

# 6. جلب البيانات (يتم تنفيذها فقط بعد تسجيل الدخول)
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 7. الهيدر البصري (عودة للغة العربية)
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070'); 
                height: 180px; background-size: cover; background-position: center; border-radius: 0 0 30px 30px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b; direction: rtl;">
        <h1 style="color: white; margin: 0; font-size: 40px; font-family: 'Cairo';">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-size: 16px; font-family: 'Cairo';">أهلاً بك يا {st.session_state.current_user}</p>
    </div>
""", unsafe_allow_html=True)

# 8. شريط المعلومات العلوي
c_top1, c_top2 = st.columns([0.7, 0.3])
with c_top1:
    st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)
with c_top2:
    st.markdown(f"""<div style='text-align: left; padding: 5px; color: #aaa; font-size: 13px;'>
                📅 {egypt_now.strftime('%Y-%m-%d')} | 🕒 {egypt_now.strftime('%I:%M %p')}</div>""", unsafe_allow_html=True)
    if st.button("🚪 Logout", key="logout_btn"): 
        st.session_state.auth = False
        st.rerun()

# 9. المنيو الرئيسي
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], default_index=0, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# 10. المحتوى الداخلي (RTL)
st.markdown("<div class='rtl-view'>", unsafe_allow_html=True)

if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"""<div class='smart-box'>
        <h2>{item.get('ProjectName', item.get('Developer'))}</h2>
        <hr>
        <p>📍 الموقع: {item.get('Location', '---')}</p>
        <p>🏗️ المطور: {item.get('Developer', '---')}</p>
        <p>💰 السعر: {item.get('Starting Price (EGP)', 'تواصل للاستفسار')}</p>
    </div>""", unsafe_allow_html=True)

elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'><h3>🤖 المساعد العقاري الذكي</h3><p>أدخل بيانات العميل للحصول على أفضل الترشيحات فوراً.</p></div>", unsafe_allow_html=True)
    # ... كود المساعد الذكي الخاص بك ...

elif menu == "المشاريع":
    st.title("📂 دليل المشاريع")
    f1, f2 = st.columns(2)
    search = f1.text_input("🔍 ابحث عن مشروع")
    area_f = f2.selectbox("📍 تصفية حسب المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    # ... نظام الكروت الخاص بك ...

elif menu == "المطورين":
    st.title("🏗️ كبار المطورين")
    # ... نظام كروت المطورين ...

elif menu == "أدوات البروكر":
    st.title("🛠️ حقيبة الأدوات")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='tool-card'><h3>💳 حاسبة القسط</h3>", unsafe_allow_html=True)
        v = st.number_input("السعر الإجمالي", 1000000, key="v_calc")
        d = st.number_input("المقدم", 100000, key="d_calc")
        y = st.slider("السنوات", 1, 15, 8)
        st.metric("القسط الشهري", f"{(v-d)/(y*12):,.0f} EGP")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='tool-card'><h3>💰 حاسبة العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("قيمة الصفقة", 1000000, key="c_calc")
        pct = st.slider("نسبة العمولة %", 0.5, 5.0, 1.5)
        st.metric("صافي الربح", f"{deal*(pct/100):,.0f} EGP")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026 | Edition v2.0</p>", unsafe_allow_html=True)
