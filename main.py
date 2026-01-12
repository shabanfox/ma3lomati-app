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
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }
    .main-header {
        background: linear-gradient(90deg, #111 0%, #000 100%);
        padding: 15px 35px; border-radius: 0 0 15px 15px;
        border: 1px solid #222; border-right: 12px solid #f59e0b;
        text-align: center; margin-bottom: 25px;
    }
    .header-title { font-weight: 900; font-size: 35px !important; color: #f59e0b; margin: 0; }
    .pro-card {
        background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b;
        border-radius: 12px; padding: 20px; margin-bottom: 15px;
        min-height: 220px; text-align: center;
    }
    .card-main-title { color: #f59e0b; font-size: 24px !important; font-weight: 900; }
    .stat-row { display: flex; justify-content: space-between; font-size: 14px; margin-top: 10px; color: #ccc; }
    .stat-val { color: #f59e0b; font-weight: bold; }
    .logout-btn button { background-color: #ff4b4b !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# 3. شريط المهام
t_col1, t_col2 = st.columns([10, 1])
with t_col2:
    if st.button("خروج"):
        st.session_state.clear()
        st.rerun()

# 4. الهيدر
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

# 5. جلب البيانات ومعالجة القيم الفارغة (حل المشكلة)
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        # استبدال أي قيمة فارغة بنص "غير محدد" لمنع أخطاء الترتيب
        data = data.fillna("غير محدد") 
        return data
    except: return pd.DataFrame()

df = load_data()

# 6. القائمة
selected = option_menu(
    menu_title=None, options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], orientation="horizontal",
    styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}}
)

# --- 🏗️ شاشة المشاريع (المعدلة لمنع الخطأ) ---
if selected == "🏗️ المشاريع":
    if not df.empty:
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
            f1, f2 = st.columns(2)
            with f1: s_p = st.text_input("🔍 اسم المشروع...")
            with f2:
                # حل المشكلة: تنظيف قائمة المناطق من القيم غير النصية قبل الترتيب
                area_list = sorted([str(x) for x in df['Area'].unique() if x != "غير محدد"])
                a_p = st.selectbox("📍 المنطقة", ["الكل"] + area_list)
            
            dff = df.copy()
            if s_p: dff = dff[dff['Projects'].astype(str).str.contains(s_p, case=False, na=False)]
            if a_p != "الكل": dff = dff[dff['Area'] == a_p]

            items = 9
            pages = max(1, math.ceil(len(dff)/items))
            page = st.number_input("الصفحة ", min_value=1, max_value=pages, step=1)
            curr = dff.iloc[(page-1)*items : page*items]

            for i in range(0, len(curr), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i+j < len(curr):
                        row = curr.iloc[i+j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="pro-card">
                                    <div class="card-main-title">{row['Projects']}</div>
                                    <div class="card-sub-title">{row['Developer']}</div>
                                    <div class="stat-row"><span>📍 الموقع:</span><span class="stat-val">{row['Area']}</span></div>
                                    <div class="stat-row"><span>💰 المقدم:</span><span class="stat-val">{row['Down_Payment']}</span></div>
                                </div>
                            """, unsafe_allow_html=True)
                            with st.expander("🔍 تفاصيل"): st.write(row.to_dict())
        with c_side:
            st.markdown("<div style='height:500px; border-right:1px solid #222; opacity:0.1; margin-right:30px;'></div>", unsafe_allow_html=True)

# --- 🏢 شاشة المطورين ---
elif selected == "🏢 المطورين":
    if not df.empty:
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            st.markdown("<h2 style='color:#f59e0b;'>🏢 المطورين</h2>", unsafe_allow_html=True)
            s_d = st.text_input("🔍 ابحث عن مطور...")
            if s_d: devs = devs[devs['Developer'].astype(str).str.contains(s_d, case=False, na=False)]
            
            items = 9
            pages = max(1, math.ceil(len(devs)/items))
            p_num = st.number_input("الصفحة", min_value=1, max_value=pages, step=1)
            curr = devs.iloc[(p_num-1)*items : p_num*items]

            for i in range(0, len(curr), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i+j < len(curr):
                        row = curr.iloc[i+j]
                        with cols[j]:
                            st.markdown(f'<div class="pro-card"><div class="card-main-title">{row["Developer"]}</div><div class="card-sub-title">👤 {row["Owner"]}</div></div>', unsafe_allow_html=True)
                            with st.expander("🔍 التفاصيل"): st.write(row['Detailed_Info'])
        with c_side:
            st.markdown("<div style='height:500px; border-right:1px solid #222; opacity:0.1; margin-right:30px;'></div>", unsafe_allow_html=True)

# --- 🛠️ شاشة الأدوات ---
elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ الأدوات</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='pro-card'><h3>💰 حاسبة القسط</h3>", unsafe_allow_html=True)
        price = st.number_input("السعر الكلي", value=1000000)
        years = st.number_input("السنين", value=7, min_value=1)
        st.markdown(f"<h2 style='color:#f59e0b;'>{price/(years*12):,.0f}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='pro-card'><h3>📈 ROI</h3>", unsafe_allow_html=True)
        inv = st.number_input("الاستثمار", value=1000000)
        rent = st.number_input("الإيجار", value=10000)
        st.markdown(f"<h2 style='color:#00ffcc;'>{(rent*12/inv)*100:.1f}%</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='pro-card'><h3>📱 مسودة</h3>", unsafe_allow_html=True)
        st.text_area("ملاحظاتك للعميل...")
        st.markdown("</div>", unsafe_allow_html=True)
