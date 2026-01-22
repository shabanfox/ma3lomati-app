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

# --- 4. التنسيق الجمالي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0rem !important; }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
        url('https://images.unsplash.com/photo-1449824913935-59a10b8d2000?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }

    .royal-header {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border-bottom: 3px solid #f59e0b;
        padding: 40px; text-align: center;
        border-radius: 0 0 60px 60px; margin-bottom: 30px;
    }

    div.stButton > button[key*="card_"] {
        background: rgba(20, 20, 20, 0.85) !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-top: 4px solid #f59e0b !important;
        border-radius: 15px !important;
        min-height: 140px !important;
        width: 100% !important;
        transition: 0.4s all ease;
        line-height: 1.6 !important;
        font-size: 16px !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-8px);
        border-color: #f59e0b !important;
        box-shadow: 0 10px 25px rgba(245, 158, 11, 0.3) !important;
    }

    .info-card { 
        background: rgba(255,255,255,0.03); 
        padding: 30px; border-radius: 25px; 
        border: 1px solid #222;
    }
    
    .label-gold { color: #f59e0b; font-weight: 900; }

    /* تنسيق زر الخروج اليميني */
    .stButton > button[key="logout_btn"] {
        background: rgba(255, 75, 75, 0.1) !important; 
        color: #ff4b4b !important;
        border: 1px solid #ff4b4b !important; 
        border-radius: 12px !important;
        font-weight: bold !important;
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
        st.markdown("<div class='info-card' style='text-align:center;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
        p_in = st.text_input("كلمة المرور", type="password")
        if st.button("دخول", use_container_width=True):
            if p_in == "2026": st.session_state.auth = True; st.rerun()
            else: st.error("خطأ")
    st.stop()

# --- 7. الواجهة الرئيسية ---
df_p, df_d, df_l = load_all_data()

st.markdown("""
    <div class="royal-header">
        <h1 style="color: #f59e0b; font-size: 55px; margin: 0; font-weight: 900;">MA3LOMATI</h1>
        <p style="color: #aaa; letter-spacing: 6px; font-size: 16px;">THE REAL ESTATE INTELLIGENCE</p>
    </div>
""", unsafe_allow_html=True)

# تعديل الترتيب ليصبح زر الخروج في اليمين (أول عمود في نظام الـ RTL)
col_menu, col_logout = st.columns([0.85, 0.15])
with col_logout:
    if st.button("🚪 خروج", key="logout_btn", use_container_width=True):
        st.session_state.auth = False; st.rerun()
with col_menu:
    menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], 
        default_index=4, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if menu != st.session_state.last_menu:
    st.session_state.selected_item = None; st.session_state.last_menu = menu

# --- 8. العرض ---

if st.session_state.selected_item is not None:
    it = st.session_state.selected_item
    if st.button("⬅️ عودة"):
        st.session_state.selected_item = None; st.rerun()
    
    c1, c2 = st.columns([0.7, 0.3])
    with c1:
        st.markdown(f"""<div class="info-card">
            <h1 style="color:#f59e0b;">{it.get('ProjectName', it.get('Project', it.get('Developer')))}</h1>
            <hr style="opacity:0.1">
            <p class="label-gold">📍 الموقع</p><h3>{it.get('Location','---')}</h3>
            <p class="label-gold">🌟 التفاصيل</p><p style="font-size:20px;">{it.get('Unique Selling Points (USP)', it.get('Notes','---'))}</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="info-card">
            <p class="label-gold">💰 السعر والسداد</p><h4>{it.get('Price & Payment','---')}</h4>
            <p class="label-gold">🏢 المطور</p><h4>{it.get('Developer','---')}</h4>
        </div>""", unsafe_allow_html=True)

else:
    if menu == "اللونشات":
        cols = st.columns(3)
        for i, r in df_l.iterrows():
            with cols[i % 3]:
                if st.button(f"🔥 {r['Project']}\n🏢 {r['Developer']}\n📍 {r['Location']}", key=f"card_l_{i}"):
                    st.session_state.selected_item = r; st.rerun()

    elif menu == "المشاريع":
        c_m, c_s = st.columns([0.7, 0.3])
        with c_s:
            st.markdown("<div class='info-card'><h4>🔍 بحث</h4>", unsafe_allow_html=True)
            search = st.text_input("اسم المشروع أو المنطقة")
            st.markdown("</div>", unsafe_allow_html=True)
        with c_m:
            dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
            grid = st.columns(2)
            for i, r in dff.head(10).reset_index().iterrows():
                with grid[i % 2]:
                    if st.button(f"🏗️ {r['ProjectName']}\n📍 {r['Location']}\n🏢 {r['Developer']}", key=f"card_p_{i}"):
                        st.session_state.selected_item = r; st.rerun()

    elif menu == "المطورين":
        c_m, c_s = st.columns([0.7, 0.3])
        with c_s:
            st.markdown("<div class='info-card'><h4>🏢 الشركات</h4></div>", unsafe_allow_html=True)
            search_d = st.text_input("اسم المطور")
        with c_m:
            dfd = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
            grid_d = st.columns(2)
            for i, r in dfd.head(10).reset_index().iterrows():
                with grid_d[i % 2]:
                    if st.button(f"🏆 {r['Developer']}\n⭐ الفئة: {r.get('Developer Category','A')}", key=f"card_d_{i}"):
                        st.session_state.selected_item = r; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
