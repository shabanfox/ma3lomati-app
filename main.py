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

    /* حاوية الكارت لضبط العناصر فوق بعضها */
    .card-wrapper {
        position: relative;
        height: 280px;
        margin-bottom: 20px;
    }

    /* تصميم الكارت الجمالي (ده للعرض فقط) */
    .card-visual {
        background: white;
        border-radius: 15px;
        padding: 20px;
        border-right: 12px solid #001a33;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        pointer-events: none; /* عشان الضغطة تعدي من خلاله للزرار */
    }

    .card-title { color: #000000; font-size: 1.4rem; font-weight: 900; }
    .card-dev { color: #475569; font-size: 1.1rem; font-weight: 700; margin-top:5px; }
    .card-price { color: #166534; font-size: 1.6rem; font-weight: 900; }
    .card-badge { background: #001a33; color: white; padding: 8px; border-radius: 8px; text-align: center; font-weight: 900; }

    /* الزرار الشفاف اللي فوق الكارت (ده اللي بيستلم الضغطة) */
    .stButton > button {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        background: transparent !important;
        color: transparent !important;
        border: none !important;
        z-index: 999 !important; /* التأكد إنه فوق كل حاجة */
        cursor: pointer !important;
    }
    
    .stButton > button:hover {
        background: rgba(0,0,0,0.02) !important; /* ظل خفيف جداً عند الوقوف */
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        return df
    except: return None

df = get_data()

if 'page' not in st.session_state: st.session_state.page = 'main'

if st.session_state.page == 'main':
    st.markdown("<h1 style='text-align:center; font-weight:900;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
    
    search = st.text_input("🔍 ابحث عن مشروع أو مطور:")
    f_df = df.copy()
    if search:
        f_df = f_df[f_df.iloc[:, 0].str.contains(search, na=False, case=False) | f_df.iloc[:, 2].str.contains(search, na=False, case=False)]

    main_col, side_col = st.columns([3.2, 0.8])
    with main_col:
        for i in range(0, len(f_df[:9]), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(f_df):
                    row = f_df.iloc[i + j]
                    with cols[j]:
                        # 1. بنرسم الشكل الجمالي الأول
                        st.markdown(f"""
                        <div class="card-wrapper">
                            <div class="card-visual">
                                <div>
                                    <div class="card-title">{row[2]}</div>
                                    <div class="card-dev">🏢 {row[0]}</div>
                                    <div style="color:#64748b;">📍 {row[3]}</div>
                                </div>
                                <div>
                                    <div class="card-price">{row[4]}</div>
                                    <div class="card-badge">مقدم {row[10]} | {row[9]}س</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # 2. بنحط الزرار الشفاف فوقه تماماً (في نفس الـ wrapper)
                        if st.button("", key=f"btn_{i+j}"):
                            st.session_state.selected_item = row.to_list()
                            st.session_state.page = 'details'
                            st.rerun()
                        
                        st.markdown("</div>", unsafe_allow_html=True)

    with side_col:
        st.markdown("<h5 style='text-align:center; color:white; background:#b45309; padding:8px; border-radius:10px;'>🔥 أهم الفرص</h5>", unsafe_allow_html=True)
        for _, r in df.head(10).iterrows():
            st.markdown(f"<div style='background:white; padding:8px; border-right:4px solid #b45309; margin-bottom:5px; border-radius:5px;'><b>{r[2]}</b><br><small style='color:green;'>{r[4]}</small></div>", unsafe_allow_html=True)

elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 عودة"): st.session_state.page = 'main'; st.rerun()
    st.markdown(f"<div style='background:#001a33; color:white; padding:30px; border-radius:15px;'><h1>🏢 {item[0]}</h1><p>نبذة عن المطور ومشاريع الشركة.</p></div>", unsafe_allow_html=True)
    st.error(f"### 💡 الزتونة الفنية لـ {item[2]}:\n\n**{item[11]}**")
    # عرض مشاريع المطور الأخرى
    others = df[df.iloc[:, 0] == item[0]]
    st.markdown(f"### 🏗️ مشاريع أخرى لشركة {item[0]}:")
    for _, p in others.iterrows(): st.info(f"**{p[2]}** | {p[4]}")
