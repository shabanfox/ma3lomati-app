import streamlit as st
import pandas as pd

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 3. CSS Luxury Design ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
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

    /* الكارت الأسود اللي مكتوب عليه البيانات (تعديل السطرين) */
    .oval-header-card {{
        background-color: #000; 
        border: 3px solid #f59e0b; 
        border-radius: 40px;
        padding: 20px 50px; 
        text-align: center; 
        z-index: 10; 
        margin-bottom: -40px; /* تداخل أكبر ليتناسب مع السطرين */
        box-shadow: 0 15px 30px rgba(0,0,0,0.6);
        min-width: 350px;
    }}

    .title-top {{
        color: #f59e0b; 
        font-size: 28px; 
        font-weight: 900;
        margin: 0;
        line-height: 1.2;
    }}

    .subtitle-top {{
        color: #ffffff; 
        font-size: 16px; 
        font-weight: 400;
        margin: 5px 0 0 0;
        opacity: 0.9;
    }}

    /* كارت الدخول */
    .login-box {{
        background-color: #ffffff; 
        width: 420px; 
        padding: 70px 35px 35px 35px; 
        border-radius: 35px; 
        text-align: center; 
        box-shadow: 0 25px 60px rgba(0,0,0,0.5);
    }}

    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] {{ justify-content: center !important; gap: 20px; }}
    .stTabs [data-baseweb="tab"] {{ font-weight: 700 !important; font-size: 16px; }}
    
    div.stTextInput input {{
        background-color: #f4f4f4 !important;
        border: 1px solid #eee !important;
        border-radius: 12px !important;
        height: 48px !important;
        text-align: center !important;
    }}
    
    .stButton button {{
        background: #000 !important;
        color: #f59e0b !important;
        border: 2px solid #f59e0b !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        height: 52px !important;
        margin-top: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Login UI ---
if not st.session_state.auth:
    st.markdown("<div class='main-auth-wrapper'>", unsafe_allow_html=True)
    
    # الكارت الأسود وبه السطرين المطلوبة
    st.markdown(f"""
        <div class='oval-header-card'>
            <p class='title-top'>MA3LOMATI PRO</p>
            <p class='subtitle-top'>المنصة العقارية الذكية</p>
        </div>
    """, unsafe_allow_html=True)
    
    # كارت الدخول الأبيض
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["🔐 دخول", "📝 اشتراك"])
    
    with t1:
        st.write("")
        u_in = st.text_input("Username", placeholder="اسم المستخدم", label_visibility="collapsed", key="u")
        p_in = st.text_input("Password", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="p")
        if st.button("دخول للمنصة", use_container_width=True):
            if p_in == "2026": # كود الدخول السريع
                st.session_state.auth = True; st.rerun()
            else:
                st.error("البيانات غير صحيحة")
            
    with t2:
        st.write("")
        st.text_input("Name", placeholder="الأسم بالكامل", label_visibility="collapsed", key="reg_n")
        st.text_input("Phone", placeholder="رقم الواتساب", label_visibility="collapsed", key="reg_p")
        if st.button("طلب تفعيل الحساب", use_container_width=True):
            st.success("تم إرسال طلبك بنجاح!")

    st.markdown("</div>", unsafe_allow_html=True) 
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. بعد الدخول ---
else:
    st.markdown('<h1 style="color:#f59e0b; text-align:center; padding-top:50px;">MA3LOMATI PRO</h1>', unsafe_allow_html=True)
    if st.sidebar.button("🚪 تسجيل خروج"):
        st.session_state.auth = False; st.rerun()
