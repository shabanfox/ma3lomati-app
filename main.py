import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - النسخة الاحترافية الشاملة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    .block-container { padding-top: 1rem !important; }

    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f8fafc; 
    }

    /* الهيدر: العنوان يمين */
    .header-wrapper {
        display: flex; justify-content: space-between; align-items: center;
        background: white; padding: 15px 30px; border-radius: 15px;
        box-shadow: 0 2px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
    }
    .right-side { color: #003366; font-weight: 900; font-size: 1.8rem; margin: 0; }

    /* مربع البحث المتطور */
    .advanced-search-box {
        background: white; padding: 25px; border-radius: 20px;
        border: 1px solid #e2e8f0; margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.03);
    }

    /* الكروت */
    .small-grid-card {
        background: white; border-radius: 12px; padding: 15px;
        height: 120px; display: flex; flex-direction: column;
        justify-content: center; border: 1px solid #e2e8f0;
        border-right: 6px solid #003366; margin-bottom: 8px;
        transition: 0.3s ease;
    }
    .small-grid-card:hover { transform: translateY(-3px); box-shadow: 0 8px 15px rgba(0,0,0,0.08); }

    div.stButton > button {
        border-radius: 8px !important; font-family: 'Cairo', sans-serif !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات ومعالجتها رقمياً للفلاتر
@st.cache_data(ttl=60)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [str(c).strip() for c in df.columns]
        # تنظيف البيانات الرقمية
        for col in ['Price', 'Downpayment', 'Years']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.extract('(\d+)')[0], errors='coerce').fillna(0)
        return df
    except: return None

df = load_data()

# 4. إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'search_query' not in st.session_state: st.session_state.search_query = ""
if 'current_page' not in st.session_state: st.session_state.current_page = 1

def reset_page(): st.session_state.current_page = 1

# --- الهيدر ---
st.markdown('<div class="header-wrapper"><div class="right-side">منصة معلوماتى العقارية</div><div></div></div>', unsafe_allow_html=True)

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main' and df is not None:
    
    # --- مربع البحث المتطور (Advanced Dynamic Filters) ---
    st.markdown('<div class="advanced-search-box">', unsafe_allow_html=True)
    st.markdown('<p style="color:#003366; font-weight:900; font-size:1.2rem; margin-bottom:15px;">🔍 الفلاتر الذكية</p>', unsafe_allow_html=True)
    
    row1_c1, row1_c2, row1_c3 = st.columns([2, 1, 1])
    with row1_c1:
        s_name = st.text_input("اسم المطور / المشروع", value=st.session_state.search_query, on_change=reset_page)
        st.session_state.search_query = s_name
    with row1_c2:
        areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
        s_area = st.selectbox("📍 المنطقة", areas, on_change=reset_page)
    with row1_c3:
        s_years = st.selectbox("⏳ مدة التقسيط (سنة)", ["الكل", "3", "5", "7", "8", "10"], on_change=reset_page)

    row2_c1, row2_c2, row2_c3 = st.columns(3)
    with row2_c1:
        s_down = st.selectbox("💰 نسبة المقدم", ["الكل", "0%", "5%", "10%", "15%", "20%"], on_change=reset_page)
    with row2_c2:
        s_price = st.selectbox("💵 الميزانية الإجمالية", ["الكل", "أقل من 5 مليون", "5 - 10 مليون", "أكثر من 10 مليون"], on_change=reset_page)
    with row2_c3:
        st.write(" ")
        if st.button("🔄 مسح الفلاتر", use_container_width=True):
            st.session_state.search_query = ""; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # تطبيق منطق الفلترة
    f_df = df.copy()
    if st.session_state.search_query:
        f_df = f_df[f_df['Developer'].astype(str).str.contains(st.session_state.search_query, case=False, na=False)]
    if s_area != "الكل":
        f_df = f_df[f_df['Area'] == s_area]
    if s_years != "الكل":
        f_df = f_df[f_df['Years'] >= int(s_years)]
    if s_down != "الكل":
        d_val = int(s_down.replace('%',''))
        f_df = f_df[f_df['Downpayment'] <= d_val]

    # --- عرض المحتوى (3 صفوف × 2 عمود) ---
    col_main, col_side = st.columns([2.3, 1])

    with col_main:
        items_per_page = 6 # 3 صفوف
        total_pages = math.ceil(len(f_df) / items_per_page)
        start_idx = (st.session_state.current_page - 1) * items_per_page
        page_items = f_df.iloc[start_idx : start_idx + items_per_page]

        if f_df.empty:
            st.info("لا توجد نتائج مطابقة.")
        else:
            grid = st.columns(2)
            for idx, (i, row) in enumerate(page_items.reset_index().iterrows()):
                with grid[idx % 2]:
                    st.markdown(f"""
                        <div class="small-grid-card">
                            <div style="font-weight:900; color:#003366; font-size:1.1rem;">{row.get('Developer')}</div>
                            <div style="color:#64748b; font-size:0.85rem;">📍 {row.get('Area')}</div>
                            <div style="margin-top:8px;">
                                <small style="background:#f0f7ff; color:#003366; padding:2px 6px; border-radius:4px;">💰 مقدم: {row.get('Downpayment')}%</small>
                                <small style="background:#fff7ed; color:#9a3412; padding:2px 6px; border-radius:4px;">⏳ تقسيط: {row.get('Years')} سنوات</small>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("عرض التفاصيل", key=f"btn_{i}", use_container_width=True):
                        st.session_state.selected_item = row.to_dict(); st.session_state.page = 'details'; st.rerun()

        # أزرار التنقل
        if total_pages > 1:
            st.write("---")
            p1, p2, p3 = st.columns([1, 2, 1])
            if p3.button("التالي ⬅️") and st.session_state.current_page < total_pages:
                st.session_state.current_page += 1; st.rerun()
            p2.markdown(f'<p style="text-align:center;">صفحة {st.session_state.current_page} من {total_pages}</p>', unsafe_allow_html=True)
            if p1.button("➡️ السابق") and st.session_state.current_page > 1:
                st.session_state.current_page -= 1; st.rerun()

    with col_side:
        st.markdown('<div style="background:white; padding:20px; border-radius:15px; border:1px solid #e2e8f0; text-align:center;">'
                    f'<h5 style="color:#64748b; margin:0;">النتائج المطابقة</h5><h2 style="color:#003366;">{len(f_df)}</h2></div>', unsafe_allow_html=True)

# --- صفحة التفاصيل (بالزرين: معلومات ومشاريع) ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 عودة للبحث"): st.session_state.page = 'main'; st.rerun()
    
    st.markdown(f'<div style="background:white; padding:25px; border-radius:15px; border-right:10px solid #003366; margin-bottom:20px;">'
                f'<h1 style="color:#003366; margin:0;">{item.get("Developer")}</h1></div>', unsafe_allow_html=True)

    # الزرين المطلوبين بنظام التبويبات الشيك
    tab_info, tab_projs = st.tabs(["📝 معلومات المطور", "🏗️ مشاريع المطور"])
    
    with tab_info:
        st.markdown("### 📝 النبذة والزتونة الفنية")
        st.write(item.get('Detailed_Info', 'لا توجد بيانات حالية.'))
    
    with tab_projs:
        st.markdown(f"### 🏙️ كافة مشاريع {item.get('Developer')}")
        dev_projs = df[df['Developer'] == item.get('Developer')]
        for _, proj in dev_projs.iterrows():
            st.markdown(f"""
                <div style="background:white; padding:15px; border-radius:10px; border:1px solid #eee; margin-bottom:10px;">
                    <b>🏗️ مشروع في منطقة:</b> {proj.get('Area')}
                </div>
            """, unsafe_allow_html=True)
