import streamlit as st
import pandas as pd

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- الروابط ---
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"

# --- 3. Custom CSS (التركيز على الجزء العلوي) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Montserrat:wght@900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    /* تقليل الهوامش العلوية للمنصة بالكامل */
    .block-container {{ padding-top: 1rem !important; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover;
        font-family: 'Cairo', sans-serif;
    }}

    /* حاوية تبدأ من أعلى الصفحة */
    .top-auth-wrapper {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start; /* تبدأ من فوق */
        padding-top: 20px; /* مسافة بسيطة من السقف */
        width: 100%;
    }}

    /* اسم المنصة الضخم */
    .brand-overlay {{
        font-family: 'Montserrat', sans-serif;
        font-size: 60px;
        font-weight: 900;
        background: linear-gradient(180deg, #f59e0b 0%, #d97706 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: -30px; /* التداخل مع الكارد */
        z-index: 99;
        filter: drop-shadow(0px 5px 15px rgba(0,0,0,0.5));
    }}

    /* الكارد المصغر */
    .auth-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(25px);
        width: 360px;
        padding: 45px 25px 25px 25px;
        border-radius: 25px;
        border: 1px solid rgba(245, 158, 11, 0.3);
        box-shadow: 0 20px 40px rgba(0,0,0,0.6);
        text-align: center;
    }}

    /* تبويبات أنيقة */
    .stTabs [data-baseweb="tab-list"] {{ justify-content: center; gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{ font-size: 15px !important; color: #888 !important; }}
    .stTabs [aria-selected="true"] {{ color: #f59e0b !important; }}

    .stTextInput>div>div>input {{
        background: rgba(255, 255, 255, 0.07) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        height: 38px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Logic ---
def validate_login(u, p):
    try:
        df = pd.read_csv(USER_SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        match = df[(df['Name'].astype(str).str.strip() == str(u).strip()) & 
                   (df['Password'].astype(str).str.strip() == str(p).strip())]
        return not match.empty
    except: return False

# --- 5. UI ---
if not st.session_state.auth:
    st.markdown("<div class='top-auth-wrapper'>", unsafe_allow_html=True)
    
    # الاسم فوق الكارد
    st.markdown("<div class='brand-overlay'>MA3LOMATI</div>", unsafe_allow_html=True)
    
    # الكارد
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["دخول", "اشتراك"] if st.session_state.lang=="AR" else ["Login", "Sign Up"])
    
    with t1:
        st.write("")
        u_val = st.text_input("الاسم" if st.session_state.lang=="AR" else "Name", key="log_u")
        p_val = st.text_input("كلمة المرور" if st.session_state.lang=="AR" else "Password", type="password", key="log_p")
        if st.button("دخول" if st.session_state.lang=="AR" else "Sign In", use_container_width=True, type="primary"):
            if validate_login(u_val, p_val):
                st.session_state.auth = True; st.rerun()
            else: st.error("❌")

    with t2:
        st.write("")
        st.text_input("واتساب" if st.session_state.lang=="AR" else "WhatsApp")
        st.text_input("الشركة" if st.session_state.lang=="AR" else "Company")
        st.text_input("الباسورد" if st.session_state.lang=="AR" else "Password", type="password")
        if st.button("إرسال" if st.session_state.lang=="AR" else "Submit", use_container_width=True):
            st.success("تم")

    if st.button("🌐 EN/AR", size="small"):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

else:
    # المنصة من الداخل
    st.markdown("<h2 style='text-align:center; color:#f59e0b;'>MA3LOMATI PRO</h2>", unsafe_allow_html=True)
    if st.button("خروج"):
        st.session_state.auth = False; st.rerun()
