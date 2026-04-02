import streamlit as st
import pandas as pd

# --- 1. Page Config ---
st.set_config = st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- الروابط ---
BG_IMG = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1920&q=80" # خلفية فضاء تقنية
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"

# --- 3. CSS (The Masterpiece UI) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;700;900&family=Montserrat:wght@900&display=swap');
    
    header, [data-testid="stHeader"], [data-testid="stToolbar"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}

    [data-testid="stAppViewContainer"] {{
        background: radial-gradient(circle at center, rgba(0,0,0,0.85) 0%, rgba(0,0,0,1) 100%), url('{BG_IMG}');
        background-size: cover;
        font-family: 'Cairo', sans-serif;
    }}

    /* الحاوية العلوية المركزية */
    .main-auth-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        height: 100vh;
        padding-top: 80px;
    }}

    /* اسم الموقع - ضخم ومضيء */
    .main-logo {{
        font-family: 'Montserrat', sans-serif;
        font-size: 80px;
        font-weight: 900;
        text-transform: uppercase;
        color: #fff;
        text-shadow: 0 0 20px rgba(245, 158, 11, 0.6), 0 0 40px rgba(245, 158, 11, 0.3);
        margin-bottom: -50px; /* تداخل احترافي مع الصندوق */
        z-index: 10;
        letter-spacing: 10px;
    }}

    /* الصندوق الزجاجي الشيك جداً */
    .glass-login-box {{
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(40px);
        -webkit-backdrop-filter: blur(40px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 2px solid rgba(245, 158, 11, 0.5); /* خط ذهبي رفيع من فوق */
        width: 380px;
        padding: 70px 35px 35px 35px;
        border-radius: 40px;
        box-shadow: 0 40px 100px rgba(0,0,0,0.9);
        text-align: center;
    }}

    /* تحسين شكل التبويبات */
    .stTabs [data-baseweb="tab-list"] {{ border-bottom: none !important; }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent !important;
        color: #555 !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #f59e0b !important;
    }}

    /* تصميم الحقول بشكل مدمج */
    .stTextInput input {{
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 15px !important;
        color: #eee !important;
        height: 45px !important;
        transition: 0.3s;
    }}
    .stTextInput input:focus {{
        border-color: #f59e0b !important;
        background: rgba(255, 255, 255, 0.07) !important;
    }}

    /* زر الدخول الذهبي */
    .stButton>button {{
        background: linear-gradient(90deg, #f59e0b, #d97706) !important;
        color: #000 !important;
        border: none !important;
        border-radius: 15px !important;
        height: 45px !important;
        font-weight: 900 !important;
        letter-spacing: 1px;
        box-shadow: 0 10px 20px rgba(217, 119, 6, 0.2) !important;
    }}
    
    .stButton>button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 15px 30px rgba(217, 119, 6, 0.4) !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. واجهة الدخول ---
if not st.session_state.auth:
    st.markdown("<div class='main-auth-container'>", unsafe_allow_html=True)
    
    # اسم المنصة هو الأساس
    st.markdown("<div class='main-logo'>MA3LOMATI</div>", unsafe_allow_html=True)
    
    # الصندوق خلف الاسم
    st.markdown("<div class='glass-login-box'>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["LOG IN", "JOIN"] if st.session_state.lang=="EN" else ["دخول", "اشتراك"])
    
    with tab1:
        st.write("")
        u = st.text_input("Name" if st.session_state.lang=="EN" else "اسم المستخدم", placeholder="Enter Name", key="u")
        p = st.text_input("Pass" if st.session_state.lang=="EN" else "كلمة المرور", placeholder="••••••••", type="password", key="p")
        st.write("")
        if st.button("SIGN IN" if st.session_state.lang=="EN" else "دخول الآن", use_container_width=True):
            try:
                df = pd.read_csv(USER_SHEET_URL)
                df.columns = [c.strip() for c in df.columns]
                if any((df['Name'].astype(str) == u) & (df['Password'].astype(str) == p)):
                    st.session_state.auth = True; st.rerun()
                else: st.error("Wrong Data")
            except: st.error("Connection Error")

    with tab2:
        st.write("")
        st.text_input("WhatsApp" if st.session_state.lang=="EN" else "رقم الواتساب")
        st.text_input("Company" if st.session_state.lang=="EN" else "اسم الشركة")
        if st.button("SUBMIT REQUEST" if st.session_state.lang=="EN" else "إرسال الطلب", use_container_width=True):
            st.success("Request Sent!")

    st.write("---")
    if st.button("🌐 SWITCH LANGUAGE", size="small"):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 5. المنصة من الداخل ---
else:
    st.markdown("<h1 style='text-align:center; color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state.auth = False; st.rerun()
