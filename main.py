import streamlit as st
import pandas as pd

# --- 1. Page Config ---
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", initial_sidebar_state="collapsed")

# --- روابط البيانات ---
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"

# --- 2. Custom CSS (تصميم نظيف وممركز علوياً) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إزالة الفراغ الأبيض العلوي تماماً */
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0rem !important; margin-top: 0rem !important; }
    [data-testid="stAppViewContainer"] { background-color: #f8f9fa; font-family: 'Cairo', sans-serif; }

    .main-container {
        display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
        width: 100%; padding-top: 10px;
    }

    /* العنوان البيضاوي الفخم - خلفية سوداء فريم ذهبي */
    .oval-header {
        background-color: #000;
        border: 3px solid #f59e0b;
        border-radius: 50px; /* شكل بيضاوي انسيابي */
        padding: 15px 40px;
        color: #f59e0b;
        font-size: 24px;
        font-weight: 900;
        text-align: center;
        z-index: 10;
        margin-bottom: -20px;
        min-width: 320px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    /* كارت واحد فقط - خلفية بيضاء */
    .login-card {
        background-color: #ffffff;
        width: 360px;
        padding: 40px 30px 25px 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
    }

    /* رمز القفل الذهبي */
    .lock-icon { font-size: 35px; color: #f59e0b; margin-bottom: 5px; }

    /* الحقول: خلفية سوداء - نص أبيض */
    .stTextInput input {
        background-color: #111 !important;
        color: #fff !important;
        border: 1px solid #f59e0b !important;
        border-radius: 8px !important;
        height: 40px !important;
        text-align: center;
    }

    /* زر الدخول الذهبي الأسود */
    .stButton>button {
        background-color: #000 !important;
        color: #f59e0b !important;
        border: 2px solid #f59e0b !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #f59e0b !important; color: #000 !important; }

    /* تنسيق التبويبات داخل الكارت */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 10px; }
    .stTabs [data-baseweb="tab"] { color: #888 !important; font-size: 14px !important; }
    .stTabs [aria-selected="true"] { color: #f59e0b !important; border-bottom-color: #f59e0b !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. Logic ---
if 'auth' not in st.session_state: st.session_state.auth = False

def validate_user(u, p):
    try:
        df = pd.read_csv(USER_SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        match = df[(df['Name'].astype(str).str.strip() == str(u).strip()) & 
                   (df['Password'].astype(str).str.strip() == str(p).strip())]
        return not match.empty
    except: return False

# --- 4. UI ---
if not st.session_state.auth:
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    
    # الإطار البيضاوي (العنوان)
    st.markdown("<div class='oval-header'>منصة معلوماتي العقارية</div>", unsafe_allow_html=True)
    
    # الكارت الموحد
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    st.markdown("<div class='lock-icon'>🔒</div>", unsafe_allow_html=True)
    
    tab_log, tab_sign = st.tabs(["تسجيل الدخول", "طلب اشتراك"])
    
    with tab_log:
        st.write("")
        user = st.text_input("اسم المستخدم", placeholder="الاسم", label_visibility="collapsed", key="l1")
        pwd = st.text_input("كلمة المرور", type="password", placeholder="كلمة المرور", label_visibility="collapsed", key="l2")
        if st.button("دخول"):
            if validate_user(user, pwd):
                st.session_state.auth = True; st.rerun()
            else: st.error("خطأ في البيانات")
            
    with tab_sign:
        st.write("")
        st.text_input("الاسم", placeholder="الاسم الكامل", label_visibility="collapsed", key="s1")
        st.text_input("الواتساب", placeholder="رقم الواتساب", label_visibility="collapsed", key="s2")
        st.text_input("الشركة", placeholder="اسم الشركة", label_visibility="collapsed", key="s3")
        if st.button("إرسال الطلب"):
            st.success("تم إرسال طلبك بنجاح")
            
    st.markdown("</div></div>", unsafe_allow_html=True)

else:
    # محتوى المنصة بعد الدخول
    st.title("مرحباً بك في منصة معلوماتي")
    if st.button("تسجيل خروج"):
        st.session_state.auth = False; st.rerun()
