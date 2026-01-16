import streamlit as st
import pandas as pd
import math
import feedparser
import urllib.parse
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0

# 3. جلب الأخبار (RSS)
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "جاري تحديث الأخبار العقارية..."
    except: return "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."

news_text = get_real_news()

# 4. التنسيق الجمالي (CSS المطور)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    /* الهيدر */
    .luxury-header {{
        background: rgba(15, 15, 15, 0.9); backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b; padding: 15px 30px;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; border-radius: 0 0 25px 25px; margin-bottom: 15px;
    }}
    .logo-text {{ color: #f59e0b; font-weight: 900; font-size: 24px; text-shadow: 0 0 8px rgba(245, 158, 11, 0.4); }}
    
    /* شريط الأخبار */
    .ticker-wrap {{ width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 10px; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* كروت الشبكة الرئيسية */
    .grid-card {{ 
        background: #111; border: 1px solid #222; 
        border-right: 4px solid #f59e0b; border-radius: 12px; padding: 15px; margin-bottom: 15px;
        min-height: 180px; transition: 0.3s;
    }}
    .grid-card:hover {{ border-color: #f59e0b; background: #161616; }}

    /* --- تنسيق خانة استلام فوري الجديد --- */
    .ready-sidebar-container {{
        background: #0d0d0d; border: 1px solid #222; border-radius: 15px; padding: 12px;
        max-height: 80vh; overflow-y: auto; border-top: 3px solid #10b981;
    }}
    .ready-card {{
        background: #161616; border-right: 3px solid #10b981; padding: 10px; 
        border-radius: 8px; margin-bottom: 8px; transition: 0.2s;
    }}
    .ready-card:hover {{ background: #1f1f1f; }}
    .ready-title {{ color: #f59e0b; font-size: 14px; font-weight: bold; margin-bottom: 2px; }}
    .ready-loc {{ color: #888; font-size: 11px; }}
    /* ------------------------------------- */

    .tier-badge {{ background: #f59e0b; color: #000; padding: 1px 6px; border-radius: 4px; font-weight: bold; font-size: 10px; }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        if st.text_input("Passcode", type="password") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# بناء الهيدر
now = datetime.now().strftime("%Y-%m-%d | %H:%M")
st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI <span style="color:white; font-size:14px;">PRO</span></div><div style="color:#aaa; font-size:12px; text-align:left;">📅 {now}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], 
    default_index=1, orientation="horizontal",
    styles={"container": {"background-color": "#0a0a0a", "padding": "0"}, "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}}
)

# جلب البيانات
@st.cache_data(ttl=60)
def load_all_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("").astype(str)
        d = pd.read_csv(u_d).fillna("").astype(str)
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_all_data()

# --- توزيع المساحة 70/30 ---
main_col, side_col = st.columns([0.75, 0.25])

# --- الجانب الأيمن (استلام فوري) معدل ---
with side_col:
    st.markdown("<p style='color:#10b981; text-align:center; font-weight:bold; font-size:15px; margin-bottom:10px;'>🔑 استلام فوري فقط</p>", unsafe_allow_html=True)
    st.markdown("<div class='ready-sidebar-container'>", unsafe_allow_html=True)
    # فلترة الاستلام الفوري
    ready_items = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
    if not ready_items.empty:
        for _, row in ready_items.iterrows():
            st.markdown(f"""
                <div class="ready-card">
                    <div class="ready-title">{row.get('Project Name', 'مشروع')}</div>
                    <div class="ready-loc">📍 {row.get('Area', 'الموقع')}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:#555; font-size:11px; text-align:center;'>لا توجد وحدات فورية حالياً</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- الجانب الرئيسي (المشاريع والمطورين) ---
with main_col:
    if menu == "المشاريع":
        s_p = st.text_input("🔍 بحث سـريع...")
        dff_p = df_p.copy()
        if s_p: dff_p = dff_p[dff_p.apply(lambda r: r.astype(str).str.contains(s_p, case=False).any(), axis=1)]
        
        limit = 6
        curr_page = dff_p.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]

        for i in range(0, len(curr_page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(curr_page):
                    row = curr_page.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class='grid-card'>
                                <h3 style='color:#f59e0b; font-size:18px; margin-bottom:10px;'>{row.get('Project Name')}</h3>
                                <p style='font-size:13px;'>📍 <b>الموقع:</b> {row.get('Area')}</p>
                                <p style='font-size:13px; color:#aaa;'>🏢 <b>المطور:</b> {row.get('Developer')}</p>
                                <div style='font-size:11px; color:#666; border-top:1px solid #222; margin-top:10px; padding-top:5px;'>📐 {row.get('Project Area')}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("تفاصيل المشروع"):
                            st.info(f"🎨 **Master Plan:** {row.get('Master Plan', 'N/A')}")
                            st.success(f"⚙️ **إدارة المشروع:** {row.get('Management', 'N/A')}")
                            st.write(f"✨ **المميزات:** {row.get('Project Features')}")

        st.write("---")
        c1, c2 = st.columns(2)
        if c1.button("التالي ⬅️"): st.session_state.p_idx += 1; st.rerun()
        if c2.button("➡️ السابق"): st.session_state.p_idx = max(0, st.session_state.p_idx-1); st.rerun()

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
                        st.markdown(f"""
                            <div class='grid-card'>
                                <div style="display:flex; justify-content:space-between;">
                                    <h3 style='color:#f59e0b; font-size:17px;'>{row.get('Developer')}</h3>
                                    <span class="tier-badge">{row.get('Developer Category', 'N/A')}</span>
                                </div>
                                <p style='font-size:13px; margin-top:5px;'>👤 المالك: {row.get('Owner')}</p>
                                <p style='color:#10b981; font-weight:bold; font-size:13px;'>🏗️ المشاريع: {row.get('Number of Projects')}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("📖 سابقة الأعمال"):
                            st.write(row.get('Detailed_Info'))

    elif menu == "الأدوات":
        st.markdown("<h3 style='color:#f59e0b;'>🛠️ الأدوات</h3>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🧮 القسط", "📐 المساحة"])
        with t1:
            price = st.number_input("السعر", 1000000); y = st.slider("السنين", 1, 15, 8)
            st.metric("القسط الشهري", f"{price/(y*12):,.0f}")
        with t2:
            sq = st.number_input("متر", 100.0); st.write(f"قدم: {sq*10.76:,.2f}")

if st.button("🚪 خروج"):
    st.session_state.auth = False
    st.rerun()
