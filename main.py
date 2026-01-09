import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - وضع الأزرار داخل الهيدر على اليسار
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    .block-container {
        padding-top: 0rem !important;
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
        background-image: linear-gradient(to left, rgba(0, 26, 51, 0.9), rgba(0, 68, 255, 0.3)), 
        url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        height: 150px;
        border-radius: 0 0 20px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 40px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        position: relative;
    }

    .platform-name {
        color: white;
        font-size: 1.8rem;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    /* تنسيق حاوية الأزرار لتكون فوق الهيدر على اليسار */
    .nav-buttons {
        position: absolute;
        left: 40px;
        top: 50%;
        transform: translateY(-50%);
        display: flex;
        gap: 12px;
        z-index: 1000;
    }

    /* جعل أزرار الـ Streamlit شفافة وأنيقة لتناسب الهيدر */
    div.stButton > button {
        background-color: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 8px !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: bold !important;
        padding: 5px 20px !important;
        transition: 0.3s !important;
        backdrop-filter: blur(5px);
    }

    div.stButton > button:hover {
        background-color: white !important;
        color: #001a33 !important;
        border-color: white !important;
    }

    /* كروت الشركات */
    .dev-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #e2e8f0;
        border-right: 5px solid #0044ff;
        margin-bottom: 10px;
        height: 110px;
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

# 4. بناء الهيدر مع الأزرار في اليسار والاسم في اليمين
# نستخدم حاوية واحدة للهيدر
st.markdown('<div class="hero-header"><div class="platform-name">منصة معلوماتى العقارية</div></div>', unsafe_allow_html=True)

# وضع الأزرار في اليسار فوق الهيدر باستخدام Columns مع Offset
header_overlay = st.columns([1, 1, 4]) 
with header_overlay[0]: # العمود الأول من اليسار
    if st.button("🏠 الرئيسية"):
        st.session_state.page = 'main'; st.session_state.search_query = ""; st.rerun()
with header_overlay[1]: # العمود الثاني من اليسار
    if st.button("👤 دخول"):
        st.toast("قريباً")

# 5. إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'search_query' not in st.session_state: st.session_state.search_query = ""

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main' and df is not None:
    col_main, col_side = st.columns([2, 1])

    with col_main:
        # شريط البحث
        st.session_state.search_query = st.text_input("🔍 ابحث عن مطورك العقاري...", value=st.session_state.search_query)
        
        f_df = df.copy()
        if st.session_state.search_query:
            f_df = f_df[f_df['Developer'].astype(str).str.contains(st.session_state.search_query, case=False, na=False)]

        # عرض الشركات
        grid = st.columns(2)
        for idx, (i, row) in enumerate(f_df.head(6).reset_index().iterrows()):
            with grid[idx % 2]:
                st.markdown(f"""
                    <div class="dev-card">
                        <div style="font-weight: 900; color: #001a33; font-size: 1.1rem;">{row['Developer']}</div>
                        <div style="color: #64748b; font-size: 0.85rem;">📍 {row['Area']}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("التفاصيل", key=f"btn_{i}"):
                    st.session_state.selected_item = row.to_dict(); st.session_state.page = 'details'; st.rerun()

    with col_side:
        st.markdown('<div style="background:white; padding:15px; border-radius:15px; border:1px solid #e2e8f0;">', unsafe_allow_html=True)
        st.markdown('<p style="font-weight:900; color:#001a33; border-bottom:1px solid #eee; padding-bottom:5px;">🏆 قائمة الكبار</p>', unsafe_allow_html=True)
        top_companies = ["Mountain View", "SODIC", "Emaar", "TMG", "Palm Hills", "Hassan Allam"]
        for comp in top_companies:
            if st.button(f"🏢 {comp}", key=f"side_{comp}"):
                st.session_state.search_query = comp; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# صفحة التفاصيل
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    st.markdown(f"""
        <div style="background:white; padding:30px; border-radius:20px; border:1px solid #e2e8f0; text-align:right;">
            <h1 style="color:#001a33; border-right:8px solid #0044ff; padding-right:15px;">{item['Developer']}</h1>
            <p style="color:#64748b; font-weight:bold;">📍 المنطقة: {item['Area']}</p>
            <hr>
            <p style="font-size:1.2rem; line-height:1.8;">{item.get('Company_Bio', 'المعلومات الفنية ستتوفر قريباً.')}</p>
        </div>
    """, unsafe_allow_html=True)
