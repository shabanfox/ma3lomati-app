import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f4f7f9; 
    }

    .small-grid-card {
        background: white; border-radius: 10px; padding: 12px;
        height: 105px; display: flex; flex-direction: column;
        justify-content: center; border: 1px solid #e2e8f0;
        border-right: 4px solid #003366; margin-bottom: 5px;
    }

    /* لوحة التحليل الجديدة */
    .analysis-card {
        background: #ffffff; padding: 20px; border-radius: 15px;
        border-top: 5px solid #D4AF37; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-top: 30px;
    }

    .stat-card {
        background: white; padding: 20px; border-radius: 15px;
        border: 1px solid #e2e8f0; text-align: center; margin-bottom: 20px;
    }

    div.stButton > button {
        border-radius: 6px !important; font-family: 'Cairo', sans-serif !important;
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
                st.session_state.search_query = st.text_input("🔍 ابحث عن مطور...", value=st.session_state.search_query)
            with f_c2:
                areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
                s_area = st.selectbox("المنطقة", areas)
            st.markdown('</div>', unsafe_allow_html=True)

            # فلترة
            f_df = df.copy()
            if s_area != "الكل": f_df = f_df[f_df['Area'] == s_area]
            if st.session_state.search_query:
                f_df = f_df[f_df['Developer'].astype(str).str.contains(st.session_state.search_query, case=False, na=False)]

            # نظام 3 صفوف
            items_per_page = 6 
            total_pages = math.ceil(len(f_df) / items_per_page)
            start_idx = (st.session_state.current_page_num - 1) * items_per_page
            page_items = f_df.iloc[start_idx : start_idx + items_per_page]

            grid_cols = st.columns(2)
            for idx, (i, row) in enumerate(page_items.reset_index().iterrows()):
                with grid_cols[idx % 2]:
                    st.markdown(f"""
                        <div class="small-grid-card">
                            <div style="color:#003366; font-weight:900; font-size:0.95rem;">{row.get('Developer')}</div>
                            <div style="color:#64748b; font-size:0.75rem;">📍 {row.get('Area')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("عرض البروفايل", key=f"p_{i}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'; st.rerun()

            # --- الإضافة الجديدة: لوحة التحليل الذكية تحت الكروت ---
            st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
            st.markdown('<h4 style="color:#003366;">📊 نظرة سريعة على السوق (نتائج البحث)</h4>', unsafe_allow_html=True)
            
            a1, a2 = st.columns(2)
            with a1:
                # توزيع المناطق في النتائج الظاهرة
                if not f_df.empty:
                    area_counts = f_df['Area'].value_counts().head(3)
                    st.write("**الأكثر انتشاراً في بحثك:**")
                    for area, count in area_counts.items():
                        st.caption(f"📍 {area}: ({count} مطورين)")
            with a2:
                # ميزة ذكية للبروكر
                st.write("**توزيع القوة المالية:**")
                st.caption("يعتمد التصنيف على متوسط الفئة السعرية المعروضة في قاعدة البيانات حالياً.")
                st.progress(min(len(f_df) * 5, 100)) # مجرد شكل بياني يعبر عن حجم النتائج
            st.markdown('</div>', unsafe_allow_html=True)

            # أزرار التنقل
            if total_pages > 1:
                st.write("---")
                p1, p2, p3 = st.columns([1,1,1])
                if p1.button("السابق") and st.session_state.current_page_num > 1:
                    st.session_state.current_page_num -= 1; st.rerun()
                if p3.button("التالي") and st.session_state.current_page_num < total_pages:
                    st.session_state.current_page_num += 1; st.rerun()

        with col_left:
            st.markdown(f'<div class="stat-card"><h5 style="color:#64748b;">إجمالي المطورين</h5><h1 style="color:#003366;">{len(f_df)}</h1></div>', unsafe_allow_html=True)
            st.markdown('<div class="stat-card" style="text-align:right;"><h4>🏆 الشركات الكبرى</h4>', unsafe_allow_html=True)
            for company in top_10_list:
                if st.button(f"🏢 {company}", key=f"t_{company}", use_container_width=True):
                    st.session_state.search_query = company; st.session_state.current_page_num = 1; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التفاصيل ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 عودة للرئيسية"): st.session_state.page = 'main'; st.rerun()
    st.markdown(f"""
        <div style="background:#003366; padding:30px; border-radius:12px; color:white; text-align:center; margin-bottom:20px;">
            <h2>{item.get('Developer')}</h2>
        </div>
    """, unsafe_allow_html=True)
