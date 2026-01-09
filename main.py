import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - التعديلات الجديدة لليمين واللون الأزرق
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

    /* الهيدر بصورة عقارات احترافية */
    .hero-header {
        background-image: linear-gradient(to left, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.2)), 
        url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        height: 140px;
        border-radius: 0 0 20px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 40px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        position: relative;
    }

    /* اسم المنصة في أقصى اليمين باللون الأزرق */
    .platform-name {
        color: #0044ff !important; /* اللون الأزرق المطلوب */
        font-size: 2.2rem;
        font-weight: 900;
        text-align: right;
        flex-grow: 1;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
    }

    /* حاوية الأزرار في اليسار */
    .nav-buttons-left {
        display: flex;
        gap: 10px;
        justify-content: flex-end;
    }

    /* ستايل الأزرار */
    div.stButton > button {
        background-color: #001a33 !important;
        color: white !important;
        border-radius: 8px !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: bold !important;
        padding: 5px 20px !important;
        border: none !important;
        transition: 0.3s !important;
    }

    div.stButton > button:hover {
        background-color: #0044ff !important;
        box-shadow: 0 4px 12px rgba(0,68,255,0.3);
    }

    /* كروت الشركات */
    .dev-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #e2e8f0;
        border-right: 5px solid #0044ff;
        margin-bottom: 10px;
        height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
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

# 4. بناء الهيدر الاحترافي
# الحاوية الأساسية للهيدر
st.markdown('<div class="hero-header"><div class="platform-name">منصة معلوماتى العقارية</div></div>', unsafe_allow_html=True)

# وضع الأزرار في جهة اليسار فوق الهيدر
header_overlay = st.columns([1.2, 1.2, 5]) 
with header_overlay[0]:
    if st.button("🏠 الرئيسية"):
        st.session_state.page = 'main'; st.session_state.search_query = ""; st.rerun()
with header_overlay[1]:
    if st.button("👤 دخول"):
        st.toast("قريباً")

# 5. إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'search_query' not in st.session_state: st.session_state.search_query = ""

# --- المحتوى الرئيسي ---
if st.session_state.page == 'main' and df is not None:
    col_main, col_side = st.columns([2.2, 1])

    with col_main:
        # البحث
        st.session_state.search_query = st.text_input("🔍 ابحث عن مطور عقاري...", value=st.session_state.search_query)
        
        f_df = df.copy()
        if st.session_state.search_query:
            f_df = f_df[f_df['Developer'].astype(str).str.contains(st.session_state.search_query, case=False, na=False)]

        # عرض الشركات (2 في كل صف)
        grid = st.columns(2)
        for idx, (i, row) in enumerate(f_df.head(6).reset_index().iterrows()):
            with grid[idx % 2]:
                st.markdown(f"""
                    <div class="dev-card">
                        <div style="font-weight: 900; color: #001a33; font-size: 1.1rem;">{row['Developer']}</div>
                        <div style="color: #64748b; font-size: 0.85rem;">📍 {row['Area']}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("عرض التفاصيل", key=f"btn_{i}"):
                    st.session_state.selected_item = row.to_dict(); st.session_state.page = 'details'; st.rerun()

    with col_side:
        st.markdown('<div style="background:white; padding:15px; border-radius:15px; border:1px solid #e2e8f0; box-shadow: 0 4px 6px rgba(0,0,0,0.02);">', unsafe_allow_html=True)
        st.markdown('<p style="font-weight:900; color:#0044ff; border-bottom:2px solid #f1f5f9; padding-bottom:10px; font-size:1.1rem;">🏆 قائمة الكبار</p>', unsafe_allow_html=True)
        top_companies = ["Mountain View", "SODIC", "Emaar", "TMG", "Palm Hills", "Ora Developers", "Hassan Allam"]
        for comp in top_companies:
            if st.button(f"🏢 {comp}", key=f"side_{comp}"):
                st.session_state.search_query = comp; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# صفحة التفاصيل
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    st.markdown(f"""
        <div style="background:white; padding:30px; border-radius:20px; border:1px solid #e2e8f0; text-align:right; box-shadow: 0 10px 30px rgba(0,0,0,0.05);">
            <h1 style="color:#0044ff; border-right:10px solid #001a33; padding-right:20px;">{item['Developer']}</h1>
            <p style="color:#64748b; font-size:1.1rem; margin-top:10px;">📍 الموقع: <b>{item['Area']}</b></p>
            <hr style="border:0; border-top:1px solid #eee; margin:25px 0;">
            <p style="font-size:1.25rem; line-height:1.9; color:#1e293b;">{item.get('Company_Bio', 'المعلومات الفنية ستتوفر قريباً لهذه الشركة.')}</p>
        </div>
    """, unsafe_allow_html=True)
