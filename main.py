import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS فاخر (التوسيط الكامل)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء العناصر الافتراضية */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f0f2f6; 
    }

    /* حاوية التوسيط المطلق لصفحة تسجيل الدخول */
    .main-login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: #f0f2f6;
        z-index: 9999;
    }

    .login-box {
        background: #000000;
        padding: 50px;
        border-radius: 40px;
        border: 6px solid #f59e0b;
        box-shadow: 0px 20px 50px rgba(0,0,0,0.3);
        text-align: center;
        width: 450px;
    }

    .login-box h1 {
        color: #f59e0b;
        font-weight: 900;
        font-size: 3rem;
        margin-bottom: 5px;
    }

    .login-box p {
        color: #ffffff;
        font-size: 1.1rem;
        margin-bottom: 30px;
        letter-spacing: 1px;
    }

    /* ستايل زر الخروج الثابت */
    .logout-container {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 99999;
    }

    /* ستايل الأزرار العامة */
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 4px 4px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
        font-size: 1.1rem !important; min-height: 50px !important;
    }
    
    /* زر الدخول الخاص بالصندوق */
    .login-box div.stButton > button {
        background-color: #f59e0b !important;
        color: #000 !important;
        width: 100% !important;
        border: none !important;
    }

    /* ستايل حقل الإدخال */
    .stTextInput input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 2px solid #f59e0b !important;
        border-radius: 15px !important;
        text-align: center;
        font-size: 1.2rem !important;
        height: 55px !important;
    }

    /* تنسيق محتوى المنصة بعد الدخول */
    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 30px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000; margin-top: 60px;
    }
    
    .custom-card {
        background: #ffffff; border: 4px solid #000; padding: 20px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. نظام التحقق من الدخول ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def login_page():
    # كود HTML للتوسيط الكامل
    st.markdown("""
        <div class="main-login-container">
            <div class="login-box">
                <h1>🏠</h1>
                <h2 style="color:#f59e0b; font-weight:900; margin-bottom:10px;">معلوماتى العقارية</h2>
                <p>يرجى إدخال مفتاح الدخول للمنصة</p>
    """, unsafe_allow_html=True)
    
    # حقل كلمة المرور (باستخدام streamlit)
    pwd = st.text_input("كلمة المرور", type="password", key="login_pass", label_visibility="collapsed", placeholder="••••••••")
    
    if st.button("فتح المنصة الآن"):
        if pwd == "Ma3lomati_2026":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ عذراً، كلمة المرور غير صحيحة")
            
    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True)

# منع عرض أي شيء قبل تسجيل الدخول
if not st.session_state.authenticated:
    login_page()
    st.stop()

# --- 4. المحتوى بعد تسجيل الدخول ---

# زر الخروج الثابت
st.markdown('<div class="logout-container">', unsafe_allow_html=True)
if st.button("🔒 تسجيل الخروج", key="logout_btn"):
    st.session_state.authenticated = False
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# جلب البيانات
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

# تهيئة الحالة
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'current_page' not in st.session_state: st.session_state.current_page = 0

# عرض الصفحة الرئيسية
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1><p>بوابة المستشار العقاري الذكية</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢 دليل المطورين الشامل", use_container_width=True): 
            st.session_state.view = 'comp'; st.session_state.current_page = 0; st.rerun()
    with c2:
        if st.button("🛠️ أدوات البروكر الذكية", use_container_width=True): 
            st.session_state.view = 'tools'; st.rerun()

# (بقية الكود الخاص بالدليل والأدوات يتبع نفس المنطق السابق...)
elif st.session_state.view == 'comp':
    if st.session_state.selected_dev:
        dev_name = st.session_state.selected_dev
        row = df[df['Developer'] == dev_name].iloc[0]
        st.markdown(f'<div class="hero-banner"><h2>{dev_name}</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 العودة للقائمة"): st.session_state.selected_dev = None; st.rerun()
        
        col_r, col_l = st.columns([1.2, 1])
        with col_r:
            st.markdown(f'<div class="custom-card"><h3>👤 المالك</h3><p>{row.get("Owner", "-")}</p><h3>📖 الوصف</h3><p>{row.get("Description", "-")}</p></div>', unsafe_allow_html=True)
        with col_l:
            st.markdown(f'<div class="custom-card"><h3>🏗️ المشاريع</h3><b>📍 المناطق:</b> {row.get("Area", "-")}<br><b>💰 الأسعار:</b> {row.get("Price", "-")}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
        search = st.text_input("🔍 ابحث عن مطور...")
        dev_list = df['Developer'].unique()
        if search: dev_list = [d for d in dev_list if search.lower() in str(d).lower()]
        
        # عرض المطورين بشكل شبكي
        for i in range(0, len(dev_list[:12]), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(dev_list):
                    d = dev_list[i + j]
                    if cols[j].button(d, key=f"d_{d}", use_container_width=True):
                        st.session_state.selected_dev = d; st.rerun()

elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
    st.info("حاسبات الأقساط والـ ROI متاحة هنا..")
