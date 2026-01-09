import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - تم تقليل الحوامش والارتفاع للهيدر
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f4f7f9; 
    }

    /* هيدر نحيف جداً */
    .header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: white;
        padding: 5px 15px; /* تقليل المساحة الداخلية */
        border-radius: 8px;
        box-shadow: 0 1px 5px rgba(0,0,0,0.05);
        margin-bottom: 15px; /* تقليل المسافة تحت الهيدر */
    }

    .dark-bold-text {
        color: #001a33 !important;
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        margin-bottom: 5px;
    }

    .small-grid-card {
        background: white; border-radius: 10px; padding: 12px;
        height: 100px; display: flex; flex-direction: column;
        justify-content: center; border: 1px solid #e2e8f0;
        border-right: 5px solid #0044ff; margin-bottom: 5px;
    }

    /* أزرار الهيدر بحجم أصغر */
    div.stButton > button {
        background-color: #0044ff !important; 
        color: white !important; 
        border-radius: 6px !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: bold !important;
        height: 32px; /* تقليل ارتفاع الأزرار */
        width: 100%;
        font-size: 0.85rem !important;
        border: none !important;
    }

    .header-btns div.stButton > button {
        width: auto !important;
        padding: 0 15px !important;
        background-color: #001a33 !important;
        border: 1px solid #0044ff !important;
    }

    .stat-card {
        background: white; padding: 15px; border-radius: 12px;
        border: 1px solid #e2e8f0; text-align: center; margin-bottom: 15px;
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

# 4. إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'current_page_num' not in st.session_state: st.session_state.current_page_num = 1
if 'search_query' not in st.session_state: st.session_state.search_query = ""
if 'selected_area' not in st.session_state: st.session_state.selected_area = "الكل"

def reset_pagination():
    st.session_state.current_page_num = 1

# --- الهيدر النحيف (Slim Header) ---
st.markdown('<div class="header-bar">', unsafe_allow_html=True)
h_col1, h_col2 = st.columns([3, 1])

with h_col1:
    # تقليل حجم الخط في العنوان
    st.markdown('<h3 style="color:#001a33; font-weight:900; margin:0; font-size:1.3rem;">منصة معلوماتى العقارية</h3>', unsafe_allow_html=True)

with h_col2:
    st.markdown('<div class="header-btns">', unsafe_allow_html=True)
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("🏠 الرئيسية"):
            st.session_state.page = 'main'
            st.session_state.search_query = ""
            st.session_state.selected_area = "الكل"
            st.rerun()
    with btn_col2:
        if st.button("👤 دخول"):
            st.toast("قريباً")
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    if df is not None:
        col_right, col_left = st.columns([1.8, 1])

        with col_right:
            # منطقة الفلاتر
            st.markdown('<div style="background:white; padding:10px; border-radius:10px; border:1px solid #e2e8f0; margin-bottom:15px;">', unsafe_allow_html=True)
            f_c1, f_c2 = st.columns([2, 1])
            with f_c1:
                st.session_state.search_query = st.text_input("🔍 ابحث هنا...", value=st.session_state.search_query, on_change=reset_pagination, label_visibility="collapsed")
            with f_c2:
                areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
                st.session_state.selected_area = st.selectbox("المنطقة", areas, index=areas.index(st.session_state.selected_area), on_change=reset_pagination, label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

            # تطبيق الفلترة
            f_df = df.copy()
            if st.session_state.selected_area != "الكل":
                f_df = f_df[f_df['Area'] == st.session_state.selected_area]
            if st.session_state.search_query:
                q = st.session_state.search_query.lower()
                f_df = f_df[f_df['Developer'].astype(str).str.lower().str.contains(q, na=False)]

            # الكروت
            items_per_page = 6 
            total_pages = math.ceil(len(f_df) / items_per_page)
            start_idx = (st.session_state.current_page_num - 1) * items_per_page
            page_items = f_df.iloc[start_idx : start_idx + items_per_page]

            grid_cols = st.columns(2)
            for idx, (i, row) in enumerate(page_items.reset_index().iterrows()):
                with grid_cols[idx % 2]:
                    st.markdown(f"""
                        <div class="small-grid-card">
                            <div style="color:#001a33; font-weight:900; font-size:0.95rem;">{row.get('Developer')}</div>
                            <div style="color:#475569; font-weight:bold; font-size:0.75rem;">📍 {row.get('Area')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("تفاصيل", key=f"btn_{i}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'; st.rerun()

            # الترقيم
            if total_pages > 1:
                p_c1, p_c2, p_c3, p_c4 = st.columns([1,1,1,1])
                if p_c2.button("السابق") and st.session_state.current_page_num > 1:
                    st.session_state.current_page_num -= 1; st.rerun()
                if p_c3.button("التالي") and st.session_state.current_page_num < total_pages:
                    st.session_state.current_page_num += 1; st.rerun()

        with col_left:
            st.markdown(f'<div class="stat-card" style="padding:10px;"><p style="margin:0; font-weight:bold; color:#001a33;">النتائج: {len(f_df)}</p></div>', unsafe_allow_html=True)
            st.markdown('<div class="stat-card" style="text-align:right;"><p class="dark-bold-text" style="font-size:1rem !important;">🏆 الكبار</p>', unsafe_allow_html=True)
            top_10 = ["Mountain View", "SODIC", "Emaar", "TMG", "Ora Developers", "Palm Hills", "Tatweer Misr", "Misr Italia", "Orascom", "Hassan Allam"]
            for company in top_10:
                if st.button(f"🏢 {company}", key=f"top_{company}"):
                    st.session_state.search_query = company
                    st.session_state.selected_area = "الكل"
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التفاصيل ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    st.markdown(f'<div style="background:#001a33; padding:15px; border-radius:10px; color:white; text-align:center;"><h2 style="margin:0;">{item.get("Developer")}</h2></div>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="stat-card" style="text-align:right; border-right:8px solid #0044ff;">
            <p class="dark-bold-text">📖 النبذة الفنية</p>
            <p style="color:#1e293b; font-size:1.1rem; line-height:1.6; font-weight:bold;">{item.get('Company_Bio', 'لا توجد معلومات.')}</p>
        </div>
    """, unsafe_allow_html=True)
