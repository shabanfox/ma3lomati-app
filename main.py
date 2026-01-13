import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (اللغة والدخول)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = 'Arabic'

# نصوص الواجهة
ui = {
    'Arabic': {
        'title': "منصة معلوماتي العقارية", 'projects': "🏗️ المشاريع", 'devs': "🏢 المطورين", 
        'tools': "🛠️ الأدوات", 'logout': "🚪 خروج", 'search': "🔍 بحث...", 
        'filter_area': "📍 المنطقة", 'details': "🔎 التفاصيل", 'next': "التالي ⬅️", 'prev': "➡️ السابق", 
        'dir': "rtl", 'align': "right"
    },
    'English': {
        'title': "Ma3lomati Real Estate", 'projects': "🏗️ Projects", 'devs': "🏢 Developers", 
        'tools': "🛠️ Tools", 'logout': "🚪 Logout", 'search': "🔍 Search...", 
        'filter_area': "📍 Area", 'details': "🔎 Details", 'next': "Next ➡️", 'prev': "⬅️ Prev", 
        'dir': "ltr", 'align': "left"
    }
}
T = ui[st.session_state.lang]

# 3. التنسيق (CSS)
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
    .stButton button {{ background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; }}
    </style>
""", unsafe_allow_html=True)

# 4. جلب البيانات (حصرياً من روابطك)
@st.cache_data(ttl=60)
def load_data():
    u_projects = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_devs = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        df_p = pd.read_csv(u_projects).drop_duplicates(subset=['Project Name']).fillna("غير متوفر").astype(str)
        # حذف التكرار للمطورين بناءً على اسم المطور
        df_d = pd.read_csv(u_devs).drop_duplicates(subset=['Developer Name']).fillna("غير متوفر").astype(str)
        return df_p, df_d
    except:
        return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 5. نظام الدخول
if not st.session_state.auth:
    st.markdown(f'<div class="oval-header"><h1 class="header-title">{T["title"]}</h1></div>', unsafe_allow_html=True)
    pwd = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        if pwd == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- التحكم العلوي ---
c1, c2 = st.columns([1, 1])
with c1:
    if st.button(T['logout']): st.session_state.auth = False; st.rerun()
with c2:
    if st.button("🇺🇸 EN / 🇪🇬 AR"):
        st.session_state.lang = 'English' if st.session_state.lang == 'Arabic' else 'Arabic'
        st.rerun()

st.markdown(f'<div class="oval-header"><h1 class="header-title">{T["title"]}</h1></div>', unsafe_allow_html=True)
menu = option_menu(None, [T['tools'], T['projects'], T['devs']], icons=["tools", "building", "person-vcard"], orientation="horizontal")

# تقسيم المساحة 70%
if st.session_state.lang == 'Arabic': main_col, _ = st.columns([0.7, 0.3])
else: _, main_col = st.columns([0.3, 0.7])

with main_col:
    # --- 🏗️ قسم المشاريع ---
    if menu == T['projects']:
        st.markdown(f"<h2 style='color:#f59e0b;'>{T['projects']}</h2>", unsafe_allow_html=True)
        st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        with f1: s_p = st.text_input(T['search'])
        with f2: 
            as_ = ["الكل"] + sorted(df_p['Area'].unique().tolist()) if not df_p.empty else []
            sel_a = st.selectbox(T['filter_area'], as_)
        st.markdown("</div>", unsafe_allow_html=True)

        dff_p = df_p.copy()
        if s_p: dff_p = dff_p[dff_p['Project Name'].str.contains(s_p, case=False)]
        if sel_a != "الكل": dff_p = dff_p[dff_p['Area'] == sel_a]

        grid_limit = 9
        if 'idx_p' not in st.session_state: st.session_state.idx_p = 0
        total_p = math.ceil(len(dff_p) / grid_limit)
        curr_p = dff_p.iloc[st.session_state.idx_p*grid_limit : (st.session_state.idx_p+1)*grid_limit]

        for i in range(0, len(curr_p), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(curr_p):
                    row = curr_p.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h3 style='color:#f59e0b; font-size:16px;'>{row['Project Name']}</h3><p style='font-size:13px;'>🏢 {row['Developer']}</p><p style='color:#888;'>📍 {row['Area']}</p></div>", unsafe_allow_html=True)
                        with st.expander(T['details']):
                            st.write(f"👷 الاستشاري: {row.get('Consultant', 'N/A')}")
                            st.info(f"✅ المميزات: {row.get('Project Features', 'N/A')}")
                            st.warning(f"⚠️ العيوب: {row.get('Project Flaws', 'N/A')}")
        
        st.write("---")
        b1, b2, _ = st.columns([0.2, 0.2, 0.6])
        if b1.button(T['next']) and st.session_state.idx_p < total_p-1: st.session_state.idx_p += 1; st.rerun()
        if b2.button(T['prev']) and st.session_state.idx_p > 0: st.session_state.idx_p -= 1; st.rerun()

    # --- 🏢 قسم المطورين (المعدل حسب خاناتك) ---
    elif menu == T['devs']:
        st.markdown(f"<h2 style='color:#f59e0b;'>{T['devs']}</h2>", unsafe_allow_html=True)
        s_d = st.text_input("🔍 بحث عن مطور...")
        
        dff_d = df_d.copy()
        if s_d: dff_d = dff_d[dff_d['Developer Name'].str.contains(s_d, case=False)]

        for i in range(0, len(dff_d), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(dff_d):
                    row = dff_d.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h4 style='color:#f59e0b;'>{row['Developer Name']}</h4><p>👤 المالك: {row['Owner']}</p></div>", unsafe_allow_html=True)
                        with st.expander("📖 تفاصيل المطور"):
                            st.write(f"📝 **عن الشركة:** {row.get('Detailed_Info', 'N/A')}")
                            st.divider()
                            st.markdown("⏳ **History**")
                            st.info(row.get('History', 'جاري التحديث...'))
                            st.divider()
                            st.markdown("🏗️ **Previous Work**")
                            st.success(row.get('Previous Work', 'جاري التحديث...'))

    # --- 🛠️ أدوات البروكر ---
    elif menu == T['tools']:
        st.markdown(f"<h2 style='color:#f59e0b;'>{T['tools']}</h2>", unsafe_allow_html=True)
        calc1, calc2 = st.columns(2)
        with calc1:
            price = st.number_input("سعر الوحدة", 1000000)
            years = st.slider("السنوات", 1, 15, 8)
            st.metric("القسط الشهري", f"{price/(years*12):,.0f} ج.م")
