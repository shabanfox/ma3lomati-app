import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS للكروت الصغيرة جداً والمحاذاة لليمين
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; 
        text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f0f2f5; 
    }

    /* تنسيق الكروت لتكون صغيرة ومحاذية لليمين */
    .project-card {
        background: white; 
        border-radius: 8px; 
        padding: 10px;
        border-right: 5px solid #003366; 
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        height: 180px; /* حجم أصغر */
        display: flex; 
        flex-direction: column; 
        justify-content: space-between;
    }

    .project-title { color: #003366; font-size: 0.9rem; font-weight: 700; margin: 0; line-height: 1.2; }
    .dev-name { color: #64748b; font-size: 0.75rem; margin-bottom: 5px; }
    .price-val { color: #16a34a; font-weight: 700; font-size: 0.9rem; }
    
    /* تنسيق القائمة الجانبية */
    .rank-item {
        background: #003366; color: white; padding: 6px;
        border-radius: 6px; margin-bottom: 6px; text-align: center;
        font-size: 0.8rem; border-left: 4px solid #fbbf24;
    }

    /* تعديل المسافات بين الأعمدة */
    [data-testid="column"] { padding: 0 5px !important; }
    
    .stButton>button { 
        font-family: 'Cairo'; 
        padding: 0px 5px; 
        font-size: 0.75rem; 
        height: 30px; 
        border-radius: 5px;
    }
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
    if 'current_page' not in st.session_state: st.session_state.current_page = 0

    # --- القائمة الجانبية اليسرى (ترتيب أفضل الشركات) ---
    with st.sidebar:
        st.markdown("<h3 style='text-align:center;'>🏆 أفضل الشركات</h3>", unsafe_allow_html=True)
        top_list = ["Mountain View", "Palm Hills", "SODIC", "Emaar Misr", "Ora Dev", "Nile Dev", "LMD", "Hassan Allam", "Misr Italia", "Tatweer Misr"]
        for i, name in enumerate(top_list, 1):
            st.markdown(f'<div class="rank-item">{i}# {name}</div>', unsafe_allow_html=True)

    # --- الصفحة الرئيسية ---
    if st.session_state.page == 'main':
        st.markdown("<h2 style='text-align:right; color:#003366; margin-right:10px;'>🏠 منصة معلوماتى العقارية</h2>", unsafe_allow_html=True)
        
        # البحث والفلاتر في الأعلى
        search_col, area_col, type_col = st.columns([2, 1, 1])
        with search_col: search_q = st.text_input("🔍 بحث سريح", placeholder="اسم المشروع...")
        with area_col: s_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df.iloc[:, 3].unique().tolist()))
        with type_col: s_type = st.selectbox("🏠 النوع", ["الكل"] + sorted(df.iloc[:, 7].unique().tolist()))

        # تطبيق الفلاتر
        f_df = df.copy()
        if s_area != "الكل": f_df = f_df[f_df.iloc[:, 3] == s_area]
        if s_type != "الكل": f_df = f_df[f_df.iloc[:, 7] == s_type]
        if search_q:
            f_df = f_df[f_df.iloc[:, 0].str.contains(search_q, na=False, case=False) | 
                        f_df.iloc[:, 2].str.contains(search_q, na=False, case=False)]

        # --- الحسابات لـ 3 صفوف (9 كروت) ---
        items_per_page = 9
        total_pages = math.ceil(len(f_df) / items_per_page)
        start_idx = st.session_state.current_page * items_per_page
        current_items = f_df.iloc[start_idx : start_idx + items_per_page]

        # --- عرض الكروت في اليمين (3 في كل صف) ---
        for i in range(0, len(current_items), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(current_items):
                    row = current_items.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="project-card">
                                <div>
                                    <p class="project-title">{row[2]}</p>
                                    <p class="dev-name">{row[0]}</p>
                                    <p style="font-size:0.75rem; margin:0;">📍 {row[3]}</p>
                                </div>
                                <div>
                                    <p class="price-val">{row[4]}</p>
                                    <div style="font-size:0.7rem; color:#475569;">
                                        مقدم: {row[10]} | {row[9]}سنين
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"تفاصيل {row[2]}", key=f"btn_{start_idx+i+j}", use_container_width=True):
                            st.session_state.selected_item = row.to_list()
                            st.session_state.page = 'details'
                            st.rerun()

        # --- التنقل بين الصفحات ---
        st.write("")
        nav_prev, nav_info, nav_next = st.columns([1, 2, 1])
        with nav_prev:
            if st.session_state.current_page > 0:
                if st.button("⬅️ السابق"):
                    st.session_state.current_page -= 1
                    st.rerun()
        with nav_info:
            st.write(f"<p style='text-align:center; font-size:0.8rem;'>صفحة {st.session_state.current_page + 1} من {total_pages}</p>", unsafe_allow_html=True)
        with nav_next:
            if st.session_state.current_page < total_pages - 1:
                if st.button("التالي ➡️"):
                    st.session_state.current_page += 1
                    st.rerun()

    # --- صفحة التفاصيل ---
    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        if st.button("🔙 عودة"):
            st.session_state.page = 'main'
            st.rerun()
        st.markdown(f"<div style='background:white; padding:15px; border-radius:10px; border-right:6px solid #003366;'><h3>{item[2]}</h3><p>{item[0]}</p></div>", unsafe_allow_html=True)
        st.info(f"**الزتونة:** {item[11]}")
        st.write(f"**السعر:** {item[4]} | **المقدم:** {item[10]} | **التقسيط:** {item[9]} سنوات")
