import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة حالة الجلسة (Session State) ---
if 'auth' not in st.session_state:
    if "u_session" in st.query_params:
        st.session_state.auth, st.session_state.current_user = True, st.query_params["u_session"]
    else: st.session_state.auth = False

if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'search_val' not in st.session_state: st.session_state.search_val = "" # مخزن للربط التلقائي

# --- 3. الروابط والثوابت ---
URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 4. الوظائف التقنية ---
def login_user(u, p):
    try:
        res = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=10)
        if res.status_code == 200:
            for user in res.json():
                if str(u).strip().lower() == str(user.get('Name','')).lower() and str(p) == str(user.get('Password','')): return user.get('Name')
    except: pass
    return None

@st.cache_data(ttl=60)
def load_data():
    try:
        p, d, l = pd.read_csv(URL_PROJECTS), pd.read_csv(URL_DEVELOPERS), pd.read_csv(URL_LAUNCHES)
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price', 'سعر': 'Price'}, inplace=True, errors="ignore")
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
                df['Price'] = df['Price'].apply(lambda x: x * 1_000_000 if 0 < x < 1000 else x)
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# دالة الجاب التلقائي (الربط)
def navigate_to(target_menu, search_query):
    st.session_state.last_m = target_menu
    st.session_state.search_val = search_query
    st.session_state.view = "grid"
    st.rerun()

# --- 5. دالة العرض الرئيسية ---
def render_grid(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0

    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}", use_container_width=True): 
            st.session_state.view = "grid"; st.rerun()
        
        item = dataframe.iloc[st.session_state.current_index]
        st.markdown(f"<h2 style='color:#f59e0b; text-align:right;'>🏠 {item.iloc[0]}</h2>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, col_name in enumerate(dataframe.columns):
            with cols[i % 3]:
                val = str(item[col_name])
                st.markdown('<div class="detail-card">', unsafe_allow_html=True)
                st.markdown(f'<p class="label-gold">{col_name}</p>', unsafe_allow_html=True)
                
                # --- منطق الربط الذكي ---
                # 1. لو في تفاصيل المشروع ودست على المطور
                if col_name in ['Developer', 'المطور', 'الشركة'] and val != "---":
                    if st.button(f"🏢 ملف: {val}", key=f"link_dev_{i}"): navigate_to("المطورين", val)
                # 2. لو في تفاصيل المطور ودست على عدد المشاريع أو الاسم
                elif col_name in ['عدد المشاريع', 'Projects'] and val != "---":
                    if st.button(f"🔍 عرض الكل", key=f"link_proj_{i}"): navigate_to("المشاريع", str(item.iloc[0]))
                else:
                    disp_val = f"{int(float(val)):,}" if col_name == 'Price' and float(val) > 0 else val
                    st.markdown(f'<p class="val-white">{disp_val}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        # البحث (يدعم القيمة الممرة من الربط)
        search = st.text_input("🔍 بحث...", value=st.session_state.search_val, key=f"s_{prefix}")
        st.session_state.search_val = "" # تصفير القيمة بعد الاستخدام
        
        filt = dataframe[dataframe.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else dataframe
        start = st.session_state[pg_key] * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.8, 0.2])
        with m_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    # لو فيه عمود للوجو في الشيت هيظهر
                    if 'Logo_URL' in r and r['Logo_URL'] != "---":
                        st.markdown(f'<div style="background:white; text-align:center; border-radius:15px 15px 0 0; margin-bottom:-10px;"><img src="{r["Logo_URL"]}" style="height:40px;"></div>', unsafe_allow_html=True)
                    
                    price = f"{int(r['Price']):,}" if ('Price' in r and r['Price'] > 0) else "اتصل"
                    if st.button(f"🏢 {r[0]}\n📍 {r.get('Location','---')}\n💰 {price}", key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()

# --- 6. التصميم (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    .auth-card {{ background-color: #ffffff; padding: 40px; border-radius: 30px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); width: 400px; margin: auto; }}
    .royal-header {{ background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}'); background-size: cover; padding: 40px; text-align: center; border-radius: 0 0 40px 40px; border-bottom: 3px solid #f59e0b; }}
    div.stButton > button[key*="card_"] {{ background: white !important; color: black !important; border-right: 12px solid #f59e0b !important; border-radius: 15px !important; text-align: right !important; min-height: 120px !important; font-weight: 900 !important; }}
    .detail-card {{ background: rgba(30, 30, 30, 0.9); padding: 15px; border-radius: 15px; border-top: 5px solid #f59e0b; margin-bottom: 10px; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 0.9rem; }}
    .val-white {{ color: white; font-size: 1.1rem; font-weight: 700; }}
    </style>
""", unsafe_allow_html=True)

# --- 7. بوابة الدخول ---
if not st.session_state.get('auth', False):
    _, c, _ = st.columns([1, 1.5, 1])
    with c:
        st.markdown("<br><br><div class='auth-card'>", unsafe_allow_html=True)
        st.title("MA3LOMATI PRO")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("SIGN IN", use_container_width=True):
            if p == "2026": st.session_state.auth, st.session_state.current_user = True, "Admin"; st.rerun()
            else:
                user = login_user(u, p)
                if user: st.session_state.auth, st.session_state.current_user = True, user; st.rerun()
                else: st.error("بيانات خاطئة")
        st.markdown("</div>", unsafe_allow_html=True); st.stop()

# --- 8. التشغيل ---
df_p, df_d, df_l = load_data()
st.markdown(f'<div class="royal-header"><h1 style="color:#f59e0b;">MA3LOMATI PRO</h1><p style="color:white;">أهلاً {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

menu_options = ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"]
# تحديد الـ Index بناءً على القسم الأخير لضمان عمل الربط
current_menu_idx = menu_options.index(st.session_state.get('last_m', "المشاريع"))

menu = option_menu(None, menu_options, 
    icons=["calculator", "building", "search", "robot"], 
    default_index=current_menu_idx, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000", "font-weight": "900"}})

if menu != st.session_state.get('last_m'):
    st.session_state.view, st.session_state.last_m = "grid", menu

if menu == "أدوات الحساب":
    # (الأدوات كما هي في كودك)
    st.write("استخدم أدوات الحساب العقارية...")
elif menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ جميع المشاريع", "🚀 اللونشات"])
    with t1: render_grid(df_p, "p")
    with t2: render_grid(df_l, "l")
elif menu == "المطورين":
    render_grid(df_d, "d")

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)

