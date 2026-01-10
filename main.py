import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# تصميم CSS (تمت إضافة تنسيق لصفحة تسجيل الدخول)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }
    
    /* تنسيق صندوق تسجيل الدخول */
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 40px;
        background: #000;
        border-radius: 20px;
        border: 4px solid #f59e0b;
        box-shadow: 15px 15px 0px #ccc;
        text-align: center;
        color: #f59e0b;
    }

    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000;
    }
    .custom-card {
        background: #ffffff; border: 4px solid #000; padding: 20px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000;
        text-align: right;
    }
    .card-title { font-size: 1.8rem; font-weight: 900; color: #f59e0b; border-bottom: 3px solid #000; padding-bottom: 10px; margin-bottom: 15px; }
    
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 4px 4px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
        font-size: 1.1rem !important; min-height: 50px !important;
    }
    div.stButton > button:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0px #f59e0b !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. نظام تسجيل الدخول ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    if not st.session_state.authenticated:
        # واجهة تسجيل الدخول
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h1>🔐 دخول المنصة</h1>', unsafe_allow_html=True)
        password = st.text_input("أدخل كلمة المرور الخاصة بالمستشارين", type="password")
        if st.button("تسجيل الدخول"):
            if password == "Ma3lomati_2026": # كلمة المرور الخاصة بك
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ كلمة المرور غير صحيحة")
        st.markdown('</div>', unsafe_allow_html=True)
        return False
    return True

# إذا لم يتم تسجيل الدخول، أوقف الكود هنا
if not check_password():
    st.stop()

# --- 3. بقية الكود (لا يظهر إلا بعد الدخول) ---

@st.cache_data(ttl=300)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"حدث خطأ أثناء تحميل البيانات: {e}")
        return pd.DataFrame()

# تهيئة الحالة
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'current_page' not in st.session_state: st.session_state.current_page = 0

df = load_data()

# إضافة زر تسجيل الخروج في الأعلى
if st.sidebar.button("🔓 تسجيل الخروج"):
    st.session_state.authenticated = False
    st.rerun()

# --- منطق التنقل الرئيسي ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢 دليل المطورين الشامل", use_container_width=True): 
            st.session_state.view = 'comp'; st.session_state.current_page = 0; st.rerun()
    with c2:
        if st.button("🛠️ أدوات البروكر الذكية", use_container_width=True): 
            st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'comp':
    # كود عرض المطورين (كما هو في ملفك)
    if st.session_state.selected_dev:
        dev_name = st.session_state.selected_dev
        row = df[df['Developer'] == dev_name].iloc[0]
        st.markdown(f'<div class="hero-banner"><h2>{dev_name}</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 العودة للقائمة"): 
            st.session_state.selected_dev = None; st.rerun()
        
        col_r, col_l = st.columns([1.2, 1])
        with col_r:
            st.markdown(f'<div class="custom-card"><div class="card-title">👤 تفاصيل المالك</div><p>{row.get("Owner", "غير متوفر")}</p></div>', unsafe_allow_html=True)
        with col_l:
            st.markdown(f'<div class="custom-card"><div class="card-title">🏗️ معلومات المشاريع</div><p>{row.get("Area", "-")}</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
        # ... بقية كود عرض المربعات الخاص بك ...

elif st.session_state.view == 'tools':
    # كود أدوات البروكر (كما هو في ملفك)
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر المحترف</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
    # ... حاسبة الأقساط والـ ROI ...
