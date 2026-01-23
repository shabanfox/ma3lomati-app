import streamlit as st
import pandas as pd

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 3. CSS Luxury Centered UI ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        font-family: 'Cairo', sans-serif;
    }}

    /* حاوية التوسيط الكامل */
    .main-auth-wrapper {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        width: 100%;
    }}

    /* الكارت اللي مكتوب عليه اسم الموقع (الستايل اللي طلبته) */
    .oval-header-card {{
        background-color: #000; 
        border: 3px solid #f59e0b; 
        border-radius: 50px;
        padding: 15px 40px; 
        color: #f59e0b; 
        font-size: 26px; 
        font-weight: 900;
        text-align: center; 
        z-index: 10; 
        margin-bottom: -25px; /* ليدخل جزئياً في كارت الدخول */
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        min-width: 320px;
    }}

    /* كارت الدخول الأبيض أو الشفاف (حسب رغبتك، هنا جعلته أبيض لبروز الكارت الأسود) */
    .login-box {{
        background-color: #ffffff; 
        width: 400px; 
        padding: 60px 35px 35px 35px; 
        border-radius: 30px; 
        text-align: center; 
        box-shadow: 0 20px 50px rgba(0,0,0,0.4);
    }}

    /* تنسيق النصوص والتبويبات داخل الكارت الأبيض */
    .stTabs [data-baseweb="tab-list"] {{ justify-content: center !important; }}
    .stTabs [data-baseweb="tab"] {{ font-weight: 700 !important; color: #444 !important; }}
    .stTabs [aria-selected="true"] {{ color: #f59e0b !important; }}
    
    div.stTextInput input {{
        background-color: #f9f9f9 !important;
        border: 1px solid #ddd !important;
        border-radius: 12px !important;
        height: 45px !important;
        text-align: center !important;
    }}
    
    .stButton button {{
        background: #000 !important;
        color: #f59e0b !important;
        border: 2px solid #f59e0b !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        height: 50px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Login UI ---
if not st.session_state.auth:
    # بدء حاوية التوسيط
    st.markdown("<div class='main-auth-wrapper'>", unsafe_allow_html=True)
    
    # 1. الكارت اللي مكتوب عليه اسم الموقع
    st.markdown("<div class='oval-header-card'>MA3LOMATI PRO</div>", unsafe_allow_html=True)
    
    # 2. كارت الدخول
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    
    # إضافة جملة المنصة العقارية تحت الكارت مباشرة
    st.markdown("<p style='color:#666; font-weight:700; margin-top:-10px; margin-bottom:20px;'>المنصة العقارية الذكية</p>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["تسجيل الدخول", "اشتراك جديد"])
    
    with t1:
        st.write("")
        st.text_input("Username", placeholder="اسم المستخدم", label_visibility="collapsed", key="u")
        st.text_input("Password", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="p")
        if st.button("دخول للمنصة", use_container_width=True):
            st.session_state.auth = True
            st.rerun()
            
    with t2:
        st.write("")
        st.info("للاشتراك، يرجى التواصل مع الدعم الفني لتفعيل الحساب.")
        st.text_input("رقم الهاتف", placeholder="01xxxxxxxxx", key="s1")
        st.button("طلب انضمام", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True) # قفل الكارت الأبيض
    st.markdown("</div>", unsafe_allow_html=True) # قفل التوسيط
    st.stop()

# --- 5. التطبيق الداخلي ---
else:
    st.title("مرحباً بك في MA3LOMATI PRO")
    if st.button("تسجيل خروج"):
        st.session_state.auth = False
        st.rerun()
