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
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f1f5f9; 
    }

    /* الكارت الجمالي */
    .card-container {
        position: relative; background: white; border-radius: 15px; padding: 20px;
        border-right: 12px solid #001a33; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        min-height: 250px; transition: 0.3s; display: flex; flex-direction: column; justify-content: space-between;
    }
    .card-container:hover { transform: translateY(-5px); border-right-color: #16a34a; }
    .card-title { color: #000000; font-size: 1.4rem; font-weight: 900; }
    .card-price { color: #166534; font-size: 1.6rem; font-weight: 900; margin: 10px 0; }
    
    /* الزر الشفاف */
    .stButton button {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: transparent !important; border: none !important; color: transparent !important;
        z-index: 10; cursor: pointer;
    }
    
    /* ستايل صفحة المطور */
    .dev-header { background: #001a33; color: white; padding: 30px; border-radius: 15px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

def extract_num(text):
    if pd.isna(text): return 0
    res = re.findall(r'\d+', str(text).replace(',', ''))
    return int(res[0]) if res else 0

@st.cache_data
def get_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    df = pd.read_csv(url)
    df.columns = [c.strip() for c in df.columns]
    df['p_val'] = df.iloc[:, 4].apply(extract_num)
    return df

df = get_data()

# إدارة التنقل بين الصفحات
if 'page' not in st.session_state: st.session_state.page = 'main'

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    st.markdown("<h1 style='text-align:center; color:#000000; font-weight:900;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
    search_term = st.text_input("🔍 ابحث عن مشروع أو مطور:", placeholder="مثال: SODIC...")
    
    f_df = df.copy()
    if search_term:
        f_df = f_df[f_df.iloc[:, 0].str.contains(search_term, na=False, case=False) | f_df.iloc[:, 2].str.contains(search_term, na=False, case=False)]

    main_col, side_col = st.columns([3.1, 0.9])
    with main_col:
        for i in range(0, len(f_df[:9]), 3):
            row_cols = st.columns(3)
            for j in range(3):
                if i + j < len(f_df):
                    row = f_df.iloc[i + j]
                    with row_cols[j]:
                        st.markdown(f"""
                            <div class="card-container">
                                <div>
                                    <div class="card-title">{row[2]}</div>
                                    <div style="color:#475569; font-weight:700;">🏢 {row[0]}</div>
                                    <div style="color:#64748b;">📍 {row[3]}</div>
                                </div>
                                <div>
                                    <div class="card-price">{row[4]}</div>
                                    <div style="background:#001a33; color:white; padding:8px; border-radius:8px; text-align:center; font-weight:900;">مقدم {row[10]}</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        if st.button("", key=f"btn_{i+j}"):
                            st.session_state.selected_item = row.to_list()
                            st.session_state.page = 'details'; st.rerun()

    with side_col:
        st.markdown("<h5 style='text-align:center; color:white; background:#b45309; padding:8px; border-radius:10px; font-weight:900;'>🔥 أقوى 10 فرص</h5>", unsafe_allow_html=True)
        for idx, row in df.head(10).iterrows():
            st.markdown(f"""<div style="background:white; padding:8px; border-right:4px solid #b45309; margin-bottom:5px; border-radius:5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <div style="font-weight:900; font-size:0.85rem;">{row[2]}</div>
                <div style="color:#166534; font-size:0.8rem; font-weight:700;">{row[4]}</div>
            </div>""", unsafe_allow_html=True)

# --- صفحة التفاصيل والمطور الجديدة ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item # بيانات المشروع المختار
    dev_name = item[0] # اسم المطور
    
    if st.button("🔙 العودة للقائمة الرئيسية"): st.session_state.page = 'main'; st.rerun()

    # 1. قسم المطور
    st.markdown(f"""
        <div class="dev-header">
            <h1 style="margin:0; font-weight:900;">🏢 {dev_name}</h1>
            <p style="font-size:1.2rem; opacity:0.9;">نبذة عن المطور: يعتبر {dev_name} من رواد التطوير العقاري في مصر، ويتميز بمشاريعه التي تلتزم بأعلى معايير الجودة والتسليم في المواعيد المحددة.</p>
        </div>
    """, unsafe_allow_html=True)

    # 2. الزتونة للمشروع الحالي
    st.error(f"### 💡 الزتونة الفنية لـ {item[2]}:\n\n**{item[11]}**")
    
    # 3. مشاريع الشركة الأخرى
    st.markdown(f"### 🏗️ جميع مشاريع شركة {dev_name}:")
    dev_projects = df[df.iloc[:, 0] == dev_name] # فلترة المشاريع لهذا المطور فقط
    
    for i in range(0, len(dev_projects), 4):
        p_cols = st.columns(4)
        for j in range(4):
            if i + j < len(dev_projects):
                p_row = dev_projects.iloc[i + j]
                with p_cols[j]:
                    st.success(f"**{p_row[2]}**\n\n📍 {p_row[3]}\n\n💰 {p_row[4]}")
