import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# تصميم CSS احترافي (معدل لإضافة زر تسجيل الدخول)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* حاوية زر تسجيل الدخول فوق الهيدر */
    .top-nav {
        display: flex;
        justify-content: flex-start; /* ليكون على اليسار في واجهة RTL */
        padding: 10px 20px;
        background: transparent;
    }
    
    .login-btn {
        background-color: #000;
        color: #f59e0b !important;
        padding: 8px 25px;
        border-radius: 12px;
        border: 2px solid #f59e0b;
        font-weight: 900;
        text-decoration: none;
        font-size: 1rem;
        box-shadow: 4px 4px 0px #f59e0b;
        transition: 0.3s;
    }
    
    .login-btn:hover {
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0px #000;
        background-color: #f59e0b;
        color: #000 !important;
    }

    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000;
        position: relative;
    }
    
    /* باقي التنسيقات الخاصة بك */
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
    </style>
""", unsafe_allow_html=True)

# إضافة زر تسجيل الدخول في أعلى الصفحة على اليسار
st.markdown('<div class="top-nav"><a href="#" class="login-btn">تسجيل الدخول</a></div>', unsafe_allow_html=True)

# 2. وظيفة جلب البيانات
@st.cache_data(ttl=300)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"خطأ: {e}")
        return pd.DataFrame()

# تهيئة الحالة (Session State)
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'current_page' not in st.session_state: st.session_state.current_page = 0

df = load_data()

# --- المنطق الخاص بالتنقل (Main, Comp, Tools) يظل كما هو دون تغيير ---
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
    # كود عرض المطورين... (كما هو في ملفك الأصلي)
    pass

elif st.session_state.view == 'tools':
    # كود أدوات البروكر (الحاسبات التي أضفناها سابقاً)
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر المحترف</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
    
    t1, t2 = st.columns(2)
    with t1:
        st.markdown('<div class="custom-card"><div class="card-title">💰 حاسبة الأقساط</div></div>', unsafe_allow_html=True)
        total_price = st.number_input("إجمالي سعر الوحدة (ج.م)", min_value=0, step=100000)
        down_payment_pct = st.number_input("نسبة المقدم (%)", min_value=0, max_value=100, step=5)
        years = st.number_input("عدد سنوات التقسيط", min_value=1, max_value=30, step=1)
        if total_price > 0:
            down_val = total_price * (down_payment_pct / 100)
            remaining = total_price - down_val
            monthly = remaining / (years * 12)
            st.markdown(f'<div style="background:#000; color:#f59e0b; padding:15px; border-radius:10px; text-align:center;"><h3>المقدم: {down_val:,.0f} ج.م</h3><h2>القسط: {monthly:,.0f} ج.م</h2></div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="custom-card"><div class="card-title">📈 حاسبة العائد ROI</div></div>', unsafe_allow_html=True)
        investment = st.number_input("إجمالي مبلغ الشراء", min_value=0, step=100000)
        expected_rent = st.number_input("الإيجار الشهري المتوقع", min_value=0, step=1000)
        if investment > 0 and expected_rent > 0:
            roi = ((expected_rent * 12) / investment) * 100
            st.markdown(f'<div style="background:#f59e0b; color:#000; padding:15px; border-radius:10px; text-align:center; border:3px solid #000;"><h2>نسبة العائد: {roi:.2f}% سنوياً</h2></div>', unsafe_allow_html=True)
