import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import requests # مكتبة ضرورية للربط

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CONSTANTS ---
# تم إضافة رابط السكريبت للربط
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
ITEMS_PER_PAGE = 6

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'view' not in st.session_state: st.session_state.view = "grid" 
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'last_menu' not in st.session_state: st.session_state.last_menu = "Launches"
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 3. Functions (Auth & Signup) ---
def check_auth(u, p):
    try:
        df = pd.read_csv(USER_SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        return not df[(df['Name'].astype(str) == str(u)) & (df['Password'].astype(str) == str(p))].empty
    except: return False

def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        return response.text == "Success"
    except: return False

# --- 4. CSS Luxury Design (نفس تصميمك بدون تعديل) ---
direction = "rtl" if st.session_state.lang == "AR" else "ltr"
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {direction} !important; font-family: 'Cairo', sans-serif;
    }}
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: flex-start; width: 100%; padding-top: 20px; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 24px; font-weight: 900;
        text-align: center; z-index: 10; margin-bottom: -30px; min-width: 360px;
    }}
    .auth-card {{ background-color: #ffffff; width: 380px; padding: 55px 35px 30px 35px; border-radius: 30px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); }}
    .lock-gold {{ font-size: 45px; color: #f59e0b; margin-bottom: 5px; }}
    .auth-card div.stTextInput input {{ background-color: #000 !important; color: #fff !important; border: 1px solid #f59e0b !important; border-radius: 12px !important; text-align: center !important; height: 45px !important; }}
    /* ... باقي الـ CSS الخاص بك ... */
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIN & REGISTER PAGE ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>منصة معلوماتي العقارية</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.markdown("<div class='lock-gold'>🔒</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Login / دخول", "Register / اشتراك"])
    
    with tab1:
        u = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed", key="login_u")
        p = st.text_input("Pass", type="password", placeholder="كلمة المرور", label_visibility="collapsed", key="login_p")
        if st.button("SIGN IN", use_container_width=True):
            if check_auth(u, p): 
                st.session_state.auth = True
                st.rerun()
            else: st.error("خطأ في البيانات")
            
    with tab2:
        # حقول الاشتراك المربوطة بالشيت
        reg_name = st.text_input("Full Name / الاسم", placeholder="الاسم بالكامل", key="rn")
        reg_email = st.text_input("Email / الإيميل", placeholder="example@gmail.com", key="re")
        reg_pass = st.text_input("Password / كلمة السر", type="password", placeholder="Password", key="rp")
        reg_wa = st.text_input("WhatsApp / واتساب", placeholder="01xxxxxxxxx", key="rw")
        reg_comp = st.text_input("Company / الشركة", placeholder="اسم الشركة", key="rc")
        
        if st.button("CREATE ACCOUNT", use_container_width=True):
            if reg_name and reg_email and reg_pass:
                with st.spinner("جاري تسجيل بياناتك..."):
                    if signup_user(reg_name, reg_pass, reg_email, reg_wa, reg_comp):
                        st.success("تم الاشتراك بنجاح! يمكنك الدخول الآن")
                    else:
                        st.error("فشل الاتصال بالسيرفر، تأكد من إعدادات الشيت")
            else:
                st.warning("يرجى ملء الحقول الأساسية")
                
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("🌐 Change Language / تغيير اللغة"):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. باقي كود المنصة الخاص بك (بدون أي تعديل) ---
# ... استكمل الكود الخاص بك من هنا ...
