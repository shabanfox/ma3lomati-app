import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS احترافي (يشمل صفحة الدخول، الحاسبة، وتوزيع الـ 70%)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء العناصر الافتراضية */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] > section:first-child > div:first-child {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #ffffff; margin: 0 !important; padding: 0 !important;
    }

    /* --- صفحة الدخول (البيضاوي الذهبي) --- */
    .login-wrapper { display: flex; flex-direction: column; align-items: center; width: 100%; }
    .hero-oval-header {
        background: #000000; border: 5px solid #f59e0b; border-top: none; 
        padding: 50px 20px; border-radius: 0px 0px 500px 500px; 
        text-align: center; width: 100%; max-width: 800px;
        box-shadow: 0px 15px 30px rgba(0,0,0,0.2); margin-bottom: 40px;
    }
    .hero-oval-header h1 { color: #f59e0b; font-weight: 900; font-size: 2.8rem; margin: 0; }
    .gold-lock { font-size: 70px; color: #f59e0b; margin-bottom: 20px; }

    /* حقل الباسورد (أسود على أبيض) */
    .stTextInput input {
        background-color: #ffffff !important; color: #000000 !important;
        border: 3px solid #000000 !important; border-radius: 15px !important;
        text-align: center; font-size: 1.3rem !important; height: 60px !important;
        font-weight: 700; box-shadow: 5px 5px 0px #f59e0b !important;
    }
    
    /* --- تصميم الكروت والأزرار بعد الدخول --- */
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

    /* زر الخروج العائم */
    .logout-box { position: fixed; top: 10px; left: 10px; z-index: 999; }
    
    /* حاسبة العائد - تصميم مميز */
    .roi-result {
        background: #f59e0b; color: #000; padding: 20px; border-radius: 15px;
        text-align: center; border: 4px solid #000; font-weight: 900;
    }
    </style>
""", unsafe_allow_html=True)

# 3. نظام التحقق (Session State)
if 'auth' not in st.session_state: st.session_state.auth = False

def login_screen():
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="hero-oval-header"><h1>منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="gold-lock">🔒</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        pwd = st.text_input("كلمة المرور", type="password", placeholder="أدخل الرمز السري", label_visibility="collapsed")
        if st.button("دخول للمنصة"):
            if pwd == "Ma3lomati_2026":
                st.session_state.auth = True; st.rerun()
            else: st.error("⚠️ الرمز غير صحيح")
    st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.auth:
    login_screen(); st.stop()

# --- المنصة بعد الدخول ---
st.markdown('<div class="logout-box">', unsafe_allow_html=True)
if st.button("🔒 خروج"): st.session_state.auth = False; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

@st.cache_data(ttl=300)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df.columns = [str(c).strip() for c in df.columns]; return df
    except: return pd.DataFrame()

if 'view' not in st.session_state: st.session_state.view = 'main'
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
df = load_data()

# --- محتوى المنصة ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى - لوحة التحكم</h1></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢 دليل المطورين الشامل", use_container_width=True): st.session_state.view = 'comp'; st.rerun()
    with c2:
        if st.button("🛠️ أدوات الحاسبة الذكية", use_container_width=True): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'comp':
    st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
    
    # توزيع المساحة: 70% يمين للمطورين، 30% يسار فراغ أو فلاتر
    col_devs, col_side = st.columns([0.7, 0.3])
    
    with col_devs: # الجانب الأيمن (70%)
        if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
        search = st.text_input("🔍 ابحث عن اسم المطور...")
        dev_list = df['Developer'].unique()
        if search: dev_list = [d for d in dev_list if search.lower() in str(d).lower()]
        
        # عرض المطورين في شبكة
        for i in range(0, len(dev_list), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(dev_list):
                    name = dev_list[i+j]
                    if cols[j].button(name, key=name, use_container_width=True):
                        st.session_state.selected_dev = name; st.rerun()

elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر المحترف</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
    
    t1, t2 = st.columns(2)
    with t1:
        st.markdown('<div class="custom-card"><div class="card-title">💰 حاسبة الأقساط</div></div>', unsafe_allow_html=True)
        p = st.number_input("سعر الوحدة", min_value=0, step=100000)
        dp = st.number_input("المقدم (%)", 0, 100, 10)
        y = st.number_input("السنوات", 1, 30, 7)
        if p > 0:
            m = (p - (p*(dp/100))) / (y*12)
            st.success(f"القسط الشهري المتوقع: {m:,.0f} ج.م")

    with t2:
        st.markdown('<div class="custom-card"><div class="card-title">📈 حاسبة العائد الإيجاري (ROI)</div></div>', unsafe_allow_html=True)
        invest = st.number_input("إجمالي قيمة العقار (ج.م)", min_value=0, step=100000)
        rent = st.number_input("الإيجار الشهري المتوقع (ج.م)", min_value=0, step=1000)
        if invest > 0 and rent > 0:
            annual = rent * 12
            roi = (annual / invest) * 100
            st.markdown(f'<div class="roi-result">العائد السنوي المتوقع: {roi:.2f}% <br> الدخل السنوي: {annual:,.0f} ج.م</div>', unsafe_allow_html=True)
