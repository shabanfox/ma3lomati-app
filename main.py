import streamlit as st
import pandas as pd
import math
import feedparser
import urllib.parse
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة حالة الجلسة (لضمان عمل الأزرار بشكل صحيح)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'ready_idx' not in st.session_state: st.session_state.ready_idx = 0

# 3. جلب الأخبار
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        return "  •  ".join([item.title for item in feed.entries[:10]])
    except: return "سوق العقارات المصري 2026: متابعة مستمرة."

news_text = get_real_news()

# 4. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    body, [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0rem !important; }
    .luxury-header { background: rgba(15,15,15,0.9); border-bottom: 2px solid #f59e0b; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; border-radius: 0 0 25px 25px; margin-bottom: 15px; }
    .logo-text { color: #f59e0b; font-weight: 900; font-size: 24px; }
    .ticker-wrap { width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 10px; }
    .ticker { display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .grid-card { background: #111; border: 1px solid #222; border-right: 4px solid #f59e0b; border-radius: 12px; padding: 15px; margin-bottom: 15px; min-height: 180px; }
    .ready-sidebar-container { background: #0d0d0d; border: 1px solid #222; border-radius: 15px; padding: 12px; margin-bottom: 10px; }
    .ready-card { background: #161616; border-right: 3px solid #10b981; padding: 8px; border-radius: 8px; margin-bottom: 6px; }
    .ready-title { color: #f59e0b; font-size: 13px; font-weight: bold; }
    .ready-loc { color: #888; font-size: 10px; }
    </style>
""", unsafe_allow_html=True)

# 5. نظام الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.2,1])
    with c2:
        if st.text_input("Passcode", type="password") == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# بناء الهيدر
now = datetime.now().strftime("%H:%M")
st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI PRO</div><div style="color:#aaa; font-size:12px;">⌚ {now}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], icons=["tools", "building", "person-vcard"], default_index=1, orientation="horizontal",
    styles={"container": {"background-color": "#0a0a0a"}, "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# 6. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("").astype(str)
        d = pd.read_csv(u_d).fillna("").astype(str)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# توزيع المساحة 75% أساسي و 25% جانبي
main_col, side_col = st.columns([0.75, 0.25])

# --- الجانب الأيمن: استلام فوري (8 عناصر + تحكم) ---
with side_col:
    st.markdown("<p style='color:#10b981; text-align:center; font-weight:bold; font-size:14px;'>🔑 استلام فوري</p>", unsafe_allow_html=True)
    ready_items = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
    
    r_start = st.session_state.ready_idx * 8
    r_page = ready_items.iloc[r_start : r_start + 8]
    
    st.markdown("<div class='ready-sidebar-container'>", unsafe_allow_html=True)
    for _, row in r_page.iterrows():
        st.markdown(f"<div class='ready-card'><div class='ready-title'>{row.get('Project Name')}</div><div class='ready-loc'>📍 {row.get('Area')}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    rc1, rc2 = st.columns(2)
    if rc1.button("السابق 🔼"): st.session_state.ready_idx = max(0, st.session_state.ready_idx - 1); st.rerun()
    if rc2.button("التالي 🔽"): 
        if r_start + 8 < len(ready_items): st.session_state.ready_idx += 1; st.rerun()

# --- الجانب الرئيسي ---
with main_col:
    if menu == "المشاريع":
        search = st.text_input("🔍 ابحث في المشاريع...")
        filtered = df_p.copy()
        if search: filtered = filtered[filtered.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        
        p_page = filtered.iloc[st.session_state.p_idx*6 : (st.session_state.p_idx+1)*6]
        for i in range(0, len(p_page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(p_page):
                    r = p_page.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h3 style='color:#f59e0b; font-size:18px;'>{r.get('Project Name')}</h3><p>📍 {r.get('Area')}</p></div>", unsafe_allow_html=True)
                        with st.expander("التفاصيل الكاملة"):
                            st.write(f"🎨 **Master Plan:** {r.get('Master Plan')}")
                            st.write(f"⚙️ **Management:** {r.get('Management')}")
                            st.write(f"✨ **المميزات:** {r.get('Project Features')}")

    elif menu == "المطورين":
        for i in range(0, len(df_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(df_d):
                    r = df_d.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h3>{r.get('Developer')}</h3><p>👤 {r.get('Owner')}</p></div>", unsafe_allow_html=True)
                        with st.expander("سابقة الأعمال"): 
                            st.write(f"📜 **عن الشركة:** {r.get('Detailed_Info')}")
                            st.write(f"🏗️ **المشاريع السابقة:** {r.get('Previous_Projects')}")

    elif menu == "الأدوات":
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ الأدوات</h2>", unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["🧮 القسط والعمولة", "📐 المساحات", "📝 نوت"])
        with t1:
            price = st.number_input("السعر", 1000000)
            years = st.slider("السنين", 1, 15, 8)
            st.metric("القسط الشهري", f"{price/(years*12):,.0f} ج.م")
            st.success(f"💰 عمولتك (1.5%): {price*0.015:,.0f} ج.م")
        with t2:
            sqm = st.number_input("مساحة متر", 100.0)
            st.write(f"📏 قدم مربع: {sqm*10.76:,.2f}")
        with t3:
            st.text_area("سجل ملاحظات العميل...")
