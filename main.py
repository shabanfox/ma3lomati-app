import streamlit as st
import pandas as pd
import math
import feedparser
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0

# 3. جلب الأخبار (أبطأ سرعة ممكنة 180 ثانية)
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "جاري تحديث أخبار السوق..."
    except: return "سوق العقارات المصري: متابعة مستمرة لأحدث المشروعات."

news_text = get_real_news()

# 4. التنسيق (CSS) - العودة لتصميم الـ 70% والشبكة الاحترافية
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    .oval-header {{ background-color: #000; border: 3px solid #f59e0b; border-radius: 50px; padding: 10px 30px; margin: 10px auto; text-align: center; width: fit-content; }}
    .header-title {{ color: #f59e0b; font-weight: 900; font-size: 24px !important; margin: 0; }}
    
    .ticker-wrap {{ width: 100%; background: #111; border-bottom: 2px solid #f59e0b; padding: 8px 0; overflow: hidden; white-space: nowrap; }}
    .ticker {{ display: inline-block; animation: ticker 180s linear infinite; color: #fff; font-size: 14px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    
    .grid-card {{ background: #161616; border: 1px solid #222; border-top: 4px solid #f59e0b; border-radius: 12px; padding: 15px; min-height: 200px; margin-bottom: 15px; }}
    .logout-btn button {{ background-color: #7f1d1d !important; color: white !important; border: none !important; border-radius: 20px !important; }}
    .stButton button {{ background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; border-radius: 8px !important; }}
    </style>
""", unsafe_allow_html=True)

# 5. جلب البيانات من الشيتين
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

# 6. نظام الدخول
if not st.session_state.auth:
    st.markdown('<div class="oval-header"><h1 class="header-title">Ma3lomati PRO</h1></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        if st.text_input("كلمة المرور", type="password") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# الهيدر وزر الخروج
top_col1, top_col2 = st.columns([0.15, 0.85])
with top_col1:
    if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()

st.markdown('<div class="oval-header"><h1 class="header-title">منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
st.markdown(f'<div class="ticker-wrap"><div class="ticker"><b>🚀 أخبار السوق الآن:</b> {news_text}</div></div>', unsafe_allow_html=True)

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], icons=["tools", "building", "person-vcard"], orientation="horizontal")

# --- تقسيم الشاشة 70% للمحتوى الرئيسي ---
main_col, side_spacer = st.columns([0.7, 0.3])

with main_col:
    if menu == "المشاريع":
        st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع التفصيلي</h2>", unsafe_allow_html=True)
        s_p = st.text_input("🔍 ابحث عن مشروع...")
        dff_p = df_p.copy()
        if s_p: dff_p = dff_p[dff_p['Project Name'].str.contains(s_p, case=False)]
        
        limit = 6
        total_p = math.ceil(len(dff_p) / limit)
        curr_page = dff_p.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]

        for i in range(0, len(curr_page), 2): # عرض 2 في الصف لمساحة الـ 70%
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(curr_page):
                    row = curr_page.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class='grid-card'>
                                <h3 style='color:#f59e0b;'>{row.get('Project Name')}</h3>
                                <p>📍 <b>الموقع:</b> {row.get('Area')}</p>
                                <p>📐 <b>المساحة:</b> {row.get('Project Area')}</p>
                                <p>🏢 <b>المطور:</b> {row.get('Developer')}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("🔎 كامل التفاصيل"):
                            st.info(f"✅ المميزات: {row.get('Project Features')}")
                            st.error(f"⚠️ العيوب: {row.get('Project Flaws')}")
        
        st.write("---")
        b1, b2 = st.columns(2)
        if b1.button("الصفحة التالية ⬅️"): st.session_state.p_idx += 1; st.rerun()
        if b2.button("➡️ الصفحة السابقة"): st.session_state.p_idx -= 1; st.rerun()

    elif menu == "المطورين":
        st.markdown("<h2 style='color:#f59e0b;'>🏢 شبكة المطورين</h2>", unsafe_allow_html=True)
        s_d = st.text_input("🔍 ابحث عن المطور...")
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
                                <h3 style='color:#f59e0b;'>{row.get('Developer')}</h3>
                                <p>👤 <b>المالك:</b> {row.get('Owner')}</p>
                                <p style='font-size:13px;'>{row.get('Competitive Advantage')[:60]}...</p>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("📖 سابقة الأعمال والتاريخ"):
                            st.success(f"ℹ️ تفاصيل: {row.get('Detailed_Info')}")
        
        st.write("---")
        db1, db2 = st.columns(2)
        if db1.button("المطور التالي ⬅️"): st.session_state.d_idx += 1; st.rerun()
        if db2.button("➡️ المطور السابق"): st.session_state.d_idx -= 1; st.rerun()

    elif menu == "الأدوات":
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ 6 أدوات بروكر</h2>", unsafe_allow_html=True)
        t1, t2, t3, t4, t5, t6 = st.tabs(["🧮 الأقساط", "📈 العمولة", "📐 المساحات", "💰 ROI", "🏠 الفائدة", "📝 نوت"])
        with t1:
            p = st.number_input("السعر", 1000000); d = st.number_input("المقدم", p*0.1); y = st.slider("السنين", 1, 15, 8)
            st.metric("قسط شهري", f"{(p-d)/(y*12):,.0f} ج.م")
        with t2: r = st.number_input("النسبة %", 1.5); st.metric("العمولة", f"{p*(r/100):,.0f} ج.م")
        with t3: sq = st.number_input("المساحة بالمتر", 100.0); st.write(f"القدم المربع: {sq*10.76:,.2f}")
        with t4: rent = st.number_input("الإيجار", 10000); st.metric("ROI", f"{(rent*12/p)*100:.2f}%")
        with t5: f = st.slider("الفائدة %", 1, 30, 20); st.write(f"الإجمالي بالفائدة: {p*(1+(f/100)*y):,.0f}")
        with t6: st.text_area("ملاحظات العميل...")
