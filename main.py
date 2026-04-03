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
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0

# 3. التنسيق الجمالي (CSS المطور) - زر الخروج والألوان الواضحة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container { padding-top: 0rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { background-color: #f8fafc; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    
    /* الهيدر الفاخر */
    .luxury-header {
        background: #0f172a; border-bottom: 3px solid #f59e0b; padding: 10px 30px;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; border-radius: 0 0 20px 20px; margin-bottom: 10px;
    }
    .logo-text { color: #f59e0b; font-weight: 900; font-size: 24px; }
    
    /* شريط الأخبار */
    .ticker-wrap { width: 100%; background: #ffffff; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #e2e8f0; }
    .ticker { display: inline-block; animation: ticker 120s linear infinite; color: #475569; font-size: 13px; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    /* كروت الشبكة */
    .grid-card { 
        background: white; border: 1px solid #e2e8f0; 
        border-right: 5px solid #f59e0b; border-radius: 12px; padding: 15px; margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); transition: 0.3s;
    }
    .grid-card:hover { border-color: #3b82f6; transform: translateY(-3px); }

    /* حاوية الاستلام الفوري */
    .ready-sidebar-container {
        background: white; border: 1px solid #e2e8f0; border-radius: 15px; padding: 12px;
        border-top: 4px solid #10b981;
    }
    .ready-card { background: #f0fdf4; border-right: 3px solid #10b981; padding: 8px; border-radius: 8px; margin-bottom: 8px; }
    </style>
""", unsafe_allow_html=True)

# 4. جلب الأخبار والبيانات
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        feed = feedparser.parse("https://www.youm7.com/rss/SectionRss?SectionID=297")
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "جاري تحديث الأخبار..."
    except: return "سوق العقارات المصري 2026: متابعة مستمرة."

@st.cache_data(ttl=60)
def load_all_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("").astype(str)
        d = pd.read_csv(u_d).fillna("").astype(str)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#0f172a;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        if st.text_input("كلمة المرور", type="password") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# 6. الهيدر وزر الخروج
col_h1, col_h2 = st.columns([0.8, 0.2])
with col_h1:
    st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI <span style="color:white; font-size:14px;">PRO</span></div><div style="color:#aaa; font-size:12px;">📅 {datetime.now().strftime("%H:%M")}</div></div>', unsafe_allow_html=True)
with col_h2:
    if st.button("🚪 خروج الآمن"):
        st.session_state.auth = False; st.rerun()

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {get_real_news()}</div></div>', unsafe_allow_html=True)

# 7. المنيو الرئيسي
menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], 
    default_index=1, orientation="horizontal",
    styles={"container": {"background-color": "white", "padding": "5px", "border":"1px solid #e2e8f0"}, "nav-link-selected": {"background-color": "#0f172a", "color": "#f59e0b"}}
)

df_p, df_d = load_all_data()

# توزيع المساحة 75/25
main_col, side_col = st.columns([0.75, 0.25])

# --- الجانب الأيمن (استلام فوري) ---
with side_col:
    st.markdown("<p style='color:#10b981; text-align:center; font-weight:bold;'>🔑 استلام فوري</p>", unsafe_allow_html=True)
    st.markdown("<div class='ready-sidebar-container'>", unsafe_allow_html=True)
    ready_items = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
    for _, row in ready_items.head(8).iterrows():
        st.markdown(f'<div class="ready-card"><div style="color:#0f172a; font-size:13px; font-weight:bold;">{row.get("Project Name", "مشروع")}</div><div style="color:#64748b; font-size:11px;">📍 {row.get("Area", "الموقع")}</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- الجانب الرئيسي ---
with main_col:
    if menu == "المشاريع":
        search = st.text_input("🔍 بحث سريع في المشاريع...")
        dff = df_p.copy()
        if search: dff = dff[dff.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        
        limit = 6
        items = dff.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]
        
        cols = st.columns(2)
        for i, (idx, row) in enumerate(items.iterrows()):
            with cols[i % 2]:
                st.markdown(f"""
                    <div class="grid-card">
                        <h3 style="color:#0f172a; font-size:18px; margin:0;">{row.get('Project Name')}</h3>
                        <p style="color:#3b82f6; font-size:13px; font-weight:bold;">📍 {row.get('Area')}</p>
                        <p style="color:#64748b; font-size:12px;">🏢 المطور: {row.get('Developer')}</p>
                        <div style="border-top:1px solid #f1f5f9; margin-top:10px; padding-top:5px; font-size:11px; color:#94a3b8;">📐 {row.get('Project Area')}</div>
                    </div>
                """, unsafe_allow_html=True)
                with st.expander("تفاصيل الزتونة"):
                    st.info(f"🎨 Master Plan: {row.get('Master Plan')}")
                    st.write(f"✨ المميزات: {row.get('Project Features')}")

        st.markdown("---")
        c1, c2, c3 = st.columns([1,2,1])
        if c1.button("السابق ➡️"): st.session_state.p_idx = max(0, st.session_state.p_idx-1); st.rerun()
        with c2: st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.p_idx + 1}</p>", unsafe_allow_html=True)
        if c3.button("التالي ⬅️"): st.session_state.p_idx += 1; st.rerun()

    elif menu == "المطورين":
        search_d = st.text_input("🔍 ابحث عن المطور...")
        dff_d = df_d.copy()
        if search_d: dff_d = dff_d[dff_d.apply(lambda r: r.astype(str).str.contains(search_d, case=False).any(), axis=1)]
        
        for i in range(0, len(dff_d.head(10)), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(dff_d):
                    row = dff_d.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="grid-card" style="border-right:5px solid #3b82f6;">
                                <h3 style="color:#0f172a; font-size:17px;">{row.get('Developer')}</h3>
                                <p style="color:#64748b; font-size:13px;">👤 المالك: {row.get('Owner')}</p>
                                <p style="color:#10b981; font-weight:bold; font-size:13px;">🏗️ المشاريع: {row.get('Number of Projects')}</p>
                            </div>
                        """, unsafe_allow_html=True)

    elif menu == "الأدوات":
        st.markdown("<div style='background:white; padding:20px; border-radius:15px; border:1px solid #e2e8f0;'>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🧮 حاسبة القسط", "📐 محول المساحات"])
        with t1:
            price = st.number_input("سعر الوحدة", value=5000000)
            years = st.slider("سنوات التقسيط", 1, 15, 8)
            st.metric("القسط الشهري", f"{price/(years*12):,.0f} ج.م")
        with t2:
            sq = st.number_input("المساحة بالمتر", value=100.0)
            st.info(f"المساحة بالقدم: {sq*10.76:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
