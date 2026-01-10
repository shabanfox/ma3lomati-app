import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS المطور
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] > section:first-child > div:first-child { padding-top: 0rem !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* العنوان البيضاوي المنسدل */
    .hero-oval-header {
        background: #000000; border: 5px solid #f59e0b; border-top: none; 
        padding: 40px 20px; border-radius: 0px 0px 500px 500px; 
        text-align: center; width: 100%; max-width: 800px; margin: 0 auto 20px auto;
        box-shadow: 0px 15px 30px rgba(0,0,0,0.2);
    }
    .hero-oval-header h1 { color: #f59e0b; font-weight: 900; font-size: 2.2rem; margin: 0; }

    /* ستايل الكروت والأدوات */
    .custom-card {
        background: #ffffff; border: 4px solid #000; padding: 20px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000;
    }
    .project-tag {
        background: #000; color: #f59e0b; padding: 5px 12px; 
        border-radius: 50px; font-size: 0.85rem; font-weight: 700;
        display: inline-block; margin: 3px; border: 1px solid #f59e0b;
    }

    /* أزرار التنقل الرئيسية */
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 4px 4px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important; height: 60px !important;
    }
    div.stButton > button:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0px #f59e0b !important; }
    
    .logout-box { position: fixed; top: 10px; left: 10px; z-index: 999; }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة الجلسة والبيانات
if 'auth' not in st.session_state: st.session_state.auth = False
if 'view' not in st.session_state: st.session_state.view = 'comp' # الافتراضي دليل المطورين
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None

@st.cache_data(ttl=300)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except: return pd.DataFrame()

# 4. شاشة الدخول
if not st.session_state.auth:
    st.markdown('<div class="hero-oval-header"><h1>منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        pwd = st.text_input("قفل الدخول", type="password", placeholder="أدخل كلمة المرور")
        if st.button("فتح المنصة", use_container_width=True):
            if pwd == "Ma3lomati_2026": st.session_state.auth = True; st.rerun()
            else: st.error("❌ خطأ في كلمة المرور")
    st.stop()

# --- واجهة المنصة بعد الدخول ---
df = load_data()

# الهيدر البيضاوي ثابت في كل الصفحات
st.markdown('<div class="hero-oval-header"><h1>منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

# زر الخروج العائم
st.markdown('<div class="logout-box">', unsafe_allow_html=True)
if st.button("🔒 خروج"): st.session_state.auth = False; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- شريط التنقل الرئيسي (بديل كلمة الرئيسية) ---
n_col1, n_col2 = st.columns(2)
with n_col1:
    if st.button("🏢 دليل المطورين الشامل", use_container_width=True):
        st.session_state.view = 'comp'; st.session_state.selected_dev = None; st.rerun()
with n_col2:
    if st.button("🛠️ أدوات البروكر الذكية", use_container_width=True):
        st.session_state.view = 'tools'; st.rerun()

st.write("---")

# --- عرض المحتوى بناءً على الزر المختار ---
if st.session_state.view == 'comp':
    if st.session_state.selected_dev:
        # تفاصيل المطور المختارة
        name = st.session_state.selected_dev
        row = df[df['Developer'] == name].iloc[0]
        if st.button("🔙 العودة للقائمة"): st.session_state.selected_dev = None; st.rerun()
        
        cr, cl = st.columns([1.3, 1])
        with cr:
            st.markdown(f'<div class="custom-card"><h3>👤 المالك</h3><p>{row.get("Owner", "-")}</p><h3>📖 الوصف</h3><p>{row.get("Description", "-")}</p></div>', unsafe_allow_html=True)
            with st.expander("🏗️ محفظة المشاريع", expanded=True):
                projects = str(row.get("Projects", "-")).split(",")
                for p in projects:
                    st.markdown(f'<span class="project-tag">🔹 {p.strip()}</span>', unsafe_allow_html=True)
        with cl:
            st.markdown(f'<div class="custom-card"><h3>📊 بيانات المشاريع</h3><b>📍 المناطق:</b> {row.get("Area", "-")}<br><b>💰 الأسعار:</b> {row.get("Price", "-")}<br><b>💵 المقدم:</b> {row.get("Down_Payment", "-")}<br><b>📅 التقسيط:</b> {row.get("Installments", "-")}</div>', unsafe_allow_html=True)
    else:
        # البحث والفلترة (الدليل)
        col_main, col_filter = st.columns([0.75, 0.25])
        with col_filter:
            st.markdown('<div class="custom-card" style="padding:10px;"><h4>🎯 فلاتر</h4></div>', unsafe_allow_html=True)
            all_areas = ["الكل"] + sorted(list(set([a.strip() for sublist in df['Area'].dropna().str.split(',') for a in sublist])))
            selected_area = st.selectbox("اختر منطقة:", all_areas)
        
        with col_main:
            search = st.text_input("🔍 ابحث عن مطور أو مشروع...")
            f_df = df.copy()
            if selected_area != "الكل":
                f_df = f_df[f_df['Area'].str.contains(selected_area, na=False)]
            if search:
                f_df = f_df[f_df['Developer'].str.contains(search, na=False, case=False) | f_df['Projects'].str.contains(search, na=False, case=False)]
            
            devs = f_df['Developer'].unique()
            for i in range(0, len(devs), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i+j < len(devs):
                        d_name = devs[i+j]
                        if cols[j].button(d_name, key=f"d_{d_name}", use_container_width=True):
                            st.session_state.selected_dev = d_name; st.rerun()

elif st.session_state.view == 'tools':
    # قسم الأدوات
    st.markdown('<h2 style="text-align:center;">🛠️ أدوات البروكر</h2>', unsafe_allow_html=True)
    t1, t2 = st.columns(2)
    with t1:
        st.markdown('<div class="custom-card"><h4>💰 حاسبة القسط</h4></div>', unsafe_allow_html=True)
        price = st.number_input("السعر الإجمالي", step=100000)
        down = st.number_input("المقدم (%)", 0, 100, 10)
        years = st.number_input("السنوات", 1, 30, 7)
        if price > 0:
            st.warning(f"القسط الشهري: {((price - (price*down/100)) / (years*12)):,.0f}")
    with t2:
        st.markdown('<div class="custom-card"><h4>📈 حساب ROI</h4></div>', unsafe_allow_html=True)
        inv = st.number_input("الاستثمار", step=100000)
        rent = st.number_input("الإيجار", step=1000)
        if inv > 0:
            st.success(f"العائد السنوي: {(rent*12/inv)*100:.2f}%")
