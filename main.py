import streamlit as st
import pandas as pd
import math
import feedparser
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

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

# 4. التنسيق الجمالي (CSS المطور لدمج الأزرار)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    .luxury-header {{
        background: rgba(15, 15, 15, 0.9); backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b; padding: 15px 30px;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; border-radius: 0 0 25px 25px; margin-bottom: 15px;
    }
    .logo-text {{ color: #f59e0b; font-weight: 900; font-size: 24px; }}
    
    .ticker-wrap {{ width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 10px; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* تحويل زر Streamlit إلى كارت BrokerEdge */
    div.stButton > button[key*="card_"] {{
        background-color: #111 !important;
        color: white !important;
        border: 1px solid #222 !important;
        border-right: 5px solid #f59e0b !important;
        border-radius: 12px !important;
        width: 100% !important;
        height: 160px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: flex-start !important;
        justify-content: center !important;
        padding: 20px !important;
        transition: 0.3s !important;
        text-align: right !important;
    }}
    div.stButton > button[key*="card_"]:hover {{
        background-color: #1a1a1a !important;
        border-color: #f59e0b !important;
        transform: translateY(-5px) !important;
    }}

    .ready-sidebar-container {{
        background: #0d0d0d; border: 1px solid #222; border-radius: 15px; padding: 12px;
        max-height: 80vh; overflow-y: auto; border-top: 3px solid #10b981;
    }}
    .ready-card {{ background: #161616; border-right: 3px solid #10b981; padding: 10px; border-radius: 8px; margin-bottom: 8px; }}
    
    /* زر الخروج الصغير */
    div.stButton > button[key="logout_btn"] {{
        background-color: #ef4444 !important; color: white !important;
        height: 30px !important; width: 60px !important; font-size: 11px !important; border: none !important;
    }}
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

# بناء الهيدر
now = datetime.now().strftime("%Y-%m-%d")
st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI <span style="color:white; font-size:14px;">PRO</span></div><div style="color:#aaa; font-size:12px;">📅 {now}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], 
    default_index=1, orientation="horizontal",
    styles={"container": {"background-color": "#0a0a0a"}, "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}}
)

# جلب البيانات
@st.cache_data(ttl=60)
def load_all_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("").astype(str)
        d = pd.read_csv(u_d).fillna("").astype(str)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_all_data()

# --- توزيع المساحة 75/25 ---
main_col, side_col = st.columns([0.75, 0.25])

# الجانب الأيسر (استلام فوري)
with side_col:
    st.markdown("<p style='color:#10b981; text-align:center; font-weight:bold; font-size:15px;'>🔑 استلام فوري</p>", unsafe_allow_html=True)
    st.markdown("<div class='ready-sidebar-container'>", unsafe_allow_html=True)
    ready_items = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(10)
    for _, row in ready_items.iterrows():
        st.markdown(f'<div class="ready-card"><div style="color:#f59e0b; font-size:13px;">{row.get("Project Name")}</div><div style="color:#888; font-size:10px;">📍 {row.get("Area")}</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("تسجيل خروج", key="logout_btn"):
        st.session_state.auth = False; st.rerun()

# الجانب الرئيسي
with main_col:
    if st.session_state.selected_item:
        # عرض التفاصيل عند الضغط
        item = st.session_state.selected_item
        if st.button("⬅️ عودة للقائمة", key="back_btn"):
            st.session_state.selected_item = None; st.rerun()
        
        st.markdown(f"""
            <div style="background:#111; padding:25px; border-radius:15px; border-right:5px solid #f59e0b; color:white;">
                <h2 style="color:#f59e0b;">{item.get('Project Name', item.get('Developer'))}</h2>
                <p>📍 الموقع: {item.get('Area', 'N/A')}</p>
                <hr style="opacity:0.1;">
                <p style="font-size:16px;">{item.get('Project Features', item.get('Detailed_Info', 'لا توجد تفاصيل إضافية'))}</p>
            </div>
        """, unsafe_allow_html=True)

    elif menu == "المشاريع":
        s_p = st.text_input("🔍 بحث سـريع عن المشاريع...")
        dff_p = df_p.copy()
        if s_p: dff_p = dff_p[dff_p.apply(lambda r: r.astype(str).str.contains(s_p, case=False).any(), axis=1)]
        
        limit = 6
        items = dff_p.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]

        for i in range(0, len(items), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(items):
                    row = items.iloc[i+j]
                    with cols[j]:
                        # الزر المخصص (الكارت)
                        btn_label = f"{row.get('Project Name')}\n\n📍 {row.get('Area')}"
                        if st.button(btn_label, key=f"card_p_{i+j}"):
                            st.session_state.selected_item = row
                            st.rerun()

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
                        btn_label = f"{row.get('Developer')}\n\n🏗️ مشاريع: {row.get('Number of Projects')}"
                        if st.button(btn_label, key=f"card_d_{i+j}"):
                            st.session_state.selected_item = row
                            st.rerun()

    elif menu == "الأدوات":
        st.info("قسم الأدوات يعمل بشكل طبيعي")
