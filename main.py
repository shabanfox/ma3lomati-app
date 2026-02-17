import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة الثيم (التبديل بين الذهبي والافتراضي) ---
if 'theme' not in st.session_state:
    st.session_state.theme = "Gold"  # الثيم الافتراضي عند الفتح

# --- 3. إدارة حالة الجلسة والروابط (كما هي تماماً) ---
if 'auth' not in st.session_state:
    st.session_state.auth = "u_session" in st.query_params
    st.session_state.current_user = st.query_params.get("u_session", "Guest")

if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0

URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# --- 4. محرك التصميم الديناميكي ---
def apply_theme():
    GOLD_GRADIENT = "linear-gradient(135deg, #D4AF37 0%, #F9E29C 50%, #B8860B 100%)"
    
    if st.session_state.theme == "Gold":
        # تصميم الكود الذهبي (المودرن)
        st.markdown(f"""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
            [data-testid="stAppViewContainer"] {{ background-color: #0a0a0a !important; color: white !important; direction: rtl !important; font-family: 'Cairo' !important; }}
            .modern-card {{ background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 15px; padding: 20px; margin-bottom: 10px; text-align: right; }}
            div.stButton > button {{ background: {GOLD_GRADIENT} !important; color: black !important; border: none !important; border-radius: 10px !important; font-weight: 900 !important; width: 100% !important; }}
            .stTabs [aria-selected="true"] {{ background: {GOLD_GRADIENT} !important; color: black !important; font-weight: bold; }}
            header, [data-testid="stHeader"] {{ visibility: hidden; }}
            </style>
        """, unsafe_allow_html=True)
    else:
        # تصميم الكود القديم (الافتراضي)
        st.markdown("""
            <style>
            [data-testid="stAppViewContainer"] { background-color: white !important; color: black !important; direction: rtl !important; }
            .modern-card { border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 10px; }
            /* نرجع الأزرار لشكلها العادي الرمادي */
            div.stButton > button { background-color: #f0f2f6 !important; color: black !important; border: 1px solid #ccc !important; }
            header, [data-testid="stHeader"] { visibility: visible; }
            </style>
        """, unsafe_allow_html=True)

apply_theme()

# --- 5. بوابة الدخول ---
if not st.session_state.auth:
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.title("تسجيل الدخول")
        u = st.text_input("User")
        p = st.text_input("Pass", type="password")
        if st.button("دخول"):
            if p == "2026": 
                st.session_state.auth = True; st.rerun()
            else: st.error("خطأ!")
    st.stop()

# --- 6. شريط التحكم العلوي (تبديل الشكل) ---
t_col1, t_col2 = st.columns([8, 2])
with t_col2:
    theme_choice = st.toggle("تفعيل الوضع الذهبي ✨", value=(st.session_state.theme == "Gold"))
    new_theme = "Gold" if theme_choice else "Classic"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

# --- 7. عرض البيانات (نفس المنطق بتاعك) ---
@st.cache_data(ttl=60)
def load_data():
    try:
        p = pd.read_csv(URL_PROJECTS).fillna("---")
        d = pd.read_csv(URL_DEVELOPERS).fillna("---")
        l = pd.read_csv(URL_LAUNCHES).fillna("---")
        return p, d, l
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# الهيدر
title_color = "#D4AF37" if st.session_state.theme == "Gold" else "#000"
st.markdown(f"<h1 style='text-align:center; color:{title_color};'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)

menu = option_menu(None, ["المشاريع", "المطورين", "أدوات الحساب"], 
    icons=["search", "building", "calculator"], orientation="horizontal")

if menu == "المشاريع":
    # عرض المشاريع
    search = st.text_input("🔍 ابحث...")
    grid = st.columns(2)
    # مثال لعرض أول 4 مشاريع
    for i, (idx, r) in enumerate(df_p.head(4).iterrows()):
        with grid[i%2]:
            st.markdown(f"""
                <div class="modern-card">
                    <h3>🏢 {r.iloc[0]}</h3>
                    <p>الموقع: {r.get('Area','---')}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"تفاصيل {r.iloc[0]}", key=f"btn_{idx}"):
                st.info(f"فتح تفاصيل: {r.iloc[0]}")

elif menu == "أدوات الحساب":
    st.subheader("🧮 حاسبة القروض")
    st.number_input("السعر")
    st.button("احسب")

st.markdown(f"<p style='text-align:center; opacity:0.5;'>MA3LOMATI {st.session_state.theme} Edition</p>", unsafe_allow_html=True)
