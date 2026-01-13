import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (الدخول واللغة)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = 'Arabic'

# نصوص الواجهة المزدوجة
ui = {
    'Arabic': {
        'title': "منصة معلوماتي العقارية", 'projects': "🏗️ المشاريع", 'devs': "🏢 المطورين", 
        'tools': "🛠️ أدوات البروكر", 'logout': "🚪 خروج", 'search': "🔍 بحث بالاسم...", 
        'filter_area': "📍 المنطقة", 'filter_dev': "🏢 المطور", 'details': "🔎 التفاصيل", 
        'pros': "✅ المميزات", 'cons': "⚠️ العيوب", 'next': "التالي ⬅️", 'prev': "➡️ السابق", 
        'dir': "rtl", 'align': "right"
    },
    'English': {
        'title': "Ma3lomati Real Estate", 'projects': "🏗️ Projects", 'devs': "🏢 Developers", 
        'tools': "🛠️ Tools", 'logout': "🚪 Logout", 'search': "🔍 Search Name...", 
        'filter_area': "📍 Area", 'filter_dev': "🏢 Developer", 'details': "🔎 Details", 
        'pros': "✅ Features", 'cons': "⚠️ Flaws", 'next': "Next ➡️", 'prev': "⬅️ Prev", 
        'dir': "ltr", 'align': "left"
    }
}
T = ui[st.session_state.lang]

# 3. التنسيق المتقدم (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ 
        background-color: #050505; direction: {T['dir']} !important; 
        text-align: {T['align']} !important; font-family: 'Cairo', sans-serif; 
    }}
    .oval-header {{ background-color: #000; border: 3px solid #f59e0b; border-radius: 50px; padding: 10px 30px; width: fit-content; margin: 10px auto 20px auto; text-align: center; box-shadow: 0px 4px 15px rgba(245, 158, 11, 0.4); }}
    .header-title {{ color: #f59e0b; font-weight: 900; font-size: 26px !important; margin: 0; }}
    .grid-card {{ background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; border-radius: 12px; padding: 15px; min-height: 160px; margin-bottom: 10px; transition: 0.3s; }}
    .grid-card:hover {{ border: 1px solid #f59e0b; transform: translateY(-5px); }}
    .filter-box {{ background: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px; }}
    .stButton button {{ background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; width: 100% !important; }}
    .logout-btn button {{ background-color: #ff4b4b !important; color: white !important; }}
    </style>
""", unsafe_allow_html=True)

# 4. جلب البيانات (حصرياً من الروابط المقدمة مع حذف التكرار)
@st.cache_data(ttl=60)
def load_all_data():
    # رابط المشاريع (Sheet 1) ورابط المطورين (Sheet 2)
    u_projects = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_devs = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        df_p = pd.read_csv(u_projects).drop_duplicates(subset=['Project Name']).fillna("غير متوفر").astype(str)
        df_d = pd.read_csv(u_devs).drop_duplicates(subset=['Developer']).fillna("غير متوفر").astype(str)
        return df_p, df_d
    except:
        return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_all_data()

# 5. نظام الدخول
if not st.session_state.auth:
    st.markdown(f'<div class="oval-header"><h1 class="header-title">{T["title"]}</h1></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown("<div style='max-width:400px; margin:auto;'>", unsafe_allow_html=True)
        pwd = st.text_input("Password / كلمة المرور", type="password")
        if st.button("Login / دخول"):
            if pwd == "2026": st.session_state.auth = True; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- واجهة المستخدم بعد الدخول ---
top_c1, top_c2 = st.columns([1, 1])
with top_c1:
    if st.button(T['logout']): st.session_state.auth = False; st.rerun()
with top_c2:
    if st.button("🇺🇸 English / 🇪🇬 العربية"):
        st.session_state.lang = 'English' if st.session_state.lang == 'Arabic' else 'Arabic'
        st.rerun()

st.markdown(f'<div class="oval-header"><h1 class="header-title">{T["title"]}</h1></div>', unsafe_allow_html=True)
menu = option_menu(None, [T['tools'], T['projects'], T['devs']], icons=["tools", "building", "person-vcard"], orientation="horizontal")

# توزيع المساحة (70% يمين للعربي / 70% يسار للإنجليزي)
if st.session_state.lang == 'Arabic': main_col, _ = st.columns([0.7, 0.3])
else: _, main_col = st.columns([0.3, 0.7])

with main_col:
    # --- 🏗️ قسم المشاريع ---
    if menu == T['projects']:
        st.markdown(f"<h2 style='color:#f59e0b;'>{T['projects']}</h2>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
            f1, f2 = st.columns(2)
            with f1: f_search = st.text_input(T['search'])
            with f2: 
                area_opts = ["All/الكل"] + sorted(df_p['Area'].unique().tolist()) if not df_p.empty else []
                f_area = st.selectbox(T['filter_area'], area_opts)
            st.markdown("</div>", unsafe_allow_html=True)

        dff = df_p.copy()
        if f_search: dff = dff[dff['Project Name'].str.contains(f_search, case=False)]
        if f_area != "All/الكل": dff = dff[dff['Area'] == f_area]

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
                            <p style='font-size:12px; color:#888;'>📍 {row['Area']}</p>
                        </div>""", unsafe_allow_html=True)
                        with st.expander(T['details']):
                            st.write(f"👷 **الاستشاري:** {row.get('Consultant', 'غير متوفر')}")
                            st.info(f"**{T['pros']}:** {row.get('Project Features', 'جاري التحديث')}")
                            st.warning(f"**{T['cons']}:** {row.get('Project Flaws', 'جاري التحديث')}")

        # أزرار التنقل
        st.write("---")
        b1, b2, _ = st.columns([0.2, 0.2, 0.6])
        if b1.button(T['next']) and st.session_state.p_idx < total_p - 1: st.session_state.p_idx += 1; st.rerun()
        if b2.button(T['prev']) and st.session_state.p_idx > 0: st.session_state.p_idx -= 1; st.rerun()

    # --- 🏢 قسم المطورين ---
    elif menu == T['devs']:
        st.markdown(f"<h2 style='color:#f59e0b;'>{T['devs']}</h2>", unsafe_allow_html=True)
        f_dev_search = st.text_input("🔍 اسم الشركة / Company Name")
        dff_d = df_d.copy()
        if f_dev_search: dff_d = dff_d[dff_d['Developer'].str.contains(f_dev_search, case=False)]
        
        for i in range(0, len(dff_d), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(dff_d):
                    row = dff_d.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h4 style='color:#f59e0b;'>{row['Developer']}</h4><p>👤 {row['Owner']}</p></div>", unsafe_allow_html=True)
                        with st.expander("الملف التعريفي"): st.write(row['Detailed_Info'])

    # --- 🛠️ أدوات البروكر ---
    elif menu == T['tools']:
        st.markdown(f"<h2 style='color:#f59e0b;'>{T['tools']}</h2>", unsafe_allow_html=True)
        col_calc1, col_calc2 = st.columns(2)
        with col_calc1:
            st.subheader("💰 حاسبة الأقساط")
            u_p = st.number_input("سعر الوحدة", value=1000000, step=100000)
            u_y = st.slider("عدد السنوات", 1, 15, 8)
            st.metric("القسط الشهري", f"{u_p/(u_y*12):,.0f} ج.م")
        with col_calc2:
            st.subheader("📝 ملاحظات العميل")
            c_name = st.text_input("اسم العميل")
            c_note = st.text_area("ملاحظات المتابعة")
            if st.button("حفظ الملاحظة"): st.success("تم الحفظ (تجريبي)")
