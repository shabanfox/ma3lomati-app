import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة الجلسة ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

# --- 3. التصميم المودرن الفائق (Advanced CSS) ---
GOLD_GRADIENT = "linear-gradient(135deg, #D4AF37 0%, #F9E29C 50%, #B8860B 100%)"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;700;900&display=swap');
    
    * {{ font-family: 'Cairo', sans-serif; }}
    
    /* خلفية سينمائية */
    [data-testid="stAppViewContainer"] {{
        background: radial-gradient(circle at top right, #1a1a1a, #000000);
        color: white; direction: rtl; text-align: right;
    }}
    
    header {{ visibility: hidden; }}

    /* كروت زجاجية متطورة */
    .modern-card {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 24px;
        padding: 25px;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    
    .modern-card:hover {{
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid {GOLD_COLOR}55;
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
    }}

    /* الهيدر الطافي */
    .floating-header {{
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(15px);
        border-bottom: 1px solid {GOLD_COLOR}44;
        padding: 20px;
        text-align: center;
        border-radius: 0 0 40px 40px;
        margin-bottom: 40px;
    }}

    /* الأزرار الذهبية المعدنية */
    div.stButton > button {{
        background: {GOLD_GRADIENT} !important;
        color: #000 !important;
        border: none !important;
        border-radius: 15px !important;
        font-weight: 900 !important;
        font-size: 1rem !important;
        padding: 12px 24px !important;
        transition: 0.4s !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3) !important;
    }}
    
    div.stButton > button:hover {{
        transform: scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.5) !important;
    }}

    /* تنسيق التبويبات */
    .stTabs [aria-selected="true"] {{
        background: {GOLD_GRADIENT} !important;
        color: black !important;
        border-radius: 12px !important;
    }}

    /* حاسبة القسط - التصميم المودرن */
    .calc-box {{
        border-right: 4px solid {GOLD_COLOR};
        background: rgba(212, 175, 55, 0.05);
        padding: 15px;
        border-radius: 12px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. دالة الدخول (Login UI) ---
if not st.session_state.auth:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown(f"""
            <div style="text-align:center; padding:40px; background:rgba(255,255,255,0.02); border-radius:30px; border:1px solid rgba(212,175,55,0.3);">
                <h1 style="color:#D4AF37; font-size:3rem; font-weight:900;">MA3LOMATI</h1>
                <p style="color:#888; letter-spacing:3px;">PRO ACCESS 2026</p>
            </div><br>
        """, unsafe_allow_html=True)
        pwd = st.text_input("Security Key", type="password", placeholder="••••••••")
        if st.button("Unlock System 🔓"):
            if pwd == "2026":
                st.session_state.auth = True
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 5. تحميل البيانات (Load Data) ---
@st.cache_data
def get_all_data():
    # نفس دالة التحميل السابقة مع التأكد من جلب ملف المونتي جلالة المحدث
    p = pd.read_csv(URL_PROJECTS)
    d = pd.read_csv(URL_DEVELOPERS)
    l = pd.read_csv(URL_LAUNCHES)
    return p.fillna("-"), d.fillna("-"), l.fillna("-")

df_p, df_d, df_l = get_all_data()

# --- 6. الواجهة الرئيسية ---
st.markdown(f"""
    <div class="floating-header">
        <h1 style="margin:0; background:{GOLD_GRADIENT}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight:900;">MA3LOMATI PRO</h1>
        <p style="margin:0; color:#666;">مرحباً بك في عصر العقارات الذكي</p>
    </div>
""", unsafe_allow_html=True)

menu = option_menu(None, ["الحاسبة", "المطورين", "المشاريع", "الذكاء الاصطناعي"], 
    icons=["calculator-fill", "building-fill", "search", "cpu-fill"], 
    default_index=2, orientation="horizontal",
    styles={
        "container": {"background-color": "rgba(255,255,255,0.02)", "border-radius": "20px", "padding": "10px"},
        "nav-link": {"color": "#aaa", "font-size": "16px", "font-weight": "bold"},
        "nav-link-selected": {"background": GOLD_GRADIENT, "color": "black"}
    })

# --- 7. عرض المشاريع بشكل Modern Grid ---
if menu == "المشاريع":
    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🏗️ المشروعات", "🚀 الإطلاق الجديد"])
    
    with tab1:
        s1, s2 = st.columns([3, 1])
        search = s1.text_input("🔍 ابحث عن حلمك القادم...", placeholder="مثال: المونتي جلالة، تطوير مصر...")
        
        # عرض المشاريع بكروت مودرن
        cols = st.columns(2)
        for i, (idx, row) in enumerate(df_p.iterrows()):
            with cols[i%2]:
                st.markdown(f"""
                    <div class="modern-card">
                        <span style="color:{GOLD_COLOR}; font-size:0.8rem; font-weight:bold;">{row.get('Developer','مطور عقاري')}</span>
                        <h2 style="margin:10px 0; font-weight:900;">{row[0]}</h2>
                        <div style="display:flex; justify-content:space-between; margin-top:15px;">
                            <div class="calc-box">📍 {row.get('Location','---')}</div>
                            <div class="calc-box">💰 {row.get('Price','---')}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"استكشاف {row[0]} ⮕", key=f"p_{idx}"):
                    # منطق عرض التفاصيل
                    pass

elif menu == "الحاسبة":
    st.markdown("<h2 style='text-align:center;'>🧮 أدوات الحساب المتقدمة</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='modern-card'>", unsafe_allow_html=True)
        price = st.number_input("سعر الوحدة الإجمالي", value=10000000)
        years = st.slider("مدة التقسيط (سنوات)", 1, 15, 8)
        down_payment = st.number_input("المقدم المدفوع", value=1000000)
        monthly = (price - down_payment) / (years * 12)
        st.markdown(f"<h3>القسط الشهري: <span style='color:{GOLD_COLOR}'>{monthly:,.0f} ج.م</span></h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# زر الخروج في الفوتر
st.sidebar.markdown("---")
if st.sidebar.button("Logout 🔒"):
    st.session_state.auth = False
    st.rerun()

st.markdown(f"<p style='text-align:center; color:#444; margin-top:60px;'>MA3LOMATI PRO © 2026 | Designed for Excellence</p>", unsafe_allow_html=True)
