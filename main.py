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

# 2. رابط الـ Apps Script الخاص بك
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# 3. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- وظائف الربط مع جوجل شيت ---
def signup_user(name, pwd, email, wa, comp):
    # تحويل البيانات إلى تنسيق JSON للإرسال
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload, timeout=10)
        # إذا كان السكريبت يرجع كلمة Success فالتسجيل نجح
        return "Success" in response.text 
    except: return False

def login_user(user_input, pwd_input):
    try:
        # إضافة nocache لضمان جلب أحدث المشتركين
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=10)
        if response.status_code == 200:
            users_list = response.json()
            for user_data in users_list:
                name_s = str(user_data.get('Name', user_data.get('name', ''))).strip()
                pass_s = str(user_data.get('Password', user_data.get('password', ''))).strip()
                email_s = str(user_data.get('Email', user_data.get('email', ''))).strip()
                
                # المقارنة
                if (user_input.strip().lower() == name_s.lower() or user_input.strip().lower() == email_s.lower()) and str(pwd_input).strip() == pass_s:
                    return name_s
        return None
    except: return None

# 4. جلب الأخبار (تم الاختصار للأداء)
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        feed = feedparser.parse("https://www.youm7.com/rss/SectionRss?SectionID=297")
        return "  •  ".join([item.title for item in feed.entries[:10]])
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى في مصر لعام 2026."

news_text = get_real_news()

# 5. التنسيق الجمالي CSS (نفس كودك الأصلي)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    .ticker-wrap {{ width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 20px; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    div.stButton > button {{ border-radius: 12px !important; width: 100%; font-weight: bold; }}
    .smart-box {{ background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; }}
    </style>
""", unsafe_allow_html=True)

# 6. شاشة الدخول والاشتراك
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:30px;'><h1 style='color:#f59e0b; font-size:50px;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["🔐 تسجيل دخول", "📝 اشتراك جديد"])
    
    with tab_login:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            u_input = st.text_input("الأسم أو الجيميل", key="log_user")
            p_input = st.text_input("كلمة السر", type="password", key="log_pass")
            if st.button("دخول للمنصة 🚀"):
                if p_input == "2026":
                    st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
                else:
                    user_verified = login_user(u_input, p_input)
                    if user_verified:
                        st.session_state.auth = True; st.session_state.current_user = user_verified; st.rerun()
                    else: st.error("بيانات الدخول غير صحيحة")

    with tab_signup:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            r_n = st.text_input("الأسم بالكامل", key="reg_n")
            r_p = st.text_input("كلمة السر المرجوة", type="password", key="reg_p")
            r_e = st.text_input("الجيميل", key="reg_e")
            r_w = st.text_input("رقم الواتساب", key="reg_w")
            r_c = st.text_input("الشركة", key="reg_c")
            if st.button("تأكيد الاشتراك ✅"):
                if r_n and r_p and r_e:
                    with st.spinner("جاري تسجيل بياناتك..."):
                        if signup_user(r_n, r_p, r_e, r_w, r_c):
                            st.success("تم تسجيلك بنجاح! انتقل الآن لتبويب (تسجيل دخول).")
                            st.balloons()
                        else: st.error("حدث خطأ في الاتصال، تأكد من إعدادات الـ Apps Script")
                else: st.warning("يرجى ملء الخانات الأساسية (الاسم، الباسورد، الإيميل)")
    st.stop()

# --- باقي كود التطبيق (المشاريع، الأدوات، إلخ) يوضع هنا كما هو في ملفك الأصلي ---
st.write(f"أهلاً بك {st.session_state.current_user}")
# ... بقية الكود الخاص بك ...
