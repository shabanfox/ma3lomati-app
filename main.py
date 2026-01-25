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
if 'lang' not in st.session_state: st.session_state.lang = "Arabic"
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'messages' not in st.session_state: st.session_state.messages = []

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- 4. وظائف الربط ---
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

# --- 5. التصميم الجمالي CSS (تعديل القمة للهاتف) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    /* منع التمرير في شاشة الدخول فقط */
    {"html, body, [data-testid='stAppViewContainer'] { overflow: hidden !important; height: 100vh !important; }" if not st.session_state.auth else ""}

    .block-container {{ padding: 0rem !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: #000000;
        background-image: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {"rtl" if st.session_state.lang == "Arabic" else "ltr"} !important;
        font-family: 'Cairo', sans-serif;
    }}

    /* تصميم كارت الدخول بالأعلى للهاتف */
    .auth-top-box {{
        display: flex; flex-direction: column; align-items: center;
        padding-top: 15px; width: 100%;
    }}
    .login-card {{
        background: #111111; border: 2px solid #f59e0b; border-radius: 20px;
        padding: 25px 20px; width: 92%; max-width: 420px;
        box-shadow: 0 0 25px rgba(245, 158, 11, 0.3); text-align: center;
    }}
    .gold-title {{ color: #f59e0b; font-size: 28px; font-weight: 900; margin-bottom: 10px; }}

    /* حقول بيضاء واضحة جداً للهاتف */
    div.stTextInput input {{
        background-color: #ffffff !important; color: #000000 !important;
        border: 2px solid #f59e0b !important; border-radius: 10px !important;
        height: 50px !important; font-size: 18px !important; font-weight: bold !important;
        text-align: center !important;
    }}
    .stButton > button {{
        background: #f59e0b !important; color: #000 !important; font-weight: 900 !important;
        height: 55px !important; border-radius: 10px !important; font-size: 20px !important;
        width: 100% !important; border: none !important;
    }}

    /* تنسيق المحتوى الداخلي */
    .ticker-wrap {{ width: 100%; background: rgba(245,158,11,0.1); padding: 8px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #f59e0b; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 3px solid #f59e0b;
        padding: 40px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 20px;
    }}
    .detail-card {{ background: rgba(20, 20, 20, 0.9); padding: 20px; border-radius: 20px; border-top: 5px solid #f59e0b; color: white; border: 1px solid #333; margin-bottom:15px; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 15px; }}
    .val-white {{ color: white; font-size: 17px; border-bottom: 1px solid #333; padding-bottom:3px; margin-bottom: 8px; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. صفحة الدخول (القمة للهاتف) ---
if not st.session_state.auth:
    # شريط اللغة في الأعلى
    c_l1, c_l2, c_l3 = st.columns([0.1, 0.7, 0.2])
    with c_l3:
        l_sel = st.selectbox("🌐", ["العربية", "English"], label_visibility="collapsed")
        st.session_state.lang = "Arabic" if l_sel == "العربية" else "English"

    st.markdown('<div class="auth-top-box">', unsafe_allow_html=True)
    with st.container():
        st.markdown(f'<div class="login-card"><div class="gold-title">MA3LOMATI PRO</div>', unsafe_allow_html=True)
        
        t_log, t_reg = st.tabs(["🔐 دخول" if st.session_state.lang=="Arabic" else "🔐 Login", 
                                "📝 اشتراك" if st.session_state.lang=="Arabic" else "📝 Sign"])
        
        with t_log:
            u_in = st.text_input("U", key="u_log", placeholder="المستخدم", label_visibility="collapsed")
            p_in = st.text_input("P", type="password", key="p_log", placeholder="كلمة المرور", label_visibility="collapsed")
            if st.button("SIGN IN 🚀"):
                if p_in == "2026":
                    st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
                else:
                    verified = login_user(u_in, p_in)
                    if verified:
                        st.session_state.auth = True; st.session_state.current_user = verified; st.rerun()
                    else: st.error("بيانات غير صحيحة")
        
        with t_reg:
            st.text_input("الأسم", placeholder="الاسم بالكامل")
            st.text_input("الإيميل", placeholder="الإيميل")
            st.button("إرسال طلب الانضمام")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 7. جلب البيانات (بعد الدخول) ---
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

# --- 8. الهيدر الداخلي ---
st.markdown(f'<div class="royal-header"><h1 style="color:white; margin:0; font-size:35px;">MA3LOMATI PRO</h1><p style="color:#f59e0b;">مرحباً {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

c_nav1, c_nav2 = st.columns([0.8, 0.2])
with c_nav1:
    st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)
with c_nav2:
    if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()

# --- 9. القائمة الرئيسية ---
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["briefcase", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

if 'last_menu' not in st.session_state or menu != st.session_state.last_menu:
    st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu

# --- 10. محتوى الصفحات ---
if menu == "أدوات البروكر":
    st.markdown("<h2 style='text-align:center; color:#f59e0b;'>🛠️ الأدوات</h2>", unsafe_allow_html=True)
    v = st.number_input("إجمالي السعر", 1000000)
    y = st.slider("عدد السنين", 1, 15, 8)
    st.metric("القسط الشهري", f"{v/(y*12):,.0f}")

elif menu == "المساعد الذكي":
    st.markdown("<div class='detail-card'><h3>🤖 المساعد الذكي</h3></div>", unsafe_allow_html=True)
    if pmt := st.chat_input("اسألني عن أي شيء..."):
        st.session_state.messages.append({"role": "user", "content": pmt})
        st.rerun()

else:
    active_df = df_p if menu=="المشاريع" else (df_l if menu=="Launches" else df_d)
    if active_df.empty: st.error("لا توجد بيانات")
    else:
        col_main = active_df.columns[0]
        if st.session_state.view == "details":
            item = active_df.iloc[st.session_state.current_index]
            if st.button("⬅ عودة"): st.session_state.view = "grid"; st.rerun()
            h = '<div class="detail-card">'
            for k, v in item.items(): h += f'<p class="label-gold">{k}</p><p class="val-white">{v}</p>'
            st.markdown(h+'</div>', unsafe_allow_html=True)
        else:
            search = st.text_input("🔍 بحث...")
            filt = active_df[active_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else active_df
            disp = filt.iloc[st.session_state.page_num*ITEMS_PER_PAGE : (st.session_state.page_num+1)*ITEMS_PER_PAGE]
            for idx, r in disp.iterrows():
                if st.button(f"🏢 {r[col_main]} | {r.get('Location', '')}", key=f"card_{idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()
