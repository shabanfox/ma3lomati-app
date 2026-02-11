import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة الحالة ---
if 'auth' not in st.session_state:
    if "u_session" in st.query_params:
        st.session_state.auth = True
        st.session_state.current_user = st.query_params["u_session"]
    else:
        st.session_state.auth = False

if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0

# --- 3. الروابط ---
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
ITEMS_PER_PAGE = 6

# --- 4. تحميل البيانات مع معالجة الملايين ---
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
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price', 'سعر': 'Price'}, inplace=True, errors="ignore")
            
            if 'Price' in df.columns:
                # تنظيف وتحويل الملايين تلقائياً
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
                df['Price'] = df['Price'].apply(lambda x: x * 1_000_000 if 0 < x < 1000 else x)
                
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 5. دالة العرض المحدثة ---
def render_grid(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0

    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}", use_container_width=True): 
            st.session_state.view = "grid"; st.rerun()
        
        item = dataframe.iloc[st.session_state.current_index]
        cols = dataframe.columns
        c1, c2, c3 = st.columns(3)
        for i, col_name in enumerate(cols):
            with [c1, c2, c3][i % 3]:
                # تنسيق السعر داخل التفاصيل أيضاً
                val = item[col_name]
                if col_name == 'Price': val = f"{int(val):,}"
                st.markdown(f'<div class="detail-card"><p class="label-gold">{col_name}</p><p class="val-white">{val}</p></div>', unsafe_allow_html=True)
    else:
        # فلاتر
        f1, f2 = st.columns([1, 1])
        with f1: search = st.text_input("🔍 بحث...", key=f"s_{prefix}")
        with f2:
            locs = ["الكل"] + sorted([str(x).strip() for x in dataframe['Location'].unique() if str(x).strip() not in ["---", "nan", ""]]) if 'Location' in dataframe.columns else ["الكل"]
            sel_area = st.selectbox("📍 المنطقة", locs, key=f"l_{prefix}")

        filt = dataframe.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_area != "الكل": filt = filt[filt['Location'].astype(str).str.contains(sel_area, case=False, na=False)]

        start = st.session_state[pg_key] * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        grid = st.columns(2)
        for i, (idx, r) in enumerate(disp.iterrows()):
            with grid[i%2]:
                p_val = f"{int(r['Price']):,}" if r['Price'] > 0 else "اتصل للسعر"
                card_content = f"🏠 **{r[0]}**\n\n📍 {r.get('Location','---')}\n💰 {p_val} ج.م"
                if st.button(card_content, key=f"card_{prefix}_{idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()

# --- 6. التنسيق والموقع (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background: #000; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    .royal-header {{ background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}'); background-size: cover; border-bottom: 3px solid #f59e0b; padding: 40px; text-align: center; border-radius: 0 0 40px 40px; }}
    div.stButton > button[key*="card_"] {{ background: white !important; color: black !important; border-right: 10px solid #f59e0b !important; border-radius: 15px !important; text-align: right !important; min-height: 140px !important; font-weight: 900 !important; }}
    .detail-card {{ background: #111; padding: 20px; border-radius: 15px; border-top: 5px solid #f59e0b; margin-bottom: 10px; border: 1px solid #333; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; }}
    .val-white {{ color: white; font-size: 1.2rem; }}
    </style>
""", unsafe_allow_html=True)

# --- 7. التشغيل ---
df_p, df_d, df_l = load_data()

if not st.session_state.get('auth', False):
    st.title("MA3LOMATI PRO")
    u = st.text_input("User")
    p = st.text_input("Pass", type="password")
    if st.button("دخول"):
        if p == "2026": st.session_state.auth, st.session_state.current_user = True, u; st.rerun()
else:
    st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b;">مرحباً {st.session_state.current_user}</p></div>', unsafe_allow_html=True)
    menu = option_menu(None, ["المطورين", "المشاريع"], icons=["building", "search"], orientation="horizontal")
    
    if menu == "المشاريع": render_grid(df_p, "p")
    else: render_grid(df_d, "d")
