import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS متطور
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f0f2f6; 
    }
    .stSearchInput { border-radius: 20px; }
    .top-dev-box {
        background: white; padding: 15px; border-radius: 12px;
        border-bottom: 4px solid #003366; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .project-card {
        background: white; border-radius: 15px; padding: 20px;
        border-right: 10px solid #003366; margin-bottom: 20px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
    }
    .price-tag { color: #16a34a; font-weight: 900; font-size: 1.3rem; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [c.strip() for c in df.columns]
        return df
    except: return None

df = load_data()

if df is not None:
    if 'page' not in st.session_state: st.session_state.page = 'main'

    # --- القائمة الجانبية (الفلاتر) ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/609/609803.png", width=100)
        st.title("تصفية البحث")
        f_area = st.multiselect("📍 المناطق", options=df.iloc[:, 3].unique().tolist(), default=[])
        f_type = st.multiselect("🏠 نوع الوحدة", options=df.iloc[:, 7].unique().tolist(), default=[])
        st.divider()
        st.info("استخدم الفلاتر أعلاه لتحديد بحثك بدقة")

    # --- الصفحة الرئيسية ---
    if st.session_state.page == 'main':
        st.markdown("<h1 style='text-align:center; color:#003366;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        
        # 1. شريط البحث العلوي
        search_query = st.text_input("🔍 ابحث عن مطور أو مشروع محدد...", placeholder="اكتب اسم الشركة أو الكمبوند هنا")

        # 2. قائمة أفضل المطورين (سلايدر أفقي بسيط)
        st.subheader("🏆 أفضل المطورين")
        top_devs = ["Mountain View", "Palm Hills", "SODIC", "Emaar Misr", "Ora Dev", "Nile Dev"]
        cols_devs = st.columns(len(top_devs))
        for i, dev in enumerate(top_devs):
            with cols_devs[i]:
                st.markdown(f'<div class="top-dev-box"><b>{dev}</b></div>', unsafe_allow_html=True)

        st.divider()

        # تطبيق الفلاتر والبحث
        f_df = df.copy()
        if f_area: f_df = f_df[f_df.iloc[:, 3].isin(f_area)]
        if f_type: f_df = f_df[f_df.iloc[:, 7].isin(f_type)]
        if search_query:
            f_df = f_df[f_df.iloc[:, 0].str.contains(search_query, na=False, case=False) | 
                        f_df.iloc[:, 2].str.contains(search_query, na=False, case=False)]

        # 3. عرض النتائج
        st.subheader(f"📂 المشاريع المتاحة ({len(f_df)})")
        grid = st.columns(2)
        for idx, (i, row) in enumerate(f_df.iterrows()):
            with grid[idx % 2]:
                st.markdown(f"""
                    <div class="project-card">
                        <div style="display:flex; justify-content:space-between; align-items:start;">
                            <h2 style="margin:0; color:#003366;">{row[2]}</h2>
                            <span class="price-tag">{row[4]}</span>
                        </div>
                        <p style="color:#64748b; font-size:1.1rem; margin:5px 0;">🏢 <b>المطور:</b> {row[0]}</p>
                        <p>📍 {row[3]} | 🔑 استلام {row[8]}</p>
                        <div style="background:#f8fafc; padding:10px; border-radius:8px; font-size:0.9rem;">
                            💰 مقدم {row[10]} | ⏳ تقسيط {row[9]} سنوات
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"التفاصيل والزتونة لـ {row[2]}", key=f"btn_{i}", use_container_width=True):
                    st.session_state.selected_item = row.to_list()
                    st.session_state.page = 'details'
                    st.rerun()

    # --- صفحة التفاصيل ---
    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        if st.button("🔙 العودة لنتائج البحث"):
            st.session_state.page = 'main'
            st.rerun()

        st.markdown(f"""
            <div style="background:white; padding:30px; border-radius:15px; border-right:12px solid #003366; margin-top:20px;">
                <h1 style="color:#003366; margin:0;">{item[2]}</h1>
                <p style="font-size:1.4rem;">المطور: <b>{item[0]}</b> | المالك: <b>{item[1]}</b></p>
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["📝 الزتونة الفنية والمعلومات", "🏗️ كل مشاريع المطور"])
        
        with tab1:
            c1, c2 = st.columns(2)
            with c1:
                st.info(f"**الزتونة الفنية:**\n\n {item[11]}")
                st.warning(f"**وصف المشروع:**\n\n {item[6]}")
            with c2:
                st.success(f"### نظام السداد\n- **السعر:** {item[4]}\n- **أقل استثمار:** {item[5]}\n- **المقدم:** {item[10]}\n- **السنوات:** {item[9]}")
                st.write(f"**الاستلام:** {item[8]}")

        with tab2:
            st.subheader(f"مشاريع أخرى تابعة لـ {item[0]}")
            others = df[df.iloc[:, 0] == item[0]]
            for _, p in others.iterrows():
                st.markdown(f"- **{p[2]}** في منطقة {p[3]} (السعر: {p[4]})")
