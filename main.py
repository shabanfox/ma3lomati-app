import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS للكروت الصغيرة والمساحات
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f4f6f9; 
    }

    /* الكروت الميني */
    .mini-card {
        background: white; border-radius: 8px; padding: 10px;
        border-right: 4px solid #003366; margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        height: 150px; display: flex; flex-direction: column; justify-content: space-between;
    }

    .title-text { color: #003366; font-size: 0.85rem; font-weight: 700; margin: 0; }
    .dev-text { color: #64748b; font-size: 0.7rem; }
    .price-text { color: #16a34a; font-weight: 700; font-size: 0.85rem; }
    
    /* القائمة الجانبية */
    .rank-box {
        background: #003366; color: white; padding: 5px 10px;
        border-radius: 5px; margin-bottom: 5px; text-align: center;
        font-size: 0.75rem; border-left: 3px solid #fbbf24;
    }

    .stButton>button { 
        font-family: 'Cairo'; padding: 0px; font-size: 0.7rem; height: 25px; border-radius: 4px;
    }
    
    /* إلغاء الفراغات الزائدة */
    .block-container { padding-top: 2rem; }
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
        st.markdown("<h4 style='text-align:center;'>🏆 أفضل المطورين</h4>", unsafe_allow_html=True)
        top_list = ["Mountain View", "Palm Hills", "SODIC", "Emaar Misr", "Ora Dev", "Nile Dev", "Hassan Allam", "TMG"]
        for i, name in enumerate(top_list, 1):
            st.markdown(f'<div class="rank-box">{i}# {name}</div>', unsafe_allow_html=True)

    # --- الصفحة الرئيسية ---
    if st.session_state.page == 'main':
        st.markdown("<h2 style='color:#003366;'>🏠 منصة معلوماتى العقارية</h2>", unsafe_allow_html=True)
        
        # البحث والفلاتر
        f1, f2, f3 = st.columns([2, 1, 1])
        with f1: search_q = st.text_input("🔍 بحث", placeholder="المشروع أو المطور...")
        with f2: s_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df.iloc[:, 3].unique().tolist()))
        with f3: s_type = st.selectbox("🏠 النوع", ["الكل"] + sorted(df.iloc[:, 7].unique().tolist()))

        # تقسيم الصفحة لعمودين: يمين للكروت، يسار للفراغ (الإضافة المستقبلية)
        main_col, empty_col = st.columns([3, 1])

        with main_col:
            # فلترة البيانات
            f_df = df.copy()
            if s_area != "الكل": f_df = f_df[f_df.iloc[:, 3] == s_area]
            if s_type != "الكل": f_df = f_df[f_df.iloc[:, 7] == s_type]
            if search_q:
                f_df = f_df[f_df.iloc[:, 0].str.contains(search_q, na=False, case=False) | 
                            f_df.iloc[:, 2].str.contains(search_q, na=False, case=False)]

            # نظام الصفحات (9 كروت)
            items_per_page = 9
            total_pages = math.ceil(len(f_df) / items_per_page)
            start_idx = st.session_state.current_page * items_per_page
            current_items = f_df.iloc[start_idx : start_idx + items_per_page]

            # عرض الكروت في اليمين (3 في الصف)
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
                                        <p class="dev-text">{row[0]}</p>
                                        <p style="font-size:0.65rem; margin:0;">📍 {row[3]}</p>
                                    </div>
                                    <div>
                                        <p class="price-text">{row[4]}</p>
                                        <div style="font-size:0.65rem; color:#475569; background:#f1f5f9; padding:2px 5px; border-radius:3px;">
                                            مقدم: {row[10]} | {row[9]}س
                                        </div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"تفاصيل {row[2][:10]}..", key=f"btn_{start_idx+i+j}", use_container_width=True):
                                st.session_state.selected_item = row.to_list()
                                st.session_state.page = 'details'
                                st.rerun()

            # أزرار التنقل
            st.write("")
            n1, n2, n3 = st.columns([1,1,1])
            with n1: 
                if st.session_state.current_page > 0 and st.button("⬅️"): 
                    st.session_state.current_page -= 1
                    st.rerun()
            with n2: st.write(f"<p style='text-align:center; font-size:0.7rem;'>{st.session_state.current_page+1}/{total_pages}</p>", unsafe_allow_html=True)
            with n3: 
                if st.session_state.current_page < total_pages - 1 and st.button("➡️"):
                    st.session_state.current_page += 1
                    st.rerun()

        with empty_col:
            # هذا هو المكان الفارغ في جهة اليسار
            st.markdown("<div style='height:500px; border:2px dashed #ccc; border-radius:10px; display:flex; align-items:center; justify-content:center; color:#ccc;'>مساحة للإضافة هنا</div>", unsafe_allow_html=True)

    # --- صفحة التفاصيل ---
    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        if st.button("🔙 عودة"):
            st.session_state.page = 'main'
            st.rerun()
        st.markdown(f"### {item[2]}")
        st.info(f"**الزتونة:** {item[11]}")
        st.write(f"**المطور:** {item[0]} | **السعر:** {item[4]}")
