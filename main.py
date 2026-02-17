import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الثوابت والروابط (كما هي في كودك الأصلي تماماً) ---
GOLD_COLOR = "#D4AF37"
GOLD_GRADIENT = "linear-gradient(135deg, #D4AF37 0%, #F9E29C 50%, #B8860B 100%)"

if 'auth' not in st.session_state:
    st.session_state.auth = "u_session" in st.query_params
    st.session_state.current_user = st.query_params.get("u_session", "Guest")

if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0

URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

@st.cache_data(ttl=60)
def load_data():
    try:
        p = pd.read_csv(URL_PROJECTS).fillna("---")
        d = pd.read_csv(URL_DEVELOPERS).fillna("---")
        l = pd.read_csv(URL_LAUNCHES).fillna("---")
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price'}, inplace=True, errors="ignore")
        return p, d, l
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 3. محرك التصميم القوي (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إجبار الخلفية السوداء */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: #0a0a0a !important;
        color: white !important;
        direction: rtl !important;
        font-family: 'Cairo', sans-serif !important;
    }}

    /* تصميم الكارت الذهبي */
    .modern-card {{
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        margin-bottom: 15px !important;
        text-align: right !important;
        transition: 0.3s !important;
    }}
    .modern-card:hover {{
        border-color: {GOLD_COLOR} !important;
        background: rgba(212, 175, 55, 0.05) !important;
        transform: translateY(-5px);
    }}

    /* تصميم أزرار ستريمليت لتصبح ذهبية غصب عنها */
    div.stButton > button {{
        background: {GOLD_GRADIENT} !important;
        color: black !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        height: 3em !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.2) !important;
    }}

    /* تصميم التبويبات */
    .stTabs [aria-selected="true"] {{
        background: {GOLD_GRADIENT} !important;
        color: black !important;
        border-radius: 10px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. دالة عرض الشبكة المعدلة ---
def render_grid(dataframe, prefix):
    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}"):
            st.session_state.view = "grid"; st.rerun()
        
        item = dataframe.iloc[st.session_state.current_index]
        st.markdown(f"<h2 style='color:{GOLD_COLOR}'>🏠 {item.iloc[0]}</h2>", unsafe_allow_html=True)
        for col in dataframe.columns:
            st.markdown(f"<div style='background:#111; padding:10px; margin:5px; border-radius:10px;'><b style='color:{GOLD_COLOR}'>{col}:</b> {item[col]}</div>", unsafe_allow_html=True)
    
    else:
        search = st.text_input("🔍 ابحث هنا...", key=f"s_{prefix}")
        filt = dataframe[dataframe.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else dataframe
        
        grid = st.columns(2)
        for i, (idx, r) in enumerate(filt.head(10).iterrows()):
            with grid[i%2]:
                # الكارت كـ HTML للجمال
                st.markdown(f"""
                    <div class="modern-card">
                        <h3 style="color:{GOLD_COLOR}; margin:0;">🏢 {str(r[0])}</h3>
                        <p style="color:#aaa; font-size:0.9rem; margin:10px 0;">📍 {r.get('Location','---')}</p>
                    </div>
                """, unsafe_allow_html=True)
                # زر التفاصيل (ستريمليت) لكنه سيأخذ التصميم الذهبي من الـ CSS أعلاه
                if st.button(f"عرض تفاصيل {str(r[0])[:15]}", key=f"btn_{prefix}_{idx}"):
                    st.session_state.current_index = idx
                    st.session_state.view = f"details_{prefix}"
                    st.rerun()

# --- 5. تنفيذ التطبيق ---
if not st.session_state.auth:
    # صفحة التسجيل (مختصرة للتركيز على التصميم)
    st.markdown("<h1 style='text-align:center;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    u = st.text_input("User")
    p = st.text_input("Pass", type="password")
    if st.button("SIGN IN"):
        if p == "2026": 
            st.session_state.auth = True
            st.rerun()
    st.stop()

df_p, df_d, df_l = load_data()

# الهيدر
st.markdown(f"<h1 style='text-align:center; color:{GOLD_COLOR}; border-bottom:1px solid #333; padding:20px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)

menu = option_menu(None, ["المطورين", "المشاريع", "أدوات الحساب"], 
    icons=["building", "search", "calculator"], orientation="horizontal",
    styles={"nav-link-selected": {"background": GOLD_GRADIENT, "color": "black"}})

if menu == "المشاريع":
    t1, t2 = st.tabs(["المشاريع", "اللونشات"])
    with t1: render_grid(df_p, "p")
    with t2: render_grid(df_l, "l")
elif menu == "المطورين":
    render_grid(df_d, "d")
elif menu == "أدوات الحساب":
    st.markdown(f"<h2 style='color:{GOLD_COLOR}'>💰 حاسبة القروض</h2>", unsafe_allow_html=True)
    # حاسبة بسيطة كمثال
    price = st.number_input("سعر الوحدة", value=1000000)
    st.write(f"القسط التقريبي: {price/96:,.0f} شهرياً")
