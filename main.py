import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة الحالة والحفاظ على الجلسة ---
if 'auth' not in st.session_state:
    if "u_session" in st.query_params:
        st.session_state.auth = True
        st.session_state.current_user = st.query_params["u_session"]
    else:
        st.session_state.auth = False

if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 3. الروابط والبيانات ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 4. الوظائف ---
def login_user(user_input, pwd_input):
    try:
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=15)
        if response.status_code == 200:
            users_list = response.json()
            user_input = str(user_input).strip().lower()
            for user_data in users_list:
                name_s = str(user_data.get('Name', user_data.get('name', ''))).strip()
                email_s = str(user_data.get('Email', user_data.get('email', ''))).strip()
                pass_s = str(user_data.get('Password', user_data.get('password', ''))).strip()
                if (user_input == name_s.lower() or user_input == email_s.lower()) and str(pwd_input) == pass_s:
                    return name_s
        return None
    except: return None

def logout():
    st.session_state.auth = False
    st.query_params.clear()
    st.rerun()

# --- 5. CSS ---
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
    .auth-card {{ background-color: #ffffff; width: 380px; padding: 55px 35px 30px 35px; border-radius: 30px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); margin: auto; }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 3px solid #f59e0b;
        padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 10px;
    }}
    div.stButton > button[key*="card_"] {{
        background: linear-gradient(145deg, #ffffff, #f9f9f9) !important;
        color: #1a1a1a !important; border-right: 6px solid #f59e0b !important;
        border-radius: 15px !important; padding: 20px !important; text-align: right !important;
        min-height: 160px !important; width: 100% !important; box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }}
    .detail-card {{ background: rgba(20, 20, 20, 0.9); padding: 25px; border-radius: 20px; border-top: 5px solid #f59e0b; color: white; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; }}
    /* تخصيص التبويبات الداخلية */
    .stTabs [data-baseweb="tab-list"] {{ gap: 20px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent !important; color: white !important;
        border-radius: 10px; padding: 10px 20px; font-weight: bold;
    }}
    .stTabs [aria-selected="true"] {{ background-color: #f59e0b !important; color: black !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. تسجيل الدخول ---
if not st.session_state.auth:
    st.markdown("<br><br><div class='auth-card'>", unsafe_allow_html=True)
    st.subheader("MA3LOMATI PRO")
    u = st.text_input("User", placeholder="اسم المستخدم", key="u")
    p = st.text_input("Pass", type="password", placeholder="كلمة السر", key="p")
    if st.button("دخول 🚀", use_container_width=True):
        if p == "2026": 
            st.session_state.auth, st.session_state.current_user = True, "Admin"
            st.query_params["u_session"] = "Admin"
            st.rerun()
        else:
            user = login_user(u, p)
            if user: 
                st.session_state.auth, st.session_state.current_user = True, user
                st.query_params["u_session"] = user
                st.rerun()
            else: st.error("بيانات خاطئة")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 7. جلب البيانات ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
    for df in [p, d, l]: 
        df.columns = [c.strip() for c in df.columns]
        df.rename(columns={'Area': 'Location', 'الموقع': 'Location'}, inplace=True, errors="ignore")
    return p.fillna("---"), d.fillna("---"), l.fillna("---")

df_p, df_d, df_l = load_data()

# --- 8. الواجهة الرئيسية ---
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p>مرحباً {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

# المنيو الرئيسي (تم حذف Launches منه)
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["briefcase", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.page_num, st.session_state.last_m = "grid", 0, menu

if st.button("🚪 خروج"): logout()

# --- 9. تنفيذ الأقسام ---
if menu == "المشاريع":
    # التبويبات الداخلية داخل قسم المشاريع
    tab_all, tab_launches = st.tabs(["🏗️ كل المشاريع", "🚀 اللونشات الجديدة"])
    
    with tab_all:
        active_df = df_p
        # نفس منطق العرض القديم
        if st.session_state.view == "details" and "proj" in st.session_state.get('subview', ''):
             if st.button("⬅ عودة"): st.session_state.view = "grid"; st.rerun()
             # عرض التفاصيل هنا...
        else:
            search = st.text_input("🔍 ابحث في المشاريع...")
            filt = active_df[active_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
            # عرض الكروت...
            for idx, r in filt.head(6).iterrows():
                if st.button(f"🏠 {r[0]}\n📍 {r.get('Location','---')}", key=f"card_p_{idx}"):
                    st.session_state.current_index, st.session_state.view, st.session_state.subview = idx, "details", "proj"
                    st.rerun()

    with tab_launches:
        active_df = df_l
        st.write("### أحدث الانطلاقات العقارية 2026")
        for idx, r in active_df.iterrows():
            st.info(f"🚀 **{r[0]}** - المطور: {r.get('Developer','---')} | الموقع: {r.get('Location','---')}")
            if st.button(f"عرض تفاصيل {r[0]}", key=f"card_l_{idx}"):
                st.session_state.current_index, st.session_state.view, st.session_state.subview = idx, "details", "launch"
                st.rerun()

elif menu == "المطورين":
    # عرض المطورين...
    for idx, r in df_d.head(10).iterrows():
        st.button(f"🏢 {r[0]}", key=f"card_d_{idx}")

elif menu == "أدوات البروكر":
    st.subheader("🔢 آلات حسابية للبروكر")
    # آلة القسط والعمولة...

elif menu == "المساعد الذكي":
    st.chat_input("اسألني عن أي عقار...")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
