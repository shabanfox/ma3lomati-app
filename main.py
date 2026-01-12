import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة وإزالة الفراغات
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق (CSS) - تركيز كامل على الجهة اليمنى
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container { padding-top: 0rem !important; margin-top: -20px; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    
    [data-testid="stAppViewContainer"] { 
        background-color: #050505; 
        direction: RTL !important; 
        text-align: right !important; 
        font-family: 'Cairo', sans-serif; 
    }

    /* الهيدر البيضاوي */
    .oval-header {
        background-color: #000;
        border: 3px solid #f59e0b;
        border-radius: 50px;
        padding: 10px 30px;
        width: fit-content;
        margin: 0 auto 20px auto;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(245, 158, 11, 0.4);
    }
    .header-title { color: #f59e0b; font-weight: 900; font-size: 26px !important; margin: 0; }

    /* ستايل صفحة الدخول */
    .login-box {
        max-width: 400px;
        margin: 40px auto;
        padding: 30px;
        background: #111;
        border-radius: 20px;
        border: 1px solid #222;
        text-align: center;
    }
    div[data-baseweb="input"] { background-color: white !important; border-radius: 8px !important; }
    input { color: black !important; font-weight: bold !important; text-align: center !important; }

    /* العناوين والأزرار في اليمين */
    .right-header {
        color: #f59e0b;
        text-align: right !important;
        font-weight: 900;
        border-right: 10px solid #f59e0b;
        padding-right: 15px;
        margin: 20px 0;
        font-size: 24px;
    }

    /* الكروت الشبكية */
    .grid-card {
        background: #111;
        border: 1px solid #222;
        border-top: 4px solid #f59e0b;
        border-radius: 12px;
        padding: 15px;
        height: 180px;
        margin-bottom: 10px;
        text-align: right;
    }

    /* محاذاة أزرار ستريمليت لليمين */
    .stButton { text-align: right !important; }
    .stButton button { 
        background-color: #1a1a1a !important; 
        color: #f59e0b !important; 
        border: 1px solid #333 !important;
        width: auto !important;
        min-width: 120px;
    }
    
    /* قائمة الخيارات محاذاة لليمين */
    .nav-link-selected { background-color: #f59e0b !important; }
    </style>
""", unsafe_allow_html=True)

# 3. حماية الدخول (2026)
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="oval-header"><h1 class="header-title">منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#f59e0b; font-size:50px;'>🔒</h1>", unsafe_allow_html=True)
    pwd = st.text_input("أدخل كلمة المرور", type="password")
    if st.button("دخول"):
        if pwd == "2026":
            st.session_state.auth = True
            st.rerun()
        else: st.error("خطأ في الباسورد")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# 4. تحميل البيانات
@st.cache_data(ttl=60)
def load_data():
    urls = [
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv",
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    ]
    dfs = [pd.read_csv(u) for u in urls]
    combined = pd.concat(dfs, ignore_index=True)
    combined.columns = [str(c).strip() for c in combined.columns]
    return combined.fillna("غير متوفر").astype(str)

df = load_data()
grid_limit = 9

# الهيدر العلوي
st.markdown('<div class="oval-header"><h1 class="header-title">منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

# المنيو - جعلناه في اليمين عبر الأعمدة
m_col1, m_col2 = st.columns([0.7, 0.3])
with m_col2:
    selected = option_menu(None, ["🏢 المطورين", "🏗️ المشاريع", "🛠️ الأدوات"], 
                          icons=["person-vcard", "building", "tools"], 
                          menu_icon="cast", default_index=1,
                          styles={"container": {"background-color": "#000", "border": "1px solid #222"}})

# زر الخروج في أقصى اليمين تحت المنيو
with m_col2:
    if st.button("🚪 خروج من النظام"):
        st.session_state.auth = False
        st.rerun()

# --- قسم المشاريع ---
if selected == "🏗️ المشاريع":
    st.markdown("<h1 class='right-header'>دليل المشاريع العقارية</h1>", unsafe_allow_html=True)
    
    # محاذاة البحث لليمين
    s_col1, s_col2 = st.columns([0.6, 0.4])
    with s_col2: search = st.text_input("🔍 ابحث عن مشروع...")
    
    dff = df.copy()
    if search: dff = dff[dff.apply(lambda r: search.lower() in r.astype(str).str.lower().values, axis=1)]

    if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
    pages_count = math.ceil(len(dff) / grid_limit)
    curr_df = dff.iloc[st.session_state.p_idx * grid_limit : (st.session_state.p_idx + 1) * grid_limit]

    # عرض الشبكة
    for i in range(0, len(curr_df), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(curr_df):
                row = curr_df.iloc[i + j]
                with cols[j]:
                    st.markdown(f"""<div class='grid-card'>
                        <h3 style='color:#f59e0b;'>{row['Project Name']}</h3>
                        <p>🏢 {row['Developer']}</p>
                        <p style='color:#777; font-size:12px;'>📍 {row['Area']}</p>
                    </div>""", unsafe_allow_html=True)
                    with st.expander("التفاصيل الفنية"):
                        st.write(f"👷 الاستشاري: {row['Consultant']}")
                        st.write(f"⭐ الميزة: {row['Competitive Advantage']}")

    # أزرار التنقل - في اليمين تماماً
    st.write("---")
    nav_col1, nav_col2, nav_col3 = st.columns([0.15, 0.15, 0.7])
    with nav_col1:
        if st.button("التالي ⬅️") and st.session_state.p_idx < pages_count - 1:
            st.session_state.p_idx += 1; st.rerun()
    with nav_col2:
        if st.button("➡️ السابق") and st.session_state.p_idx > 0:
            st.session_state.p_idx -= 1; st.rerun()
    
    st.markdown(f"<p style='text-align:right;'>صفحة {st.session_state.p_idx + 1} من {pages_count}</p>", unsafe_allow_html=True)

# --- قسم المطورين ---
elif selected == "🏢 المطورين":
    st.markdown("<h1 class='right-header'>دليل المطورين</h1>", unsafe_allow_html=True)
    devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer'])
    
    if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
    dev_pages = math.ceil(len(devs) / grid_limit)
    curr_devs = devs.iloc[st.session_state.d_idx * grid_limit : (st.session_state.d_idx + 1) * grid_limit]

    for i in range(0, len(curr_devs), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(curr_devs):
                row = curr_devs.iloc[i + j]
                with cols[j]:
                    st.markdown(f"<div class='grid-card'><h3 style='color:#f59e0b;'>{row['Developer']}</h3><p>👤 {row['Owner']}</p></div>", unsafe_allow_html=True)
                    with st.expander("بروفايل الشركة"):
                        st.write(row['Detailed_Info'])

    # أزرار تنقل المطورين يمين
    st.write("---")
    dn1, dn2, _ = st.columns([0.15, 0.15, 0.7])
    with hide1 := dn1:
        if st.button("التالي ⬅️", key="dnxt") and st.session_state.d_idx < dev_pages - 1:
            st.session_state.d_idx += 1; st.rerun()
    with hide2 := dn2:
        if st.button("➡️ السابق", key="dprv") and st.session_state.d_idx > 0:
            st.session_state.d_idx -= 1; st.rerun()

# --- قسم الأدوات ---
elif selected == "🛠️ الأدوات":
    st.markdown("<h1 class='right-header'>أدوات البروكر</h1>", unsafe_allow_html=True)
    # تفعيل الأدوات هنا بوضوح
    t_col1, t_col2 = st.columns(2)
    with t_col2:
        st.info("💰 حاسبة الأقساط والمساحات قيد العمل")
        price = st.number_input("سعر الوحدة", 1000000)
        st.success(f"قسط الـ 8 سنوات التقريبي: {price/96:,.0f} ج.م")
