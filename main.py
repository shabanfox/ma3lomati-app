import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS للكروت الصغيرة والقائمة الجانبية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8f9fa; 
    }
    .project-card {
        background: white; border-radius: 10px; padding: 12px;
        border-top: 4px solid #003366; margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        height: 220px; display: flex; flex-direction: column; justify-content: space-between;
    }
    .project-title { color: #003366; font-size: 1rem; font-weight: 700; margin: 0; }
    .dev-name { color: #64748b; font-size: 0.85rem; }
    .price-val { color: #16a34a; font-weight: 700; font-size: 0.95rem; }
    .rank-item {
        background: #003366; color: white; padding: 8px;
        border-radius: 8px; margin-bottom: 8px; text-align: center;
        font-size: 0.85rem; border-right: 4px solid #fbbf24;
    }
    .stButton>button { font-family: 'Cairo'; padding: 2px 10px; font-size: 0.85rem; }
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
    # تهيئة الحالة (Session State)
    if 'page' not in st.session_state: st.session_state.page = 'main'
    if 'current_page' not in st.session_state: st.session_state.current_page = 0

    # --- القائمة الجانبية اليسرى (أفضل الشركات) ---
    with st.sidebar:
        st.markdown("<h3 style='text-align:center;'>🏆 أفضل الشركات</h3>", unsafe_allow_html=True)
        top_list = ["Mountain View", "Palm Hills", "SODIC", "Emaar Misr", "Ora Dev", "Nile Dev", "LMD", "Hassan Allam"]
        for i, name in enumerate(top_list, 1):
            st.markdown(f'<div class="rank-item">{i}# {name}</div>', unsafe_allow_html=True)

    # --- الصفحة الرئيسية ---
    if st.session_state.page == 'main':
        st.markdown("<h2 style='text-align:center; color:#003366; margin-bottom:20px;'>🏠 منصة معلوماتى العقارية</h2>", unsafe_allow_html=True)
        
        # البحث والفلاتر (مدمجة)
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1: search_q = st.text_input("🔍 ابحث عن مشروع أو مطور")
        with c2: s_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df.iloc[:, 3].unique().tolist()))
        with c3: s_type = st.selectbox("🏠 النوع", ["الكل"] + sorted(df.iloc[:, 7].unique().tolist()))

        # الفلترة
        f_df = df.copy()
        if s_area != "الكل": f_df = f_df[f_df.iloc[:, 3] == s_area]
        if s_type != "الكل": f_df = f_df[f_df.iloc[:, 7] == s_type]
        if search_q:
            f_df = f_df[f_df.iloc[:, 0].str.contains(search_q, na=False, case=False) | 
                        f_df.iloc[:, 2].str.contains(search_q, na=False, case=False)]

        # --- حساب الصفحات (9 كروت لكل صفحة = 3 صفوف) ---
        items_per_page = 9
        total_pages = math.ceil(len(f_df) / items_per_page)
        start_idx = st.session_state.current_page * items_per_page
        end_idx = start_idx + items_per_page
        current_items = f_df.iloc[start_idx:end_idx]

        # عرض الكروت (3 في الصف)
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
                                    <p style="font-size:0.8rem; margin:0;">📍 {row[3]} | 🔑 {row[8]}</p>
                                </div>
                                <div>
                                    <p class="price-val">{row[4]}</p>
                                    <div style="font-size:0.75rem; background:#f1f5f9; padding:5px; border-radius:4px;">
                                        مقدم: {row[10]} | قسط: {row[9]}س
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"تفاصيل {row[2]}", key=f"btn_{start_idx+i+j}", use_container_width=True):
                            st.session_state.selected_item = row.to_list()
                            st.session_state.page = 'details'
                            st.rerun()

        # --- أزرار التنقل بين الصفحات ---
        st.write("---")
        p_col1, p_col2, p_col3 = st.columns([1, 2, 1])
        with p_col1:
            if st.session_state.current_page > 0:
                if st.button("⬅️ السابق"):
                    st.session_state.current_page -= 1
                    st.rerun()
        with p_col2:
            st.write(f"<p style='text-align:center;'>صفحة {st.session_state.current_page + 1} من {max(1, total_pages)}</p>", unsafe_allow_html=True)
        with p_col3:
            if st.session_state.current_page < total_pages - 1:
                if st.button("التالي ➡️"):
                    st.session_state.current_page += 1
                    st.rerun()

    # --- صفحة التفاصيل ---
    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        if st.button("🔙 عودة للرئيسية"):
            st.session_state.page = 'main'
            st.rerun()

        st.markdown(f"<div style='background:white; padding:20px; border-radius:15px; border-right:8px solid #003366;'><h2>{item[2]}</h2><p>المطور: {item[0]} | المالك: {item[1]}</p></div>", unsafe_allow_html=True)
        
        t1, t2 = st.tabs(["📝 الزتونة", "🏗️ مشاريع المطور"])
        with t1:
            st.info(f"**الزتونة الفنية:** {item[11]}")
            st.success(f"السعر: {item[4]} | المقدم: {item[10]} | التقسيط: {item[9]} سنوات")
            st.write(f"**الوصف:** {item[6]}")
        with t2:
            others = df[df.iloc[:, 0] == item[0]]
            for _, p in others.iterrows():
                st.write(f"- {p[2]} ({p[3]})")
