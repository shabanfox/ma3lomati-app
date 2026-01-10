import streamlit as st

# 1. إعدادات الصفحة وتصفير الهوامش تماماً
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS مخصص (التصاق علوي + شكل بيضاوي + ألوان مخصصة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء أي عناصر افتراضية تسبب فراغاً */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* تصفير هوامش Streamlit العلوية تماماً */
    [data-testid="stAppViewContainer"] > section:first-child > div:first-child {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #ffffff;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* الحاوية الرئيسية */
    .login-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }

    /* الشكل البيضاوي الأسود خلف العنوان وملتصق بالأعلى */
    .hero-oval-header {
        background: #000000;
        border: 4px solid #f59e0b; /* فريم ذهبي */
        border-top: none; /* إزالة الحد العلوي للالتصاق */
        padding: 50px 20px;
        border-radius: 0px 0px 500px 500px; /* انحناء بيضاوي من الأسفل */
        text-align: center;
        width: 100%;
        max-width: 800px;
        box-shadow: 0px 15px 30px rgba(0,0,0,0.2);
        margin-bottom: 40px;
    }

    .hero-oval-header h1 {
        color: #f59e0b;
        font-weight: 900;
        font-size: 2.8rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* رمز القفل الذهبي */
    .gold-lock {
        font-size: 70px;
        color: #f59e0b;
        margin-bottom: 20px;
        filter: drop-shadow(0px 0px 10px rgba(245, 158, 11, 0.4));
    }

    /* صندوق المدخلات */
    .input-container {
        width: 100%;
        max-width: 400px;
        text-align: center;
        padding: 20px;
    }

    /* ستايل حقل الباسورد: نص أسود على خلفية بيضاء */
    .stTextInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 3px solid #000000 !important;
        border-radius: 15px !important;
        text-align: center;
        font-size: 1.3rem !important;
        height: 60px !important;
        font-weight: 700;
        box-shadow: 5px 5px 0px #f59e0b !important;
    }

    /* زر الدخول */
    div.stButton > button {
        background-color: #f59e0b !important;
        color: #000000 !important;
        border: 3px solid #000000 !important;
        border-radius: 15px !important;
        font-weight: 900 !important;
        font-size: 1.4rem !important;
        width: 100% !important;
        height: 60px !important;
        margin-top: 25px;
        box-shadow: 5px 5px 0px #000000 !important;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        transform: translate(-2px, -2px);
        box-shadow: 7px 7px 0px #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. منطق التحقق من الدخول
if 'auth' not in st.session_state:
    st.session_state.auth = False

def login_page():
    # الحاوية الكلية
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    
    # 1. العنوان داخل الشكل البيضاوي الملتصق بالأعلى
    st.markdown("""
        <div class="hero-oval-header">
            <h1>منصة معلوماتي العقارية</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. رمز القفل
    st.markdown('<div class="gold-lock">🔒</div>', unsafe_allow_html=True)
    
    # 3. منطقة الإدخال
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    pwd = st.text_input("كلمة المرور", type="password", placeholder="كلمة المرور", label_visibility="collapsed")
    
    if st.button("دخول"):
        if pwd == "Ma3lomati_2026":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("⚠️ كلمة المرور غير صحيحة")
            
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# تفعيل صفحة الدخول
if not st.session_state.auth:
    login_page()
    st.stop()

# --- محتوى الموقع بعد الدخول ---
st.success("أهلاً بك في منصة معلوماتي")
if st.button("خروج"):
    st.session_state.auth = False
    st.rerun()
