import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "عربي"
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0

# --- 3. الروابط ---
URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 4. تحميل البيانات ---
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

# --- 5. دالة العرض الرئيسية (70% المحتوى) ---
def render_main_content(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0
    
    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة الرئيسية", key=f"back_{prefix}"): 
            st.session_state.view = "grid"; st.rerun()
        item = dataframe.iloc[st.session_state.current_index]
        st.markdown(f"<h2 style='color:#f59e0b;'>🏠 {item.iloc[0]}</h2>", unsafe_allow_html=True)
        for i, col in enumerate(dataframe.columns):
            val = item[col]
            if col == 'Price': val = f"{int(val):,}" if float(val) > 0 else "اتصل"
            st.markdown(f'<div class="detail-card"><b style="color:#f59e0b">{col}:</b> {val}</div>', unsafe_allow_html=True)
    else:
        search = st.text_input("🔍 بحث سريح...", key=f"s_{prefix}")
        filt = dataframe[dataframe.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else dataframe
        
        start = st.session_state[pg_key] * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        grid = st.columns(2)
        for i, (idx, r) in enumerate(disp.iterrows()):
            with grid[i%2]:
                if st.button(f"🏢 {r[0]}\n\n📍 {r.get('Location','---')}", key=f"btn_{prefix}_{idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()

# --- 6. التصميم CSS ---
st.markdown(f"""
    <style>
    header, [data-testid="stHeader"] {{ visibility: hidden; }}
    [data-testid="stAppViewContainer"] {{ background: #0e1117; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    .side-panel {{ background: #1a1c23; padding: 20px; border-radius: 15px; border: 1px solid #f59e0b; margin-bottom: 20px; }}
    .detail-card {{ background: #262730; padding: 10px; border-radius: 5px; margin-bottom: 5px; border-right: 5px solid #f59e0b; }}
    div.stButton > button {{ border-radius: 10px !important; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# --- 7. بوابة الدخول ---
if not st.session_state.auth:
    col_l, _ = st.columns([1, 5])
    with col_l: 
        if st.button(f"🌐 {st.session_state.lang}"):
            st.session_state.lang = "EN" if st.session_state.lang == "عربي" else "عربي"; st.rerun()
    st.markdown("<h2 style='text-align:center;'>MA3LOMATI PRO 2026</h2>", unsafe_allow_html=True)
    u = st.text_input("User")
    p = st.text_input("Pass", type="password")
    if st.button("SIGN IN", use_container_width=True):
        if p == "2026" or p == "123": st.session_state.auth = True; st.rerun()
    st.stop()

# --- 8. الصفحة الرئيسية (التقسيمة 70% لـ 30%) ---
df_p, df_d, df_l = load_data()

# الهيدر وزر الخروج
st.markdown(f'<div style="background:linear-gradient(90deg, #f59e0b, #000); padding:20px; border-radius:15px; text-align:center;"><h1>MA3LOMATI PRO</h1></div>', unsafe_allow_html=True)
if st.button("Logout 🚪"): st.session_state.auth = False; st.rerun()

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

# تقسيم الصفحة الأساسي
col_main, col_side = st.columns([0.7, 0.3])

with col_main: # الجزء الـ 70%
    if menu == "المشاريع":
        t1, t2 = st.tabs(["🏗️ جميع المشاريع", "🆕 المشاريع الجديدة"])
        with t1: render_main_content(df_p, "p")
        with t2: render_main_content(df_l, "l")
    elif menu == "المطورين":
        render_main_content(df_d, "d")
    elif menu == "أدوات الحساب":
        st.subheader("🛠️ أدوات البروكر")
        pr = st.number_input("السعر", value=1000000)
        dp = st.number_input("المقدم %", value=10)
        yr = st.number_input("السنين", value=7)
        st.success(f"القسط: {(pr*(1-dp/100))/(yr*12):,.0f} ج.م")

with col_side: # الجزء الـ 30% (الأفضل والأقوى)
    st.markdown("<div class='side-panel'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#f59e0b; text-align:center;'>🔥 أفضل المشاريع</h3>", unsafe_allow_html=True)
    for i, r in df_p.head(5).iterrows():
        if st.button(f"⭐ {r[0]}", key=f"side_p_{i}", use_container_width=True):
            st.session_state.current_index, st.session_state.view = i, "details_p"; st.rerun()
    
    st.markdown("<hr style='border:1px solid #333;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#f59e0b; text-align:center;'>🏢 أقوى المطورين</h3>", unsafe_allow_html=True)
    for i, r in df_d.head(5).iterrows():
        if st.button(f"🏆 {r[0]}", key=f"side_d_{i}", use_container_width=True):
            st.session_state.current_index, st.session_state.view = i, "details_d"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
