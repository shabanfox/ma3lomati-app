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

# 3. إدارة حالة الجلسة (الاستقرار)
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- وظائف الربط مع جوجل شيت ---
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

# 4. التنسيق الجمالي (CSS) - تصميم السنتر والفخامة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Poppins:wght@300;500;700&display=swap');
    
    .block-container { padding-top: 0rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { 
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070');
        background-size: cover;
        background-position: center;
        font-family: 'Poppins', 'Cairo', sans-serif; 
    }
    
    /* جعل التبويبات في المنتصف */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 30px; }
    .stTabs [data-baseweb="tab"] { color: #888; font-size: 16px; }
    .stTabs [aria-selected="true"] { color: #f59e0b !important; border-bottom-color: #f59e0b !important; }

    .ticker-wrap { width: 100%; background: rgba(0,0,0,0.5); padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; }
    .ticker { display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    div.stButton > button { border-radius: 12px !important; transition: 0.3s !important; }
    
    .rtl-view { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    .smart-box { background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; }
    
    /* تصميم الحقول */
    input { background-color: #0a0a0a !important; color: white !important; border: 1px solid #333 !important; border-radius: 10px !important; }
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول (Centered Design)
if not st.session_state.auth:
    # إنشاء أعمدة لوضع النموذج في المنتصف
    _, col_mid, _ = st.columns([1, 1.2, 1])
    
    with col_mid:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("""
            <div style='text-align:center;'>
                <h1 style='color:#f59e0b; font-size:55px; margin-bottom:0; letter-spacing: 3px;'>MA3LOMATI</h1>
                <p style='color:#eee; font-size:16px; opacity:0.7;'>PRO REAL ESTATE PLATFORM 2026</p>
                <hr style='border-color: #333; margin: 20px 0;'>
            </div>
        """, unsafe_allow_html=True)
        
        tab_login, tab_signup = st.tabs(["🔐 SIGN IN", "📝 REGISTER"])
        
        with tab_login:
            u_input = st.text_input("Username / Email", key="main_u")
            p_input = st.text_input("Password", type="password", key="main_p")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("LOGIN TO DASHBOARD 🚀", use_container_width=True):
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
                        st.error("Authentication Failed: Check credentials")

        with tab_signup:
            r_name = st.text_input("Full Name", key="s1")
            r_email = st.text_input("Email", key="s2")
            r_pass = st.text_input("Password", type="password", key="s3")
            r_wa = st.text_input("WhatsApp Number", key="s4")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("CREATE NEW ACCOUNT ✅", use_container_width=True):
                if r_name and r_pass and r_email:
                    if signup_user(r_name, r_pass, r_email, r_wa, ""):
                        st.success("Account Created! Please Sign In.")
                    else: st.error("Database connection error")
                else: st.warning("Please complete the form")
    st.stop()

# 6. جلب البيانات (بعد الدخول فقط)
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

# 7. واجهة المستخدم بعد الدخول (RTL)
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070'); 
                height: 150px; background-size: cover; background-position: center; border-radius: 0 0 30px 30px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b; direction: rtl;">
        <h1 style="color: white; margin: 0; font-size: 35px; font-family: 'Cairo';">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-family: 'Cairo';">مرحباً بك، {st.session_state.current_user}</p>
    </div>
""", unsafe_allow_html=True)

# 8. شريط الأخبار
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

# 9. المنيو والتحكم
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], default_index=0, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# 10. عرض المحتوى
st.markdown("<div class='rtl-view'>", unsafe_allow_html=True)

if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"<div class='smart-box'><h2>{item.get('ProjectName', item.get('Developer'))}</h2><p>📍 {item.get('Location', '---')}</p></div>", unsafe_allow_html=True)

elif menu == "المساعد الذكي":
    st.title("🤖 المساعد العقاري 2026")
    st.info("قم بإدخال متطلبات العميل للوصول لأفضل الخيارات")

elif menu == "المشاريع":
    st.title("📂 دليل المشاريع")
    # هنا يوضع كود الشبكة (Grid) للمشاريع

elif menu == "المطورين":
    st.title("🏗️ قائمة المطورين العقاريين")

elif menu == "أدوات البروكر":
    st.title("🛠️ الأدوات الحسابية")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='smart-box'><h3>💳 حاسبة الأقساط</h3>", unsafe_allow_html=True)
        # كود حاسبة الأقساط
        st.markdown("</div>", unsafe_allow_html=True)

# زر الخروج
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout / خروج"):
    st.session_state.auth = False
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
