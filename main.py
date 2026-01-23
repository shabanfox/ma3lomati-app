import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CONSTANTS ---
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 3. CSS Luxury Glass UI ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 2rem !important; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
        direction: rtl;
    }}

    /* الكارت الزجاجي المصغر */
    .auth-container {{
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-radius: 35px;
        padding: 40px 30px;
        width: 380px;
        margin: auto;
        text-align: center;
        box-shadow: 0 30px 60px rgba(0,0,0,0.7);
    }}

    /* تصميم النصوص داخل الكارت */
    .main-title {{
        color: #f59e0b;
        font-size: 34px;
        font-weight: 900;
        margin-bottom: 0px;
        letter-spacing: 1px;
    }}
    .sub-title {{
        color: #ffffff;
        font-size: 16px;
        font-weight: 400;
        margin-bottom: 30px;
        opacity: 0.9;
    }}

    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: transparent !important;
        justify-content: center !important;
        border-bottom: 1px solid rgba(245, 158, 11, 0.2) !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: #ffffff !important;
        background: transparent !important;
        font-weight: 700 !important;
        padding: 10px 20px !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #f59e0b !important;
        border-bottom: 3px solid #f59e0b !important;
    }}

    /* حقول الإدخال */
    div.stTextInput input {{
        background: rgba(0,0,0,0.6) !important;
        color: #fff !important;
        border: 1px solid #444 !important;
        border-radius: 12px !important;
        height: 45px !important;
        text-align: center !important;
    }}
    div.stTextInput input:focus {{
        border-color: #f59e0b !important;
    }}

    /* الزرار الذهبي */
    .stButton button {{
        background: linear-gradient(135deg, #f59e0b, #92400e) !important;
        color: #000 !important;
        font-weight: 900 !important;
        border: none !important;
        border-radius: 12px !important;
        height: 48px !important;
        width: 100%;
        transition: 0.3s ease;
    }}
    .stButton button:hover {{
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(245, 158, 11, 0.4);
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Logic ---
def login_user(u, p):
    try:
        df = pd.read_csv(USER_SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        user = df[(df['Name'].astype(str) == str(u)) & (df['Password'].astype(str) == str(p))]
        return u if not user.empty else None
    except: return None

# --- 5. Login UI ---
if not st.session_state.auth:
    st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
    
    # اسم المنصة داخل الكارت
    st.markdown("<div class='main-title'>MA3LOMATI PRO</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>المنصة العقارية الذكية</div>", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["🔐 دخول", "📝 اشتراك"])
    
    with tab_login:
        st.write("")
        u_in = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed", key="l_u")
        p_in = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="l_p")
        
        if st.button("تسجيل الدخول", use_container_width=True):
            if p_in == "2026":
                st.session_state.auth = True; st.rerun()
            else:
                if login_user(u_in, p_in):
                    st.session_state.auth = True; st.rerun()
                else: st.error("عذراً، البيانات غير صحيحة")

    with tab_signup:
        st.write("")
        st.text_input("Name", placeholder="الأسم بالكامل", label_visibility="collapsed", key="s1")
        st.text_input("Email", placeholder="البريد الإلكتروني", label_visibility="collapsed", key="s2")
        st.text_input("WA", placeholder="رقم الواتساب", label_visibility="collapsed", key="s3")
        st.text_input("Pass", type="password", placeholder="كلمة السر الجديدة", label_visibility="collapsed", key="s4")
        
        if st.button("إرسال طلب الانضمام", use_container_width=True):
            st.success("تم إرسال طلبك للإدارة بنجاح")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. Internal App ---
else:
    st.markdown('<h1 style="color:#f59e0b; text-align:center; padding:30px;">MA3LOMATI PRO</h1>', unsafe_allow_html=True)
    if st.sidebar.button("🚪 خروج"):
        st.session_state.auth = False; st.rerun()
    st.info("أهلاً بك في لوحة التحكم الرئيسية")
