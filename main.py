import streamlit as st
import pandas as pd
import feedparser
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (Session State)
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

# 4. التنسيق الجمالي (CSS الموحد)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    /* الهيدر الذهبي */
    .luxury-header {{
        background: rgba(15, 15, 15, 0.9); backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b; padding: 15px 30px;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; border-radius: 0 0 25px 25px; margin-bottom: 15px;
    }}
    .logo-text {{ color: #f59e0b; font-weight: 900; font-size: 24px; }}
    
    /* شريط الأخبار المتحرك */
    .ticker-wrap {{ width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 10px; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* ستايل كروت المشاريع */
    div.stButton > button[key*="card_"] {{
        background-color: white !important;
        color: #111 !important;
        border: 1px solid #eee !important;
        border-radius: 15px !important;
        width: 100% !important;
        min-height: 250px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: flex-start !important;
        padding: 20px !important;
        transition: 0.3s !important;
        text-align: right !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        white-space: pre-wrap !important;
        line-height: 1.6 !important;
    }}
    div.stButton > button[key*="card_"]:hover {{
        border-color: #f59e0b !important;
        transform: translateY(-5px) !important;
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.2) !important;
    }}

    /* حاوية استلام فوري الجانبية */
    .ready-sidebar-container {{
        background: #0d0d0d; border: 1px solid #222; border-radius: 15px; padding: 12px;
        max-height: 80vh; overflow-y: auto; border-top: 3px solid #10b981;
    }}
    .ready-card {{ background: #161616; border-right: 3px solid #10b981; padding: 10px; border-radius: 8px; margin-bottom: 8px; }}
    .ready-title {{ color: #f59e0b; font-size: 14px; font-weight: bold; }}

    /* تفاصيل الموقع التفصيلية */
    .detail-loc-box {{
        background: #1a1a1a; padding: 15px; border-radius: 10px; border-right: 4px solid #f59e0b; margin: 15px 0;
    }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        if st.text_input("Passcode", type="password") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# 6. جلب البيانات من Google Sheets
@st.cache_data(ttl=60)
def load_all_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("غير متوفر").astype(str)
        d = pd.read_csv(u_d).fillna("غير متوفر").astype(str)
        return p, d
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")
        return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_all_data()

# بناء الهيدر والتيكر
now = datetime.now().strftime("%H:%M")
st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI <span style="color:white; font-size:14px;">PRO</span></div><div style="color:#aaa; font-size:12px; text-align:left;">📅 {datetime.now().strftime("%Y-%m-%d")} | {now}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], 
    default_index=1, orientation="horizontal",
    styles={"container": {"background-color": "#0a0a0a", "padding": "0"}, "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}}
)

# تقسيم الصفحة الرئيسية
main_col, side_col = st.columns([0.75, 0.25])

# --- الجانب الأيمن (استلام فوري) ---
with side_col:
    st.markdown("<p style='color:#10b981; text-align:center; font-weight:bold; font-size:15px;'>🔑 استلام فوري فقط</p>", unsafe_allow_html=True)
    st.markdown("<div class='ready-sidebar-container'>", unsafe_allow_html=True)
    if not df_p.empty:
        ready_items = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
        for _, row in ready_items.head(15).iterrows():
            st.markdown(f'<div class="ready-card"><div class="ready-title">{row.get("Project Name")}</div><div style="color:#888; font-size:11px;">📍 {row.get("Area")}</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- الجانب الأيسر (المحتوى الرئيسي) ---
with main_col:
    if st.session_state.selected_item is not None:
        item = st.session_state.selected_item
        if st.button("⬅️ عودة للقائمة", key="back"):
            st.session_state.selected_item = None; st.rerun()
        
        # صفحة تفاصيل المشروع المحدثة
        st.markdown(f"""
            <div style="background:#111; padding:30px; border-radius:15px; border-right:5px solid #f59e0b; color:white;">
                <h1 style="color:#f59e0b; margin-bottom:5px;">{item.get('Project Name', item.get('Developer'))}</h1>
                <h4 style="color:#aaa; margin-bottom:20px;">📍 {item.get('Area', '')}</h4>
                <hr style="opacity:0.1;">
                
                <div class="detail-loc-box">
                    <span style="color:#f59e0b; font-weight:bold; display:block; margin-bottom:5px;">📍 الموقع بالتفصيل:</span>
                    <span style="font-size:16px;">{item.get('Detailed Location', 'العنوان مسجل في الدفاتر الفنية.')}</span>
                </div>

                <div style="margin-top:25px; font-size:17px; line-height:1.8;">
                    <h4 style="color:#f59e0b;">🏗️ بيانات المطور:</h4>
                    <p>{item.get('Developer', 'غير مسجل')}</p>
                    <h4 style="color:#f59e0b; margin-top:20px;">✨ تفاصيل ومميزات إضافية:</h4>
                    <p>{item.get('Project Features', item.get('Detailed_Info', 'تواصل مع الإدارة للحصول على البروشور الكامل.'))}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    elif menu == "المشاريع":
        # قسم الفلاتر
        st.markdown("<h3 style='color:#f59e0b;'>🔍 فلاتر البحث الذكية</h3>", unsafe_allow_html=True)
        f1, f2, f3 = st.columns(3)
        
        with f1:
            areas = ["الكل"] + sorted(df_p['Area'].unique().tolist())
            s_area = st.selectbox("المنطقة", areas)
        with f2:
            devs = ["الكل"] + sorted(df_p['Developer'].unique().tolist())
            s_dev = st.selectbox("المطور العقاري", devs)
        with f3:
            s_name = st.text_input("اسم المشروع...")

        # تطبيق الفلترة
        dff_p = df_p.copy()
        if s_area != "الكل": dff_p = dff_p[dff_p['Area'] == s_area]
        if s_dev != "الكل": dff_p = dff_p[dff_p['Developer'] == s_dev]
        if s_name: dff_p = dff_p[dff_p['Project Name'].str.contains(s_name, case=False)]

        st.markdown(f"<p style='color:#aaa;'>نتائج البحث: {len(dff_p)} مشروع</p>", unsafe_allow_html=True)

        # عرض الكروت
        limit = 6
        curr_page = dff_p.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]

        for i in range(0, len(curr_page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(curr_page):
                    row = curr_page.iloc[i+j]
                    with cols[j]:
                        # كارت المشروع مع الموقع التفصيلي
                        label = (
                            f"🏢 {row.get('Project Name')}\n"
                            f"📍 {row.get('Area')}\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"🏗️ المطور: {row.get('Developer')}\n"
                            f"📍 الموقع: {row.get('Detailed Location')[:50]}...\n"
                            f"💰 عرض كامل التفاصيل"
                        )
                        if st.button(label, key=f"card_p_{i+j}"):
                            st.session_state.selected_item = row; st.rerun()

        # الترقيم
        if len(dff_p) > limit:
            st.markdown("---")
            cp1, cp2 = st.columns(2)
            if st.session_state.p_idx > 0:
                if cp1.button("⬅️ السابق"): st.session_state.p_idx -= 1; st.rerun()
            if (st.session_state.p_idx + 1) * limit < len(dff_p):
                if cp2.button("التالي ➡️"): st.session_state.p_idx += 1; st.rerun()

    elif menu == "المطورين":
        s_d = st.text_input("🔍 ابحث عن مطور عقاري...")
        dff_d = df_d.copy()
        if s_d: dff_d = dff_d[dff_d.apply(lambda r: r.astype(str).str.contains(s_d, case=False).any(), axis=1)]

        for i in range(0, len(dff_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(dff_d):
                    row = dff_d.iloc[i+j]
                    with cols[j]:
                        label = (
                            f"🏗️ {row.get('Developer')}\n"
                            f"⭐ الفئة: {row.get('Developer Category')}\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"👤 المالك: {row.get('Owner')}\n"
                            f"🏢 عدد المشاريع: {row.get('Number of Projects')}\n"
                            f"📖 عرض سابقة الأعمال"
                        )
                        if st.button(label, key=f"card_d_{i+j}"):
                            st.session_state.selected_item = row; st.rerun()

    elif menu == "الأدوات":
        st.markdown("<h3 style='color:#f59e0b;'>🛠️ الأدوات المساعدة</h3>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🧮 حاسبة القسط", "📐 محول المساحات"])
        with t1:
            price = st.number_input("السعر الإجمالي", 1000000); y = st.slider("سنوات التقسيط", 1, 15, 8)
            st.metric("القسط الشهري التقريبي", f"{price/(y*12):,.0f} ج.م")
        with t2:
            sq = st.number_input("المتر المربع", 100.0); st.write(f"القدم المربع: {sq*10.76:,.2f}")

# زر الخروج
st.sidebar.markdown("---")
if st.sidebar.button("🚪 خروج آمن"):
    st.session_state.auth = False; st.rerun()
