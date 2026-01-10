import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتصميم الأساسي
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# تصميم CSS شامل (حماية + تنسيق احترافي أسود وغامق)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* حماية الكود ومنع النسخ */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    * { -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* زر تسجيل الدخول فوق الهيدر على اليسار */
    .top-nav {
        display: flex;
        justify-content: flex-start;
        padding: 10px 20px;
        background: transparent;
    }
    .login-btn {
        background-color: #000; color: #f59e0b !important;
        padding: 8px 25px; border-radius: 12px; border: 2px solid #f59e0b;
        font-weight: 900; text-decoration: none; font-size: 1rem;
        box-shadow: 4px 4px 0px #f59e0b; transition: 0.3s;
    }

    /* الهيدر الرئيسي */
    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000;
    }

    /* الكروت والحاسبات */
    .custom-card, .calc-container {
        background: #ffffff; border: 4px solid #000; padding: 20px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000;
    }
    .calc-container { background-color: #0a0a0a; border: 3px solid #f59e0b; color: white; }
    
    .card-title, .calc-title { 
        font-size: 1.8rem; font-weight: 900; color: #f59e0b; 
        border-bottom: 3px solid #f59e0b; padding-bottom: 10px; margin-bottom: 15px; 
    }
    
    .result-box {
        background: #1a1a1a; border-right: 5px solid #f59e0b;
        padding: 15px; border-radius: 10px; margin-top: 15px;
    }

    /* أزرار الموقع */
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 4px 4px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
        min-height: 55px !important; width: 100%;
    }
    div.stButton > button:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0px #f59e0b !important; }
    </style>
""", unsafe_allow_html=True)

# 2. نظام الحماية وكلمة المرور
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown('<div class="hero-banner"><h1>🔒 منطقة محظورة</h1></div>', unsafe_allow_html=True)
    col_l, col_m, col_r = st.columns([1,2,1])
    with col_m:
        pwd = st.text_input("أدخل كلمة المرور للوصول", type="password")
        if st.button("فتح المنصة"):
            if pwd == "Ma3lomati_2026": # كلمة السر الخاصة بك
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة")
    st.stop()

# 3. وظيفة جلب البيانات من Google Sheets
@st.cache_data(ttl=300)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"خطأ في التحميل: {e}")
        return pd.DataFrame()

df = load_data()

# تهيئة التنقل
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'current_page' not in st.session_state: st.session_state.current_page = 0

# زر تسجيل الدخول في الأعلى
st.markdown('<div class="top-nav"><a href="#" class="login-btn">تسجيل الخروج</a></div>', unsafe_allow_html=True)

# --- محتوى المنصة ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢 دليل المطورين الشامل"): 
            st.session_state.view = 'comp'; st.session_state.current_page = 0; st.rerun()
    with c2:
        if st.button("🛠️ أدوات البروكر الذكية"): 
            st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'comp':
    if st.session_state.selected_dev:
        # صفحة تفاصيل المطور
        dev_name = st.session_state.selected_dev
        row = df[df['Developer'] == dev_name].iloc[0]
        st.markdown(f'<div class="hero-banner"><h2>{dev_name}</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 العودة"): st.session_state.selected_dev = None; st.rerun()
        
        col_r, col_l = st.columns([1.2, 1])
        with col_r:
            st.markdown(f'<div class="custom-card"><div class="card-title">👤 تفاصيل المالك</div><p>{row.get("Owner", "-")}</p><div class="card-title">📖 الوصف</div><p>{row.get("Description", "-")}</p></div>', unsafe_allow_html=True)
        with col_l:
            st.markdown(f'<div class="custom-card"><div class="card-title">🏗️ معلومات البيع</div><p><b>📍 المنطقة:</b> {row.get("Area", "-")}</p><p><b>💰 الأسعار:</b> {row.get("Price", "-")}</p><p><b>📅 التقسيط:</b> {row.get("Installments", "-")}</p></div>', unsafe_allow_html=True)
    else:
        # قائمة المطورين
        st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
        search = st.text_input("🔍 ابحث عن مطور...")
        
        dev_list = df['Developer'].unique()
        if search: dev_list = [d for d in dev_list if search.lower() in str(d).lower()]
        
        items_per_page = 9
        total_pages = (len(dev_list)-1)//items_per_page + 1
        start = st.session_state.current_page * items_per_page
        current_devs = dev_list[start:start+items_per_page]

        for i in range(0, len(current_devs), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(current_devs):
                    name = current_devs[i+j]
                    if cols[j].button(name, key=f"d_{name}"):
                        st.session_state.selected_dev = name; st.rerun()
        
        # التنقل بين الصفحات
        n1, n2, n3 = st.columns([1,2,1])
        with n1: 
            if st.session_state.current_page > 0 and st.button("⬅️ السابق"):
                st.session_state.current_page -= 1; st.rerun()
        with n3:
            if start + items_per_page < len(dev_list) and st.button("التالي ➡️"):
                st.session_state.current_page += 1; st.rerun()

elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر المحترف</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="calc-container"><div class="calc-title">💰 حاسبة الأقساط</div>', unsafe_allow_html=True)
        p = st.number_input("سعر الوحدة", min_value=0, step=100000, key="p_calc")
        d = st.number_input("المقدم (%)", min_value=0, max_value=100, step=5, key="d_calc")
        y = st.number_input("السنوات", min_value=1, max_value=30, step=1, key="y_calc")
        if p > 0:
            monthly = (p - (p*d/100)) / (y*12)
            st.markdown(f'<div class="result-box"><h3>القسط الشهري:</h3><h2>{monthly:,.0f} ج.م</h2></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="calc-container"><div class="calc-title">📈 العائد ROI & Yield</div>', unsafe_allow_html=True)
        inv = st.number_input("قيمة الاستثمار", min_value=0, step=100000, key="inv_calc")
        rent = st.number_input("الإيجار الشهري", min_value=0, step=1000, key="rent_calc")
        if inv > 0:
            yield_pct = ((rent * 12) / inv) * 100
            st.markdown(f'<div class="result-box"><h3>عائد الإيجار السنوي:</h3><h2 style="color:#2ecc71;">{yield_pct:.2f}%</h2></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
