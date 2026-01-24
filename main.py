import streamlit as st
import pandas as pd

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- الروابط ---
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 2. إدارة الجلسة ---
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 3. CSS "السنترة المطلقة في قلب الشاشة" ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الزوائد */
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding: 0px !important; }}

    /* خلفية كاملة وسنترة المحتوى */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)), url('{BG_IMG}');
        background-size: cover; 
        background-position: center;
        display: flex !important;
        align-items: center !important; /* سنترة طولية */
        justify-content: center !important; /* سنترة عرضية */
        height: 100vh;
        direction: rtl !important;
        font-family: 'Cairo', sans-serif;
    }}

    /* حاوية ملمومة في السنتر */
    .center-card-box {{
        width: 100%;
        max-width: 310px;
        text-align: center;
        padding: 10px;
    }}

    /* اسم المنصة في السنتر */
    .brand-title-center {{
        color: #f59e0b;
        font-size: 30px;
        font-weight: 900;
        margin-bottom: 0px;
        text-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
    }}
    
    .brand-subtitle-center {{
        color: #ffffff;
        font-size: 13px;
        opacity: 0.6;
        margin-bottom: 20px;
        letter-spacing: 0.5px;
    }}

    /* تبويبات ملمومة */
    .stTabs [data-baseweb="tab-list"] {{
        background: transparent !important;
        gap: 10px;
        justify-content: center !important;
        margin-bottom: 15px;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-size: 14px !important;
        color: #888 !important;
        padding: 5px 12px !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #f59e0b !important;
        border-bottom: 2px solid #f59e0b !important;
    }}

    /* خانات إدخال مصغرة */
    div.stTextInput input {{
        background: rgba(255, 255, 255, 0.04) !important;
        color: #fff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        height: 40px !important;
        font-size: 14px !important;
        text-align: center !important;
        margin-bottom: 5px;
    }}

    /* زرار الدخول المنسق */
    .stButton button {{
        background: linear-gradient(90deg, #f59e0b, #d97706) !important;
        color: #000 !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        height: 42px !important;
        width: 100%;
        border: none !important;
        margin-top: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. دالة التحقق من الشيت ---
def check_user(u, p):
    try:
        df = pd.read_csv(USER_SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        match = df[(df['Name'].astype(str) == str(u)) & (df['Password'].astype(str) == str(p))]
        return not match.empty
    except: return False

# --- 5. واجهة تسجيل الدخول (في قلب الشاشة) ---
if not st.session_state.auth:
    # استخدام div للسنترة
    st.markdown("<div class='center-card-box'>", unsafe_allow_html=True)
    
    st.markdown("<p class='brand-title-center'>MA3LOMATI PRO</p>", unsafe_allow_html=True)
    st.markdown("<p class='brand-subtitle-center'>المنصة العقارية الذكية</p>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["🔐 دخول", "📝 اشتراك"])
    
    with t1:
        u_in = st.text_input("U", placeholder="إسم المستخدم", label_visibility="collapsed", key="u_final")
        p_in = st.text_input("P", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="p_final")
        if st.button("دخول للمنصة", use_container_width=True):
            if check_user(u_in, p_in):
                st.session_state.auth = True; st.rerun()
            else:
                st.error("البيانات غير صحيحة")

    with t2:
        st.text_input("N", placeholder="الأسم الكامل", label_visibility="collapsed", key="n_final")
        st.text_input("W", placeholder="الواتساب", label_visibility="collapsed", key="w_final")
        if st.button("إرسال الطلب", use_container_width=True):
            st.success("تم استلام طلبك")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. المحتوى الداخلي ---
else:
    st.markdown("<h3 style='text-align:center; color:#f59e0b; padding-top:40px;'>مرحباً بك في المنصة</h3>", unsafe_allow_html=True)
    if st.sidebar.button("خروج"):
        st.session_state.auth = False; st.rerun()
