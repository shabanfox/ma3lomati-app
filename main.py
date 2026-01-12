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
    .block-container { padding-top: 0rem !important; margin-top: -10px; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: RTL !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    
    .logout-btn button { background-color: #ff4b4b !important; color: white !important; border: none !important; width: auto !important; padding: 0 20px !important; }
    .oval-header { background-color: #000; border: 3px solid #f59e0b; border-radius: 50px; padding: 10px 30px; width: fit-content; margin: 10px auto 20px auto; text-align: center; box-shadow: 0px 4px 15px rgba(245, 158, 11, 0.4); }
    .header-title { color: #f59e0b; font-weight: 900; font-size: 26px !important; margin: 0; }
    .right-header { color: #f59e0b; font-weight: 900; border-right: 8px solid #f59e0b; padding-right: 15px; margin-bottom: 20px; font-size: 22px; }
    .grid-card { background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; border-radius: 12px; padding: 15px; height: 165px; margin-bottom: 10px; transition: 0.3s; }
    .grid-card:hover { border: 1px solid #f59e0b; transform: translateY(-5px); }
    .filter-box { background: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px; }
    .stButton button { background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; width: 100% !important; }
    </style>
""", unsafe_allow_html=True)

# 3. نظام الدخول (2026)
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown('<div class="oval-header"><h1 class="header-title">منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
    pwd = st.text_input("أدخل الباسورد", type="password")
    if st.button("دخول"):
        if pwd == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- بعد الدخول ---
col_top_L, _ = st.columns([1, 1])
with col_top_L:
    if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()

st.markdown('<div class="oval-header"><h1 class="header-title">منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
menu = option_menu(None, ["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], icons=["tools", "building", "person-vcard"], orientation="horizontal")

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

# توزيع المساحة 70% يمين
main_col, empty_col = st.columns([0.7, 0.3])

with main_col:
    if menu == "🏗️ المشاريع":
        st.markdown("<h1 class='right-header'>الفلاتر المتقدمة للمشاريع</h1>", unsafe_allow_html=True)
        
        # حاوية الفلاتر
        with st.container():
            st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
            row1_1, row1_2 = st.columns(2)
            with row1_1:
                f_search = st.text_input("🔍 بحث بالاسم", placeholder="اكتب اسم المشروع...")
            with row1_2:
                f_area = st.multiselect("📍 المناطق", options=sorted(df['Area'].unique().tolist()))
            
            row2_1, row2_2 = st.columns(2)
            with row2_1:
                f_dev = st.multiselect("🏢 المطور العقاري", options=sorted(df['Developer'].unique().tolist()))
            with row2_2:
                f_cons = st.selectbox("👷 الاستشاري الهندي", ["الكل"] + sorted(df['Consultant'].unique().tolist()))
            st.markdown("</div>", unsafe_allow_html=True)

        # منطق الفلترة القوي
        dff = df.copy()
        if f_search: dff = dff[dff['Project Name'].str.contains(f_search, case=False)]
        if f_area: dff = dff[dff['Area'].isin(f_area)]
        if f_dev: dff = dff[dff['Developer'].isin(f_dev)]
        if f_cons != "الكل": dff = dff[dff['Consultant'] == f_cons]

        st.markdown(f"**نتائج البحث:** {len(dff)} مشروع")
        
        # عرض الشبكة 3×3
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
                            <h3 style='color:#f59e0b; font-size:16px;'>{row['Project Name']}</h3>
                            <p style='font-size:13px;'>🏢 {row['Developer']}</p>
                            <p style='font-size:12px; color:#888;'>📍 {row['Area']}</p>
                        </div>""", unsafe_allow_html=True)
                        with st.expander("🔎 تفاصيل"):
                            st.write(f"👷 الاستشاري: {row['Consultant']}")
                            st.write(f"⭐ الميزة: {row['Competitive Advantage']}")

        # أزرار التنقل
        st.write("---")
        b1, b2, _ = st.columns([0.2, 0.2, 0.6])
        if b1.button("التالي ⬅️") and st.session_state.p_idx < total_p - 1: st.session_state.p_idx += 1; st.rerun()
        if b2.button("➡️ السابق") and st.session_state.p_idx > 0: st.session_state.p_idx -= 1; st.rerun()

    elif menu == "🏢 المطورين":
        st.markdown("<h1 class='right-header'>دليل المطورين المحترف</h1>", unsafe_allow_html=True)
        
        dev_df = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates()
        
        # فلاتر المطورين
        st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
        d_col1, d_col2 = st.columns(2)
        with d_col1: d_name = st.text_input("🔍 اسم الشركة")
        with d_col2: d_owner = st.text_input("👤 اسم المالك")
        st.markdown("</div>", unsafe_allow_html=True)

        if d_name: dev_df = dev_df[dev_df['Developer'].str.contains(d_name, case=False)]
        if d_owner: dev_df = dev_df[dev_df['Owner'].str.contains(d_owner, case=False)]

        curr_devs = dev_df.head(grid_limit)
        for i in range(0, len(curr_devs), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(curr_devs):
                    row = curr_devs.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h4 style='color:#f59e0b;'>{row['Developer']}</h4><p>👤 {row['Owner']}</p></div>", unsafe_allow_html=True)
                        with st.expander("الملف التعريفي"): st.write(row['Detailed_Info'])

    elif menu == "🛠️ أدوات البروكر":
        st.markdown("<h1 class='right-header'>أدوات العمل</h1>", unsafe_allow_html=True)
        # (نفس أدوات البروكر السابقة مع تفعيل كامل)
        p = st.number_input("سعر الوحدة", 1000000)
        st.info(f"قسط الـ 8 سنوات: {p/96:,.0f} ج.م")
