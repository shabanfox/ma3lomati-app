import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# تصميم CSS احترافي يدمج نمط صفحة الدخول مع المنصة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء القوائم الافتراضية */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* حاوية التوسيط لصفحة تسجيل الدخول */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80vh;
    }

    .login-box {
        background: #000000;
        padding: 40px;
        border-radius: 30px;
        border: 5px solid #f59e0b;
        box-shadow: 15px 15px 0px rgba(0,0,0,0.1);
        text-align: center;
        width: 100%;
        max-width: 450px;
    }

    /* ستايل زر الخروج الثابت */
    .logout-container {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 999;
    }

    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000;
        margin-top: 50px;
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
    }
    div.stButton > button:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0px #f59e0b !important; }
    
    /* زر الدخول داخل الصندوق */
    .login-box div.stButton > button {
        background-color: #f59e0b !important;
        color: #000 !important;
        border: none !important;
        width: 100% !important;
    }

    /* ستايل المدخلات */
    .stTextInput input, .stNumberInput input {
        border: 3px solid #000 !important;
        border-radius: 12px !important;
        padding: 12px !important;
        text-align: center;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. نظام التحقق من الهوية ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

def login():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h1 style="color:#f59e0b; font-weight:900;">معلوماتى العقارية</h1>', unsafe_allow_html=True)
        st.markdown('<p style="color:#fff;">يرجى إدخال كلمة المرور للوصول للمنصة</p>', unsafe_allow_html=True)
        
        password = st.text_input("كلمة المرور", type="password", placeholder="••••••••", label_visibility="collapsed")
        
        if st.button("تسجيل الدخول الآمن"):
            if password == "Ma3lomati_2026": # كلمة المرور الخاصة بك
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# منع عرض المحتوى إلا بعد الدخول
if not st.session_state.auth:
    login()
    st.stop()

# --- 3. زر الخروج الثابت بعد الدخول ---
st.markdown('<div class="logout-container">', unsafe_allow_html=True)
if st.button("🔒 خروج"):
    st.session_state.auth = False
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- 4. باقي الكود (جلب البيانات والمنصة) ---
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

# --- التنقل والمحتوى الرئيسي ---
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
    # (هنا تضع كود عرض المطورين الخاص بك الذي أرسلته سابقاً)
    if st.session_state.selected_dev:
        dev_name = st.session_state.selected_dev
        row = df[df['Developer'] == dev_name].iloc[0]
        st.markdown(f'<div class="hero-banner"><h2>{dev_name}</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 العودة للقائمة"): 
            st.session_state.selected_dev = None; st.rerun()
        # ... بقية عرض التفاصيل ...
        st.markdown(f'<div class="custom-card"><h3>👤 تفاصيل المالك</h3><p>{row.get("Owner", "-")}</p></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
        # ... كود البحث والعرض الشبكي للمطورين ...

elif st.session_state.view == 'tools':
    # (هنا تضع كود الحاسبات ROI والأقساط الذي أرسلته سابقاً)
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر المحترف</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
    # ... كود الحاسبات ...
