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
    
    /* خلفية داكنة فخمة */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
    }}

    /* حاوية لتوسيط الكارت في الشاشة */
    .auth-wrapper {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        width: 100%;
    }}

    /* الكارت الزجاجي المدمج */
    .glass-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 45px;
        padding: 50px 40px;
        width: 420px;
        text-align: center;
        box-shadow: 0 40px 100px rgba(0,0,0,0.8);
    }}

    /* اسم المنصة داخل الكارت */
    .card-title {{
        color: #f59e0b;
        font-size: 38px;
        font-weight: 900;
        margin-bottom: 0px;
        text-shadow: 0 0 15px rgba(245, 158, 11, 0.3);
    }}
    
    .card-subtitle {{
        color: #ffffff;
        font-size: 18px;
        font-weight: 400;
        margin-bottom: 35px;
        opacity: 0.8;
        letter-spacing: 1px;
    }}

    /* تنسيق التبويبات */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: transparent !important;
        justify-content: center !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        margin-bottom: 25px;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #f59e0b !important;
        border-bottom: 3px solid #f59e0b !important;
    }}

    /* حقول الإدخال */
    div.stTextInput input {{
        background: rgba(0,0,0,0.5) !important;
        color: #fff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        height: 50px !important;
        text-align: center !important;
    }}

    /* زرار الدخول */
    .stButton button {{
        background: linear-gradient(135deg, #f59e0b, #92400e) !important;
        color: #000 !important;
        font-weight: 900 !important;
        border-radius: 15px !important;
        height: 55px !important;
        width: 100%;
        margin-top: 15px;
        border: none !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Login UI Logic ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    
    # الكارت الزجاجي
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    
    # اسم المنصة والوصف داخل الكارت مباشرة
    st.markdown("<div class='card-title'>MA3LOMATI PRO</div>", unsafe_allow_html=True)
    st.markdown("<div class='card-subtitle'>المنصة العقارية الذكية</div>", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["🔐 دخول", "📝 اشتراك"])
    
    with tab_login:
        st.write("")
        u_in = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed", key="u")
        p_in = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="p")
        
        if st.button("تسجيل الدخول", use_container_width=True):
            if p_in == "2026":
                st.session_state.auth = True; st.rerun()
            else:
                st.error("البيانات غير صحيحة")

    with tab_signup:
        st.write("")
        st.text_input("Name", placeholder="الأسم بالكامل", label_visibility="collapsed", key="s1")
        st.text_input("WA", placeholder="رقم الواتساب", label_visibility="collapsed", key="s2")
        if st.button("إرسال الطلب", use_container_width=True):
            st.success("تم إرسال طلبك للإدارة")

    st.markdown("</div>", unsafe_allow_html=True) # قفل الكارت
    st.markdown("</div>", unsafe_allow_html=True) # قفل التوسيط
    st.stop()

# --- 5. التطبيق بعد الدخول ---
else:
    st.markdown('<h1 style="color:#f59e0b; text-align:center; padding-top:50px;">MA3LOMATI PRO</h1>', unsafe_allow_html=True)
    if st.sidebar.button("خروج"):
        st.session_state.auth = False; st.rerun()
