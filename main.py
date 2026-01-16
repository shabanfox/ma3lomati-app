import streamlit as st
import pandas as pd
import math
import feedparser
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 3. جلب الأخبار الحقيقية
@st.cache_data(ttl=600)
def get_real_news():
    try:
        # استخدام مصدر أخبار اقتصادية سريع التحديث
        rss_url = "https://www.skynewsarabia.com/rss/v1/business.xml" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:20]]
        return "  •  ".join(news) if news else "جاري تحديث الأخبار..."
    except:
        return "العاصمة الإدارية الجديدة تشهد طفرة في المبيعات • ارتفاع الطلب على الوحدات التجارية • استقرار أسعار مواد البناء."

news_text = get_real_news()

# 4. التنسيق الجمالي (تعديل شريط الأخبار ليكون أسرع وأوضح)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    .luxury-header {{
        background: rgba(15, 15, 15, 0.95); backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b; padding: 10px 30px;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; border-radius: 0 0 25px 25px; margin-bottom: 10px;
    }}
    .logo-text {{ color: #f59e0b; font-weight: 900; font-size: 24px; }}
    
    /* شريط الأخبار المطور: أسرع (60 ثانية) وأوضح (خط أكبر) */
    .ticker-wrap {{ 
        width: 100%; 
        background: #000; /* خلفية سوداء تماماً للوضوح */
        padding: 12px 0; 
        overflow: hidden; 
        white-space: nowrap; 
        border-bottom: 1px solid #f59e0b; 
        margin-bottom: 15px;
    }}
    .ticker {{ 
        display: inline-block; 
        padding-right: 100%; 
        animation: ticker 60s linear infinite; /* سرعة متوسطة وواضحة */
        color: #f59e0b; 
        font-size: 18px; /* تكبير الخط للوضوح */
        font-weight: 700;
        letter-spacing: 0.5px;
    }}
    @keyframes ticker {{ 
        0% {{ transform: translateX(100%); }} 
        100% {{ transform: translateX(-100%); }} 
    }}

    /* ستايل كروت نوي الكبير بالتفاصيل */
    div.stButton > button[key*="card_"] {{
        background-color: white !important;
        color: #111 !important;
        border: 1px solid #eee !important;
        border-radius: 15px !important;
        width: 100% !important;
        min-height: 280px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: flex-start !important;
        padding: 20px !important;
        transition: 0.3s !important;
        text-align: right !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        white-space: pre-wrap !important;
    }}
    div.stButton > button[key*="card_"]:hover {{
        border-right: 6px solid #f59e0b !important;
        transform: translateY(-5px) !important;
    }}

    /* زر الخروج */
    div.stButton > button[key="logout_top"] {{
        background-color: #ef4444 !important; color: white !important;
        height: 35px !important; border: none !important; border-radius: 8px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1.5,1])
    with c2:
        if st.text_input("Passcode", type="password") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# 6. الهيدر وزر الخروج
header_main, header_btn = st.columns([0.88, 0.12])
with st.container():
    st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI <span style="color:white; font-size:14px;">PRO</span></div><div></div></div>', unsafe_allow_html=True)
    with header_btn:
        st.markdown("<div style='margin-top:-60px; text-align:left;'>", unsafe_allow_html=True)
        if st.button("🚪 خروج", key="logout_top"):
            st.session_state.auth = False; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# عرض الشريط (أسرع وأوضح)
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔴 عاجل: {news_text}   •   تم التحديث الآن: {datetime.now().strftime("%H:%M")}</div></div>', unsafe_allow_html=True)

# 7. البيانات
@st.cache_data(ttl=60)
def load_all_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("").astype(str)
        d = pd.read_csv(u_d).fillna("").astype(str)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_all_data()

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], 
    default_index=1, orientation="horizontal",
    styles={"container": {"background-color": "#0a0a0a"}, "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}}
)

main_col, side_col = st.columns([0.75, 0.25])

# الجزء الجانبي (استلام فوري)
with side_col:
    st.markdown("<p style='color:#10b981; text-align:center; font-weight:bold;'>🔑 استلام فوري</p>", unsafe_allow_html=True)
    st.markdown("<div style='background:#0d0d0d; border-radius:15px; padding:10px; border-top:3px solid #10b981;'>", unsafe_allow_html=True)
    ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(10)
    for _, row in ready.iterrows():
        st.markdown(f'<div style="background:#161616; padding:8px; border-right:3px solid #10b981; margin-bottom:5px; border-radius:5px;"><div style="color:#f59e0b; font-size:12px;">{row.get("Project Name")}</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# الجزء الرئيسي
with main_col:
    if st.session_state.selected_item is not None:
        item = st.session_state.selected_item
        if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
        st.markdown(f"<div style='background:#111; padding:25px; border-radius:15px; border-right:8px solid #f59e0b; color:white;'><h1>{item.get('Project Name', item.get('Developer'))}</h1><hr>{item.get('Project Features', item.get('Detailed_Info'))}</div>", unsafe_allow_html=True)

    elif menu == "المشاريع":
        search = st.text_input("🔍 بحث عن مشروع...")
        dff = df_p.copy()
        if search: dff = dff[dff.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        
        limit = 6
        items = dff.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]
        
        for i in range(0, len(items), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(items):
                    row = items.iloc[i+j]
                    with cols[j]:
                        label = f"🏢 {row.get('Project Name')}\n📍 الموقع: {row.get('Area')}\n━━━━━━━━━━━━\n🏗️ المطور: {row.get('Developer')}\n📐 المساحة: {row.get('Project Area')}"
                        if st.button(label, key=f"card_p_{i+j}"): st.session_state.selected_item = row; st.rerun()
        
        st.write("---")
        n1, _, n2 = st.columns([1, 2, 1])
        if n1.button("السابق ⬅️", key="p_p"): st.session_state.p_idx = max(0, st.session_state.p_idx-1); st.rerun()
        if n2.button("التالي ➡️", key="p_n"): st.session_state.p_idx += 1; st.rerun()

    elif menu == "المطورين":
        search_d = st.text_input("🔍 بحث عن مطور...")
        dff_d = df_d.copy()
        if search_d: dff_d = dff_d[dff_d.apply(lambda r: r.astype(str).str.contains(search_d, case=False).any(), axis=1)]

        limit_d = 6
        items_d = dff_d.iloc[st.session_state.d_idx*limit_d : (st.session_state.d_idx+1)*limit_d]

        for i in range(0, len(items_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(items_d):
                    row = items_d.iloc[i+j]
                    with cols[j]:
                        label = f"🏗️ {row.get('Developer')}\n⭐ فئة: {row.get('Developer Category')}\n━━━━━━━━━━━━\n👤 المالك: {row.get('Owner')}\n🏢 مشاريع: {row.get('Number of Projects')}"
                        if st.button(label, key=f"card_d_{i+j}"): st.session_state.selected_item = row; st.rerun()

        st.write("---")
        nd1, _, nd2 = st.columns([1, 2, 1])
        if nd1.button("السابق ⬅️", key="d_p"): st.session_state.d_idx = max(0, st.session_state.d_idx-1); st.rerun()
        if nd2.button("التالي ➡️", key="d_n"): st.session_state.d_idx += 1; st.rerun()

    elif menu == "الأدوات":
        st.markdown("<h3 style='color:#f59e0b;'>🛠️ الأدوات</h3>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🧮 القسط", "📐 المساحة"])
        with t1:
            price = st.number_input("السعر", 1000000); y = st.slider("السنين", 1, 15, 8)
            st.metric("القسط الشهري", f"{price/(y*12):,.0f} ج.م")
        with t2:
            sq = st.number_input("متر", 100.0); st.write(f"قدم: {sq*10.76:,.2f}")
