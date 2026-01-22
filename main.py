import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة وإلغاء الهوامش ---
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

# --- 4. التنسيق الجمالي المتطور (CSS) ---
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
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }

    /* كروت احترافية بتفاصيل غنية */
    div.stButton > button[key*="card_"] {
        background: rgba(20, 20, 20, 0.85) !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-top: 4px solid #f59e0b !important; /* لمسة ذهبية علوية */
        border-radius: 15px !important;
        min-height: 140px !important;
        width: 100% !important;
        transition: 0.4s all ease;
        line-height: 1.6 !important;
        font-size: 16px !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: #f59e0b !important;
        box-shadow: 0 10px 25px rgba(245, 158, 11, 0.3) !important;
        background: rgba(30, 30, 30, 0.95) !important;
    }

    .info-card { 
        background: rgba(255,255,255,0.03); 
        padding: 30px; border-radius: 25px; 
        border: 1px solid #222; backdrop-filter: blur(10px);
    }
    
    .label-gold { color: #f59e0b; font-weight: 900; letter-spacing: 1px; }

    /* زر الخروج اليساري */
    .stButton > button[key="logout_btn"] {
        background: transparent !important; color: #ff4b4b !important;
        border: 1px solid #ff4b4b !important; border-radius: 12px !important;
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

# --- 6. صفحة الدخول ---
if not st.session_state.auth:
    _, col_login, _ = st.columns([1, 1.2, 1])
    with col_login:
        st.markdown("<div style='height:150px;'></div>", unsafe_allow_html=True)
        st.markdown("<div class='info-card' style='text-align:center;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
        p_in = st.text_input("كلمة مرور النظام", type="password")
        if st.button("دخول للمنصة الملكية", use_container_width=True):
            if p_in == "2026": st.session_state.auth = True; st.rerun()
            else: st.error("غير مصرح بالدخول")
    st.stop()

# --- 7. الواجهة الرئيسية ---
df_p, df_d, df_l = load_all_data()

st.markdown("""
    <div class="royal-header">
        <h1 style="color: #f59e0b; font-size: 55px; margin: 0; font-weight: 900; text-shadow: 2px 2px 10px rgba(0,0,0,0.5);">MA3LOMATI</h1>
        <p style="color: #aaa; letter-spacing: 6px; font-size: 16px;">THE NEXT GENERATION OF REAL ESTATE</p>
    </div>
""", unsafe_allow_html=True)

col_logout, col_menu = st.columns([0.15, 0.85])
with col_logout:
    if st.button("🚪 خروج", key="logout_btn", use_container_width=True):
        st.session_state.auth = False; st.rerun()
with col_menu:
    menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], 
        default_index=4, orientation="horizontal",
        styles={"nav-link": {"font-weight": "bold", "color": "white", "font-size": "18px"},
                "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if menu != st.session_state.last_menu:
    st.session_state.selected_item = None; st.session_state.last_menu = menu

# --- 8. المحتوى الرئيسي ---

if st.session_state.selected_item is not None:
    it = st.session_state.selected_item
    if st.button("⬅️ عودة للقائمة الرئيسية"):
        st.session_state.selected_item = None; st.rerun()
    
    c_main, c_side = st.columns([0.7, 0.3])
    with c_main:
        st.markdown(f"""<div class="info-card">
            <h1 style="color:#f59e0b; font-size:40px;">{it.get('ProjectName', it.get('Project', it.get('Developer')))}</h1>
            <hr style="opacity:0.1; margin: 20px 0;">
            <p class="label-gold">📍 الموقع الجغرافي</p><h3>{it.get('Location','---')}</h3>
            <p class="label-gold">🌟 لماذا هذا المشروع؟ (USP)</p>
            <p style="font-size:20px; line-height:1.8; color:#ddd;">{it.get('Unique Selling Points (USP)', it.get('Notes','---'))}</p>
        </div>""", unsafe_allow_html=True)
    with c_side:
        st.markdown(f"""<div class="info-card">
            <p class="label-gold">💰 أنظمة السداد</p><h3>{it.get('Price & Payment','---')}</h3>
            <hr style="opacity:0.1">
            <p class="label-gold">🏢 الشركة المطورة</p><h4>{it.get('Developer','---')}</h4>
            <p class="label-gold">⭐ فئة المطور</p><h4>{it.get('Developer Category','A+')}</h4>
        </div>""", unsafe_allow_html=True)

else:
    if menu == "اللونشات":
        st.markdown("<h3 style='color:#f59e0b; margin-right:20px;'>🚀 انطلاقات حصرية 2026</h3>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, r in df_l.iterrows():
            with cols[i % 3]:
                # كارت غني بالبيانات وشكله أجمل
                btn_text = f"🔥 {r['Project']}\n🏢 {r['Developer']}\n📍 {r['Location']}"
                if st.button(btn_text, key=f"card_l_{i}"):
                    st.session_state.selected_item = r; st.rerun()

    elif menu == "المشاريع":
        c_m, c_s = st.columns([0.7, 0.3])
        with c_s:
            st.markdown("<div class='info-card'><h4>🔍 فلترة ذكية</h4>", unsafe_allow_html=True)
            search = st.text_input("ابحث باسم المشروع أو المنطقة")
            st.markdown("</div>", unsafe_allow_html=True)
        with c_m:
            dff = df_p[df_p['ProjectName'].str.contains(search, case=False) | df_p['Location'].str.contains(search, case=False)] if search else df_p
            grid = st.columns(2)
            for i, r in dff.head(10).reset_index().iterrows():
                with grid[i % 2]:
                    if st.button(f"🏗️ {r['ProjectName']}\n📍 {r['Location']}\n🏢 {r['Developer']}", key=f"card_p_{i}"):
                        st.session_state.selected_item = r; st.rerun()

    elif menu == "المطورين":
        c_m, c_s = st.columns([0.7, 0.3])
        with c_s:
            st.markdown("<div class='info-card'><h4>🏆 شركاء النجاح</h4><p>كبار المطورين في السوق المصري</p></div>", unsafe_allow_html=True)
            search_d = st.text_input("ابحث عن شركة مطورة")
        with c_m:
            dfd = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
            grid_d = st.columns(2)
            for i, r in dfd.head(10).reset_index().iterrows():
                with grid_d[i % 2]:
                    if st.button(f"🏆 {r['Developer']}\n⭐ الفئة: {r.get('Developer Category','A')}", key=f"card_d_{i}"):
                        st.session_state.selected_item = r; st.rerun()

    elif menu == "المساعد الذكي":
        st.markdown("<div class='info-card' style='max-width:800px; margin:auto;'><h2>🤖 المساعد العقاري الذكي</h2><p>قيد التطوير لربط طلبات عملائك بأفضل الفرص المتاحة...</p></div>", unsafe_allow_html=True)

    elif menu == "أدوات البروكر":
        st.markdown("<div class='info-card'><h3>🛠️ حقيبة الأدوات الحسابية</h3>", unsafe_allow_html=True)
        price = st.number_input("سعر الوحدة الإجمالي", 1000000, step=100000)
        years = st.slider("مدة التقسيط (سنوات)", 1, 15, 8)
        st.metric("قيمة القسط الشهري", f"{price/(years*12):,.0f} EGP")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br><p style='text-align:center; color:#444; font-weight:bold;'>MA3LOMATI PRO © 2026 | PREMIUM EXPERIENCE</p>", unsafe_allow_html=True)
