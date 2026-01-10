import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS - التوسيط المطلق وفخامة التصميم
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء القوائم الافتراضية */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f0f2f6; 
    }

    /* حاوية التوسيط المطلق لصفحة تسجيل الدخول */
    .stApp {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .login-box {
        background: #000000;
        padding: 50px;
        border-radius: 35px;
        border: 5px solid #f59e0b;
        box-shadow: 0px 20px 50px rgba(0,0,0,0.3);
        text-align: center;
        width: 450px;
    }

    .login-box h1 { color: #f59e0b; font-weight: 900; font-size: 2.8rem; margin-bottom: 10px; }
    .login-box p { color: #ffffff; margin-bottom: 30px; opacity: 0.8; }

    /* زر الخروج الثابت */
    .logout-container {
        position: fixed;
        top: 20px; right: 20px;
        z-index: 99999;
    }

    /* ستايل الأزرار العام */
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 4px 4px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
        font-size: 1.1rem !important; min-height: 50px !important;
    }
    
    /* تخصيص زر الدخول */
    .login-box div.stButton > button {
        background-color: #f59e0b !important;
        color: #000 !important;
        width: 100% !important;
        border: none !important;
    }

    /* ستايل مدخلات النصوص */
    .stTextInput input {
        background-color: #1a1a1a !important; color: white !important;
        border: 2px solid #f59e0b !important; border-radius: 12px !important;
        text-align: center; font-size: 1.2rem !important; height: 55px !important;
    }

    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000; margin-top: 80px;
    }
    
    .custom-card {
        background: #ffffff; border: 4px solid #000; padding: 20px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000;
    }
    .card-title { font-size: 1.8rem; font-weight: 900; color: #f59e0b; border-bottom: 3px solid #000; padding-bottom: 10px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. نظام التحقق من الهوية ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def login_page():
    # كود عرض المربع الأسود في منتصف الصفحة
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h1>معلوماتى</h1>', unsafe_allow_html=True)
    st.markdown('<p>المنصة العقارية الذكية للمحترفين</p>', unsafe_allow_html=True)
    
    pwd = st.text_input("كلمة المرور", type="password", placeholder="أدخل كلمة المرور السرية", label_visibility="collapsed")
    
    if st.button("دخول للمنصة"):
        if pwd == "Ma3lomati_2026": # يمكنك تغيير كلمة المرور هنا
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ كلمة المرور غير صحيحة")
            
    st.markdown('</div>', unsafe_allow_html=True)

# حماية المحتوى: إذا لم يسجل الدخول، اعرض صفحة الدخول فقط وتوقف
if not st.session_state.authenticated:
    login_page()
    st.stop()

# --- 4. محتوى المنصة (يظهر بعد تسجيل الدخول) ---

# زر الخروج الثابت في الزاوية
st.markdown('<div class="logout-container">', unsafe_allow_html=True)
if st.button("🔒 خروج", key="logout_btn"):
    st.session_state.authenticated = False
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# وظيفة جلب البيانات
@st.cache_data(ttl=300)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

df = load_data()

# تهيئة حالة التنقل
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'current_page' not in st.session_state: st.session_state.current_page = 0

# عرض الصفحة الرئيسية
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢 دليل المطورين الشامل", use_container_width=True): 
            st.session_state.view = 'comp'; st.session_state.current_page = 0; st.rerun()
    with c2:
        if st.button("🛠️ أدوات البروكر الذكية", use_container_width=True): 
            st.session_state.view = 'tools'; st.rerun()

# باقي منطق الصفحات (دليل المطورين والأدوات) كما في كودك الأصلي...
elif st.session_state.view == 'comp':
    # (هنا يتم وضع كود عرض المطورين الخاص بك)
    if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
    st.write("محتوى دليل المطورين يظهر هنا...")

elif st.session_state.view == 'tools':
    # (هنا يتم وضع كود حاسبة الأقساط والـ ROI الخاص بك)
    if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
    st.write("محتوى الأدوات يظهر هنا...")
