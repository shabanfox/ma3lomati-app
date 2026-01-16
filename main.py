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

# 4. التنسيق الجمالي (UI/UX)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    /* الهيدر الذهبي */
    .luxury-header {{
        background: rgba(15, 15, 15, 0.95); backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b; padding: 15px 30px;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; border-radius: 0 0 25px 25px; margin-bottom: 15px;
    }}
    .logo-text {{ color: #f59e0b; font-weight: 900; font-size: 26px; letter-spacing: 1px; }}
    
    /* شريط الأخبار */
    .ticker-wrap {{ width: 100%; background: transparent; padding: 8px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 15px; }}
    .ticker {{ display: inline-block; animation: ticker 120s linear infinite; color: #aaa; font-size: 14px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* الكروت الاحترافية (تصميم نوي) */
    div.stButton > button[key*="card_"] {{
        background: white !important;
        color: #1a1a1a !important;
        border: none !important;
        border-radius: 20px !important;
        width: 100% !important;
        min-height: 240px !important;
        padding: 25px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        text-align: right !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
        white-space: pre-wrap !important;
        line-height: 1.7 !important;
    }}
    div.stButton > button[key*="card_"]:hover {{
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 15px 30px rgba(245, 158, 11, 0.3) !important;
        background: #fdfdfd !important;
    }}

    /* الاستلام الفوري الجانبي */
    .ready-sidebar-container {{
        background: #0d0d0d; border: 1px solid #222; border-radius: 20px; padding: 15px;
        max-height: 75vh; overflow-y: auto; border-top: 4px solid #10b981;
    }}
    .ready-card {{ background: #161616; border-right: 4px solid #10b981; padding: 12px; border-radius: 10px; margin-bottom: 10px; transition: 0.3s; }}
    .ready-card:hover {{ background: #222; }}
    .ready-title {{ color: #f59e0b; font-size: 15px; font-weight: bold; margin-bottom: 4px; }}
    
    .info-label {{ color: #f59e0b; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# 5. نظام الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:120px;'><h1 style='color:#f59e0b; font-size:50px;'>MA3LOMATI <span style='color:white'>PRO</span></h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1.2,1])
    with c2:
        pin = st.text_input("Passcode", type="password", placeholder="أدخل رمز الدخول لعام 2026")
        if pin == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# بناء الواجهة العلوية
st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI <span style="color:white; font-size:14px;">PRO</span></div><div style="color:#aaa; font-size:12px; text-align:left;">📅 {datetime.now().strftime("%Y-%m-%d")} | {datetime.now().strftime("%H:%M")}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

# 6. جلب وتنظيف البيانات
@st.cache_data(ttl=300)
def load_and_clean_data(cache_val):
    u_p = f"https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv&cache={cache_val}"
    u_d = f"https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv&cache={cache_val}"
    try:
        p = pd.read_csv(u_p)
        d = pd.read_csv(u_d)
        def cleaner(df):
            df = df.fillna("قيد التحديث ⏳")
            return df.applymap(lambda x: "قيد التحديث ⏳" if str(x).strip().lower() in ['none', 'nan', '', 'null'] else x)
        return cleaner(p), cleaner(d)
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_and_clean_data(st.session_state.cache_key)

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], 
    default_index=1, orientation="horizontal",
    styles={
        "container": {"background-color": "#0a0a0a", "padding": "0", "border-radius": "0"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "color": "#aaa"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}
    }
)

# 7. توزيع الصفحة
main_col, side_col = st.columns([0.78, 0.22])

with side_col:
    st.markdown("<p style='color:#10b981; text-align:center; font-weight:900; font-size:18px; margin-bottom:10px;'>🔑 استلام فوري</p>", unsafe_allow_html=True)
    st.markdown("<div class='ready-sidebar-container'>", unsafe_allow_html=True)
    if not df_p.empty:
        ready_df = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
        for _, row in ready_df.head(15).iterrows():
            st.markdown(f'<div class="ready-card"><div class="ready-title">{row.get("Project Name")}</div><div style="color:#888; font-size:12px;">📍 {row.get("Area")}</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with main_col:
    # عرض صفحة التفاصيل
    if st.session_state.selected_item is not None:
        item = st.session_state.selected_item
        if st.button("⬅️ عودة للقائمة الرئيسية"):
            st.session_state.selected_item = None; st.rerun()
        
        st.markdown(f"""
            <div style="background:#111; padding:35px; border-radius:20px; border-right:6px solid #f59e0b; color:white; box-shadow: 0 20px 40px rgba(0,0,0,0.4);">
                <h1 style="color:#f59e0b; margin-bottom:5px; font-size:32px;">{item.get('Project Name', item.get('Developer'))}</h1>
                <p style="color:#888; font-size:18px;">{item.get('Area', 'معلومات المطور العقاري')}</p>
                <hr style="opacity:0.1; margin:20px 0;">
                <div style="font-size:19px; line-height:1.9; color:#e0e0e0;">
                    {item.get('Project Features', item.get('Detailed_Info', 'التفاصيل قيد المراجعة...'))}
                </div>
            </div>
        """, unsafe_allow_html=True)

    elif menu == "المشاريع":
        c1, c2, c3 = st.columns([1,1,0.3])
        s_p = c1.text_input("🔍 ابحث عن اسم المشروع أو المنطقة...")
        if c3.button("🔄", help="تحديث البيانات من جوجل"):
            st.cache_data.clear()
            st.session_state.cache_key = random.randint(1, 999999)
            st.rerun()

        dff_p = df_p.copy()
        if s_p: dff_p = dff_p[dff_p.apply(lambda r: r.astype(str).str.contains(s_p, case=False).any(), axis=1)]
        
        # عرض الكروت في شبكة (Grid)
        for i in range(0, len(dff_p), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(dff_p):
                    row = dff_p.iloc[i+j]
                    with cols[j]:
                        card_text = (
                            f"🏢 {row.get('Project Name')}\n"
                            f"📍 {row.get('Area')}\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"📐 المساحة: {row.get('Project Area')}\n"
                            f"🏗️ المطور: {row.get('Developer')}\n\n"
                            f"✨ انقر لعرض التفاصيل الكاملة"
                        )
                        if st.button(card_text, key=f"card_p_{i+j}"):
                            st.session_state.selected_item = row; st.rerun()

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
                        card_text = (
                            f"🏗️ {row.get('Developer')}\n"
                            f"⭐ التصنيف: {row.get('Developer Category')}\n"
                            f"━━━━━━━━━━━━━━\n"
                            f"👤 المالك: {row.get('Owner')}\n"
                            f"🏢 عدد المشاريع: {row.get('Number of Projects')}\n\n"
                            f"📖 عرض سابقة الأعمال"
                        )
                        if st.button(card_text, key=f"card_d_{i+j}"):
                            st.session_state.selected_item = row; st.rerun()

    elif menu == "الأدوات":
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ الأدوات الذكية</h2>", unsafe_allow_html=True)
        col_calc, col_unit = st.columns(2)
        with col_calc:
            st.subheader("💰 حاسبة الأقساط")
            price = st.number_input("سعر الوحدة", 1000000)
            years = st.slider("سنوات السداد", 1, 15, 8)
            st.metric("القسط الشهري", f"{price/(years*12):,.0f} ج.م")
        with col_unit:
            st.subheader("📐 محول المساحات")
            sqm = st.number_input("المساحة (متر مربع)", 100.0)
            st.info(f"القدم المربع: {sqm * 10.76:,.2f}")

# زر الخروج في التذييل
st.sidebar.markdown("---")
if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state.auth = False; st.rerun()
