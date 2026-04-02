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

# --- 3. CSS (تصميم الاسم فوق الكارت الزجاجي) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Orbitron:wght@900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover;
        font-family: 'Cairo', sans-serif;
    }}

    /* الحاوية العلوية المركزية */
    .hero-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        width: 100%;
        padding-top: 50px;
    }}

    /* اسم المنصة الضخم الذي يغطي جزءاً من الكارت */
    .brand-overlay {{
        font-family: 'Orbitron', sans-serif;
        font-size: 58px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(180deg, #f59e0b 20%, #78350f 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        z-index: 10; /* فوق الكارت */
        margin-bottom: -45px; /* تداخل عميق لإظهار الكارت كخلفية */
        letter-spacing: 4px;
        filter: drop-shadow(0px 10px 20px rgba(0,0,0,0.8));
    }}

    /* الكارت المصغر كخلفية (Glassmorphism) */
    .glass-card {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        width: 340px;
        padding: 60px 25px 25px 25px; /* Padding علوي لترك مساحة للاسم */
        border-radius: 30px;
        border: 1px solid rgba(245, 158, 11, 0.2);
        box-shadow: 0 30px 60px rgba(0,0,0,0.9);
        text-align: center;
        z-index: 1;
    }}

    /* تنسيق العناصر الداخلية */
    .stTabs [data-baseweb="tab-list"] {{ justify-content: center; gap: 8px; }}
    .stTabs [data-baseweb="tab"] {{ font-size: 13px !important; color: #666 !important; }}
    .stTabs [aria-selected="true"] {{ color: #f59e0b !important; border-bottom-color: #f59e0b !important; }}

    .stTextInput input {{
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 15px !important;
        height: 35px !important;
        text-align: center;
    }}

    .stButton>button {{
        background-color: #f59e0b !important;
        color: black !important;
        border-radius: 15px !important;
        font-weight: 900 !important;
        border: none !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. التحقق من البيانات ---
def do_login(u, p):
    try:
        df = pd.read_csv(USER_SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        check = df[(df['Name'].astype(str).str.strip() == str(u).strip()) & 
                   (df['Password'].astype(str).str.strip() == str(p).strip())]
        return not check.empty
    except: return False

# --- 5. واجهة الدخول ---
if not st.session_state.auth:
    st.markdown("<div class='hero-container'>", unsafe_allow_html=True)
    
    # الاسم "راكب" فوق الكارت
    st.markdown("<div class='brand-overlay'>MA3LOMATI</div>", unsafe_allow_html=True)
    
    # الكارت الزجاجي كخلفية للاسم وللحقول
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    
    tab_l, tab_s = st.tabs(["دخول", "اشتراك"] if st.session_state.lang=="AR" else ["Login", "Sign Up"])
    
    with tab_l:
        st.write("")
        u_in = st.text_input("Username" if st.session_state.lang=="EN" else "الاسم", key="u_log")
        p_in = st.text_input("Password" if st.session_state.lang=="EN" else "كلمة المرور", type="password", key="p_log")
        if st.button("LOG IN" if st.session_state.lang=="EN" else "دخول", use_container_width=True):
            if do_login(u_in, p_in):
                st.session_state.auth = True; st.rerun()
            else: st.error("❌")

    with tab_s:
        st.write("")
        st.text_input("WhatsApp" if st.session_state.lang=="EN" else "واتساب")
        st.text_input("Company" if st.session_state.lang=="EN" else "الشركة")
        if st.button("JOIN" if st.session_state.lang=="EN" else "طلب انضمام", use_container_width=True):
            st.success("Sent")

    st.write("---")
    if st.button("🌐 AR / EN", size="small"):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 6. المنصة من الداخل ---
else:
    st.markdown("<h1 style='text-align:center; color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state.auth = False; st.rerun()
