import streamlit as st
import pandas as pd
import requests
import feedparser
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الروابط والألوان المطورة ---
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
MAIN_COLOR = "#00d4ff" 
ACCENT_COLOR = "#005f73"

if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "Arabic"

# --- 3. التصميم الجمالي المطور (Premium UI) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; }}
    
    /* خلفية متدرجة سينمائية */
    [data-testid="stAppViewContainer"] {{
        background: radial-gradient(circle at top right, #001219, #000000);
        direction: {"rtl" if st.session_state.lang == "Arabic" else "ltr"} !important;
        font-family: 'Cairo', sans-serif;
    }}

    /* تصميم كارت الدخول (Glassmorphism المطور) */
    .auth-card {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 25px;
        padding: 35px 25px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.8);
        text-align: center;
        margin-top: 20px;
    }}

    /* تصميم الهيدر الداخلي (Modern Gradient) */
    .modern-header {{
        background: linear-gradient(135deg, {ACCENT_COLOR} 0%, #000 100%);
        padding: 25px;
        border-radius: 0 0 30px 30px;
        border-bottom: 2px solid {MAIN_COLOR};
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,212,255,0.2);
    }}

    /* الكروت الداخلية (Interactive Cards) */
    div.stButton > button[key*="card_"] {{
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(0, 212, 255, 0.2) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        transition: 0.4s all ease !important;
        text-align: right !important;
    }}
    div.stButton > button[key*="card_"]:hover {{
        border-color: {MAIN_COLOR} !important;
        background: rgba(0, 212, 255, 0.1) !important;
        transform: translateY(-5px);
    }}

    /* تنسيق الـ Badges للمعلومات */
    .info-badge {{
        background: rgba(0, 212, 255, 0.1);
        color: {MAIN_COLOR};
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 12px;
        font-weight: bold;
        border: 1px solid {MAIN_COLOR};
    }}

    /* إخفاء السكرول بار المزعج */
    ::-webkit-scrollbar {{ width: 5px; }}
    ::-webkit-scrollbar-track {{ background: #000; }}
    ::-webkit-scrollbar-thumb {{ background: {MAIN_COLOR}; border-radius: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. واجهة الدخول المطورة ---
if not st.session_state.auth:
    # زر اللغة (أيقونة فقط)
    st.write(f"<div style='text-align:left; padding:10px;'><span style='color:{MAIN_COLOR}'>🌐 {st.session_state.lang}</span></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    with col2:
        st.markdown(f"""
            <div class="auth-card">
                <h1 style='color:{MAIN_COLOR}; font-weight:900; letter-spacing:2px; margin-bottom:0;'>MA3LOMATI</h1>
                <p style='color:#666; font-size:12px; margin-bottom:25px;'>PREMIUM REAL ESTATE INTELLIGENCE</p>
        """, unsafe_allow_html=True)
        
        tab_log, tab_reg = st.tabs(["🔐 LOGIN", "📝 JOIN"])
        with tab_log:
            u = st.text_input("User", placeholder="Username", label_visibility="collapsed")
            p = st.text_input("Pass", type="password", placeholder="Password", label_visibility="collapsed")
            if st.button("ENTER SYSTEM"):
                if p == "2026": # تجربة سريعة
                    st.session_state.auth = True
                    st.session_state.current_user = "Admin"
                    st.rerun()
        
        with tab_reg:
            st.markdown(f"<p style='color:#888;'>سجل بياناتك وسيتم تفعيل حسابك فوراً</p>", unsafe_allow_html=True)
            st.text_input("Name", placeholder="Full Name", label_visibility="collapsed")
            st.button("REQUEST ACCESS")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. الواجهة الداخلية (بعد الدخول) ---
# الهيدر المطور
st.markdown(f"""
    <div class="modern-header">
        <h2 style="color:white; margin:0; font-weight:900;">MA3LOMATI <span style="color:{MAIN_COLOR}">PRO</span></h2>
        <div style="margin-top:5px;">
            <span class="info-badge">VIP ACCESS</span>
            <span class="info-badge">{st.session_state.current_user}</span>
            <span class="info-badge">2026 EDITION</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# القائمة السفلية أو العلوية المتطورة
menu = option_menu(None, ["المشاريع", "المطورين", "أدواتي", "AI بوت"], 
    icons=["house-door", "building", "calculator", "robot"], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"background-color": "transparent"},
        "nav-link": {"color": "white", "font-size": "14px", "font-weight": "600"},
        "nav-link-selected": {"background-color": MAIN_COLOR, "color": "black"}
    })

# محتوى تجريبي للكروت المطورة
st.write("### 🏢 المشاريع المقترحة")
c1, c2 = st.columns(2)
with c1:
    if st.button("🏢 مشروع العاصمة الإدارية الجديدة\n📍 التجمع الخامس | متاح حالياً", key="card_1"):
        pass
with c2:
    if st.button("🏢 مشروع نور سيتي\n📍 حدائق العاصمة | قيد الإنشاء", key="card_2"):
        pass

# زر خروج عائم
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout"):
    st.session_state.auth = False
    st.rerun()

