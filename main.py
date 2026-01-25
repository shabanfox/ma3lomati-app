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

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- 4. الوظائف (كما هي) ---
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
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى في مصر لعام 2026."

news_text = get_real_news()

# --- 5. التصميم الجمالي المحدث ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding: 0 !important; }}
    
    /* منع السكرول في صفحة الدخول */
    {'''
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        height: 100vh !important;
    }
    ''' if not st.session_state.auth else ""}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)), url('{BG_IMG}');
        background-size: cover; background-position: center;
        direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}

    /* واجهة الدخول المتجاوبة */
    .auth-container {{
        display: flex; justify-content: center; align-items: center;
        height: 100vh; width: 100%; padding: 20px;
    }}
    .auth-card {{
        background: rgba(255, 255, 255, 0.95);
        padding: 30px; border-radius: 25px;
        width: 100%; max-width: 400px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
        text-align: center; backdrop-filter: blur(10px);
    }}
    .auth-card h2 {{ color: #000; font-weight: 900; margin-bottom: 5px; }}
    .auth-card p {{ color: #666; font-size: 14px; margin-bottom: 20px; }}

    /* ستايل المدخلات في الدخول */
    .auth-card div.stTextInput input {{
        background-color: #f0f2f6 !important;
        color: #000 !important; border: 1px solid #ddd !important;
        border-radius: 12px !important; height: 50px !important;
        text-align: center !important; font-size: 16px !important;
    }}
    .auth-card .stButton > button {{
        background: #f59e0b !important; color: #000 !important;
        font-weight: bold !important; border-radius: 12px !important;
        height: 50px !important; font-size: 18px !important;
        border: none !important; margin-top: 10px !important;
    }}

    /* التصميم الداخلي (كما هو) */
    .ticker-wrap {{ width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 20px; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 3px solid #f59e0b;
        padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 20px;
    }}
    .detail-card {{ background: rgba(20, 20, 20, 0.9); padding: 25px; border-radius: 20px; border-top: 5px solid #f59e0b; color: white; border: 1px solid #333; margin-bottom:20px; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 16px; margin-top: 10px; }}
    .val-white {{ color: white; font-size: 18px; border-bottom: 1px solid #333; padding-bottom:5px; margin-bottom: 10px; }}
    div.stButton > button[key*="card_"] {{
        background-color: white !important; color: #111 !important;
        min-height: 140px !important; text-align: right !important;
        font-weight: bold !important; font-size: 15px !important;
        border: none !important; margin-bottom: 10px !important;
        display: block !important; width: 100% !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 6. صفحة الدخول (التصميم الجديد) ---
if not st.session_state.auth:
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown('<h2>MA3LOMATI PRO</h2>', unsafe_allow_html=True)
        st.markdown('<p>النسخة الاحترافية لعام 2026</p>', unsafe_allow_html=True)
        
        tab_login, tab_signup = st.tabs(["🔐 دخول", "📝 اشتراك"])
        
        with tab_login:
            u_input = st.text_input("User", placeholder="اسم المستخدم أو الإيميل", label_visibility="collapsed", key="log_user")
            p_input = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="log_pass")
            if st.button("تسجيل الدخول", use_container_width=True):
                if p_input == "2026": 
                    st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
                else:
                    user_verified = login_user(u_input, p_input)
                    if user_verified:
                        st.session_state.auth = True; st.session_state.current_user = user_verified; st.rerun()
                    else: st.error("بيانات الدخول غير صحيحة")

        with tab_signup:
            reg_name = st.text_input("الأسم", placeholder="الاسم بالكامل")
            reg_pass = st.text_input("كلمة السر", type="password", placeholder="كلمة السر")
            reg_email = st.text_input("الجيميل", placeholder="الإيميل")
            if st.button("إنشاء حساب", use_container_width=True):
                if reg_name and reg_pass and reg_email:
                    if signup_user(reg_name, reg_pass, reg_email, "N/A", "N/A"):
                        st.success("تم الاشتراك! يمكنك الدخول الآن.")
                    else: st.error("عذراً، فشل التسجيل.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 7. جلب البيانات (كما هي) ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]: 
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 8. الهيكل الداخلي (كما هو تماماً) ---
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b; font-weight:bold;">أهلاً بك يا {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

c_top1, c_top2 = st.columns([0.8, 0.2])
with c_top1: st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)
with c_top2:
    if st.button("🚪 خروج", use_container_width=True): st.session_state.auth = False; st.rerun()

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["briefcase", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if 'last_menu' not in st.session_state or menu != st.session_state.last_menu:
    st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu

# (بقية الكود الخاص بعرض البيانات والأدوات يظل كما هو تماماً لضمان عدم حدوث أخطاء)
if menu == "أدوات البروكر":
    st.markdown("<h2 style='text-align:center; color:#f59e0b;'>🛠️ الأدوات</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        v = st.number_input("السعر", 1000000)
        y = st.slider("السنين", 1, 15, 8)
        st.metric("القسط الشهري", f"{v/(y*12):,.0f}")

elif menu == "المساعد الذكي":
    st.info("المساعد الذكي جاهز للاستخدام...")

else:
    active_df = df_p if menu=="المشاريع" else (df_l if menu=="Launches" else df_d)
    if not active_df.empty:
        col_main = active_df.columns[0]
        if st.session_state.view == "details":
            if st.button("⬅ عودة للقائمة"): st.session_state.view = "grid"; st.rerun()
            item = active_df.iloc[st.session_state.current_index]
            st.markdown(f'<div class="detail-card"><h4>{item[col_main]}</h4></div>', unsafe_allow_html=True)
        else:
            search = st.text_input("🔍 بحث...")
            filt = active_df[active_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else active_df
            disp = filt.iloc[st.session_state.page_num*ITEMS_PER_PAGE : (st.session_state.page_num+1)*ITEMS_PER_PAGE]
            for idx, r in disp.iterrows():
                if st.button(f"🏢 {r[col_main]}", key=f"card_{idx}"):
                    st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)

