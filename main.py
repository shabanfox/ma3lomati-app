import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f0f2f5; 
    }

    .main-card {
        background: #ffffff; border-radius: 15px; padding: 25px;
        border-right: 12px solid #001a33; margin-bottom: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        min-height: 180px; display: flex; flex-direction: column; justify-content: center; align-items: center;
    }
    .dev-name { color: #001a33; font-size: 1.5rem; font-weight: 900; margin-bottom: 10px; }
    .project-count { background: #e0f2fe; color: #0369a1; padding: 4px 12px; border-radius: 20px; font-weight: 700; font-size: 0.9rem; }

    .stButton>button { 
        background-color: #001a33 !important; color: white !important;
        font-weight: 900 !important; border-radius: 10px; height: 45px; width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [c.strip() for c in df.columns]
        return df
    except: return None

df = get_data()

if df is not None:
    # تهيئة الحالة
    if 'page' not in st.session_state: st.session_state.page = 'main'
    if 'current_page' not in st.session_state: st.session_state.current_page = 0

    if st.session_state.page == 'main':
        st.markdown("<h1 style='text-align:center; color:#001a33; font-weight:900;'>🏠 دليل المطورين العقاريين</h1>", unsafe_allow_html=True)
        
        search_term = st.text_input("🔍 ابحث عن اسم المطور:", placeholder="اكتب اسم الشركة...")

        # معالجة البيانات: استخراج المطورين وعدد مشاريعهم
        dev_list = df.iloc[:, 0].value_counts().reset_index()
        dev_list.columns = ['developer', 'count']
        
        if search_term:
            dev_list = dev_list[dev_list['developer'].str.contains(search_term, na=False, case=False)]

        st.markdown("---")
        
        # التقسيم (3 كروت في الصف)
        items_per_page = 9
        total_pages = math.ceil(len(dev_list) / items_per_page)
        start_idx = st.session_state.current_page * items_per_page
        current_devs = dev_list.iloc[start_idx : start_idx + items_per_page]

        for i in range(0, len(current_devs), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(current_devs):
                    row = current_devs.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="main-card">
                                <div class="dev-name">🏢 {row['developer']}</div>
                                <div class="project-count">المشاريع المتاحة: {row['count']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"عرض مشاريع {row['developer'][:15]}", key=f"btn_{start_idx + i + j}"):
                            st.session_state.selected_dev = row['developer']
                            st.session_state.page = 'details'
                            st.rerun()

        # أزرار التنقل
        st.markdown("---")
        nav1, nav2, nav3 = st.columns([1, 2, 1])
        with nav1:
            if st.session_state.current_page > 0:
                if st.button("⬅️ السابق"): st.session_state.current_page -= 1; st.rerun()
        with nav2:
            st.markdown(f"<p style='text-align:center; font-weight:900;'>صفحة {st.session_state.current_page+1} من {total_pages}</p>", unsafe_allow_html=True)
        with nav3:
            if st.session_state.current_page < total_pages - 1:
                if st.button("التالي ➡️"): st.session_state.current_page += 1; st.rerun()

    elif st.session_state.page == 'details':
        dev_name = st.session_state.selected_dev
        projects = df[df.iloc[:, 0] == dev_name]
        
        if st.button("🔙 عودة للقائمة الرئيسية"):
            st.session_state.page = 'main'
            st.rerun()
            
        st.markdown(f"<div style='background:#001a33; color:white; padding:25px; border-radius:15px;'><h1>🏢 {dev_name}</h1></div>", unsafe_allow_html=True)
        
        st.markdown("### 🏗️ قائمة المشاريع والزتونة الفنية:")
        for _, row in projects.iterrows():
            with st.expander(f"📍 {row[2]} - السعر: {row[4]}"):
                st.write(f"**الموقع:** {row[3]}")
                st.write(f"**نظام السداد:** مقدم {row[10]} | تقسيط على {row[9]} سنوات")
                st.error(f"**💡 الزتونة الفنية:** {row[11]}")
