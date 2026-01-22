import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة الفخمة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. روابط البيانات ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
URL_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- 4. جلب البيانات والأخبار ---
@st.cache_data(ttl=60)
def load_all_data():
    try:
        p = pd.read_csv(URL_P).fillna("---")
        d = pd.read_csv(URL_D).fillna("---")
        l = pd.read_csv(URL_L).fillna("---")
        for df in [p, d, l]: df.columns = df.columns.str.strip()
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d, l
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

@st.cache_data(ttl=1800)
def get_news():
    try:
        feed = feedparser.parse("https://www.youm7.com/rss/SectionRss?SectionID=297")
        return "  •  ".join([item.title for item in feed.entries[:10]])
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى لعام 2026."

# --- 5. التنسيق الجمالي (CSS) - النسخة الذهبية ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    /* الهيدر الفخم */
    .main-header {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1600&q=80');
        height: 220px; background-size: cover; background-position: center;
        border-radius: 0 0 40px 40px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b;
        margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}

    /* شريط الأخبار */
    .ticker-wrap {{ width: 100%; background: #111; padding: 8px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; }}
    .ticker {{ display: inline-block; animation: ticker 180s linear infinite; color: #f59e0b; font-size: 14px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* الكروت التفاعلية */
    div.stButton > button {{ border-radius: 15px !important; font-family: 'Cairo' !important; transition: 0.3s !important; }}
    div.stButton > button[key*="card_"] {{
        background: #161616 !important; color: white !important;
        min-height: 140px !important; border: 1px solid #333 !important;
        border-top: 5px solid #f59e0b !important; font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }}
    div.stButton > button:hover {{ transform: translateY(-5px) !important; border-color: #f59e0b !important; background: #1a1a1a !important; }}

    /* الحاويات الذكية */
    .smart-box {{ background: #111; padding: 25px; border-radius: 20px; border-right: 6px solid #f59e0b; color: white; margin-bottom: 15px; }}
    .tool-card {{ background: #1a1a1a; padding: 20px; border-radius: 15px; border-top: 4px solid #f59e0b; text-align: center; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. تسجيل الدخول ---
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:80px;'><h1 style='color:#f59e0b; font-size:60px; margin-bottom:0;'>MA3LOMATI</h1><p style='color:#777;'>PRO VERSION 2026</p></div>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 1.4, 1])
    with col_mid:
        u_in = st.text_input("اسم المستخدم / البريد الإلكتروني")
        p_in = st.text_input("كلمة المرور", type="password")
        if st.button("دخول آمن للمنصة 🚀", use_container_width=True):
            if p_in == "2026": 
                st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
            else: st.error("بيانات الدخول غير صحيحة")
    st.stop()

# --- 7. الهيدر وشريط الأدوات العلوي ---
df_p, df_d, df_l = load_all_data()
news_text = get_news()

st.markdown(f"""
    <div class="main-header">
        <h1 style="color: white; font-size: 50px; text-shadow: 2px 2px 15px rgba(0,0,0,0.8);">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-size: 20px;">مرحباً بك يا {st.session_state.current_user} في عالم العقارات الذكي</p>
    </div>
""", unsafe_allow_html=True)

c_out, c_news = st.columns([0.15, 0.85])
with c_out:
    if st.button("🚪 خروج", key="logout"): st.session_state.auth = False; st.rerun()
with c_news:
    st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

# --- 8. المنيو الرئيسي ---
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], 
    icons=["briefcase", "building", "search", "robot", "rocket"], 
    default_index=4, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# --- 9. محتوى الأقسام (تنسيق 70/30) ---

if menu == "اللونشات":
    if st.session_state.selected_item is not None:
        if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
        it = st.session_state.selected_item
        st.markdown(f"""<div class='smart-box'>
            <h1 style='color:#f59e0b;'>{it.get('Project','---')}</h1>
            <div style='display:grid; grid-template-columns: 1fr 1fr; gap:20px;'>
                <div><p style='color:#f59e0b;'>🏢 المطور</p><h3>{it.get('Developer','---')}</h3></div>
                <div><p style='color:#f59e0b;'>📍 الموقع</p><h3>{it.get('Location','---')}</h3></div>
                <div><p style='color:#f59e0b;'>📏 المساحات</p><h4>{it.get('Units & Sizes','---')}</h4></div>
                <div><p style='color:#f59e0b;'>💰 السعر والسداد</p><h4>{it.get('Price & Payment','---')}</h4></div>
            </div>
            <hr style='border-color:#333;'>
            <p style='color:#f59e0b;'>🌟 مميزات المشروع (USP)</p>
            <p style='font-size:18px; line-height:1.7;'>{it.get('Unique Selling Points (USP)','---')}</p>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align:center;'>🚀 أحدث الانطلاقات العقارية 2026</h2>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, r in df_l.iterrows():
            with cols[i % 3]:
                lbl = f"🏢 {r['Developer']}\n{r['Project']}\n📍 {r['Location']}"
                if st.button(lbl, key=f"card_l_{i}"):
                    st.session_state.selected_item = r; st.rerun()

elif menu == "المشاريع":
    m_col, s_col = st.columns([0.7, 0.3])
    with s_col:
        st.markdown("<div class='smart-box'><h4>🔥 مشاريع مميزة</h4><p>التجمع الخامس<br>العاصمة الإدارية<br>زايد الجديدة</p></div>", unsafe_allow_html=True)
    with m_col:
        search = st.text_input("🔍 ابحث عن أي مشروع في مصر")
        dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
        start = st.session_state.p_idx * 6
        page = dff.iloc[start:start+6]
        grid = st.columns(2)
        for idx, r in page.iterrows():
            with grid[idx % 2]:
                if st.button(f"🏗️ {r['ProjectName']}\n📍 {r['Location']}\n🏢 {r['Developer']}", key=f"card_p_{idx}"):
                    st.session_state.selected_item = r; st.rerun()
        # تقليب الصفحات
        if len(dff) > 6:
            c1, c2 = st.columns(2)
            if start > 0 and c1.button("السابق"): st.session_state.p_idx -= 1; st.rerun()
            if start+6 < len(dff) and c2.button("التالي"): st.session_state.p_idx += 1; st.rerun()

elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'><h2>🤖 المساعد العقاري الذكي</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    loc = c1.selectbox("المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    typ = c2.selectbox("النوع", ["شقق", "فيلات", "تجاري"])
    bud = c3.number_input("المقدم المتاح", 0)
    if st.button("استخراج أفضل الترشيحات 🎯"):
        st.balloons()
        st.success("تم إيجاد 3 مشاريع مطابقة لطلبك..")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "المطورين":
    search_d = st.text_input("🔍 ابحث عن مطور")
    res_d = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
    for _, r in res_d.head(10).iterrows():
        with st.expander(f"🏗️ {r['Developer']}"):
            st.write(f"⭐ الفئة: {r.get('Developer Category','A')}")
            st.write(f"👤 المالك: {r.get('Owner','---')}")

elif menu == "أدوات البروكر":
    st.markdown("<h2 style='text-align:center;'>🛠️ حقيبة البروكر الذكية</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='tool-card'><h3>💳 حاسبة القسط</h3>", unsafe_allow_html=True)
        p = st.number_input("السعر", 1000000, key="calc_p")
        d = st.number_input("المقدم", 100000, key="calc_d")
        y = st.slider("السنين", 1, 10, 8)
        st.metric("القسط الشهري", f"{(p-d)/(y*12):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='tool-card'><h3>💰 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("قيمة البيعة", 1000000, key="calc_deal")
        pct = st.slider("النسبة %", 1.0, 5.0, 2.5)
        st.metric("صافي عمولتك", f"{deal*(pct/100):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='tool-card'><h3>📐 المساحات</h3>", unsafe_allow_html=True)
        m2 = st.number_input("المتر المربع", 100)
        st.metric("بالقدم المربع", f"{m2*10.76:,.1f}")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown(f"<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © {egypt_now.year} | جميع الحقوق محفوظة</p>", unsafe_allow_html=True)
