import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة والستايل الجمالي
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }

    /* تصميم الكارت الجمالي المحفوظ */
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
        z-index: 1;
    }

    .card-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        border-right-color: #16a34a;
    }

    .card-title { color: #000000 !important; font-size: 1.4rem; font-weight: 900; margin-bottom: 5px; }
    .card-dev { color: #475569 !important; font-size: 1.1rem; font-weight: 700; }
    .card-loc { color: #64748b !important; font-size: 1rem; font-weight: 600; margin-bottom: 10px; }
    .card-price { color: #166534 !important; font-size: 1.6rem; font-weight: 900; margin: 10px 0; }
    .card-badge { 
        background: #001a33; color: white; padding: 8px; 
        border-radius: 8px; text-align: center; font-weight: 900; font-size: 1rem;
    }

    /* جعل زرار Streamlit يغطي الكارت بالكامل ويكون شفافاً تماماً */
    div.stButton > button {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        z-index: 10;
        cursor: pointer;
    }
    div.stButton > button:hover { background: transparent !important; border: none !important; }

    /* خانة البحث والفلاتر */
    .stTextInput input { border: 3px solid #000000 !important; border-radius: 10px !important; font-weight: 900 !important; }
    
    /* كروت الفرص ميكرو - يسار */
    .micro-card {
        background: #ffffff; border-radius: 8px; padding: 10px;
        border-right: 6px solid #b45309; margin-bottom: 8px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.1);
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
    if 'current_page' not in st.session_state: st.session_state.current_page = 0

    if st.session_state.page == 'main':
        st.markdown("<h1 style='text-align:center; color:#000000; font-weight:900;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        
        search_term = st.text_input("🔍 ابحث عن مشروع أو مطور:", placeholder="اكتب هنا...")
        
        f_df = df.copy()
        if search_term:
            f_df = f_df[f_df.iloc[:, 0].str.contains(search_term, na=False, case=False) | f_df.iloc[:, 2].str.contains(search_term, na=False, case=False)]

        st.markdown("---")
        main_col, side_col = st.columns([3.2, 0.8])

        with main_col:
            items_per_page = 9
            total_pages = math.ceil(len(f_df) / items_per_page)
            current_items = f_df.iloc[st.session_state.current_page * items_per_page : (st.session_state.current_page + 1) * items_per_page]

            # عرض 3 كروت في الصف
            for i in range(0, len(current_items), 3):
                row_cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_items):
                        row = current_items.iloc[i + j]
                        with row_cols[j]:
                            # تصميم الكارت الجمالي
                            st.markdown(f"""
                                <div class="card-container">
                                    <div>
                                        <div class="card-title">{row[2]}</div>
                                        <div class="card-dev">🏢 {row[0]}</div>
                                        <div class="card-loc">📍 {row[3]}</div>
                                    </div>
                                    <div>
                                        <div class="card-price">{row[4]}</div>
                                        <div class="card-badge">مقدم {row[10]} | {row[9]} سنوات</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            # الزر الشفاف الذي يجعل الكارت بالكامل قابلاً للضغط
                            if st.button("", key=f"btn_{i+j}"):
                                st.session_state.selected_item = row.to_list()
                                st.session_state.page = 'details'
                                st.rerun()

            # أزرار التنقل (السابق والتالي)
            st.markdown("---")
            n1, n2, n3 = st.columns([1, 2, 1])
            with n1:
                if st.session_state.current_page > 0:
                    if st.button("⬅️ السابق", key="prev"): st.session_state.current_page -= 1; st.rerun()
            with n2:
                st.markdown(f"<p style='text-align:center; font-weight:900; font-size:1.2rem;'>صفحة {st.session_state.current_page+1} من {total_pages}</p>", unsafe_allow_html=True)
            with n3:
                if st.session_state.current_page < total_pages - 1:
                    if st.button("التالي ➡️", key="next"): st.session_state.current_page += 1; st.rerun()

        with side_col:
            st.markdown("<h5 style='text-align:center; color:white; background:#b45309; padding:8px; border-radius:10px; font-weight:900;'>🔥 أقوى 10 فرص</h5>", unsafe_allow_html=True)
            for idx, row in df.head(10).iterrows():
                st.markdown(f"""<div class="micro-card">
                    <div style="font-weight:900; font-size:0.9rem;">{row[2]}</div>
                    <div style="color:#166534; font-weight:700; font-size:0.85rem;">{row[4]}</div>
                </div>""", unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        dev_name = item[0]
        if st.button("🔙 العودة للقائمة الرئيسية"): st.session_state.page = 'main'; st.rerun()

        # صفحة المطور
        st.markdown(f"""
            <div style="background:#001a33; color:white; padding:30px; border-radius:15px; margin-bottom:20px;">
                <h1 style="margin:0;">🏢 {dev_name}</h1>
                <p style="font-size:1.2rem; margin-top:10px;">شركة {dev_name} من المطورين الموثوقين بالسوق العقاري المصري، وتتميز بمشاريعها ذات العائد الاستثماري المرتفع والجودة العالية.</p>
            </div>
        """, unsafe_allow_html=True)

        st.error(f"### 💡 الزتونة الفنية لـ {item[2]}:\n\n**{item[11]}**")
        
        st.markdown(f"### 🏗️ مشاريع أخرى لشركة {dev_name}:")
        others = df[df.iloc[:, 0] == dev_name]
        for i in range(0, len(others), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(others):
                    with cols[j]: st.info(f"**{others.iloc[i+j][2]}**\n\n📍 {others.iloc[i+j][3]}\n\n💰 {others.iloc[i+j][4]}")
