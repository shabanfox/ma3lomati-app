import streamlit as st
import pandas as pd
import feedparser
import urllib.parse
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 3. جلب الأخبار العقارية
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
    .ticker-wrap {{ width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 20px; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    div.stButton > button {{ border-radius: 12px !important; font-family: 'Cairo', sans-serif !important; }}
    div.stButton > button[key*="card_"] {{
        background-color: white !important; color: #111 !important;
        min-height: 180px !important; text-align: right !important;
        font-weight: bold !important; font-size: 15px !important;
        border: none !important; transition: 0.3s !important;
    }}
    div.stButton > button[key*="card_"]:hover {{ transform: translateY(-5px) !important; border: 2px solid #f59e0b !important; }}
    .smart-box {{ background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; margin-top: 10px; }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b; font-size:60px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1,1])
    with c2:
        if st.text_input("كود الدخول المباشر", type="password") == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# 6. جلب البيانات (مع معالجة الدمج والتكرار)
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        
        # --- دمج المطورين ---
        if 'Developer' in p.columns:
            p['Developer'] = p['Developer'].astype(str).apply(lambda x: " ".join(x.split()).strip())
        if 'Developer' in d.columns:
            d['Developer'] = d['Developer'].astype(str).apply(lambda x: " ".join(x.split()).strip())
            d = d.drop_duplicates(subset=['Developer'], keep='first')

        # --- دمج المشاريع ---
        if 'Project Name' in p.columns:
            p['Project Name'] = p['Project Name'].astype(str).apply(lambda x: " ".join(x.split()).strip())
            p = p.drop_duplicates(subset=['Project Name', 'Developer'], keep='first')
            
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 7. الهيدر
h_col1, h_col2, h_col3 = st.columns([1.5, 2, 1])
with h_col1: st.markdown('<div style="color: #f59e0b; font-weight: 900; font-size: 28px;">MA3LOMATI PRO</div>', unsafe_allow_html=True)
with h_col2:
    st.markdown(f"<div style='text-align:center; color:white;'>📅 {datetime.now().strftime('%Y-%m-%d')} | 🕒 {datetime.now().strftime('%I:%M %p')}</div>", unsafe_allow_html=True)
with h_col3:
    if st.button("🚪 خروج", use_container_width=True): st.session_state.auth = False; st.rerun()

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

# 8. القائمة الرئيسية
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "people", "tools"], default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# 9. عرض المحتوى
col_main, col_side = st.columns([0.78, 0.22])

with col_side:
    st.markdown("<h4 style='color:#10b981; text-align:center;'>🔑 استلام فوري</h4>", unsafe_allow_html=True)
    if not df_p.empty:
        ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(10)
        for _, row in ready.iterrows():
            st.markdown(f'<div style="background:#111; border-right:3px solid #10b981; padding:10px; border-radius:10px; margin-bottom:8px; font-size:12px; color:white;">{row["Project Name"]}</div>', unsafe_allow_html=True)

with col_main:
    if st.session_state.selected_item is not None:
        if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
        item = st.session_state.selected_item
        st.markdown(f"<div class='smart-box'><h2>{item.get('Project Name', 'تفاصيل')}</h2><hr><p>{item.get('Developer', '---')}</p></div>", unsafe_allow_html=True)

    elif menu == "المشاريع":
        f1, f2 = st.columns(2)
        search = f1.text_input("🔍 بحث")
        area_f = f2.selectbox("📍 المنطقة", ["الكل"] + sorted(df_p['Area'].unique().tolist()) if 'Area' in df_p.columns else ["الكل"])
        
        dff = df_p.copy()
        if search: dff = dff[dff['Project Name'].str.contains(search, case=False)]
        if area_f != "الكل": dff = dff[dff['Area'] == area_f]
        
        start = st.session_state.p_idx * 6
        page = dff.iloc[start:start+6]
        for i in range(0, len(page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page):
                    row = page.iloc[i+j]
                    if cols[j].button(f"🏢 {row['Project Name']}\n🏗️ {row['Developer']}", key=f"card_p_{start+i+j}"):
                        st.session_state.selected_item = row; st.rerun()
        
        st.markdown("---")
        p1, _, p2 = st.columns([1,2,1])
        if st.session_state.p_idx > 0 and p1.button("⬅️ السابق"): st.session_state.p_idx -= 1; st.rerun()
        if start + 6 < len(dff) and p2.button("التالي ➡️"): st.session_state.p_idx += 1; st.rerun()

    elif menu == "المطورين":
        dev_list = sorted(df_p['Developer'].unique().tolist())
        for d in dev_list:
            with st.expander(f"🏗️ {d}"):
                st.write(f"مشاريع المطور: {', '.join(df_p[df_p['Developer']==d]['Project Name'].tolist())}")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
