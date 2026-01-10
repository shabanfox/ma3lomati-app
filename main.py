import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS - السحر كله هنا للتوسيط الكامل
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الهيدر والقوائم */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* جعل الصفحة مرنة للتوسيط */
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #121212; /* خلفية داكنة فخمة */
    }

    /* حاوية التوسيط المطلق */
    .stApp {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* تصميم صندوق الدخول */
    .login-box {
        background: #000000;
        padding: 60px;
        border-radius: 40px;
        border: 4px solid #f59e0b;
        box-shadow: 0px 0px 50px rgba(245, 158, 11, 0.2);
        text-align: center;
        max-width: 450px;
        width: 90%;
    }

    .login-box h1 {
        color: #f59e0b;
        font-weight: 900;
        font-size: 3.5rem;
        margin-bottom: 0px;
    }

    .login-box h2 {
        color: #fff;
        font-weight: 700;
        margin-bottom: 20px;
    }

    /* ستايل زر الخروج الثابت (يظهر بعد الدخول) */
    .logout-container {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
    }

    /* ستايل مدخلات النصوص */
    .stTextInput input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 2px solid #333 !important;
        border-radius: 15px !important;
        text-align: center;
        font-size: 1.2rem !important;
        height: 55px !important;
    }
    .stTextInput input:focus {
        border-color: #f59e0b !important;
    }

    /* ستايل الأزرار */
    div.stButton > button {
        border-radius: 15px !important;
        font-weight: 900 !important;
        background-color: #f59e0b !important;
        color: #000 !important;
        border: none !important;
        width: 100% !important;
        height: 55px !important;
        font-size: 1.2rem !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0px 0px 20px rgba(245, 158, 11, 0.4) !important;
    }
    
    /* محتوى المنصة */
    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 30px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 3px solid #f59e0b;
        margin-top: 80px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. نظام التحقق من الدخول ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def login_page():
    # الصندوق يظهر الآن في منتصف الشاشة تلقائياً
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h1>🏠</h1>', unsafe_allow_html=True)
    st.markdown('<h2>معلوماتى العقارية</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#aaa;">دخول المستشارين العقاريين</p>', unsafe_allow_html=True)
    
    pwd = st.text_input("كلمة المرور", type="password", key="p_in", label_visibility="collapsed", placeholder="أدخل كلمة المرور")
    
    if st.button("دخول آمن"):
        if pwd == "Ma3lomati_2026":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ كلمة المرور غير صحيحة")
    
    st.markdown('</div>', unsafe_allow_html=True)

# فحص الحالة
if not st.session_state.authenticated:
    login_page()
    st.stop()

# --- 4. المحتوى بعد الدخول ---

# زر الخروج (ثابت فوق عاليمين)
st.markdown('<div class="logout-container">', unsafe_allow_html=True)
if st.button("🔒 خروج", key="logout_btn"):
    st.session_state.authenticated = False
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# الهيدر الرئيسي للمنصة
st.markdown('<div class="hero-banner"><h1>🏠 أهلاً بك في منصة معلوماتى</h1><p>أدواتك للنجاح في السوق العقاري</p></div>', unsafe_allow_html=True)

# أزرار التنقل الرئيسية
c1, c2 = st.columns(2)
with c1:
    if st.button("🏢 دليل المطورين", use_container_width=True):
        st.write("تم الانتقال لدليل المطورين...")
with c2:
    if st.button("🛠️ الأدوات الذكية", use_container_width=True):
        st.write("تم الانتقال للأدوات...")
