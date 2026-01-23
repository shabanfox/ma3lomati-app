import streamlit as st
import pandas as pd

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 3. CSS "Top-Aligned Floating UI" ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.85)), 
                    url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
    }}

    /* الحاوية الآن تبدأ من الأعلى مع حشو بسيط */
    .top-auth-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start; /* دفع العناصر للأعلى */
        height: 100vh;
        width: 100%;
        max-width: 450px;
        margin: auto;
        padding-top: 5rem; /* المسافة من سقف الصفحة */
    }}

    /* اسم المنصة */
    .brand-glow-top {{
        color: #f59e0b;
        font-size: 52px;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 0 30px rgba(245, 158, 11, 0.5);
        text-align: center;
    }}
    
    .brand-tagline-top {{
        color: #ffffff;
        font-size: 19px;
        font-weight: 400;
        margin-bottom: 30px;
        letter-spacing: 2px;
        opacity: 0.9;
        text-align: center;
    }}

    /* التبويبات الشفافة */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: transparent !important;
        justify-content: center !important;
        border: none !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: rgba(255,255,255,0.6) !important;
        font-weight: 700 !important;
        font-size: 18px !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #f59e0b !important;
        border-bottom: 3px solid #f59e0b !important;
    }}

    /* المدخلات العائمة */
    div.stTextInput input {{
        background: rgba(255, 255, 255, 0.07) !important;
        color: #fff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        height: 50px !important;
        text-align: center !important;
        backdrop-filter: blur(10px);
    }}
    div.stTextInput input:focus {{
        border-color: #f59e0b !important;
    }}

    /* الزرار */
    .stButton button {{
        background: linear-gradient(90deg, #f59e0b, #d97706) !important;
        color: #000 !important;
        font-weight: 900 !important;
        border-radius: 15px !important;
        height: 50px !important;
        margin-top: 15px;
        border: none !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Logic ---
if not st.session_state.auth:
    # الحاوية الموجهة للأعلى
    st.markdown("<div class='top-auth-container'>", unsafe_allow_html=True)
    
    st.markdown("<p class='brand-glow-top'>MA3LOMATI PRO</p>", unsafe_allow_html=True)
    st.markdown("<p class='brand-tagline-top'>المنصة العقارية الذكية</p>", unsafe_allow_html=True)
    
    t_log, t_reg = st.tabs(["🔐 دخول", "📝 اشتراك"])
    
    with t_log:
        st.write("")
        u = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed", key="user_top")
        p = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="pass_top")
        if st.button("دخول للمنصة", use_container_width=True):
            if p == "2026":
                st.session_state.auth = True; st.rerun()
            else:
                st.error("البيانات غير صحيحة")

    with t_reg:
        st.write("")
        st.text_input("Name", placeholder="الأسم بالكامل", label_visibility="collapsed", key="r1_top")
        st.button("طلب انضمام", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. الداخلية ---
else:
    st.markdown('<h1 style="color:#f59e0b; text-align:center; padding-top:30px;">MA3LOMATI PRO</h1>', unsafe_allow_html=True)
    if st.sidebar.button("خروج"):
        st.session_state.auth = False; st.rerun()
