import streamlit as st
import pandas as pd
import math
import feedparser
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = 'Arabic'
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0

# 3. جلب الأخبار (بطيئة جداً جداً)
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "جاري تحديث أخبار السوق العقاري..."
    except: return "سوق العقارات المصري: متابعة مستمرة لأحدث الفرص."

news_text = get_real_news()

# 4. التنسيق (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    /* الهيدر */
    .header-bar {{ display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; background: #000; border-bottom: 1px solid #222; }}
    .oval-header {{ background-color: #000; border: 3px solid #f59e0b; border-radius: 50px; padding: 10px 30px; margin: 10px auto; text-align: center; width: fit-content; }}
    .header-title {{ color: #f59e0b; font-weight: 900; font-size: 24px !important; margin: 0; }}
    
    /* شريط الأخبار */
    .ticker-wrap {{ width: 100%; background: #111; border-bottom: 2px solid #f59e0b; padding: 8px 0; overflow: hidden; white-space: nowrap; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #fff; font-size: 14px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    
    /* الكروت والشبكة */
    .grid-card {{ background: #161616; border: 1px solid #222; border-top: 4px solid #f59e0b; border-radius: 12px; padding: 15px; min-height: 180px; margin-bottom: 15px; transition: 0.3s; }}
    .grid-card:hover {{ border-color: #f59e0b; transform: translateY(-5px); }}
    
    /* الأزرار */
    .stButton button {{ background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; border-radius: 8px !important; width: 100%; font-weight: bold; }}
    .logout-btn button {{ background-color: #7f1d1d !important; color: white !important; border: none !important; }}
    </style>
""", unsafe_allow_html=True)

# 5. تحميل البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        df_p = pd.read_csv(u_p).fillna("غير متوفر").astype(str)
        df_d = pd.read_csv(u_d).fillna("غير متوفر").astype(str)
        df_p.columns = df_p.columns.str.strip()
        df_d.columns = df_d.columns.str.strip()
        return df_p, df_d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 6. نظام الدخول
if not st.session_state.auth:
    st.markdown('<div class="oval-header"><h1 class="header-title">Ma3lomati PRO</h1></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if st.text_input("كلمة المرور", type="password") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# --- الهيدر العلوي (زر الخروج واللغة) ---
h_col1, h_col2, h_col3 = st.columns([1, 2, 1])
with h_col1:
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("🚪 خروج"): 
        st.session_state.auth = False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with h_col3:
    if st.button("🌐 English"): st.session_state.lang = 'English'

st.markdown('<div class="oval-header"><h1 class="header-title">منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
st.markdown(f'<div class="ticker-wrap"><div class="ticker"><b>🚀 أخبار السوق الآن:</b> {news_text}</div></div>', unsafe_allow_html=True)

# المنيو الرئيسي
menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], icons=["tools", "building", "person-vcard"], orientation="horizontal")

main_col, _ = st.columns([0.85, 0.15])

with main_col:
    # --- 🏗️ قسم المشاريع (شبكة وأزرار تالي وسابق) ---
    if menu == "المشاريع":
        st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
        s_p = st.text_input("🔍 ابحث عن مشروع...")
        dff_p = df_p.copy()
        if s_p: dff_p = dff_p[dff_p['Project Name'].str.contains(s_p, case=False)]
        
        limit = 6
        total_pages = math.ceil(len(dff_p) / limit)
        curr_page = dff_p.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]

        for i in range(0, len(curr_page), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(curr_page):
                    row = curr_page.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h3>{row.get('Project Name')}</h3><p>📍 {row.get('Area')}</p><p>🏢 {row.get('Developer')}</p></div>", unsafe_allow_html=True)
                        with st.expander("🔎 التفاصيل"):
                            st.write(f"📐 المساحة: {row.get('Project Area')}")
                            st.info(f"✅ المميزات: {row.get('Project Features')}")
        
        st.write("---")
        b1, b2 = st.columns(2)
        if b1.button("التالي ⬅️") and st.session_state.p_idx < total_pages-1: st.session_state.p_idx += 1; st.rerun()
        if b2.button("➡️ السابق") and st.session_state.p_idx > 0: st.session_state.p_idx -= 1; st.rerun()

    # --- 🏢 قسم المطورين (شبكة وأزرار تالي وسابق) ---
    elif menu == "المطورين":
        st.markdown("<h2 style='color:#f59e0b;'>🏢 شبكة المطورين</h2>", unsafe_allow_html=True)
        s_d = st.text_input("🔍 بحث عن شركة...")
        dff_d = df_d.copy()
        name_col = next((c for c in dff_d.columns if 'Name' in c or 'Developer' in c), dff_d.columns[0])
        if s_d: dff_d = dff_d[dff_d[name_col].str.contains(s_d, case=False)]

        limit_d = 6
        total_p_d = math.ceil(len(dff_d) / limit_d)
        curr_d = dff_d.iloc[st.session_state.d_idx*limit_d : (st.session_state.d_idx+1)*limit_d]

        for i in range(0, len(curr_d), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(curr_d):
                    row = curr_d.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h3>{row[name_col]}</h3><p>👤 المالك: {row.get('Owner')}</p></div>", unsafe_allow_html=True)
                        with st.expander("📖 التاريخ وسابقة الأعمال"):
                            st.warning(f"⏳ التاريخ: {row.get('History')}")
                            st.success(f"🏗️ سابقة الأعمال: {row.get('Previous Work')}")
        
        st.write("---")
        db1, db2 = st.columns(2)
        if db1.button("المطور التالي ⬅️") and st.session_state.d_idx < total_p_d-1: st.session_state.d_idx += 1; st.rerun()
        if db2.button("➡️ المطور السابق") and st.session_state.d_idx > 0: st.session_state.d_idx -= 1; st.rerun()

    # --- 🛠️ 6 أدوات بروكر كاملة ---
    elif menu == "الأدوات":
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ الأدوات الاحترافية</h2>", unsafe_allow_html=True)
        t1, t2, t3, t4, t5, t6 = st.tabs(["🧮 الأقساط", "📈 العمولة", "📐 المساحة", "💰 العائد", "🏠 الفائدة", "📝 الملاحظات"])
        
        with t1:
            p = st.number_input("سعر الوحدة", 1000000)
            d = st.number_input("المقدم", p*0.1)
            y = st.slider("السنين", 1, 15, 8)
            st.metric("القسط الشهري", f"{(p-d)/(y*12):,.0f} ج.م")
        with t2:
            r = st.number_input("النسبة %", 1.5)
            st.metric("العمولة", f"{p*(r/100):,.0f} ج.م")
        with t3:
            sq = st.number_input("المتر", 100.0)
            st.write(f"قدم مربع: {sq*10.76:,.2f}")
        with t4:
            rent = st.number_input("الإيجار", 10000)
            st.metric("ROI سنوي", f"{(rent*12/p)*100:.2f}%")
        with t5:
            f = st.slider("الفائدة %", 1, 30, 20)
            st.write(f"الإجمالي بالفوائد: {p*(1+(f/100)*y):,.0f}")
        with t6:
            st.text_area("ملاحظات مكالمة العميل...")
            st.button("حفظ الملاحظة")
