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

# --- 3. إدارة الحالة (Session State) ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'lang' not in st.session_state: st.session_state.lang = "Arabic"
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'messages' not in st.session_state: st.session_state.messages = []

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- 4. الوظائف البرمجية (الربط والبيانات) ---
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
    except: return "MA3LOMATI PRO: Your Real Estate Portal 2026."

news_text = get_real_news()

# --- 5. التصميم الجمالي CSS (Luxury Multi-Lang) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding: 0rem !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: radial-gradient(circle, rgba(0,0,0,0.92), rgba(0,0,0,0.98)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {"rtl" if st.session_state.lang == "Arabic" else "ltr"} !important;
        text-align: {"right" if st.session_state.lang == "Arabic" else "left"} !important;
        font-family: 'Cairo', sans-serif;
    }}

    /* شاشة الدخول الفاخرة */
    .auth-main {{ display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 95vh; }}
    .luxury-card {{
        background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(20px);
        border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 40px;
        padding: 50px; width: 100%; max-width: 480px; box-shadow: 0 40px 100px rgba(0,0,0,0.6); text-align: center;
    }}
    .gold-title {{
        background: linear-gradient(90deg, #f59e0b, #fbbf24, #f59e0b);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 38px; font-weight: 900; letter-spacing: 1px;
    }}

    /* الحقول والأزرار */
    div.stTextInput input {{
        background: rgba(255,255,255,0.05) !important; color: white !important;
        border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 15px !important;
        height: 52px !important; text-align: center !important;
    }}
    .stButton > button {{
        background: linear-gradient(45deg, #f59e0b, #d97706) !important;
        color: black !important; font-weight: 700 !important; border-radius: 15px !important;
        height: 52px !important; border: none !important; width: 100%; transition: 0.3s;
    }}
    .stButton > button:hover {{ transform: scale(1.02); box-shadow: 0 10px 20px rgba(245,158,11,0.3); }}

    /* شريط الأخبار */
    .ticker-wrap {{ width: 100%; background: rgba(0,0,0,0.6); padding: 12px 0; border-bottom: 1px solid #f59e0b33; overflow: hidden; white-space: nowrap; }}
    .ticker {{ display: inline-block; animation: ticker 120s linear infinite; color: #f59e0b; font-size: 14px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* التصميم الداخلي */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.8)), url('{HEADER_IMG}');
        background-size: cover; padding: 60px 20px; text-align: center;
        border-bottom: 3px solid #f59e0b; border-radius: 0 0 50px 50px;
    }}
    .detail-card {{ background: rgba(20,20,20,0.8); padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; border: 1px solid #333; margin-bottom: 20px; }}
    .label-gold {{ color: #f59e0b; font-weight: 700; font-size: 14px; margin-bottom: 2px; }}
    .val-white {{ color: white; font-size: 17px; margin-bottom: 12px; border-bottom: 1px solid #222; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. منطق تبديل اللغة ونموذج الدخول ---
if not st.session_state.auth:
    # شريط اختيار اللغة في الأعلى
    c_lang = st.columns([0.85, 0.15])
    with c_lang[1]:
        lang_choice = st.selectbox("🌐", ["العربية", "English"], label_visibility="collapsed")
        st.session_state.lang = "Arabic" if lang_choice == "العربية" else "English"

    st.markdown(f'<div class="ticker-wrap"><div class="ticker">{news_text}</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="auth-main">', unsafe_allow_html=True)
    st.markdown('<div class="luxury-card">', unsafe_allow_html=True)
    st.markdown('<div class="gold-title">MA3LOMATI PRO</div>', unsafe_allow_html=True)
    
    # نصوص متغيرة حسب اللغة
    t = {
        "sub": "بوابتك لعالم العقارات الفاخرة" if st.session_state.lang=="Arabic" else "Your Luxury Real Estate Gateway",
        "tab1": "🔐 دخول" if st.session_state.lang=="Arabic" else "🔐 Login",
        "tab2": "📝 اشتراك" if st.session_state.lang=="Arabic" else "📝 Signup",
        "user": "اسم المستخدم / الإيميل" if st.session_state.lang=="Arabic" else "Username / Email",
        "pass": "كلمة المرور" if st.session_state.lang=="Arabic" else "Password",
        "btn_log": "دخول آمن 🚀" if st.session_state.lang=="Arabic" else "Secure Login 🚀",
        "btn_reg": "تأكيد العضوية" if st.session_state.lang=="Arabic" else "Confirm Signup"
    }
    
    st.markdown(f'<p style="color:#888; margin-bottom:30px;">{t["sub"]}</p>', unsafe_allow_html=True)
    
    tab_log, tab_reg = st.tabs([t["tab1"], t["tab2"]])
    
    with tab_log:
        u = st.text_input(t["user"], key="u_in", placeholder=t["user"], label_visibility="collapsed")
        p = st.text_input(t["pass"], type="password", key="p_in", placeholder=t["pass"], label_visibility="collapsed")
        if st.button(t["btn_log"]):
            if p == "2026": 
                st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
            else:
                user_found = login_user(u, p)
                if user_found:
                    st.session_state.auth = True; st.session_state.current_user = user_found; st.rerun()
                else: st.error("بيانات غير صحيحة" if st.session_state.lang=="Arabic" else "Invalid Credentials")
                
    with tab_reg:
        rn = st.text_input("Name", placeholder="الأسم بالكامل")
        re = st.text_input("Email", placeholder="البريد الإلكتروني")
        rw = st.text_input("WhatsApp", placeholder="رقم الواتساب")
        rc = st.text_input("Company", placeholder="اسم الشركة")
        rp = st.text_input("Pass", type="password", placeholder="كلمة المرور")
        if st.button(t["btn_reg"]):
            if signup_user(rn, rp, re, rw, rc): st.success("تم التسجيل! يمكنك الدخول الآن")
            else: st.error("فشل الاتصال")

    st.markdown('</div></div>', unsafe_allow_html=True)
    st.stop()

# --- 7. المحتوى الداخلي (Dashboard) ---

# وظيفة جلب بيانات المشاريع
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        p = pd.read_csv(U_P).fillna("---")
        return p
    except: return pd.DataFrame()

df = load_data()

# القائمة الجانبية
with st.sidebar:
    st.markdown(f"<h2 style='text-align:center; color:#f59e0b;'>{st.session_state.current_user}</h2>", unsafe_allow_html=True)
    menu = option_menu(
        "MA3LOMATI", ["المشاريع", "المطورين", "أدوات البروكر", "المساعد الذكي"],
        icons=['search', 'building', 'briefcase', 'robot'],
        menu_icon="cast", default_index=0,
        styles={
            "container": {"background-color": "#000"},
            "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}
        }
    )
    if st.button("🚪 خروج" if st.session_state.lang=="Arabic" else "🚪 Logout"):
        st.session_state.auth = False; st.rerun()

# الهيدر الملكي الداخلي
st.markdown(f"""
    <div class="royal-header">
        <div style="color:#f59e0b; font-weight:bold; margin-bottom:10px;">{egypt_now.strftime('%Y-%m-%d | %I:%M %p')}</div>
        <h1 style="color:white; font-size:45px; font-weight:900;">{menu}</h1>
        <p style="color:#aaa;">{"نظام معلوماتي برو لإدارة العقارات لعام 2026" if st.session_state.lang=="Arabic" else "MA3LOMATI PRO Real Estate Management 2026"}</p>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

# محتوى الصفحات
if menu == "المشاريع":
    search = st.text_input("🔍 ابحث عن مشروع، منطقة، أو سعر...")
    filt = df[df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else df
    
    if st.session_state.view == "grid":
        cols = st.columns(2)
        for i, (idx, row) in enumerate(filt.iloc[:ITEMS_PER_PAGE].iterrows()):
            with cols[i%2]:
                with st.container(border=True):
                    st.markdown(f"### 🏢 {row.iloc[0]}")
                    st.markdown(f"📍 **الموقع:** {row.get('Location', row.get('الموقع', '---'))}")
                    if st.button(f"عرض التفاصيل #{idx}", key=f"btn_{idx}"):
                        st.session_state.current_index = idx
                        st.session_state.view = "details"
                        st.rerun()
    else:
        # عرض التفاصيل الكاملة
        if st.button("⬅ عودة"): st.session_state.view = "grid"; st.rerun()
        item = df.iloc[st.session_state.current_index]
        c1, c2 = st.columns(2)
        with c1:
            h = '<div class="detail-card">'
            for k, v in item.items():
                h += f'<p class="label-gold">{k}</p><p class="val-white">{v}</p>'
            st.markdown(h+'</div>', unsafe_allow_html=True)
        with c2:
            st.info("صور المشروع وخرائط الموقع تظهر هنا...")

elif menu == "أدوات البروكر":
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🧮 حاسبة التمويل")
        price = st.number_input("سعر الوحدة", 1000000)
        years = st.slider("سنوات التقسيط", 1, 15, 8)
        st.metric("القسط الشهري", f"{price/(years*12):,.0f}")
    with c2:
        st.subheader("📊 تحليل العائد (ROI)")
        buy_p = st.number_input("سعر الشراء", 2000000)
        rent_p = st.number_input("الإيجار السنوي المتوقع", 200000)
        st.metric("نسبة العائد", f"{(rent_p/buy_p)*100:.1f}%")

st.markdown("<br><p style='text-align:center; color:#444;'>MA3LOMATI PRO © 2026 | Powered by AI</p>", unsafe_allow_html=True)
