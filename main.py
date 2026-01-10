import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
    }
    .main-header {
        background: #000; color: #f59e0b; padding: 15px; border-radius: 15px;
        text-align: center; margin-bottom: 20px; border: 2px solid #f59e0b;
    }
    .project-card {
        background-color: #f9f9f9; padding: 10px; border-radius: 8px;
        border-right: 4px solid #f59e0b; margin-bottom: 5px; font-weight: 700;
    }
    /* تنسيق أزرار التنقل */
    .stButton > button { width: 100%; border-radius: 10px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

df = load_data()

# إدارة حالة الصفحة في session_state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0

if not df.empty:
    proj_col = df.columns[0] 
    dev_col = df.columns[1]  
    loc_col = df.columns[2] if len(df.columns) > 2 else None

    st.markdown('<div class="main-header"><h1>🚀 منصة معلوماتى: دليل الشركات</h1></div>', unsafe_allow_html=True)

    tab_search, tab_tools = st.tabs(["🔍 دليل الشركات", "🛠️ أدوات البروكر"])

    with tab_search:
        col_side, col_main = st.columns([1, 3])

        with col_side:
            st.markdown("### ⚙️ تصفية")
            search_query = st.text_input("🔍 ابحث عن شركة أو مشروع")
            if loc_col:
                all_locs = ["كل المناطق"] + sorted(df[loc_col].dropna().unique().tolist())
                selected_loc = st.selectbox("📍 المنطقة", all_locs)
            else:
                selected_loc = "كل المناطق"

        with col_main:
            # الفلترة
            filtered_df = df.copy()
            if search_query:
                filtered_df = filtered_df[
                    filtered_df[dev_col].str.contains(search_query, na=False, case=False) |
                    filtered_df[proj_col].str.contains(search_query, na=False, case=False)
                ]
            if selected_loc != "كل المناطق" and loc_col:
                filtered_df = filtered_df[filtered_df[loc_col] == selected_loc]

            # الشركات الفريدة
            unique_devs = filtered_df[dev_col].dropna().unique()
            total_companies = len(unique_devs)
            
            # حسابات الصفحات (10 شركات لكل صفحة)
            items_per_page = 10
            total_pages = (total_companies // items_per_page) + (1 if total_companies % items_per_page > 0 else 0)
            
            # التأكد من أن الصفحة الحالية لا تتعدى الإجمالي بعد الفلترة
            if st.session_state.current_page >= total_pages:
                st.session_state.current_page = 0

            start_idx = st.session_state.current_page * items_per_page
            end_idx = start_idx + items_per_page
            current_list = unique_devs[start_idx:end_idx]

            st.success(f"✅ عرض {len(current_list)} من إجمالي {total_companies} شركة (صفحة {st.session_state.current_page + 1} من {total_pages})")

            # عرض الشركات
            for dev in current_list:
                with st.expander(f"🏢 المطور: {dev}"):
                    dev_projects = filtered_df[filtered_df[dev_col] == dev][proj_col].unique()
                    for p in dev_projects:
                        st.markdown(f'<div class="project-card">📍 مشروع: {p}</div>', unsafe_allow_html=True)

            # أزرار التنقل (السابق والتالي)
            st.write("---")
            nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
            
            with nav_col1:
                if st.button("⬅️ السابق") and st.session_state.current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()
            
            with nav_col3:
                if st.button("التالي ➡️") and st.session_state.current_page < total_pages - 1:
                    st.session_state.current_page += 1
                    st.rerun()

    with tab_tools:
        # تبويب الأدوات كما هو
        st.markdown("### 🛠️ الأدوات الحسابية")
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            price = st.number_input("سعر الوحدة", value=1000000)
            down = st.slider("المقدم (%)", 0, 50, 10)
            years = st.number_input("السنوات", 1, 15, 8)
            t_down = price * (down/100)
            monthly = (price - t_down) / (years * 12) if years > 0 else 0
            st.metric("المقدم", f"{t_down:,.0f}")
            st.metric("القسط", f"{monthly:,.0f}")
        with t_col2:
            buy = st.number_input("سعر الشراء", value=2000000)
            rent = st.number_input("الإيجار السنوي", value=160000)
            roi = (rent / buy) * 100 if buy > 0 else 0
            st.metric("ROI %", f"{roi:.2f} %")

