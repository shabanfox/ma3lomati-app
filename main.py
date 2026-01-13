import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (اللغة والدخول)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = 'Arabic'

# نصوص الواجهة
ui = {
    'Arabic': {
        'title': "منصة معلوماتي العقارية", 'projects': "🏗️ المشاريع", 'devs': "🏢 المطورين", 
        'tools': "🛠️ أدوات البروكر", 'logout': "🚪 خروج", 'search': "🔍 بحث بالاسم...", 
        'filter_area': "📍 تصفية بالمنطقة", 'filter_dev': "🏢 المطور العقاري",
        'details': "🔎 تفاصيل المشروع", 'pros': "✅ مميزات المشروع", 'cons': "⚠️ عيوب المشروع",
        'next': "التالي ⬅️", 'prev': "➡️ السابق", 'dir': "rtl", 'align': "right"
    },
    'English': {
        'title': "Ma3lomati Real Estate", 'projects': "🏗️ Projects", 'devs': "🏢 Developers", 
        'tools': "🛠️ Broker Tools", 'logout': "🚪 Logout", 'search': "🔍 Search Name...", 
        'filter_area': "📍 Filter by Area", 'filter_dev': "🏢 Developer",
        'details': "🔎 Project Details", 'pros': "✅ Project Features", 'cons': "⚠️ Project Flaws",
        'next': "Next ➡️", 'prev': "⬅️ Prev", 'dir': "ltr", 'align': "left"
    }
}
T = ui[st.session_state.lang]

# 3. التنسيق (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; margin-top: -10px; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ 
        background-color: #050505; direction: {T['dir']} !important; 
        text-align: {T['align']} !important; font-family: 'Cairo', sans-serif; 
    }}
    .logout-btn button {{ background-color: #ff4b4b !important; color: white !important; border-radius: 10px; }}
    .oval-header {{ background-color: #000; border: 3px solid #f59e0b; border-radius: 50px; padding: 10px 30px; width: fit-content; margin: 10px auto 20px auto; text-align: center; box-shadow: 0px 4px 15px rgba(245, 158, 11, 0.4); }}
    .header-title {{ color: #f59e0b; font-weight: 900; font-size: 26px !important; margin: 0; }}
    .right-header {{ color: #f59e0b; font-weight: 900; border-right: 8px solid #f59e0b; padding-right: 15px; margin-bottom: 20px; font-size: 22px; }}
    .grid-card {{ background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; border-radius: 12px; padding: 15px; height: 165px; margin-bottom: 10px; transition: 0.3s; }}
    .grid-card:hover {{ border: 1px solid #f59e0b; transform: translateY(-5px); }}
    .filter-box {{ background: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px; }}
    .stButton button {{ background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; width: 100% !important; }}
    </style>
""", unsafe_allow_html=True)

# 4. نظام الدخول
if not st.session_state.auth:
    st.markdown(f'<div class="oval-header"><h1 class="header-title">{T["title"]}</h1></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown("<div style='max-width:400px; margin:auto;'>", unsafe_allow_html=True)
        pwd = st.text_input("Password / كلمة المرور", type="password")
        if st.button("Login / دخول"):
            if pwd == "2026": st.session_state.auth = True; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- واجهة الموقع الرئيسية ---

# الهيدر العلوي (خروج + تبديل لغة)
c1, c2 = st.columns([1, 1])
with c1:
    if st.button(T['logout']): st.session_state.auth = False; st.rerun()
with c2:
    lang_btn = "🇺🇸 English" if st.session_state.lang == 'Arabic' else "🇪🇬 العربية"
    if st.button(lang_label := lang_btn):
        st.session_state.lang = 'English' if st.session_state.lang == 'Arabic' else 'Arabic'
        st.rerun()

st.markdown(f'<div class="oval-header"><h1 class="header-title">{T["title"]}</h1></div>', unsafe_allow_html=True)

# المنيو الرئيسي
menu = option_menu(None, [T['tools'], T['projects'], T['devs']], 
                  icons=["tools", "building", "person-vcard"], 
                  orientation="horizontal")

# 5. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    # الرابط الأول للمشاريع والثاني للمطورين (يتم تحويلهم لـ CSV داخلياً)
    u1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u2 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        df_p = pd.read_csv(u1).fillna("غير متوفر").astype(str)
        df_d = pd.read_csv(u2).fillna("غير متوفر").astype(str)
        return df_p, df_d
    except: return pd.DataFrame(), pd.DataFrame()

df_projects, df_developers = load_data()

# توزيع المساحة 70% يمين أو يسار حسب اللغة
if st.session_state.lang == 'Arabic':
    main_col, empty_col = st.columns([0.7, 0.3])
else:
    empty_col, main_col = st.columns([0.3, 0.7])

with main_col:
    # --- قسم المشاريع ---
    if menu == T['projects']:
        st.markdown(f"<h1 class='right-header'>{T['projects']}</h1>", unsafe_allow_html=True)
        
        # الفلاتر القوية
        st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
        f_c1, f_c2 = st.columns(2)
        with f_c1: search = st.text_input(T['search'])
        with f_c2: 
            area_list = ["الكل / All"] + sorted(df_projects['Area'].unique().tolist()) if 'Area' in df_projects.columns else []
            sel_area = st.selectbox(T['filter_area'], area_list)
        
        f_c3, f_c4 = st.columns(2)
        with f_c3:
            dev_list = ["الكل / All"] + sorted(df_projects['Developer'].unique().tolist()) if 'Developer' in df_projects.columns else []
            sel_dev = st.selectbox(T['filter_dev'], dev_list)
        with f_c4:
            cons_list = ["الكل / All"] + sorted(df_projects['Consultant'].unique().tolist()) if 'Consultant' in df_projects.columns else []
            sel_cons = st.selectbox("👷 الاستشاري", cons_list)
        st.markdown("</div>", unsafe_allow_html=True)

        # منطق التصفية
        dff = df_projects.copy()
        if search: dff = dff[dff.apply(lambda r: search.lower() in r.astype(str).str.lower().values, axis=1)]
        if sel_area != "الكل / All": dff = dff[dff['Area'] == sel_area]
        if sel_dev != "الكل / All": dff = dff[dff['Developer'] == sel_dev]
        if sel_cons != "الكل / All": dff = dff[dff['Consultant'] == sel_cons]

        # عرض الشبكة
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
                            <h3 style='color:#f59e0b; font-size:16px;'>{row.get('Project Name', 'N/A')}</h3>
                            <p style='font-size:13px;'>🏢 {row.get('Developer', 'N/A')}</p>
                            <p style='font-size:12px; color:#888;'>📍 {row.get('Area', 'N/A')}</p>
                        </div>""", unsafe_allow_html=True)
                        with st.expander(T['details']):
                            st.info(f"👷 {row.get('Consultant', 'غير متوفر')}")
                            st.success(f"**{T['pros']}:**\n{row.get('Project Features', 'جاري التحديث...')}")
                            st.warning(f"**{T['cons']}:**\n{row.get('Project Flaws', 'جاري التحديث...')}")

        # التنقل
        st.divider()
        b1, b2, _ = st.columns([0.2, 0.2, 0.6])
        if b1.button(T['next']) and st.session_state.p_idx < total_p - 1: st.session_state.p_idx += 1; st.rerun()
        if b2.button(T['prev']) and st.session_state.p_idx > 0: st.session_state.p_idx -= 1; st.rerun()

    # --- قسم المطورين ---
    elif menu == T['devs']:
        st.markdown(f"<h1 class='right-header'>{T['devs']}</h1>", unsafe_allow_html=True)
        # فلاتر المطورين
        d_name = st.text_input("🔍 اسم المطور / Developer Name")
        dff_d = df_developers.copy()
        if d_name: dff_d = dff_d[dff_d['Developer'].str.contains(d_name, case=False)]
        
        for i in range(0, len(dff_d.head(9)), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(dff_d):
                    row = dff_d.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h4 style='color:#f59e0b;'>{row.get('Developer', 'N/A')}</h4><p>👤 {row.get('Owner', 'N/A')}</p></div>", unsafe_allow_html=True)
                        with st.expander("الملف التعريفي"): st.write(row.get('Detailed_Info', ''))

    # --- أدوات البروكر ---
    elif menu == T['tools']:
        st.markdown(f"<h1 class='right-header'>{T['tools']}</h1>", unsafe_allow_html=True)
        t_c1, t_c2 = st.columns(2)
        with t_c1:
            st.subheader("💰 حاسبة القسط")
            price = st.number_input("السعر", value=1000000)
            years = st.slider("السنين", 1, 15, 8)
            st.metric("القسط الشهري", f"{price/(years*12):,.0f} ج.م")
        with t_c2:
            st.subheader("📝 ملاحظات سريعة")
            st.text_area("سجل بيانات عميلك هنا...")
            st.button("حفظ مؤقت")
