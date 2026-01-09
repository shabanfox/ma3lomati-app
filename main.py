import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) لمحاكاة الصورة الاحترافية
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
        background-image: linear-gradient(to left, rgba(0, 26, 51, 0.8), rgba(0, 68, 255, 0.4)), 
        url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        height: 180px;
        border-radius: 0 0 20px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 40px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        margin-bottom: 30px;
        position: relative;
    }

    .platform-name {
        color: white;
        font-size: 2rem;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    /* أزرار الهيدر الشفافة */
    .header-btns-container {
        display: flex;
        gap: 15px;
    }

    .stButton > button {
        border-radius: 8px !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: bold !important;
        transition: 0.3s !important;
    }

    /* ستايل كروت الشركات */
    .dev-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        border-top: 4px solid #0044ff;
        transition: transform 0.3s;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .dev-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.05); }

    /* القسم الجانبي (قائمة الكبار) */
    .sidebar-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
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
        if 'Developer' in df.columns:
            df = df.sort_values(by='Developer', ascending=True)
        return df
    except: return None

df = load_data()

# 4. الهيدر الاحترافي (Hero Section)
st.markdown(f"""
    <div class="hero-header">
        <div class="platform-name">منصة معلوماتى العقارية</div>
        <div style="display: flex; gap: 10px;">
            </div>
    </div>
""", unsafe_allow_html=True)

# وضع الأزرار فعلياً فوق الهيدر باستخدام أعمدة مطلقة
header_cols = st.columns([4, 1, 1, 0.5])
with header_cols[1]:
    if st.button("🏠 الرئيسية"):
        st.session_state.page = 'main'; st.rerun()
with header_cols[2]:
    if st.button("👤 دخول"):
        st.toast("قريباً")

# 5. إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'search_query' not in st.session_state: st.session_state.search_query = ""

# --- المحتوى الرئيسي ---
if st.session_state.page == 'main' and df is not None:
    main_col, side_col = st.columns([2.5, 1])

    with main_col:
        # البحث
        search = st.text_input("🔍 ابحث عن المطور العقاري...", value=st.session_state.search_query, placeholder="مثلاً: سوديك، إعمار...")
        
        f_df = df.copy()
        if search:
            f_df = f_df[f_df['Developer'].astype(str).str.contains(search, case=False, na=False)]

        # عرض الكروت (Grid)
        grid = st.columns(2)
        for idx, (i, row) in enumerate(f_df.head(6).reset_index().iterrows()):
            with grid[idx % 2]:
                st.markdown(f"""
                    <div class="dev-card">
                        <div>
                            <div style="font-weight: 900; color: #001a33; font-size: 1.2rem;">{row['Developer']}</div>
                            <div style="color: #64748b; font-size: 0.9rem;">📍 {row['Area']}</div>
                        </div>
                        <div style="color: #0044ff; font-weight: bold; font-size: 0.8rem;">اضغط للتفاصيل ←</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("فتح الملف", key=f"v_{i}"):
                    st.session_state.selected_item = row.to_dict(); st.session_state.page = 'details'; st.rerun()

    with side_col:
        st.markdown('<div class="sidebar-box">', unsafe_allow_html=True)
        st.markdown('<p style="font-weight: 900; color: #001a33; font-size: 1.1rem; border-bottom: 2px solid #f1f5f9; padding-bottom: 10px;">🏆 أقوى المطورين</p>', unsafe_allow_html=True)
        top_10 = ["Mountain View", "SODIC", "Emaar", "TMG", "Ora Developers", "Palm Hills", "Tatweer Misr", "Misr Italia"]
        for company in top_10:
            if st.button(f"🏢 {company}", key=f"side_{company}"):
                st.session_state.search_query = company; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# صفحة التفاصيل
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    st.markdown(f"""
        <div style="background: white; padding: 40px; border-radius: 20px; border: 1px solid #e2e8f0; text-align: center;">
            <h1 style="color: #001a33;">{item['Developer']}</h1>
            <p style="font-size: 1.2rem; color: #64748b;">📍 {item['Area']}</p>
            <hr style="border: 0.5px solid #f1f5f9; margin: 30px 0;">
            <div style="text-align: right; line-height: 1.8; font-weight: bold;">{item.get('Company_Bio', 'المعلومات قيد التحديث...')}</div>
        </div>
    """, unsafe_allow_html=True)
