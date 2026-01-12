import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. هندسة التصميم (CSS) - شريط المهام والهيدر والكروت
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; 
        text-align: right; 
        font-family: 'Cairo', sans-serif;
    }

    /* شريط المهام العلوي (Top Bar) */
    .top-bar {
        background: #111;
        padding: 5px 20px;
        border-bottom: 2px solid #f59e0b;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    /* الهيدر الرئيسي */
    .main-header {
        background: linear-gradient(90deg, #111 0%, #000 100%);
        padding: 35px;
        border-radius: 15px;
        border: 1px solid #222;
        border-right: 12px solid #f59e0b;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .header-title {
        font-weight: 900;
        font-size: 48px !important;
        color: #f59e0b;
        margin: 0;
    }

    /* كروت البيانات */
    .grid-card {
        background: linear-gradient(145deg, #111, #080808);
        border: 1px solid #222;
        border-top: 5px solid #f59e0b;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 15px;
        min-height: 420px;
        height: auto;
        transition: 0.3s all;
        direction: rtl;
        text-align: right;
    }
    .grid-card:hover { border-color: #f59e0b; transform: translateY(-5px); box-shadow: 0 5px 15px rgba(245,158,11,0.2); }
    
    /* أحجام الخطوط الكبيرة */
    .card-title { 
        color: #f59e0b; 
        font-size: 32px !important; 
        font-weight: 900 !important; 
        margin-bottom: 8px; 
        line-height: 1.2;
    }
    .card-subtitle { 
        color: #ffffff; 
        font-size: 24px !important; 
        font-weight: 700 !important; 
        margin-bottom: 15px; 
        border-bottom: 2px solid #333; 
        padding-bottom: 8px; 
    }
    
    .stat-line { display: flex; justify-content: space-between; font-size: 16px; margin-bottom: 10px; }
    .stat-label { color: #888; }
    .stat-value { color: #f59e0b; font-weight: bold; }

    .badge-gold { 
        background: #f59e0b; 
        color: black; 
        padding: 5px 15px; 
        border-radius: 5px; 
        font-weight: 900; 
        font-size: 18px; 
        align-self: flex-start; 
        margin-bottom: 15px; 
    }

    /* تخصيص زر الخروج */
    div[data-testid="stColumn"]:nth-child(2) button {
        background-color: #ff4b4b !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. شريط المهام (Top Bar)
top_col1, top_col2 = st.columns([9, 1])
with top_col1:
    st.markdown('<div style="padding-top:10px; color:#888;">نظام إدارة المعلومات العقارية | v2.0</div>', unsafe_allow_html=True)
with top_col2:
    if st.button("خروج"):
        st.session_state.clear()
        st.rerun()

# 4. الهيدر
st.markdown("""
    <div class="main-header">
        <h1 class="header-title">🏢 منصة معلوماتي العقارية</h1>
        <p style="color: #666; font-size: 18px; margin-top:10px;">دليل المطورين والمشاريع الأكثر دقة في مصر</p>
    </div>
""", unsafe_allow_html=True)

# 5. جلب البيانات من Google Sheets
@st.cache_data(ttl=300)
def load_all_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except Exception as e:
        st.error("عذراً، تعذر تحميل البيانات حالياً.")
        return pd.DataFrame()

df = load_all_data()

# 6. قائمة التنقل (Option Menu)
selected = option_menu(
    menu_title=None, 
    options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], 
    default_index=0, 
    orientation="horizontal",
    styles={
        "container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"},
        "nav-link": {"font-size": "18px", "color":"white", "font-family": "Cairo"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"},
    }
)

# --- شاشة أدوات البروكر ---
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
        if inv > 0: st.markdown(f"<h3 style='color:#00ffcc; text-align:center;'>{(rent*12/inv)*100:.2f} % سنوياً</h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div style='background:#111; padding:20px; border-radius:15px; border-right:5px solid #fff;'><h3>📱 رسالة عرض</h3>", unsafe_allow_html=True)
        name = st.text_input("اسم العميل")
        proj_opt = df['Projects'].unique() if not df.empty else ["-"]
        proj = st.selectbox("المشروع", proj_opt)
        if st.button("تجهيز النص"): st.code(f"أهلاً {name}، أرشح لك مشروع {proj}.. للتفاصيل تواصل معي.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- شاشة المشاريع ---
elif selected == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
    if not df.empty:
        f1, f2, f3 = st.columns([2,1,1])
        with f1: s_p = st.text_input("🔍 ابحث عن اسم المشروع...")
        with f2: a_p = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df['Area'].dropna().unique().tolist()))
        with f3: t_p = st.selectbox("🏠 النوع", ["الكل"] + sorted(df['Type'].dropna().unique().tolist()))
        
        dff_p = df.copy()
        if s_p: dff_p = dff_p[dff_p['Projects'].str.contains(s_p, case=False, na=False)]
        if a_p != "الكل": dff_p = dff_p[dff_p['Area'] == a_p]
        if t_p != "الكل": dff_p = dff_p[dff_p['Type'] == t_p]

        items_p = 9
        pages_p = max(1, math.ceil(len(dff_p)/items_p))
        if 'pg_p' not in st.session_state: st.session_state.pg_p = 1
        curr_p = dff_p.iloc[(st.session_state.pg_p-1)*items_p : st.session_state.pg_p*items_p]

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
                                <div class="badge-gold">بدأ من: {row.get('Min_Val (Start Price)','0')}</div>
                                <div class="stat-line"><span class="stat-label">📍 الموقع:</span><span class="stat-value">{row.get('Area','-')}</span></div>
                                <div class="stat-line"><span class="stat-label">💰 المقدم:</span><span class="stat-value">{row.get('Down_Payment','-')}</span></div>
                                <div class="stat-line"><span class="stat-label">⏳ التقسيط:</span><span class="stat-value">{row.get('Installments','-')}</span></div>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("🔍 تفاصيل إضافية"): st.write(row.to_dict())

# --- شاشة المطورين ---
elif selected == "🏢 المطورين":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏢 سجل المطورين العقاريين</h2>", unsafe_allow_html=True)
    if not df.empty:
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        s_d = st.text_input("🔍 ابحث عن اسم المطور...")
        if s_d: devs = devs[devs['Developer'].str.contains(s_d, case=False, na=False)]

        items_d = 9
        pages_d = max(1, math.ceil(len(devs)/items_d))
        if 'pg_d' not in st.session_state: st.session_state.pg_d = 1
        curr_d = devs.iloc[(st.session_state.pg_d-1)*items_d : st.session_state.pg_d*items_d]

        for i in range(0, len(curr_d), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(curr_d):
                    row = curr_d.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="grid-card">
                                <div class="card-title">🏢 {row.get('Developer', '-')}</div>
                                <div class="card-subtitle">👤 المالك: {row.get('Owner', 'غير مسجل')}</div>
                                <div style="font-size:16px; color:#bbb; flex-grow:1; overflow:hidden;">
                                    <b>نبذة عن الشركة:</b><br>{str(row.get('Detailed_Info', 'لا توجد تفاصيل'))[:220]}...
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("📄 سابقة الأعمال"): st.write(row.get('Detailed_Info'))
