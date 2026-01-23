import streamlit as st
import pandas as pd

# --- 1. Page Config ---
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", initial_sidebar_state="collapsed")

# --- روابط ---
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"

# --- 2. Custom CSS (التصميم البيضاوي والذهبي) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الهوامش العلوية تماماً */
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0rem !important; margin-top: 0rem !important; }
    [data-testid="stAppViewContainer"] { background-color: #f0f2f6; font-family: 'Cairo', sans-serif; }

    .main-container {
        display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
        width: 100%; padding-top: 20px;
    }

    /* الشعار البيضاوي الفخم */
    .oval-header {
        background-color: #000;
        border: 3px solid #f59e0b;
        border-radius: 50% / 100%; /* شكل بيضاوي */
        padding: 20px 60px;
        color: #f59e0b;
        font-size: 32px;
        font-weight: 900;
        text-align: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        margin-bottom: -20px;
        z-index: 10;
        min-width: 400px;
    }

    /* كارت الدخول الأبيض */
    .login-box {
        background-color: #ffffff;
        width: 400px;
        padding: 60px 40px 40px 40px;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        text-align: center;
    }

    /* رمز القفل الذهبي */
    .lock-icon {
        font-size: 40px;
        color: #f59e0b;
        margin-bottom: 10px;
    }

    /* حقول الإدخال (أسود بخط أبيض) */
    .stTextInput input {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #f59e0b !important;
        border-radius: 10px !important;
        height: 45px !important;
        text-align: center;
    }

    /* زر الدخول */
    .stButton>button {
        background-color: #000 !important;
        color: #f59e0b !important;
        border: 2px solid #f59e0b !important;
        border-radius: 10px !important;
        font-weight: 900 !important;
        width: 100%;
        height: 45px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #f59e0b !important;
        color: #000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. التحقق من الدخول ---
if 'auth' not in st.session_state: st.session_state.auth = False

def check_login(u, p):
    try:
        df = pd.read_csv(USER_SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        match = df[(df['Name'].astype(str).str.strip() == str(u).strip()) & 
                   (df['Password'].astype(str).str.strip() == str(p).strip())]
        return not match.empty
    except: return False

# --- 4. واجهة المستخدم ---
if not st.session_state.auth:
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    # الجملة في الإطار البيضاوي الأسود بحد ذهبي
    st.markdown("<div class='oval-header'>منصة معلوماتي العقارية</div>", unsafe_allow_html=True)
    
    # الكارت الأبيض تحتها
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    
    # رمز القفل الذهبي
    st.markdown("<div class='lock-icon'>🔒</div>", unsafe_allow_html=True)
    
    u_name = st.text_input("اسم المستخدم", placeholder="ادخل الاسم هنا", label_visibility="collapsed")
    u_pass = st.text_input("كلمة المرور", type="password", placeholder="كلمة المرور", label_visibility="collapsed")
    
    st.write("") # مسافة بسيطة
    
    if st.button("دخول"):
        if check_login(u_name, u_pass):
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("بيانات الدخول غير صحيحة")
            
    st.markdown("</div></div>", unsafe_allow_html=True)

else:
    # المنصة من الداخل
    st.success("تم تسجيل الدخول بنجاح")
    if st.button("خروج"):
        st.session_state.auth = False
        st.rerun()
