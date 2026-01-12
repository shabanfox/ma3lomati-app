import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. هندسة التصميم (CSS) - تقليل الفراغات العلوية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* حذف هوامش Streamlit الافتراضية */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }

    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }

    /* شريط المهام العلوي (Top Bar) */
    .top-bar {
        background: #111;
        padding: 5px 25px;
        border-bottom: 2px solid #f59e0b;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0px; /* إلغاء الفراغ تحت التوب بار */
    }

    /* الهيدر الرئيسي - تعديل المسافات */
    .main-header {
        background: linear-gradient(90deg, #111 0%, #000 100%);
        padding: 20px 35px; /* تقليل البادينج الداخلي */
        border-radius: 0 0 15px 15px; /* تدوير الحواف السفلية فقط */
        border: 1px solid #222;
        border-right: 12px solid #f59e0b;
        text-align: center;
        margin-top: 0px !important; /* إلغاء الفراغ فوق الهيدر */
        margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    .header-title { font-weight: 900; font-size: 40px !important; color: #f59e0b; margin: 0; }

    /* كروت البيانات */
    .grid-card {
        background: linear-gradient(145deg, #111, #080808);
        border: 1px solid #222;
        border-top: 5px solid #f59e0b;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 15px;
        min-height: 400px;
        transition: 0.3s all;
        direction: rtl; text-align: right;
    }
    
    .card-title { color: #f59e0b; font-size: 30px !important; font-weight: 900 !important; margin-bottom: 8px; }
    .card-subtitle { color: #ffffff; font-size: 22px !important; font-weight: 700 !important; border-bottom: 2px solid #333; padding-bottom: 8px; margin-bottom: 15px; }
    
    .stat-line { display: flex; justify-content: space-between; font-size: 16px; margin-bottom: 10px; }
    .stat-value { color: #f59e0b; font-weight: bold; }

    /* تنسيق زر الخروج */
    div[data-testid="stColumn"] button {
        background-color: #ff4b4b !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. شريط المهام (Top Bar) مدمج
t_col1, t_col2 = st.columns([9, 1])
with t_col1:
    st.markdown('<div style="padding-top:15px; color:#888; font-size:14px;">نظام معلوماتي العقاري PRO 2026</div>', unsafe_allow_html=True)
with t_col2:
    if st.button("خروج"):
        st.session_state.clear()
        st.rerun()

# 4. الهيدر (ملتصق بالأعلى)
st.markdown("""
    <div class="main-header">
        <h1 class="header-title">🏢 منصة معلوماتي العقارية</h1>
    </div>
""", unsafe_allow_html=True)

# 5. جلب البيانات
@st.cache_data(ttl=300)
def load_all_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except:
        return pd.DataFrame()

df = load_all_data()

# 6. قائمة التنقل
selected = option_menu(
    menu_title=None, 
    options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], 
    default_index=0, 
    orientation="horizontal",
    styles={
        "container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b", "padding": "0!important"},
        "nav-link": {"font-size": "18px", "color":"white", "font-family": "Cairo"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"},
    }
)

# --- شاشات العرض ---
if selected == "🏗️ المشاريع":
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
                                <div class="stat-line"><span class="stat-label">📍 الموقع:</span><span class="stat-value">{row.get('Area','-')}</span></div>
                                <div class="stat-line"><span class="stat-label">💰 المقدم:</span><span class="stat-value">{row.get('Down_Payment','-')}</span></div>
                                <div class="stat-line"><span class="stat-label">⏳ التقسيط:</span><span class="stat-value">{row.get('Installments','-')}</span></div>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("🔍 تفاصيل"): st.write(row.to_dict())

elif selected == "🏢 المطورين":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏢 سجل المطورين</h2>", unsafe_allow_html=True)
    if not df.empty:
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        s_d = st.text_input("🔍 ابحث عن المطور...")
        if s_d: devs = devs[devs['Developer'].str.contains(s_d, case=False, na=False)]
        
        for i in range(0, len(devs.iloc[:9]), 3): # عرض أول 9 مطورين
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

elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدواتك</h2>", unsafe_allow_html=True)
    st.info("استخدم الحاسبات المتاحة في الأعلى لتسهيل عملك مع العملاء.")
