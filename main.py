import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- روابط البيانات (رابط الشيت الذي أرسلته) ---
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 2. إدارة الجلسة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 3. تصميم الـ CSS (المنتصف من فوق + بدون كروت) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding: 0px !important; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}

    /* الحاوية: منتصف عرضاً ومن فوق طولاً */
    .top-center-container {{
        position: absolute;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 420px;
        text-align: center;
        z-index: 1000;
    }}

    .brand-title {{
        color: #f59e0b;
        font-size: 50px;
        font-weight: 900;
        margin-bottom: 0px;
        text-shadow: 0 0 20px rgba(245, 158, 11, 0.5);
    }}
    
    .brand-tagline {{
        color: #ffffff;
        font-size: 18px;
        margin-bottom: 30px;
        opacity: 0.8;
    }}

    /* تصميم التبويبات */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px;
        justify-content: center !important;
        border: none !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #f59e0b !important;
        border-bottom: 2px solid #f59e0b !important;
    }}

    /* حقول الإدخال */
    div.stTextInput input {{
        background: rgba(0, 0, 0, 0.7) !important;
        color: #fff !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 12px !important;
        height: 50px !important;
        text-align: center !important;
    }}

    /* الزرار */
    .stButton button {{
        background: linear-gradient(90deg, #f59e0b, #d97706) !important;
        color: #000 !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        height: 50px !important;
        border: none !important;
        margin-top: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. دالة التحقق من الشيت ---
def check_user(username, password):
    try:
        # جلب البيانات من الرابط الذي أرسلته
        df = pd.read_csv(USER_SHEET_URL)
        df.columns = [c.strip() for c in df.columns] # إزالة أي مسافات من أسماء الأعمدة
        
        # البحث عن الاسم والباسورد (تأكد أن الأعمدة في الشيت اسمها Name و Password)
        match = df[(df['Name'].astype(str) == str(username)) & 
                   (df['Password'].astype(str) == str(password))]
        return not match.empty
    except Exception as e:
        st.error(f"خطأ في الاتصال بالشيت: {e}")
        return False

# --- 5. واجهة تسجيل الدخول والاشتراك ---
if not st.session_state.auth:
    st.markdown("<div class='top-center-container'>", unsafe_allow_html=True)
    st.markdown("<p class='brand-title'>MA3LOMATI PRO</p>", unsafe_allow_html=True)
    st.markdown("<p class='brand-tagline'>المنصة العقارية الذكية</p>", unsafe_allow_html=True)
    
    t_login, t_signup = st.tabs(["🔐 تسجيل الدخول", "📝 اشتراك جديد"])
    
    with t_login:
        u = st.text_input("Username", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_log")
        p = st.text_input("Password", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="p_log")
        if st.button("دخول للمنصة", use_container_width=True):
            if check_user(u, p):
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")

    with t_signup:
        st.text_input("Full Name", placeholder="الاسم بالكامل", label_visibility="collapsed", key="s_name")
        st.text_input("Phone", placeholder="رقم الهاتف", label_visibility="collapsed", key="s_phone")
        if st.button("إرسال طلب اشتراك", use_container_width=True):
            st.success("تم إرسال طلبك للإدارة بنجاح")
            
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. الصفحة الداخلية بعد الدخول ---
else:
    st.markdown("<h1 style='text-align:center; color:#f59e0b; padding-top:50px;'>مرحباً بك في لوحة التحكم</h1>", unsafe_allow_html=True)
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()
