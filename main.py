import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة - وضع الـ Wide لضمان ظهور 3 كروت جنب بعض
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS احترافي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f4f7f6; 
    }
    /* تنسيق كارت المشروع ليكون 3 في الصف */
    .project-card {
        background: white; border-radius: 12px; padding: 15px;
        border-top: 5px solid #003366; margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.06);
        height: 280px; display: flex; flex-direction: column; justify-content: space-between;
    }
    /* تنسيق قائمة أفضل المطورين في الجانب */
    .rank-item {
        background: #003366; color: white; padding: 12px;
        border-radius: 10px; margin-bottom: 10px; text-align: center;
        font-weight: bold; border-right: 6px solid #fbbf24;
    }
    .price-tag { color: #16a34a; font-weight: 900; font-size: 1.1rem; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات من رابط CSV الخاص بك
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

    # --- الجانب الأيسر (Sidebar): قائمة أفضل المطورين ---
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;'>🏆 أفضل المطورين</h2>", unsafe_allow_html=True)
        top_devs = ["Mountain View", "Palm Hills", "SODIC", "Emaar Misr", "Hassan Allam", "Ora Dev", "TMG", "Nile Dev", "La Vista", "LMD"]
        for i, name in enumerate(top_devs, 1):
            st.markdown(f'<div class="rank-item">{i}# {name}</div>', unsafe_allow_html=True)

    # --- الصفحة الرئيسية ---
    if st.session_state.page == 'main':
        st.markdown("<h1 style='text-align:center; color:#003366;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        
        # قسم البحث والفلاتر في الأعلى
        col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
        with col_s1:
            search_query = st.text_input("🔍 ابحث باسم المشروع أو المطور", placeholder="اكتب هنا...")
        with col_s2:
            s_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df.iloc[:, 3].unique().tolist()))
        with col_s3:
            s_type = st.selectbox("🏠 النوع", ["الكل"] + sorted(df.iloc[:, 7].unique().tolist()))

        # تطبيق الفلترة
        f_df = df.copy()
        if s_area != "الكل": f_df = f_df[f_df.iloc[:, 3] == s_area]
        if s_type != "الكل": f_df = f_df[f_df.iloc[:, 7] == s_type]
        if search_query:
            f_df = f_df[f_df.iloc[:, 0].str.contains(search_query, na=False, case=False) | 
                        f_df.iloc[:, 2].str.contains(search_query, na=False, case=False)]

        st.divider()

        # --- عرض 3 مشاريع في الصف الواحدة ---
        for i in range(0, len(f_df), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(f_df):
                    row = f_df.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="project-card">
                                <div>
                                    <div style="display:flex; justify-content:space-between;">
                                        <b style="color:#003366; font-size:1.1rem;">{row[2]}</b>
                                        <span class="price-tag">{row[4]}</span>
                                    </div>
                                    <p style="font-size:0.9rem; color:#64748b;">{row[0]}</p>
                                    <div style="font-size:0.8rem;">📍 {row[3]} | 🔑 {row[8]}</div>
                                </div>
                                <div style="background:#f1f5f9; padding:8px; border-radius:5px; font-size:0.8rem;">
                                    💰 مقدم {row[10]} | ⏳ {row[9]} سنوات
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"تفاصيل {row[2]}", key=f"btn_{i+j}", use_container_width=True):
                            st.session_state.selected_item = row.to_list()
                            st.session_state.page = 'details'
                            st.rerun()

    # --- صفحة التفاصيل ---
    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        if st.button("🔙 العودة للرئيسية"):
            st.session_state.page = 'main'
            st.rerun()

        st.markdown(f"""
            <div style="background:white; padding:25px; border-radius:15px; border-right:12px solid #003366; margin-top:10px;">
                <h1 style="color:#003366;">{item[2]}</h1>
                <p>بواسطة: <b>{item[0]}</b> | المالك: <b>{item[1]}</b></p>
            </div>
        """, unsafe_allow_html=True)

        t1, t2 = st.tabs(["📝 الزتونة والمعلومات", "🏗️ مشاريع المطور"])
        with t1:
            c1, c2 = st.columns(2)
            with c1:
                st.info(f"**الزتونة الفنية:**\n\n {item[11]}")
                st.write(f"**الوصف:** {item[6]}")
            with c2:
                st.success(f"**السعر:** {item[4]}\n\n**المقدم:** {item[10]}\n\n**السنوات:** {item[9]}")
                st.warning(f"**الاستلام:** {item[8]}")
        with t2:
            others = df[df.iloc[:, 0] == item[0]]
            for _, p in others.iterrows():
                st.markdown(f"- **{p[2]}** ({p[3]})")
