import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الثوابت التصميمية (الذهب الملكي) ---
GOLD_COLOR = "#D4AF37"
GOLD_GRADIENT = "linear-gradient(135deg, #D4AF37 0%, #F9E29C 50%, #B8860B 100%)"

# --- 3. إدارة الجلسة والبيانات ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'view' not in st.session_state: st.session_state.view = "grid"

URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sb?gid=732423049&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        p = pd.read_csv(URL_PROJECTS).fillna("---")
        d = pd.read_csv(URL_DEVELOPERS).fillna("---")
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

# --- 4. محرك التصميم (CSS Injection) ---
# هنا قمنا بتغيير شكل كل شيء حرفياً
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* الخلفية العامة */
    [data-testid="stAppViewContainer"] {{
        background: #0a0a0a !important;
        color: white !important;
        direction: rtl !important;
    }}

    /* إخفاء الهيدر الافتراضي لستريمليت */
    header, [data-testid="stHeader"] {{ visibility: hidden; }}

    /* تصميم الكارت المودرن (Custom HTML) */
    .card-container {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        transition: 0.4s;
        position: relative;
    }}
    .card-container:hover {{
        border-color: {GOLD_COLOR};
        background: rgba(212, 175, 55, 0.05);
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}

    /* تصميم العنوان داخل الكارت */
    .card-title {{
        color: {GOLD_COLOR};
        font-size: 1.4rem;
        font-weight: 900;
        margin-bottom: 10px;
    }}

    /* الأزرار الذهبية الحقيقية */
    div.stButton > button {{
        background: {GOLD_GRADIENT} !important;
        color: black !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 10px 25px !important;
        font-weight: 900 !important;
        font-family: 'Cairo' !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.2) !important;
    }}
    
    /* المدخلات (Search Bar) */
    .stTextInput input {{
        background: rgba(255,255,255,0.05) !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 15px !important;
        text-align: right !important;
    }}

    /* التبويبات (Tabs) */
    .stTabs [aria-selected="true"] {{
        background: {GOLD_GRADIENT} !important;
        color: black !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. بوابة الدخول المودرن ---
if not st.session_state.auth:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown(f"""
            <div style="text-align:center; padding:50px 0;">
                <h1 style="background:{GOLD_GRADIENT}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size:4rem; font-weight:900;">MA3LOMATI</h1>
                <p style="color:#666; letter-spacing:5px;">PREMIUM ACCESS</p>
            </div>
        """, unsafe_allow_html=True)
        pwd = st.text_input("Security Key", type="password", placeholder="ادخل رمز الدخول")
        if st.button("Unlock System 🔓"):
            if pwd == "2026":
                st.session_state.auth = True
                st.rerun()
    st.stop()

# --- 6. المحتوى الرئيسي ---
df_p, df_d = load_data()

# الهيدر الملكي
st.markdown(f"""
    <div style="text-align:center; padding:30px; border-bottom:1px solid rgba(212,175,55,0.2); margin-bottom:30px;">
        <h1 style="background:{GOLD_GRADIENT}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin:0; font-weight:900;">MA3LOMATI PRO</h1>
    </div>
""", unsafe_allow_html=True)

menu = option_menu(None, ["الحاسبة", "المطورين", "المشاريع"], 
    icons=["calculator", "building", "search"], 
    default_index=2, orientation="horizontal",
    styles={
        "container": {"background-color": "transparent"},
        "nav-link": {"color": "#888", "font-family": "Cairo"},
        "nav-link-selected": {"background": GOLD_GRADIENT, "color": "black", "font-weight": "bold"}
    })

if menu == "المشاريع":
    s1, s2 = st.columns([3, 1])
    with s1: search = st.text_input("🔍 ابحث عن اسم المشروع أو الموقع...", placeholder="مثال: المونتي جلالة")
    
    filt = df_p[df_p.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else df_p

    # عرض المشاريع بكروت مخصصة تماماً
    grid = st.columns(2)
    for i, (idx, row) in enumerate(filt.iterrows()):
        with grid[i%2]:
            st.markdown(f"""
                <div class="card-container">
                    <div class="card-title">🏢 {row.iloc[0]}</div>
                    <div style="color:#aaa; font-size:0.9rem;">
                        📍 الموقع: <span style="color:white">{row.get('Area','---')}</span><br>
                        🏗️ المطور: <span style="color:white">{row.get('Developer','---')}</span><br>
                        💰 السعر يبدأ من: <span style="color:{GOLD_COLOR}; font-weight:bold;">{row.get('Price','---')}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            # الزرار الآن تحت الكارت مباشرة وبنفس التصميم
            if st.button(f"تفاصيل {row.iloc[0]} ⮕", key=f"btn_{idx}"):
                st.info(f"عرض بيانات: {row.iloc[0]}")

elif menu == "الحاسبة":
    st.markdown(f"<h2 style='color:{GOLD_COLOR}'>🧮 حاسبة القروض العقارية</h2>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        price = c1.number_input("سعر الوحدة", value=5000000)
        years = c2.number_input("سنوات التقسيط", value=8)
        monthly = price / (years * 12)
        st.markdown(f"<h1 style='text-align:center; color:{GOLD_COLOR}'>{monthly:,.0f} ج.م / شهر</h1>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#333; margin-top:100px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
