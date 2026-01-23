import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- روابط الصور والبيانات ---
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"

# --- 3. Custom CSS (The Luxury Look) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Orbitron:wght@900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover;
        font-family: 'Cairo', sans-serif;
    }}

    /* الحاوية الرئيسية لتوسيط الكارد */
    .main-wrapper {{
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        min-height: 80vh; padding-top: 50px;
    }}

    /* اسم المنصة الضخم فوق الكارد */
    .super-title {{
        font-family: 'Orbitron', sans-serif;
        font-size: 70px; font-weight: 900;
        background: linear-gradient(180deg, #f59e0b 30%, #78350f 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: -40px; /* لجعله يتداخل مع الكارد */
        z-index: 10; position: relative;
        text-shadow: 0px 10px 20px rgba(0,0,0,0.5);
    }}

    /* كارد تسجيل الدخول الصغير والفخم */
    .mini-auth-card {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(30px);
        width: 350px; padding: 50px 30px 30px 30px;
        border-radius: 30px;
        border: 1px solid rgba(245, 158, 11, 0.2);
        box-shadow: 0 25px 50px rgba(0,0,0,0.8);
        text-align: center;
    }}

    /* تعديل التبويبات */
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{
        font-size: 14px !important; height: 35px !important; color: #888 !important;
    }}
    .stTabs [aria-selected="true"] {{ color: #f59e0b !important; }}

    /* تصغير خانات الإدخال */
    .stTextInput input {{
        height: 35px !important; font-size: 14px !important;
        background: rgba(0,0,0,0.2) !important; border: 1px solid #333 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Logic & UI ---
if not st.session_state.auth:
    # عرض الصفحة
    st.markdown("<div class='main-wrapper'>", unsafe_allow_html=True)
    
    # الاسم الضخم
    st.markdown("<h1 class='super-title'>MA3LOMATI</h1>", unsafe_allow_html=True)
    
    # الكارد الصغير
    st.markdown("<div class='mini-auth-card'>", unsafe_allow_html=True)
    
    tab_in, tab_up = st.tabs(["Login", "Sign Up"] if st.session_state.lang=="EN" else ["دخول", "اشتراك"])
    
    with tab_in:
        u = st.text_input("Name" if st.session_state.lang=="EN" else "الاسم", key="li_u")
        p = st.text_input("Pass" if st.session_state.lang=="EN" else "كلمة المرور", type="password", key="li_p")
        if st.button("GO" if st.session_state.lang=="EN" else "دخول", use_container_width=True, type="primary"):
            # دالة الربط بالشيت
            try:
                df = pd.read_csv(USER_SHEET_URL)
                df.columns = [c.strip() for c in df.columns]
                if any((df['Name'].astype(str) == u) & (df['Password'].astype(str) == p)):
                    st.session_state.auth = True; st.rerun()
                else: st.error("❌")
            except: st.error("Error")

    with tab_up:
        st.text_input("WhatsApp" if st.session_state.lang=="EN" else "واتساب")
        st.text_input("Company" if st.session_state.lang=="EN" else "الشركة")
        st.text_input("Pass" if st.session_state.lang=="EN" else "الباسورد", type="password")
        if st.button("Join" if st.session_state.lang=="EN" else "طلب انضمام", use_container_width=True):
            st.success("Sent")

    st.write("---")
    if st.button("🌐 EN/AR", size="small"):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()

    st.markdown("</div>", unsafe_allow_html=True) # قفل الكارد
    st.markdown("</div>", unsafe_allow_html=True) # قفل الحاوية

else:
    # --- المنصة من الداخل (كودك الأصلي) ---
    st.markdown(f"<h1 style='color:#f59e0b; text-align:center;'>Welcome to MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state.auth = False; st.rerun()
