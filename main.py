import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة حالة الجلسة ---
if 'auth' not in st.session_state:
    if "u_session" in st.query_params:
        st.session_state.auth, st.session_state.current_user = True, st.query_params["u_session"]
    else: st.session_state.auth = False

if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0

# --- 3. الروابط والثوابت ---
URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

BG_IMG = "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=2070&auto=format&fit=crop"
GOLD_COLOR = "#D4AF37"
DARK_CARD = "rgba(20, 20, 20, 0.85)"

# --- 4. الوظائف التقنية ---
@st.cache_data(ttl=300)
def load_data():
    try:
        p = pd.read_csv(URL_PROJECTS); d = pd.read_csv(URL_DEVELOPERS); l = pd.read_csv(URL_LAUNCHES)
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price'}, inplace=True, errors="ignore")
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
                df['Price'] = df['Price'].apply(lambda x: x * 1_000_000 if 0 < x < 1000 else x)
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 5. التصميم الفاخر (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;700;900&display=swap');
    
    /* الأساسيات */
    * {{ font-family: 'Cairo', sans-serif; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl; text-align: right;
    }}
    header {{ visibility: hidden; }}
    
    /* الهيدر الحديث */
    .main-header {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        padding: 40px; border-radius: 0 0 50px 50px;
        border-bottom: 2px solid {GOLD_COLOR};
        text-align: center; margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .main-header h1 {{ color: {GOLD_COLOR}; font-weight: 900; font-size: 3.5rem; letter-spacing: 2px; margin: 0; }}
    
    /* الكروت الزجاجية */
    .glass-card {{
        background: {DARK_CARD};
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 20px; padding: 25px;
        transition: all 0.4s ease;
    }}
    .glass-card:hover {{ border: 1px solid {GOLD_COLOR}; transform: translateY(-5px); box-shadow: 0 10px 20px rgba(212, 175, 55, 0.2); }}

    /* أزرار مخصصة */
    div.stButton > button {{
        background: linear-gradient(45deg, #000, #222) !important;
        color: {GOLD_COLOR} !important;
        border: 1px solid {GOLD_COLOR} !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        transition: 0.3s !important;
        width: 100%;
    }}
    div.stButton > button:hover {{
        background: {GOLD_COLOR} !important;
        color: black !important;
        box-shadow: 0 0 15px {GOLD_COLOR};
    }}

    /* تفاصيل المحتوى */
    .stat-label {{ color: #888; font-size: 0.9rem; margin-bottom: 5px; }}
    .stat-value {{ color: white; font-size: 1.2rem; font-weight: 700; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. بوابة الدخول (Modern Login) ---
if not st.session_state.get('auth', False):
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1, 1.5, 1])
    with col_m:
        st.markdown(f"""
            <div style="background:rgba(0,0,0,0.7); padding:40px; border-radius:30px; border:1px solid {GOLD_COLOR}; text-align:center;">
                <h1 style="color:{GOLD_COLOR};">MA3LOMATI PRO</h1>
                <p style="color:#eee;">نظام إدارة البيانات العقارية الذكي</p>
            </div>
        """, unsafe_allow_html=True)
        u = st.text_input("Username", key="login_u")
        p = st.text_input("Password", type="password", key="login_p")
        if st.button("دخول للنظام", use_container_width=True):
            if p == "2026": # كلمة سر بسيطة للتجربة
                st.session_state.auth, st.session_state.current_user = True, u
                st.rerun()
            else: st.error("خطأ في البيانات")
    st.stop()

# --- 7. المحتوى الرئيسي ---
df_p, df_d, df_l = load_data()

st.markdown(f"""
    <div class="main-header">
        <h1>MA3LOMATI PRO</h1>
        <p style="color:#aaa;">مرحباً بك، {st.session_state.current_user} | الاستبصار العقاري لعام 2026</p>
    </div>
""", unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building-up", "search-heart", "cpu"], 
    default_index=2, orientation="horizontal",
    styles={
        "container": {"background-color": "rgba(0,0,0,0.5)", "border-radius": "15px", "border": f"1px solid {GOLD_COLOR}"},
        "nav-link": {"font-size": "18px", "text-align": "center", "margin": "5px", "color": "white"},
        "nav-link-selected": {"background-color": GOLD_COLOR, "color": "black", "font-weight": "900"}
    }
)

# --- 8. منطق العرض المطور ---
def render_modern_grid(df, prefix):
    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}"): 
            st.session_state.view = "grid"; st.rerun()
        
        item = df.iloc[st.session_state.current_index]
        st.markdown(f"<h1 style='color:{GOLD_COLOR};'>{item.iloc[0]}</h1>", unsafe_allow_html=True)
        
        # كروت التفاصيل الزجاجية
        cols = st.columns(3)
        for i, col in enumerate(df.columns):
            with cols[i%3]:
                st.markdown(f"""
                    <div class="glass-card" style="margin-bottom:15px;">
                        <div class="stat-label">{col}</div>
                        <div class="stat-value">{item[col]}</div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        # شريط البحث الأنيق
        s_col1, s_col2 = st.columns([3, 1])
        with s_col1: search = st.text_input("🔍 ابحث عن (مشروع، مطور، منطقة)...", placeholder="اكتب هنا...")
        with s_col2: 
            locs = ["الكل"] + sorted(df['Location'].unique().tolist()) if 'Location' in df.columns else ["الكل"]
            sel_loc = st.selectbox("📍 الموقع", locs)

        # فلترة
        filtered = df.copy()
        if search: filtered = filtered[filtered.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_loc != "الكل": filtered = filtered[filtered['Location'] == sel_loc]

        # العرض في كروت حديثة
        cols = st.columns(2)
        for i, (idx, row) in enumerate(filtered.iterrows()):
            with cols[i%2]:
                st.markdown(f"""
                    <div class="glass-card" style="margin-bottom:20px;">
                        <h3 style="color:{GOLD_COLOR}; margin-bottom:10px;">{row[0]}</h3>
                        <p style="color:#ccc; font-size:0.9rem;">📍 {row.get('Location','---')}</p>
                        <p style="color:white; font-weight:bold; font-size:1.1rem;">💰 {row.get('Price','اتصل للسعر')}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("عرض التفاصيل", key=f"btn_{prefix}_{idx}"):
                    st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"
                    st.rerun()

# --- 9. تبديل الأقسام ---
if menu == "أدوات الحساب":
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='glass-card' style='border-top:5px solid {GOLD_COLOR}'><h3>💰 حاسبة القسط</h3>", unsafe_allow_html=True)
        pr = st.number_input("السعر الإجمالي", value=5000000)
        dp = st.slider("المقدم (%)", 0, 50, 10)
        yr = st.number_input("السنوات", value=8)
        monthly = (pr * (1 - dp/100)) / (yr * 12) if yr > 0 else 0
        st.markdown(f"<h2 style='color:{GOLD_COLOR}'>{monthly:,.0f} ج.م</h2><p>قسط شهري</p></div>", unsafe_allow_html=True)
    # باقي الأدوات تتبع نفس النمط...

elif menu == "المشاريع":
    tabs = st.tabs(["🏗️ المشروعات الحالية", "🚀 انطلاقات جديدة"])
    with tabs[0]: render_modern_grid(df_p, "p")
    with tabs[1]: render_modern_grid(df_l, "l")

elif menu == "المطورين":
    render_modern_grid(df_d, "d")

elif menu == "المساعد الذكي":
    st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding:100px;">
            <h1 style="font-size:5rem;">🤖</h1>
            <h2>MA3LOMATI AI</h2>
            <p>ذكاء اصطناعي عقاري لتحليل الاتجاهات (قيد التجهيز)</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown(f"<p style='text-align:center; color:#555; margin-top:100px;'>MA3LOMATI PRO VERSION 4.0 | 2026</p>", unsafe_allow_html=True)
