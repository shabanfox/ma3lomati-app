import streamlit as st
import pandas as pd
import feedparser
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
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

# 4. التنسيق الجمالي الموحد (Noir & Gold)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    
    .luxury-header {
        background: rgba(15, 15, 15, 0.9); backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b; padding: 15px 30px;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; border-radius: 0 0 25px 25px; margin-bottom: 15px;
    }
    .logo-text { color: #f59e0b; font-weight: 900; font-size: 24px; }
    
    .ticker-wrap { width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 10px; }
    .ticker { display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    /* ستايل الكروت الموحد */
    div.stButton > button {
        background-color: white !important;
        color: #111 !important;
        border: 1px solid #eee !important;
        border-radius: 15px !important;
        width: 100% !important;
        min-height: 220px !important;
        padding: 20px !important;
        text-align: right !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        transition: 0.3s !important;
    }
    div.stButton > button:hover {
        border-color: #f59e0b !important;
        transform: translateY(-3px) !important;
    }
    
    .detail-card { background: #111; padding: 30px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; }
    .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0; }
    .info-item { background: #1a1a1a; padding: 12px; border-radius: 10px; border: 1px solid #333; }
    .label { color: #f59e0b; font-weight: bold; font-size: 14px; display: block; }
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1.5,1])
    with c2:
        pw = st.text_input("Passcode", type="password")
        if st.button("دخول"):
            if pw == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# 6. جلب البيانات من الشيتات
@st.cache_data(ttl=60)
def load_all_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("غير متوفر").astype(str)
        d = pd.read_csv(u_d).fillna("غير متوفر").astype(str)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_all_data()

# الهيدر والتيكر
st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI PRO</div><div style="color:#aaa; font-size:12px;">📅 {datetime.now().strftime("%Y-%m-%d")}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], 
    default_index=1, orientation="horizontal",
    styles={"container": {"background-color": "#0a0a0a", "padding": "0"}, "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}}
)

main_col, side_col = st.columns([0.75, 0.25])

with side_col:
    st.markdown("<p style='color:#10b981; text-align:center; font-weight:bold;'>🔑 استلام فوري</p>", unsafe_allow_html=True)
    if not df_p.empty:
        ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
        for _, r in ready.head(10).iterrows():
            st.markdown(f'<div style="background:#161616; padding:10px; border-radius:8px; margin-bottom:5px; border-right:3px solid #10b981; color:#eee; font-size:13px;">{r.get("Project Name")}</div>', unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🚪 خروج آمن", use_container_width=True):
        st.session_state.auth = False; st.rerun()

with main_col:
    # --- عرض التفاصيل (مشروع أو مطور) ---
    if st.session_state.selected_item is not None:
        item = st.session_state.selected_item
        if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
        
        # إذا كان المختار مشروع
        if 'Project Name' in item:
            st.markdown(f"""
            <div class="detail-card">
                <h1 style="color:#f59e0b;">{item.get('Project Name')}</h1>
                <p>📍 {item.get('Area')}</p>
                <div class="info-grid">
                    <div class="info-item"><span class="label">🏗️ المطور:</span>{item.get('Developer')}</div>
                    <div class="info-item"><span class="label">📐 مساحة المشروع:</span>{item.get('Project Area')}</div>
                    <div class="info-item"><span class="label">🏢 الإدارة والتشغيل:</span>{item.get('Management')}</div>
                    <div class="info-item"><span class="label">📋 الماستر بلان:</span>{item.get('Master Plan')}</div>
                </div>
                <div class="info-item" style="margin-bottom:15px; border-right:4px solid #f59e0b;">
                    <span class="label">📍 الموقع بالتفصيل (Detailed Location):</span>{item.get('Detailed Location')}
                </div>
                <div class="info-item"><span class="label">✨ مميزات المشروع (Features):</span>{item.get('Project Features')}</div>
            </div>
            """, unsafe_allow_html=True)
            
        # إذا كان المختار مطور
        else:
            st.markdown(f"""
            <div class="detail-card">
                <h1 style="color:#f59e0b;">{item.get('Developer')}</h1>
                <p>⭐ التصنيف: {item.get('Developer Category')}</p>
                <div class="info-grid">
                    <div class="info-item"><span class="label">👑 المالك:</span>{item.get('Owner')}</div>
                    <div class="info-item"><span class="label">🏢 عدد المشاريع:</span>{item.get('Number of Projects')}</div>
                    <div class="info-item"><span class="label">📍 منطقة النشاط:</span>{item.get('Main Region of Activity')}</div>
                    <div class="info-item"><span class="label">🏠 المقر الرئيسي:</span>{item.get('Headquarters Address')}</div>
                </div>
                <div class="info-item" style="margin-bottom:15px; border-right:4px solid #f59e0b;">
                    <span class="label">📖 سابقة الأعمال (Previous Projects):</span>{item.get('Previous Projects')}
                </div>
                <div class="info-item" style="margin-bottom:20px;"><span class="label">ℹ️ معلومات إضافية:</span>{item.get('Detailed_Info')}</div>
                <div style="text-align:center;"><a href="{item.get('Company Website / Portfolio')}" target="_blank" style="background:#f59e0b; color:black; padding:10px 25px; border-radius:20px; text-decoration:none; font-weight:bold;">🌐 الموقع الإلكتروني</a></div>
            </div>
            """, unsafe_allow_html=True)

    elif menu == "المشاريع":
        c1, c2, c3 = st.columns(3)
        with c1:
            areas = ["الكل"] + sorted(df_p['Area'].unique().tolist())
            s_area = st.selectbox("المنطقة", areas)
        with c2:
            devs = ["الكل"] + sorted(df_p['Developer'].unique().tolist())
            s_dev = st.selectbox("المطور", devs)
        with c3:
            s_name = st.text_input("ابحث عن اسم المشروع...")

        dff_p = df_p.copy()
        if s_area != "الكل": dff_p = dff_p[dff_p['Area'] == s_area]
        if s_dev != "الكل": dff_p = dff_p[dff_p['Developer'] == s_dev]
        if s_name: dff_p = dff_p[dff_p['Project Name'].str.contains(s_name, case=False)]

        limit = 6
        curr = dff_p.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]
        for i in range(0, len(curr), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(curr):
                    row = curr.iloc[i+j]
                    with cols[j]:
                        lbl = f"🏢 {row.get('Project Name')}\n📍 {row.get('Area')}\n🏗️ {row.get('Developer')}\n📐 {row.get('Project Area')}"
                        if st.button(lbl, key=f"p_{i+j}"): st.session_state.selected_item = row; st.rerun()

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
                        lbl = f"🏗️ {row.get('Developer')}\n👑 {row.get('Owner')}\n⭐ فئة {row.get('Developer Category')}\n📍 {row.get('Main Region of Activity')}"
                        if st.button(lbl, key=f"d_{i+j}"): st.session_state.selected_item = row; st.rerun()

    elif menu == "الأدوات":
        st.markdown("<h3 style='color:#f59e0b;'>🛠️ الأدوات المساعدة</h3>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🧮 حاسبة القسط", "📐 محول المساحات"])
        with t1:
            price = st.number_input("السعر الإجمالي", 1000000); y = st.slider("سنوات التقسيط", 1, 15, 8)
            st.metric("القسط الشهري التقريبي", f"{price/(y*12):,.0f} ج.م")
        with t2:
            sq = st.number_input("المتر المربع", 100.0); st.write(f"القدم المربع: {sq*10.76:,.2f}")
