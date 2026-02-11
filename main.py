import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة الحالة (Session State) ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "عربي"
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0

# --- 3. الروابط ---
URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 4. الوظائف ---
def login_user(u, p):
    try:
        res = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=10)
        if res.status_code == 200:
            for user in res.json():
                if str(u).strip().lower() == str(user.get('Name')).strip().lower() and str(p) == str(user.get('Password')):
                    return user.get('Name')
        return None
    except: return None

@st.cache_data(ttl=60)
def load_data():
    try:
        p, d, l = pd.read_csv(URL_PROJECTS), pd.read_csv(URL_DEVELOPERS), pd.read_csv(URL_LAUNCHES)
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price'}, inplace=True, errors="ignore")
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
                df['Price'] = df['Price'].apply(lambda x: x * 1_000_000 if 0 < x < 1000 else x)
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def render_grid(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0
    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ Back / عودة", key=f"back_{prefix}", use_container_width=True): 
            st.session_state.view = "grid"; st.rerun()
        item = dataframe.iloc[st.session_state.current_index]
        st.markdown(f"<h2 style='color:#f59e0b; text-align:right;'>🏠 {item.iloc[0]}</h2>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, col_name in enumerate(dataframe.columns):
            with cols[i % 3]:
                val = item[col_name]
                if col_name == 'Price': val = f"{int(val):,}" if float(val) > 0 else "---"
                st.markdown(f'<div class="detail-card"><p class="label-gold">{col_name}</p><p class="val-white">{val}</p></div>', unsafe_allow_html=True)
    else:
        f1, f2 = st.columns([2, 1])
        with f1: search = st.text_input("🔍 Search / بحث", key=f"s_{prefix}")
        with f2:
            locs = ["الكل"] + sorted([str(x).strip() for x in dataframe['Location'].unique() if str(x).strip() not in ["---", "nan", ""]]) if 'Location' in dataframe.columns else ["الكل"]
            sel_area = st.selectbox("📍 Location / الموقع", locs, key=f"l_{prefix}")
        filt = dataframe.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_area != "الكل": filt = filt[filt['Location'].astype(str).str.contains(sel_area, case=False, na=False)]
        start = st.session_state[pg_key] * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        m_c, s_c = st.columns([0.8, 0.2])
        with m_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    p_v = f"{int(r['Price']):,}" if ('Price' in r and r['Price'] > 0) else "Contact"
                    if st.button(f"🏢 {r[0]}\n\n📍 {r.get('Location','---')}\n💰 {p_v}", key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
            p1, px, p2 = st.columns([1, 1, 1])
            with p1: 
                if st.session_state[pg_key] > 0 and st.button("⬅ Prev", key=f"prev_{prefix}"): st.session_state[pg_key] -= 1; st.rerun()
            with px: st.markdown(f"<p style='text-align:center; color:#f59e0b;'>Page {st.session_state[pg_key]+1}</p>", unsafe_allow_html=True)
            with p2:
                if (start + ITEMS_PER_PAGE) < len(filt) and st.button("Next ➡", key=f"next_{prefix}"): st.session_state[pg_key] += 1; st.rerun()
        with s_c:
            st.markdown("<p style='color:#f59e0b; font-weight:bold;'>🔥 Suggestions</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(8).iterrows():
                if st.button(f"📌 {str(s_row[0])[:12]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()

# --- 5. CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}'); background-size: cover; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    .auth-card {{ background: white; padding: 40px; border-radius: 30px; text-align: center; width: 350px; margin: auto; }}
    .royal-header {{ background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}'); background-size: cover; padding: 40px; text-align: center; border-radius: 0 0 40px 40px; border-bottom: 3px solid #f59e0b; }}
    div.stButton > button[key*="card_"] {{ background: white !important; color: black !important; border-right: 12px solid #f59e0b !important; border-radius: 15px !important; min-height: 140px !important; font-weight: 900 !important; }}
    .detail-card {{ background: rgba(30,30,30,0.9); padding: 15px; border-radius: 10px; border-top: 4px solid #f59e0b; margin-bottom: 10px; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; }}
    .val-white {{ color: white; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. بوابة الدخول ---
if not st.session_state.auth:
    col_l, col_r = st.columns([8, 2])
    with col_r: # زر اللغة
        if st.button(f"🌐 {st.session_state.lang}"):
            st.session_state.lang = "English" if st.session_state.lang == "عربي" else "عربي"; st.rerun()
    
    st.markdown("<br><br><div class='auth-card'>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:black;'>{'الدخول' if st.session_state.lang == 'عربي' else 'Login'}</h2>", unsafe_allow_html=True)
    u = st.text_input("User", placeholder="Username")
    p = st.text_input("Pass", type="password", placeholder="Password")
    if st.button("SIGN IN 🚀", use_container_width=True):
        if p == "2026": st.session_state.auth, st.session_state.current_user = True, "Admin"; st.rerun()
        else:
            user = login_user(u, p)
            if user: st.session_state.auth, st.session_state.current_user = True, user; st.rerun()
            else: st.error("Error")
    st.markdown("</div>", unsafe_allow_html=True); st.stop()

# --- 7. الصفحة الرئيسية ---
df_p, df_d, df_l = load_data()

# الهيدر مع زر الخروج
st.markdown('<div class="royal-header"><h1>MA3LOMATI PRO</h1></div>', unsafe_allow_html=True)
c_user, c_out = st.columns([9, 1])
with c_user: st.markdown(f"<p style='color:#f59e0b;'>Welcome, {st.session_state.current_user}</p>", unsafe_allow_html=True)
with c_out: 
    if st.button("🚪 Out", size="small"): st.session_state.auth = False; st.rerun()

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

if menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ جميع المشاريع", "🆕 المشاريع الجديدة"])
    with t1: render_grid(df_p, "p")
    with t2: render_grid(df_l, "l")
elif menu == "المطورين": render_grid(df_d, "d")
elif menu == "أدوات الحساب": st.info("Calculator Tools")
elif menu == "المساعد الذكي": st.info("AI Assistant")
