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
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }

    /* تصميم الكارت الجمالي */
    .card-container {
        position: relative;
        background: white;
        border-radius: 15px;
        padding: 20px;
        border-right: 12px solid #001a33;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        min-height: 250px;
        transition: 0.3s;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .card-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        border-right-color: #16a34a;
    }

    .card-title { color: #000000; font-size: 1.4rem; font-weight: 900; margin-bottom: 5px; }
    .card-dev { color: #475569; font-size: 1.1rem; font-weight: 700; }
    .card-loc { color: #64748b; font-size: 1rem; font-weight: 600; margin-bottom: 10px; }
    .card-price { color: #166534; font-size: 1.6rem; font-weight: 900; margin: 10px 0; }
    .card-badge { 
        background: #001a33; color: white; padding: 8px; 
        border-radius: 8px; text-align: center; font-weight: 900; font-size: 1rem;
    }

    /* جعل زرار Streamlit شفاف ويغطي الكارت بالكامل */
    .stButton button {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        z-index: 10;
        cursor: pointer;
    }
    
    .stButton button:hover { background: transparent !important; border: none !important; }

    /* البحث */
    .stTextInput input { border: 3px solid #000000 !important; border-radius: 10px !important; font-weight: 900 !important; }
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
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        df['p_val'] = df.iloc[:, 4].apply(extract_num)
        df['d_val'] = df.iloc[:, 10].apply(extract_num)
        return df
    except: return None

df = get_data()

if df is not None:
    if 'page' not in st.session_state: st.session_state.page = 'main'
    if 'current_page' not in st.session_state: st.session_state.current_page = 0

    if st.session_state.page == 'main':
        st.markdown("<h1 style='text-align:center; color:#000000; font-weight:900;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        
        search_term = st.text_input("🔍 ابحث عن مشروع أو مطور:", placeholder="مثال: بالم هيلز...")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: s_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df.iloc[:, 3].unique().tolist()))
        with c2: s_type = st.selectbox("🏠 النوع", ["الكل"] + sorted(df.iloc[:, 7].unique().tolist()))
        with c3: m_price = st.number_input("💰 أقصى سعر", value=0)
        with c4: m_down = st.number_input("💵 أقصى مقدم", value=0)

        f_df = df.copy()
        if search_term: f_df = f_df[f_df.iloc[:, 0].str.contains(search_term, na=False, case=False) | f_df.iloc[:, 2].str.contains(search_term, na=False, case=False)]
        if s_area != "الكل": f_df = f_df[f_df.iloc[:, 3] == s_area]
        if s_type != "الكل": f_df = f_df[f_df.iloc[:, 7] == s_type]
        if m_price > 0: f_df = f_df[f_df['p_val'] <= m_price]
        if m_down > 0: f_df = f_df[f_df['d_val'] <= m_down]

        st.markdown("---")

        main_col, side_col = st.columns([3.1, 0.9])

        with main_col:
            items_per_page = 9
            total_pages = math.ceil(len(f_df) / items_per_page)
            current_items = f_df.iloc[st.session_state.current_page * items_per_page : (st.session_state.current_page + 1) * items_per_page]

            for i in range(0, len(current_items), 3):
                row_cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_items):
                        row = current_items.iloc[i + j]
                        with row_cols[j]:
                            # حاوية الكارت (التصميم الجمالي)
                            st.markdown(f"""
                                <div class="card-container">
                                    <div>
                                        <div class="card-title">{row[2]}</div>
                                        <div class="card-dev">🏢 {row[0]}</div>
                                        <div class="card-loc">📍 {row[3]}</div>
                                    </div>
                                    <div>
                                        <div class="card-price">{row[4]}</div>
                                        <div class="card-badge">مقدم {row[10]} | {row[9]}س</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            # الزر الشفاف الذي يغطي الكارت
                            if st.button("", key=f"btn_{i+j}"):
                                st.session_state.selected_item = row.to_list()
                                st.session_state.page = 'details'; st.rerun()

            # أزرار التنقل
            st.markdown("---")
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            with nav1:
                if st.session_state.current_page > 0:
                    if st.button("⬅️ السابق", key="prev"): st.session_state.current_page -= 1; st.rerun()
            with nav2: st.markdown(f"<p style='text-align:center; font-weight:900;'>صفحة {st.session_state.current_page+1}/{total_pages}</p>", unsafe_allow_html=True)
            with nav3:
                if st.session_state.current_page < total_pages - 1:
                    if st.button("التالي ➡️", key="next"): st.session_state.current_page += 1; st.rerun()

        with side_col:
            st.markdown("<h5 style='text-align:center; color:white; background:#b45309; padding:8px; border-radius:10px; font-weight:900;'>🔥 أقوى 10 فرص</h5>", unsafe_allow_html=True)
            for idx, row in df.head(10).iterrows():
                st.markdown(f"""<div class="micro-card"><div style="font-weight:900; font-size:0.9rem;">#{idx+1} {row[2]}</div><div style="color:#166534; font-weight:700; font-size:0.85rem;">{row[4]}</div></div>""", unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        if st.button("🔙 عودة للقائمة"): st.session_state.page = 'main'; st.rerun()
        st.markdown(f"<h1 style='color:#000000; font-weight:900;'>{item[2]}</h1>", unsafe_allow_html=True)
        st.error(f"### 💡 الزتونة الفنية:\n\n**{item[11]}**")
        st.success(f"المطور: {item[0]} | السعر: {item[4]} | المقدم: {item[10]} | التقسيط: {item[9]} سنوات")
