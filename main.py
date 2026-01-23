import streamlit as st
import pandas as pd

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 3. CSS "Ultra-Top Floating UI" ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.6)), 
                    url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
    }}

    /* حاوية تدفع العناصر لأعلى الصفحة تماماً */
    .ultra-top-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start; /* دفع العناصر للأعلى */
        height: 100vh;
        width: 100%;
        max-width: 450px;
        margin: auto;
        padding-top: 2rem; /* مسافة بسيطة جداً من السقف */
    }}

    /* اسم المنصة في الأعلى */
    .brand-glow-top {{
        color: #f59e0b;
        font-size: 55px; /* تكبير الخط ليكون بارزاً */
        font-weight: 900;
        margin: 0;
        text-shadow: 0 10px 30px rgba(0,0,0,0.5);
        text-align: center;
    }}
    
    .brand-tagline-top {{
        color: #ffffff;
        font-size: 20px;
        font-weight: 400;
        margin-bottom: 25px;
        letter-spacing: 2px;
        text-align: center;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
    }}

    /* التبويبات الشفافة */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(0,0,0,0.3) !important;
        border-radius: 20px;
        padding: 5px;
        justify-content: center !important;
        border: none !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: rgba(255,255,255,0.7) !important;
        font-weight: 700 !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #f59e0b !important;
        background: rgba(255,255,255,0.05) !important;
        border-radius: 15px;
    }}

    /* حقول الإدخال عائمة */
    div.stTextInput input {{
        background: rgba(0, 0, 0, 0.7) !important;
        color: #fff !important;
        border: 1px solid rgba(245, 158, 11, 0.4) !important;
        border-radius: 15px !important;
        height: 55px !important;
        text-align: center !important;
        font-size: 18px !important;
    }}

    /* زرار الدخول */
    .stButton button {{
        background: linear-gradient(90deg, #f59e0b, #d97706) !important;
        color: #000 !important;
        font-weight: 900 !important;
        border-radius: 15px !important;
        height: 55px !important;
        margin-top: 20px;
        border: none !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. UI Logic ---
if not st.session_state.auth:
    # الحاوية الملتصقة بالأعلى
    st.markdown("<div class='ultra-top-container'>", unsafe_allow_html=True)
    
    # اسم الموقع والوصف في قمة الصفحة
    st.markdown("<p class='brand-glow-top'>MA3LOMATI PRO</p>", unsafe_allow_html=True)
    st.markdown("<p class='brand-tagline-top'>المنصة العقارية الذكية</p>", unsafe_allow_html=True)
    
    t_log, t_reg = st.tabs(["🔐 دخول", "📝 اشتراك"])
    
    with t_log:
        st.write("")
        u = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_top")
        p = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="p_top")
        if st.button("دخول للمنصة 🚀", use_container_width=True):
            if p == "2026":
                st.session_state.auth = True; st.rerun()
            else:
                st.error("خطأ في البيانات")

    with t_reg:
        st.write("")
        st.text_input("Phone", placeholder="رقم الهاتف", label_visibility="collapsed", key="r_top")
        st.button("طلب تفعيل الحساب", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. التطبيق الداخلي ---
else:
    st.markdown('<h1 style="color:#f59e0b; text-align:center; padding-top:30px;">MA3LOMATI PRO</h1>', unsafe_allow_html=True)
    if st.sidebar.button("خروج"):
        st.session_state.auth = False; st.rerun()
