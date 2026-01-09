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
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f4f7f9; 
    }

    /* تحويل زر Streamlit لكارت فخم */
    div.stButton > button {
        display: block !important;
        width: 100% !important;
        min-height: 260px !important;
        background: white !important;
        border: none !important;
        border-right: 12px solid #001a33 !important; /* الهوية البصرية الكحلية */
        border-radius: 15px !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08) !important;
        padding: 25px !important;
        transition: all 0.4s ease !important;
        text-align: right !important;
        line-height: 1.6 !important;
    }

    div.stButton > button:hover {
        transform: translateY(-8px) !important;
        border-right-color: #16a34a !important; /* أخضر عند التفاعل */
        box-shadow: 0 20px 40px rgba(0,0,0,0.12) !important;
    }

    /* تحسين شكل المدخلات */
    .stTextInput input {
        border: 2px solid #001a33 !important;
        border-radius: 12px !important;
        padding: 10px !important;
        font-weight: 700 !important;
    }

    /* كروت الفرص الجانبية */
    .side-card {
        background: white; padding: 12px; border-radius: 10px;
        border-right: 5px solid #e67e22; margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
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
    if 'page' not in st.session_state: st.session_state.page = 'main'

    if st.session_state.page == 'main':
        st.markdown("<h1 style='text-align:center; color:#001a33; font-weight:900; margin-bottom:30px;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        
        search = st.text_input("🔍 ابحث عن حلمك العقاري (اسم المشروع أو الشركة)...")
        
        f_df = df.copy()
        if search:
            f_df = f_df[f_df.iloc[:, 0].str.contains(search, na=False, case=False) | f_df.iloc[:, 2].str.contains(search, na=False, case=False)]

        st.markdown("<br>", unsafe_allow_html=True)
        m_col, s_col = st.columns([3.3, 0.7])

        with m_col:
            for i in range(0, len(f_df[:9]), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(f_df):
                        row = f_df.iloc[i + j]
                        
                        # تنسيق النصوص داخل الكارت-الزرار
                        # استخدمنا رموز الـ Emoji والـ New Lines لتنسيق الشكل
                        card_content = (
                            f"📌 {row[2]}\n"          # اسم المشروع
                            f"🏢 {row[0]}\n"          # المطور
                            f"📍 {row[3]}\n\n"        # الموقع
                            f"💰 {row[4]}\n"          # السعر
                            f"💳 مقدم {row[10]} | {row[9]}س" # المقدم والتقسيط
                        )
                        
                        with cols[j]:
                            if st.button(card_content, key=f"p_{i+j}"):
                                st.session_state.selected_item = row.to_list()
                                st.session_state.page = 'details'
                                st.rerun()

        with s_col:
            st.markdown("<h5 style='text-align:center; color:#001a33; font-weight:900;'>🔥 فرص ذهبية</h5>", unsafe_allow_html=True)
            for _, row in df.head(10).iterrows():
                st.markdown(f"""<div class="side-card">
                    <div style="font-weight:900; font-size:0.9rem; color:#333;">{row[2]}</div>
                    <div style="color:#16a34a; font-weight:700; font-size:0.8rem;">{row[4]}</div>
                </div>""", unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        if st.button("🔙 العودة للرئيسية"): st.session_state.page = 'main'; st.rerun()
        
        # هيدر صفحة المطور
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #001a33 0%, #003366 100%); color:white; padding:40px; border-radius:20px; text-align:center; box-shadow: 0 10px 20px rgba(0,0,0,0.2);">
                <h1 style="margin:0; font-size:2.5rem;">🏢 {item[0]}</h1>
                <p style="font-size:1.2rem; opacity:0.9; margin-top:15px;">نحن نختار لك أفضل المطورين لضمان استثمارك العقاري.</p>
            </div>
        """, unsafe_allow_html=True)

        st.warning(f"### 🎯 الزتونة الفنية للمشروع:\n{item[11]}")
        
        # مشاريع الشركة التانية
        st.markdown(f"### 🏗️ المزيد من أعمال شركة {item[0]}:")
        others = df[df.iloc[:, 0] == item[0]]
        for _, p in others.iterrows():
            st.success(f"🏠 **{p[2]}** | 💰 السعر: {p[4]} | 📍 الموقع: {p[3]}")
