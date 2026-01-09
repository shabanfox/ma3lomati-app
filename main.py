import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - رفع الأزرار لأعلى اليسار
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        padding-left: 5% !important;
        padding-right: 5% !important;
    }

    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f8fafc; 
    }

    /* الهيدر الاحترافي */
    .hero-header {
        background-image: linear-gradient(to left, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.3)), 
        url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        height: 120px;
        border-radius: 0 0 25px 25px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 40px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        position: relative;
    }

    /* اسم المنصة أقصى اليمين */
    .platform-name {
        color: #0044ff !important;
        font-size: 1.8rem;
        font-weight: 900;
        margin: 0;
    }

    /* حاوية الأزرار - تم رفعها للأعلى */
    .stButton > button {
        background-color: #001a33 !important;
        color: white !important;
        border-radius: 8px !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: bold !important;
        height: 35px !important;
        padding: 0 20px !important;
        border: none !important;
        font-size: 0.85rem !important;
        transition: 0.3s !important;
        margin-top: -60px; /* سحب الأزرار للأعلى لتكون في مستوى العنوان */
    }

    div.stButton > button:hover {
        background-color: #0044ff !important;
        transform: translateY(-2px);
    }

    .dev-card {
        background: white; border-radius: 12px; padding: 15px;
        border: 1px solid #e2e8f0; border-right: 5px solid #0044ff;
        margin-bottom: 10px; height: 100px;
        display: flex; flex-direction: column; justify-content: center;
    }

    .sidebar-box {
        background: white; padding: 15px; border-radius: 15px;
        border: 1px solid #e2e8f0;
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

# 4. بناء الهيدر
st.markdown('<div class="hero-header"><div class="platform-name">منصة معلوماتى العقارية</div></div>', unsafe_allow_html=True)

# وضع الأزرار في أقصى اليسار العلوي
header_overlay = st.columns([1, 1, 5]) 
with header_overlay[0]:
    if st.button("🏠 الرئيسية"):
        st.session_state.page = 'main'; st.session_state.search_query = ""; st.rerun()
with header_overlay[1]:
    if st.button("👤 دخول"):
        st.toast("نافذة الدخول قريباً")

# 5. إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'search_query' not in st.session_state: st.session_state.search_query = ""

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main' and df is not None:
    col_main, col_side = st.columns([2.2, 1])

    with col_main:
        st.session_state.search_query = st.text_input("🔍 ابحث عن المطور...", value=st.session_state.search_query)
        f_df = df.copy()
        if st.session_state.search_query:
            f_df = f_df[f_df['Developer'].astype(str).str.contains(st.session_state.search_query, case=False, na=False)]

        grid = st.columns(2)
        for idx, (i, row) in enumerate(f_df.head(6).reset_index().iterrows()):
            with grid[idx % 2]:
                st.markdown(f"""
                    <div class="dev-card">
                        <div style="font-weight: 900; color: #001a33;">{row['Developer']}</div>
                        <div style="color: #64748b; font-size: 0.8rem;">📍 {row['Area']}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("عرض", key=f"btn_{i}"):
                    st.session_state.selected_item = row.to_dict(); st.session_state.page = 'details'; st.rerun()

    with col_side:
        st.markdown('<div class="sidebar-box">', unsafe_allow_html=True)
        st.markdown('<p style="font-weight:900; color:#0044ff; border-bottom:1px solid #f1f5f9; padding-bottom:10px;">🏆 الكبار</p>', unsafe_allow_html=True)
        top_list = ["Mountain View", "SODIC", "Emaar", "TMG", "Palm Hills", "Ora Developers"]
        for comp in top_list:
            if st.button(f"🏢 {comp}", key=f"side_{comp}"):
                st.session_state.search_query = comp; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# صفحة التفاصيل
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    st.markdown(f"""
        <div style="background:white; padding:30px; border-radius:20px; border:1px solid #e2e8f0; text-align:right;">
            <h1 style="color:#0044ff; border-right:10px solid #001a33; padding-right:15px;">{item['Developer']}</h1>
            <p style="color:#64748b;">📍 المنطقة: {item['Area']}</p>
            <hr>
            <p style="font-size:1.2rem; line-height:1.8;">{item.get('Company_Bio', 'المعلومات ستتوفر قريباً.')}</p>
        </div>
    """, unsafe_allow_html=True)
