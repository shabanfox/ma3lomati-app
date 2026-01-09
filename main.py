import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - كروت صغيرة مجمعة لليمين
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f4f7f9; 
    }

    /* مربع الفلتر */
    .filter-card {
        background: white; padding: 15px; border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0; margin-bottom: 20px;
    }

    /* الكارت الصغير المخصص لليمين */
    .small-grid-card {
        background: white; border-radius: 10px; padding: 15px;
        height: 110px; display: flex; flex-direction: column;
        justify-content: center; border: 1px solid #e2e8f0;
        border-right: 4px solid #003366; 
        transition: all 0.2s ease;
        margin-bottom: 5px;
    }
    .small-grid-card:hover { 
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-right-color: #D4AF37;
    }

    /* تنسيق الأزرار الصغيرة */
    div.stButton > button {
        background-color: white !important; color: #003366 !important;
        border: 1px solid #003366 !important; border-radius: 4px !important;
        font-family: 'Cairo', sans-serif !important; font-weight: bold !important;
        height: 30px; font-size: 0.8rem !important; width: 100%;
    }
    div.stButton > button:hover { background-color: #003366 !important; color: white !important; }

    .title-text { color: #003366; font-weight: 900; font-size: 1.8rem; margin-bottom: 15px; }
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
if 'compare_list' not in st.session_state: st.session_state.compare_list = []

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    st.markdown('<div class="title-text">منصة معلوماتى العقارية</div>', unsafe_allow_html=True)

    if df is not None:
        # تقسيم الصفحة لجزئين: اليمين للكروت واليسار للإضافة القادمة
        col_right, col_left = st.columns([1.5, 1]) # اليمين أوسع قليلاً للكروت

        with col_right:
            # مربع الفلتر (داخل عمود اليمين ليكون متناسقاً)
            st.markdown('<div class="filter-card">', unsafe_allow_html=True)
            f_c1, f_c2 = st.columns([1, 1])
            with f_c1:
                search_query = st.text_input("بحث...", placeholder="اسم المطور/الميزة")
            with f_c2:
                areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
                s_area = st.selectbox("المنطقة", areas)
            st.markdown('</div>', unsafe_allow_html=True)

            # منطق الفلترة
            f_df = df.copy()
            if s_area != "الكل": f_df = f_df[f_df['Area'] == s_area]
            if search_query:
                f_df = f_df[f_df['Developer'].astype(str).str.contains(search_query, case=False, na=False) |
                            f_df.get('Detailed_Info','').astype(str).str.contains(search_query, case=False, na=False)]

            # تقسيم الصفحات (نعرض مثلاً 8 كروت بنظام 2*4 في اليمين)
            items_per_page = 8
            total_pages = math.ceil(len(f_df) / items_per_page)
            start_idx = (st.session_state.current_page_num - 1) * items_per_page
            page_items = f_df.iloc[start_idx : start_idx + items_per_page]

            # عرض الكروت في اليمين بنظام 2*2 (داخل العمود الأيمن)
            grid_cols = st.columns(2)
            for idx, (i, row) in enumerate(page_items.reset_index().iterrows()):
                with grid_cols[idx % 2]:
                    st.markdown(f"""
                        <div class="small-grid-card">
                            <div style="color:#003366; font-weight:900; font-size:0.95rem;">{row.get('Developer')}</div>
                            <div style="color:#64748b; font-size:0.75rem;">📍 {row.get('Area', '-')}</div>
                            <div style="color:#D4AF37; font-weight:bold; font-size:0.85rem; margin-top:5px;">💰 {row.get('Price', '-')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    b1, b2 = st.columns(2)
                    with b1:
                        if st.button("تفاصيل", key=f"d_{i}"):
                            st.session_state.selected_item = row.to_dict()
                            st.session_state.page = 'details'; st.rerun()
                    with b2:
                        name = str(row['Developer'])
                        is_in = name in st.session_state.compare_list
                        if st.button("قارن" if not is_in else "إزالة", key=f"c_{i}"):
                            if not is_in: st.session_state.compare_list.append(name)
                            else: st.session_state.compare_list.remove(name)
                            st.rerun()

            # أزرار التنقل (بشكل أصغر)
            if total_pages > 1:
                st.write("")
                p_c1, p_c2, p_c3 = st.columns([1,2,1])
                with p_c2:
                    c_p, c_n = st.columns(2)
                    if c_p.button("السابق") and st.session_state.current_page_num > 1:
                        st.session_state.current_page_num -= 1; st.rerun()
                    if c_n.button("التالي") and st.session_state.current_page_num < total_pages:
                        st.session_state.current_page_num += 1; st.rerun()

        with col_left:
            # مساحة الإضافة جهة اليسار
            st.markdown("""
                <div style="background: #e2e8f0; border: 2px dashed #94a3b8; border-radius: 15px; 
                height: 600px; display: flex; align-items: center; justify-content: center; color: #64748b;">
                    مساحة مخصصة للإضافة (يسار الشاشة)
                </div>
            """, unsafe_allow_html=True)

# --- صفحة التفاصيل (تفتح في كامل الصفحة) ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 عودة"): st.session_state.page = 'main'; st.rerun()
    st.markdown(f"""
        <div style="background-color: #003366; padding: 30px; border-radius: 12px; color: white; text-align: center; margin-bottom: 20px;">
            <h2 style="margin:0;">{item.get('Developer')}</h2>
        </div>
        <div class="filter-card" style="border-right: 8px solid #003366;">
            <p style="font-size:1.1rem; line-height:1.7;">{item.get('Detailed_Info', 'لا توجد بيانات.')}</p>
        </div>
    """, unsafe_allow_html=True)
