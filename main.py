import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS) - النسخة المطورة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }

    /* زر الخروج */
    .stButton > button[key="logout_btn"] {
        background-color: #ff4b4b !important; color: white !important;
        border: none !important; padding: 5px 20px !important; border-radius: 5px !important;
        width: auto !important;
    }

    /* الهيدر الرئيسي */
    .main-header {
        background: linear-gradient(90deg, #111 0%, #000 100%);
        padding: 15px 35px; border-radius: 0 0 15px 15px;
        border: 1px solid #222; border-right: 12px solid #f59e0b;
        text-align: center; margin-bottom: 25px;
    }
    .header-title { font-weight: 900; font-size: 30px !important; color: #f59e0b; margin: 0; }

    /* تصميم الكروت */
    .pro-card { 
        background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; 
        border-radius: 12px; padding: 20px; margin-bottom: 10px; 
        min-height: 320px; text-align: center; display: flex; flex-direction: column; justify-content: space-between;
    }
    .card-main-title { color: #f59e0b; font-size: 20px !important; font-weight: 900; margin-bottom: 5px; }
    .dev-label { color: #888; font-size: 14px; margin-bottom: 15px; }
    
    .stat-row { display: flex; justify-content: space-between; font-size: 13px; margin-top: 8px; color: #ccc; border-bottom: 1px solid #1a1a1a; padding-bottom: 5px; }
    .stat-val { color: #f59e0b; font-weight: bold; }
    
    /* صندوق الميزة التنافسية والـ Owner */
    .info-box { 
        background: #1a150b; color: #f59e0b; font-size: 12px; padding: 10px; 
        border-radius: 8px; margin-top: 10px; border: 1px dashed #f59e0b; 
        text-align: right; line-height: 1.6;
    }

    /* الأزرار */
    .stButton button { 
        width: 100%; background-color: #1a1a1a !important; color: #f59e0b !important; 
        border: 1px solid #333 !important; font-weight: bold; border-radius: 8px; height: 45px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. شريط الخروج العلوي
col_t1, col_t2 = st.columns([10, 1])
with col_t2:
    if st.button("خروج", key="logout_btn"):
        st.session_state.clear()
        st.rerun()

# 4. وظيفة جلب البيانات
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        data = data.fillna("غير متوفر").astype(str)
        return data
    except: return pd.DataFrame()

df = load_data()

# 5. الهيدر والقائمة
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

selected = option_menu(
    menu_title=None, 
    options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], 
    orientation="horizontal",
    styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}}
)

# تهيئة عدادات الصفحات
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'd_page' not in st.session_state: st.session_state.d_page = 0

# --- 🏗️ شاشة المشاريع (70% يمين | 30% يسار) ---
if selected == "🏗️ المشاريع":
    if not df.empty:
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع التفصيلي</h2>", unsafe_allow_html=True)
            f1, f2 = st.columns(2)
            with f1: s_p = st.text_input("🔍 ابحث باسم المشروع...")
            with f2: 
                area_col = 'Area' if 'Area' in df.columns else df.columns[0]
                a_p = st.selectbox("📍 تصفية بالمنطقة", ["الكل"] + sorted(df[area_col].unique().tolist()))
            
            dff = df.copy()
            name_col = 'Project Name' if 'Project Name' in df.columns else 'Projects'
            if s_p: dff = dff[dff[name_col].str.contains(s_p, case=False)]
            if a_p != "الكل": dff = dff[dff[area_col] == a_p]

            items = 9
            total_p = max(1, math.ceil(len(dff) / items))
            if st.session_state.p_page >= total_p: st.session_state.p_page = 0
            
            curr = dff.iloc[st.session_state.p_page * items : (st.session_state.p_page + 1) * items]

            for i in range(0, len(curr), 3):
                grid_cols = st.columns(3)
                for j in range(len(grid_cols)):
                    idx = i + j
                    if idx < len(curr):
                        row = curr.iloc[idx]
                        with grid_cols[j]:
                            st.markdown(f"""
                                <div class="pro-card">
                                    <div>
                                        <div class="card-main-title">{row.get(name_col, '-')}</div>
                                        <div class="dev-label">{row.get('Developer', '-')}</div>
                                        <div class="stat-row"><span>👷 الاستشاري:</span><span class="stat-val">{row.get('Consultant', '-')}</span></div>
                                        <div class="stat-row"><span>📏 المساحة:</span><span class="stat-val">{row.get('Size (Acres)', '-')} فدان</span></div>
                                        <div class="stat-row"><span>🏠 النوع:</span><span class="stat-val">{row.get('شقق/فيلات', '-')}</span></div>
                                        <div class="stat-row"><span>📍 الموقع:</span><span class="stat-val">{row.get('Area', '-')}</span></div>
                                    </div>
                                    <div class="info-box"><b>⭐ الميزة التنافسية:</b><br>{row.get('Competitive Advantage', 'غير متوفرة')}</div>
                                </div>
                            """, unsafe_allow_html=True)

            # أزرار التنقل
            st.write("---")
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            if nav3.button("التالي ⬅️", key="p_next"): st.session_state.p_page += 1; st.rerun()
            nav2.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.p_page + 1} من {total_p}</p>", unsafe_allow_html=True)
            if nav1.button("➡️ السابق", key="p_prev") and st.session_state.p_page > 0: st.session_state.p_page -= 1; st.rerun()

# --- 🏢 شاشة المطورين (تطوير بيانات الـ Owner) ---
elif selected == "🏢 المطورين":
    if not df.empty:
        devs_raw = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            st.markdown("<h2 style='color:#f59e0b;'>🏢 المطورين العقاريين</h2>", unsafe_allow_html=True)
            s_d = st.text_input("🔍 ابحث عن مطور...")
            if s_d: devs_raw = devs_raw[devs_raw['Developer'].str.contains(s_d, case=False)]

            items = 9
            total_d = max(1, math.ceil(len(devs_raw) / items))
            curr_devs = devs_raw.iloc[st.session_state.d_page * items : (st.session_state.d_page + 1) * items]

            for i in range(0, len(curr_devs), 3):
                cols = st.columns(3)
                for j in range(len(cols)):
                    idx = i + j
                    if idx < len(curr_devs):
                        row = curr_devs.iloc[idx]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="pro-card" style="min-height:260px;">
                                    <div class="card-main-title">{row['Developer']}</div>
                                    <div class="info-box" style="background:#000; border:1px solid #222;">
                                        <div style="color:#888; font-size:11px;">👤 المالك / رئيس مجلس الإدارة:</div>
                                        <div style="color:#f59e0b; font-weight:bold; font-size:15px;">{row['Owner']}</div>
                                    </div>
                                    <div style="font-size:12px; color:#666; margin-top:10px;">{row['Detailed_Info'][:120]}...</div>
                                </div>
                            """, unsafe_allow_html=True)

            # أزرار التنقل المطورين
            st.write("---")
            d1, d2, d3 = st.columns([1, 2, 1])
            if d3.button("التالي ⬅️", key="d_next"): st.session_state.d_page += 1; st.rerun()
            d2.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.d_page + 1} من {total_d}</p>", unsafe_allow_html=True)
            if d1.button("➡️ السابق", key="d_prev") and st.session_state.d_page > 0: st.session_state.d_page -= 1; st.rerun()

# --- 🛠️ شاشة أدوات البروكر (كاملة) ---
elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات البروكر الذكية</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='pro-card'><h3>💰 حاسبة القسط</h3>", unsafe_allow_html=True)
        price = st.number_input("إجمالي السعر", value=1000000, step=100000)
        years = st.number_input("السنين", value=7, min_value=1)
        st.markdown(f"<h2 style='color:#f59e0b;'>{price/(years*12):,.0f} ج/شهري</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='pro-card'><h3>📏 محول المساحة</h3>", unsafe_allow_html=True)
        acre = st.number_input("المساحة بالفدان", value=1.0)
        st.markdown(f"<h2 style='color:#f59e0b;'>{acre*4200:,.0f} متر مربع</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    st.text_area("📝 مسودة ملاحظات العميل السريعة...", height=150)
