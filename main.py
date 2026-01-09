import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - الأزرار الزرقاء والنصوص الغامقة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f4f7f9; 
    }

    .dark-bold-text {
        color: #001a33 !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        margin-bottom: 10px;
    }

    .small-grid-card {
        background: white; border-radius: 10px; padding: 12px;
        height: 110px; display: flex; flex-direction: column;
        justify-content: center; border: 1px solid #e2e8f0;
        border-right: 5px solid #0044ff; margin-bottom: 5px;
    }

    div.stButton > button {
        background-color: #0044ff !important; 
        color: white !important; 
        border-radius: 8px !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: bold !important;
        height: 35px; width: 100%;
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

# 4. إدارة الحالة الديناميكية (Dynamic State)
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'current_page_num' not in st.session_state: st.session_state.current_page_num = 1
if 'search_query' not in st.session_state: st.session_state.search_query = ""
if 'selected_area' not in st.session_state: st.session_state.selected_area = "الكل"

# وظائف التحديث اللحظي
def reset_pagination():
    st.session_state.current_page_num = 1

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    st.markdown('<h1 style="color:#001a33; font-weight:900;">منصة معلوماتى العقارية</h1>', unsafe_allow_html=True)

    if df is not None:
        col_right, col_left = st.columns([1.8, 1])

        with col_right:
            # الفلاتر الديناميكية
            st.markdown('<div style="background:white; padding:15px; border-radius:12px; border:1px solid #e2e8f0; margin-bottom:15px;">', unsafe_allow_html=True)
            f_c1, f_c2 = st.columns([2, 1])
            with f_c1:
                # البحث ديناميكي بمجرد الكتابة
                st.session_state.search_query = st.text_input(
                    "🔍 ابحث لحظياً عن مطور أو ميزة...", 
                    value=st.session_state.search_query,
                    on_change=reset_pagination
                )
            with f_c2:
                areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
                st.session_state.selected_area = st.selectbox(
                    "المنطقة", 
                    areas, 
                    index=areas.index(st.session_state.selected_area),
                    on_change=reset_pagination
                )
            st.markdown('</div>', unsafe_allow_html=True)

            # تطبيق الفلترة اللحظية
            f_df = df.copy()
            if st.session_state.selected_area != "الكل":
                f_df = f_df[f_df['Area'] == st.session_state.selected_area]
            
            if st.session_state.search_query:
                q = st.session_state.search_query.lower()
                f_df = f_df[
                    f_df['Developer'].astype(str).str.lower().str.contains(q, na=False) |
                    f_df.get('Detailed_Info', '').astype(str).str.lower().str.contains(q, na=False)
                ]

            # نظام عرض 6 كروت
            items_per_page = 6 
            total_pages = math.ceil(len(f_df) / items_per_page)
            start_idx = (st.session_state.current_page_num - 1) * items_per_page
            page_items = f_df.iloc[start_idx : start_idx + items_per_page]

            # الشبكة الديناميكية
            grid_cols = st.columns(2)
            for idx, (i, row) in enumerate(page_items.reset_index().iterrows()):
                with grid_cols[idx % 2]:
                    st.markdown(f"""
                        <div class="small-grid-card">
                            <div style="color:#001a33; font-weight:900; font-size:1.1rem;">{row.get('Developer')}</div>
                            <div style="color:#475569; font-weight:bold;">📍 {row.get('Area')}</div>
                            <div style="color:#0044ff; font-size:0.85rem; font-weight:bold;">💰 {row.get('Price', '')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("👁️ تفاصيل البروفايل", key=f"btn_{i}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'; st.rerun()

            # التنقل بين الصفحات
            if total_pages > 1:
                st.markdown(f'<p class="dark-bold-text" style="text-align:center;">صفحة {st.session_state.current_page_num} من {total_pages}</p>', unsafe_allow_html=True)
                p_c1, p_c2, p_c3, p_c4 = st.columns([1,1,1,1])
                if p_c2.button("السابق") and st.session_state.current_page_num > 1:
                    st.session_state.current_page_num -= 1; st.rerun()
                if p_c3.button("التالي") and st.session_state.current_page_num < total_pages:
                    st.session_state.current_page_num += 1; st.rerun()

        with col_left:
            # عداد ديناميكي يتحدث مع البحث
            st.markdown(f"""
                <div class="stat-card">
                    <p class="dark-bold-text">النتائج المطابقة الآن</p>
                    <h1 style="color:#0044ff; margin:0; font-size:3.5rem;">{len(f_df)}</h1>
                </div>
            """, unsafe_allow_html=True)

            # أزرار الـ Top 10 (فلترة سريعة ديناميكية)
            st.markdown('<div class="stat-card" style="text-align:right;"><p class="dark-bold-text">🏆 اختصار المطورين الكبار</p>', unsafe_allow_html=True)
            top_10_list = ["Mountain View", "SODIC", "Emaar", "TMG", "Ora Developers", "Palm Hills", "Tatweer Misr", "Misr Italia", "Orascom", "Hassan Allam"]
            for company in top_10_list:
                if st.button(f"🏢 {company}", key=f"top_{company}"):
                    st.session_state.search_query = company
                    st.session_state.selected_area = "الكل"
                    st.session_state.current_page_num = 1
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التفاصيل ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("⬅️ عودة للقائمة الرئيسية"): st.session_state.page = 'main'; st.rerun()
    st.markdown(f"""
        <div style="background:#001a33; padding:40px; border-radius:15px; color:white; text-align:center; margin-bottom:25px;">
            <h1 style="color:white !important; margin:0;">{item.get('Developer')}</h1>
            <p style="font-size:1.2rem; opacity:0.9;">نظرة شاملة ومفصلة</p>
        </div>
        <div class="stat-card" style="text-align:right; border-right:10px solid #0044ff;">
            <p class="dark-bold-text">📖 نبذة المطور والزتونة الفنية</p>
            <p style="color:#1e293b; font-size:1.2rem; line-height:1.8; font-weight:bold;">
                {item.get('Company_Bio', 'المعلومات سيتم تحديثها قريباً من قبل فريق العمل.')}
            </p>
        </div>
    """, unsafe_allow_html=True)
