import streamlit as st
import pandas as pd

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- الروابط ---
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"

# --- 3. CSS مخصص (التمركز العلوي الكامل) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Montserrat:wght@900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    /* إزالة أي هوامش افتراضية من الأعلى */
    .block-container {{ padding-top: 0rem !important; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover;
        font-family: 'Cairo', sans-serif;
    }}

    /* الحاوية الرئيسية تبدأ من أعلى نقطة في الشاشة */
    .hero-wrapper {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        width: 100%;
        padding-top: 30px; /* مسافة بسيطة من حافة المتصفح */
    }}

    /* اسم المنصة الضخم والفخم في المنتصف */
    .brand-name {{
        font-family: 'Montserrat', sans-serif;
        font-size: 55px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(180deg, #f59e0b 0%, #d97706 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: -25px; /* تداخل احترافي مع الكارد */
        z-index: 100;
        letter-spacing: 2px;
        filter: drop-shadow(0px 5px 15px rgba(0,0,0,0.5));
    }}

    /* كارد الدخول المصغر والأنيق */
    .mini-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        width: 350px; /* حجم صغير ومحدد */
        padding: 40px 25px 25px 25px;
        border-radius: 25px;
        border: 1px solid rgba(245, 158, 11, 0.3);
        box-shadow: 0 20px 60px rgba(0,0,0,0.7);
        text-align: center;
    }}

    /* تنسيق التبويبات (Tabs) */
    .stTabs [data-baseweb="tab-list"] {{ justify-content: center; gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{ font-size: 14px !important; color: #888 !important; font-weight: 700 !important; }}
    .stTabs [aria-selected="true"] {{ color: #f59e0b !important; border-bottom-color: #f59e0b !important; }}

    /* تنسيق الحقول */
    .stTextInput>div>div>input {{
        background: rgba(0,0,0,0.3) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        height: 38px !important;
    }}
    
    .stButton>button {{
        border-radius: 12px !important;
        font-weight: 700 !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. دالة التحقق ---
def check_login(u, p):
    try:
        df = pd.read_csv(USER_SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        user_match = df[(df['Name'].astype(str).str.strip() == str(u).strip()) & 
                        (df['Password'].astype(str).str.strip() == str(p).strip())]
        return not user_match.empty
    except: return False

# --- 5. واجهة المستخدم ---
if not st.session_state.auth:
    st.markdown("<div class='hero-wrapper'>", unsafe_allow_html=True)
    
    # الاسم في المنتصف فوق خالص
    st.markdown("<div class='brand-name'>MA3LOMATI</div>", unsafe_allow_html=True)
    
    # صفحة الدخول الصغيرة والجميلة
    st.markdown("<div class='mini-card'>", unsafe_allow_html=True)
    
    t_login, t_signup = st.tabs(["دخول", "اشتراك"] if st.session_state.lang=="AR" else ["Login", "Sign Up"])
    
    with t_login:
        st.write("")
        u_val = st.text_input("الاسم" if st.session_state.lang=="AR" else "Name", key="log_user")
        p_val = st.text_input("كلمة المرور" if st.session_state.lang=="AR" else "Password", type="password", key="log_pass")
        st.write("")
        if st.button("دخول" if st.session_state.lang=="AR" else "Sign In", use_container_width=True, type="primary"):
            if check_login(u_val, p_val):
                st.session_state.auth = True; st.rerun()
            else: st.error("❌")

    with t_signup:
        st.write("")
        st.text_input("الاسم بالكامل" if st.session_state.lang=="AR" else "Full Name")
        st.text_input("واتساب" if st.session_state.lang=="AR" else "WhatsApp")
        st.text_input("الشركة" if st.session_state.lang=="AR" else "Company")
        if st.button("طلب اشتراك" if st.session_state.lang=="AR" else "Join Now", use_container_width=True):
            st.success("📩 تم إرسال طلبك")

    st.write("---")
    if st.button("🌐 Change Language", size="small"):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 6. المنصة من الداخل (بعد تسجيل الدخول) ---
else:
    st.markdown("<h2 style='text-align:center; color:#f59e0b; margin-top:20px;'>MA3LOMATI PRO</h2>", unsafe_allow_html=True)
    st.info("تم تسجيل الدخول بنجاح! ضع كود المنصة هنا.")
    if st.button("Logout"):
        st.session_state.auth = False; st.rerun()
