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

# 2. الروابط (جوجل شيت)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"

# 3. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'selected_launch' not in st.session_state: st.session_state.selected_launch = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- وظائف الدخول والاشتراك ---
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

# 4. جلب الأخبار
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى في مصر لعام 2026."

news_text = get_real_news()

# 5. التنسيق الجمالي (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    .ticker-wrap {{ width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 20px; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    div.stButton > button {{ border-radius: 12px !important; transition: 0.3s !important; }}
    /* ستايل كروت اللونشات والمشاريع */
    div.stButton > button[key*="card_"], div.stButton > button[key*="lnch_"] {{
        background-color: #161616 !important; color: white !important;
        min-height: 140px !important; text-align: right !important;
        font-weight: bold !important; font-size: 15px !important;
        border: 1px solid #333 !important; border-top: 5px solid #f59e0b !important;
        display: block !important; width: 100% !important; white-space: pre-line !important;
    }}
    div.stButton > button:hover {{ transform: translateY(-5px) !important; border-color: #f59e0b !important; }}
    
    .smart-box {{ background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; }}
    .detail-card {{ background: #111; padding: 30px; border-radius: 20px; border-right: 8px solid #f59e0b; text-align: right; }}
    .label {{ color: #f59e0b; font-weight: bold; font-size: 14px; }}
    .value {{ color: #fff; font-size: 18px; margin-bottom: 15px; }}
    </style>
""", unsafe_allow_html=True)

# 6. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:50px;'><h1 style='color:#f59e0b; font-size:60px;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
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
                    if user_verified: st.session_state.auth = True; st.session_state.current_user = user_verified; st.rerun()
                    else: st.error("بيانات الدخول غير صحيحة")
    with tab_signup:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            reg_name = st.text_input("الأسم بالكامل")
            reg_pass = st.text_input("كلمة السر المرجوة", type="password")
            reg_email = st.text_input("الجيميل")
            if st.button("تأكيد الاشتراك ✅"):
                if reg_name and reg_pass and reg_email:
                    if signup_user(reg_name, reg_pass, reg_email, "---", "---"): st.success("تم تسجيلك بنجاح!")
                    else: st.error("خطأ في الاتصال")
    st.stop()

# 7. جلب البيانات
@st.cache_data(ttl=60)
def load_all_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        l = pd.read_csv(URL_LAUNCHES).fillna("---")
        for df in [p, d, l]: df.columns = df.columns.str.strip()
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d, l
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_all_data()

# 8. الهيدر
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 180px; background-size: cover; background-position: center; border-radius: 0 0 30px 30px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b;">
        <h1 style="color: white; margin: 0; font-size: 40px;">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b;">أهلاً بك يا {st.session_state.current_user}</p>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

# 9. المنيو
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], 
    icons=["briefcase", "building", "search", "robot", "rocket"], 
    default_index=4, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- 10. منطق الصفحات ---

# صفحة اللونشات (الجديدة)
if menu == "اللونشات":
    if st.session_state.selected_launch is not None:
        item = st.session_state.selected_launch
        if st.button("⬅️ عودة لقائمة اللونشات"): st.session_state.selected_launch = None; st.rerun()
        
        st.markdown(f"""<div class='detail-card'>
            <h1 style='color:#f59e0b;'>{item.get('Project', '---')}</h1>
            <p class='label'>🏢 المطور</p><p class='value'>{item.get('Developer', '---')}</p>
            <p class='label'>📍 الموقع</p><p class='value'>{item.get('Location', '---')}</p>
            <p class='label'>📏 المساحات والأنواع</p><p class='value'>{item.get('Units & Sizes', '---')}</p>
            <p class='label'>💰 السعر والسداد</p><p class='value'>{item.get('Price & Payment', '---')}</p>
            <hr style='border-color:#333;'>
            <p class='label'>🌟 مميزات المشروع (USP)</p><p style='line-height:1.6;'>{item.get('Unique Selling Points (USP)', '---')}</p>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align:center; color:white;'>🚀 أحدث لونشات 2026</h2>", unsafe_allow_html=True)
        if not df_l.empty:
            cols = st.columns(3)
            for index, row in df_l.iterrows():
                with cols[index % 3]:
                    lbl = f"🏢 {row.get('Developer', '---')}\n{row.get('Project', '---')}\n📍 {row.get('Location', '---')}"
                    if st.button(lbl, key=f"lnch_{index}"):
                        st.session_state.selected_launch = row; st.rerun()

# المساعد الذكي
elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 المساعد الذكي")
    # ... (نفس كود المساعد الذكي الخاص بك)
    st.markdown("</div>", unsafe_allow_html=True)

# المشاريع
elif menu == "المشاريع":
    if st.session_state.selected_item is not None:
        if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
        item = st.session_state.selected_item
        st.markdown(f"<div class='smart-box'><h2>{item.get('ProjectName')}</h2><p>الموقع: {item.get('Location')}</p></div>", unsafe_allow_html=True)
    else:
        # ... (نفس كود عرض المشاريع الخاص بك معPagination)
        st.write("استخدم البحث للوصول للمشاريع")

# المطورين وأدوات البروكر (تكملة الكود الخاص بك)
elif menu == "المطورين":
    st.write("قائمة المطورين")

elif menu == "أدوات البروكر":
    st.title("🛠️ حقيبة البروكر")
    # ... (نفس كود الحسابات الخاص بك)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
