import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS مرن (Responsive)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f1f5f9; 
    }

    /* تحسين عرض الحاويات على الموبايل */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 calc(100% - 1rem) !important;
    }

    /* الكارت الرئيسي */
    .mini-card {
        background: white; border-radius: 12px; padding: 15px;
        border-right: 6px solid #003366; margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        min-height: 160px; display: flex; flex-direction: column; justify-content: space-between;
    }
    
    .title-text { color: #003366; font-size: 1.1rem; font-weight: 900; margin: 0; }
    .price-text { color: #15803d; font-weight: 900; font-size: 1.1rem; margin: 5px 0; }
    
    /* قائمة أقوى 10 مشاريع */
    .top-project-card {
        background: white; border-radius: 8px; padding: 10px;
        border-right: 4px solid #fbbf24; margin-bottom: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }

    /* إخفاء المساحات الزائدة في الموبايل */
    @media (max-width: 768px) {
        .mini-card { height: auto; }
        [data-testid="stHorizontalBlock"] { flex-direction: column !important; }
    }
    
    .stButton>button { 
        background-color: #003366 !important; color: white !important;
        width: 100%; font-family: 'Cairo'; font-weight: 700;
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

    # --- القائمة الجانبية (أفضل الشركات) ---
    with st.sidebar:
        st.markdown("<h3 style='text-align:center;'>🏆 أفضل المطورين</h3>", unsafe_allow_html=True)
        top_list = ["Mountain View", "Palm Hills", "SODIC", "Emaar Misr", "Ora Dev", "Nile Dev", "Hassan Allam", "TMG"]
        for i, name in enumerate(top_list, 1):
            st.markdown(f"""<div style='background:#003366; color:white; padding:8px; border-radius:8px; margin-bottom:5px; text-align:center; font-weight:700; font-size:0.9rem;'>{i}# {name}</div>""", unsafe_allow_html=True)

    # --- الصفحة الرئيسية ---
    if st.session_state.page == 'main':
        st.markdown("<h1 style='color:#003366; text-align:center; font-size:1.8rem;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        
        # البحث والفلاتر (ستترتب تحت بعضها في الموبايل تلقائياً)
        search_q = st.text_input("🔍 ابحث عن مشروع أو مطور")
        c_area, c_type = st.columns(2)
        with c_area: s_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df.iloc[:, 3].unique().tolist()))
        with c_type: s_type = st.selectbox("🏠 النوع", ["الكل"] + sorted(df.iloc[:, 7].unique().tolist()))

        # تقسيم الشاشة (في الموبايل سيظهر اليمين ثم يسار تحت بعض)
        main_col, left_panel = st.columns([2.5, 1])

        with main_col:
            f_df = df.copy()
            if s_area != "الكل": f_df = f_df[f_df.iloc[:, 3] == s_area]
            if s_type != "الكل": f_df = f_df[f_df.iloc[:, 7] == s_type]
            if search_q: f_df = f_df[f_df.iloc[:, 0].str.contains(search_q, na=False, case=False) | f_df.iloc[:, 2].str.contains(search_q, na=False, case=False)]

            items_per_page = 9
            total_pages = math.ceil(len(f_df) / items_per_page)
            start_idx = st.session_state.current_page * items_per_page
            current_items = f_df.iloc[start_idx : start_idx + items_per_page]

            # عرض الكروت: في الكمبيوتر 3 أعمدة، وفي الموبايل ستتحول تلقائياً لعمود واحد
            for i in range(0, len(current_items), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_items):
                        row = current_items.iloc[i + j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="mini-card">
                                    <div>
                                        <p class="title-text">{row[2]}</p>
                                        <p style="color:#64748b; font-size:0.9rem; font-weight:700;">{row[0]}</p>
                                        <p style="font-size:0.85rem;">📍 {row[3]}</p>
                                    </div>
                                    <div>
                                        <p class="price-text">{row[4]}</p>
                                        <div style="font-size:0.85rem; color:#1e293b; background:#e2e8f0; padding:5px; border-radius:5px; text-align:center; font-weight:700;">
                                            مقدم {row[10]} | {row[9]}س
                                        </div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"تفاصيل {row[2][:12]}", key=f"btn_{start_idx+i+j}"):
                                st.session_state.selected_item = row.to_list()
                                st.session_state.page = 'details'
                                st.rerun()
            
            # أزرار الصفحات
            st.divider()
            b1, b2, b3 = st.columns([1,1,1])
            with b1: 
                if st.session_state.current_page > 0 and st.button("⬅️"): st.session_state.current_page -= 1; st.rerun()
            with b2: st.write(f"<p style='text-align:center;'>{st.session_state.current_page+1}/{total_pages}</p>", unsafe_allow_html=True)
            with b3: 
                if st.session_state.current_page < total_pages - 1 and st.button("➡️"): st.session_state.current_page += 1; st.rerun()

        with left_panel:
            st.markdown("<h4 style='text-align:center; color:#003366; background:#fbbf24; padding:8px; border-radius:8px;'>🔥 أقوى 10 مشاريع</h4>", unsafe_allow_html=True)
            top_10 = df.head(10)
            for idx, row in top_10.iterrows():
                st.markdown(f"""
                    <div class="top-project-card">
                        <b><span style="color:#fbbf24;">#{idx+1}</span> {row[2]}</b><br>
                        <small>{row[3]} | {row[4]}</small>
                    </div>
                """, unsafe_allow_html=True)

    # --- صفحة التفاصيل ---
    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        if st.button("🔙 عودة"): st.session_state.page = 'main'; st.rerun()
        st.markdown(f"<h2 style='color:#003366;'>{item[2]}</h2>", unsafe_allow_html=True)
        st.info(f"**الزتونة الفنية:**\n\n{item[11]}")
        st.success(f"المطور: {item[0]} | السعر: {item[4]} | المقدم: {item[10]} | التقسيط: {item[9]} سنوات")
