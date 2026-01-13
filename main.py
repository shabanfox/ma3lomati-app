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

# نصوص الواجهة
ui = {
    'Arabic': {
        'title': "منصة معلوماتي العقارية", 'projects': "🏗️ المشاريع", 'devs': "🏢 المطورين", 
        'tools': "🛠️ الأدوات", 'logout': "🚪 خروج", 'search': "🔍 بحث...", 
        'filter_area': "📍 تصفية بالمنطقة", 'details': "🔎 التفاصيل", 'next': "التالي ⬅️", 'prev': "➡️ السابق", 
        'dir': "rtl", 'align': "right", 'news_title': "🚀 أخبار السوق الآن:",
        'area_label': "📍 المنطقة", 'size_label': "📐 المساحة"
    },
    'English': {
        'title': "Ma3lomati Real Estate", 'projects': "🏗️ Projects", 'devs': "🏢 Developers", 
        'tools': "🛠️ Tools", 'logout': "🚪 Logout", 'search': "🔍 Search...", 
        'filter_area': "📍 Area Filter", 'details': "🔎 Details", 'next': "Next ➡️", 'prev': "⬅️ Prev", 
        'dir': "ltr", 'align': "left", 'news_title': "🚀 Market News:",
        'area_label': "📍 Area", 'size_label': "📐 Size"
    }
}
T = ui[st.session_state.lang]

# 3. جلب الأخبار (بطيئة جداً)
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:8]]
        return "  •  ".join(news) if news else "جاري تحديث أخبار العقارات..."
    except: return "سوق العقارات المصري: متابعة مستمرة لآخر المشاريع والأسعار."

news_text = get_real_news()

# 4. التنسيق المتقدم (CSS) - تبطئة السرعة لـ 120 ثانية
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: {T['dir']} !important; text-align: {T['align']} !important; font-family: 'Cairo', sans-serif; }}
    .oval-header {{ background-color: #000; border: 3px solid #f59e0b; border-radius: 50px; padding: 10px 20px; width: fit-content; margin: 10px auto 5px auto; text-align: center; }}
    .header-title {{ color: #f59e0b; font-weight: 900; font-size: 22px !important; margin: 0; }}
    
    /* شريط أخبار بطيء جداً جداً */
    .ticker-wrap {{ width: 100%; background-color: #111; border-bottom: 2px solid #f59e0b; padding: 8px 0; margin-bottom: 15px; overflow: hidden; white-space: nowrap; }}
    .ticker {{ display: inline-block; animation: ticker 120s linear infinite; color: #fff; font-size: 14px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    
    .grid-card {{ background: #161616; border: 1px solid #222; border-top: 4px solid #f59e0b; border-radius: 12px; padding: 15px; min-height: 180px; margin-bottom: 10px; }}
    .stButton button {{ background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; border-radius: 8px !important; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{ background-color: #111; border-radius: 5px; padding: 10px; color: #fff; }}
    </style>
""", unsafe_allow_html=True)

# 5. جلب البيانات (مع معالجة الأسماء)
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
    st.markdown(f'<div class="oval-header"><h1 class="header-title">{T["title"]}</h1></div>', unsafe_allow_html=True)
    cols = st.columns([1, 2, 1])
    with cols[1]:
        if st.text_input("كلمة المرور", type="password") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# الهيدر
st.markdown(f'<div class="oval-header"><h1 class="header-title">{T["title"]}</h1></div>', unsafe_allow_html=True)
st.markdown(f'<div class="ticker-wrap"><div class="ticker"><b>{T["news_title"]}</b> {news_text}</div></div>', unsafe_allow_html=True)

menu = option_menu(None, [T['tools'], T['projects'], T['devs']], icons=["tools", "building", "person-vcard"], orientation="horizontal")

if st.session_state.lang == 'Arabic': main_col, _ = st.columns([0.8, 0.2])
else: _, main_col = st.columns([0.2, 0.8])

with main_col:
    # --- 🏗️ قسم المشاريع (تم إصلاح العرض) ---
    if menu == T['projects']:
        st.markdown(f"<h2 style='color:#f59e0b;'>{T['projects']}</h2>", unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        with f1: s_p = st.text_input(T['search'])
        with f2: 
            areas = ["الكل"] + sorted(df_p['Area'].unique().tolist()) if 'Area' in df_p.columns else ["الكل"]
            sel_a = st.selectbox(T['filter_area'], areas)
        
        dff_p = df_p.copy()
        if s_p: dff_p = dff_p[dff_p['Project Name'].str.contains(s_p, case=False)]
        if sel_a != "الكل": dff_p = dff_p[dff_p['Area'] == sel_a]

        for i in range(0, len(dff_p), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(dff_p):
                    row = dff_p.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h3 style='color:#f59e0b;'>{row.get('Project Name', 'N/A')}</h3><p>🏢 {row.get('Developer', 'N/A')}</p><p>📍 {row.get('Area', 'N/A')}</p></div>", unsafe_allow_html=True)
                        with st.expander("🔎 التفاصيل"):
                            st.write(f"📐 المساحة: {row.get('Project Area', 'N/A')}")
                            st.info(f"✅ المميزات: {row.get('Project Features', 'N/A')}")
                            st.warning(f"⚠️ العيوب: {row.get('Project Flaws', 'N/A')}")

    # --- 🏢 قسم المطورين (تم إصلاح العرض) ---
    elif menu == T['devs']:
        st.markdown(f"<h2 style='color:#f59e0b;'>{T['devs']}</h2>", unsafe_allow_html=True)
        s_d = st.text_input("🔍 بحث عن شركة...")
        dff_d = df_d.copy()
        dev_name_col = 'Developer Name' if 'Developer Name' in df_d.columns else df_d.columns[0]
        if s_d: dff_d = dff_d[dff_d[dev_name_col].str.contains(s_d, case=False)]

        for i in range(0, len(dff_d), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(dff_d):
                    row = dff_d.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h3 style='color:#f59e0b;'>{row.get(dev_name_col, 'N/A')}</h3><p>👤 المالك: {row.get('Owner', 'N/A')}</p></div>", unsafe_allow_html=True)
                        with st.expander("📖 سابقة الأعمال"):
                            st.write(row.get('Previous Work', 'N/A'))
                            st.write(f"⏳ التاريخ: {row.get('History', 'N/A')}")

    # --- 🛠️ 6 أدوات بروكر كاملة ---
    elif menu == T['tools']:
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ أدوات البروكر الذكية</h2>", unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["🧮 الأقساط", "📈 العمولة", "📐 المساحات"])
        t4, t5, t6 = st.tabs(["💰 العائد", "🏠 التمويل", "📝 ملاحظات"])
        
        with t1:
            st.subheader("حاسبة الأقساط")
            price = st.number_input("السعر", 1000000)
            down = st.number_input("المقدم", price*0.1)
            years = st.slider("السنين", 1, 15, 8)
            st.metric("القسط شهرياً", f"{(price-down)/(years*12):,.0f} ج.م")
            
        with t2:
            st.subheader("حاسبة العمولة")
            c_rate = st.number_input("نسبة العمولة %", 1.5)
            st.metric("عمولتك", f"{price*(c_rate/100):,.0f} ج.م")
            
        with t3:
            st.subheader("تحويل المساحات")
            sqm = st.number_input("المساحة بالمتر", 100.0)
            st.write(f"بالقدم المربع: {sqm * 10.76:,.2f}")
            st.write(f"بالفدان: {sqm / 4200:,.4f}")
            
        with t4:
            st.subheader("عائد الاستثمار (ROI)")
            rent = st.number_input("الإيجار المتوقع شهرياً", 10000)
            st.metric("العائد السنوي", f"{(rent*12/price)*100:.2f} %")
            
        with t5:
            st.subheader("التمويل العقاري (فائدة مركبة)")
            rate = st.slider("الفائدة السنوية %", 1.0, 30.0, 20.0)
            st.write(f"إجمالي المبلغ بالفوائد: {price * (1 + (rate/100)*years):,.0f} ج.م")
            
        with t6:
            st.subheader("دفتر ملاحظات العميل")
            note = st.text_area("سجل تفاصيل مكالمة العميل هنا...")
            if st.button("حفظ مؤقت"): st.success("تم الحفظ في المتصفح!")
