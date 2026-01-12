import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }

    /* الهيدر */
    .main-header {
        background: linear-gradient(90deg, #111 0%, #000 100%);
        padding: 15px 35px; border-radius: 0 0 15px 15px;
        border: 1px solid #222; border-right: 12px solid #f59e0b;
        text-align: center; margin-bottom: 25px;
    }
    .header-title { font-weight: 900; font-size: 35px !important; color: #f59e0b; margin: 0; }

    /* الكروت */
    .pro-card { 
        background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; 
        border-radius: 12px; padding: 20px; margin-bottom: 10px; 
        min-height: 320px; text-align: center; display: flex; flex-direction: column; justify-content: space-between;
    }
    .card-main-title { color: #f59e0b; font-size: 20px !important; font-weight: 900; margin-bottom: 5px; }
    .dev-label { color: #888; font-size: 14px; margin-bottom: 15px; }
    
    .stat-row { display: flex; justify-content: space-between; font-size: 13px; margin-top: 8px; color: #ccc; border-bottom: 1px solid #1a1a1a; padding-bottom: 5px; }
    .stat-val { color: #f59e0b; font-weight: bold; }
    
    .advantage-box { 
        background: #1a150b; color: #f59e0b; font-size: 12px; padding: 10px; 
        border-radius: 8px; margin-top: 15px; border: 1px dashed #f59e0b; 
        text-align: right; line-height: 1.6;
    }

    /* الأزرار */
    .stButton button { 
        width: 100%; background-color: #1a1a1a !important; color: #f59e0b !important; 
        border: 1px solid #333 !important; font-weight: bold; border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. وظيفة جلب البيانات
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        data = data.fillna("غير متوفر").astype(str)
        return data
    except:
        return pd.DataFrame()

df = load_data()

# 4. الهيدر والقائمة العلوية
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

selected = option_menu(
    menu_title=None, 
    options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], 
    orientation="horizontal",
    styles={
        "container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"},
        "nav-link": {"font-family": "Cairo", "font-weight": "bold"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}
    }
)

# تهيئة عدادات الصفحات في الـ Session State
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'd_page' not in st.session_state: st.session_state.d_page = 0

# --- 🏗️ شاشة المشاريع (70% يمين | 30% يسار) ---
if selected == "🏗️ المشاريع":
    if not df.empty:
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            st.markdown("<h2 style='color:#f59e0b; margin-bottom:20px;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
            
            # فلاتر البحث
            f1, f2 = st.columns(2)
            with f1: s_p = st.text_input("🔍 ابحث عن مشروع...")
            with f2: 
                area_col = 'Area' if 'Area' in df.columns else df.columns[0]
                areas = ["الكل"] + sorted(df[area_col].unique().tolist())
                a_p = st.selectbox("📍 تصفية بالمنطقة", areas)
            
            # معالجة البيانات والفلترة
            dff = df.copy()
            name_col = 'Project Name' if 'Project Name' in df.columns else 'Projects'
            if s_p: dff = dff[dff[name_col].str.contains(s_p, case=False)]
            if a_p != "الكل": dff = dff[dff[area_col] == a_p]

            # نظام الـ 9 كروت
            items = 9
            total_p = max(1, math.ceil(len(dff) / items))
            if st.session_state.p_page >= total_p: st.session_state.p_page = 0
            
            curr_slice = dff.iloc[st.session_state.p_page * items : (st.session_state.p_page + 1) * items]

            # عرض الشبكة 3x3
            for i in range(0, len(curr_slice), 3):
                grid_cols = st.columns(3)
                for j in grid_cols:
                    idx = i + grid_cols.index(j)
                    if idx < len(curr_slice):
                        row = curr_slice.iloc[idx]
                        with j:
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
                                    <div class="advantage-box">
                                        <b>⭐ الميزة التنافسية:</b><br>{row.get('Competitive Advantage', 'لا توجد تفاصيل')}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)

            # أزرار التنقل السفلية
            st.write("---")
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            with nav3:
                if (st.session_state.p_page + 1) < total_p:
                    if st.button("التالي ⬅️", key="p_next"): st.session_state.p_page += 1; st.rerun()
            with nav2: st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.p_page + 1} من {total_p}</p>", unsafe_allow_html=True)
            with nav1:
                if st.session_state.p_page > 0:
                    if st.button("➡️ السابق", key="p_prev"): st.session_state.p_page -= 1; st.rerun()

        with c_side:
            st.markdown("<div style='border-right:1px solid #222; height:800px; opacity:0.1; margin-right:30px;'></div>", unsafe_allow_html=True)

# --- 🏢 شاشة المطورين (70% يمين | 30% يسار) ---
elif selected == "🏢 المطورين":
    if not df.empty:
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            st.markdown("<h2 style='color:#f59e0b;'>🏢 المطورين العقاريين</h2>", unsafe_allow_html=True)
            s_d = st.text_input("🔍 ابحث عن مطور...")
            if s_d: devs = devs[devs['Developer'].str.contains(s_d, case=False)]

            total_d = max(1, math.ceil(len(devs) / 9))
            curr_devs = devs.iloc[st.session_state.d_page * 9 : (st.session_state.d_page + 1) * 9]

            for i in range(0, len(curr_devs), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i+j < len(curr_devs):
                        row = curr_devs.iloc[i+j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="pro-card" style="min-height:200px;">
                                    <div class="card-main-title">{row['Developer']}</div>
                                    <div class="dev-label">👤 {row['Owner']}</div>
                                    <div style="font-size:12px; color:#aaa; text-align:right;">{row['Detailed_Info'][:150]}...</div>
                                </div>
                            """, unsafe_allow_html=True)

            st.write("---")
            n1, n2, n3 = st.columns([1, 2, 1])
            with n3:
                if (st.session_state.d_page + 1) < total_d:
                    if st.button("التالي ⬅️", key="d_next"): st.session_state.d_page += 1; st.rerun()
            with n2: st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.d_page + 1} من {total_d}</p>", unsafe_allow_html=True)
            with n1:
                if st.session_state.d_page > 0:
                    if st.button("➡️ السابق", key="d_prev"): st.session_state.d_page -= 1; st.rerun()

# --- 🛠️ شاشة أدوات البروكر ---
elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ الأدوات الذكية</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='pro-card' style='min-height:250px;'><h3>💰 حاسبة القسط</h3>", unsafe_allow_html=True)
        p = st.number_input("إجمالي السعر", value=1000000)
        y = st.number_input("السنين", value=7, min_value=1)
        st.subheader(f"{p/(y*12):,.0f} ج/شهري")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='pro-card' style='min-height:250px;'><h3>📈 حاسبة ROI</h3>", unsafe_allow_html=True)
        inv = st.number_input("الاستثمار", value=1000000)
        rent = st.number_input("الإيجار", value=10000)
        st.subheader(f"{(rent*12/inv)*100:.1f}% سنوياً")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='pro-card' style='min-height:250px;'><h3>📱 مسودة سريعة</h3>", unsafe_allow_html=True)
        st.text_area("سجل ملاحظات العميل...")
        st.markdown("</div>", unsafe_allow_html=True)
