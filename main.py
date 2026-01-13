import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = 'Arabic'

# نصوص الواجهة
ui = {
    'Arabic': {
        'title': "منصة معلوماتي العقارية", 'projects': "🏗️ المشاريع", 'devs': "🏢 المطورين", 
        'tools': "🛠️ أدوات البروكر", 'logout': "🚪 خروج", 'search': "🔍 بحث بالاسم...", 
        'filter_area': "📍 تصفية بالمنطقة", 'details': "🔎 تفاصيل", 'next': "التالي ⬅️", 'prev': "➡️ السابق", 'dir': "rtl", 'align': "right"
    },
    'English': {
        'title': "Ma3lomati Real Estate", 'projects': "🏗️ Projects", 'devs': "🏢 Developers", 
        'tools': "🛠️ Tools", 'logout': "🚪 Logout", 'search': "🔍 Search Name...", 
        'filter_area': "📍 Area Filter", 'details': "🔎 Details", 'next': "Next ➡️", 'prev': "⬅️ Prev", 'dir': "ltr", 'align': "left"
    }
}
T = ui[st.session_state.lang]

# 3. التنسيق (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: {T['dir']} !important; text-align: {T['align']} !important; font-family: 'Cairo', sans-serif; }}
    .oval-header {{ background-color: #000; border: 3px solid #f59e0b; border-radius: 50px; padding: 10px 30px; width: fit-content; margin: 10px auto 20px auto; text-align: center; box-shadow: 0px 4px 15px rgba(245, 158, 11, 0.4); }}
    .header-title {{ color: #f59e0b; font-weight: 900; font-size: 26px !important; margin: 0; }}
    .grid-card {{ background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; border-radius: 12px; padding: 15px; height: 165px; margin-bottom: 10px; }}
    .filter-box {{ background: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px; }}
    .stButton button {{ background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; }}
    </style>
""", unsafe_allow_html=True)

# 4. جلب البيانات وحذف المتكرر
@st.cache_data(ttl=60)
def load_data():
    # تحويل الروابط إلى صيغة CSV المباشرة
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        # حذف الصفوف المتكررة بناءً على اسم المشروع
        df = df.drop_duplicates(subset=['Project Name']).fillna("غير متوفر").astype(str)
        return df
    except:
        return pd.DataFrame()

df = load_data()

# 5. نظام الدخول
if not st.session_state.auth:
    st.markdown(f'<div class="oval-header"><h1 class="header-title">{T["title"]}</h1></div>', unsafe_allow_html=True)
    pwd = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        if pwd == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- بعد الدخول ---
top_L, top_R = st.columns([1, 1])
with top_L:
    if st.button(T['logout']): st.session_state.auth = False; st.rerun()
with top_R:
    if st.button("🇺🇸 EN / 🇪🇬 AR"):
        st.session_state.lang = 'English' if st.session_state.lang == 'Arabic' else 'Arabic'
        st.rerun()

st.markdown(f'<div class="oval-header"><h1 class="header-title">{T["title"]}</h1></div>', unsafe_allow_html=True)

menu = option_menu(None, [T['tools'], T['projects'], T['devs']], icons=["tools", "building", "person-vcard"], orientation="horizontal")

# تقسيم المساحة 70%
if st.session_state.lang == 'Arabic': main_col, _ = st.columns([0.7, 0.3])
else: _, main_col = st.columns([0.3, 0.7])

with main_col:
    if menu == T['projects']:
        st.markdown(f"<h2 style='color:#f59e0b;'>{T['projects']}</h2>", unsafe_allow_html=True)
        
        # الفلاتر
        st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        with f1: search = st.text_input(T['search'])
        with f2: 
            areas = ["الكل"] + sorted(df['Area'].unique().tolist()) if not df.empty else []
            sel_area = st.selectbox(T['filter_area'], areas)
        st.markdown("</div>", unsafe_allow_html=True)

        # تصفية
        dff = df.copy()
        if search: dff = dff[dff['Project Name'].str.contains(search, case=False)]
        if sel_area != "الكل": dff = dff[dff['Area'] == sel_area]

        # الشبكة
        grid_limit = 9
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
                            <p style='color:#888;'>📍 {row['Area']}</p>
                        </div>""", unsafe_allow_html=True)
                        with st.expander(T['details']):
                            st.write(f"✅ المميزات: {row.get('Project Features', 'N/A')}")
                            st.write(f"⚠️ العيوب: {row.get('Project Flaws', 'N/A')}")

        # التنقل
        st.write("---")
        b1, b2, _ = st.columns([0.2, 0.2, 0.6])
        if b1.button(T['next']) and st.session_state.p_idx < total_p - 1: st.session_state.p_idx += 1; st.rerun()
        if b2.button(T['prev']) and st.session_state.p_idx > 0: st.session_state.p_idx -= 1; st.rerun()

    elif menu == T['tools']:
        st.info("أدوات البروكر (حاسبة الأقساط والعمولة) مفعلة وجاهزة.")
        p = st.number_input("سعر الوحدة", 1000000)
        st.success(f"قسط الـ 8 سنوات: {p/96:,.0f} ج.م")
