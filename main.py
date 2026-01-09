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

    /* تصميم الكارت الجمالي المدمج */
    .clickable-card {
        position: relative;
        background: #ffffff; border-radius: 15px; padding: 20px;
        border-right: 12px solid #001a33; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        min-height: 240px;
        transition: 0.3s;
        display: flex; flex-direction: column; justify-content: space-between;
        z-index: 1;
    }
    .clickable-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        border-right-color: #059669;
    }

    /* جعل زرار Streamlit يغطي الكارت بالكامل ويكون شفافاً */
    .stButton button {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        z-index: 10; /* فوق محتوى الكارت */
        cursor: pointer;
    }

    /* نصوص الكارت */
    .card-title { color: #000000 !important; font-size: 1.4rem; font-weight: 900; margin: 0; }
    .card-dev { color: #475569 !important; font-size: 1.1rem; font-weight: 700; }
    .card-price { color: #059669 !important; font-size: 1.5rem; font-weight: 900; }
    .card-badge { 
        background: #001a33; color: white; padding: 6px; 
        border-radius: 8px; text-align: center; font-weight: 900; 
    }

    /* ستايل صفحة المطور */
    .dev-box { background: #001a33; color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px; }
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
        df['price_val'] = df.iloc[:, 4].apply(extract_num)
        return df
    except: return None

df = get_data()

if df is not None:
    if 'page' not in st.session_state: st.session_state.page = 'main'
    if 'current_page' not in st.session_state: st.session_state.current_page = 0

    # --- الصفحة الرئيسية ---
    if st.session_state.page == 'main':
        st.markdown("<h1 style='text-align:center; color:#001a33; font-weight:900;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        
        search_term = st.text_input("🔍 ابحث عن مشروع أو مطور:", placeholder="مثال: SODIC...")
        
        f_df = df.copy()
        if search_term:
            f_df = f_df[f_df.iloc[:, 0].str.contains(search_term, na=False, case=False) | f_df.iloc[:, 2].str.contains(search_term, na=False, case=False)]

        st.markdown("---")
        main_col, side_col = st.columns([3.2, 0.8])

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
                            # تصميم الكارت الجمالي
                            st.markdown(f"""
                                <div class="clickable-card">
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
                            # الزر الشفاف الذي يغطي المساحة بالكامل
                            if st.button("", key=f"btn_{i+j}"):
                                st.session_state.selected_item = row.to_list()
                                st.session_state.page = 'details'
                                st.rerun()

            # أزرار التنقل
            st.markdown("---")
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            with nav1:
                if st.session_state.current_page > 0:
                    if st.button("⬅️ السابق"): st.session_state.current_page -= 1; st.rerun()
            with nav2: st.markdown(f"<p style='text-align:center; font-weight:900;'>صفحة {st.session_state.current_page+1}/{total_pages}</p>", unsafe_allow_html=True)
            with nav3:
                if st.session_state.current_page < total_pages - 1:
                    if st.button("التالي ➡️"): st.session_state.current_page += 1; st.rerun()

        with side_col:
            st.markdown("<h5 style='text-align:center; color:#ffffff; background:#d97706; padding:8px; border-radius:10px; font-weight:900;'>🔥 أقوى 10 فرص</h5>", unsafe_allow_html=True)
            for idx, row in df.head(10).iterrows():
                st.markdown(f"""<div style="background:white; padding:10px; border-right:5px solid #d97706; margin-bottom:5px; border-radius:8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                    <div style="font-weight:900; font-size:0.9rem;">{row[2]}</div>
                    <div style="color:#059669; font-size:0.8rem; font-weight:700;">{row[4]}</div>
                </div>""", unsafe_allow_html=True)

    # --- صفحة التفاصيل (نبذة المطور ومشاريع الشركة) ---
    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        dev_name = item[0]

        if st.button("🔙 العودة للقائمة"):
            st.session_state.page = 'main'
            st.rerun()

        # نبذة المطور
        st.markdown(f"""
            <div class="dev-box">
                <h1 style="margin:0;">🏢 {dev_name}</h1>
                <p style="font-size:1.1rem; opacity:0.9; margin-top:10px;">
                شركة {dev_name} تعد واحدة من أكبر الكيانات العقارية، ولها سجل حافل من المشاريع الناجحة التي تتميز بالتصاميم العصرية والالتزام بمواعيد التسليم.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # الزتونة الفنية للمشروع المختار
        st.error(f"### 💡 الزتونة الفنية لـ {item[2]}:\n\n**{item[11]}**")

        st.markdown("---")
        
        # مشاريع الشركة الأخرى
        st.markdown(f"### 🏗️ مشاريع أخرى لشركة {dev_name}:")
        other_projects = df[df.iloc[:, 0] == dev_name]
        
        for i in range(0, len(other_projects), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(other_projects):
                    p = other_projects.iloc[i + j]
                    with cols[j]:
                        st.info(f"**{p[2]}**\n\n📍 {p[3]}\n\n💰 {p[4]}")
