import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# تصميم CSS احترافي وشامل (يشمل صفحة الدخول والتوسيط)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء القوائم الافتراضية */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f0f2f6; 
    }

    /* حاوية التوسيط المطلق لصفحة تسجيل الدخول */
    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #121212;
        z-index: 9999;
    }

    .login-box {
        background: #000000;
        padding: 50px;
        border-radius: 35px;
        border: 4px solid #f59e0b;
        box-shadow: 0px 0px 50px rgba(245, 158, 11, 0.2);
        text-align: center;
        width: 400px;
    }

    .login-box h1 { color: #f59e0b; font-weight: 900; font-size: 2.5rem; margin-bottom: 10px; }
    .login-box p { color: #ffffff; margin-bottom: 30px; opacity: 0.8; }

    /* زر الخروج الثابت */
    .logout-container {
        position: fixed;
        top: 20px; right: 20px;
        z-index: 99999;
    }

    /* ستايل الأزرار */
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 4px 4px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
        font-size: 1.1rem !important; min-height: 50px !important;
    }
    div.stButton > button:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0px #f59e0b !important; }
    
    /* تخصيص زر الدخول */
    .login-box div.stButton > button {
        background-color: #f59e0b !important;
        color: #000 !important;
        width: 100% !important;
        border: none !important;
    }

    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000; margin-top: 60px;
    }
    
    .stTextInput input {
        background-color: #1a1a1a !important; color: white !important;
        border: 2px solid #f59e0b !important; border-radius: 12px !important;
        text-align: center; font-size: 1.2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. نظام تسجيل الدخول ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def login_page():
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h1>معلوماتى</h1>', unsafe_allow_html=True)
        st.markdown('<p>المنصة العقارية الذكية</p>', unsafe_allow_html=True)
        
        pwd = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور", label_visibility="collapsed")
        
        if st.button("دخول للمنصة"):
            if pwd == "Ma3lomati_2026":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.markdown('<p style="color: #ff4b4b; font-weight: bold;">❌ كلمة المرور غير صحيحة</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# حماية التطبيق
if not st.session_state.authenticated:
    login_page()
    st.stop()

# --- 3. زر الخروج (يظهر بعد الدخول) ---
st.markdown('<div class="logout-container">', unsafe_allow_html=True)
if st.button("🔒 خروج", key="logout_btn"):
    st.session_state.authenticated = False
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- 4. جلب البيانات (كودك الأصلي) ---
@st.cache_data(ttl=300)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

# --- التنقل والمحتوى الرئيسي (كودك الأصلي) ---
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'current_page' not in st.session_state: st.session_state.current_page = 0

if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢 دليل المطورين الشامل", use_container_width=True): 
            st.session_state.view = 'comp'; st.session_state.current_page = 0; st.rerun()
    with c2:
        if st.button("🛠️ أدوات البروكر الذكية", use_container_width=True): 
            st.session_state.view = 'tools'; st.rerun()

# (يتبع باقي منطق الصفحات الخاصة بك لدليل المطورين والأدوات...)
elif st.session_state.view == 'comp':
    # ... نفس كود عرض المطورين الخاص بك ...
    if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
    st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
    # (هنا تضع كود عرض الشبكة والبحث)

elif st.session_state.view == 'tools':
    # ... نفس كود الحاسبات الخاص بك ...
    if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر</h2></div>', unsafe_allow_html=True)
