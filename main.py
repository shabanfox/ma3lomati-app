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
        font-family: 'Cairo', sans-serif; background-color: #f4f7f9; 
    }

    .header-bar {
        display: flex; justify-content: space-between; align-items: center;
        background-color: white; padding: 10px 20px; border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 10px;
    }

    /* بار المؤشرات الاقتصادية */
    .market-bar {
        background: #001a33; color: white; padding: 5px 15px;
        border-radius: 8px; margin-bottom: 20px; font-size: 0.85rem;
        display: flex; justify-content: space-around;
    }

    .small-grid-card {
        background: white; border-radius: 10px; padding: 12px;
        height: 130px; display: flex; flex-direction: column;
        justify-content: center; border: 1px solid #e2e8f0;
        border-right: 5px solid #0044ff; margin-bottom: 5px; position: relative;
    }

    /* تاجات الزتونة */
    .tag {
        display: inline-block; background: #e0e7ff; color: #0044ff;
        padding: 2px 8px; border-radius: 5px; font-size: 0.7rem;
        margin-top: 5px; font-weight: bold;
    }

    div.stButton > button {
        background-color: #0044ff !important; color: white !important; 
        border-radius: 8px !important; font-weight: bold !important; height: 35px; width: 100%;
    }

    .header-btns div.stButton > button {
        width: auto !important; padding: 0 20px !important;
        background-color: #001a33 !important; border: 1px solid #0044ff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات والترتيب
@st.cache_data(ttl=60)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [str(c).strip() for c in df.columns]
        # الترتيب من الأقوى (Rank 1) للأقل
        if 'Rank' in df.columns:
            df['Rank'] = pd.to_numeric(df['Rank'], errors='coerce').fillna(999)
            df = df.sort_values(by='Rank', ascending=True)
        return df
    except: return None

df = load_data()

# الهيدر
st.markdown('<div class="header-bar">', unsafe_allow_html=True)
h_col1, h_col2 = st.columns([2, 1])
with h_col1: st.markdown('<h2 style="color:#001a33; font-weight:900; margin:0;">منصة معلوماتى العقارية</h2>', unsafe_allow_html=True)
with h_col2:
    st.markdown('<div class="header-btns">', unsafe_allow_html=True)
    bc1, bc2 = st.columns(2)
    with bc1: 
        if st.button("🏠 الرئيسية"): st.session_state.page='main'; st.rerun()
    with bc2: 
        if st.button("👤 دخول"): st.toast("قريباً")
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# إضافة بار المؤشرات الاقتصادي (الاقتراح الأول)
st.markdown("""
    <div class="market-bar">
        <span>💵 دولار/جنيه: 48.50</span>
        <span>🟡 ذهب عيار 21: 3250 ج.م</span>
        <span>📈 حالة السوق: مستقر</span>
    </div>
""", unsafe_allow_html=True)

# باقي منطق الصفحة (Main)
if 'page' not in st.session_state: st.session_state.page = 'main'
if st.session_state.page == 'main' and df is not None:
    col_right, col_left = st.columns([1.8, 1])
    with col_right:
        # الفلاتر والبحث
        st.session_state.search_query = st.text_input("🔍 ابحث عن المطور (مثلاً: سوديك)...")
        
        f_df = df.copy()
        if st.session_state.search_query:
            f_df = f_df[f_df['Developer'].astype(str).str.contains(st.session_state.search_query, case=False, na=False)]
        
        # عرض الكروت
        grid_cols = st.columns(2)
        page_items = f_df.head(6) # للعرض السريع
        for idx, (i, row) in enumerate(page_items.reset_index().iterrows()):
            with grid_cols[idx % 2]:
                # التاجات الديناميكية (الاقتراح الثاني)
                tags = row.get('Tags', 'مطور موثوق').split(',') 
                tags_html = "".join([f'<span class="tag">{t}</span> ' for t in tags[:2]])
                
                st.markdown(f"""
                    <div class="small-grid-card">
                        <div style="color:#001a33; font-weight:900; font-size:1.1rem;">{row.get('Developer')}</div>
                        <div style="color:#475569; font-size:0.8rem;">📍 {row.get('Area')}</div>
                        <div>{tags_html}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("التفاصيل", key=f"d_{i}"):
                    st.session_state.selected_item = row.to_dict(); st.session_state.page='details'; st.rerun()
    
    with col_left:
        st.markdown(f'<div class="stat-card"><h3>{len(f_df)}</h3><p>مطور متاح</p></div>', unsafe_allow_html=True)

# صفحة التفاصيل
elif st.session_state.page == 'details':
    st.write("عرض تفاصيل المطور...")
