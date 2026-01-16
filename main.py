import streamlit as st
import pandas as pd
import feedparser
import random
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 3. جلب الأخبار
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        return "  •  ".join([item.title for item in feed.entries[:10]])
    except: return "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."

# 4. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    
    /* ستايل الفلاتر */
    .stSelectbox label, .stTextInput label { color: #f59e0b !important; font-weight: bold !important; }
    div[data-baseweb="select"] { background-color: #111 !important; border-radius: 10px !important; }

    .luxury-header {
        background: rgba(15, 15, 15, 0.9); backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b; padding: 15px 30px;
        display: flex; justify-content: space-between; align-items: center;
        border-radius: 0 0 25px 25px; margin-bottom: 15px;
    }
    .logo-text { color: #f59e0b; font-weight: 900; font-size: 24px; }
    
    div.stButton > button[key*="card_"] {
        background-color: white !important; color: #111 !important;
        border-radius: 15px !important; width: 100% !important;
        min-height: 220px !important; text-align: right !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        font-weight: bold !important; line-height: 1.6 !important;
    }
    div.stButton > button[key*="card_"]:hover { border-color: #f59e0b !important; transform: translateY(-5px) !important; }
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1.5,1])
    with c2:
        if st.text_input("Passcode", type="password") == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# الهيدر
st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI PRO</div><div style="color:#aaa; font-size:12px;">📅 {datetime.now().strftime("%Y-%m-%d")}</div></div>', unsafe_allow_html=True)

# جلب البيانات
@st.cache_data(ttl=60)
def load_all_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---"); d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip(); d.columns = d.columns.str.strip()
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_all_data()

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

main_col, side_col = st.columns([0.75, 0.25])

with side_col:
    st.markdown("<p style='color:#10b981; text-align:center; font-weight:bold;'>🔑 استلام فوري</p>", unsafe_allow_html=True)
    ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(10)
    for _, row in ready.iterrows():
        st.markdown(f'<div style="background:#161616; border-right:3px solid #10b981; padding:8px; border-radius:8px; margin-bottom:5px; color:#ddd; font-size:12px;">{row.get("Project Name")}</div>', unsafe_allow_html=True)

with main_col:
    if st.session_state.selected_item is not None:
        if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
        item = st.session_state.selected_item
        st.markdown(f"<div style='background:#111; padding:30px; border-radius:15px; border-right:5px solid #f59e0b; color:white;'><h1>{item.get('Project Name', item.get('Developer'))}</h1><hr>{item.get('Project Features', item.get('Detailed_Info', 'لا توجد تفاصيل'))}</div>", unsafe_allow_html=True)

    elif menu == "المشاريع":
        # صف الفلاتر الجميل
        f1, f2, f3 = st.columns(3)
        search_txt = f1.text_input("🔍 بحث بالاسم", "")
        area_list = ["الكل"] + sorted(df_p['Area'].unique().tolist())
        area_filter = f2.selectbox("📍 تصفية بالمنطقة", area_list)
        dev_list = ["الكل"] + sorted(df_p['Developer'].unique().tolist())
        dev_filter = f3.selectbox("🏗️ تصفية بالمطور", dev_list)

        dff = df_p.copy()
        if search_txt: dff = dff[dff.apply(lambda r: r.astype(str).str.contains(search_txt, case=False).any(), axis=1)]
        if area_filter != "الكل": dff = dff[dff['Area'] == area_filter]
        if dev_filter != "الكل": dff = dff[dff['Developer'] == dev_filter]

        limit = 6
        start = st.session_state.p_idx * limit
        curr_page = dff.iloc[start:start+limit]

        for i in range(0, len(curr_page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(curr_page):
                    row = curr_page.iloc[i+j]
                    label = f"🏢 {row.get('Project Name')}\n📍 {row.get('Area')}\n🏗️ {row.get('Developer')}\n💰 عرض التفاصيل"
                    if cols[j].button(label, key=f"card_p_{start+i+j}"): st.session_state.selected_item = row; st.rerun()
        
        # أزرار التنقل
        st.markdown("---")
        c1, _, c3 = st.columns([1,2,1])
        if st.session_state.p_idx > 0:
            if c1.button("⬅️ السابق", key="p_prev"): st.session_state.p_idx -= 1; st.rerun()
        if start + limit < len(dff):
            if c3.button("التالي ➡️", key="p_next"): st.session_state.p_idx += 1; st.rerun()

    elif menu == "المطورين":
        f1_d, f2_d = st.columns(2)
        search_d = f1_d.text_input("🔍 بحث عن مطور", "")
        cat_list = ["الكل"] + sorted(df_d['Developer Category'].unique().tolist())
        cat_filter = f2_d.selectbox("⭐ تصفية بالفئة", cat_list)

        dff_d = df_d.copy()
        if search_d: dff_d = dff_d[dff_d.apply(lambda r: r.astype(str).str.contains(search_d, case=False).any(), axis=1)]
        if cat_filter != "الكل": dff_d = dff_d[dff_d['Developer Category'] == cat_filter]

        limit_d = 6
        start_d = st.session_state.d_idx * limit_d
        curr_page_d = dff_d.iloc[start_d:start_d+limit_d]

        for i in range(0, len(curr_page_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(curr_page_d):
                    row = curr_page_d.iloc[i+j]
                    label = f"🏗️ {row.get('Developer')}\n⭐ الفئة: {row.get('Developer Category')}\n👤 المالك: {row.get('Owner')}\n📖 سابقة الأعمال"
                    if cols[j].button(label, key=f"card_d_{start_d+i+j}"): st.session_state.selected_item = row; st.rerun()

        st.markdown("---")
        dc1, _, dc3 = st.columns([1,2,1])
        if st.session_state.d_idx > 0:
            if dc1.button("⬅️ السابق", key="d_prev"): st.session_state.d_idx -= 1; st.rerun()
        if start_d + limit_d < len(dff_d):
            if dc3.button("التالي ➡️", key="d_next"): st.session_state.d_idx += 1; st.rerun()

    elif menu == "الأدوات":
        st.info("🛠️ حاسبة الأقساط والمساحات")
        price = st.number_input("السعر", 1000000); y = st.slider("السنين", 1, 15, 8)
        st.metric("القسط الشهري", f"{price/(y*12):,.0f}")

if st.button("🚪 خروج آمن", key="logout_btn"): st.session_state.auth = False; st.rerun()
