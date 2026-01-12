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
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; }
    .main-header { background: linear-gradient(90deg, #111 0%, #000 100%); padding: 15px; border-radius: 0 0 15px 15px; border-right: 10px solid #f59e0b; text-align: center; margin-bottom: 20px; }
    .header-title { font-weight: 900; font-size: 30px !important; color: #f59e0b; margin: 0; }
    .pro-card { background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; border-radius: 12px; padding: 20px; margin-bottom: 10px; min-height: 200px; text-align: center; }
    .card-main-title { color: #f59e0b; font-size: 20px !important; font-weight: 900; }
    .stat-row { display: flex; justify-content: space-between; font-size: 14px; margin-top: 8px; color: #ccc; border-bottom: 1px solid #222; padding-bottom: 4px; }
    .stat-val { color: #f59e0b; font-weight: bold; }
    .stButton button { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

# 4. جلب البيانات (معالجة الأخطاء)
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

# 5. القائمة
selected = option_menu(
    menu_title=None, options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], orientation="horizontal",
    styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}}
)

# --- 🏗️ شاشة المشاريع (تعمل الآن بكفاءة) ---
if selected == "🏗️ المشاريع":
    if not df.empty:
        # تهيئة حالة الصفحة للمشاريع
        if 'p_page' not in st.session_state: st.session_state.p_page = 0
        
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
            f1, f2 = st.columns(2)
            with f1: s_p = st.text_input("🔍 ابحث عن اسم المشروع...")
            with f2: 
                areas = sorted(df['Area'].unique().tolist())
                a_p = st.selectbox("📍 المنطقة", ["الكل"] + areas)
            
            # الفلترة
            dff = df.copy()
            if s_p: dff = dff[dff['Projects'].str.contains(s_p, case=False)]
            if a_p != "الكل": dff = dff[dff['Area'] == a_p]

            # نظام الترقيم (9 كروت)
            items = 9
            total_p = math.ceil(len(dff) / items)
            if st.session_state.p_page >= total_p: st.session_state.p_page = 0 # حماية عند تغير البحث
            
            start = st.session_state.p_page * items
            curr_proj = dff.iloc[start : start + items]

            # عرض الشبكة
            for i in range(0, len(curr_proj), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i+j < len(curr_proj):
                        row = curr_proj.iloc[i+j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="pro-card">
                                    <div class="card-main-title">{row['Projects']}</div>
                                    <div style="font-size:14px; color:#888;">{row['Developer']}</div>
                                    <div class="stat-row"><span>📍 الموقع</span><span class="stat-val">{row['Area']}</span></div>
                                    <div class="stat-row"><span>💰 المقدم</span><span class="stat-val">{row['Down_Payment']}</span></div>
                                </div>
                            """, unsafe_allow_html=True)
                            with st.expander("🔍 تفاصيل كاملة"): st.write(row.to_dict())
            
            # أزرار التنقل السفلية
            st.write("---")
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            with nav3:
                if (st.session_state.p_page + 1) < total_p:
                    if st.button("التالي ⬅️", key="next_p"): st.session_state.p_page += 1; st.rerun()
            with nav2: st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.p_page + 1} من {total_p}</p>", unsafe_allow_html=True)
            with nav1:
                if st.session_state.p_page > 0:
                    if st.button("➡️ السابق", key="prev_p"): st.session_state.p_page -= 1; st.rerun()

        with c_side: st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)

# --- 🏢 شاشة المطورين ---
elif selected == "🏢 المطورين":
    if not df.empty:
        if 'd_page' not in st.session_state: st.session_state.d_page = 0
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            st.markdown("<h2 style='color:#f59e0b;'>🏢 المطورين</h2>", unsafe_allow_html=True)
            s_d = st.text_input("🔍 ابحث عن مطور...")
            if s_d: devs = devs[devs['Developer'].str.contains(s_d, case=False)]

            items = 9
            total_d = math.ceil(len(devs) / items)
            start = st.session_state.d_page * items
            curr_devs = devs.iloc[start : start + items]

            for i in range(0, len(curr_devs), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i+j < len(curr_devs):
                        row = curr_devs.iloc[i+j]
                        with cols[j]:
                            st.markdown(f'<div class="pro-card"><div class="card-main-title">{row["Developer"]}</div><div style="color:#888;">👤 {row["Owner"]}</div></div>', unsafe_allow_html=True)
                            with st.expander("📄 سابقة الأعمال"): st.write(row['Detailed_Info'])
            
            st.write("---")
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            with nav3:
                if (st.session_state.d_page + 1) < total_d:
                    if st.button("التالي ⬅️", key="next_d"): st.session_state.d_page += 1; st.rerun()
            with nav2: st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.d_page + 1} من {total_d}</p>", unsafe_allow_html=True)
            with nav1:
                if st.session_state.d_page > 0:
                    if st.button("➡️ السابق", key="prev_d"): st.session_state.d_page -= 1; st.rerun()

# --- 🛠️ شاشة الأدوات ---
elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات البروكر</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='pro-card'><h3>💰 القسط</h3>", unsafe_allow_html=True)
        pr = st.number_input("السعر", value=1000000)
        yr = st.number_input("السنين", value=7, min_value=1)
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
        st.text_area("ملاحظات سريعة...")
        st.markdown("</div>", unsafe_allow_html=True)
