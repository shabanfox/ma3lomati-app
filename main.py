import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - كروت صغيرة مجمعة لليمين مع مساحة لليسار
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f4f7f9; 
    }

    /* كروت اليمين الصغيرة */
    .small-grid-card {
        background: white; border-radius: 10px; padding: 12px;
        height: 100px; display: flex; flex-direction: column;
        justify-content: center; border: 1px solid #e2e8f0;
        border-right: 4px solid #003366; margin-bottom: 5px;
    }

    /* ستايل العداد والقائمة في اليسار */
    .stat-card {
        background: white; padding: 20px; border-radius: 15px;
        border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center; margin-bottom: 20px;
    }
    
    .bio-section {
        background: white; padding: 25px; border-radius: 15px;
        border-right: 8px solid #D4AF37; margin-bottom: 20px;
    }

    div.stButton > button {
        border-radius: 6px !important; font-family: 'Cairo', sans-serif !important;
        height: 32px; font-size: 0.85rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [str(c).strip() for c in df.columns]
        if 'Developer' in df.columns:
            df = df.sort_values(by='Developer', ascending=True)
        return df
    except: return None

df = load_data()

# إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'current_page_num' not in st.session_state: st.session_state.current_page_num = 1
if 'search_query' not in st.session_state: st.session_state.search_query = ""

top_10_list = ["Mountain View", "SODIC", "Emaar", "TMG", "Ora Developers", "Palm Hills", "Tatweer Misr", "Misr Italia", "Orascom", "Hassan Allam"]

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    st.markdown('<h2 style="color:#003366; font-weight:900;">منصة معلوماتى العقارية</h2>', unsafe_allow_html=True)

    if df is not None:
        col_right, col_left = st.columns([1.8, 1])

        with col_right:
            # مربع البحث
            st.markdown('<div style="background:white; padding:15px; border-radius:12px; border:1px solid #e2e8f0; margin-bottom:15px;">', unsafe_allow_html=True)
            f_c1, f_c2 = st.columns([2, 1])
            with f_c1:
                search_input = st.text_input("🔍 ابحث عن مطور...", value=st.session_state.search_query)
                if search_input != st.session_state.search_query:
                    st.session_state.search_query = search_input
                    st.session_state.current_page_num = 1 # تصغير الصفحة عند البحث
            with f_c2:
                areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
                s_area = st.selectbox("المنطقة", areas)
            st.markdown('</div>', unsafe_allow_html=True)

            # فلترة البيانات
            f_df = df.copy()
            if s_area != "الكل": f_df = f_df[f_df['Area'] == s_area]
            if st.session_state.search_query:
                f_df = f_df[f_df['Developer'].astype(str).str.contains(st.session_state.search_query, case=False, na=False)]

            # --- منطق الـ 3 صفوف (Pagination) ---
            # بما إن الشاشة مقسومة واليمين فيه عمودين، 3 صفوف يعني 6 كروت
            items_per_page = 6 
            total_items = len(f_df)
            total_pages = math.ceil(total_items / items_per_page)
            
            start_idx = (st.session_state.current_page_num - 1) * items_per_page
            page_items = f_df.iloc[start_idx : start_idx + items_per_page]

            # عرض الكروت 2*3 (كارتين في 3 صفوف)
            grid_cols = st.columns(2)
            for idx, (i, row) in enumerate(page_items.reset_index().iterrows()):
                with grid_cols[idx % 2]:
                    st.markdown(f"""
                        <div class="small-grid-card">
                            <div style="color:#003366; font-weight:900; font-size:0.9rem;">{row.get('Developer')}</div>
                            <div style="color:#64748b; font-size:0.75rem;">📍 {row.get('Area')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("عرض البروفايل", key=f"btn_{i}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'; st.rerun()

            # أزرار التنقل بين الصفحات
            if total_pages > 1:
                st.write("---")
                p_c1, p_c2, p_c3 = st.columns([1,1,1])
                with p_c2:
                    st.write(f"صفحة {st.session_state.current_page_num} من {total_pages}")
                    b_prev, b_next = st.columns(2)
                    if b_prev.button("السابق") and st.session_state.current_page_num > 1:
                        st.session_state.current_page_num -= 1; st.rerun()
                    if b_next.button("التالي") and st.session_state.current_page_num < total_pages:
                        st.session_state.current_page_num += 1; st.rerun()

        with col_left:
            # عداد الشركات
            st.markdown(f"""
                <div class="stat-card">
                    <h5 style="margin:0; color:#64748b;">شركات مطابقة للبحث</h5>
                    <h1 style="margin:0; color:#003366;">{len(f_df)}</h1>
                </div>
            """, unsafe_allow_html=True)

            # فلتر أقوى 10 شركات
            st.markdown('<div class="stat-card" style="text-align:right;">', unsafe_allow_html=True)
            st.markdown('<h4 style="color:#003366; border-bottom:2px solid #D4AF37; padding-bottom:10px;">🏆 أقوى 10 مطورين</h4>', unsafe_allow_html=True)
            for company in top_10_list:
                if st.button(f"🏢 {company}", key=f"top_{company}", use_container_width=True):
                    st.session_state.search_query = company
                    st.session_state.current_page_num = 1
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التفاصيل ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 عودة"): st.session_state.page = 'main'; st.rerun()
    st.markdown(f"""
        <div style="background:#003366; padding:30px; border-radius:12px; color:white; text-align:center; margin-bottom:20px;">
            <h2>{item.get('Developer')}</h2>
        </div>
        <div class="bio-section">
            <h3>📖 نبذة عن الشركة</h3>
            <p>{item.get('Company_Bio', 'سيتم إضافة النبذة قريباً.')}</p>
        </div>
    """, unsafe_allow_html=True)
