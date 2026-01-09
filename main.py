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

    /* الكارت الرئيسي كزرار شفاف */
    .clickable-card {
        position: relative; background: #ffffff; border-radius: 12px; padding: 15px;
        border-right: 10px solid #001a33; box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        min-height: 220px; transition: 0.3s; display: flex; flex-direction: column; justify-content: space-between;
    }
    .clickable-card:hover { transform: translateY(-5px); border-right-color: #059669; }

    .stButton button {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: transparent !important; border: none !important; color: transparent !important;
        z-index: 10; cursor: pointer;
    }

    /* نصوص الكارت */
    .card-title { color: #000000; font-size: 1.3rem; font-weight: 900; }
    .card-price { color: #059669; font-size: 1.4rem; font-weight: 900; }

    /* كروت الـ 10 فرص (ميكرو) */
    .micro-card {
        background: white; border-radius: 8px; padding: 6px;
        border-right: 4px solid #d97706; margin-bottom: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
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
    df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
    df['price_val'] = df.iloc[:, 4].apply(extract_num)
    return df

df = get_data()

if 'page' not in st.session_state: st.session_state.page = 'main'
if 'current_page' not in st.session_state: st.session_state.current_page = 0

if st.session_state.page == 'main':
    st.markdown("<h1 style='text-align:center; font-weight:900;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
    search_q = st.text_input("🔍 ابحث عن مشروع أو مطور:")
    
    f_df = df.copy()
    if search_q:
        f_df = f_df[f_df.iloc[:, 0].str.contains(search_q, na=False, case=False) | f_df.iloc[:, 2].str.contains(search_q, na=False, case=False)]

    main_col, side_col = st.columns([3.2, 0.8])
    with main_col:
        items_per_page = 9
        total_pages = math.ceil(len(f_df) / items_per_page)
        current_items = f_df.iloc[st.session_state.current_page * items_per_page : (st.session_state.current_page + 1) * items_per_page]

        for i in range(0, len(current_items), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(current_items):
                    row = current_items.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"""<div class="clickable-card">
                            <div><div class="card-title">{row[2]}</div><div style="font-weight:700; color:#475569;">{row[0]}</div></div>
                            <div><div class="card-price">{row[4]}</div><div style="background:#001a33; color:white; padding:5px; border-radius:5px; text-align:center; font-weight:900; font-size:0.9rem;">مقدم {row[10]} | {row[9]}س</div></div>
                        </div>""", unsafe_allow_html=True)
                        if st.button("", key=f"b_{i+j}"):
                            st.session_state.selected_item = row.to_list(); st.session_state.page = 'details'; st.rerun()

        # أزرار التنقل
        n1, n2, n3 = st.columns([1, 2, 1])
        with n1: 
            if st.session_state.current_page > 0 and st.button("⬅️ السابق"): st.session_state.current_page -= 1; st.rerun()
        with n2: st.markdown(f"<p style='text-align:center; font-weight:900;'>صفحة {st.session_state.current_page+1}/{total_pages}</p>", unsafe_allow_html=True)
        with n3:
            if st.session_state.current_page < total_pages - 1 and st.button("التالي ➡️"): st.session_state.current_page += 1; st.rerun()

    with side_col:
        st.markdown("<h6 style='text-align:center; color:white; background:#d97706; padding:5px; border-radius:5px;'>🔥 أقوى 10 فرص</h6>", unsafe_allow_html=True)
        for idx, row in df.head(10).iterrows():
            st.markdown(f"""<div class="micro-card"><div style="font-weight:900; font-size:0.8rem;">{row[2]}</div><div style="color:#059669; font-size:0.75rem; font-weight:700;">{row[4]}</div></div>""", unsafe_allow_html=True)

elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 عودة"): st.session_state.page = 'main'; st.rerun()
    
    st.markdown(f"<div style='background:#001a33; color:white; padding:20px; border-radius:12px;'><h1>🏢 {item[0]}</h1><p>تعتبر شركة {item[0]} من كبار المطورين العقاريين الموثوقين.</p></div>", unsafe_allow_html=True)
    st.error(f"### 💡 الزتونة الفنية لـ {item[2]}:\n\n**{item[11]}**")
    
    st.markdown(f"### 🏗️ مشاريع أخرى لـ {item[0]}:")
    others = df[df.iloc[:, 0] == item[0]]
    for i in range(0, len(others), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(others):
                with cols[j]: st.info(f"**{others.iloc[i+j][2]}**\n\n💰 {others.iloc[i+j][4]}")
