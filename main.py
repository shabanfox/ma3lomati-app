import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; margin-top: -20px; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: RTL !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    .oval-header { background-color: #000; border: 3px solid #f59e0b; border-radius: 50px; padding: 15px 30px; width: fit-content; margin: 0 auto 20px auto; text-align: center; box-shadow: 0px 4px 15px rgba(245, 158, 11, 0.4); }
    .header-title { color: #f59e0b; font-weight: 900; font-size: 28px !important; margin: 0; }
    .login-box { max-width: 400px; margin: 30px auto; padding: 30px; background: #111; border-radius: 20px; border: 1px solid #222; text-align: center; }
    div[data-baseweb="input"] { background-color: white !important; border-radius: 8px !important; }
    input { color: black !important; font-weight: bold !important; text-align: center !important; }
    .right-header { color: #f59e0b; text-align: right !important; font-weight: 900; border-right: 10px solid #f59e0b; padding-right: 15px; margin: 20px 0; font-size: 24px; }
    .grid-card { background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; border-radius: 12px; padding: 15px; height: 180px; margin-bottom: 15px; }
    .stButton button { background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

# 3. الدخول (2026)
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown('<div class="oval-header"><h1 class="header-title">منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#f59e0b; font-size:60px;'>🔒</h1>", unsafe_allow_html=True)
    pwd = st.text_input("أدخل الباسورد", type="password")
    if st.button("دخول للنظام"):
        if pwd == "2026":
            st.session_state.auth = True
            st.rerun()
        else: st.error("عفواً، الباسورد خطأ")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# 4. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u2 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        df1 = pd.read_csv(u1); df2 = pd.read_csv(u2)
        combined = pd.concat([df1, df2], ignore_index=True)
        combined.columns = [str(c).strip() for c in combined.columns]
        return combined.fillna("غير متوفر").astype(str)
    except: return pd.DataFrame()

df = load_data()
grid_limit = 9

st.markdown('<div class="oval-header"><h1 class="header-title">منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
c_out, _ = st.columns([1, 6])
with c_out: 
    if st.button("🚪 خروج"): 
        st.session_state.auth = False; st.rerun()

menu = option_menu(None, ["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], icons=["tools", "building", "person-vcard"], orientation="horizontal")

# --- 🏗️ قسم المشاريع مع فلاتر جديدة ---
if menu == "🏗️ المشاريع":
    st.markdown("<h1 class='right-header'>دليل المشاريع العقارية</h1>", unsafe_allow_html=True)
    
    # صف البحث والفلاتر
    f_col1, f_col2, f_col3 = st.columns([0.4, 0.3, 0.3])
    with f_col1:
        search = st.text_input("🔍 بحث شامل (مشروع، مطور، كلمة)...", placeholder="اكتب هنا للبحث")
    with f_col2:
        areas = ["الكل"] + sorted(df['Area'].unique().tolist())
        selected_area = st.selectbox("📍 اختيار المنطقة", areas)
    with f_col3:
        devs_list = ["الكل"] + sorted(df['Developer'].unique().tolist())
        selected_dev = st.selectbox("🏢 تصفية بالمطور", devs_list)
    
    # تطبيق الفلاتر
    dff = df.copy()
    if search:
        dff = dff[dff.apply(lambda r: search.lower() in r.astype(str).str.lower().values, axis=1)]
    if selected_area != "الكل":
        dff = dff[dff['Area'] == selected_area]
    if selected_dev != "الكل":
        dff = dff[dff['Developer'] == selected_dev]

    # الترقيم والشبكة
    if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
    total_p = math.ceil(len(dff) / grid_limit)
    curr_df = dff.iloc[st.session_state.p_idx * grid_limit : (st.session_state.p_idx + 1) * grid_limit]

    for i in range(0, len(curr_df), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(curr_df):
                row = curr_df.iloc[i + j]
                with cols[j]:
                    st.markdown(f"""<div class='grid-card'>
                        <h3 style='color:#f59e0b; font-size:18px;'>{row['Project Name']}</h3>
                        <p style='font-size:14px;'>🏢 {row['Developer']}</p>
                        <p style='font-size:13px; color:#888;'>📍 {row['Area']}</p>
                    </div>""", unsafe_allow_html=True)
                    with st.expander("🔎 عرض التفاصيل"):
                        st.write(f"👷 الاستشاري: {row['Consultant']}")
                        st.write(f"⭐ الميزة: {row['Competitive Advantage']}")

    # أزرار التنقل يمين
    st.write("---")
    btn_r1, btn_r2, _ = st.columns([0.15, 0.15, 0.7])
    if btn_r1.button("التالي ⬅️", key="p_next"):
        if st.session_state.p_idx < total_p - 1: st.session_state.p_idx += 1; st.rerun()
    if btn_r2.button("➡️ السابق", key="p_prev"):
        if st.session_state.p_idx > 0: st.session_state.p_idx -= 1; st.rerun()
    st.markdown(f"<p style='text-align:right;'>عدد النتائج: {len(dff)} | صفحة {st.session_state.p_idx + 1} من {max(1, total_p)}</p>", unsafe_allow_html=True)

# --- 🏢 قسم المطورين ---
elif menu == "🏢 المطورين":
    st.markdown("<h1 class='right-header'>دليل المطورين</h1>", unsafe_allow_html=True)
    devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer'])
    
    # بحث في المطورين
    d_search = st.text_input("🔍 ابحث عن مطور...")
    if d_search:
        devs = devs[devs['Developer'].str.contains(d_search, case=False, na=False)]

    if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
    total_d = math.ceil(len(devs) / grid_limit)
    curr_devs = devs.iloc[st.session_state.d_idx * grid_limit : (st.session_state.d_idx + 1) * grid_limit]

    for i in range(0, len(curr_devs), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(curr_devs):
                row = curr_devs.iloc[i + j]
                with cols[j]:
                    st.markdown(f"<div class='grid-card'><h3 style='color:#f59e0b;'>{row['Developer']}</h3><p>👤 {row['Owner']}</p></div>", unsafe_allow_html=True)
                    with st.expander("📂 الملف"): st.write(row['Detailed_Info'])

    st.write("---")
    db_r1, db_r2, _ = st.columns([0.15, 0.15, 0.7])
    if db_r1.button("التالي ⬅️", key="d_next"):
        if st.session_state.d_idx < total_d - 1: st.session_state.d_idx += 1; st.rerun()
    if db_r2.button("➡️ السابق", key="d_prev"):
        if st.session_state.d_idx > 0: st.session_state.d_idx -= 1; st.rerun()

# --- 🛠️ قسم الأدوات ---
elif menu == "🛠️ أدوات البروكر":
    st.markdown("<h1 class='right-header'>أدوات العمل</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='tool-box'><h3>💰 حاسبة القسط</h3>", unsafe_allow_html=True)
        p = st.number_input("السعر", 1000000); y = st.number_input("السنوات", 8)
        st.markdown(f"<h4>القسط: {p/(max(1,y)*12):,.0f} ج.م</h4></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='tool-box'><h3>📝 مفكرة العميل</h3>", unsafe_allow_html=True)
        st.text_area("سجل الملاحظات...", height=150)
        st.markdown("</div>", unsafe_allow_html=True)
