import streamlit as st
import pandas as pd
import feedparser
import time
import random
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'cache_key' not in st.session_state: st.session_state.cache_key = random.randint(1, 999999)

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

# 4. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    
    .luxury-header {
        background: rgba(15, 15, 15, 0.9); backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b; padding: 10px 30px;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; border-radius: 0 0 25px 25px; margin-bottom: 10px;
    }
    .logo-text { color: #f59e0b; font-weight: 900; font-size: 22px; }
    
    /* ستايل الكروت الأبيض */
    div.stButton > button[key*="card_"] {
        background-color: white !important; color: #111 !important; border-radius: 12px !important; 
        width: 100% !important; min-height: 200px !important; text-align: right !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important; white-space: pre-wrap !important;
        font-size: 16px !important; font-weight: bold !important; line-height: 1.6 !important;
    }
    
    /* زر الخروج الأحمر */
    div.stButton > button[key="logout_top"] {
        background-color: #dc2626 !important; color: white !important; border-radius: 8px !important;
        padding: 5px 15px !important; font-size: 14px !important; border: none !important;
    }

    /* أزرار التالي والسابق */
    div.stButton > button[key*="_nav"] {
        background-color: #333 !important; color: white !important; width: 100% !important;
    }

    .sidebar-box { background: #0d0d0d; border: 1px solid #222; border-radius: 15px; padding: 10px; border-top: 3px solid #10b981; }
    .ready-card { background: #161616; border-right: 3px solid #10b981; padding: 8px; border-radius: 5px; margin-bottom: 5px; font-size: 13px; color: #eee; }
    .ticker-wrap { width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 10px; }
    .ticker { display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
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

# الهيدر وزر الخروج في مكانه
h_col1, h_col2 = st.columns([0.88, 0.12])
with h_col1:
    st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI PRO</div><div style="color:#aaa; font-size:12px;">📅 {datetime.now().strftime("%Y-%m-%d")}</div></div>', unsafe_allow_html=True)
with h_col2:
    st.markdown("<div style='margin-top:15px;'>", unsafe_allow_html=True)
    if st.button("🚪 خروج", key="logout_top"):
        st.session_state.auth = False; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

# 6. جلب البيانات
@st.cache_data(ttl=200)
def load_data(cache_key):
    u_p = f"https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv&cache={cache_key}"
    u_d = f"https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv&cache={cache_key}"
    try:
        p = pd.read_csv(u_p).fillna("جاري التحديث...").astype(str)
        d = pd.read_csv(u_d).fillna("جاري التحديث...").astype(str)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data(st.session_state.cache_key)

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], default_index=1, orientation="horizontal",
    styles={"container": {"background-color": "#0a0a0a"}, "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}}
)

main_col, side_col = st.columns([0.75, 0.25])

with side_col:
    st.markdown("<p style='color:#10b981; font-weight:bold;'>🔑 استلام فوري</p>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-box'>", unsafe_allow_html=True)
    if not df_p.empty:
        ready_df = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
        for _, row in ready_df.head(8).iterrows():
            st.markdown(f'<div class="ready-card"><b>{row.get("Project Name")}</b><br><small>📍 {row.get("Area")}</small></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with main_col:
    if st.session_state.selected_item is not None:
        item = st.session_state.selected_item
        if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
        st.markdown(f"""
            <div style="background:#111; padding:25px; border-radius:15px; border-right:5px solid #f59e0b; color:white;">
                <h2>{item.get('Project Name', item.get('Developer'))}</h2>
                <hr style='opacity:0.2;'>
                <p>{item.get('Project Features', item.get('Detailed_Info', 'لا توجد تفاصيل'))}</p>
            </div>
        """, unsafe_allow_html=True)

    elif menu == "المشاريع":
        search = st.text_input("🔍 ابحث في المشاريع...")
        dff = df_p.copy()
        if search: dff = dff[dff.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        
        # حصر العرض في 6 كروت فقط
        limit = 6
        pages = dff.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]
        
        for i in range(0, len(pages), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(pages):
                    row = pages.iloc[i+j]
                    with cols[j]:
                        lbl = f"🏢 {row.get('Project Name')}\n📍 {row.get('Area')}\n🏗️ {row.get('Developer')}\n📐 {row.get('Project Area')}"
                        if st.button(lbl, key=f"card_p_{i+j}"): st.session_state.selected_item = row; st.rerun()
        
        # أزرار التنقل
        st.markdown("---")
        n1, n2, n3 = st.columns([1,1,1])
        if st.session_state.p_idx > 0:
            if n1.button("⬅️ السابق", key="prev_nav"): st.session_state.p_idx -= 1; st.rerun()
        if (st.session_state.p_idx + 1) * limit < len(dff):
            if n3.button("التالي ➡️", key="next_nav"): st.session_state.p_idx += 1; st.rerun()

    elif menu == "المطورين":
        search_d = st.text_input("🔍 ابحث عن مطور...")
        dff_d = df_d.copy()
        if search_d: dff_d = dff_d[dff_d.apply(lambda r: r.astype(str).str.contains(search_d, case=False).any(), axis=1)]
        
        for i in range(0, len(dff_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(dff_d):
                    row = dff_d.iloc[i+j]
                    with cols[j]:
                        lbl = f"🏗️ {row.get('Developer')}\n👑 {row.get('Owner')}\n⭐ فئة {row.get('Developer Category')}"
                        if st.button(lbl, key=f"card_d_{i+j}"): st.session_state.selected_item = row; st.rerun()

    elif menu == "الأدوات":
        st.markdown("<h2 style='color:#f59e0b;'>الأدوات</h2>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["💰 حاسبة الأقساط", "📐 محول المساحات"])
        with t1:
            price = st.number_input("إجمالي السعر", value=2000000)
            years = st.slider("سنين التقسيط", 1, 15, 7)
            st.metric("القسط الشهري", f"{price/(years*12):,.0f} ج.م")
        with t2:
            sqm = st.number_input("المساحة م2", value=100.0)
            st.write(f"القدم المربع: {sqm * 10.76:,.2f}")
