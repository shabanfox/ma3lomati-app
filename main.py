import streamlit as st
import pandas as pd
import math
import feedparser
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (اللغة والدخول)
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

# 3. وظيفة جلب الأخبار الحقيقية (تلقائي)
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:8]]
        return "  •  ".join(news) if news else "جاري تحديث أخبار العقارات..."
    except:
        return "سوق العقارات المصري: متابعة مستمرة لآخر المشاريع والأسعار."

news_text = get_real_news()

# 4. التنسيق المتقدم (CSS) - تم تبطئة الأنيميشن هنا
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: {T['dir']} !important; text-align: {T['align']} !important; font-family: 'Cairo', sans-serif; }}
    
    .oval-header {{ background-color: #000; border: 3px solid #f59e0b; border-radius: 50px; padding: 10px 20px; width: fit-content; margin: 10px auto 5px auto; text-align: center; box-shadow: 0px 4px 15px rgba(245, 158, 11, 0.3); }}
    .header-title {{ color: #f59e0b; font-weight: 900; font-size: 22px !important; margin: 0; }}
    
    /* شريط الأخبار ببطء شديد */
    .ticker-wrap {{ width: 100%; background-color: #111; border-bottom: 2px solid #f59e0b; padding: 8px 0; margin-bottom: 15px; overflow: hidden; white-space: nowrap; }}
    .ticker {{ display: inline-block; animation: ticker 80s linear infinite; color: #fff; font-size: 14px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    
    .grid-card {{ background: #161616; border: 1px solid #222; border-top: 4px solid #f59e0b; border-radius: 12px; padding: 15px; min-height: 150px; margin-bottom: 10px; transition: 0.3s; }}
    .grid-card:hover {{ transform: translateY(-3px); border-color: #f59e0b; }}
    .filter-box {{ background: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #333; margin-bottom: 20px; }}
    .stButton button {{ background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; width: 100% !important; border-radius: 8px !important; }}
    </style>
""", unsafe_allow_html=True)

# 5. جلب البيانات وحذف التكرار
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        df_p = pd.read_csv(u_p).drop_duplicates(subset=['Project Name']).fillna("").astype(str)
        df_d = pd.read_csv(u_d).drop_duplicates(subset=['Developer Name']).fillna("").astype(str)
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
        pwd = st.text_input("Passcode", type="password")
        if st.button("دخول للنظام"):
            if pwd == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# أدوات التحكم العليا
c_l, c_r = st.columns([1, 1])
with c_l: 
    if st.button(T['logout']): st.session_state.auth = False; st.rerun()
with c_r:
    if st.button("🌐 Switch Language (AR/EN)"): 
        st.session_state.lang = 'English' if st.session_state.lang == 'Arabic' else 'Arabic'
        st.rerun()

# الهيدر والشريط الإخباري المبطأ
st.markdown(f'<div class="oval-header"><h1 class="header-title">{T["title"]}</h1></div>', unsafe_allow_html=True)
st.markdown(f'<div class="ticker-wrap"><div class="ticker"><b>{T["news_title"]}</b> {news_text} &nbsp;&nbsp;&nbsp;&nbsp; <b>{T["news_title"]}</b> {news_text}</div></div>', unsafe_allow_html=True)

# المنيو الرئيسي
menu = option_menu(None, [T['tools'], T['projects'], T['devs']], icons=["tools", "building", "person-vcard"], orientation="horizontal")

# تقسيم المساحة (Main & Sidebar placeholder)
if st.session_state.lang == 'Arabic': main_col, _ = st.columns([0.75, 0.25])
else: _, main_col = st.columns([0.25, 0.75])

with main_col:
    # --- 🏗️ قسم المشاريع ---
    if menu == T['projects']:
        st.markdown(f"<h2 style='color:#f59e0b;'>{T['projects']}</h2>", unsafe_allow_html=True)
        st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        with f1: s_p = st.text_input(T['search'], placeholder="اسم المشروع...")
        with f2: 
            areas = ["الكل"] + sorted(df_p['Area'].unique().tolist()) if 'Area' in df_p.columns else ["الكل"]
            sel_a = st.selectbox(T['filter_area'], areas)
        st.markdown("</div>", unsafe_allow_html=True)

        dff_p = df_p.copy()
        if s_p: dff_p = dff_p[dff_p['Project Name'].str.contains(s_p, case=False)]
        if sel_a != "الكل": dff_p = dff_p[dff_p['Area'] == sel_a]

        grid_limit = 9
        if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
        total_p = math.ceil(len(dff_p) / grid_limit)
        curr_p = dff_p.iloc[st.session_state.p_idx*grid_limit : (st.session_state.p_idx+1)*grid_limit]

        for i in range(0, len(curr_p), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(curr_p):
                    row = curr_p.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h3 style='color:#f59e0b; font-size:16px;'>{row.get('Project Name', 'N/A')}</h3><p style='font-size:13px;'>🏢 {row.get('Developer', 'N/A')}</p></div>", unsafe_allow_html=True)
                        with st.expander(T['details']):
                            st.write(f"**{T['area_label']}:** {row.get('Area', 'N/A')}")
                            st.write(f"**{T['size_label']}:** {row.get('Project Area', 'N/A')}")
                            st.divider()
                            st.write(f"👷 **الاستشاري:** {row.get('Consultant', 'N/A')}")
                            st.info(f"✅ **المميزات:** {row.get('Project Features', 'N/A')}")
                            st.warning(f"⚠️ **العيوب:** {row.get('Project Flaws', 'N/A')}")
        
        st.write("---")
        b1, b2, _ = st.columns([0.2, 0.2, 0.6])
        if b1.button(T['next']) and st.session_state.p_idx < total_p-1: st.session_state.p_idx += 1; st.rerun()
        if b2.button(T['prev']) and st.session_state.p_idx > 0: st.session_state.p_idx -= 1; st.rerun()

    # --- 🏢 قسم المطورين ---
    elif menu == T['devs']:
        st.markdown(f"<h2 style='color:#f59e0b;'>{T['devs']}</h2>", unsafe_allow_html=True)
        s_d = st.text_input("🔍 بحث عن مطور...", placeholder="اسم الشركة...")
        dff_d = df_d.copy()
        dev_col = 'Developer Name' if 'Developer Name' in dff_d.columns else 'Developer'
        if s_d and dev_col in dff_d.columns: dff_d = dff_d[dff_d[dev_col].str.contains(s_d, case=False)]

        for i in range(0, len(dff_d), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(dff_d):
                    row = dff_d.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h4 style='color:#f59e0b;'>{row.get(dev_col, 'N/A')}</h4><p>👤 المالك: {row.get('Owner', 'N/A')}</p></div>", unsafe_allow_html=True)
                        with st.expander("📖 تفاصيل المطور الكاملة"):
                            st.markdown("⏳ **History (تاريخ الشركة)**")
                            st.write(row.get('History', 'N/A'))
                            st.divider()
                            st.markdown("🏗️ **Previous Work (سابقة الأعمال)**")
                            st.write(row.get('Previous Work', 'N/A'))
                            st.divider()
                            st.markdown("ℹ️ **معلومات إضافية**")
                            st.write(row.get('Detailed_Info', 'N/A'))

    # --- 🛠️ كل أدوات البروكر ---
    elif menu == T['tools']:
        st.markdown(f"<h2 style='color:#f59e0b;'>{T['tools']}</h2>", unsafe_allow_html=True)
        tool_tab1, tool_tab2 = st.tabs(["🧮 حاسبة الأقساط", "📈 حاسبة العمولة"])
        
        with tool_tab1:
            st.markdown("### حساب القسط الشهري")
            price = st.number_input("سعر الوحدة الإجمالي", 1000000, step=100000)
            down = st.number_input("المقدم المدفوع", 0, step=50000)
            years = st.slider("عدد سنوات التقسيط", 1, 15, 8)
            remaining = price - down
            monthly = remaining / (years * 12)
            st.metric("المبلغ المتبقي", f"{remaining:,.0f} ج.م")
            st.success(f"قيمة القسط الشهري: {monthly:,.0f} ج.م")

        with tool_tab2:
            st.markdown("### حساب العمولة التقديرية")
            comm_rate = st.number_input("نسبة العمولة (%)", 1.0, 10.0, 1.5)
            total_comm = price * (comm_rate / 100)
            st.info(f"عمولتك المتوقعة: {total_comm:,.0f} ج.م")
