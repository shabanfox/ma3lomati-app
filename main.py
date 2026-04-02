import streamlit as st
import pandas as pd
import requests
import feedparser
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الروابط الأساسية (تأكد من صحتها) ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 3. إدارة الحالة (Session State) ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'messages' not in st.session_state: st.session_state.messages = []
if 'lang' not in st.session_state: st.session_state.lang = "EN"

# --- 4. وظائف الربط مع الشيت ---
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
                u_n = str(user_data.get('Name', user_data.get('name', ''))).strip()
                u_e = str(user_data.get('Email', user_data.get('email', ''))).strip()
                u_p = str(user_data.get('Password', user_data.get('password', ''))).strip()
                if (user_input == u_n.lower() or user_input == u_e.lower()) and pwd_input == u_p:
                    return u_n
        return None
    except: return None

# --- 5. التصميم الجمالي CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Inter:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        font-family: 'Inter', 'Cairo', sans-serif;
    }}
    .auth-card {{
        background: white; width: 400px; padding: 40px; border-radius: 25px;
        text-align: center; margin: auto; box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; padding: 40px; text-align: center; border-bottom: 3px solid #f59e0b; border-radius: 0 0 40px 40px;
    }}
    .detail-card {{ background: rgba(30, 30, 30, 0.9); padding: 20px; border-radius: 15px; border: 1px solid #444; color: white; margin-bottom: 10px; }}
    .label-gold {{ color: #f59e0b; font-weight: bold; }}
    div.stButton > button {{ border-radius: 12px !important; transition: 0.3s; }}
    div.stButton > button[key*="card_"] {{ background: white !important; color: black !important; min-height: 100px; text-align: right; width: 100%; border: none; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. صفحة الدخول (باللغتين) ---
if not st.session_state.auth:
    col_l, col_r = st.columns([0.8, 0.2])
    with col_r:
        st.session_state.lang = st.selectbox("🌐 Language", ["EN", "AR"])

    st.markdown("<br><br><div class='auth-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:black; margin-bottom:20px;'>MA3LOMATI PRO</h2>", unsafe_allow_html=True)
    
    if st.session_state.lang == "EN":
        t1, t2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        with t1:
            u = st.text_input("User/Email", key="en_u")
            p = st.text_input("Password", type="password", key="en_p")
            if st.button("SIGN IN 🚀", use_container_width=True):
                if p == "2026": st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
                else:
                    res = login_user(u, p)
                    if res: st.session_state.auth = True; st.session_state.current_user = res; st.rerun()
                    else: st.error("Wrong credentials")
        with t2:
            n = st.text_input("Name"); e = st.text_input("Email"); pw = st.text_input("Pass", type="password")
            if st.button("REGISTER ✅", use_container_width=True):
                if signup_user(n, pw, e, "---", "---"): st.success("Done! Please Login.")
    else:
        st.markdown("<div style='direction: rtl;'>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🔐 دخول", "📝 اشتراك"])
        with t1:
            u = st.text_input("الاسم أو الإيميل", key="ar_u")
            p = st.text_input("كلمة السر", type="password", key="ar_p")
            if st.button("دخول 🚀", use_container_width=True):
                if p == "2026": st.session_state.auth = True; st.session_state.current_user = "المشرف"; st.rerun()
                else:
                    res = login_user(u, p)
                    if res: st.session_state.auth = True; st.session_state.current_user = res; st.rerun()
                    else: st.error("بيانات خطأ")
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 7. جلب البيانات (مع معالجة الأخطاء الآمنة) ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]: 
            df.columns = [c.strip() for c in df.columns]
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 8. الواجهة الداخلية (عربي ثابت) ---
st.markdown(f"""<div class="royal-header"><h1 style="color: white; margin: 0; font-size: 40px;">MA3LOMATI PRO</h1>
<p style="color: #f59e0b; font-weight: bold;">أهلاً بك يا {st.session_state.current_user}</p></div>""", unsafe_allow_html=True)

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["briefcase", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if menu == "أدوات البروكر":
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("💳 حساب القسط")
        val = st.number_input("إجمالي السعر", 1000000)
        yrs = st.slider("السنين", 1, 15, 8)
        st.metric("القسط الشهري", f"{val/(yrs*12):,.0f}")

elif menu == "المشاريع" or menu == "المطورين" or menu == "Launches":
    active_df = df_p if menu=="المشاريع" else (df_l if menu=="Launches" else df_d)
    
    if active_df.empty:
        st.warning("⚠️ لا توجد بيانات. تأكد من روابط Google Sheets.")
    else:
        search = st.text_input("🔍 بحث سريع...")
        filt = active_df[active_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else active_df
        
        # عرض الشبكة بشكل آمن لتجنب KeyError
        grid = st.columns(2)
        for i, (idx, r) in enumerate(filt.head(10).iterrows()):
            with grid[i%2]:
                try:
                    name = r.iloc[0] # يأخذ أول عمود مهما كان اسمه
                    loc = r.get('Location', r.get('الموقع', '---'))
                    if st.button(f"🏢 {name}\n📍 {loc}", key=f"card_{idx}"):
                        st.session_state.current_index = idx
                        st.info(f"عرض تفاصيل: {name}")
                        st.json(r.to_dict()) # عرض سريع للبيانات
                except: continue

if st.button("🚪 خروج"):
    st.session_state.auth = False; st.rerun()
