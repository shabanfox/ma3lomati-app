import streamlit as st
import pandas as pd
import feedparser
import random
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (Session State)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0  # مؤشر الصفحات
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 3. جلب الأخبار
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        return "  •  ".join([item.title for item in feed.entries[:10]])
    except: return "جاري تحديث الأخبار العقارية..."

# 4. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    
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
        min-height: 200px !important; text-align: right !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        font-weight: bold !important; line-height: 1.6 !important;
    }
    div.stButton > button[key="logout_btn"] { background-color: #dc2626 !important; color: white !important; }
    .ticker-wrap { width: 100%; overflow: hidden; border-bottom: 1px solid #222; margin-bottom: 10px; }
    .ticker { display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; white-space: nowrap; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1.5,1])
    with c2:
        if st.text_input("Passcode", type="password") == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# الهيدر وزر الخروج
h_col1, h_col2 = st.columns([0.88, 0.12])
with h_col1:
    st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI PRO</div><div style="color:#aaa; font-size:12px;">📅 {datetime.now().strftime("%Y-%m-%d")}</div></div>', unsafe_allow_html=True)
with h_col2:
    st.markdown("<div style='margin-top:15px;'>", unsafe_allow_html=True)
    if st.button("🚪 خروج", key="logout_btn"): st.session_state.auth = False; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f'<div class="ticker-wrap"><div class="ticker">{get_real_news()}</div></div>', unsafe_allow_html=True)

# جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], icons=["tools", "building", "person"], default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

main_col, side_col = st.columns([0.75, 0.25])

with side_col:
    st.markdown("<p style='color:#10b981; font-weight:bold; text-align:center;'>🔑 استلام فوري</p>", unsafe_allow_html=True)
    ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(10)
    for _, r in ready.iterrows():
        st.markdown(f'<div style="background:#111; border-right:3px solid #10b981; padding:8px; margin-bottom:5px; border-radius:5px;"><small>{r.get("Project Name")}</small></div>', unsafe_allow_html=True)

with main_col:
    if st.session_state.selected_item is not None:
        if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
        item = st.session_state.selected_item
        st.markdown(f"<div style='background:#111; padding:20px; border-radius:15px; border-right:5px solid #f59e0b;'><h2>{item.get('Project Name', item.get('Developer'))}</h2><hr>{item.get('Project Features', item.get('Detailed_Info', 'لا توجد تفاصيل'))}</div>", unsafe_allow_html=True)

    elif menu == "المشاريع":
        search = st.text_input("🔍 ابحث هنا...")
        dff = df_p.copy()
        if search: 
            dff = dff[dff.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
            st.session_state.p_idx = 0 # ريست لالصفحات عند البحث
        
        # حسبة الـ 6 كروت
        limit = 6
        start = st.session_state.p_idx * limit
        end = start + limit
        batch = dff.iloc[start:end]

        for i in range(0, len(batch), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(batch):
                    row = batch.iloc[i+j]
                    btn_text = f"🏢 {row.get('Project Name')}\n📍 {row.get('Area')}\n🏗️ {row.get('Developer')}\n💰 عرض التفاصيل"
                    if cols[j].button(btn_text, key=f"card_p_{start+i+j}"):
                        st.session_state.selected_item = row; st.rerun()

        # أزرار التنقل (التالي والسابق)
        st.markdown("---")
        c1, c2, c3 = st.columns([1,2,1])
        if st.session_state.p_idx > 0:
            if c1.button("⬅️ السابق"): st.session_state.p_idx -= 1; st.rerun()
        if end < len(dff):
            if c3.button("التالي ➡️"): st.session_state.p_idx += 1; st.rerun()

    elif menu == "المطورين":
        dff_d = df_d.copy()
        for i in range(0, len(dff_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(dff_d):
                    row = dff_d.iloc[i+j]
                    # جلب الفئة بذكاء لضمان عدم ظهور "قيد التحديث"
                    cat = row.get('Developer Category', row.get('Category', 'A'))
                    btn_text = f"🏗️ {row.get('Developer')}\n⭐ الفئة: {cat}\n👤 المالك: {row.get('Owner')}"
                    if cols[j].button(btn_text, key=f"card_d_{i+j}"):
                        st.session_state.selected_item = row; st.rerun()

    elif menu == "الأدوات":
        st.info("🛠️ حاسبة الأقساط والمساحات")
        p = st.number_input("السعر", 1000000); y = st.slider("السنين", 1, 15, 7)
        st.metric("القسط الشهري", f"{p/(y*12):,.0f}")
