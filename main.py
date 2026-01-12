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
    .pro-card { background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; border-radius: 12px; padding: 20px; margin-bottom: 10px; min-height: 220px; text-align: center; }
    .card-main-title { color: #f59e0b; font-size: 20px !important; font-weight: 900; }
    .stat-row { display: flex; justify-content: space-between; font-size: 14px; margin-top: 8px; color: #ccc; border-bottom: 1px solid #222; padding-bottom: 4px; }
    .stat-val { color: #f59e0b; font-weight: bold; }
    .stButton button { width: 100%; border-radius: 8px; font-weight: bold; height: 45px; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        data = data.fillna("غير متوفر").astype(str)
        return data
    except Exception as e:
        st.error(f"حدث خطأ في الاتصال بالبيانات: {e}")
        return pd.DataFrame()

df = load_data()

# 4. الهيدر والقائمة
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
selected = option_menu(
    menu_title=None, options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], orientation="horizontal",
    styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}}
)

# --- نظام التحكم في الصفحات ---
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0

# --- 🏗️ شاشة المشاريع (تم التعديل لـ Project Name) ---
if selected == "🏗️ المشاريع":
    if not df.empty:
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
            
            f1, f2 = st.columns(2)
            with f1: s_p = st.text_input("🔍 ابحث عن مشروع...", placeholder="اكتب اسم المشروع هنا")
            with f2: 
                area_col = 'Area' if 'Area' in df.columns else df.columns[0]
                areas = ["الكل"] + sorted(df[area_col].unique().tolist())
                a_p = st.selectbox("📍 تصفية حسب المنطقة", areas)
            
            # تطبيق الفلترة باستخدام Project Name
            dff = df.copy()
            # التأكد من اسم العمود الصحيح
            name_col = 'Project Name' if 'Project Name' in df.columns else 'Projects'
            
            if s_p: dff = dff[dff[name_col].str.contains(s_p, case=False)]
            if a_p != "الكل": dff = dff[dff[area_col] == a_p]

            items = 9
            total_p = max(1, math.ceil(len(dff) / items))
            if st.session_state.p_idx >= total_p: st.session_state.p_idx = 0
            
            start = st.session_state.p_idx * items
            curr_slice = dff.iloc[start : start + items]

            if not curr_slice.empty:
                for i in range(0, len(curr_slice), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i+j < len(curr_slice):
                            row = curr_slice.iloc[i+j]
                            with cols[j]:
                                st.markdown(f"""
                                    <div class="pro-card">
                                        <div class="card-main-title">{row.get(name_col, 'غير مسمى')}</div>
                                        <div style="color:#888; margin-bottom:10px;">{row.get('Developer', 'مطور غير محدد')}</div>
                                        <div class="stat-row"><span>📍 المنطقة</span><span class="stat-val">{row.get('Area', '-')}</span></div>
                                        <div class="stat-row"><span>💰 المقدم</span><span class="stat-val">{row.get('Down_Payment', '-')}</span></div>
                                    </div>
                                """, unsafe_allow_html=True)
                                with st.expander("🔍 تفاصيل إضافية"):
                                    st.write(row.to_dict())
            else:
                st.info("لا توجد مشاريع مطابقة للبحث.")

            # أزرار التنقل السفلية
            st.write("---")
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            with nav3:
                if (st.session_state.p_idx + 1) < total_p:
                    if st.button("التالي ⬅️", key="btn_p_next"):
                        st.session_state.p_idx += 1; st.rerun()
            with nav2:
                st.markdown(f"<p style='text-align:center; padding-top:10px;'>صفحة {st.session_state.p_idx + 1} من {total_p}</p>", unsafe_allow_html=True)
            with nav1:
                if st.session_state.p_idx > 0:
                    if st.button("➡️ السابق", key="btn_p_prev"):
                        st.session_state.p_idx -= 1; st.rerun()
        with c_side:
            st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)

# --- 🏢 باقي الشاشات (المطورين والأدوات) تظل كما هي لضمان عمل التطبيق ---
elif selected == "🏢 المطورين":
    if not df.empty:
        dev_col = 'Developer' if 'Developer' in df.columns else df.columns[0]
        devs = df[[dev_col, 'Owner', 'Detailed_Info']].drop_duplicates(subset=[dev_col]).reset_index(drop=True)
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            st.markdown("<h2 style='color:#f59e0b;'>🏢 المطورين</h2>", unsafe_allow_html=True)
            s_d = st.text_input("🔍 ابحث عن مطور...")
            if s_d: devs = devs[devs[dev_col].str.contains(s_d, case=False)]
            total_d = max(1, math.ceil(len(devs) / 9))
            curr_devs = devs.iloc[st.session_state.d_idx * 9 : (st.session_state.d_idx + 1) * 9]
            for i in range(0, len(curr_devs), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i+j < len(curr_devs):
                        row = curr_devs.iloc[i+j]
                        with cols[j]:
                            st.markdown(f'<div class="pro-card"><div class="card-main-title">{row[dev_col]}</div><div style="color:#888;">👤 {row["Owner"]}</div></div>', unsafe_allow_html=True)
                            with st.expander("📄 سابقة الأعمال"): st.write(row['Detailed_Info'])
        with c_side: st.write("")

elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ الأدوات</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='pro-card'><h3>💰 حاسبة القسط</h3>", unsafe_allow_html=True)
        p = st.number_input("السعر", value=1000000)
        y = st.number_input("السنين", value=7, min_value=1)
        st.subheader(f"{p/(y*12):,.0f} ج/شهري")
        st.markdown("</div>", unsafe_allow_html=True)
