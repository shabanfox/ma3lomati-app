import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - النسخة المستقرة
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

    /* الهيدر: العنوان يمين والأزرار يسار */
    .header-wrapper {
        display: flex; justify-content: space-between; align-items: center;
        background: white; padding: 15px 30px; border-radius: 15px;
        box-shadow: 0 2px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
    }

    .right-side { color: #003366; font-weight: 900; font-size: 1.8rem; margin: 0; }

    /* مربع البحث المتطور */
    .advanced-search-box {
        background: white; padding: 20px; border-radius: 15px;
        border: 1px solid #e2e8f0; margin-bottom: 20px;
    }

    /* الكروت */
    .small-grid-card {
        background: white; border-radius: 12px; padding: 15px;
        height: 110px; display: flex; flex-direction: column;
        justify-content: center; border: 1px solid #e2e8f0;
        border-right: 5px solid #003366; margin-bottom: 8px;
    }

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

# 4. إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'search_query' not in st.session_state: st.session_state.search_query = ""
if 'current_page' not in st.session_state: st.session_state.current_page = 1

def reset_page(): st.session_state.current_page = 1

# --- الهيدر الثابت ---
st.markdown(f"""
    <div class="header-wrapper">
        <div class="right-side">منصة معلوماتى العقارية</div>
    </div>
""", unsafe_allow_html=True)

# أزرار التنقل السريع في اليسار
h_col1, h_col2, h_col3 = st.columns([1, 1, 4])
with h_col1:
    if st.button("🏠 الرئيسية"):
        st.session_state.page = 'main'; st.session_state.search_query = ""; reset_page(); st.rerun()
with h_col2:
    if st.button("👤 دخول"): st.toast("قريباً")

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main' and df is not None:
    
    # مربع البحث المتطور
    st.markdown('<div class="advanced-search-box">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        s_name = st.text_input("🔍 اسم المطور", value=st.session_state.search_query, on_change=reset_page)
        st.session_state.search_query = s_name
    with c2:
        areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
        s_area = st.selectbox("📍 المنطقة", areas, on_change=reset_page)
    with c3:
        s_years = st.selectbox("⏳ سنوات القسط", ["الكل", "3 سنوات", "5 سنوات", "7 سنوات", "10 سنوات"], on_change=reset_page)
    st.markdown('</div>', unsafe_allow_html=True)

    # تطبيق الفلترة
    f_df = df.copy()
    if st.session_state.search_query:
        f_df = f_df[f_df['Developer'].astype(str).str.contains(st.session_state.search_query, case=False, na=False)]
    if s_area != "الكل":
        f_df = f_df[f_df['Area'] == s_area]

    # تقسيم الصفحة (كروت / أقوى المطورين)
    col_main, col_side = st.columns([2, 1])

    with col_main:
        items_per_page = 6  # 3 صفوف (كل صف 2 كرت)
        total_pages = math.ceil(len(f_df) / items_per_page)
        start_idx = (st.session_state.current_page - 1) * items_per_page
        page_items = f_df.iloc[start_idx : start_idx + items_per_page]

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
        
        # أزرار ترقيم الصفحات
        if total_pages > 1:
            st.write("---")
            p1, p2, p3 = st.columns([1, 2, 1])
            if p3.button("التالي ⬅️") and st.session_state.current_page < total_pages:
                st.session_state.current_page += 1; st.rerun()
            p2.markdown(f'<p style="text-align:center;">صفحة {st.session_state.current_page} من {total_pages}</p>', unsafe_allow_html=True)
            if p1.button("➡️ السابق") and st.session_state.current_page > 1:
                st.session_state.current_page -= 1; st.rerun()

    with col_side:
        st.markdown('<div style="background:white; padding:20px; border-radius:15px; border:1px solid #e2e8f0;">'
                    '<div style="color:#003366; font-weight:900; border-bottom:3px solid #D4AF37; padding-bottom:5px; margin-bottom:15px;">🏆 أقوى المطورين</div>', unsafe_allow_html=True)
        for comp in ["Mountain View", "SODIC", "Emaar", "TMG", "Palm Hills"]:
            if st.button(f"🏢 {comp}", key=f"side_{comp}", use_container_width=True):
                st.session_state.search_query = comp; reset_page(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التفاصيل (التعديل المطلوب) ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    
    if st.button("🔙 عودة للرئيسية"): st.session_state.page = 'main'; st.rerun()

    st.markdown(f'<div style="background:white; padding:20px; border-radius:15px; border-right:10px solid #003366; margin:20px 0;">'
                f'<h1 style="margin:0; color:#003366;">{item.get("Developer")}</h1></div>', unsafe_allow_html=True)

    # الزرين اللي طلبتهم (استخدمت نظام Tabs لأنه أشيك وأسرع)
    tab_info, tab_projects = st.tabs(["📝 معلومات المطور", "🏗️ مشاريع المطور"])

    with tab_info:
        st.markdown("### النبذة الفنية (الزتونة)")
        st.write(item.get('Detailed_Info', 'المعلومات ستتوفر قريباً.'))

    with tab_projects:
        st.markdown(f"### كافة مشاريع {item.get('Developer')}")
        # فلترة تلقائية لعرض مشاريع هذا المطور من الجدول
        dev_projs = df[df['Developer'] == item.get('Developer')]
        for _, p in dev_projs.iterrows():
            st.markdown(f"""
                <div style="background:white; padding:15px; border-radius:10px; border:1px solid #eee; margin-bottom:10px;">
                    <b>🏗️ مشروع في منطقة:</b> {p.get('Area')}
                </div>
            """, unsafe_allow_html=True)
