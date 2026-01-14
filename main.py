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

# 4. التنسيق الجمالي (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    .luxury-header {{
        background: rgba(15, 15, 15, 0.9); backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b; padding: 20px 40px;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; border-radius: 0 0 30px 30px; margin-bottom: 20px;
    }}
    .logo-text {{ color: #f59e0b; font-weight: 900; font-size: 28px; text-shadow: 0 0 10px rgba(245, 158, 11, 0.5); }}
    
    .ticker-wrap {{ width: 100%; background: transparent; padding: 10px 0; overflow: hidden; white-space: nowrap; }}
    .ticker {{ display: inline-block; animation: ticker 180s linear infinite; color: #ccc; font-size: 14px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    .grid-card {{ 
        background: linear-gradient(145deg, #111, #1a1a1a); border: 1px solid #222; 
        border-right: 5px solid #f59e0b; border-radius: 15px; padding: 20px; margin-bottom: 20px;
        transition: all 0.4s ease; min-height: 220px; display: flex; flex-direction: column; justify-content: space-between;
    }}
    .grid-card:hover {{ transform: scale(1.02); box-shadow: 0 10px 20px rgba(245, 158, 11, 0.1); border-color: #f59e0b; }}

    .tier-badge {{ background: #f59e0b; color: #000; padding: 2px 8px; border-radius: 5px; font-weight: bold; font-size: 12px; }}
    .ready-sidebar {{ background: #0f0f0f; border: 1px solid #222; border-radius: 20px; padding: 15px; height: 80vh; overflow-y: auto; border-top: 4px solid #10b981; }}
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

# --- بناء الهيدر ---
now = datetime.now().strftime("%Y-%m-%d | %H:%M")
st.markdown(f"""
    <div class="luxury-header">
        <div class="logo-text">MA3LOMATI <span style="color:white; font-size:15px;">PRO 2026</span></div>
        <div style="color:white; font-size:14px; text-align:left;">📅 {now}<br><span style="color:#f59e0b;">Real Estate Intelligence</span></div>
    </div>
""", unsafe_allow_html=True)

# شريط الأخبار
st.markdown(f'<div class="ticker-wrap"><div class="ticker"><b>🔥 حصرياً:</b> {news_text}</div></div>', unsafe_allow_html=True)

# القائمة الرئيسية
menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], 
    default_index=1, orientation="horizontal",
    styles={"container": {"background-color": "#0a0a0a"}, "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}}
)

# 6. جلب البيانات
@st.cache_data(ttl=60)
def load_all_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        df_p = pd.read_csv(u_p).fillna("غير متوفر").astype(str)
        df_d = pd.read_csv(u_d).fillna("غير متوفر").astype(str)
        df_p.columns = df_p.columns.str.strip()
        df_d.columns = df_d.columns.str.strip()
        return df_p, df_d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_all_data()

# --- توزيع المساحة 70/30 ---
main_col, side_col = st.columns([0.7, 0.3])

# --- الجانب الأيمن (استلام فوري) ---
with side_col:
    st.markdown("<h4 style='color:#10b981; text-align:center;'>🔑 استلام فوري فقط</h4>", unsafe_allow_html=True)
    st.markdown("<div class='ready-sidebar'>", unsafe_allow_html=True)
    ready_df = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
    for _, row in ready_df.iterrows():
        st.markdown(f"""<div style='background:#161616; padding:10px; border-radius:10px; border-right:3px solid #10b981; margin-bottom:10px;'>
            <b style='color:#f59e0b;'>{row.get('Project Name')}</b><br><small>📍 {row.get('Area')}</small></div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- الجانب الرئيسي (70%) ---
with main_col:
    if menu == "المشاريع":
        st.markdown("<h2 style='color:#f59e0b;'>🏗️ استكشاف المشاريع</h2>", unsafe_allow_html=True)
        s_p = st.text_input("🔍 ابحث بالاسم أو الموقع أو المطور...")
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
                                <div>
                                    <h3 style='color:#f59e0b; margin-top:0;'>{row.get('Project Name')}</h3>
                                    <p>📍 <b>الموقع:</b> {row.get('Area')}</p>
                                    <p>🏢 <b>المطور:</b> {row.get('Developer')}</p>
                                </div>
                                <div style="font-size:12px; color:#aaa; border-top:1px solid #333; padding-top:10px;">
                                    📏 المساحة: {row.get('Project Area')}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("🔎 كامل المواصفات و Master Plan"):
                            st.success(f"🎨 **Master Plan:** {row.get('Master Plan')}")
                            st.info(f"⚙️ **إدارة المشروع (Management):** {row.get('Management')}")
                            st.warning(f"✨ المميزات: {row.get('Project Features')}")
                            st.error(f"⚠️ العيوب: {row.get('Project Flaws')}")
        
        c1, c2 = st.columns(2)
        if c1.button("الصفحة التالية"): st.session_state.p_idx += 1; st.rerun()
        if c2.button("الصفحة السابقة"): st.session_state.p_idx = max(0, st.session_state.p_idx-1); st.rerun()

    elif menu == "المطورين":
        st.markdown("<h2 style='color:#f59e0b;'>🏢 دليل المطورين</h2>", unsafe_allow_html=True)
        s_d = st.text_input("🔍 ابحث عن مطور...")
        dff_d = df_d.copy()
        if s_d: dff_d = dff_d[dff_d.apply(lambda r: r.astype(str).str.contains(s_d, case=False).any(), axis=1)]

        curr_d = dff_d.iloc[st.session_state.d_idx*6 : (st.session_state.d_idx+1)*6]
        for i in range(0, len(curr_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(curr_d):
                    row = curr_d.iloc[i+j]
                    tier = row.get('Developer Category', 'N/A')
                    with cols[j]:
                        st.markdown(f"""
                            <div class='grid-card'>
                                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                                    <h3 style='color:#f59e0b; margin-top:0;'>{row.get('Developer')}</h3>
                                    <span class="tier-badge">{tier}</span>
                                </div>
                                <p>👤 <b>المالك:</b> {row.get('Owner')}</p>
                                <p style='color:#10b981; font-weight:bold;'>🏗️ عدد المشاريع: {row.get('Number of Projects')}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("📖 سابقة الأعمال"):
                            st.write(row.get('Detailed_Info'))

    elif menu == "الأدوات":
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ الأدوات الذكية</h2>", unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["🧮 القسط", "📈 العائد", "📐 المساحة"])
        with t1:
            p = st.number_input("سعر الوحدة", 1000000); d = st.number_input("المقدم", p*0.1); y = st.slider("السنين", 1, 15, 8)
            st.metric("القسط الشهري", f"{(p-d)/(y*12):,.0f}")
        with t2:
            rent = st.number_input("الإيجار المتوقع", 10000)
            st.metric("العائد السنوي ROI", f"{(rent*12/p)*100:.2f}%")
        with t3:
            sq = st.number_input("متر مربع", 100.0)
            st.write(f"قدم مربع: {sq*10.76:,.2f}")

if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state.auth = False
    st.rerun()
