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

# --- 4. وظائف النظام ---
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
    st.query_params.clear()
    st.rerun()

# --- 5. التصميم الجمالي CSS (نفس الستايل القديم) ---
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
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: flex-start; width: 100%; padding-top: 50px; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 24px; font-weight: 900;
        text-align: center; z-index: 10; margin-bottom: -30px; min-width: 360px;
    }}
    .auth-card {{ background-color: #ffffff; width: 380px; padding: 55px 35px 30px 35px; border-radius: 30px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 3px solid #f59e0b;
        padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 10px;
    }}
    div.stButton > button[key*="card_"] {{
        background: linear-gradient(145deg, #ffffff, #f9f9f9) !important;
        color: #1a1a1a !important; border-right: 6px solid #f59e0b !important;
        border-radius: 15px !important; padding: 20px !important;
        text-align: right !important; line-height: 1.7 !important;
        min-height: 180px !important; width: 100% !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        transition: all 0.3s ease !important; white-space: pre-line !important;
        margin-bottom: 10px !important; font-family: 'Cairo', sans-serif !important;
    }}
    .detail-card {{ background: rgba(20, 20, 20, 0.9); padding: 25px; border-radius: 20px; border-top: 5px solid #f59e0b; color: white; border: 1px solid #333; margin-bottom:20px; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 14px; margin-top: 5px; }}
    .val-white {{ color: white; font-size: 16px; border-bottom: 1px solid #333; padding-bottom:5px; margin-bottom: 8px; }}
    
    /* ستايل التبويبات ليناسب التصميم */
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px; background-color: #111 !important; color: white !important;
        border-radius: 10px 10px 0 0; border: 1px solid #333; padding: 10px 20px;
    }}
    .stTabs [aria-selected="true"] {{ background-color: #f59e0b !important; color: black !important; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. منطق الدخول ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>MA3LOMATI PRO</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    u = st.text_input("User", placeholder="الأسم أو الإيميل", label_visibility="collapsed", key="u")
    p = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="p")
    if st.button("SIGN IN 🚀", use_container_width=True):
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
            else: st.error("خطأ في البيانات")
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 7. جلب البيانات ---
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

# --- 8. واجهة المنصة ---
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b;">مرحباً {st.session_state.current_user}</p></div>', unsafe_allow_html=True)
_, c_ex = st.columns([0.88, 0.12])
with c_ex:
    if st.button("🚪 خروج", key="ex", use_container_width=True): logout()

# المنيو الرئيسي (تم دمج اللونشات)
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["briefcase", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.page_num, st.session_state.last_m = "grid", 0, menu

# --- 9. تنفيذ الأقسام ---
if menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ جميع المشاريع", "🚀 اللونشات الحالية"])
    
    with t1:
        active_df = df_p
        if st.session_state.view == "details":
            if st.button("⬅ عودة للمشاريع", key="back_p"): st.session_state.view = "grid"; st.rerun()
            # عرض التفاصيل (نفس ستايلك القديم)
            item = active_df.iloc[st.session_state.current_index]
            c1, c2, c3 = st.columns(3)
            cols = active_df.columns
            for i, cs in enumerate([cols[:len(cols)//3+1], cols[len(cols)//3+1:2*len(cols)//3+1], cols[2*len(cols)//3+1:]]):
                with [c1, c2, c3][i]:
                    h = '<div class="detail-card">'
                    for k in cs: h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                    st.markdown(h+'</div>', unsafe_allow_html=True)
        else:
            search = st.text_input("🔍 بحث في المشاريع...", key="search_p")
            filt = active_df[active_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
            start = st.session_state.page_num * ITEMS_PER_PAGE
            disp = filt.iloc[start : start + ITEMS_PER_PAGE]
            
            m_c, s_c = st.columns([0.76, 0.24])
            with m_c:
                grid = st.columns(2)
                for i, (idx, r) in enumerate(disp.iterrows()):
                    with grid[i%2]:
                        card_text = f"🏠 {r[0]}\n🏗️ المطور: {r.get('Developer','---')}\n📍 الموقع: {r.get('Location','---')}"
                        if st.button(card_text, key=f"card_p_{idx}"):
                            st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()
    
    with t2:
        active_df = df_l
        if st.session_state.view == "details_l":
            if st.button("⬅ عودة للونشات", key="back_l"): st.session_state.view = "grid"; st.rerun()
            # تفاصيل اللونش
            item = active_df.iloc[st.session_state.current_index]
            st.markdown(f'<div class="detail-card"><h3>🚀 {item[0]}</h3><p>مزيد من التفاصيل قريباً...</p></div>', unsafe_allow_html=True)
        else:
            st.markdown("<p style='color:#f59e0b; font-weight:bold;'>أحدث انطلاقات 2026</p>", unsafe_allow_html=True)
            grid_l = st.columns(2)
            for i, (idx, r) in enumerate(active_df.iterrows()):
                with grid_l[i%2]:
                    card_text = f"🚀 {r[0]}\n🏗️ المطور: {r.get('Developer','---')}\n📅 موعد اللونش: {r.get('Date','2026')}"
                    if st.button(card_text, key=f"card_l_{idx}"):
                        st.session_state.current_index, st.session_state.view = idx, "details_l"; st.rerun()

elif menu == "المطورين":
    active_df = df_d
    search = st.text_input("🔍 بحث عن مطور...")
    grid_d = st.columns(2)
    for i, (idx, r) in enumerate(active_df.head(10).iterrows()):
        with grid_d[i%2]:
            if st.button(f"🏢 {r[0]}\n📈 المشاريع: {r.get('Projects','---')}", key=f"card_d_{idx}"):
                st.write(f"عرض مطور: {r[0]}")

elif menu == "أدوات البروكر":
    st.subheader("💳 أدوات الحساب العقاري")
    c1, c2 = st.columns(2)
    with c1: st.number_input("سعر الوحدة", value=1000000)
    with c2: st.number_input("سنوات التقسيط", value=8)

elif menu == "المساعد الذكي":
    st.info("نظام تحليل البيانات العقارية AI")
    st.chat_input("سؤالك عن السوق...")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026 | Powered by AI</p>", unsafe_allow_html=True)
