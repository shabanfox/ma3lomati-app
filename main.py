import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- الروابط الأساسية ---
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"

# --- 3. Custom CSS (التركيز على الفخامة والمركزية) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Montserrat:wght@900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover;
        font-family: 'Cairo', sans-serif;
    }}

    /* حاوية التمركز المطلق */
    .auth-wrapper {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 90vh;
        width: 100%;
    }}

    /* تصميم الاسم الفخم المتداخل */
    .brand-overlay {{
        font-family: 'Montserrat', sans-serif;
        font-size: 65px;
        font-weight: 900;
        letter-spacing: -2px;
        background: linear-gradient(180deg, #f59e0b 0%, #d97706 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: -35px; /* تداخل مقصود مع الكارد */
        z-index: 10;
        filter: drop-shadow(0px 5px 15px rgba(0,0,0,0.5));
    }}

    /* الكارد المصغر */
    .auth-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        width: 360px;
        padding: 50px 25px 30px 25px;
        border-radius: 25px;
        border: 1px solid rgba(245, 158, 11, 0.3);
        box-shadow: 0 25px 50px rgba(0,0,0,0.6);
        text-align: center;
    }}

    /* تنسيق التبويبات */
    .stTabs [data-baseweb="tab-list"] {{
        justify-content: center;
        gap: 15px;
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 40px;
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #888 !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #f59e0b !important;
    }}

    /* تصغير مدخلات البيانات */
    .stTextInput>div>div>input {{
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        height: 40px !important;
        border-radius: 10px !important;
    }}
    
    .stButton>button {{
        border-radius: 10px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. دالة التحقق من البيانات ---
def validate_login(user, pwd):
    try:
        df = pd.read_csv(USER_SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        u_clean = str(user).strip()
        p_clean = str(pwd).strip()
        # البحث في الشيت
        match = df[(df['Name'].astype(str).str.strip() == u_clean) & 
                   (df['Password'].astype(str).str.strip() == p_clean)]
        return not match.empty
    except:
        return False

# --- 5. منطق العرض (Login/Signup) ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    
    # الاسم الضخم فوق الكارد مباشرة
    st.markdown("<div class='brand-overlay'>MA3LOMATI</div>", unsafe_allow_html=True)
    
    # بداية الكارد
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    
    # تبويبات الدخول والاشتراك
    tab_l, tab_s = st.tabs(["تسجيل الدخول", "إنشاء حساب"] if st.session_state.lang == "AR" else ["Login", "Sign Up"])
    
    with tab_l:
        st.write("")
        u = st.text_input("الاسم" if st.session_state.lang=="AR" else "Name", key="user_val")
        p = st.text_input("كلمة المرور" if st.session_state.lang=="AR" else "Password", type="password", key="pass_val")
        st.write("")
        if st.button("دخول" if st.session_state.lang=="AR" else "Sign In", use_container_width=True, type="primary"):
            if validate_login(u, p):
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("بيانات غير صحيحة" if st.session_state.lang=="AR" else "Invalid Credentials")

    with tab_s:
        st.write("")
        st.text_input("الاسم الكامل" if st.session_state.lang=="AR" else "Full Name", key="reg_name")
        st.text_input("رقم الواتساب" if st.session_state.lang=="AR" else "WhatsApp", key="reg_wa")
        st.text_input("الشركة" if st.session_state.lang=="AR" else "Company", key="reg_co")
        st.text_input("كلمة المرور" if st.session_state.lang=="AR" else "Password", type="password", key="reg_pass")
        if st.button("إرسال الطلب" if st.session_state.lang=="AR" else "Register", use_container_width=True):
            st.success("تم الإرسال للمراجعة" if st.session_state.lang=="AR" else "Sent for approval")

    st.write("---")
    if st.button("🌐 English / العربية", use_container_width=True):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True) # قفل الكارد
    st.markdown("</div>", unsafe_allow_html=True) # قفل الحاوية

# --- 6. المنصة من الداخل (بعد تسجيل الدخول) ---
else:
    st.markdown(f"<h1 style='color:#f59e0b; text-align:center; margin-top:50px;'>MA3LOMATI PRO PLATFORM</h1>", unsafe_allow_html=True)
    st.write("---")
    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()
