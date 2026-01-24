import streamlit as st
import pandas as pd

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- الروابط ---
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 2. إدارة الجلسة ---
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 3. CSS التصميم (توسيط مطلق + عناصر مصغرة) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding: 0px !important; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)), url('{BG_IMG}');
        background-size: cover; background-position: center;
        direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}

    /* حاوية التوسيط المطلق في قلب الصفحة */
    .absolute-center {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        width: 100%;
        text-align: center;
    }}

    .compact-box {{
        width: 100%;
        max-width: 300px; /* ملموم جداً */
    }}

    /* عنوان المنصة في المنتصف */
    .brand-main-title {{
        color: #f59e0b;
        font-size: 32px; /* حجم متوسط وأنيق */
        font-weight: 900;
        margin-bottom: 5px;
        text-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
    }}
    
    .brand-subtitle {{
        color: #ffffff;
        font-size: 14px;
        opacity: 0.6;
        margin-bottom: 25px;
    }}

    /* تبويبات مصغرة */
    .stTabs [data-baseweb="tab-list"] {{
        background: transparent !important;
        gap: 15px; justify-content: center !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-size: 14px !important; color: #888 !important;
        padding: 5px 10px !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #f59e0b !important;
        border-bottom: 2px solid #f59e0b !important;
    }}

    /* حقول إدخال نحيفة */
    div.stTextInput input {{
        background: rgba(255, 255, 255, 0.03) !important;
        color: #fff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        height: 38px !important;
        font-size: 13px !important;
        text-align: center !important;
    }}

    /* زرار دخول صغير */
    .stButton button {{
        background: #f59e0b !important;
        color: #000 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        height: 40px !important;
        font-size: 14px !important;
        border: none !important;
        margin-top: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. دالة التحقق ---
def check_user(username, password):
    try:
        df = pd.read_csv(USER_SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        match = df[(df['Name'].astype(str) == str(username)) & 
                   (df['Password'].astype(str) == str(password))]
        return not match.empty
    except: return False

# --- 5. واجهة المستخدم (توسيط كامل) ---
if not st.session_state.auth:
    st.markdown("<div class='absolute-center'>", unsafe_allow_html=True)
    st.markdown("<div class='compact-box'>", unsafe_allow_html=True)
    
    # اسم المنصة في المنتصف
    st.markdown("<p class='brand-main-title'>MA3LOMATI PRO</p>", unsafe_allow_html=True)
    st.markdown("<p class='brand-subtitle'>المنصة العقارية الذكية</p>", unsafe_allow_html=True)
    
    t_login, t_join = st.tabs(["دخول", "اشتراك"])
    
    with t_login:
        u = st.text_input("اسم المستخدم", placeholder="User", label_visibility="collapsed", key="u_abs")
        p = st.text_input("كلمة السر", type="password", placeholder="Pass", label_visibility="collapsed", key="p_abs")
        if st.button("دخول للمنصة", use_container_width=True):
            if check_user(u, p):
                st.session_state.auth = True; st.rerun()
            else:
                st.error("البيانات خاطئة")

    with t_join:
        st.text_input("الأسم", placeholder="الأسم", label_visibility="collapsed", key="n_abs")
        st.text_input("الهاتف", placeholder="الهاتف", label_visibility="collapsed", key="w_abs")
        if st.button("طلب انضمام", use_container_width=True):
            st.success("تم الإرسال")
            
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. المحتوى الداخلي ---
else:
    st.markdown("<h3 style='text-align:center; color:#f59e0b; padding-top:40px;'>لوحة التحكم</h3>", unsafe_allow_html=True)
    if st.sidebar.button("خروج"):
        st.session_state.auth = False; st.rerun()
