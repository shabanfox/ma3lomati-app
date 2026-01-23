import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CONSTANTS ---
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'view' not in st.session_state: st.session_state.view = "grid" 
if 'last_menu' not in st.session_state: st.session_state.last_menu = "Launches"

# --- 3. CSS Luxury Design ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; }}
    .block-container {{ padding-top: 2rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
    }}
    /* Login Card Styling */
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; width: 100%; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 24px; font-weight: 900;
        text-align: center; z-index: 10; margin-bottom: -30px; min-width: 360px;
    }}
    .auth-card {{ 
        background-color: #ffffff; width: 450px; padding: 60px 40px 40px 40px; 
        border-radius: 35px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    }}
    /* Inputs Styling */
    div.stTextInput input {{ 
        background-color: #000 !important; color: #fff !important; 
        border: 1px solid #f59e0b !important; border-radius: 12px !important; 
        text-align: center !important; height: 45px !important;
    }}
    .stButton button {{ 
        background-color: #000 !important; color: #f59e0b !important; 
        border: 2px solid #f59e0b !important; border-radius: 12px !important;
        font-weight: 900 !important; height: 50px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Logic Functions ---
def check_auth(u, p):
    try:
        df = pd.read_csv(USER_SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        return not df[(df['Name'].astype(str).str.strip() == str(u).strip()) & 
                     (df['Password'].astype(str).str.strip() == str(p).strip())].empty
    except: return False

# --- 5. UI: LOGIN & REGISTER PAGE ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>منصة معلوماتي العقارية</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    
    mode = st.radio("Select Mode", ["Login / دخول", "Join / اشتراك"], label_visibility="collapsed", horizontal=True)
    st.write("---")

    if mode == "Login / دخول":
        st.markdown("<div class='lock-gold'>🔐</div>", unsafe_allow_html=True)
        u_log = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_l")
        p_log = st.text_input("Pass", type="password", placeholder="كلمة المرور", label_visibility="collapsed", key="p_l")
        if st.button("دخول الآن", use_container_width=True):
            if check_auth(u_log, p_log):
                st.session_state.auth = True; st.rerun()
            else: st.error("بيانات الدخول غير صحيحة")

    else:
        st.markdown("<h3 style='color:#000;'>طلب انضمام جديد</h3>", unsafe_allow_html=True)
        reg_name = st.text_input("Name", placeholder="Name / الاسم الكامل")
        reg_email = st.text_input("Email", placeholder="Email / البريد الإلكتروني")
        reg_wa = st.text_input("WhatsApp", placeholder="WhatsApp / رقم الواتساب")
        reg_comp = st.text_input("Company", placeholder="Company / اسم الشركة")
        reg_pass = st.text_input("Password", type="password", placeholder="Password (Min 8 chars)")
        
        if st.button("إرسال طلب الاشتراك", use_container_width=True):
            # نظام التحقق
            if not all([reg_name, reg_email, reg_wa, reg_comp, reg_pass]):
                st.error("يرجى ملء جميع الخانات المطلوبة!")
            elif len(reg_pass) < 8:
                st.error("عذراً، يجب أن تكون كلمة المرور 8 أرقام أو حروف على الأقل")
            else:
                # هنا يتم عرض البيانات التي سيتم إرسالها (يمكن ربطها بـ Google Sheets API لاحقاً)
                join_date = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.success(f"تم استلام طلبك يا {reg_name} بنجاح!")
                st.info(f"Join Date: {join_date}")
                st.balloons()

    st.markdown("</div>", unsafe_allow_html=True)
    st.write("")
    if st.button("🌐 English / عربي"):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. INTERNAL APP (Simplified Logic for Sample) ---
else:
    st.markdown('<div class="royal-header" style="text-align:center; padding:40px;"><h1 style="color:#f59e0b;">MA3LOMATI PRO</h1></div>', unsafe_allow_html=True)
    
    menu = option_menu(None, ["Tools", "Developers", "Projects", "AI Assistant", "Launches"], 
                       default_index=4, orientation="horizontal",
                       styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
    
    if st.button("🚪 Logout / خروج"):
        st.session_state.auth = False; st.rerun()
    
    st.info(f"Welcome to {menu} page. Data is loading...")
