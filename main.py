import streamlit as st
import pandas as pd
import feedparser
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (Session State)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
# مخزن لمراقبة تغيير المنيو
if 'active_menu' not in st.session_state: st.session_state.active_menu = "المساعد الذكي"

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# 3. جلب الأخبار العقارية
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى في مصر لعام 2026."

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
    div.stButton > button {{ border-radius: 12px !important; font-family: 'Cairo', sans-serif !important; transition: 0.3s !important; }}
    div.stButton > button[key*="card_"] {{
        background-color: white !important; color: #111 !important;
        min-height: 140px !important; text-align: right !important;
        font-weight: bold !important; font-size: 15px !important;
        border: none !important; margin-bottom: 10px !important;
        display: block !important; width: 100% !important;
    }}
    .smart-box {{ background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; }}
    .tool-card {{ background: #1a1a1a; padding: 20px; border-radius: 15px; border-top: 4px solid #f59e0b; text-align: center; height: 100%; }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b; font-size:60px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1,1])
    with c2:
        if st.text_input("كود الدخول المباشر", type="password") == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# 6. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 7. الهيدر
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 150px; background-size: cover; background-position: center; border-radius: 0 0 30px 30px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b;">
        <h1 style="color: white; margin: 0; font-size: 35px;">MA3LOMATI PRO</h1>
    </div>
""", unsafe_allow_html=True)

# 8. شريط المعلومات
c_top1, c_top2 = st.columns([0.7, 0.3])
with c_top1:
    st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)
with c_top2:
    st.markdown(f"<div style='color: #aaa; font-size: 13px;'>📅 {egypt_now.strftime('%Y-%m-%d')} | 🕒 {egypt_now.strftime('%I:%M %p')}</div>", unsafe_allow_html=True)

# 9. المنيو الرئيسي
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], default_index=0, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# *** التعديل الجوهري لحل مشكلة التعليق ***
if menu != st.session_state.active_menu:
    st.session_state.selected_item = None # مسح أي كارت مفتوح فوراً عند تغيير الصفحة
    st.session_state.active_menu = menu
    st.rerun()

# 10. منطق عرض الصفحات (تم الترتيب لضمان عمل كل الأزرار)
if st.session_state.selected_item is not None:
    # عرض التفاصيل لو تم اختيار كارت
    if st.button("⬅️ عودة للقائمة"): 
        st.session_state.selected_item = None
        st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"""<div class='smart-box'>
        <h2>{item.get('ProjectName', item.get('Developer'))}</h2>
        <p>📍 الموقع: {item.get('Location', '---')}</p>
        <p>🏗️ المطور: {item.get('Developer', '---')}</p>
        <hr><p>{item.get('Payment Plan', 'بيانات إضافية غير متوفرة')}</p>
    </div>""", unsafe_allow_html=True)

else:
    # عرض محتوى الصفحات العادي
    if menu == "المساعد الذكي":
        st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
        st.title("🤖 مساعد الربط العقاري")
        # كود المساعد الذكي...
        st.write("أهلاً بك في المحرك الذكي لعام 2026")
        st.markdown("</div>", unsafe_allow_html=True)

    elif menu == "المشاريع":
        m_col, s_col = st.columns([0.7, 0.3])
        with s_col:
            st.markdown("<h4 style='color:#10b981;'>🔑 استلام فوري</h4>", unsafe_allow_html=True)
            ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(8)
            for i, r in ready.iterrows():
                if st.button(f"✅ {r['ProjectName']}", key=f"ready_{i}"):
                    st.session_state.selected_item = r
                    st.rerun()
        with m_col:
            search = st.text_input("🔍 ابحث باسم المشروع")
            dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
            page = dff.iloc[st.session_state.p_idx*6 : st.session_state.p_idx*6+6]
            for i in range(0, len(page), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i+j < len(page):
                        row = page.iloc[i+j]
                        if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}", key=f"card_p_{i+j}"):
                            st.session_state.selected_item = row
                            st.rerun()

    elif menu == "المطورين":
        m_col, s_col = st.columns([0.7, 0.3])
        with s_col:
            st.markdown("<h4 style='color:#f59e0b;'>🏆 Top 10</h4>", unsafe_allow_html=True)
            for i, r in df_d.head(10).iterrows():
                st.write(f"⭐ {r['Developer']}")
        with m_col:
            search_d = st.text_input("🔍 ابحث عن مطور")
            dfd_f = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
            for i, row in dfd_f.head(6).iterrows():
                if st.button(f"🏗️ {row['Developer']} | {row.get('Owner','---')}", key=f"card_d_{i}"):
                    st.session_state.selected_item = row
                    st.rerun()

    elif menu == "أدوات البروكر":
        st.title("🛠️ حقيبة البروكر")
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("حاسبة القسط", "جاهزة")
        with c2: st.metric("العمولة", "جاهزة")
        with c3: st.metric("المساحة", "جاهزة")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
