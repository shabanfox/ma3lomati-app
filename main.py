import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الثوابت والألوان (تعريف المتغيرات لتجنب الـ NameError) ---
GOLD_COLOR = "#D4AF37"
GOLD_GRADIENT = "linear-gradient(135deg, #D4AF37 0%, #F9E29C 50%, #B8860B 100%)"
DARK_BG = "radial-gradient(circle at top right, #1a1a1a, #000000)"
DARK_GLASS = "rgba(255, 255, 255, 0.03)"

# --- 3. إدارة حالة الجلسة (Session State) ---
if 'auth' not in st.session_state:
    if "u_session" in st.query_params:
        st.session_state.auth, st.session_state.current_user = True, st.query_params["u_session"]
    else: st.session_state.auth = False

if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0

# --- 4. الروابط التقنية ---
URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"

# --- 5. وظيفة تحميل البيانات ---
@st.cache_data(ttl=60)
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

# --- 6. التصميم الاحترافي (Advanced Modern UI) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;700;900&display=swap');
    
    * {{ font-family: 'Cairo', sans-serif; }}
    
    [data-testid="stAppViewContainer"] {{
        background: {DARK_BG};
        color: white; direction: rtl; text-align: right;
    }}
    
    header {{ visibility: hidden; }}

    /* الهيدر المودرن */
    .main-header {{
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(15px);
        padding: 30px; border-radius: 0 0 40px 40px;
        border-bottom: 1px solid {GOLD_COLOR}44;
        text-align: center; margin-bottom: 30px;
    }}

    /* الكروت الزجاجية العصرية */
    .modern-card {{
        background: {DARK_GLASS};
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px; padding: 25px;
        transition: all 0.4s ease; margin-bottom: 20px;
    }}
    .modern-card:hover {{
        border: 1px solid {GOLD_COLOR}88;
        transform: translateY(-8px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.4);
    }}

    /* الأزرار الذهبية المعدنية */
    div.stButton > button {{
        background: {GOLD_GRADIENT} !important;
        color: black !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 900 !important;
        transition: 0.3s !important;
        width: 100%; height: 45px;
    }}
    div.stButton > button:hover {{
        transform: scale(1.02) !important;
        box-shadow: 0 0 20px {GOLD_COLOR}66 !important;
    }}

    /* زر الخروج الأحمر */
    .logout-section button {{
        background: rgba(255, 75, 75, 0.1) !important;
        color: #ff4b4b !important;
        border: 1px solid #ff4b4b !important;
    }}

    /* تفاصيل المحتوى */
    .label-gold {{ color: {GOLD_COLOR}; font-weight: 700; font-size: 0.9rem; }}
    .value-white {{ color: white; font-size: 1.1rem; }}
    </style>
""", unsafe_allow_html=True)

# --- 7. بوابة الدخول ---
if not st.session_state.get('auth', False):
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col_m, _ = st.columns([1, 1.3, 1])
    with col_m:
        st.markdown(f"""
            <div style="background:{DARK_GLASS}; padding:40px; border-radius:30px; border:1px solid {GOLD_COLOR}33; text-align:center;">
                <h1 style="background:{GOLD_GRADIENT}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight:900; font-size:3rem;">MA3LOMATI</h1>
                <p style="color:#888; letter-spacing:2px;">PRO ACCESS 2026</p>
            </div><br>
        """, unsafe_allow_html=True)
        u = st.text_input("Username", key="login_u")
        p = st.text_input("Security Key", type="password", key="login_p")
        if st.button("UNLOCK SYSTEM 🔓"):
            if p == "2026":
                st.session_state.auth, st.session_state.current_user = True, u
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 8. المحتوى الرئيسي ---
df_p, df_d, df_l = load_data()

# عرض الهيدر وزر الخروج
head_c1, head_c2 = st.columns([0.8, 0.2])
with head_c1:
    st.markdown(f"""<div class="main-header">
        <h1 style="background:{GOLD_GRADIENT}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0; font-weight:900;">MA3LOMATI PRO</h1>
        <p style="color:#666; margin:0;">مرحباً بك، {st.session_state.current_user} | عقارات المستقبل</p>
    </div>""", unsafe_allow_html=True)
with head_c2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("تسجيل الخروج", key="logout"):
        st.session_state.auth = False
        st.rerun()

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "search", "robot"], 
    default_index=2, orientation="horizontal",
    styles={
        "container": {"background-color": "transparent", "border": f"1px solid {GOLD_COLOR}33", "border-radius": "15px"},
        "nav-link": {"color": "#888", "font-size": "16px"},
        "nav-link-selected": {"background": GOLD_GRADIENT, "color": "black", "font-weight": "900"}
    })

# --- 9. دالة العرض المودرن ---
def render_modern_grid(df, prefix):
    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}"): 
            st.session_state.view = "grid"; st.rerun()
        
        item = df.iloc[st.session_state.current_index]
        st.markdown(f"<h2 style='color:{GOLD_COLOR};'>🏠 {item.iloc[0]}</h2>", unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, col_name in enumerate(df.columns):
            with cols[i%3]:
                st.markdown(f"""<div class="modern-card">
                    <p class="label-gold">{col_name}</p>
                    <p class="value-white">{item[col_name]}</p>
                </div>""", unsafe_allow_html=True)
    else:
        # البحث والفلترة
        f1, f2 = st.columns([3, 1])
        with f1: search = st.text_input("🔍 بحث ذكي...", key=f"search_{prefix}", placeholder="اسم المشروع، المطور، الموقع...")
        with f2:
            locs = ["الكل"] + sorted(df['Location'].unique().tolist()) if 'Location' in df.columns else ["الكل"]
            sel_loc = st.selectbox("📍 الموقع", locs, key=f"loc_{prefix}")

        filt = df.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_loc != "الكل": filt = filt[filt['Location'] == sel_loc]

        grid = st.columns(2)
        for i, (idx, row) in enumerate(filt.iterrows()):
            with grid[i%2]:
                st.markdown(f"""<div class="modern-card">
                    <h3 style="color:{GOLD_COLOR}; margin:0;">{row[0]}</h3>
                    <p style="color:#888; margin:5px 0;">📍 {row.get('Location','---')}</p>
                    <p style="font-weight:bold; font-size:1.2rem;">💰 {row.get('Price','اتصل للسعر')}</p>
                </div>""", unsafe_allow_html=True)
                if st.button("عرض التفاصيل", key=f"btn_{prefix}_{idx}"):
                    st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"
                    st.rerun()

# --- 10. الأقسام ---
if menu == "أدوات الحساب":
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='modern-card'><h3>💰 القسط</h3>", unsafe_allow_html=True)
        pr = st.number_input("السعر الإجمالي", value=5000000)
        yr = st.number_input("السنوات", value=8)
        res = (pr * 0.9) / (yr * 12) if yr > 0 else 0
        st.markdown(f"<h2 style='color:{GOLD_COLOR}'>{res:,.0f} ج.م</h2></div>", unsafe_allow_html=True)
    # باقي الأدوات تتبع نفس النمط...

elif menu == "المشاريع":
    tabs = st.tabs(["🏗️ المشروعات الحالية", "🚀 اللونشات الجديدة"])
    with tabs[0]: render_modern_grid(df_p, "p")
    with tabs[1]: render_modern_grid(df_l, "l")

elif menu == "المطورين":
    render_modern_grid(df_d, "d")

elif menu == "المساعد الذكي":
    st.markdown(f"<div class='modern-card' style='text-align:center;'><h1>🤖</h1><h2>MA3LOMATI AI</h2><p>نظام تحليل البيانات العقارية قيد التطوير</p></div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
