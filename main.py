import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. روابط البيانات ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
URL_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"

# --- 3. إدارة الحالة (Session State) ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'last_menu' not in st.session_state: st.session_state.last_menu = "اللونشات"

# --- 4. التنسيق الجمالي الاحترافي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* خلفية هادئة وفخمة */
    [data-testid="stAppViewContainer"] {
        background-color: #0a0a0a;
        background-image: radial-gradient(circle at 50% 50%, #1a1a1a 0%, #0a0a0a 100%);
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }

    /* هيدر ملكي */
    .royal-header {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(15px);
        border-bottom: 2px solid #f59e0b;
        padding: 35px 20px;
        text-align: center;
        border-radius: 0 0 40px 40px;
        margin-bottom: 25px;
    }

    /* كروت الأزرار */
    div.stButton > button[key*="card_"] {
        background: rgba(30, 30, 30, 0.7) !important;
        color: #e0e0e0 !important;
        border: 1px solid #333 !important;
        border-right: 5px solid #f59e0b !important;
        border-radius: 12px !important;
        min-height: 120px !important;
        font-weight: bold !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        background: rgba(245, 158, 11, 0.15) !important;
        border-color: #f59e0b !important;
        transform: translateY(-3px);
    }

    .info-card {
        background: rgba(255,255,255,0.03);
        padding: 25px; border-radius: 20px;
        border: 1px solid #222;
    }
    
    .label-gold { color: #f59e0b; font-size: 14px; font-weight: bold; margin-bottom: 5px; }
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
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d, l
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def login_user(u, p):
    if p == "2026": return "Admin"
    try:
        r = requests.get(f"{SCRIPT_URL}?nocache={time.time()}")
        if r.status_code == 200:
            for user in r.json():
                name = str(user.get('Name','')).strip()
                email = str(user.get('Email','')).strip().lower()
                password = str(user.get('Password','')).strip()
                if (u.lower() == email or u == name) and str(p) == password:
                    return name
    except: pass
    return None

# --- 6. صفحة الدخول ---
if not st.session_state.auth:
    _, col_login, _ = st.columns([1, 1.2, 1])
    with col_login:
        st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
        u_in = st.text_input("اسم المستخدم")
        p_in = st.text_input("كلمة المرور", type="password")
        if st.button("دخول آمن", use_container_width=True):
            user = login_user(u_in, p_in)
            if user:
                st.session_state.auth = True
                st.session_state.current_user = user
                st.rerun()
            else: st.error("بيانات الدخول خاطئة")
    st.stop()

# --- 7. الواجهة الرئيسية ---
df_p, df_d, df_l = load_all_data()

# الهيدر
st.markdown(f"""
    <div class="royal-header">
        <h1 style="color: #f59e0b; font-size: 45px; margin: 0;">MA3LOMATI PRO</h1>
        <p style="color: #888; font-size: 14px; letter-spacing: 3px;">نظام الإدارة العقارية الذكي 2026</p>
    </div>
""", unsafe_allow_html=True)

# المنيو وزر الخروج (الخروج يسار)
col_logout, col_menu = st.columns([0.15, 0.85])
with col_logout:
    if st.button("🚪 خروج", use_container_width=True):
        st.session_state.auth = False
        st.rerun()
with col_menu:
    menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], 
        icons=["briefcase", "building", "search", "robot", "rocket"], 
        default_index=4, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if menu != st.session_state.last_menu:
    st.session_state.selected_item = None
    st.session_state.last_menu = menu

# --- 8. المحتوى ---
if st.session_state.selected_item is not None:
    it = st.session_state.selected_item
    if st.button("⬅️ عودة"):
        st.session_state.selected_item = None
        st.rerun()
    
    c_m, c_s = st.columns([0.7, 0.3])
    with c_m:
        st.markdown(f"""<div class="info-card">
            <h2 style="color:#f59e0b;">{it.get('ProjectName', it.get('Project', it.get('Developer')))}</h2>
            <hr style="opacity:0.1">
            <p class="label-gold">📍 الموقع</p><h3>{it.get('Location','---')}</h3>
            <p class="label-gold">🌟 تفاصيل المشروع</p>
            <p style="font-size:18px;">{it.get('Unique Selling Points (USP)', it.get('Notes','---'))}</p>
        </div>""", unsafe_allow_html=True)
    with c_s:
        st.markdown(f"""<div class="info-card">
            <p class="label-gold">💰 نظام السداد</p><h3>{it.get('Price & Payment','---')}</h3>
            <p class="label-gold">🏢 المطور</p><h4>{it.get('Developer','---')}</h4>
        </div>""", unsafe_allow_html=True)

else:
    if menu == "اللونشات":
        cols = st.columns(3)
        for i, r in df_l.iterrows():
            with cols[i % 3]:
                if st.button(f"🚀 {r['Developer']}\n{r['Project']}\n📍 {r['Location']}", key=f"card_l_{i}"):
                    st.session_state.selected_item = r; st.rerun()

    elif menu == "المشاريع":
        c_m, c_s = st.columns([0.7, 0.3])
        with c_s:
            st.markdown("<div class='info-card'><h4>🔍 بحث</h4>", unsafe_allow_html=True)
            search = st.text_input("اسم المشروع")
            st.markdown("</div>", unsafe_allow_html=True)
        with c_m:
            dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
            grid = st.columns(2)
            for i, r in dff.head(10).reset_index().iterrows():
                with grid[i % 2]:
                    if st.button(f"🏗️ {r['ProjectName']}\n📍 {r['Location']}", key=f"card_p_{i}"):
                        st.session_state.selected_item = r; st.rerun()

    elif menu == "المطورين":
        c_m, c_s = st.columns([0.7, 0.3])
        with c_s:
            st.markdown("<div class='info-card'><h4>🏢 الشركات</h4><p>ترتيب حسب القوة</p></div>", unsafe_allow_html=True)
            search_d = st.text_input("اسم المطور")
        with c_m:
            dfd = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
            grid = st.columns(2)
            for i, r in dfd.head(10).reset_index().iterrows():
                with grid[i % 2
