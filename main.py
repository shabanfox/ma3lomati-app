import streamlit as st
import pandas as pd

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- الروابط ---
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 2. إدارة الجلسة ---
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 3. CSS التصميم المصغر (Compact Minimalist) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding: 0px !important; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.88), rgba(0,0,0,0.88)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}

    /* الحاوية الصغيرة جداً في المنتصف من فوق */
    .compact-top-wrapper {{
        position: absolute; top: 15px; left: 50%; transform: translateX(-50%);
        width: 100%; max-width: 320px; /* تصغير عرض الحاوية */
        text-align: center; z-index: 1000;
    }}

    /* العنوان الصغير */
    .brand-title-mini {{
        color: #f59e0b; font-size: 28px; /* تصغير العنوان */
        font-weight: 900; margin-bottom: 0px;
        text-shadow: 0 0 10px rgba(245, 158, 11, 0.3);
    }}
    
    .brand-tagline-mini {{ 
        color: #ffffff; font-size: 13px; /* تصغير الوصف */
        margin-bottom: 15px; opacity: 0.7; 
    }}

    /* التبويبات المصغرة */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(255, 255, 255, 0.03) !important;
        border-radius: 10px; height: 35px !important; gap: 10px;
    }}
    .stTabs [data-baseweb="tab"] {{ 
        font-size: 13px !important; color: #fff !important; 
        padding: 0px 10px !important; 
    }}
    .stTabs [aria-selected="true"] {{ color: #f59e0b !important; border-bottom: 2px solid #f59e0b !important; }}

    /* حقول إدخال مصغرة */
    div.stTextInput input, div.stSelectbox div {{
        background: rgba(0, 0, 0, 0.6) !important; color: #fff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 8px !important;
        text-align: center !important; height: 35px !important; /* تقليل الارتفاع */
        font-size: 13px !important;
    }}

    /* الزرار الصغير */
    .stButton button {{
        background: linear-gradient(90deg, #f59e0b, #d97706) !important;
        color: #000 !important; font-weight: 700 !important; font-size: 14px !important;
        border-radius: 8px !important; height: 38px !important;
        border: none !important; margin-top: 10px;
    }}
    
    /* تصغير المسافات بين العناصر */
    .stVerticalBlock {{ gap: 0.5rem !important; }}
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

# --- 5. واجهة الدخول المصغرة ---
if not st.session_state.auth:
    st.markdown("<div class='compact-top-wrapper'>", unsafe_allow_html=True)
    st.markdown("<p class='brand-title-mini'>MA3LOMATI PRO</p>", unsafe_allow_html=True)
    st.markdown("<p class='brand-tagline-mini'>المنصة العقارية الذكية</p>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["🔐 دخول", "📝 اشتراك"])
    
    with t1:
        u = st.text_input("U", placeholder="إسم المستخدم", label_visibility="collapsed", key="u_min")
        p = st.text_input("P", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="p_min")
        if st.button("دخول", use_container_width=True):
            if check_user(u, p):
                st.session_state.auth = True; st.rerun()
            else:
                st.error("البيانات خاطئة")

    with t2:
        st.text_input("N", placeholder="الأسم", label_visibility="collapsed", key="n_min")
        st.text_input("W", placeholder="الواتساب", label_visibility="collapsed", key="w_min")
        st.text_input("E", placeholder="الإيميل", label_visibility="collapsed", key="e_min")
        st.text_input("C", placeholder="الشركة", label_visibility="collapsed", key="c_min")
        if st.button("إرسال الطلب", use_container_width=True):
            st.success("تم الإرسال")
            
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. المحتوى الداخلي ---
else:
    st.markdown("<h2 style='text-align:center; color:#f59e0b; padding-top:80px;'>لوحة التحكم</h2>", unsafe_allow_html=True)
    if st.sidebar.button("خروج"):
        st.session_state.auth = False; st.rerun()
