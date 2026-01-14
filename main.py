import streamlit as st
import pandas as pd
import math
import feedparser
import urllib.parse
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة والأداء
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (Session State)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0

# 3. جلب الأخبار (Real-time RSS)
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297"
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "جاري تحديث أخبار السوق العقاري..."
    except: return "متابعة مستمرة لأحدث تطورات السوق العقاري المصري 2026."

news_text = get_real_news()

# 4. التنسيق الجمالي (CSS Luxury)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    /* الهيدر الفخم */
    .luxury-header {{
        background: rgba(15, 15, 15, 0.9); backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b; padding: 15px 40px;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; border-radius: 0 0 30px 30px; margin-bottom: 10px;
    }}
    .logo-text {{ color: #f59e0b; font-weight: 900; font-size: 26px; text-shadow: 0 0 10px rgba(245, 158, 11, 0.4); }}
    
    /* شريط الأخبار */
    .ticker-wrap {{ width: 100%; background: #111; padding: 8px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #ccc; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* الكروت والشبكة */
    .grid-card {{ 
        background: linear-gradient(145deg, #111, #1a1a1a); border: 1px solid #222; 
        border-right: 5px solid #f59e0b; border-radius: 15px; padding: 18px; margin-bottom: 15px;
        transition: 0.3s ease;
    }}
    .grid-card:hover {{ transform: translateY(-5px); border-color: #f59e0b; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }}

    /* القائمة الجانبية للاستلام الفوري */
    .ready-sidebar {{
        background: #0f0f0f; border: 1px solid #222; border-radius: 20px; padding: 15px;
        height: 80vh; overflow-y: auto; border-top: 4px solid #10b981;
    }}
    .ready-item {{
        background: #161616; border-right: 4px solid #10b981; padding: 12px; border-radius: 10px; margin-bottom: 12px;
    }}

    /* الأزرار */
    .stButton button {{
        background: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #f59e0b !important;
        border-radius: 12px !important; transition: 0.3s !important; width: 100%;
    }}
    .stButton button:hover {{ background: #f59e0b !important; color: #000 !important; }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة تسجيل الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        pwd = st.text_input("Passcode", type="password")
        if st.button("دخول"):
            if pwd == "2026": st.session_state.auth = True; st.rerun()
            else: st.error("كلمة المرور غير صحيحة")
    st.stop()

# --- الهيدر العلوي ---
now = datetime.now().strftime("%H:%M")
st.markdown(f"""
    <div class="luxury-header">
        <div class="logo-text">MA3LOMATI PRO</div>
        <div style="text-align:left;">
            <span style="color:#f59e0b; font-weight:bold;">⌚ {now}</span><br>
            <span style="color:#aaa; font-size:12px;">Real Estate Intelligence</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# زر الخروج
if st.button("🚪 تسجيل الخروج", key="logout"): st.session_state.auth = False; st.rerun()

# شريط الأخبار
st.markdown(f'<div class="ticker-wrap"><div class="ticker"><b>🔥 حصرياً:</b> {news_text}</div></div>', unsafe_allow_html=True)

# القائمة الرئيسية (Option Menu)
menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], 
    orientation="horizontal",
    styles={
        "container": {"background-color": "#000", "padding": "0"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"},
    }
)

# 6. جلب البيانات من Google Sheets (الروابط الخاصة بك)
@st.cache_data(ttl=60)
def load_data():
    # ملاحظة: تم تحويل pubhtml إلى export لضمان قراءة الـ CSV
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("غير متوفر").astype(str)
        d = pd.read_csv(u_d).fillna("غير متوفر").astype(str)
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# --- التوزيع الشبكي 70% أساسي و 30% جانبي ---
col_main, col_side = st.columns([0.7, 0.3])

# --- الجزء الجانبي (30%): استلام فوري فقط ---
with col_side:
    st.markdown("<h3 style='color:#10b981; text-align:center;'>🔑 استلام فوري فقط</h3>", unsafe_allow_html=True)
    st.markdown("<div class='ready-sidebar'>", unsafe_allow_html=True)
    # تصفية المشاريع الجاهزة آلياً
    ready_projects = df_p[df_p.apply(lambda row: row.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
    if not ready_projects.empty:
        for _, row in ready_projects.iterrows():
            st.markdown(f"""
                <div class="ready-item">
                    <b style="color:#f59e0b;">{row['Project Name']}</b><br>
                    <small>📍 {row['Area']}</small><br>
                    <small>🏢 {row['Developer']}</small>
                </div>
            """, unsafe_allow_html=True)
    else: st.write("لا توجد مشاريع جاهزة")
    st.markdown("</div>", unsafe_allow_html=True)

# --- الجزء الرئيسي (70%) ---
with col_main:
    if menu == "المشاريع":
        st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
        search_query = st.text_input("🔍 ابحث عن اسم المشروع، المطور، أو الموقع...")
        
        filtered_p = df_p.copy()
        if search_query:
            filtered_p = filtered_p[filtered_p.apply(lambda r: r.astype(str).str.contains(search_query, case=False).any(), axis=1)]
        
        # العرض الشبكي (2 في الصف)
        limit = 6
        curr_page = filtered_p.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]

        for i in range(0, len(curr_page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(curr_page):
                    row = curr_page.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class='grid-card'>
                                <h3 style='color:#f59e0b; margin:0;'>{row.get('Project Name')}</h3>
                                <p style='margin:5px 0;'>📍 <b>الموقع:</b> {row.get('Area')}</p>
                                <p style='margin:5px 0;'>📐 <b>المساحة:</b> {row.get('Project Area')}</p>
                                <p style='color:#aaa;'>🏢 المطور: {row.get('Developer')}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("🔎 تفاصيل إضافية"):
                            st.info(f"✨ المميزات: {row.get('Project Features')}")
                            st.error(f"⚠️ العيوب: {row.get('Project Flaws')}")

        # أزرار التنقل
        st.markdown("---")
        b1, b2 = st.columns(2)
        if b1.button("الصفحة التالية ⬅️"): st.session_state.p_idx += 1; st.rerun()
        if b2.button("➡️ الصفحة السابقة"): st.session_state.p_idx = max(0, st.session_state.p_idx-1); st.rerun()

    elif menu == "المطورين":
        st.markdown("<h2 style='color:#f59e0b;'>🏢 المطورين العقاريين</h2>", unsafe_allow_html=True)
        search_d = st.text_input("🔍 ابحث عن شركة تطوير...")
        filtered_d = df_d.copy()
        if search_d:
            filtered_d = filtered_d[filtered_d.apply(lambda r: r.astype(str).str.contains(search_d, case=False).any(), axis=1)]

        for i in range(0, len(filtered_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(filtered_d):
                    row = filtered_d.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class='grid-card'>
                                <h4 style='color:#f59e0b; margin:0;'>{row.get('Developer')}</h4>
                                <p>👤 المالك: {row.get('Owner')}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("📖 سابقة الأعمال"):
                            st.write(row.get('Detailed_Info'))
                            st.success(f"🏆 الميزة: {row.get('Competitive Advantage')}")

    elif menu == "الأدوات":
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ مركز أدوات البروكر</h2>", unsafe_allow_html=True)
        
        # رادار البحث الذكي
        st.markdown("<div style='background:#111; padding:15px; border-radius:15px; border:1px solid #f59e0b; margin-bottom:20px;'>", unsafe_allow_html=True)
        st.subheader("🕵️ رادار المشاريع الذكي (خارج الشيت)")
        ext_search = st.text_input("أدخل اسم أي مشروع غير متاح في الشيت للبحث عنه عالمياً...")
        if ext_search:
            q = urllib.parse.quote(ext_search + " عقارات مصر")
            c1, c2 = st.columns(2)
            c1.link_button("🌍 بحث شامل في جوجل", f"https://www.google.com/search?q={q}")
            c2.link_button("📍 موقعه على الخريطة", f"https://www.google.com/maps/search/{q}")
        st.markdown("</div>", unsafe_allow_html=True)

        # الأدوات المالية
        t = st.tabs(["🧮 الأقساط", "📈 الاستثمار ROI", "📐 المساحات", "💰 العمولة", "🏠 الفائدة"])
        with t[0]:
            p = st.number_input("سعر الوحدة", 1000000); d = st.number_input("المقدم", p*0.1); y = st.slider("السنين", 1, 15, 8)
            st.metric("القسط الشهري", f"{(p-d)/(y*12):,.0f} ج.م")
        with t[1]:
            rent = st.number_input("الإيجار المتوقع", 10000)
            st.metric("عائد الاستثمار ROI", f"{(rent*12/p)*100:.2f}%")
        with t[2]:
            m2 = st.number_input("المتر المربع", 100.0)
            st.write(f"القدم المربع: {m2*10.76:,.2f}")
        with t[3]:
            r = st.number_input("نسبة العمولة %", 1.5)
            st.metric("صافي العمولة", f"{p*(r/100):,.0f} ج.م")
        with t[4]:
            f = st.slider("نسبة التحميل/الفائدة %", 0, 40, 20)
            st.write(f"الإجمالي بعد الإضافة: {p*(1+f/100):,.0f}")
