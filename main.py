import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الزوائد */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }

    /* تحويل زر Streamlit لكارت جمالي بالكامل */
    div.stButton > button {
        display: block !important;
        width: 100% !important;
        min-height: 250px !important;
        background-color: white !important;
        border-right: 12px solid #001a33 !important; /* اللون الكحلي اللي كان عاجبك */
        border-top: none !important; border-left: none !important; border-bottom: none !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
        padding: 20px !important;
        transition: 0.3s !important;
        text-align: right !important;
        color: black !important;
    }

    div.stButton > button:hover {
        transform: translateY(-5px) !important;
        border-right-color: #16a34a !important; /* يقلب أخضر عند الوقوف عليه */
        box-shadow: 0 15px 30px rgba(0,0,0,0.15) !important;
    }

    /* تنسيق النصوص داخل الزرار (باستخدام الماركداون) */
    .btn-title { font-size: 1.4rem; font-weight: 900; color: #000; display: block; margin-bottom: 5px; }
    .btn-dev { font-size: 1.1rem; font-weight: 700; color: #475569; display: block; }
    .btn-loc { font-size: 1rem; color: #64748b; display: block; margin-bottom: 10px; }
    .btn-price { font-size: 1.6rem; font-weight: 900; color: #166534; display: block; margin: 10px 0; }
    .btn-badge { background: #001a33; color: white; padding: 5px 10px; border-radius: 8px; font-weight: 700; font-size: 0.9rem; }
    
    /* البحث */
    .stTextInput input { border: 3px solid #000 !important; border-radius: 10px !important; }
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
    if 'page' not in st.session_state: st.session_state.page = 'main'

    if st.session_state.page == 'main':
        st.markdown("<h1 style='text-align:center; font-weight:900;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث عن مشروع أو مطور:")
        
        f_df = df.copy()
        if search:
            f_df = f_df[f_df.iloc[:, 0].str.contains(search, na=False, case=False) | f_df.iloc[:, 2].str.contains(search, na=False, case=False)]

        st.markdown("---")
        m_col, s_col = st.columns([3.2, 0.8])

        with m_col:
            # عرض الكروت (كل كارت هو زرار فعلي)
            for i in range(0, len(f_df[:9]), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(f_df):
                        row = f_df.iloc[i + j]
                        # محتوى الزرار بتنسيق الـ CSS اللي فوق
                        label = f"""
                        {row[2]}
                        🏢 {row[0]}
                        📍 {row[3]}
                        💰 {row[4]}
                        مقدم {row[10]} | {row[9]} سنوات
                        """
                        with cols[j]:
                            # الزرار هنا بياخد الـ label كأنه نص، والـ CSS بيقوم بالباقي
                            if st.button(label, key=f"btn_{i+j}"):
                                st.session_state.selected_item = row.to_list()
                                st.session_state.page = 'details'
                                st.rerun()

        with s_col:
            st.markdown("<h5 style='background:#b45309; color:white; padding:8px; border-radius:8px; text-align:center;'>🔥 أهم الفرص</h5>", unsafe_allow_html=True)
            for idx, row in df.head(10).iterrows():
                st.markdown(f"""<div style="background:white; padding:8px; border-right:4px solid #b45309; border-radius:5px; margin-bottom:5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <div style="font-weight:900; font-size:0.85rem;">{row[2]}</div>
                    <div style="color:#166534; font-weight:700; font-size:0.8rem;">{row[4]}</div>
                </div>""", unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        if st.button("🔙 العودة"): st.session_state.page = 'main'; st.rerun()
        
        st.markdown(f"<div style='background:#001a33; color:white; padding:30px; border-radius:15px;'><h1>🏢 {item[0]}</h1><p>شركة مطورة رائدة في السوق المصري.</p></div>", unsafe_allow_html=True)
        st.error(f"### 💡 الزتونة الفنية لـ {item[2]}:\n\n**{item[11]}**")
        
        # عرض مشاريع المطور التانية
        st.markdown(f"### 🏗️ مشاريع تابعة لشركة {item[0]}:")
        others = df[df.iloc[:, 0] == item[0]]
        for _, p in others.iterrows():
            st.info(f"**{p[2]}** | 📍 {p[3]} | 💰 {p[4]}")
