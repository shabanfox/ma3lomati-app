import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; }
    
    .top-bar { display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; background: #000; }
    
    /* زر الخروج */
    .stButton > button[key="logout_btn"] {
        background-color: #ff4b4b !important; color: white !important;
        border: none !important; padding: 5px 20px !important; border-radius: 5px !important;
    }

    .main-header {
        background: linear-gradient(90deg, #111 0%, #000 100%);
        padding: 15px 35px; border-radius: 0 0 15px 15px;
        border-right: 12px solid #f59e0b; text-align: center; margin-bottom: 25px;
    }
    .header-title { font-weight: 900; font-size: 30px !important; color: #f59e0b; margin: 0; }

    .pro-card { 
        background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; 
        border-radius: 12px; padding: 20px; margin-bottom: 10px; text-align: center;
    }
    .card-main-title { color: #f59e0b; font-size: 20px !important; font-weight: 900; }
    .stat-row { display: flex; justify-content: space-between; font-size: 13px; margin-top: 8px; color: #ccc; border-bottom: 1px solid #1a1a1a; padding-bottom: 5px; }
    .stat-val { color: #f59e0b; font-weight: bold; }
    .advantage-box { background: #1a150b; color: #f59e0b; font-size: 12px; padding: 10px; border-radius: 8px; margin-top: 15px; border: 1px dashed #f59e0b; }
    
    input, textarea { background-color: #1a1a1a !important; color: #fff !important; border: 1px solid #333 !important; }
    </style>
""", unsafe_allow_html=True)

# 3. شريط الخروج العلوي
t_col1, t_col2 = st.columns([10, 1])
with t_col2:
    if st.button("خروج", key="logout_btn"):
        st.session_state.clear()
        st.rerun()

# 4. جلب البيانات
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
    menu_title=None, options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], orientation="horizontal",
    styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}}
)

# تهيئة العدادات
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'd_page' not in st.session_state: st.session_state.d_page = 0

# --- 🏗️ شاشة المشاريع ---
if selected == "🏗️ المشاريع":
    if not df.empty:
        c1, c2 = st.columns([0.7, 0.3])
        with c1:
            st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
            f1, f2 = st.columns(2)
            with f1: s_p = st.text_input("🔍 ابحث عن اسم المشروع...")
            with f2: 
                area_col = 'Area' if 'Area' in df.columns else df.columns[0]
                a_p = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df[area_col].unique().tolist()))
            
            dff = df.copy()
            name_col = 'Project Name' if 'Project Name' in df.columns else 'Projects'
            if s_p: dff = dff[dff[name_col].str.contains(s_p, case=False)]
            if a_p != "الكل": dff = dff[dff[area_col] == a_p]

            items = 9
            total_p = max(1, math.ceil(len(dff) / items))
            curr = dff.iloc[st.session_state.p_page * items : (st.session_state.p_page + 1) * items]

            for i in range(0, len(curr), 3):
                cols = st.columns(3)
                for j in range(len(cols)):
                    if i+j < len(curr):
                        row = curr.iloc[i+j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="pro-card">
                                    <div class="card-main-title">{row.get(name_col, '-')}</div>
                                    <div style="color:#888; font-size:13px; margin-bottom:10px;">{row.get('Developer', '-')}</div>
                                    <div class="stat-row"><span>👷 الاستشاري:</span><span class="stat-val">{row.get('Consultant', '-')}</span></div>
                                    <div class="stat-row"><span>📏 المساحة:</span><span class="stat-val">{row.get('Size (Acres)', '-')} فدان</span></div>
                                    <div class="stat-row"><span>🏠 النوع:</span><span class="stat-val">{row.get('شقق/فيلات', '-')}</span></div>
                                    <div class="advantage-box"><b>⭐ ميزة:</b> {row.get('Competitive Advantage', '-')[:80]}</div>
                                </div>
                            """, unsafe_allow_html=True)
            
            # أزرار التنقل
            st.write("---")
            b1, b2, b3 = st.columns([1, 2, 1])
            if b3.button("التالي ⬅️", key="p_n"): st.session_state.p_page += 1; st.rerun()
            if b1.button("➡️ السابق", key="p_p"): st.session_state.p_page -= 1; st.rerun()

# --- 🏢 شاشة المطورين ---
elif selected == "🏢 المطورين":
    if not df.empty:
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        c1, c2 = st.columns([0.7, 0.3])
        with c1:
            st.markdown("<h2 style='color:#f59e0b;'>🏢 المطورين</h2>", unsafe_allow_html=True)
            s_d = st.text_input("🔍 اسم المطور...")
            if s_d: devs = devs[devs['Developer'].str.contains(s_d, case=False)]
            
            curr_devs = devs.iloc[st.session_state.d_page * 9 : (st.session_state.d_page + 1) * 9]
            for i in range(0, len(curr_devs), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i+j < len(curr_devs):
                        row = curr_devs.iloc[i+j]
                        with cols[j]:
                            st.markdown(f'<div class="pro-card"><h3>{row["Developer"]}</h3><p>👤 {row["Owner"]}</p></div>', unsafe_allow_html=True)

# --- 🛠️ شاشة أدوات البروكر (النسخة الكاملة) ---
elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات البروكر الذكية</h2>", unsafe_allow_html=True)
    
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.markdown("<div class='pro-card'><h3>💰 حاسبة القسط</h3>", unsafe_allow_html=True)
        price = st.number_input("إجمالي السعر (جنية)", value=1000000, step=50000)
        down = st.number_input("المقدم (جنية)", value=100000, step=10000)
        years = st.number_input("عدد سنوات التقسيط", value=7, min_value=1)
        monthly = (price - down) / (years * 12) if years > 0 else 0
        st.markdown(f"<h2 style='color:#f59e0b;'>{monthly:,.0f} ج/شهرياً</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with row1_col2:
        st.markdown("<div class='pro-card'><h3>📈 حاسبة ROI (العائد)</h3>", unsafe_allow_html=True)
        total_inv = st.number_input("إجمالي الاستثمار (كاش)", value=1000000, step=50000)
        annual_rent = st.number_input("الإيجار الشهري المتوقع", value=10000) * 12
        roi = (annual_rent / total_inv) * 100 if total_inv > 0 else 0
        st.markdown(f"<h2 style='color:#00ffcc;'>{roi:.1f}% سنوياً</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.markdown("<div class='pro-card'><h3>📏 محول المساحات</h3>", unsafe_allow_html=True)
        acres = st.number_input("المساحة بالفدان", value=1.0)
        meters = acres * 4200
        st.markdown(f"<h2 style='color:#f59e0b;'>{meters:,.0f} متر مربع</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with row2_col2:
        st.markdown("<div class='pro-card'><h3>📝 مسودة الملاحظات</h3>", unsafe_allow_html=True)
        st.text_area("سجل تفاصيل العميل أو طلباته هنا...", height=150)
        st.markdown("</div>", unsafe_allow_html=True)

