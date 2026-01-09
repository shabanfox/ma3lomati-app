import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - تركيز على الأناقة والبساطة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    .block-container { padding-top: 1rem !important; }

    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f4f7f9; 
    }

    /* الهيدر */
    .header-wrapper {
        background: white; padding: 15px 30px; border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px;
        display: flex; justify-content: space-between; align-items: center;
    }

    /* مربع البحث المطور بمربعات الاختيار */
    .advanced-search-box {
        background: #ffffff; padding: 25px; border-radius: 15px;
        border: 1px solid #e2e8f0; margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }

    /* كروت المطورين */
    .small-grid-card {
        background: white; border-radius: 12px; padding: 18px;
        border: 1px solid #e2e8f0; border-right: 6px solid #003366;
        margin-bottom: 12px; transition: 0.3s;
    }
    .small-grid-card:hover { transform: translateY(-3px); box-shadow: 0 8px 15px rgba(0,0,0,0.08); }

    div.stButton > button {
        border-radius: 8px !important; font-family: 'Cairo', sans-serif !important;
        font-weight: bold !important;
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

# إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'current_page' not in st.session_state: st.session_state.current_page = 1

# --- الهيدر ---
st.markdown('<div class="header-wrapper"><div style="color:#003366; font-weight:900; font-size:1.8rem;">منصة معلوماتى العقارية</div><div></div></div>', unsafe_allow_html=True)

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main' and df is not None:
    
    # --- مربع البحث المتطور (قوائم اختيار) ---
    st.markdown('<div class="advanced-search-box">', unsafe_allow_html=True)
    st.markdown('<p style="color:#003366; font-weight:900; font-size:1.2rem; margin-bottom:15px;">🔍 ابحث بدقة عن مشروعك</p>', unsafe_allow_html=True)
    
    # الصف الأول: البحث الأساسي
    f_row1_c1, f_row1_c2, f_row1_c3 = st.columns([2, 1, 1])
    with f_row1_c1:
        search_name = st.text_input("اسم المطور / المشروع", placeholder="اكتب للبحث...")
    with f_row1_c2:
        areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
        sel_area = st.selectbox("المنطقة", areas)
    with f_row1_c3:
        years_list = ["الكل", "3 سنوات", "5 سنوات", "7 سنوات", "8 سنوات", "10 سنوات"]
        sel_years = st.selectbox("مدة التقسيط", years_list)

    # الصف الثاني: مربعات اختيار للماليات
    f_row2_c1, f_row2_c2, f_row2_c3 = st.columns(3)
    with f_row2_c1:
        # تحويل المقدم لنسبة أو رقم محدد
        down_list = ["الكل", "0%", "5%", "10%", "15%", "20%", "أخرى"]
        sel_down = st.selectbox("نسبة المقدم", down_list)
    with f_row2_c2:
        price_list = ["الكل", "أقل من 3 مليون", "3 - 7 مليون", "7 - 12 مليون", "أكثر من 12 مليون"]
        sel_price = st.selectbox("الميزانية (السعر الإجمالي)", price_list)
    with f_row2_c3:
        st.write(" ") # للمحاذاة
        if st.button("🔄 مسح الفلاتر", use_container_width=True):
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # --- منطق الفلترة ---
    f_df = df.copy()
    if search_name:
        f_df = f_df[f_df['Developer'].astype(str).str.contains(search_name, case=False, na=False)]
    if sel_area != "الكل":
        f_df = f_df[f_df['Area'] == sel_area]
    # هنا يتم إضافة شروط الفلترة لسنوات القسط والمقدم بناءً على أعمدة جدولك
    # مثال: if sel_years != "الكل": f_df = f_df[f_df['Years'] == sel_years]

    # --- عرض النتائج ---
    col_main, col_side = st.columns([2.3, 1])

    with col_main:
        items_per_page = 6
        total_pages = math.ceil(len(f_df) / items_per_page)
        start_idx = (st.session_state.current_page - 1) * items_per_page
        page_items = f_df.iloc[start_idx:start_idx+items_per_page]

        if len(f_df) == 0:
            st.warning("لم يتم العثور على نتائج تطابق اختياراتك.")
        else:
            grid = st.columns(2)
            for idx, (i, row) in enumerate(page_items.reset_index().iterrows()):
                with grid[idx % 2]:
                    st.markdown(f"""
                        <div class="small-grid-card">
                            <div style="font-weight:900; color:#003366; font-size:1.1rem;">{row.get('Developer')}</div>
                            <div style="color:#64748b; font-size:0.85rem; margin-bottom:10px;">📍 {row.get('Area')}</div>
                            <div style="display:flex; gap:10px;">
                                <small style="background:#f0f7ff; color:#003366; padding:2px 6px; border-radius:4px;">💰 مقدم {row.get('Downpayment', '10%')}</small>
                                <small style="background:#fff7ed; color:#9a3412; padding:2px 6px; border-radius:4px;">⏳ {row.get('Years', '7')} سنوات</small>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("عرض التفاصيل", key=f"btn_{i}", use_container_width=True):
                        st.session_state.selected_item = row.to_dict(); st.session_state.page = 'details'; st.rerun()

    with col_side:
        # عداد نتائج شيك
        st.markdown(f"""
            <div style="background:white; padding:20px; border-radius:15px; border:1px solid #e2e8f0; text-align:center;">
                <h5 style="color:#64748b; margin:0;">نتائج البحث</h5>
                <h2 style="color:#003366; margin:10px 0;">{len(f_df)}</h2>
                <p style="font-size:0.8rem; color:#94a3b8;">مطابق للمواصفات</p>
            </div>
        """, unsafe_allow_html=True)

# --- صفحة التفاصيل (التعديل المطلوب للنبذة والمشاريع) ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 العودة للبحث"): st.session_state.page = 'main'; st.rerun()
    
    st.markdown(f"""
        <div style="background:white; padding:30px; border-radius:15px; border-right:10px solid #003366; margin-bottom:20px;">
            <h1 style="color:#003366; margin:0;">{item.get('Developer')}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    tab_bio, tab_projs = st.tabs(["📝 نبذة عن المطور", "🏗️ مشاريع المطور"])
    
    with tab_bio:
        st.markdown(f'<div style="background:white; padding:20px; border-radius:10px;">{item.get("Detailed_Info", "لا توجد بيانات.")}</div>', unsafe_allow_html=True)
    
    with tab_projs:
        st.info(f"عرض كافة مشاريع {item.get('Developer')} في منطقة {item.get('Area')}")
        # هنا يمكنك عرض قائمة بالمشاريع من جدول البيانات
