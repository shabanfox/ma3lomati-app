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

    /* حاوية الكارت النسبية */
    .card-wrapper {
        position: relative;
        margin-bottom: 20px;
    }

    /* تصميم الكارت الجمالي */
    .card-design {
        background: white;
        border-radius: 15px;
        padding: 20px;
        border-right: 12px solid #001a33;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        min-height: 250px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        pointer-events: none; /* جعل التصميم لا يعيق الضغط على الزر خلفه */
    }

    .card-title { color: #000000 !important; font-size: 1.4rem; font-weight: 900; }
    .card-price { color: #166534 !important; font-size: 1.6rem; font-weight: 900; }
    .card-badge { background: #001a33; color: white; padding: 8px; border-radius: 8px; text-align: center; font-weight: 900; }

    /* الزر الشفاف الذي يغطي المساحة بالكامل ويكون فوق التصميم */
    div.stButton > button {
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        background: transparent !important;
        color: transparent !important;
        border: none !important;
        z-index: 100 !important; /* التأكد أنه في المقدمة تماماً */
        cursor: pointer !important;
    }
    
    /* تأثير عند تمرير الماوس على الزر يظهر على الكارت */
    .card-wrapper:hover .card-design {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        border-right-color: #16a34a;
        transition: 0.3s;
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
        df['p_val'] = df.iloc[:, 4].apply(extract_num)
        return df
    except: return None

df = get_data()

if df is not None:
    if 'page' not in st.session_state: st.session_state.page = 'main'
    
    if st.session_state.page == 'main':
        st.markdown("<h1 style='text-align:center; color:#000000; font-weight:900;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        search_term = st.text_input("🔍 ابحث هنا...", placeholder="مشروع أو مطور")
        
        f_df = df.copy()
        if search_term:
            f_df = f_df[f_df.iloc[:, 0].str.contains(search_term, na=False, case=False) | f_df.iloc[:, 2].str.contains(search_term, na=False, case=False)]

        st.markdown("---")
        main_col, side_col = st.columns([3.2, 0.8])

        with main_col:
            for i in range(0, len(f_df[:9]), 3):
                row_cols = st.columns(3)
                for j in range(3):
                    if i + j < len(f_df):
                        row = f_df.iloc[i + j]
                        with row_cols[j]:
                            # استخدام container لضمان ترتيب العناصر
                            st.markdown(f"""
                                <div class="card-wrapper">
                                    <div class="card-design">
                                        <div>
                                            <div class="card-title">{row[2]}</div>
                                            <div style="color:#475569; font-weight:700;">🏢 {row[0]}</div>
                                            <div style="color:#64748b;">📍 {row[3]}</div>
                                        </div>
                                        <div>
                                            <div class="card-price">{row[4]}</div>
                                            <div class="card-badge">مقدم {row[10]} | {row[9]}س</div>
                                        </div>
                                    </div>
                            """, unsafe_allow_html=True)
                            
                            # الزر الشفاف يوضع هنا (داخل الـ card-wrapper)
                            if st.button("", key=f"btn_{i+j}"):
                                st.session_state.selected_item = row.to_list()
                                st.session_state.page = 'details'
                                st.rerun()
                                
                            st.markdown("</div>", unsafe_allow_html=True) # إغلاق الـ card-wrapper

        with side_col:
            st.markdown("<h5 style='text-align:center; color:white; background:#b45309; padding:8px; border-radius:10px;'>🔥 أقوى الفرص</h5>", unsafe_allow_html=True)
            for idx, row in df.head(10).iterrows():
                st.markdown(f"<div style='background:white; padding:8px; border-right:4px solid #b45309; margin-bottom:5px; border-radius:5px;'><b>{row[2]}</b><br><small style='color:green;'>{row[4]}</small></div>", unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        if st.button("🔙 العودة"): st.session_state.page = 'main'; st.rerun()
        
        st.markdown(f"<div style='background:#001a33; color:white; padding:25px; border-radius:15px;'><h1>🏢 {item[0]}</h1><p>نبذة عن المطور ومصداقيته في السوق.</p></div>", unsafe_allow_html=True)
        st.error(f"### 💡 الزتونة الفنية:\n\n**{item[11]}**")
        
        st.markdown(f"### 🏗️ مشاريع أخرى لشركة {item[0]}:")
        others = df[df.iloc[:, 0] == item[0]]
        for idx, p in others.iterrows():
            st.info(f"**{p[2]}** - 📍 {p[3]} - 💰 {p[4]}")
