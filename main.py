import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة (واسعة لـ 3 كروت)
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS مخصص (3 كروت في الصف + قائمة جانبية)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f4f7f6; 
    }
    /* تصميم الكارت ليكون مناسب لـ 3 في الصف */
    .project-card {
        background: white; border-radius: 12px; padding: 15px;
        border-top: 5px solid #003366; margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.06);
        height: 280px; display: flex; flex-direction: column; justify-content: space-between;
    }
    .top-rank-card {
        background: #003366; color: white; padding: 10px;
        border-radius: 8px; margin-bottom: 8px; text-align: center;
        font-size: 0.9rem; border-right: 5px solid #fbbf24;
    }
    .price-tag { color: #16a34a; font-weight: 900; font-size: 1.1rem; }
    .stButton>button { border-radius: 8px; font-family: 'Cairo'; }
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

    # --- القائمة الجانبية اليسرى (أفضل المطورين/المشاريع) ---
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;'>🏆 أفضل المطورين</h2>", unsafe_allow_html=True)
        # قائمة مرتبة لأفضل الشركات
        top_list = ["Mountain View", "Palm Hills", "SODIC", "Emaar Misr", "Hassan Allam", "Ora Dev", "TMG", "Nile Dev"]
        for rank, name in enumerate(top_list, 1):
            st.markdown(f'<div class="top-rank-card">{rank}# {name}</div>', unsafe_allow_html=True)
        
        st.divider()
        st.markdown("### 📍 فلاتر سريعة")
        f_area = st.selectbox("اختار المنطقة", ["الكل"] + sorted(df.iloc[:, 3].unique().tolist()))
        f_type = st.selectbox("نوع الوحدة", ["الكل"] + sorted(df.iloc[:, 7].unique().tolist()))

    # --- الصفحة الرئيسية ---
    if st.session_state.page == 'main':
        st.markdown("<h1 style='text-align:center; color:#003366;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        
        # البحث العلوي
        search_query = st.text_input("🔍 ابحث عن مشروع أو مطور...", placeholder="اكتب هنا للبحث السريع...")

        # تطبيق الفلترة
        f_df = df.copy()
        if f_area != "الكل": f_df = f_df[f_df.iloc[:, 3] == f_area]
        if f_type != "الكل": f_df = f_df[f_df.iloc[:, 7] == f_type]
        if search_query:
            f_df = f_df[f_df.iloc[:, 0].str.contains(search_query, na=False, case=False) | 
                        f_df.iloc[:, 2].str.contains(search_query, na=False, case=False)]

        # --- عرض النتائج (3 كروت في الصف) ---
        st.write(f"عرض **{len(f_df)}** مشروع")
        
        # إنشاء الصفوف بـ 3 أعمدة
        for start_idx in range(0, len(f_df), 3):
            cols = st.columns(3)
            for i in range(3):
                idx = start_idx + i
                if idx < len(f_df):
                    row = f_df.iloc[idx]
                    with cols[i]:
                        st.markdown(f"""
                            <div class="project-card">
                                <div>
                                    <div style="display:flex; justify-content:space-between;">
                                        <b style="color:#003366; font-size:1.1rem;">{row[2]}</b>
                                        <span class="price-tag">{row[4]}</span>
                                    </div>
                                    <p style="font-size:0.9rem; color:#64748b; margin:5px 0;">{row[0]}</p>
                                    <div style="font-size:0.8rem;">📍 {row[3]}</div>
                                </div>
                                <div>
                                    <div style="background:#f1f5f9; padding:8px; border-radius:5px; font-size:0.8rem; margin-bottom:10px;">
                                        💰 مقدم {row[10]} | ⏳ {row[9]} سنين
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"تفاصيل {row[2]}", key=f"btn_{idx}", use_container_width=True):
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
            <div style="background:white; padding:30px; border-radius:15px; border-right:12px solid #003366; margin-top:20px;">
                <h1 style="color:#003366; margin:0;">{item[2]}</h1>
                <p style="font-size:1.4rem;">المطور: <b>{item[0]}</b> | المالك: <b>{item[1]}</b></p>
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["📝 الزتونة الفنية", "🏗️ مشاريع المطور"])
        with tab1:
            c1, c2 = st.columns(2)
            with c1:
                st.info(f"**الزتونة:** {item[11]}")
                st.write(f"**الوصف:** {item[6]}")
            with c2:
                st.success(f"**السعر:** {item[4]}\n\n**المقدم:** {item[10]}\n\n**التقسيط:** {item[9]} سنوات")
                st.warning(f"**الاستلام:** {item[8]}")
