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
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
    }

    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f8fafc; 
    }

    .header-wrapper {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: white;
        padding: 15px 30px;
        border-radius: 15px;
        box-shadow: 0 2px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    .right-side {
        color: #003366;
        font-weight: 900;
        font-size: 1.8rem;
        margin: 0;
    }

    .small-grid-card {
        background: white; border-radius: 12px; padding: 15px;
        height: 110px; display: flex; flex-direction: column;
        justify-content: center; border: 1px solid #e2e8f0;
        border-right: 5px solid #003366; margin-bottom: 8px;
    }

    .sidebar-section {
        background: white; padding: 20px; border-radius: 15px;
        border: 1px solid #e2e8f0;
    }

    .sidebar-title {
        color: #003366; font-weight: 900; font-size: 1.2rem;
        border-bottom: 3px solid #D4AF37; padding-bottom: 8px; margin-bottom: 15px;
    }

    div.stButton > button {
        border-radius: 8px !important; font-family: 'Cairo', sans-serif !important;
        font-weight: bold !important;
    }
    
    .pagination-info {
        text-align: center; color: #64748b; font-weight: bold; margin-top: 10px;
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
        return df
    except: return None

df = load_data()

# 4. إدارة الحالة (State)
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'search_query' not in st.session_state: st.session_state.search_query = ""
if 'current_page' not in st.session_state: st.session_state.current_page = 1

def reset_page():
    st.session_state.current_page = 1

# --- الهيدر ---
st.markdown('<div class="header-wrapper"><div class="right-side">منصة معلوماتى العقارية</div><div></div></div>', unsafe_allow_html=True)

h_col1, h_col2, h_col3 = st.columns([1, 1, 4])
with h_col1:
    if st.button("🏠 الرئيسية"):
        st.session_state.page = 'main'; st.session_state.search_query = ""; reset_page(); st.rerun()
with h_col2:
    if st.button("👤 دخول"):
        st.toast("قريباً")

# --- محتوى الصفحة ---
if st.session_state.page == 'main' and df is not None:
    col_main, col_side = st.columns([2, 1])

    with col_main:
        # البحث
        search_q = st.text_input("🔍 ابحث عن المطور...", value=st.session_state.search_query, on_change=reset_page)
        st.session_state.search_query = search_q

        f_df = df.copy()
        if st.session_state.search_query:
            f_df = f_df[f_df['Developer'].astype(str).str.contains(st.session_state.search_query, case=False, na=False)]

        # --- تعديل عدد الصفوف ليكون 3 (يعني 6 شركات في الصفحة) ---
        items_per_page = 6  # 3 صفوف × 2 عمود
        total_items = len(f_df)
        total_pages = math.ceil(total_items / items_per_page)
        
        if st.session_state.current_page > total_pages: st.session_state.current_page = 1
        
        start_idx = (st.session_state.current_page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        page_items = f_df.iloc[start_idx:end_idx]

        # عرض الكروت في صفوف
        grid = st.columns(2)
        for idx, (i, row) in enumerate(page_items.reset_index().iterrows()):
            with grid[idx % 2]:
                st.markdown(f"""
                    <div class="small-grid-card">
                        <div style="color:#003366; font-weight:900; font-size:1.1rem;">{row.get('Developer')}</div>
                        <div style="color:#64748b; font-size:0.85rem;">📍 {row.get('Area')}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("التفاصيل", key=f"btn_{i}", use_container_width=True):
                    st.session_state.selected_item = row.to_dict(); st.session_state.page = 'details'; st.rerun()

        # أزرار التنقل
        if total_pages > 1:
            st.write("---")
            pag_col1, pag_col2, pag_col3 = st.columns([1, 2, 1])
            with pag_col3:
                if st.button("الصفحة التالية ⬅️") and st.session_state.current_page < total_pages:
                    st.session_state.current_page += 1; st.rerun()
            with pag_col2:
                st.markdown(f'<div class="pagination-info">صفحة {st.session_state.current_page} من {total_pages}</div>', unsafe_allow_html=True)
            with pag_col1:
                if st.button("➡️ الصفحة السابقة") and st.session_state.current_page > 1:
                    st.session_state.current_page -= 1; st.rerun()

    with col_side:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">🏆 أقوى المطورين</div>', unsafe_allow_html=True)
        top_list = ["Mountain View", "SODIC", "Emaar", "TMG", "Palm Hills", "Ora Developers", "Hassan Allam"]
        for comp in top_list:
            if st.button(f"🏢 {comp}", key=f"side_{comp}", use_container_width=True):
                st.session_state.search_query = comp; reset_page(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# صفحة التفاصيل
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    st.markdown(f"""
        <div style="background:white; padding:30px; border-radius:20px; border:1px solid #e2e8f0; text-align:right;">
            <h1 style="color:#003366; border-right:8px solid #D4AF37; padding-right:15px;">{item.get('Developer')}</h1>
            <p style="color:#64748b; font-weight:bold;">📍 المنطقة: {item.get('Area')}</p>
            <hr>
            <p style="font-size:1.2rem; line-height:1.8;">{item.get('Detailed_Info', 'المعلومات ستتوفر قريباً.')}</p>
        </div>
    """, unsafe_allow_html=True)
