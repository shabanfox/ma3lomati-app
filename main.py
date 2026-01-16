import streamlit as st
import pandas as pd
import feedparser
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 3. جلب الأخبار
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "جاري تحديث الأخبار العقارية..."
    except: return "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."

news_text = get_real_news()

# 4. التنسيق الجمالي (إعادة الشكل السابق المفضل)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container { padding-top: 0rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    
    /* الهيدر الذهبي */
    .luxury-header {
        background: rgba(15, 15, 15, 0.9); backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b; padding: 15px 30px;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; border-radius: 0 0 25px 25px; margin-bottom: 15px;
    }
    .logo-text { color: #f59e0b; font-weight: 900; font-size: 24px; }
    
    /* شريط الأخبار */
    .ticker-wrap { width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 10px; }
    .ticker { display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    /* الكروت البيضاء (الشكل السابق المفضل) */
    div.stButton > button {
        background-color: white !important;
        color: #111 !important;
        border: 1px solid #eee !important;
        border-radius: 15px !important;
        width: 100% !important;
        min-height: 240px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: flex-start !important;
        padding: 20px !important;
        transition: 0.3s !important;
        text-align: right !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        white-space: pre-wrap !important;
        line-height: 1.6 !important;
    }
    div.stButton > button:hover {
        border-color: #f59e0b !important;
        transform: translateY(-5px) !important;
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.2) !important;
    }

    /* صناديق التفاصيل */
    .detail-container { background:#111; padding:30px; border-radius:15px; border-right:5px solid #f59e0b; color:white; }
    .info-tag { background: #1a1a1a; padding: 10px; border-radius: 8px; border: 1px solid #333; margin-bottom: 10px; }
    .gold-label { color: #f59e0b; font-weight: bold; font-size: 0.9rem; display: block; }
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1.5,1])
    with c2:
        if st.text_input("Passcode", type="password") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# 6. تحميل البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("غير متوفر").astype(str)
        d = pd.read_csv(u_d).fillna("غير متوفر").astype(str)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# الهيدر
st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI PRO</div><div style="color:#aaa; font-size:12px;">📅 {datetime.now().strftime("%Y-%m-%d")}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], 
    default_index=1, orientation="horizontal",
    styles={"container": {"background-color": "#0a0a0a", "padding": "0"}, "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}}
)

main_col, side_col = st.columns([0.75, 0.25])

with side_col:
    st.markdown("<p style='color:#10b981; text-align:center; font-weight:bold;'>🔑 استلام فوري</p>", unsafe_allow_html=True)
    ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
    for _, r in ready.head(10).iterrows():
        st.markdown(f'<div style="background:#161616; padding:8px; border-radius:8px; margin-bottom:5px; border-right:3px solid #10b981; color:#aaa; font-size:12px;">{r.get("Project Name")}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🚪 خروج آمن", use_container_width=True):
        st.session_state.auth = False; st.rerun()

with main_col:
    if st.session_state.selected_item is not None:
        item = st.session_state.selected_item
        if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
        
        # تفاصيل المشروع
        if 'Project Name' in item:
            st.markdown(f"""
                <div class="detail-container">
                    <h1 style="color:#f59e0b; margin-bottom:0;">{item.get('Project Name')}</h1>
                    <p style="color:#aaa; margin-bottom:20px;">📍 {item.get('Area')}</p>
                    <div class="info-tag"><span class="gold-label">📍 الموقع بالتفصيل:</span>{item.get('Detailed Location')}</div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                        <div class="info-tag"><span class="gold-label">🏗️ المطور:</span>{item.get('Developer')}</div>
                        <div class="info-tag"><span class="gold-label">📐 مساحة المشروع:</span>{item.get('Project Area')}</div>
                        <div class="info-tag"><span class="gold-label">🏢 الإدارة:</span>{item.get('Management')}</div>
                        <div class="info-tag"><span class="gold-label">📋 الماستر بلان:</span>{item.get('Master Plan')}</div>
                    </div>
                    <div class="info-tag"><span class="gold-label">✨ المميزات:</span>{item.get('Project Features')}</div>
                </div>
            """, unsafe_allow_html=True)
        # تفاصيل المطور
        else:
            st.markdown(f"""
                <div class="detail-container">
                    <h1 style="color:#f59e0b;">{item.get('Developer')}</h1>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                        <div class="info-tag"><span class="gold-label">👑 المالك:</span>{item.get('Owner')}</div>
                        <div class="info-tag"><span class="gold-label">🏢 المشاريع:</span>{item.get('Number of Projects')}</div>
                        <div class="info-tag"><span class="gold-label">📍 النشاط:</span>{item.get('Main Region of Activity')}</div>
                        <div class="info-tag"><span class="gold-label">⭐ الفئة:</span>{item.get('Developer Category')}</div>
                    </div>
                    <div class="info-tag"><span class="gold-label">📖 سابقة الأعمال:</span>{item.get('Previous Projects')}</div>
                    <div class="info-tag"><span class="gold-label">ℹ️ معلومات:</span>{item.get('Detailed_Info')}</div>
                </div>
            """, unsafe_allow_html=True)

    elif menu == "المشاريع":
        c1, c2, c3 = st.columns(3)
        with c1: s_area = st.selectbox("المنطقة", ["الكل"] + sorted(df_p['Area'].unique().tolist()))
        with c2: s_dev = st.selectbox("المطور", ["الكل"] + sorted(df_p['Developer'].unique().tolist()))
        with c3: s_name = st.text_input("بحث بالاسم...")

        dff = df_p.copy()
        if s_area != "الكل": dff = dff[dff['Area'] == s_area]
        if s_dev != "الكل": dff = dff[dff['Developer'] == s_dev]
        if s_name: dff = dff[dff['Project Name'].str.contains(s_name, case=False)]

        limit = 6
        curr = dff.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]
        for i in range(0, len(curr), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(curr):
                    row = curr.iloc[i+j]
                    with cols[j]:
                        lbl = f"🏢 {row.get('Project Name')}\n📍 {row.get('Area')}\n🏗️ {row.get('Developer')}\n📐 {row.get('Project Area')}\n\n🔗 اضغط للتفاصيل والموقع"
                        if st.button(lbl, key=f"p_{i+j}"): st.session_state.selected_item = row; st.rerun()

    elif menu == "المطورين":
        s_d = st.text_input("🔍 ابحث عن مطور...")
        dff_d = df_d.copy()
        if s_d: dff_d = dff_d[dff_d.apply(lambda r: r.astype(str).str.contains(s_d, case=False).any(), axis=1)]
        
        for i in range(0, len(dff_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(dff_d):
                    row = dff_d.iloc[i+j]
                    with cols[j]:
                        lbl = f"🏗️ {row.get('Developer')}\n👑 {row.get('Owner')}\n📍 {row.get('Main Region of Activity')}\n⭐ فئة {row.get('Developer Category')}"
                        if st.button(lbl, key=f"d_{i+j}"): st.session_state.selected_item = row; st.rerun()

    elif menu == "الأدوات":
        st.info("حاسبة الأقساط والمساحات متاحة هنا.")
