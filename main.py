import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS احترافي (يشمل صفحة الدخول والمنصة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* صفحة تسجيل الدخول */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80vh;
    }
    .login-card {
        background: #000000;
        padding: 50px;
        border-radius: 30px;
        border: 4px solid #f59e0b;
        box-shadow: 0px 0px 30px rgba(245, 158, 11, 0.3);
        text-align: center;
        width: 100%;
        max-width: 450px;
    }
    
    /* زر الخروج العائم */
    .logout-box {
        position: fixed;
        top: 15px;
        right: 15px;
        z-index: 9999;
    }

    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000; margin-top: 50px;
    }
    
    .custom-card {
        background: #ffffff; border: 4px solid #000; padding: 20px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000;
        text-align: right;
    }
    
    /* ستايل الأزرار */
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 4px 4px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
        font-size: 1.1rem !important; min-height: 50px !important;
        transition: 0.3s;
    }
    div.stButton > button:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0px #f59e0b !important; }
    
    /* ستايل زر الدخول الخاص */
    .login-card div.stButton > button {
        background-color: #f59e0b !important;
        color: #000 !important;
        border: none !important;
        width: 100% !important;
    }

    /* ستايل حقل كلمة المرور */
    .stTextInput input {
        background-color: #1a1a1a !important;
        color: #f59e0b !important;
        border: 2px solid #f59e0b !important;
        border-radius: 12px !important;
        text-align: center;
        font-size: 1.2rem !important;
        padding: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. نظام التحقق من الهوية
if 'auth' not in st.session_state:
    st.session_state.auth = False

def login_screen():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<h1 style="color:#f59e0b; font-weight:900; margin-bottom:10px;">دخول المستشارين</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:#ffffff; margin-bottom:30px; opacity:0.8;">منصة معلوماتى العقارية الذكية</p>', unsafe_allow_html=True)
        
        pwd = st.text_input("كلمة المرور", type="password", placeholder="أدخل رمز الدخول السرّي", label_visibility="collapsed")
        
        if st.button("فتح المنصة الآن 🔓"):
            if pwd == "Ma3lomati_2026": # يمكنك تغيير كلمة المرور هنا
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("❌ كلمة المرور غير صحيحة")
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# إذا لم يسجل الدخول، اعرض صفحة الدخول فقط
if not st.session_state.auth:
    login_screen()
    st.stop()

# --- بعد تسجيل الدخول بنجاح يظهر باقي الكود ---

# زر الخروج
st.markdown('<div class="logout-box">', unsafe_allow_html=True)
if st.button("🔒 خروج"):
    st.session_state.auth = False
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# 2. وظيفة جلب البيانات
@st.cache_data(ttl=300)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

# تهيئة الحالة
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'current_page' not in st.session_state: st.session_state.current_page = 0

df = load_data()

# --- التنقل والمحتوى الرئيسي (نفس منطق كودك) ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢 دليل المطورين الشامل", use_container_width=True): 
            st.session_state.view = 'comp'; st.session_state.current_page = 0; st.rerun()
    with c2:
        if st.button("🛠️ أدوات البروكر الذكية", use_container_width=True): 
            st.session_state.view = 'tools'; st.rerun()

# (بقية الكود الخاص بك لـ comp و tools يوضع هنا...)
elif st.session_state.view == 'comp':
    # كود دليل المطورين...
    if st.button("🔙 العودة"): st.session_state.view = 'main'; st.rerun()
    st.write("محتوى المطورين") # ضع كود العرض هنا

elif st.session_state.view == 'tools':
    # كود الأدوات...
    if st.button("🔙 العودة"): st.session_state.view = 'main'; st.rerun()
    st.write("محتوى الأدوات") # ضع كود الحاسبة هنا
