import streamlit as st
import pandas as pd

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 3. CSS "Absolute Middle Center" UI ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding: 0px !important; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
    }}

    /* حاوية السنترة المطلقة (نص الشاشة بالظبط) */
    .absolute-center-wrapper {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center; /* سنترة طولية */
        height: 100vh;
        width: 100%;
        text-align: center;
    }}

    .auth-box {{
        width: 100%;
        max-width: 420px;
        padding: 20px;
    }}

    /* اسم المنصة في المنتصف بتوهج ملكي */
    .brand-main {{
        color: #f59e0b;
        font-size: 52px;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 0 30px rgba(245, 158, 11, 0.5);
        line-height: 1.1;
    }}
    
    .brand-sub {{
        color: #ffffff;
        font-size: 20px;
        font-weight: 400;
        margin-bottom: 40px;
        letter-spacing: 1px;
        opacity: 0.9;
    }}

    /* التبويبات الشفافة */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: transparent !important;
        justify-content: center !important;
        border-bottom: 1px solid rgba(255,255,255,0.1) !important;
        margin-bottom: 30px;
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

    /* خانات الإدخال */
    div.stTextInput input {{
        background: rgba(255, 255, 255, 0.05) !important;
        color: #fff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        height: 55px !important;
        text-align: center !important;
        font-size: 16px !important;
    }}
    div.stTextInput input:focus {{
        border-color: #f59e0b !important;
        background: rgba(255, 255, 255, 0.1) !important;
    }}

    /* زرار الدخول */
    .stButton button {{
        background: linear-gradient(90deg, #f59e0b, #d97706) !important;
        color: #000 !important;
        font-weight: 900 !important;
        border-radius: 15px !important;
        height: 55px !important;
        width: 100%;
        margin-top: 20px;
        border: none !important;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.2);
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Login Logic ---
if not st.session_state.auth:
    # تطبيق السنترة المطلقة في منتصف الصفحة
    st.markdown("<div class='absolute-center-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='auth-box'>", unsafe_allow_html=True)
    
    # اسم المنصة في المنتصف
    st.markdown("<p class='brand-main'>MA3LOMATI PRO</p>", unsafe_allow_html=True)
    st.markdown("<p class='brand-sub'>المنصة العقارية الذكية</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 تسجيل الدخول", "📝 طلب انضمام"])
    
    with tab1:
        st.write("")
        u_name = st.text_input("Username", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_mid")
        p_word = st.text_input("Password", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="p_mid")
        
        if st.button("دخول للمنصة 🚀", use_container_width=True):
            if p_word == "2026":
                st.session_state.auth = True; st.rerun()
            else:
                st.error("البيانات غير صحيحة")

    with tab2:
        st.write("")
        st.text_input("Full Name", placeholder="الاسم بالكامل", label_visibility="collapsed", key="reg_n")
        st.text_input("WA", placeholder="رقم الواتساب", label_visibility="collapsed", key="reg_w")
        if st.button("إرسال طلب تفعيل", use_container_width=True):
            st.success("تم استلام طلبك")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. الصفحة الداخلية ---
else:
    st.markdown('<h1 style="color:#f59e0b; text-align:center; padding-top:50px;">MA3LOMATI PRO</h1>', unsafe_allow_html=True)
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False; st.rerun()
