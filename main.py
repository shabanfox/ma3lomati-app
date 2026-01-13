import streamlit as st
import pandas as pd
import math
import feedparser
from streamlit_option_menu import option_menu 
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0

# 3. جلب الأخبار
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "جاري تحديث الأخبار..."
    except: return "سوق العقارات المصري: متابعة مستمرة."

news_text = get_real_news()

# 4. التنسيق الجمالي المطور (Header 2.0)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #0a0a0a; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    /* الهيدر الجمالي الجديد */
    .luxury-header {{
        background: rgba(15, 15, 15, 0.8);
        backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b;
        padding: 20px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 30px rgba(245, 158, 11, 0.1);
        position: sticky;
        top: 0;
        z-index: 999;
        margin-bottom: 20px;
        border-radius: 0 0 30px 30px;
    }}
    
    .logo-text {{
        color: #f59e0b;
        font-weight: 900;
        font-size: 28px;
        text-shadow: 0 0 10px rgba(245, 158, 11, 0.5);
        letter-spacing: 1px;
    }}
    
    .header-info {{ color: #ffffff; font-size: 14px; text-align: left; }}
    
    /* شريط الأخبار */
    .ticker-wrap {{ 
        width: 100%; background: transparent; padding: 10px 0; overflow: hidden; white-space: nowrap; 
    }}
    .ticker {{ 
        display: inline-block; animation: ticker 180s linear infinite; color: #ccc; font-size: 14px; 
    }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* كروت الشبكة */
    .grid-card {{ 
        background: linear-gradient(145deg, #111, #1a1a1a);
        border: 1px solid #222; 
        border-right: 5px solid #f59e0b; 
        border-radius: 15px; padding: 20px; margin-bottom: 20px;
        transition: all 0.4s ease;
    }}
    .grid-card:hover {{ transform: scale(1.02); box-shadow: 0 10px 20px rgba(0,0,0,0.5); border-color: #f59e0b; }}

    /* أزرار مخصصة */
    .stButton button {{
        background: linear-gradient(90deg, #1a1a1a, #222) !important;
        color: #f59e0b !important;
        border: 1px solid #f59e0b !important;
        border-radius: 12px !important;
        transition: 0.3s !important;
    }}
    .stButton button:hover {{ background: #f59e0b !important; color: #000 !important; }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول (بسيطة وجذابة)
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding:100px;'><h1 style='color:#f59e0b;'>Ma3lomati PRO</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        if st.text_input("Passcode", type="password") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# --- بناء الهيدر المطور ---
now = datetime.now().strftime("%Y-%m-%d | %H:%M")
st.markdown(f"""
    <div class="luxury-header">
        <div class="logo-text">MA3LOMATI <span style="color:white; font-size:15px;">PRO 2026</span></div>
        <div class="header-info">
            <span style="color:#f59e0b;">📅 {now}</span><br>
            <span style="color:#aaa;">سوق العقارات المصري</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# زر الخروج في مكان مميز
col_out, col_empty = st.columns([0.15, 0.85])
with col_out:
    if st.button("🚪 تسجيل الخروج"): st.session_state.auth = False; st.rerun()

# شريط الأخبار
st.markdown(f'<div class="ticker-wrap"><div class="ticker"><b>🔥 حصرياً:</b> {news_text}</div></div>', unsafe_allow_html=True)

# القائمة الرئيسية
menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], 
    menu_icon="cast", default_index=1, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#0a0a0a"},
        "icon": {"color": "#f59e0b", "font-size": "18px"}, 
        "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#222"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black"},
    }
)

# 6. جلب البيانات من الشيتين
@st.cache_data(ttl=60)
def load_all_data():
    u_projects = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_developers = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        df_p = pd.read_csv(u_projects).fillna("غير متوفر").astype(str)
        df_d = pd.read_csv(u_developers).fillna("غير متوفر").astype(str)
        df_p.columns = df_p.columns.str.strip()
        df_d.columns = df_d.columns.str.strip()
        return df_p, df_d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_all_data()

# --- توزيع المساحة 70% ---
main_col, _ = st.columns([0.7, 0.3])

with main_col:
    if menu == "المشاريع":
        st.markdown("<h2 style='color:#f59e0b;'>🏗️ استكشاف المشاريع</h2>", unsafe_allow_html=True)
        s_p = st.text_input("🔍 ابحث بالاسم أو الموقع...")
        dff_p = df_p.copy()
        if s_p: dff_p = dff_p[dff_p['Project Name'].str.contains(s_p, case=False) | dff_p['Area'].str.contains(s_p, case=False)]
        
        limit = 6
        total_p = math.ceil(len(dff_p) / limit)
        curr_page = dff_p.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]

        for i in range(0, len(curr_page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(curr_page):
                    row = curr_page.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class='grid-card'>
                                <h3 style='color:#f59e0b; margin-top:0;'>{row.get('Project Name')}</h3>
                                <p>📍 <b>الموقع:</b> {row.get('Area')}</p>
                                <p>📐 <b>المساحة:</b> {row.get('Project Area')}</p>
                                <p style="color:#aaa;">🏢 المطور: {row.get('Developer')}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("🔎 كامل المواصفات"):
                            st.info(f"✨ المميزات: {row.get('Project Features')}")
                            st.warning(f"⚠️ العيوب: {row.get('Project Flaws')}")
        
        st.write("---")
        b1, b2 = st.columns(2)
        if b1.button("الصفحة التالية"): st.session_state.p_idx += 1; st.rerun()
        if b2.button("الصفحة السابقة"): st.session_state.p_idx -= 1; st.rerun()

    elif menu == "المطورين":
        st.markdown("<h2 style='color:#f59e0b;'>🏢 دليل المطورين</h2>", unsafe_allow_html=True)
        s_d = st.text_input("🔍 بحث عن شركة...")
        dff_d = df_d.copy()
        
        limit_d = 6
        total_d_p = math.ceil(len(dff_d) / limit_d)
        curr_d = dff_d.iloc[st.session_state.d_idx*limit_d : (st.session_state.d_idx+1)*limit_d]

        for i in range(0, len(curr_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(curr_d):
                    row = curr_d.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class='grid-card'>
                                <h3 style='color:#f59e0b; margin-top:0;'>{row.get('Developer')}</h3>
                                <p>👤 <b>المالك:</b> {row.get('Owner')}</p>
                                <p style='font-size:13px; color:#aaa;'>{row.get('Competitive Advantage')[:80]}...</p>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("📖 سابقة الأعمال"):
                            st.write(row.get('Detailed_Info'))

    elif menu == "الأدوات":
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ الأدوات الذكية</h2>", unsafe_allow_html=True)
        t1, t2, t3, t4, t5, t6 = st.tabs(["🧮 أقساط", "📈 عمولة", "📐 مساحة", "💰 عائد", "🏠 فائدة", "📝 نوت"])
        # (أكواد الأدوات كما هي لضمان استقرار العمليات الحسابية)
        with t1: p = st.number_input("السعر", 1000000); d = st.number_input("المقدم", p*0.1); y = st.slider("السنين", 1, 15, 8); st.metric("قسط", f"{(p-d)/(y*12):,.0f}")
        with t2: r = st.number_input("النسبة %", 1.5); st.metric("عمولة", f"{p*(r/100):,.0f}")
        with t3: sq = st.number_input("المتر", 100.0); st.write(f"قدم: {sq*10.76:,.2f}")
        with t4: rent = st.number_input("الإيجار", 10000); st.metric("ROI", f"{(rent*12/p)*100:.2f}%")
        with t5: f = st.slider("الفائدة %", 1, 30, 20); st.write(f"الإجمالي: {p*(1+(f/100)*y):,.0f}")
        with t6: st.text_area("نوت..."); st.button("حفظ")
