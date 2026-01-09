import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) المطور للفلاتر الديناميكية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    .block-container { padding-top: 1rem !important; }

    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f0f4f8; 
    }

    /* الهيدر */
    .header-wrapper {
        background: white; padding: 15px 30px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
        display: flex; justify-content: space-between; align-items: center;
    }

    /* مربع البحث المتطور */
    .advanced-search-box {
        background: white; padding: 25px; border-radius: 20px;
        border: 1px solid #e2e8f0; margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.03);
    }

    .filter-label { color: #003366; font-weight: 700; margin-bottom: 8px; display: block; }

    /* كروت المطورين */
    .small-grid-card {
        background: white; border-radius: 15px; padding: 20px;
        border: 1px solid #e2e8f0; border-right: 6px solid #0044ff;
        margin-bottom: 15px; transition: 0.3s ease;
    }
    .small-grid-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.08); }

    /* الأزرار */
    div.stButton > button {
        border-radius: 10px !important; font-family: 'Cairo', sans-serif !important;
        font-weight: bold !important; transition: 0.3s;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات (مع معالجة القيم العددية)
@st.cache_data(ttl=60)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [str(c).strip() for c in df.columns]
        # تحويل الأعمدة الرقمية لضمان عمل الفلاتر (إذا كانت تحتوي على أرقام)
        for col in ['Price', 'Downpayment', 'Years']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[^0-9]', '', regex=True), errors='coerce').fillna(0)
        return df
    except: return None

df = load_data()

# 4. إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'current_page' not in st.session_state: st.session_state.current_page = 1

def reset_page(): st.session_state.current_page = 1

# --- الهيدر ---
st.markdown('<div class="header-wrapper"><div style="color:#003366; font-weight:900; font-size:1.8rem;">منصة معلوماتى العقارية</div><div></div></div>', unsafe_allow_html=True)

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main' and df is not None:
    
    # --- مربع البحث المتطور (Advanced Filter Section) ---
    st.markdown('<div class="advanced-search-box">', unsafe_allow_html=True)
    st.markdown('<p style="color:#0044ff; font-weight:900; font-size:1.2rem; margin-bottom:20px;">🔍 محرك البحث الذكي</p>', unsafe_allow_html=True)
    
    row1_c1, row1_c2, row1_c3 = st.columns([2, 1, 1])
    with row1_c1:
        search_name = st.text_input("اسم المطور", placeholder="اكتب اسم الشركة هنا...", on_change=reset_page)
    with row1_c2:
        all_areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
        sel_area = st.selectbox("المنطقة", all_areas, on_change=reset_page)
    with row1_c3:
        sel_years = st.selectbox("عدد سنوات القسط", ["الكل", "3 سنوات", "5 سنوات", "7 سنوات", "10 سنوات", "أكثر"], on_change=reset_page)

    st.markdown('<hr style="margin:15px 0; border-top:1px solid #eee;">', unsafe_allow_html=True)
    
    row2_c1, row2_c2, row2_c3 = st.columns(3)
    with row2_c1:
        max_price = st.select_slider("أقصى سعر إجمالي (مليون ج.م)", options=list(range(1, 51)), value=50, on_change=reset_page)
    with row2_c2:
        max_down = st.select_slider("أقصى مقدم (ألف ج.م)", options=list(range(50, 1001, 50)), value=1000, on_change=reset_page)
    with row2_c3:
        st.write(" ") # محاذاة
        if st.button("✨ تنظيف الفلاتر", use_container_width=True):
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- منطق الفلترة المتقدم ---
    f_df = df.copy()
    if search_name:
        f_df = f_df[f_df['Developer'].astype(str).str.contains(search_name, case=False, na=False)]
    if sel_area != "الكل":
        f_df = f_df[f_df['Area'] == sel_area]
    
    # ملاحظة: الفلاتر الرقمية أدناه تعمل إذا كانت بيانات الـ CSV تحتوي على أعمدة (Price, Downpayment, Years)
    if 'Price' in f_df.columns:
        f_df = f_df[f_df['Price'] <= max_price * 1000000]
    if 'Downpayment' in f_df.columns:
        f_df = f_df[f_df['Downpayment'] <= max_down * 1000]

    # --- عرض النتائج ---
    col_main, col_side = st.columns([2.3, 1])

    with col_main:
        items_per_page = 6
        total_pages = math.ceil(len(f_df) / items_per_page)
        start_idx = (st.session_state.current_page - 1) * items_per_page
        page_items = f_df.iloc[start_idx:start_idx+items_per_page]

        if len(f_df) == 0:
            st.info("لم نجد نتائج تطابق هذه المواصفات.. حاول تقليل القيود.")
        else:
            grid = st.columns(2)
            for idx, (i, row) in enumerate(page_items.reset_index().iterrows()):
                with grid[idx % 2]:
                    st.markdown(f"""
                        <div class="small-grid-card">
                            <div style="font-weight:900; color:#003366; font-size:1.2rem; margin-bottom:5px;">{row.get('Developer')}</div>
                            <div style="color:#64748b; font-size:0.9rem;">📍 {row.get('Area')}</div>
                            <div style="display:flex; justify-content:space-between; margin-top:10px;">
                                <span style="background:#eef2ff; color:#0044ff; padding:2px 8px; border-radius:5px; font-size:0.8rem;">💰 مقدم: {row.get('Downpayment', '---')}</span>
                                <span style="background:#fff7ed; color:#ea580c; padding:2px 8px; border-radius:5px; font-size:0.8rem;">⏳ {row.get('Years', '---')} سنوات</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("فتح ملف الشركة", key=f"det_{i}", use_container_width=True):
                        st.session_state.selected_item = row.to_dict(); st.session_state.page = 'details'; st.rerun()

    with col_side:
        st.markdown(f"""
            <div style="background:#003366; color:white; padding:20px; border-radius:15px; text-align:center;">
                <h4 style="margin:0;">النتائج المطابقة</h4>
                <h1 style="margin:0; font-size:3rem;">{len(f_df)}</h1>
                <p style="margin:0; opacity:0.8;">شركة ومطوّر</p>
            </div>
        """, unsafe_allow_html=True)

# --- صفحة التفاصيل ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 عودة للبحث"): st.session_state.page = 'main'; st.rerun()
    st.markdown(f"""
        <div style="background:white; padding:40px; border-radius:25px; border-right:10px solid #0044ff;">
            <h1 style="color:#003366;">{item.get('Developer')}</h1>
            <p style="font-size:1.3rem; line-height:1.8;">{item.get('Detailed_Info', 'لا توجد بيانات فنية حالياً.')}</p>
        </div>
    """, unsafe_allow_html=True)
