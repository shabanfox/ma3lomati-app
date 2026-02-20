import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 2. الروابط الأساسية ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 3. وظائف النظام ---
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

def logout():
    st.session_state.auth = False
    st.session_state.current_user = None
    st.rerun()

# --- 4. التصميم الجمالي CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 3px solid #f59e0b;
        padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 10px;
    }}
    div.stButton > button[key*="card_"] {{
        background: linear-gradient(145deg, #ffffff, #f9f9f9) !important;
        color: #1a1a1a !important; border-right: 6px solid #f59e0b !important;
        border-radius: 15px !important; padding: 20px !important; text-align: right !important;
        min-height: 180px !important; width: 100% !important; box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        white-space: pre-line !important; font-family: 'Cairo', sans-serif !important;
    }}
    .detail-card {{ background: rgba(20, 20, 20, 0.9); padding: 25px; border-radius: 20px; border-top: 5px solid #f59e0b; color: white; border: 1px solid #333; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 14px; margin-top: 5px; }}
    .val-white {{ color: white; font-size: 16px; border-bottom: 1px solid #333; padding-bottom:5px; }}
    
    /* ستايل التبويبات الداخلية */
    .stTabs [data-baseweb="tab-list"] {{ gap: 20px; }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px; background-color: rgba(255,255,255,0.05);
        border-radius: 10px; color: white !important; padding: 0 30px;
    }}
    .stTabs [aria-selected="true"] {{ background-color: #f59e0b !important; color: black !important; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. منطق الدخول (تم الإبقاء عليه كما هو) ---
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    u = st.text_input("User", key="u_login")
    p = st.text_input("Pass", type="password", key="p_login")
    if st.button("SIGN IN"):
        if p == "2026" or login_user(u, p):
            st.session_state.auth, st.session_state.current_user = True, u or "Admin"
            st.rerun()
    st.stop()

# --- 6. جلب البيانات ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]: 
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 7. واجهة المنصة ---
st.markdown(f'<div class="royal-header"><h1 style="color:white; margin:0; font-size:40px;">MA3LOMATI PRO</h1></div>', unsafe_allow_html=True)

# القائمة الرئيسية المحدثة (بدون Launches)
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["briefcase", "building", "house", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

# --- 8. تنفيذ الأقسام ---

if menu == "المشاريع":
    # طلبك: تقسيم صفحة المشاريع لـ (جميع المشاريع) و (مشاريع جديدة)
    tab_all, tab_new = st.tabs(["🏗️ جميع المشاريع", "🚀 المشاريع الجديدة"])
    
    with tab_all:
        search_all = st.text_input("🔍 بحث في جميع المشاريع...", key="search_all")
        filt_all = df_p[df_p.apply(lambda r: r.astype(str).str.contains(search_all, case=False).any(), axis=1)] if search_all else df_p
        
        # عرض الكروت لجميع المشاريع
        grid_all = st.columns(2)
        for i, (idx, r) in enumerate(filt_all.head(10).iterrows()):
            with grid_all[i%2]:
                card_text = f"🏠 {r[0]}\n📍 {r.get('Location','---')}\n🏗️ {r.get('Developer','---')}"
                if st.button(card_text, key=f"card_all_{idx}"):
                    st.info(f"تفاصيل المشروع: {r[0]}")

    with tab_new:
        st.markdown("<h3 style='color:#f59e0b;'>أحدث الانطلاقات (Launches)</h3>", unsafe_allow_html=True)
        search_new = st.text_input("🔍 بحث في المشاريع الجديدة...", key="search_new")
        filt_new = df_l[df_l.apply(lambda r: r.astype(str).str.contains(search_new, case=False).any(), axis=1)] if search_new else df_l
        
        # عرض الكروت للمشاريع الجديدة (بيانات شيت اللونشات)
        grid_new = st.columns(2)
        for i, (idx, r) in enumerate(filt_new.iterrows()):
            with grid_new[i%2]:
                card_text = f"🚀 {r[0]}\n📍 {r.get('Location','---')}\n✨ مشروع جديد كلياً"
                if st.button(card_text, key=f"card_new_{idx}"):
                    st.success(f"تفاصيل اللونش: {r[0]}")

elif menu == "المطورين":
    st.dataframe(df_d, use_container_width=True)

elif menu == "أدوات البروكر":
    st.subheader("🛠️ أدوات الحساب")
    v = st.number_input("السعر", value=1000000)
    st.write(f"القسط الشهري على 8 سنوات: {v/(8*12):,.0f}")

elif menu == "المساعد الذكي":
    st.chat_input("اسألني عن أي عقار...")

if st.sidebar.button("🚪 خروج"): logout()
