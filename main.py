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
        border-radius: 12px; padding: 20px; margin-bottom: 10px;
        min-height: 200px; text-align: center;
    }
    .card-main-title { color: #f59e0b; font-size: 22px !important; font-weight: 900; }
    .stat-row { display: flex; justify-content: space-between; font-size: 14px; margin-top: 8px; color: #ccc; }
    .stat-val { color: #f59e0b; font-weight: bold; }
    
    /* تنسيق أزرار التنقل */
    .stButton button { background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #f59e0b !important; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

# 4. جلب البيانات
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        data = data.astype(str).replace(['nan', 'None', ''], 'غير متوفر')
        return data
    except: return pd.DataFrame()

df = load_data()

# 5. القائمة
selected = option_menu(
    menu_title=None, options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], orientation="horizontal",
    styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}}
)

# --- 🏢 شاشة المطورين ---
if selected == "🏢 المطورين":
    if not df.empty:
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            st.markdown("<h2 style='color:#f59e0b;'>🏢 المطورين العقاريين</h2>", unsafe_allow_html=True)
            s_d = st.text_input("🔍 ابحث عن مطور...")
            if s_d: devs = devs[devs['Developer'].str.contains(s_d, case=False, na=False)]
            
            # نظام التنقل 9 كروت
            if 'dev_page' not in st.session_state: st.session_state.dev_page = 0
            items_per_page = 9
            total_pages = math.ceil(len(devs) / items_per_page)
            
            curr = devs.iloc[st.session_state.dev_page * items_per_page : (st.session_state.dev_page + 1) * items_per_page]

            for i in range(0, len(curr), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i+j < len(curr):
                        row = curr.iloc[i+j]
                        with cols[j]:
                            st.markdown(f'<div class="pro-card"><div class="card-main-title">{row["Developer"]}</div><div class="card-sub-title">👤 {row["Owner"]}</div></div>', unsafe_allow_html=True)
                            with st.expander("🔍 التفاصيل"): st.write(row['Detailed_Info'])
            
            # أزرار التنقل تحت في صفحة المطورين
            st.write("---")
            nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
            with nav_col3:
                if (st.session_state.dev_page + 1) < total_pages:
                    if st.button("التالي ⬅️"):
                        st.session_state.dev_page += 1
                        st.rerun()
            with nav_col2:
                st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.dev_page + 1} من {total_pages}</p>", unsafe_allow_html=True)
            with nav_col1:
                if st.session_state.dev_page > 0:
                    if st.button("➡️ السابق"):
                        st.session_state.dev_page -= 1
                        st.rerun()

# --- 🏗️ شاشة المشاريع ---
elif selected == "🏗️ المشاريع":
    if not df.empty:
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
            f1, f2 = st.columns(2)
            with f1: s_p = st.text_input("🔍 ابحث عن مشروع...")
            with f2:
                area_list = sorted(df['Area'].unique().tolist())
                a_p = st.selectbox("📍 المنطقة", ["الكل"] + area_list)
            
            dff = df.copy()
            if s_p: dff = dff[dff['Projects'].str.contains(s_p, case=False, na=False)]
            if a_p != "الكل": dff = dff[dff['Area'] == a_p]

            # نظام التنقل 9 كروت
            if 'proj_page' not in st.session_state: st.session_state.proj_page = 0
            items_per_page = 9
            total_pages = math.ceil(len(dff) / items_per_page)
            
            curr = dff.iloc[st.session_state.proj_page * items_per_page : (st.session_state.proj_page + 1) * items_per_page]

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
                            with st.expander("🔍 التفاصيل"): st.write(row.to_dict())
            
            # أزرار التنقل تحت في صفحة المشاريع
            st.write("---")
            pnav_col1, pnav_col2, pnav_col3 = st.columns([1, 2, 1])
            with pnav_col3:
                if (st.session_state.proj_page + 1) < total_pages:
                    if st.button("التالي (مشاريع) ⬅️"):
                        st.session_state.proj_page += 1
                        st.rerun()
            with pnav_col2:
                st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.proj_page + 1} من {total_pages}</p>", unsafe_allow_html=True)
            with pnav_col1:
                if st.session_state.proj_page > 0:
                    if st.button("➡️ السابق (مشاريع)"):
                        st.session_state.proj_page -= 1
                        st.rerun()

# --- 🛠️ شاشة الأدوات ---
elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات البروكر</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='pro-card'><h3>💰 حاسبة القسط</h3>", unsafe_allow_html=True)
        pr = st.number_input("السعر", value=1000000)
        yr = st.number_input("السنين", value=7)
        st.subheader(f"{pr/(yr*12):,.0f} ج/شهري")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='pro-card'><h3>📈 ROI</h3>", unsafe_allow_html=True)
        inv = st.number_input("الاستثمار", value=1000000)
        rent = st.number_input("الإيجار", value=10000)
        st.subheader(f"{(rent*12/inv)*100:.1f}%")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='pro-card'><h3>📝 مسودة</h3>", unsafe_allow_html=True)
        st.text_area("اكتب ملاحظات العميل هنا...")
        st.markdown("</div>", unsafe_allow_html=True)
