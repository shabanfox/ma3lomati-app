import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - ألوان واضحة جداً
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f4f7f9; 
    }

    /* نصوص واضحة جداً */
    .stMarkdown, p, span, label {
        color: #1e293b !important; /* لون رمادي غامق جداً قريب للأسود */
        font-weight: 500;
    }

    /* كروت اليمين */
    .small-grid-card {
        background: white; border-radius: 10px; padding: 12px;
        height: 100px; display: flex; flex-direction: column;
        justify-content: center; border: 1px solid #e2e8f0;
        border-right: 4px solid #003366; margin-bottom: 5px;
    }

    /* عداد الصفحات */
    .page-info {
        color: #003366 !important;
        font-weight: 900 !important;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 10px;
    }

    .stat-card {
        background: white; padding: 20px; border-radius: 15px;
        border: 1px solid #e2e8f0; text-align: center; margin-bottom: 20px;
    }

    /* أزرار واضحة */
    div.stButton > button {
        border-radius: 6px !important; 
        font-family: 'Cairo', sans-serif !important;
        color: #003366 !important;
        border: 1px solid #003366 !important;
        font-weight: bold !important;
    }
    div.stButton > button:hover {
        background-color: #003366 !important;
        color: white !important;
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
                search_input = st.text_input("🔍 ابحث عن مطور (عربي/English)...", value=st.session_state.search_query)
                if search_input != st.session_state.search_query:
                    st.session_state.search_query = search_input
                    st.session_state.current_page_num = 1
            with f_c2:
                areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
                s_area = st.selectbox("تصفية بالمنطقة", areas)
            st.markdown('</div>', unsafe_allow_html=True)

            # فلترة
            f_df = df.copy()
            if s_area != "الكل": f_df = f_df[f_df['Area'] == s_area]
            if st.session_state.search_query:
                f_df = f_df[f_df['Developer'].astype(str).str.contains(st.session_state.search_query, case=False, na=False)]

            # نظام 3 صفوف (6 كروت)
            items_per_page = 6 
            total_pages = math.ceil(len(f_df) / items_per_page)
            start_idx = (st.session_state.current_page_num - 1) * items_per_page
            page_items = f_df.iloc[start_idx : start_idx + items_per_page]

            grid_cols = st.columns(2)
            for idx, (i, row) in enumerate(page_items.reset_index().iterrows()):
                with grid_cols[idx % 2]:
                    st.markdown(f"""
                        <div class="small-grid-card">
                            <div style="color:#003366; font-weight:900; font-size:1rem;">{row.get('Developer')}</div>
                            <div style="color:#475569; font-size:0.8rem;">📍 {row.get('Area')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("عرض البروفايل", key=f"btn_{i}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'; st.rerun()

            # --- أزرار التنقل (بألوان واضحة) ---
            if total_pages > 1:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f'<div class="page-info">صفحة {st.session_state.current_page_num} من {total_pages}</div>', unsafe_allow_html=True)
                p_c1, p_c2, p_c3, p_c4 = st.columns([1,1,1,1])
                with p_c2:
                    if st.button("⬅️ السابق") and st.session_state.current_page_num > 1:
                        st.session_state.current_page_num -= 1; st.rerun()
                with p_c3:
                    if st.button("التالي ➡️") and st.session_state.current_page_num < total_pages:
                        st.session_state.current_page_num += 1; st.rerun()

        with col_left:
            st.markdown(f'<div class="stat-card"><h5 style="color:#475569;">نتائج البحث</h5><h2 style="color:#003366;">{len(f_df)} شركة</h2></div>', unsafe_allow_html=True)
            st.markdown('<div class="stat-card" style="text-align:right;"><h4 style="color:#003366;">🏆 أقوى 10 شركات</h4>', unsafe_allow_html=True)
            for company in top_10_list:
                if st.button(f"🏢 {company}", key=f"top_{company}", use_container_width=True):
                    st.session_state.search_query = company
                    st.session_state.current_page_num = 1
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التفاصيل ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 عودة للرئيسية"): st.session_state.page = 'main'; st.rerun()
    st.markdown(f"""
        <div style="background:#003366; padding:30px; border-radius:12px; color:white; text-align:center; margin-bottom:20px;">
            <h2 style="color:white !important;">{item.get('Developer')}</h2>
        </div>
        <div class="stat-card" style="text-align:right; border-right:8px solid #D4AF37;">
            <h3 style="color:#003366;">📖 نبذة عن الشركة</h3>
            <p style="color:#1e293b; font-size:1.1rem; line-height:1.7;">{item.get('Company_Bio', 'المعلومات ستتوفر قريباً.')}</p>
        </div>
    """, unsafe_allow_html=True)
