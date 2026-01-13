import streamlit as st
import pandas as pd
import math
import feedparser
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة والأداء العالي
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. وظيفة جلب البيانات مع تخزين مؤقت (Speed Optimization)
@st.cache_data(ttl=300)
def load_full_data():
    # روابط الشيتات الخاصة بك
    u_projects = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_developers = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_projects).fillna("").astype(str)
        d = pd.read_csv(u_developers).fillna("").astype(str)
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        return p, d
    except:
        return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_full_data()

# 3. التصميم (CSS Luxury) - الهيدر والشبكة والـ 70/30
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    body, [data-testid="stAppViewContainer"] { background-color: #050505; color: white; direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    .block-container { padding-top: 0rem !important; }
    header { visibility: hidden; }
    
    /* الهيدر الزجاجي */
    .luxury-header {
        background: rgba(15, 15, 15, 0.9); backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b; padding: 20px 40px;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; border-radius: 0 0 25px 25px; margin-bottom: 20px;
    }
    .logo-text { color: #f59e0b; font-weight: 900; font-size: 28px; text-shadow: 0 0 10px rgba(245, 158, 11, 0.4); }

    /* شبكة الكروت */
    .grid-card {
        background: linear-gradient(145deg, #111, #1a1a1a);
        border: 1px solid #222; border-right: 5px solid #f59e0b;
        border-radius: 15px; padding: 20px; margin-bottom: 20px;
        transition: 0.3s ease;
    }
    .grid-card:hover { transform: translateY(-5px); border-color: #f59e0b; }

    /* منطقة الاستلام الفوري */
    .ready-sidebar {
        background: #0f0f0f; border: 1px solid #222; border-radius: 15px; padding: 15px;
        height: 85vh; overflow-y: auto; border-top: 4px solid #10b981;
    }
    .ready-item {
        background: #161616; border-right: 4px solid #10b981;
        padding: 12px; border-radius: 8px; margin-bottom: 12px;
    }
    
    /* الأزرار والأدوات */
    .stButton button { background: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #f59e0b !important; border-radius: 10px !important; width: 100%; }
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [aria-selected="true"] { background-color: #f59e0b !important; color: black !important; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# 4. نظام الحماية
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    if st.text_input("Passcode", type="password") == "2026": 
        st.session_state.auth = True; st.rerun()
    st.stop()

# --- 5. بناء الهيدر المطور ---
st.markdown(f"""
    <div class="luxury-header">
        <div class="logo-text">MA3LOMATI <span style="color:white; font-size:14px;">PRO 2026</span></div>
        <div style="color:#aaa; font-size:14px;">📅 {datetime.now().strftime("%Y-%m-%d")}</div>
    </div>
""", unsafe_allow_html=True)

# المنيو الرئيسي
menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], orientation="horizontal",
    styles={"container": {"background-color": "#000"}, "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- 6. تقسيم الشاشة (70% محتوى | 30% استلام فوري) ---
col_main, col_side = st.columns([0.7, 0.3])

# --- الجانب الأيمن: استلام فوري دائم ---
with col_side:
    st.markdown("<h3 style='color:#10b981; text-align:center;'>🔑 استلام فوري فقط</h3>", unsafe_allow_html=True)
    st.markdown("<div class='ready-sidebar'>", unsafe_allow_html=True)
    # فلترة تلقائية للمشاريع الجاهزة
    ready_df = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
    if not ready_df.empty:
        for _, row in ready_df.iterrows():
            st.markdown(f"""
                <div class="ready-item">
                    <b style="color:#f59e0b; font-size:16px;">{row['Project Name']}</b><br>
                    <small>📍 {row['Area']}</small><br>
                    <small>🏢 {row['Developer']}</small>
                </div>
            """, unsafe_allow_html=True)
    else: st.write("لا توجد بيانات حالياً")
    st.markdown("</div>", unsafe_allow_html=True)

# --- الجانب الأيسر: المحتوى الرئيسي ---
with col_main:
    if menu == "المشاريع":
        st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
        search_p = st.text_input("🔍 ابحث عن أي مشروع، منطقة، أو مطور...")
        
        filtered_p = df_p.copy()
        if search_p:
            filtered_p = filtered_p[filtered_p.apply(lambda r: r.astype(str).str.contains(search_p, case=False).any(), axis=1)]
        
        # شبكة المشاريع
        for i in range(0, len(filtered_p), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(filtered_p):
                    row = filtered_p.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="grid-card">
                                <h3 style="color:#f59e0b; margin-top:0;">{row['Project Name']}</h3>
                                <p>📍 <b>الموقع:</b> {row['Area']}</p>
                                <p>📐 <b>المساحة:</b> {row['Project Area']}</p>
                                <p style="color:#aaa;">🏢 المطور: {row.get('Developer')}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("🔎 التفاصيل الكاملة"):
                            st.info(f"✨ المميزات: {row.get('Project Features')}")
                            st.warning(f"⚠️ العيوب: {row.get('Project Flaws')}")

    elif menu == "المطورين":
        st.markdown("<h2 style='color:#f59e0b;'>🏢 دليل المطورين</h2>", unsafe_allow_html=True)
        search_d = st.text_input("🔍 بحث عن مطور...")
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
                            <div class="grid-card">
                                <h3 style="color:#f59e0b; margin-top:0;">{row['Developer']}</h3>
                                <p>👤 <b>المالك:</b> {row['Owner']}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("📖 التاريخ وسابقة الأعمال"):
                            st.write(f"ℹ️ **عن الشركة:** {row.get('Detailed_Info')}")
                            st.success(f"🏆 **الميزة التنافسية:** {row.get('Competitive Advantage')}")

    elif menu == "الأدوات":
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ مركز الأدوات المتطور</h2>", unsafe_allow_html=True)
        t = st.tabs(["🧮 الأقساط", "📈 الاستثمار ROI", "📐 المساحات", "🤝 تقييم العميل", "💰 العمولة", "📝 نوت"])
        
        with t[0]:
            p = st.number_input("سعر الوحدة", 1000000); d = st.number_input("المقدم", p*0.1); y = st.slider("السنين", 1, 15, 8)
            st.metric("القسط الشهري", f"{(p-d)/(y*12):,.0f} ج.م")
        with t[1]:
            rent = st.number_input("الإيجار المتوقع", 10000)
            st.metric("ROI السنوي", f"{(rent*12/p)*100:.2f}%")
            st.write(f"⏳ استرداد رأس المال خلال: {p/(rent*12):,.1f} سنة")
        with t[2]:
            m2 = st.number_input("المساحة m2", 100.0)
            st.write(f"قدم مربع: {m2*10.76:,.2f} | قيراط: {m2/175:,.2f}")
        with t[3]:
            st.selectbox("جدية العميل", ["بارد", "مقارن", "جاهز للتعاقد"])
            st.progress(70)
        with t[4]:
            comm = st.number_input("نسبة العمولة %", 1.5)
            st.metric("صافي عمولتك", f"{p*(comm/100):,.0f} ج.م")
        with t[5]:
            st.text_area("ملاحظات العميل...")

# 7. زر الخروج
st.sidebar.markdown("---")
if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state.auth = False
    st.rerun()
