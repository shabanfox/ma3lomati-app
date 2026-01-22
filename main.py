import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. روابط البيانات ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
URL_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'last_menu' not in st.session_state: st.session_state.last_menu = "اللونشات"

# --- 4. التنسيق الجمالي (CSS) لتوحيد أحجام الكروت ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0rem !important; }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
        url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }

    .royal-header {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border-bottom: 2px solid #f59e0b;
        padding: 25px; text-align: center;
        border-radius: 0 0 40px 40px; margin-bottom: 20px;
    }

    /* توحيد حجم الكروت تماماً */
    div.stButton > button[key*="card_"] {
        background: rgba(30, 30, 30, 0.9) !important;
        color: #f59e0b !important; 
        border: 1px solid #444 !important;
        border-radius: 12px !important; 
        
        /* الأبعاد الثابتة هنا */
        height: 100px !important; 
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        
        font-size: 16px !important;
        font-weight: 700 !important;
        overflow: hidden !important;
        transition: 0.3s;
    }
    
    div.stButton > button:hover { 
        background: #f59e0b !important; 
        color: black !important;
        border-color: #f59e0b !important;
    }

    .info-card { background: rgba(0,0,0,0.7); padding: 25px; border-radius: 20px; border: 1px solid #333; }
    .label-gold { color: #f59e0b; font-weight: bold; }
    
    .stButton > button[key="logout_btn"] {
        background-color: transparent !important; color: #ff4b4b !important;
        border: 1px solid #ff4b4b !important; border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. وظائف البيانات ---
@st.cache_data(ttl=60)
def load_all_data():
    try:
        p = pd.read_csv(URL_P).fillna("---")
        d = pd.read_csv(URL_D).fillna("---")
        l = pd.read_csv(URL_L).fillna("---")
        for df in [p, d, l]: df.columns = df.columns.str.strip()
        p.rename(columns={'Area': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d, l
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 6. الدخول ---
if not st.session_state.auth:
    _, col_login, _ = st.columns([1, 1.2, 1])
    with col_login:
        st.markdown("<div style='height:150px;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='info-card' style='text-align:center;'><h2 style='color:#f59e0b;'>MA3LOMATI PRO</h2>", unsafe_allow_html=True)
        p_in = st.text_input("كلمة المرور", type="password")
        if st.button("دخول", use_container_width=True):
            if p_in == "2026": st.session_state.auth = True; st.rerun()
            else: st.error("خطأ")
    st.stop()

# --- 7. الواجهة ---
df_p, df_d, df_l = load_all_data()

st.markdown("""
    <div class="royal-header">
        <h1 style="color: #f59e0b; font-size: 45px; margin: 0; font-weight: 900;">MA3LOMATI</h1>
        <p style="color: #eee; letter-spacing: 4px; font-size: 14px;">REAL ESTATE INTELLIGENCE</p>
    </div>
""", unsafe_allow_html=True)

col_logout, col_menu = st.columns([0.15, 0.85])
with col_logout:
    if st.button("🚪 خروج", key="logout_btn", use_container_width=True):
        st.session_state.auth = False; st.rerun()
with col_menu:
    menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], 
        default_index=4, orientation="horizontal",
        styles={"nav-link": {"font-weight": "bold", "color": "white"},
                "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if menu != st.session_state.last_menu:
    st.session_state.selected_item = None; st.session_state.last_menu = menu

# --- 8. العرض ---

if st.session_state.selected_item is not None:
    it = st.session_state.selected_item
    if st.button("⬅️ عودة للقائمة"):
        st.session_state.selected_item = None; st.rerun()
    
    c1, c2 = st.columns([0.7, 0.3])
    with c1:
        st.markdown(f"""<div class="info-card">
            <h1 style="color:#f59e0b;">{it.get('ProjectName', it.get('Project', it.get('Developer')))}</h1>
            <hr style="opacity:0.2">
            <p class="label-gold">📍 الموقع</p><h3>{it.get('Location','---')}</h3>
            <p class="label-gold">🌟 التفاصيل</p><p style="font-size:18px;">{it.get('Unique Selling Points (USP)', it.get('Notes','---'))}</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="info-card">
            <p class="label-gold">💰 السعر والسداد</p><h4>{it.get('Price & Payment','---')}</h4>
            <p class="label-gold">🏢 المطور</p><h4>{it.get('Developer','---')}</h4>
        </div>""", unsafe_allow_html=True)

else:
    if menu == "اللونشات":
        st.markdown("<h4 style='color:#f59e0b;'>🚀 أحدث اللونشات</h4>", unsafe_allow_html=True)
        # تقسيم الشبكة لـ 4 أعمدة متساوية
        grid_l = st.columns(4)
        for i, r in df_l.iterrows():
            with grid_l[i % 4]:
                if st.button(f"{r['Project']}", key=f"card_l_{i}"):
                    st.session_state.selected_item = r; st.rerun()

    elif menu == "المشاريع":
        c_m, c_s = st.columns([0.7, 0.3])
        with c_s:
            st.markdown("<div class='info-card'><h4>🔍 بحث سريع</h4>", unsafe_allow_html=True)
            search = st.text_input("اسم المشروع")
            st.markdown("</div>", unsafe_allow_html=True)
        with c_m:
            dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
            # 3 أعمدة متساوية تماماً في المساحة المتاحة
            grid_p = st.columns(3)
            for i, r in dff.head(15).reset_index().iterrows():
                with grid_p[i % 3]:
                    if st.button(f"{r['ProjectName']}", key=f"card_p_{i}"):
                        st.session_state.selected_item = r; st.rerun()

    elif menu == "المطورين":
        c_m, c_s = st.columns([0.7, 0.3])
        with c_s:
            st.markdown("<div class='info-card'><h4>🏢 الشركات</h4></div>", unsafe_allow_html=True)
            search_d = st.text_input("اسم المطور")
        with c_m:
            dfd = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
            grid_d = st.columns(3)
            for i, r in dfd.head(15).reset_index().iterrows():
                with grid_d[i % 3]:
                    if st.button(f"{r['Developer']}", key=f"card_d_{i}"):
                        st.session_state.selected_item = r; st.rerun()

    elif menu == "المساعد الذكي":
        st.markdown("<div class='info-card' style='max-width:800px; margin:auto;'><h2>🤖 المساعد الذكي</h2><p>سيتم ربط الطلبات قريباً...</p></div>", unsafe_allow_html=True)

    elif menu == "أدوات البروكر":
        st.markdown("<div class='info-card'><h3>🛠️ الحاسبة العقارية</h3><p>جاهزة للعمل...</p></div>", unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#555;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
