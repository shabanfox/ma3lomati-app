import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }

    .main-header {
        background: linear-gradient(90deg, #111 0%, #000 100%);
        padding: 15px 35px; border-radius: 0 0 15px 15px;
        border: 1px solid #222; border-right: 12px solid #f59e0b;
        text-align: center; margin-bottom: 20px;
    }
    .header-title { font-weight: 900; font-size: 35px !important; color: #f59e0b; margin: 0; }

    .grid-card {
        background: linear-gradient(145deg, #111, #080808);
        border: 1px solid #222; border-top: 5px solid #f59e0b;
        border-radius: 12px; padding: 25px; margin-bottom: 5px;
        min-height: 380px; direction: rtl;
    }
    
    .card-title { color: #f59e0b; font-size: 28px !important; font-weight: 900 !important; margin-bottom: 5px; }
    .card-subtitle { color: #ffffff; font-size: 20px !important; font-weight: 700 !important; border-bottom: 1px solid #333; padding-bottom: 8px; margin-bottom: 12px; }
    
    .stat-line { display: flex; justify-content: space-between; font-size: 15px; margin-bottom: 8px; }
    .stat-label { color: #888; }
    .stat-value { color: #f59e0b; font-weight: bold; }

    /* تحسين شكل الـ Expander (التفاصيل) */
    .streamlit-expanderHeader { background-color: #1a1a1a !important; color: #f59e0b !important; border-radius: 8px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. شريط علوي بسيط
c_top1, c_top2 = st.columns([9, 1])
with c_top1: st.markdown('<div style="padding-top:10px; color:#555;">نظام المعلومات العقاري - PRO</div>', unsafe_allow_html=True)
with c_top2: 
    if st.button("خروج"): st.session_state.clear(); st.rerun()

st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

# 4. تحميل البيانات
@st.cache_data(ttl=300)
def load_all_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except: return pd.DataFrame()

df = load_all_data()

# 5. القائمة
selected = option_menu(
    menu_title=None, options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], orientation="horizontal",
    styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"},
            "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"}}
)

# --- 🛠️ شاشة أدوات البروكر ---
if selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ عُدة البروكر المحترف</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div style='background:#111; padding:20px; border-radius:15px; border-right:5px solid #f59e0b;'><h3>💰 حاسبة القسط</h3>", unsafe_allow_html=True)
        p = st.number_input("السعر الكلي", value=1000000)
        dp = st.number_input("المقدم %", value=10)
        y = st.number_input("سنين القسط", value=7)
        res = (p - (dp/100*p))/(y*12) if y>0 else 0
        st.markdown(f"<h3 style='color:#f59e0b; text-align:center;'>{res:,.0f} ج.م/شهرياً</h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div style='background:#111; padding:20px; border-radius:15px; border-right:5px solid #00ffcc;'><h3>📈 حاسبة ROI</h3>", unsafe_allow_html=True)
        inv = st.number_input("الاستثمار", value=2000000)
        rent = st.number_input("الإيجار الشهري", value=15000)
        st.markdown(f"<h3 style='color:#00ffcc; text-align:center;'>{(rent*12/inv)*100:.2f} % سنوياً</h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div style='background:#111; padding:20px; border-radius:15px; border-right:5px solid #fff;'><h3>📱 رسالة عرض</h3>", unsafe_allow_html=True)
        name = st.text_input("اسم العميل")
        if st.button("تجهيز"): st.code(f"أهلاً {name}، متاح لدينا وحدات مميزة.. تواصل معي.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 🏗️ شاشة المشاريع ---
elif selected == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
    if not df.empty:
        search = st.text_input("🔍 ابحث عن اسم المشروع...")
        dff = df[df['Projects'].str.contains(search, case=False, na=False)] if search else df
        
        for i in range(0, len(dff.iloc[:12]), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(dff):
                    row = dff.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="grid-card">
                                <div class="card-title">🏗️ {row.get('Projects','-')}</div>
                                <div class="card-subtitle">🏢 {row.get('Developer','-')}</div>
                                <div class="stat-line"><span class="stat-label">📍 الموقع:</span><span class="stat-value">{row.get('Area','-')}</span></div>
                                <div class="stat-line"><span class="stat-label">💰 المقدم:</span><span class="stat-value">{row.get('Down_Payment','-')}</span></div>
                                <div class="stat-line"><span class="stat-label">⏳ التقسيط:</span><span class="stat-value">{row.get('Installments','-')}</span></div>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("🔍 تفاصيل المشروع الكاملة"):
                            st.write(row.to_dict())

# --- 🏢 شاشة المطورين ---
elif selected == "🏢 المطورين":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏢 سجل المطورين العقاريين</h2>", unsafe_allow_html=True)
    if not df.empty:
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        search_d = st.text_input("🔍 ابحث عن اسم المطور...")
        if search_d: devs = devs[devs['Developer'].str.contains(search_d, case=False, na=False)]
        
        for i in range(0, len(devs.iloc[:12]), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(devs):
                    row = devs.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="grid-card">
                                <div class="card-title">🏢 {row.get('Developer', '-')}</div>
                                <div class="card-subtitle">👤 المالك: {row.get('Owner', 'غير مسجل')}</div>
                                <div style="color:#bbb; font-size:14px; min-height:100px;">
                                    <b>نبذة:</b><br>{str(row.get('Detailed_Info', ''))[:150]}...
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("📄 سابقة الأعمال والتفاصيل"):
                            st.info(f"المالك: {row.get('Owner')}")
                            st.write(row.get('Detailed_Info'))
