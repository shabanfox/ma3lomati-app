import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة والستايل
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f0f2f5; 
    }

    /* خانة البحث */
    .stTextInput input {
        border: 3px solid #001a33 !important;
        border-radius: 10px !important;
        font-weight: 900 !important;
    }

    /* الكروت الرئيسية للمطورين */
    .main-card {
        background: #ffffff; border-radius: 15px; padding: 20px;
        border-right: 12px solid #001a33; margin-bottom: 10px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        min-height: 200px; display: flex; flex-direction: column; justify-content: center;
    }
    .dev-name { color: #000000 !important; font-size: 1.6rem; font-weight: 900; text-align: center; }
    .project-count { color: #059669 !important; font-size: 1.1rem; font-weight: 700; text-align: center; margin-top: 10px; }

    /* كروت الفرص ميكرو */
    .micro-card {
        background: #ffffff; border-radius: 8px; padding: 6px;
        border-right: 5px solid #d97706; margin-bottom: 5px;
    }

    /* الأزرار */
    .stButton>button { 
        background-color: #001a33 !important; color: #ffffff !important;
        width: 100%; font-weight: 900 !important; border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

def extract_num(text):
    if pd.isna(text): return 0
    res = re.findall(r'\d+', str(text).replace(',', ''))
    return int(res[0]) if res else 0

@st.cache_data
def get_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [c.strip() for c in df.columns]
        df['price_val'] = df.iloc[:, 4].apply(extract_num)
        df['down_val'] = df.iloc[:, 10].apply(extract_num)
        return df
    except: return None

df = get_data()

if df is not None:
    if 'page' not in st.session_state: st.session_state.page = 'main'
    if 'current_page' not in st.session_state: st.session_state.current_page = 0

    if st.session_state.page == 'main':
        st.markdown("<h1 style='text-align:center; color:#001a33; font-weight:900;'>🏠 دليل المطورين العقاريين</h1>", unsafe_allow_html=True)
        
        # البحث والفلاتر
        search_term = st.text_input("🔍 ابحث عن اسم المطور:", placeholder="اكتب اسم الشركة هنا...")
        
        # تجميع البيانات حسب اسم المطور
        # سنأخذ أول ظهور لكل مطور لعرضه في الكارت
        dev_group = df.groupby(df.iloc[:, 0]).first().reset_index()
        # إضافة عدد المشاريع لكل مطور
        dev_counts = df.iloc[:, 0].value_counts().to_dict()
        
        f_df = dev_group.copy()
        if search_term:
            f_df = f_df[f_df.iloc[:, 0].str.contains(search_term, na=False, case=False)]

        st.markdown("---")
        main_col, side_col = st.columns([3.2, 0.8])

        with main_col:
            items_per_page = 9
            total_pages = math.ceil(len(f_df) / items_per_page)
            start_idx = st.session_state.current_page * items_per_page
            current_items = f_df.iloc[start_idx : start_idx + items_per_page]

            for i in range(0, len(current_items), 3):
                row_cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_items):
                        row = current_items.iloc[i + j]
                        dev_name = row[0]
                        with row_cols[j]:
                            st.markdown(f"""
                                <div class="main-card">
                                    <div class="dev-name">🏢 {dev_name}</div>
                                    <div class="project-count">عدد المشاريع المتاحة: {dev_counts.get(dev_name, 0)}</div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"مشاريع {dev_name[:10]}", key=f"dev_{i+j}"):
                                st.session_state.selected_dev = dev_name
                                st.session_state.page = 'details'
                                st.rerun()

            # التنقل بين الصفحات
            st.markdown("---")
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            with nav1:
                if st.session_state.current_page > 0:
                    if st.button("⬅️ السابق"): st.session_state.current_page -= 1; st.rerun()
            with nav2: st.markdown(f"<p style='text-align:center; font-weight:900;'>صفحة {st.session_state.current_page+1} من {total_pages}</p>", unsafe_allow_html=True)
            with nav3:
                if st.session_state.current_page < total_pages - 1:
                    if st.button("التالي ➡️"): st.session_state.current_page += 1; st.rerun()

        with side_col:
            st.markdown("<h5 style='text-align:center; color:#ffffff; background:#d97706; padding:8px; border-radius:10px; font-weight:900;'>🔥 أهم 10 مشاريع</h5>", unsafe_allow_html=True)
            for idx, row in df.head(10).iterrows():
                st.markdown(f"""<div class="micro-card">
                    <div style="font-weight:900; font-size:0.85rem;">{row[2]}</div>
                    <div style="color:#059669; font-size:0.8rem; font-weight:700;">{row[4]}</div>
                </div>""", unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        dev_name = st.session_state.selected_dev
        dev_projects = df[df.iloc[:, 0] == dev_name]
        
        if st.button("⬅️ عودة للقائمة الرئيسية"): st.session_state.page = 'main'; st.rerun()
        
        st.markdown(f"<h1 style='color:#001a33; font-weight:900;'>🏢 {dev_name}</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.subheader(f"🏗️ مشاريع شركة {dev_name}:")
        
        # عرض كل مشروع من مشاريع المطور في "انفو" منفصل مع الزتونة الفنية بتاعته
        for idx, row in dev_projects.iterrows():
            with st.expander(f"📍 مشروع: {row[2]} - السعر: {row[4]}"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write(f"**الموقع:** {row[3]}")
                    st.write(f"**النوع:** {row[7]}")
                with col_b:
                    st.write(f"**المقدم:** {row[10]}")
                    st.write(f"**التقسيط:** {row[9]} سنوات")
                st.error(f"**💡 الزتونة الفنية للمشروع:** {row[11]}")
