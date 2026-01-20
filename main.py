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

# 2. روابط الهوية البصرية (الصور الجذابة)
LOGO_URL = "https://images.unsplash.com/photo-1560518883-ce09059eeffa?q=80&w=1000&auto=format&fit=crop"
HEADER_BG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=2000&auto=format&fit=crop"

# 3. الرابط الخاص بك لربط الجوجل شيت (الـ Apps Script) - ثابت كما هو في كودك
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# 4. إدارة الحالة والتوقيت المصري
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- وظائف الربط مع جوجل شيت (الخلفية) - تم إعادتها بالكامل ---
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

# جلب الأخبار العقارية
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى في مصر لعام 2026."

news_text = get_real_news()

# 5. التنسيق الجمالي (CSS) - النسخة الذهبية الفاخرة 2026
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #0a0a0a; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    .custom-header {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('{HEADER_BG}');
        background-size: cover; background-position: center; height: 200px;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        border-bottom: 4px solid #D4AF37; border-radius: 0 0 30px 30px;
    }}

    .ticker-wrap {{ width: 100%; background: #111; padding: 10px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #333; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #D4AF37; font-size: 14px; font-weight: bold; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    div.stButton > button[key*="card_"] {{
        background: linear-gradient(145deg, #1a1a1a, #111) !important;
        color: #D4AF37 !important; border: 1px solid #333 !important;
        border-right: 6px solid #D4AF37 !important; border-radius: 15px !important;
        min-height: 120px !important; transition: 0.4s !important; width: 100% !important;
        font-weight: bold !important; font-size: 15px !important;
    }}
    div.stButton > button[key*="card_"]:hover {{ transform: translateY(-5px) !important; border-right: 10px solid #fff !important; box-shadow: 0 10px 20px rgba(212,175,55,0.2) !important; color: white !important; }}
    
    .smart-box {{ background: rgba(26,26,26,0.95); border: 1px solid #D4AF37; padding: 25px; border-radius: 20px; color: white; }}
    .side-card {{ background: #161616; padding: 15px; border-radius: 12px; border-right: 3px solid #D4AF37; margin-bottom: 10px; }}
    .tool-card {{ background: #1a1a1a; padding: 20px; border-radius: 15px; border-top: 4px solid #D4AF37; text-align: center; }}
    
    /* تعديل المدخلات */
    .stTextInput input, .stSelectbox select {{ background-color: #1a1a1a !important; color: white !important; border: 1px solid #333 !important; }}
    label {{ color: #D4AF37 !important; font-weight: bold !important; }}
    </style>
""", unsafe_allow_html=True)

# 6. شاشة الدخول والاشتراك (الربط الحي)
if not st.session_state.auth:
    st.markdown(f"""<div style='text-align:center; padding-top:40px;'>
        <img src='{LOGO_URL}' style='width:120px; border-radius:50%; border:3px solid #D4AF37;'>
        <h1 style='color:#D4AF37; font-size:50px; margin-bottom:0;'>MA3LOMATI PRO</h1>
        <p style='color:white; font-size:18px;'>المنصة العقارية الأكثر تطوراً في مصر 2026</p>
    </div>""", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["🔐 تسجيل دخول", "📝 اشتراك جديد"])
    
    with tab_login:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            u_input = st.text_input("الأسم أو الجيميل", key="log_user")
            p_input = st.text_input("كلمة السر", type="password", key="log_pass")
            if st.button("دخول للمنصة 🚀"):
                if p_input == "2026": # الكود المباشر
                    st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
                else:
                    user_verified = login_user(u_input, p_input)
                    if user_verified:
                        st.session_state.auth = True; st.session_state.current_user = user_verified; st.rerun()
                    else: st.error("بيانات الدخول غير صحيحة")

    with tab_signup:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            reg_name = st.text_input("الأسم بالكامل")
            reg_pass = st.text_input("كلمة السر المرجوة", type="password")
            reg_email = st.text_input("الجيميل")
            reg_wa = st.text_input("رقم الواتساب")
            reg_co = st.text_input("الشركة")
            if st.button("تأكيد الاشتراك ✅"):
                if reg_name and reg_pass and reg_email:
                    if signup_user(reg_name, reg_pass, reg_email, reg_wa, reg_co):
                        st.success("تم تسجيلك بنجاح! اذهب الآن لتبويب تسجيل الدخول.")
                    else: st.error("حدث خطأ في الاتصال بالسيرفر")
                else: st.warning("يرجى ملء كافة البيانات")
    st.stop()

# 7. جلب البيانات من الجوجل شيت (كما في كودك)
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

# 8. الهيدر البصري بعد الدخول
st.markdown(f"""
    <div class="custom-header">
        <h1 style="color: white; margin: 0; font-size: 40px; text-shadow: 2px 2px 10px rgba(0,0,0,0.5);">MA3LOMATI PRO</h1>
        <p style="color: #D4AF37; font-weight: bold; font-size: 18px;">أهلاً بك يا {st.session_state.current_user}</p>
    </div>
""", unsafe_allow_html=True)

# 9. شريط المعلومات العلوي
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)
c_top1, c_top2 = st.columns([0.8, 0.2])
with c_top2:
    if st.button("🚪 خروج", key="logout"): st.session_state.auth = False; st.rerun()

# 10. المنيو الرئيسي الفاخر
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], default_index=0, orientation="horizontal",
    styles={
        "container": {"background-color": "#111", "border": "1px solid #333"},
        "nav-link-selected": {"background-color": "#D4AF37", "color": "black", "font-weight": "bold"}
    })

# --- منطق الصفحات (المشاريع، المطورين، المساعد) يستمر من هنا كما هو في كودك ---
# مع التأكد من استخدام زرار الكروت بنفس الـ Key "card_" ليأخذ التصميم الذهبي.

if menu == "المشاريع":
    st.title("🏗️ استكشاف المشاريع")
    # ... ضع كود عرض المشاريع الخاص بك هنا ...
    st.write("البيانات جاهزة للعرض...")

st.markdown(f"<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026 | {egypt_now.year}</p>", unsafe_allow_html=True)
