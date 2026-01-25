import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات المنصة ---
st.set_page_config(page_title="MA3LOMATI PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الروابط والألوان ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
CYAN = "#00f2ff"  # لون لبني نيون متطور
DARK_BG = "#050505"

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "Arabic"

# --- 4. التصميم المطور (UX/UI Edition) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; height: 0; }}
    
    /* منع التمرير في صفحة الدخول فقط */
    {'''html, body, [data-testid="stAppViewContainer"] { 
        overflow: hidden !important; 
        height: 100vh !important; 
        background: #000 !important;
    }''' if not st.session_state.auth else ""}

    .block-container {{ padding: 0 !important; }}

    [data-testid="stAppViewContainer"] {{
        background: radial-gradient(circle at 50% 10%, #001a1a 0%, #000 100%);
        direction: {"rtl" if st.session_state.lang == "Arabic" else "ltr"} !important;
        font-family: 'Cairo', sans-serif;
    }}

    /* كارت الدخول الزجاجي (The Glass Card) */
    .auth-wrapper {{
        display: flex; flex-direction: column; align-items: center;
        padding-top: 5vh; height: 100vh;
    }}
    .glass-card {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(0, 242, 255, 0.3);
        border-radius: 30px;
        padding: 40px 30px;
        width: 92%; max-width: 420px;
        box-shadow: 0 0 40px rgba(0, 242, 255, 0.1);
        text-align: center;
    }}

    /* نصوص متوهجة */
    .neon-title {{
        color: {CYAN}; font-size: 35px; font-weight: 900;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
        margin-bottom: 5px;
    }}

    /* حقول الإدخال فائقة الوضوح */
    div.stTextInput input {{
        background: #fff !important; color: #000 !important;
        border: 2px solid {CYAN} !important; border-radius: 15px !important;
        height: 55px !important; font-size: 18px !important; font-weight: bold !important;
        text-align: center !important; transition: 0.3s;
    }}
    div.stTextInput input:focus {{
        box-shadow: 0 0 15px {CYAN} !important;
    }}

    /* الأزرار المطورة */
    .stButton > button {{
        background: linear-gradient(90deg, {CYAN}, #00a8ff) !important;
        color: #000 !important; font-weight: 900 !important;
        height: 55px !important; border-radius: 15px !important;
        font-size: 18px !important; border: none !important;
        box-shadow: 0 5px 15px rgba(0, 242, 255, 0.3) !important;
    }}

    /* التبويبات (Tabs) */
    .stTabs [data-baseweb="tab-list"] {{ border: none; }}
    .stTabs [data-baseweb="tab"] {{ color: #666 !important; font-weight: bold; }}
    .stTabs [aria-selected="true"] {{ color: {CYAN} !important; border-bottom-color: {CYAN} !important; }}

    /* الهيدر الداخلي المصغر جداً */
    .top-nav {{
        background: rgba(0,0,0,0.8); padding: 10px; 
        border-bottom: 1px solid {CYAN}; text-align: center;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. منطق واجهة الدخول (The Pro Interface) ---
if not st.session_state.auth:
    # زر اللغة العائم
    c1, c2, c3 = st.columns([0.1, 0.7, 0.2])
    with c3:
        lang_sel = st.selectbox("🌐", ["العربية", "English"], label_visibility="collapsed")
        st.session_state.lang = "Arabic" if lang_sel == "العربية" else "English"

    st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
    with st.container():
        st.markdown(f'''
            <div class="glass-card">
                <div class="neon-title">MA3LOMATI</div>
                <p style="color:#eee; font-size:14px; margin-bottom:20px; letter-spacing:2px;">
                    {"بوابتك لعقارات المستقبل" if st.session_state.lang=="Arabic" else "FUTURE REAL ESTATE PORTAL"}
                </p>
        ''', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔑 " + ("دخول" if st.session_state.lang=="Arabic" else "LOGIN"), 
                              "📝 " + ("اشتراك" if st.session_state.lang=="Arabic" else "JOIN")])
        
        with tab1:
            u = st.text_input("User", key="u_log", placeholder=("المستخدم" if st.session_state.lang=="Arabic" else "User"), label_visibility="collapsed")
            p = st.text_input("Pass", type="password", key="p_log", placeholder=("كلمة السر" if st.session_state.lang=="Arabic" else "Pass"), label_visibility="collapsed")
            if st.button("LOG IN"):
                if p == "2026": # دخول سريع للأدمن
                    st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
                # هنا يمكنك إضافة دالة login_user(u, p)
        
        with tab2:
            st.text_input("Full Name", placeholder=("الاسم بالكامل" if st.session_state.lang=="Arabic" else "Full Name"), label_visibility="collapsed")
            st.text_input("Phone", placeholder=("واتساب" if st.session_state.lang=="Arabic" else "WhatsApp"), label_visibility="collapsed")
            if st.button("GET STARTED"):
                st.info("سنتواصل معك للتفعيل" if st.session_state.lang=="Arabic" else "Wait for admin activation")
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 6. الواجهة الداخلية (Compact Pro Dashboard) ---
st.markdown(f'''
    <div class="top-nav">
        <h3 style="color:white; margin:0;">MA3LOMATI <span style="color:{CYAN}">PRO</span></h3>
        <span style="color:{CYAN}; font-size:12px;">Welcome, {st.session_state.current_user}</span>
    </div>
''', unsafe_allow_html=True)

# قائمة خيارات احترافية
selected = option_menu(None, ["المشاريع", "المطورين", "أدوات", "AI"], 
    icons=["search", "building", "calculator", "robot"], 
    orientation="horizontal", 
    styles={
        "container": {"background-color": "transparent"},
        "nav-link-selected": {"background-color": CYAN, "color": "black", "font-weight": "bold"}
    })

# محتوى تجريبي
st.write(f"### 📍 قسم {selected}")
if st.button("🚪 خروج الآمن"):
    st.session_state.auth = False
    st.rerun()

st.markdown(f"<p style='text-align:center; color:#333; margin-top:100px;'>MA3LOMATI PLATINUM V4 © 2026</p>", unsafe_allow_html=True)

