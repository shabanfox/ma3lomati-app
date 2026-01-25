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

# --- 3. إدارة الحالة (Session State) ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'page' not in st.session_state: st.session_state.page = "الرئيسية"

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
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى لعام 2026."

news_text = get_real_news()

# --- 5. التصميم الجمالي CSS (نسخة VIP الشاملة) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding: 0rem !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}

    /* شاشة الدخول */
    .login-wrapper {{ display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }}
    .glass-card {{
        background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px);
        border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 35px;
        padding: 45px; width: 100%; max-width: 450px; text-align: center;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }}
    .brand-title {{ font-size: 35px; font-weight: 900; background: linear-gradient(90deg, #f59e0b, #fbbf24); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    
    /* الحقول والأزرار */
    div.stTextInput input {{ background-color: rgba(255,255,255,0.05) !important; color: white !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px !important; height: 50px !important; text-align: center !important; }}
    .stButton > button {{ width: 100% !important; background: linear-gradient(45deg, #f59e0b, #d97706) !important; color: black !important; font-weight: 700 !important; border-radius: 12px !important; border: none !important; height: 50px !important; }}
    
    /* شريط الأخبار */
    .ticker-wrap {{ width: 100%; background: rgba(245, 158, 11, 0.1); padding: 10px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid rgba(245, 158, 11, 0.3); }}
    .ticker {{ display: inline-block; animation: ticker 120s linear infinite; color: #f59e0b; font-size: 14px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* هيدر الصفحة الداخلية */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 3px solid #f59e0b;
        padding: 50px 20px; text-align: center; border-radius: 0 0 50px 50px; margin-bottom: 30px;
    }}
    
    /* الكروت الداخلية */
    .card {{ background: rgba(255,255,255,0.02); padding: 25px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05); transition: 0.3s; }}
    .card:hover {{ border-color: #f59e0b; background: rgba(255,255,255,0.05); }}
    .gold-text {{ color: #f59e0b; font-weight: 700; }}
    </style>
    """, unsafe_allow_html=True)

# --- 6. منطق العرض (تسجيل الدخول أو المحتوى) ---

if not st.session_state.auth:
    # --- صفحة تسجيل الدخول الفاخرة ---
    st.markdown(f'<div class="ticker-wrap"><div class="ticker">{news_text}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="glass-card"><div class="brand-title">MA3LOMATI PRO</div><p style="color:#888;">النظام العقاري الاحترافي 2026</p>', unsafe_allow_html=True)
        tab_log, tab_reg = st.tabs(["🔑 تسجيل دخول", "📝 عضوية جديدة"])
        
        with tab_log:
            u = st.text_input("اسم المستخدم", placeholder="User or Email", key="log_u")
            p = st.text_input("كلمة المرور", type="password", placeholder="••••••••", key="log_p")
            if st.button("دخول للنظام"):
                name = login_user(u, p)
                if name:
                    st.session_state.auth = True
                    st.session_state.current_user = name
                    st.rerun()
                else: st.error("بيانات غير صحيحة")
        
        with tab_reg:
            rn = st.text_input("الاسم بالكامل")
            re = st.text_input("الإيميل")
            rw = st.text_input("واتساب")
            rc = st.text_input("الشركة")
            rp = st.text_input("كلمة المرور", type="password", key="reg_p")
            if st.button("إنشاء حساب"):
                if signup_user(rn, rp, re, rw, rc): st.success("تم بنجاح! سجل دخولك")
                else: st.error("حدث خطأ")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- الصفحة الداخلية (بعد الدخول) ---
    
    # 1. القائمة الجانبية (Sidebar Menu)
    with st.sidebar:
        st.markdown(f"<h2 style='text-align:center; color:#f59e0b;'>{st.session_state.current_user}</h2>", unsafe_allow_html=True)
        selected = option_menu(
            "القائمة الرئيسية", ["الرئيسية", "قاعدة البيانات", "إضافة عقار", "الإحصائيات", "الإعدادات"],
            icons=['house', 'database', 'plus-circle', 'graph-up', 'gear'],
            menu_icon="cast", default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#000"},
                "icon": {"color": "#f59e0b", "font-size": "20px"}, 
                "nav-link": {"font-size": "16px", "text-align": "right", "margin":"5px", "--hover-color": "#222"},
                "nav-link-selected": {"background-color": "#f59e0b", "color": "black"},
            }
        )
        if st.button("تسجيل الخروج"):
            st.session_state.auth = False
            st.rerun()

    # 2. الهيدر الملكي
    st.markdown(f"""
        <div class="royal-header">
            <div style="font-size:14px; color:#f59e0b; margin-bottom:10px;">{egypt_now.strftime('%Y-%m-%d | %I:%M %p')}</div>
            <h1 style="color:white; font-weight:900;">{selected}</h1>
            <p style="color:#ccc;">نظام إدارة المعلومات العقارية الذكي</p>
        </div>
    """, unsafe_allow_html=True)

    # 3. محتوى الصفحات
    if selected == "الرئيسية":
        st.markdown(f'<div class="ticker-wrap"><div class="ticker">{news_text}</div></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="card"><h3 class="gold-text">🏢 الوحدات المتاحة</h3><h2>1,245</h2><p>تحديث اليوم</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="card"><h3 class="gold-text">💰 إجمالي الاستثمارات</h3><h2>540M</h2><p>جنيه مصري</p></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="card"><h3 class="gold-text">🤝 صفقات ناجحة</h3><h2>89</h2><p>هذا الشهر</p></div>', unsafe_allow_html=True)
            
        st.write("---")
        st.subheader("📍 آخر التحديثات العقارية")
        # مثال لجدول بيانات
        data = pd.DataFrame({
            "المشروع": ["العاصمة الإدارية", "نور سيتي", "بادية", "الجونة"],
            "الحالة": ["متاح", "مباع بالكامل", "تحت الإنشاء", "متاح"],
            "السعر المتوسط": ["4.5M", "3.2M", "6.1M", "12.5M"]
        })
        st.table(data)

    elif selected == "قاعدة البيانات":
        st.subheader("🔍 البحث المتقدم في الوحدات")
        search = st.text_input("ابحث باسم المنطقة أو العميل...")
        st.info("سيتم عرض نتائج البحث من جوجل شيت هنا...")

    elif selected == "الإحصائيات":
        st.markdown('<div class="card">تحليل السوق العقاري لعام 2026 سيظهر هنا قريباً</div>', unsafe_allow_html=True)

    # تذييل الصفحة
    st.markdown("<br><p style='text-align:center; color:#555;'>MA3LOMATI PRO © 2026 - All Rights Reserved</p>", unsafe_allow_html=True)
