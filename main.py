import streamlit as st
import pandas as pd

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 3. CSS "Absolute Top" UI ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* حذف أي مساحات افتراضية من ستريمليت */
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding: 0px !important; margin: 0px !important; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.7)), 
                    url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
    }}

    /* حاوية تبدأ من الصفر فوق */
    .stick-to-top-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        height: 100vh;
        width: 100%;
        max-width: 450px;
        margin: auto;
        padding-top: 0px !important; /* لا يوجد مسافة من السقف */
    }}

    /* اسم المنصة - أول شيء في الصفحة */
    .brand-top {{
        color: #f59e0b;
        font-size: 55px;
        font-weight: 900;
        margin-top: 10px; /* مسافة بسيطة جداً لجمال الخط */
        margin-bottom: 0px;
        text-shadow: 0 10px 20px rgba(0,0,0,0.9);
        text-align: center;
    }}
    
    .tagline-top {{
        color: #ffffff;
        font-size: 18px;
        font-weight: 400;
        margin-bottom: 20px;
        opacity: 0.9;
        text-align: center;
    }}

    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 0px 0px 15px 15px;
        justify-content: center !important;
        border: none !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: rgba(255,255,255,0.7) !important;
        font-weight: 700 !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #f59e0b !important;
    }}

    /* خانات الإدخال */
    div.stTextInput input {{
        background: rgba(0, 0, 0, 0.8) !important;
        color: #fff !important;
        border: 1px solid #444 !important;
        border-radius: 12px !important;
        height: 50px !important;
        text-align: center !important;
    }}

    /* زرار الدخول */
    .stButton button {{
        background: #f59e0b !important;
        color: #000 !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        height: 50px !important;
        border: none !important;
        margin-top: 15px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Logic ---
if not st.session_state.auth:
    # الحاوية بتبدأ من أول بكسل
    st.markdown("<div class='stick-to-top-container'>", unsafe_allow_html=True)
    
    st.markdown("<p class='brand-top'>MA3LOMATI PRO</p>", unsafe_allow_html=True)
    st.markdown("<p class='tagline-top'>المنصة العقارية الذكية</p>", unsafe_allow_html=True)
    
    t_log, t_reg = st.tabs(["🔐 دخول", "📝 اشتراك"])
    
    with t_log:
        st.write("")
        u = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_top_fix")
        p = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="p_top_fix")
        if st.button("دخول للمنصة", use_container_width=True):
            if p == "2026":
                st.session_state.auth = True; st.rerun()
            else:
                st.error("البيانات غير صحيحة")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. الداخلية ---
else:
    st.success("تم تسجيل الدخول!")
    if st.button("خروج"):
        st.session_state.auth = False; st.rerun()
