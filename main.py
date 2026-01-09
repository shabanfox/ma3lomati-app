import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - الهيدر المتحرك وتنسيق اليمين
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f4f7f9; 
    }

    /* الهيدر الاحترافي بخلفية متحركة */
    .header-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: linear-gradient(-45deg, #001a33, #0044ff, #001a33, #0088ff);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        padding: 8px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        color: white;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* أزرار الهيدر */
    .header-btns div.stButton > button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 6px !important;
        height: 32px;
        padding: 0 15px !important;
        font-size: 0.85rem !important;
        transition: 0.3s;
    }
    
    .header-btns div.stButton > button:hover {
        background-color: white !important;
        color: #001a33 !important;
    }

    .small-grid-card {
        background: white; border-radius: 10px; padding: 10px;
        height: 90px; display: flex; flex-direction: column;
        justify-content: center; border: 1px solid #e2e8f0;
        border-right: 5px solid #0044ff; margin-bottom: 5px;
    }

    div.stButton > button {
        background-color: #0044ff !important; 
        color: white !important; 
        border-radius: 6px !important;
        height: 35px; width: 100%; border: none !important;
    }

    .stat-card {
        background: white; padding: 12px; border-radius: 10px;
        border: 1px solid #e2e8f0; text-align: center; margin-bottom: 10px;
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

# --- الهيدر (Header) باليمين والخلفية المتحركة ---
st.markdown('<div class="header-bar">', unsafe_allow_html=True)
h_col1, h_col2 = st.columns([3, 1])

with h_col1:
    # اسم المنصة في اليمين تماماً
    st.markdown('<h3 style="margin:0; font-weight:900; font-size:1.4rem; color:white;">منصة معلوماتى العقارية</h3>', unsafe_allow_html=True)

with h_col2:
    # الأزرار في اليسار
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

# --- المحتوى الرئيسي ---
if st.session_state.page == 'main':
    if df is not None:
        col_right, col_left = st.columns([1.8, 1])

        with col_right:
            # منطقة البحث
            st.markdown('<div style="background:white; padding:8px; border-radius:10px; border:1px solid #e2e8f0; margin-bottom:10px;">', unsafe_allow_html=True)
            f_c1, f_c2 = st.columns([2, 1])
            with f_c1:
                st.session_state.search_query = st.text_input("ابحث...", value=st.session_state.search_query, label_visibility="collapsed")
            with f_c2:
                areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
                st.session_state.selected_area = st.selectbox("المنطقة", areas, index=areas.index(st.session_state.selected_area), label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

            # تطبيق الفلترة
            f_df = df.copy()
            if st.session_state.selected_area != "الكل":
                f_df = f_df[f_df['Area'] == st.session_state.selected_area]
            if st.session_state.search_query:
                q = st.session_state.search_query.lower()
                f_df = f_df[f_df['Developer'].astype(str).str.lower().str.contains(q, na=False)]

            items_per_page = 6
            start_idx = (st.session_state.current_page_num - 1) * items_per_page
            page_items = f_df.iloc[start_idx : start_idx + items_per_page]

            grid_cols = st.columns(2)
            for idx, (i, row) in enumerate(page_items.reset_index().iterrows()):
                with grid_cols[idx % 2]:
                    st.markdown(f"""
                        <div class="small-grid-card">
                            <div style="color:#001a33; font-weight:900; font-size:0.9rem;">{row.get('Developer')}</div>
                            <div style="color:#475569; font-weight:bold; font-size:0.7rem;">📍 {row.get('Area')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("تفاصيل", key=f"btn_{i}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'; st.rerun()

        with col_left:
            st.markdown(f'<div class="stat-card" style="padding:8px;"><p style="margin:0; font-weight:bold; color:#001a33;">النتائج: {len(f_df)}</p></div>', unsafe_allow_html=True)
            st.markdown('<div class="stat-card" style="text-align:right;"><p style="color:#001a33; font-weight:900; margin-bottom:5px;">🏆 الكبار</p>', unsafe_allow_html=True)
            top_10 = ["Mountain View", "SODIC", "Emaar", "TMG", "Ora Developers", "Palm Hills", "Tatweer Misr", "Misr Italia", "Orascom", "Hassan Allam"]
            for company in top_10:
                if st.button(f"🏢 {company}", key=f"top_{company}"):
                    st.session_state.search_query = company; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    st.markdown(f'<div style="background:#001a33; padding:15px; border-radius:10px; color:white; text-align:center;"><h3 style="margin:0;">{item.get("Developer")}</h3></div>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown(f'<div class="stat-card" style="text-align:right; border-right:5px solid #0044ff;"><p style="font-weight:bold;">{item.get("Company_Bio", "لا توجد معلومات.")}</p></div>', unsafe_allow_html=True)
