import streamlit as st
import pandas as pd
import math
import feedparser
import urllib.parse
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (الدخول + الصفحات)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
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

# 4. التنسيق الجمالي (CSS المطور)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    body, [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0rem !important; }

    /* الهيدر */
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

    /* الكروت الرئيسية */
    .grid-card { 
        background: #111; border: 1px solid #222; border-right: 4px solid #f59e0b; 
        border-radius: 12px; padding: 15px; margin-bottom: 15px; min-height: 180px; 
    }
    
    /* خانة استلام فوري */
    .ready-sidebar-container { background: #0d0d0d; border: 1px solid #222; border-radius: 15px; padding: 12px; margin-bottom: 10px; }
    .ready-card { background: #161616; border-right: 3px solid #10b981; padding: 8px; border-radius: 8px; margin-bottom: 6px; }
    .ready-title { color: #f59e0b; font-size: 13px; font-weight: bold; }
    .ready-loc { color: #888; font-size: 10px; }

    /* تحسين شكل التابات والأدوات */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #111; border-radius: 10px; padding: 10px 20px; color: #fff; }
    .stTabs [aria-selected="true"] { background-color: #f59e0b !important; color: #000 !important; }
    </style>
""", unsafe_allow_html=True)

# 5. الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.2,1])
    with c2:
        if st.text_input("Passcode", type="password") == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# بناء الواجهة
now = datetime.now().strftime("%H:%M")
st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI PRO</div><div style="color:#aaa; font-size:12px;">⌚ {now}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], icons=["tools", "building", "person-vcard"], default_index=1, orientation="horizontal",
    styles={"container": {"background-color": "#0a0a0a"}, "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("").astype(str)
        d = pd.read_csv(u_d).fillna("").astype(str)
        p.columns = p.columns.str.strip(); d.columns = d.columns.str.strip()
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# توزيع المساحة 75/25
main_col, side_col = st.columns([0.75, 0.25])

# --- الجانب الأيمن: استلام فوري (8 عناصر + Pagination) ---
with side_col:
    st.markdown("<p style='color:#10b981; text-align:center; font-weight:bold; font-size:14px;'>🔑 استلام فوري</p>", unsafe_allow_html=True)
    ready_df = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
    
    r_limit = 8
    r_start = st.session_state.ready_idx * r_limit
    r_page = ready_df.iloc[r_start : r_start + r_limit]
    
    st.markdown("<div class='ready-sidebar-container'>", unsafe_allow_html=True)
    for _, row in r_page.iterrows():
        st.markdown(f"<div class='ready-card'><div class='ready-title'>{row.get('Project Name')}</div><div class='ready-loc'>📍 {row.get('Area')}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # أزرار تحكم الاستلام الفوري
    rc1, rc2 = st.columns(2)
    if rc1.button("السابق 🔼", key="r_prev"): st.session_state.ready_idx = max(0, st.session_state.ready_idx - 1); st.rerun()
    if rc2.button("التالي 🔽", key="r_next"): 
        if r_start + r_limit < len(ready_df): st.session_state.ready_idx += 1; st.rerun()

# --- الجانب الرئيسي ---
with main_col:
    if menu == "المشاريع":
        search = st.text_input("🔍 بحث في المشاريع...")
        filtered = df_p.copy()
        if search: filtered = filtered[filtered.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        
        p_page = filtered.iloc[st.session_state.p_idx*6 : (st.session_state.p_idx+1)*6]
        for i in range(0, len(p_page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(p_page):
                    r = p_page.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h3 style='color:#f59e0b; font-size:18px;'>{r.get('Project Name')}</h3><p style='font-size:13px;'>📍 {r.get('Area')}</p><p style='color:#aaa; font-size:12px;'>🏢 {r.get('Developer')}</p></div>", unsafe_allow_html=True)
                        with st.expander("التفاصيل الكاملة"):
                            st.write(f"🎨 **Master Plan:** {r.get('Master Plan')}")
                            st.write(f"⚙️ **Management:** {r.get('Management')}")
                            st.write(f"✨ **المميزات:** {r.get('Project Features')}")

    elif menu == "المطورين":
        d_page = df_d.iloc[st.session_state.d_idx*6 : (st.session_state.d_idx+1)*6]
        for i in range(0, len(d_page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(d_page):
                    r = d_page.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h3>{r.get('Developer')}</h3><p>👤 {r.get('Owner')}</p><p style='color:#10b981;'>🏗️ المشاريع: {r.get('Number of Projects')}</p></div>", unsafe_allow_html=True)
                        with st.expander("سابقة الأعمال"): st.write(r.get('Detailed_Info'))

    elif menu == "الأدوات":
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ صندوق أدوات البروكر الذكي</h2>", unsafe_allow_html=True)
        t1, t2, t3, t4, t5 = st.tabs(["🧮 حاسبة الأقساط", "💰 العائد والعمولة", "📐 تحويل المساحات", "🕵️ رادار البحث", "📝 المفكرة"])
        
        with t1:
            c1, c2 = st.columns(2)
            price = c1.number_input("سعر الوحدة", 1000000)
            down = c2.number_input("المقدم", price*0.1)
            years = st.slider("سنوات التقسيط", 1, 15, 8)
            st.metric("القسط الشهري", f"{(price-down)/(years*12):,.0f} ج.م")
            
        with t2:
            c1, c2 = st.columns(2)
            rent = c1.number_input("الإيجار المتوقع", 10000)
            comm_pct = c2.number_input("نسبة العمولة %", 1.5)
            st.info(f"📈 العائد السنوي (ROI): {(rent*12/price)*100:.2f}%")
            st.success(f"💵 عمولة البيع المتوقعة: {price*(comm_pct/100):,.0f} ج.م")

        with t3:
            sqm = st.number_input("المساحة بالمتر المربع", 100.0)
            st.write(f"📏 بالقدم المربع: {sqm*10.76:,.2f} sqft")
            st.write(f"📏 بالفدان: {sqm/4200:.4f} فدان")

        with t4:
            radar = st.text_input("🕵️ ابحث عن أي مشروع أو مطور في جوجل...")
            if radar: st.link_button(f"بحث عن {radar}", f"https://www.google.com/search?q={urllib.parse.quote(radar + ' عقارات مصر')}")

        with t5:
            st.text_area("📝 سجل ملاحظاتك السريعة هنا (لحفظها مؤقتاً أثناء المكالمة):")
            st.button("حفظ الملاحظات")

if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()
