import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_config = st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- الثوابت وروابط الشيتات ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# رابط شيت المستخدمين (الذي أرسلته أنت)
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"

# --- 2. إدارة الجلسة (Session State) ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 3. تصميم CSS (عربي واحترافي) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.92)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}
    /* حاوية تسجيل الدخول في السنتر فوق */
    .auth-wrapper {{
        position: absolute; top: 0; left: 50%; transform: translateX(-50%);
        width: 100%; max-width: 420px; padding-top: 40px; text-align: center; z-index: 100;
    }}
    .brand-glow {{ color: #f59e0b; font-size: 45px; font-weight: 900; text-shadow: 0 0 20px rgba(245,158,11,0.5); margin:0; }}
    div.stTextInput input {{ background-color: rgba(0,0,0,0.7) !important; color: #fff !important; border: 1px solid #f59e0b !important; border-radius: 12px !important; text-align: center !important; height: 48px !important; }}
    div.stButton > button {{ background: linear-gradient(90deg, #f59e0b, #d97706) !important; color: #000 !important; font-weight: 900 !important; border-radius: 12px !important; border: none !important; height: 50px !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. وظائف جلب البيانات والتحقق ---
def check_auth(u, p):
    """التحقق من المستخدم عبر رابط الشيت المباشر"""
    try:
        # قراءة الشيت أونلاين
        df = pd.read_csv(USER_SHEET_URL)
        # تنظيف أسماء الأعمدة من أي فراغات
        df.columns = [c.strip() for c in df.columns]
        # البحث عن تطابق الاسم وكلمة السر
        # ملاحظة: تأكد أن الأعمدة في الشيت اسمها (Name) و (Password)
        match = df[(df['Name'].astype(str) == str(u)) & (df['Password'].astype(str) == str(p))]
        return not match.empty
    except Exception as e:
        st.error(f"حدث خطأ في الاتصال بقاعدة البيانات: {e}")
        return False

@st.cache_data(ttl=60)
def load_app_data():
    """تحميل بيانات العقارات والمشاريع"""
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(U_P)
        return df.fillna("---")
    except: return pd.DataFrame()

# --- 5. واجهة تسجيل الدخول المرتبطة بالشيت ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<p class='brand-glow'>MA3LOMATI PRO</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:white; opacity:0.8;'>منصة معلوماتي العقارية الذكية</p>", unsafe_allow_html=True)
    
    tab_in, tab_reg = st.tabs(["🔐 دخول", "📝 طلب اشتراك"])
    
    with tab_in:
        user_input = st.text_input("اسم المستخدم", placeholder="أدخل الاسم", label_visibility="collapsed", key="u_field")
        pass_input = st.text_input("كلمة السر", type="password", placeholder="أدخل كلمة السر", label_visibility="collapsed", key="p_field")
        
        if st.button("تسجيل الدخول", use_container_width=True):
            if user_input and pass_input:
                with st.spinner('جاري التحقق من البيانات...'):
                    if check_auth(user_input, pass_input):
                        st.session_state.auth = True
                        st.success("تم تسجيل الدخول بنجاح!")
                        st.rerun()
                    else:
                        st.error("اسم المستخدم أو كلمة السر غير صحيحة")
            else:
                st.warning("يرجى إدخال البيانات")

    with tab_reg:
        st.markdown("<p style='color:white;'>يرجى التواصل مع الإدارة لإنشاء حساب جديد</p>", unsafe_allow_html=True)
        st.text_input("الأسم بالكامل", placeholder="إسمك الثلاثي", label_visibility="collapsed")
        st.button("إرسال طلب الانضمام", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. التطبيق الداخلي بعد نجاح الدخول ---
else:
    df_main = load_app_data()
    st.markdown(f'<div style="text-align:center; padding:20px;"><h1 style="color:#f59e0b;">مرحباً بك في MA3LOMATI PRO</h1></div>', unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()

    st.info("تم جلب البيانات بنجاح من شيت جوجل المرتبط.")
    st.dataframe(df_main)
