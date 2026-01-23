import streamlit as st
import pandas as pd

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 3. CSS "Bottom-Aligned Floating UI" ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.9)), 
                    url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
    }}

    /* حاوية تدفع العناصر لأسفل الصفحة */
    .bottom-auth-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-end; /* دفع العناصر للأسفل */
        height: 100vh;
        width: 100%;
        max-width: 450px;
        margin: auto;
        padding-bottom: 5rem; /* مسافة من قاع الصفحة */
    }}

    /* اسم المنصة عائم في الأسفل */
    .brand-glow-bottom {{
        color: #f59e0b;
        font-size: 48px;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 0 25px rgba(245, 158, 11, 0.6);
        text-align: center;
    }}
    
    .brand-tagline-bottom {{
        color: #ffffff;
        font-size: 18px;
        font-weight: 400;
        margin-bottom: 30px;
        letter-spacing: 1px;
        opacity: 0.95;
        text-align: center;
    }}

    /* التبويبات الشفافة */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: transparent !important;
        justify-content: center !important;
        border: none !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: rgba(255,255,255,0.7) !important;
        font-weight: 700 !important;
        font-size: 17px !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #f59e0b !important;
        border-bottom: 3px solid #f59e0b !important;
    }}

    /* حقول الإدخال بتأثير زجاجي خفيف */
    div.stTextInput input {{
        background: rgba(0, 0, 0, 0.6) !important;
        color: #fff !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 15px !important;
        height: 50px !important;
        text-align: center !important;
        backdrop-filter: blur(5px);
    }}
    div.stTextInput input:focus {{
        border-color: #f59e0b !important;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.2) !important;
    }}

    /* زرار الدخول */
    .stButton button {{
        background: linear-gradient(90deg, #f59e0b, #d97706) !important;
        color: #000 !important;
        font-weight: 900 !important;
        border-radius: 15px !important;
        height: 52px !important;
        margin-top: 15px;
        border: none !important;
        transition: 0.3s;
    }}
    .stButton button:hover {{
        transform: scale(1.02);
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Logic ---
if not st.session_state.auth:
    # بدء الحاوية المستقرة في الأسفل
    st.markdown("<div class='bottom-auth-container'>", unsafe_allow_html=True)
    
    # اسم الموقع والوصف عائمين فوق العناصر
    st.markdown("<p class='brand-glow-bottom'>MA3LOMATI PRO</p>", unsafe_allow_html=True)
    st.markdown("<p class='brand-tagline-bottom'>المنصة العقارية الذكية</p>", unsafe_allow_html=True)
    
    t_log, t_reg = st.tabs(["🔐 دخول", "📝 اشتراك"])
    
    with t_log:
        st.write("")
        u = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_bottom")
        p = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="p_bottom")
        if st.button("دخول للمنصة 🚀", use_container_width=True):
            if p == "2026":
                st.session_state.auth = True; st.rerun()
            else:
                st.error("خطأ في البيانات")

    with t_reg:
        st.write("")
        st.text_input("Phone", placeholder="رقم الهاتف للتواصل", label_visibility="collapsed", key="r_bottom")
        st.button("طلب اشتراك جديد", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True) # قفل الحاوية
    st.stop()

# --- 5. بعد الدخول ---
else:
    st.markdown('<h1 style="color:#f59e0b; text-align:center; padding-top:30px;">MA3LOMATI PRO</h1>', unsafe_allow_html=True)
    if st.sidebar.button("خروج"):
        st.session_state.auth = False; st.rerun()
