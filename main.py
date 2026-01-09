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
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }

    /* تصميم الكارت */
    .project-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        min-height: 280px;
        display: flex;
        flex-direction: column;
        position: relative;
    }

    /* ستايل زر التفاصيل الأزرق */
    .stButton > button {
        background-color: #1d4ed8 !important; /* لون أزرق صريح */
        color: white !important;
        border-radius: 10px !important;
        font-weight: 900 !important;
        width: 100% !important;
        border: none !important;
        margin-bottom: 15px !important; /* عشان يكون فوق البيانات */
        height: 45px !important;
    }
    
    .stButton > button:hover {
        background-color: #1e40af !important;
        box-shadow: 0 5px 15px rgba(29, 78, 216, 0.3) !important;
    }

    /* تنسيق النصوص */
    .title-text { color: #000; font-size: 1.3rem; font-weight: 900; margin-bottom: 5px; }
    .dev-text { color: #475569; font-size: 1rem; font-weight: 700; }
    .price-text { color: #15803d; font-size: 1.4rem; font-weight: 900; margin: 10px 0; }
    .badge-info { background: #f1f5f9; padding: 5px 10px; border-radius: 8px; font-size: 0.9rem; font-weight: 700; color: #1e293b; border: 1px solid #e2e8f0; }
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

if 'page' not in st.session_state: st.session_state.page = 'main'

if st.session_state.page == 'main':
    st.markdown("<h1 style='text-align:center; font-weight:900; color:#1e3a8a;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
    
    search = st.text_input("🔍 ابحث عن مشروع أو مطور:", placeholder="اكتب هنا للبحث...")
    f_df = df.copy()
    if search:
        f_df = f_df[f_df.iloc[:, 0].str.contains(search, na=False, case=False) | f_df.iloc[:, 2].str.contains(search, na=False, case=False)]

    st.markdown("---")
    
    # شبكة العرض: 3 صفوف × 3 أعمدة = 9 كروت
    display_df = f_df.head(9) 
    
    for i in range(0, len(display_df), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(display_df):
                row = display_df.iloc[i + j]
                with cols[j]:
                    with st.container():
                        # حاوية الكارت
                        st.markdown(f"""
                        <div class="project-card">
                        """, unsafe_allow_html=True)
                        
                        # الزر الأزرق في الأعلى
                        if st.button(f"📄 تفاصيل {row[2][:15]}", key=f"btn_{i+j}"):
                            st.session_state.selected_item = row.to_list()
                            st.session_state.page = 'details'
                            st.rerun()
                        
                        # بيانات الكارت تحت الزر
                        st.markdown(f"""
                            <div class="title-text">{row[2]}</div>
                            <div class="dev-text">🏢 {row[0]}</div>
                            <div style="color:#64748b; font-size:0.9rem;">📍 {row[3]}</div>
                            <div class="price-text">{row[4]}</div>
                            <div class="badge-info">💵 مقدم: {row[10]} | 🗓️ {row[9]}س</div>
                        </div>
                        """, unsafe_allow_html=True)

elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 العودة للقائمة الرئيسية"): st.session_state.page = 'main'; st.rerun()
    
    # صفحة المطور
    st.markdown(f"""
        <div style="background:#1e3a8a; color:white; padding:30px; border-radius:15px; margin-bottom:20px;">
            <h1 style="margin:0;">🏢 {item[0]}</h1>
            <p style="font-size:1.2rem; margin-top:10px;">نبذة عن المطور ومشاريع الشركة العقارية.</p>
        </div>
    """, unsafe_allow_html=True)

    st.error(f"### 💡 الزتونة الفنية لـ {item[2]}:\n\n**{item[11]}**")
    
    # مشاريع الشركة الأخرى
    st.markdown(f"### 🏗️ مشاريع أخرى لشركة {item[0]}:")
    others = df[df.iloc[:, 0] == item[0]]
    for _, p in others.iterrows():
        st.info(f"🏠 **{p[2]}** | 💰 {p[4]} | 📍 {p[3]}")
