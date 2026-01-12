import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO - النسخة الشاملة", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; }
    .main-header { background: linear-gradient(90deg, #111 0%, #000 100%); padding: 15px; border-radius: 0 0 15px 15px; border-right: 12px solid #f59e0b; text-align: center; margin-bottom: 25px; }
    .header-title { font-weight: 900; font-size: 30px !important; color: #f59e0b; margin: 0; }
    .pro-card { background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; border-radius: 12px; padding: 20px; text-align: center; height: 100%; min-height: 220px; }
    .detail-box { background: #0d0d0d; border-right: 6px solid #f59e0b; border-radius: 12px; padding: 25px; color: #eee; border: 1px solid #222; animation: fadeIn 0.4s; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    .card-title { color: #f59e0b; font-size: 19px !important; font-weight: 900; }
    .stButton button { background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; border-radius: 8px; font-weight: bold; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# 3. وظيفة جلب ودمج البيانات من الرابطين
@st.cache_data(ttl=60)
def load_combined_data():
    urls = [
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv",
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    ]
    all_dfs = []
    for url in urls:
        try:
            temp_df = pd.read_csv(url)
            temp_df.columns = [str(c).strip() for c in temp_df.columns]
            all_dfs.append(temp_df)
        except: continue
    if not all_dfs: return pd.DataFrame()
    combined = pd.concat(all_dfs, ignore_index=True)
    return combined.fillna("غير متوفر").astype(str)

df = load_combined_data()

# 4. إدارة الحالة
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'd_page' not in st.session_state: st.session_state.d_page = 0
if 'active_proj' not in st.session_state: st.session_state.active_proj = None
if 'active_dev' not in st.session_state: st.session_state.active_dev = None

# الهيدر والمنيو
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي العقارية PRO</h1></div>', unsafe_allow_html=True)
selected = option_menu(None, ["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
                       icons=["tools", "building", "person-badge"], orientation="horizontal",
                       styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}})

# --- 🏗️ قسم المشاريع ---
if selected == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
    search_p = st.text_input("🔍 ابحث في المشاريع...")
    dff = df.copy()
    if search_p: dff = dff[dff['Project Name'].str.contains(search_p, case=False) | dff['Developer'].str.contains(search_p, case=False)]
    
    items_p = 9
    total_p = max(1, math.ceil(len(dff) / items_p))
    curr_p = dff.iloc[st.session_state.p_page * items_p : (st.session_state.p_page + 1) * items_p].reset_index()

    for i in range(0, len(curr_p), 3):
        row_ids = curr_p['index'].iloc[i:i+3].tolist()
        if st.session_state.active_proj in row_ids:
            p_data = df.loc[st.session_state.active_proj]
            st.markdown("---")
            c1, c2 = st.columns([0.3, 0.7])
            with c1:
                st.markdown(f"<div class='pro-card'><div class='card-title'>{p_data['Project Name']}</div><p>{p_data['Developer']}</p></div>", unsafe_allow_html=True)
                if st.button("⬅️ إغلاق", key=f"cp_{p_data.name}"): st.session_state.active_proj = None; st.rerun()
            with c2:
                st.markdown(f"<div class='detail-box'><h3>🏗️ {p_data['Project Name']}</h3><p>📍 {p_data['Area']} | 📏 {p_data['Size (Acres)']} فدان</p><p><b>👷 الاستشاري:</b> {p_data['Consultant']}</p><p><b>⭐ المميزات:</b> {p_data['Competitive Advantage']}</p></div>", unsafe_allow_html=True)
            st.markdown("---")
        else:
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(curr_p):
                    item = curr_p.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='pro-card'><div class='card-title'>{item['Project Name']}</div><p>{item['Developer']}</p></div>", unsafe_allow_html=True)
                        if st.button("🔍 التفاصيل", key=f"bp_{item['index']}"): st.session_state.active_proj = item['index']; st.rerun()

# --- 🏢 قسم المطورين (الإصلاح هنا) ---
elif selected == "🏢 المطورين":
    st.markdown("<h2 style='color:#f59e0b;'>🏢 دليل المطورين</h2>", unsafe_allow_html=True)
    # تجميع المطورين وإزالة التكرار مع الحفاظ على أهم البيانات
    devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
    
    search_d = st.text_input("🔍 ابحث عن مطور...")
    if search_d: devs = devs[devs['Developer'].str.contains(search_d, case=False)]

    items_d = 9
    total_d = max(1, math.ceil(len(devs) / items_d))
    curr_d = devs.iloc[st.session_state.d_page * items_d : (st.session_state.d_page + 1) * items_d].reset_index()

    for i in range(0, len(curr_d), 3):
        row_indices = curr_d['index'].iloc[i:i+3].tolist()
        if st.session_state.active_dev in row_indices:
            d_data = devs.iloc[st.session_state.active_dev]
            st.markdown("---")
            c1, c2 = st.columns([0.3, 0.7])
            with c1:
                st.markdown(f"<div class='pro-card'><div class='card-title'>{d_data['Developer']}</div><p>{d_data['Owner']}</p></div>", unsafe_allow_html=True)
                if st.button("⬅️ إغلاق الملف", key=f"cd_{d_data.name}"): st.session_state.active_dev = None; st.rerun()
            with c2:
                st.markdown(f"""<div class='detail-box'>
                    <h3 style='color:#f59e0b;'>🏢 ملف شركة {d_data['Developer']}</h3>
                    <p><b>👤 رئيس مجلس الإدارة:</b> {d_data['Owner']}</p>
                    <p><b>📜 نبذة تاريخية:</b><br>{d_data['Detailed_Info']}</p>
                </div>""", unsafe_allow_html=True)
            st.markdown("---")
        else:
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(curr_d):
                    item = curr_d.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='pro-card'><div class='card-title'>{item['Developer']}</div><p style='color:#888;'>{item['Owner']}</p></div>", unsafe_allow_html=True)
                        if st.button("🔍 عرض الملف", key=f"bd_{item['index']}"): st.session_state.active_dev = item['index']; st.rerun()

    # أزرار التنقل للمطورين
    st.write("---")
    d1, d2, d3 = st.columns([1, 2, 1])
    if d3.button("التالي ⬅️", key="dn") and st.session_state.d_page < total_d-1: st.session_state.d_page += 1; st.rerun()
    d2.markdown(f"<center>صفحة {st.session_state.d_page+1} من {total_d}</center>", unsafe_allow_html=True)
    if d1.button("➡️ السابق", key="dp") and st.session_state.d_page > 0: st.session_state.d_page -= 1; st.rerun()

# --- 🛠️ قسم الأدوات ---
elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b;'>🛠️ الأدوات الذكية</h2>")
    st.info("حاسبة الأقساط والمفكرة تعمل بكفاءة.")
