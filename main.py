import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'search_query' not in st.session_state: st.session_state.search_query = ""

# --- 3. تحميل البيانات ---
@st.cache_data(ttl=60)
def load_data():
    urls = {
        "p": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv",
        "d": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv",
        "l": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    }
    try:
        p, d, l = pd.read_csv(urls["p"]), pd.read_csv(urls["d"]), pd.read_csv(urls["l"])
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price', 'المطور': 'Developer', 'Developer Name': 'Developer'}, inplace=True, errors="ignore")
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
                df['Price'] = df['Price'].apply(lambda x: x * 1_000_000 if 0 < x < 1000 else x)
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 4. دالة العرض المربوطة ---
def render_grid(dataframe, prefix, all_data=None):
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0

    if st.session_state.view == f"details_{prefix}":
        # صفحة التفاصيل
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}", use_container_width=True): 
            st.session_state.view = "grid"; st.rerun()
        
        item = dataframe.iloc[st.session_state.current_index]
        st.markdown(f"### 📄 {item.iloc[0]}")
        
        # --- ميزة الربط ---
        if prefix == "p" and 'Developer' in item:
            if st.button(f"🏢 عرض ملف المطور: {item['Developer']}", use_container_width=True):
                st.session_state.search_query = item['Developer']
                st.session_state.menu_choice = "المطورين"
                st.session_state.view = "grid"
                st.rerun()
        
        cols = st.columns(3)
        for i, col in enumerate(dataframe.columns):
            with cols[i % 3]:
                val = item[col]
                if col == 'Price': val = f"{int(val):,}" if float(val) > 0 else "اتصل"
                st.markdown(f'<div class="detail-card"><p class="label-gold">{col}</p><p class="val-white">{val}</p></div>', unsafe_allow_html=True)
                
    else:
        # صفحة القائمة
        search = st.text_input("🔍 بحث...", value=st.session_state.search_query, key=f"s_{prefix}")
        st.session_state.search_query = "" # تصغير السيرش بعد الاستخدام
        
        filt = dataframe.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        
        start = st.session_state[pg_key] * 6
        disp = filt.iloc[start : start + 6]
        
        grid = st.columns(2)
        for i, (idx, r) in enumerate(disp.iterrows()):
            with grid[i%2]:
                p_val = f"{int(r['Price']):,}" if 'Price' in r and r['Price'] > 0 else "التفاصيل"
                card_text = f"🏢 {r[0]}\n\n📍 {r.get('Location','---')}\n💰 {p_val}"
                if st.button(card_text, key=f"card_{prefix}_{idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()

# --- 5. التنسيق (CSS) ---
st.markdown("""
    <style>
    header, [data-testid="stHeader"] { visibility: hidden; }
    [data-testid="stAppViewContainer"] { background: #000; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    div.stButton > button[key*="card_"] { background: white !important; color: black !important; border-right: 12px solid #f59e0b !important; border-radius: 15px !important; min-height: 140px !important; font-weight: 900 !important; }
    .detail-card { background: #111; padding: 15px; border-radius: 10px; border-top: 4px solid #f59e0b; margin-bottom: 10px; border: 1px solid #333; }
    .label-gold { color: #f59e0b; font-weight: bold; margin:0; }
    .val-white { color: white; font-size: 1.1rem; margin:0; }
    </style>
""", unsafe_allow_html=True)

# --- 6. التشغيل ---
if not st.session_state.auth:
    p = st.text_input("Pass", type="password")
    if st.button("دخول"):
        if p == "2026": st.session_state.auth = True; st.rerun()
else:
    # المنيو مع الحفاظ على الاختيار
    if 'menu_choice' not in st.session_state: st.session_state.menu_choice = "المشاريع"
    
    menu = option_menu(None, ["المطورين", "المشاريع", "اللونشات"], 
                       icons=["building", "search", "rocket"], 
                       default_index=1 if st.session_state.menu_choice == "المشاريع" else 0,
                       orientation="horizontal")
    
    st.session_state.menu_choice = menu
    
    if menu == "المشاريع": render_grid(df_p, "p")
    elif menu == "اللونشات": render_grid(df_l, "l")
    else: render_grid(df_d, "d")
