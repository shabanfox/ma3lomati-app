import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# تصميم CSS فاخر ومطور
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8f9fa; 
    }
    
    /* ستايل صفحة تسجيل الدخول الفاخرة */
    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80vh;
    }
    
    .login-box {
        width: 100%;
        max-width: 500px;
        padding: 50px;
        background: #000000;
        border-radius: 30px;
        border: 5px solid #f59e0b;
        box-shadow: 20px 20px 0px rgba(0,0,0,0.1);
        text-align: center;
        margin: auto;
    }

    .login-box h1 {
        color: #f59e0b;
        font-weight: 900;
        font-size: 2.5rem;
        margin-bottom: 10px;
        border-bottom: 2px solid #f59e0b;
        display: inline-block;
        padding-bottom: 10px;
    }

    .login-box p {
        color: #ffffff;
        font-size: 1.2rem;
        margin-bottom: 30px;
        opacity: 0.9;
    }

    /* زر الخروج الثابت */
    .logout-container {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 999999;
    }

    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 30px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000;
        margin-top: 60px;
    }

    .custom-card {
        background: #ffffff; border: 4px solid #000; padding: 25px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000;
    }

    .card-title { font-size: 1.8rem; font-weight: 900; color: #f59e0b; border-bottom: 3px solid #000; padding-bottom: 10px; margin-bottom: 15px; }
    
    /* ستايل الأزرار */
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 4px 4px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
        font-size: 1.2rem !important; min-height: 55px !important;
        transition: 0.3s;
    }
    div.stButton > button:hover { transform: translate(-3px, -3px); box-shadow: 7px 7px 0px #f59e0b !important; }
    
    /* تخصيص زر الدخول داخل الصندوق */
    .login-box div.stButton > button {
        background-color: #f59e0b !important;
        color: #000 !important;
        width: 100%;
        margin-top: 20px;
    }

    /* ستايل المدخلات */
    .stTextInput input {
        border: 3px solid #f59e0b !important;
        border-radius: 12px !important;
        padding: 15px !important;
        background: #111 !important;
        color: #fff !important;
        text-align: center;
        font-size: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. نظام تسجيل الدخول ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def login_page():
    # استخدام حاوية لتوسيط الصندوق
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown('<h1>🏠 معلوماتى</h1>', unsafe_allow_html=True)
        st.markdown('<p>المنصة الذكية للمستشار العقاري المحترف</p>', unsafe_allow_html=True)
        
        # حقل كلمة المرور
        pwd = st.text_input("أدخل كلمة المرور السرية", type="password", key="pwd_field", label_visibility="collapsed")
        
        if st.button("تسجيل الدخول الآمن"):
            if pwd == "Ma3lomati_2026":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.markdown('<p style="color:#ff4b4b; font-weight:bold; margin-top:10px;">⚠️ كلمة المرور غير صحيحة</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# حماية المحتوى
if not st.session_state.authenticated:
    login_page()
    st.stop()

# --- زر الخروج الثابت ---
st.markdown('<div class="logout-container">', unsafe_allow_html=True)
if st.button("🔒 خروج", key="logout_btn"):
    st.session_state.authenticated = False
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- 3. وظيفة جلب البيانات ---
@st.cache_data(ttl=300)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"خطأ في الاتصال: {e}")
        return pd.DataFrame()

# تهيئة الحالة
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'current_page' not in st.session_state: st.session_state.current_page = 0

df = load_data()

# --- 4. المحتوى الرئيسي ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1><p>دليل المطورين وأدوات التحليل العقاري</p></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢 دليل المطورين الشامل", use_container_width=True): 
            st.session_state.view = 'comp'; st.session_state.current_page = 0; st.rerun()
    with c2:
        if st.button("🛠️ أدوات البروكر الذكية", use_container_width=True): 
            st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'comp':
    if st.session_state.selected_dev:
        # صفحة التفاصيل
        dev_name = st.session_state.selected_dev
        row = df[df['Developer'] == dev_name].iloc[0]
        st.markdown(f'<div class="hero-banner"><h2>{dev_name}</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 العودة للقائمة"): 
            st.session_state.selected_dev = None; st.rerun()
        
        col_r, col_l = st.columns([1.2, 1])
        with col_r:
            st.markdown(f'<div class="custom-card"><div class="card-title">👤 تفاصيل المالك</div><p>{row.get("Owner", "غير متوفر")}</p><div class="card-title" style="margin-top:20px;">📖 فلسفة الشركة</div><p>{row.get("Description", "لا يوجد وصف")}</p></div>', unsafe_allow_html=True)
        with col_l:
            st.markdown(f'<div class="custom-card"><div class="card-title">🏗️ معلومات المشاريع</div><b>📍 المناطق:</b> {row.get("Area", "-")}<br><b>💰 الأسعار:</b> {row.get("Price", "-")}<br><b>💵 المقدم:</b> {row.get("Down_Payment", "-")}<br><b>📅 التقسيط:</b> {row.get("Installments", "-")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="custom-card"><div class="card-title">💡 سابقة الأعمال</div><p style="font-weight:900; color:#f59e0b;">{row.get("Projects", "-")}</p><hr>{row.get("Detailed_Info", "لا توجد تفاصيل إضافية")}</div>', unsafe_allow_html=True)

    else:
        st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
        col_main, _ = st.columns([0.7, 0.3])
        with col_main:
            if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
            search = st.text_input("🔍 ابحث عن مطور...")
            dev_list = df['Developer'].unique()
            if search: dev_list = [d for d in dev_list if search.lower() in str(d).lower()]
            
            items_per_page = 9
            total_pages = (len(dev_list) - 1) // items_per_page + 1
            start_idx = st.session_state.current_page * items_per_page
            current_devs = dev_list[start_idx:start_idx + items_per_page]

            for i in range(0, len(current_devs), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_devs):
                        d_name = current_devs[i + j]
                        if cols[j].button(d_name, key=f"btn_{d_name}", use_container_width=True):
                            st.session_state.selected_dev = d_name; st.rerun()

            st.write("---")
            nav_prev, nav_page, nav_next = st.columns([1, 2, 1])
            with nav_prev:
                if st.session_state.current_page > 0:
                    if st.button("⬅️ السابق"): st.session_state.current_page -= 1; st.rerun()
            with nav_page:
                st.markdown(f"<p style='text-align:center; font-weight:bold;'>صفحة {st.session_state.current_page + 1} من {total_pages}</p>", unsafe_allow_html=True)
            with nav_next:
                if (start_idx + items_per_page) < len(dev_list):
                    if st.button("التالي ➡️"): st.session_state.current_page += 1; st.rerun()

elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر المحترف</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
    
    t1, t2 = st.columns(2)
    with t1:
        st.markdown('<div class="custom-card"><div class="card-title">💰 حاسبة الأقساط</div></div>', unsafe_allow_html=True)
        total_price = st.number_input("إجمالي سعر الوحدة", min_value=0, step=100000)
        down_payment_pct = st.number_input("نسبة المقدم (%)", min_value=0, max_value=100, step=5)
        years = st.number_input("سنوات التقسيط", min_value=1, max_value=30, step=1)
        
        if total_price > 0:
            down_val = total_price * (down_payment_pct / 100)
            remaining = total_price - down_val
            monthly = remaining / (years * 12)
            st.markdown(f'<div style="background:#000; color:#f59e0b; padding:20px; border-radius:15px; text-align:center;"><h3>المقدم: {down_val:,.0f} ج.م</h3><h2>القسط: {monthly:,.0f} ج.م</h2></div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="custom-card"><div class="card-title">📈 حاسبة العائد ROI</div></div>', unsafe_allow_html=True)
        investment = st.number_input("المبلغ المستثمر", min_value=0, step=100000)
        expected_rent = st.number_input("الإيجار الشهري", min_value=0, step=1000)
        
        if investment > 0 and expected_rent > 0:
            annual_income = expected_rent * 12
            roi = (annual_income / investment) * 100
            st.markdown(f'<div style="background:#f59e0b; color:#000; padding:20px; border-radius:15px; text-align:center; border:3px solid #000;"><h3>الدخل السنوي: {annual_income:,.0f} ج.م</h3><h2>العائد: {roi:.2f}% سنوياً</h2></div>', unsafe_allow_html=True)
