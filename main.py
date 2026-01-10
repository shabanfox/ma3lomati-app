import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتصميم الأساسي
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# تصميم CSS شامل (أسود بالكامل وتعديل ألوان المدخلات)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* حماية ومنع النسخ */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    * { -webkit-user-select: none; user-select: none; }
    
    /* خلفية الموقع العامة */
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #000000; 
    }

    /* الهيدر الرئيسي */
    .hero-banner { 
        background: #0a0a0a; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #1a1a1a;
    }

    /* تصميم الحاسبات (أسود بالكامل) */
    .calc-container {
        background-color: #0a0a0a;
        border: 2px solid #333;
        border-radius: 20px;
        padding: 25px;
        color: white;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    
    .calc-title { 
        font-size: 1.6rem; font-weight: 900; color: #f59e0b; 
        border-bottom: 2px solid #f59e0b; padding-bottom: 10px; margin-bottom: 20px; 
    }

    /* تعديل شكل حقول الإدخال لتصبح سوداء */
    .stNumberInput input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    .stNumberInput label {
        color: #f59e0b !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
    }

    .result-box {
        background: #111; border-right: 5px solid #f59e0b;
        padding: 15px; border-radius: 10px; margin-top: 15px;
        text-align: center;
    }

    /* أزرار الموقع */
    div.stButton > button {
        border: 2px solid #f59e0b !important; border-radius: 12px !important;
        background-color: #000 !important; color: #f59e0b !important;
        font-weight: 900 !important; min-height: 50px !important; width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #f59e0b !important; color: #000 !important; }

    /* زر الخروج/الدخول */
    .top-nav { display: flex; justify-content: flex-start; padding: 10px; }
    .login-btn {
        background-color: #000; color: #f59e0b; padding: 5px 20px; 
        border: 1px solid #f59e0b; border-radius: 10px; text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

# 2. نظام الدخول
if "authenticated" not in st.session_state: st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown('<div class="hero-banner"><h1>🔒 تسجيل الدخول لمنصة معلوماتى</h1></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1,1.5,1])
    with col:
        pwd = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            if pwd == "Ma3lomati_2026":
                st.session_state["authenticated"] = True
                st.rerun()
            else: st.error("خطأ!")
    st.stop()

# 3. جلب البيانات
@st.cache_data(ttl=300)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try: return pd.read_csv(sheet_url)
    except: return pd.DataFrame()

df = load_data()

# الحالة والتنقل
if 'view' not in st.session_state: st.session_state.view = 'main'

# الهيدر العلوي
st.markdown('<div class="top-nav"><a href="#" class="login-btn">خروج</a></div>', unsafe_allow_html=True)

# --- الصفحات ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢 دليل المطورين"): st.session_state.view = 'comp'; st.rerun()
    with c2:
        if st.button("🛠️ أدوات البروكر"): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'comp':
    # كود عرض المطورين (مختصر للتوضيح)
    st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 العودة"): st.session_state.view = 'main'; st.rerun()
    st.dataframe(df, use_container_width=True)

elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر الذكية</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 العودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="calc-container"><div class="calc-title">💰 حاسبة الأقساط</div>', unsafe_allow_html=True)
        p = st.number_input("إجمالي سعر الوحدة (ج.م)", min_value=0, step=100000, key="p_in")
        d = st.number_input("نسبة المقدم (%)", min_value=0, max_value=100, step=5, key="d_in")
        y = st.number_input("عدد سنوات التقسيط", min_value=1, max_value=30, step=1, key="y_in")
        
        if p > 0:
            down_val = p * (d / 100)
            monthly = (p - down_val) / (y * 12)
            st.markdown(f'<div class="result-box"><h3>المقدم: {down_val:,.0f} ج.م</h3><h2>القسط: {monthly:,.0f} ج.م</h2></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="calc-container"><div class="calc-title">📈 حاسبة العائد ROI</div>', unsafe_allow_html=True)
        inv = st.number_input("إجمالي المبلغ المستثمر (سعر الشراء)", min_value=0, step=100000, key="inv_in")
        rent = st.number_input("الإيجار الشهري المتوقع", min_value=0, step=1000, key="rent_in")
        
        if inv > 0:
            yield_val = ((rent * 12) / inv) * 100
            st.markdown(f'<div class="result-box"><h3>عائد الإيجار السنوي:</h3><h2 style="color:#2ecc71;">{yield_val:.2f}%</h2></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
