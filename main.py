import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- روابط الصور والخلفيات ---
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
# رابط الشيت (يجب أن يكون مفعل فيه إذن الكتابة إذا كنت تريد حفظ المشتركين الجدد برمجياً، 
# أو يمكنك استقبال بياناتهم يدوياً، هنا سنركز على التصميم والربط للقراءة)
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"

# --- 3. CSS للتصميم الممركز والفخم ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url('{BG_IMG}');
        background-size: cover; background-position: center;
        font-family: 'Cairo', sans-serif;
    }}

    /* حاوية ممركزة تماماً */
    .main-login-wrapper {{
        display: flex; justify-content: center; align-items: center;
        min-height: 80vh; direction: {"rtl" if st.session_state.lang == "AR" else "ltr"};
    }}

    .auth-card {{
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(20px);
        padding: 40px;
        border-radius: 25px;
        border: 1px solid rgba(245, 158, 11, 0.3);
        width: 100%;
        max-width: 450px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        text-align: center;
    }}
    
    .stTextInput>div>div>input {{
        background: rgba(255,255,255,0.1) !important;
        color: white !important; border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }}
    
    .gold-text {{ color: #f59e0b; font-weight: 900; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Authentication Logic ---
def check_auth(u, p):
    try:
        df = pd.read_csv(USER_SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        match = df[(df['Name'].astype(str).str.strip() == str(u).strip()) & 
                   (df['Password'].astype(str).str.strip() == str(p).strip())]
    except: return False

# --- 5. Auth UI (Login & Sign Up) ---
if not st.session_state.auth:
    st.markdown("<div class='main-login-wrapper'>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
        st.markdown("<h1 class='gold-text'>MA3LOMATI</h1>", unsafe_allow_html=True)
        
        # تبويبات داخل الكارد للتبديل بين دخول واشتراك
        tab_login, tab_signup = st.tabs(["تسجيل الدخول", "إنشاء حساب جديد"] if st.session_state.lang=="AR" else ["Login", "Sign Up"])
        
        with tab_login:
            st.write("")
            u_in = st.text_input("الاسم" if st.session_state.lang=="AR" else "Name", key="li_u")
            p_in = st.text_input("كلمة المرور" if st.session_state.lang=="AR" else "Password", type="password", key="li_p")
            if st.button("دخول" if st.session_state.lang=="AR" else "Login", use_container_width=True, type="primary"):
                # هنا نضع دالة check_auth
                st.session_state.auth = True # للتجربة الآن
                st.rerun()

        with tab_signup:
            st.write("")
            new_name = st.text_input("الاسم بالكامل" if st.session_state.lang=="AR" else "Full Name")
            new_email = st.text_input("البريد الإلكتروني" if st.session_state.lang=="AR" else "Email")
            new_whatsapp = st.text_input("واتساب" if st.session_state.lang=="AR" else "WhatsApp")
            new_company = st.text_input("الشركة" if st.session_state.lang=="AR" else "Company")
            new_pass = st.text_input("كلمة مرور جديدة" if st.session_state.lang=="AR" else "New Password", type="password")
            
            if st.button("إرسال طلب اشتراك" if st.session_state.lang=="AR" else "Request Access", use_container_width=True):
                st.success("تم إرسال بياناتك للمراجعة" if st.session_state.lang=="AR" else "Request sent for approval")

        st.write("---")
        if st.button("🌐 Change Language", size="small"):
            st.session_state.lang = "EN" if st.session_state.lang == "AR" else "AR"
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # المنصة من الداخل (كودك الأصلي)
    st.title("مرحباً بك في المنصة")
    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()
