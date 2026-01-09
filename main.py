import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS متقدم للكروت الجانبية والرئيسية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }
    /* كروت المشاريع الرئيسية (اليمين) */
    .mini-card {
        background: white; border-radius: 8px; padding: 10px;
        border-right: 4px solid #003366; margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        height: 140px; display: flex; flex-direction: column; justify-content: space-between;
    }
    /* كروت "أقوى 10 مشاريع" (اليسار) */
    .top-project-card {
        background: linear-gradient(90deg, #ffffff 0%, #f0f7ff 100%);
        border-radius: 6px; padding: 6px 10px;
        border-right: 3px solid #fbbf24; margin-bottom: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        font-size: 0.75rem;
    }
    .rank-num { color: #fbbf24; font-weight: 900; margin-left: 5px; }
    .title-text { color: #003366; font-size: 0.8rem; font-weight: 700; margin: 0; }
    .price-text { color: #16a34a; font-weight: 700; font-size: 0.75rem; }
    
    /* القائمة الجانبية (Sidebar) */
    .rank-box {
        background: #003366; color: white; padding: 4px;
        border-radius: 4px; margin-bottom: 4px; text-align: center;
        font-size: 0.7rem;
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

    # --- القائمة الجانبية (أفضل المطورين) ---
    with st.sidebar:
        st.markdown("<h4 style='text-align:center;'>🏆 أفضل المطورين</h4>", unsafe_allow_html=True)
        top_list = ["Mountain View", "Palm Hills", "SODIC", "Emaar Misr", "Ora Dev", "Nile Dev", "Hassan Allam", "LMD"]
        for i, name in enumerate(top_list, 1):
            st.markdown(f'<div class="rank-box">{i}# {name}</div>', unsafe_allow_html=True)

    # --- الصفحة الرئيسية ---
    if st.session_state.page == 'main':
        st.markdown("<h2 style='color:#003366; margin-bottom:0;'>🏠 منصة معلوماتى العقارية</h2>", unsafe_allow_html=True)
        
        # البحث والفلاتر
        f1, f2, f3 = st.columns([2, 1, 1])
        with f1: search_q = st.text_input("🔍 بحث سريح", placeholder="المشروع...")
        with f2: s_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df.iloc[:, 3].unique().tolist()))
        with f3: s_type = st.selectbox("🏠 النوع", ["الكل"] + sorted(df.iloc[:, 7].unique().tolist()))

        # تقسيم المحتوى: يمين (كروت رئيسية) | يسار (أقوى 10 مشاريع)
        main_col, left_panel = st.columns([3, 1])

        with main_col:
            f_df = df.copy()
            if s_area != "الكل": f_df = f_df[f_df.iloc[:, 3] == s_area]
            if s_type != "الكل": f_df = f_df[f_df.iloc[:, 7] == s_type]
            if search_q: f_df = f_df[f_df.iloc[:, 0].str.contains(search_q, na=False, case=False) | f_df.iloc[:, 2].str.contains(search_q, na=False, case=False)]

            items_per_page = 9
            total_pages = math.ceil(len(f_df) / items_per_page)
            start_idx = st.session_state.current_page * items_per_page
            current_items = f_df.iloc[start_idx : start_idx + items_per_page]

            for i in range(0, len(current_items), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_items):
                        row = current_items.iloc[i + j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="mini-card">
                                    <p class="title-text">{row[2]}</p>
                                    <p style="font-size:0.65rem; color:#64748b; margin:0;">{row[0]}</p>
                                    <p class="price-text">{row[4]}</p>
                                    <div style="font-size:0.65rem; background:#f1f5f9; padding:2px; border-radius:3px; text-align:center;">
                                        مقدم {row[10]} | {row[9]}س
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"تفاصيل {row[2][:8]}", key=f"btn_{start_idx+i+j}", use_container_width=True):
                                st.session_state.selected_item = row.to_list()
                                st.session_state.page = 'details'
                                st.rerun()
            
            # أزرار التنقل
            st.write(f"<p style='text-align:center; font-size:0.7rem;'>صفحة {st.session_state.current_page+1} من {total_pages}</p>", unsafe_allow_html=True)
            col_b1, col_b2 = st.columns(2)
            with col_b1: 
                if st.session_state.current_page > 0 and st.button("السابق"): st.session_state.current_page -= 1; st.rerun()
            with col_b2: 
                if st.session_state.current_page < total_pages - 1 and st.button("التالي"): st.session_state.current_page += 1; st.rerun()

        with left_panel:
            st.markdown("<h5 style='text-align:center; color:#003366;'>🔥 أقوى 10 مشاريع</h5>", unsafe_allow_html=True)
            # نأخذ أول 10 مشاريع من الشيت كأقوى مشاريع (أو يمكنك تمييزهم في الشيت)
            top_10 = df.head(10)
            for idx, row in top_10.iterrows():
                st.markdown(f"""
                    <div class="top-project-card">
                        <span class="rank-num">#{idx+1}</span>
                        <b>{row[2]}</b> <br>
                        <span style="font-size:0.65rem; color:#64748b;">{row[3]} | 💰 {row[4]}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.write("---")
            st.markdown("<div style='height:100px; border:1px dashed #ccc; border-radius:10px; text-align:center; font-size:0.7rem; color:#ccc; padding-top:20px;'>مساحة إضافية</div>", unsafe_allow_html=True)

    # --- صفحة التفاصيل (نفس الكود السابق) ---
    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        if st.button("🔙 عودة"): st.session_state.page = 'main'; st.rerun()
        st.markdown(f"### {item[2]}")
        st.info(f"**الزتونة:** {item[11]}")
