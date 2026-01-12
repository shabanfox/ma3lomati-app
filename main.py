import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق (CSS) - حذف الفراغات وتكبير الخطوط
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }

    .top-bar {
        background: #111; padding: 5px 25px; border-bottom: 2px solid #f59e0b;
        display: flex; justify-content: space-between; align-items: center;
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
        border-radius: 12px; padding: 25px; margin-bottom: 15px;
        min-height: 400px; direction: rtl;
    }
    
    .card-title { color: #f59e0b; font-size: 30px !important; font-weight: 900 !important; }
    .card-subtitle { color: #ffffff; font-size: 22px !important; font-weight: 700 !important; border-bottom: 1px solid #333; padding-bottom: 8px; }
    
    .stat-line { display: flex; justify-content: space-between; font-size: 16px; margin-bottom: 10px; }
    .stat-value { color: #f59e0b; font-weight: bold; }

    /* أزرار الأدوات */
    .stButton button { background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #f59e0b !important; }
    .logout-btn button { background-color: #ff4b4b !important; color: white !important; border: none !important; }
    </style>
""", unsafe_allow_html=True)

# 3. شريط المهام العلوي
t_col1, t_col2 = st.columns([9, 1])
with t_col1:
    st.markdown('<div style="padding-top:15px; color:#888;">نظام معلوماتي العقاري PRO 2026</div>', unsafe_allow_html=True)
with t_col2:
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("خروج"):
        st.session_state.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 4. الهيدر
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

# 5. جلب البيانات
@st.cache_data(ttl=300)
def load_all_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except: return pd.DataFrame()

df = load_all_data()

# 6. القائمة
selected = option_menu(
    menu_title=None, options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], orientation="horizontal",
    styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"},
            "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"}}
)

# --- 🛠️ شاشة أدوات البروكر (تمت إعادتها بالكامل) ---
if selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ عُدة البروكر المحترف</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("<div style='background:#111; padding:20px; border-radius:15px; border-right:5px solid #f59e0b;'><h3>💰 حاسبة القسط</h3>", unsafe_allow_html=True)
        p = st.number_input("السعر الكلي", value=1000000, step=100000)
        dp_pct = st.number_input("المقدم %", value=10, step=5)
        dp_val = (dp_pct/100)*p
        remain = p - dp_val
        st.write(f"المقدم: {dp_val:,.0f} | المتبقي: {remain:,.0f}")
        y = st.number_input("سنين القسط", value=7, min_value=1)
        monthly = remain/(y*12) if y > 0 else 0
        st.markdown(f"<h3 style='color:#f59e0b; text-align:center;'>{monthly:,.0f} ج.م/شهرياً</h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div style='background:#111; padding:20px; border-radius:15px; border-right:5px solid #00ffcc;'><h3>📈 حاسبة العائد ROI</h3>", unsafe_allow_html=True)
        inv = st.number_input("إجمالي الاستثمار", value=2000000)
        rent = st.number_input("إيجار متوقع (شهري)", value=15000)
        if inv > 0:
            st.markdown(f"<h3 style='color:#00ffcc; text-align:center;'>{(rent*12/inv)*100:.2f} % سنوياً</h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c3:
        st.markdown("<div style='background:#111; padding:20px; border-radius:15px; border-right:5px solid #fff;'><h3>📱 رسالة عرض</h3>", unsafe_allow_html=True)
        name = st.text_input("اسم العميل")
        proj_list = df['Projects'].unique() if not df.empty else ["-"]
        proj = st.selectbox("المشروع", proj_list)
        if st.button("تجهيز النص"):
            st.code(f"أهلاً {name}، أرشح لك مشروع {proj}.. للتفاصيل تواصل معي.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 🏗️ شاشة المشاريع ---
elif selected == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
    if not df.empty:
        f1, f2, f3 = st.columns([2,1,1])
        with f1: s_p = st.text_input("🔍 ابحث...")
        with f2: a_p = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df['Area'].dropna().unique().tolist()))
        with f3: t_p = st.selectbox("🏠 النوع", ["الكل"] + sorted(df['Type'].dropna().unique().tolist()))
        
        dff_p = df.copy()
        if s_p: dff_p = dff_p[dff_p['Projects'].str.contains(s_p, case=False, na=False)]
        if a_p != "الكل": dff_p = dff_p[dff_p['Area'] == a_p]
        if t_p != "الكل": dff_p = dff_p[dff_p['Type'] == t_p]

        curr_p = dff_p.iloc[:12] # عرض أول 12 مشروع
        for i in range(0, len(curr_p), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(curr_p):
                    row = curr_p.iloc[i+j]
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

# --- 🏢 شاشة المطورين ---
elif selected == "🏢 المطورين":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏢 سجل المطورين</h2>", unsafe_allow_html=True)
    if not df.empty:
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).iloc[:12]
        for i in range(0, len(devs), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(devs):
                    row = devs.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="grid-card">
                                <div class="card-title">🏢 {row.get('Developer', '-')}</div>
                                <div class="card-subtitle">👤 المالك: {row.get('Owner', 'غير مسجل')}</div>
                                <div style="font-size:16px; color:#bbb;">{str(row.get('Detailed_Info', ''))[:150]}...</div>
                            </div>
                        """, unsafe_allow_html=True)
