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

    /* تصميم الكارت المدمج */
    .stButton button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: none !important;
        border-right: 12px solid #001a33 !important;
        border-radius: 15px !important;
        padding: 20px !important;
        width: 100% !important;
        min-height: 240px !important;
        text-align: right !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1) !important;
        display: block !important;
        transition: 0.3s !important;
    }

    .stButton button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 12px 24px rgba(0,0,0,0.15) !important;
        border-right-color: #059669 !important;
    }

    /* نصوص البحث */
    .stTextInput input {
        border: 2px solid #001a33 !important;
        border-radius: 10px !important;
        font-weight: 900 !important;
    }

    /* كروت الـ 10 فرص ميكرو */
    .micro-card {
        background: white; border-radius: 8px; padding: 10px;
        border-right: 5px solid #d97706; margin-bottom: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
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
        df['price_val'] = df.iloc[:, 4].apply(extract_num)
        return df
    except: return None

df = get_data()

if df is not None:
    if 'page' not in st.session_state: st.session_state.page = 'main'
    if 'current_page' not in st.session_state: st.session_state.current_page = 0

    # --- الصفحة الرئيسية ---
    if st.session_state.page == 'main':
        st.markdown("<h1 style='text-align:center; color:#000000; font-weight:900;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        
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
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_items):
                        row = current_items.iloc[i + j]
                        with cols[j]:
                            # محتوى الكارت المدمج داخل الزر
                            card_html = f"""
                            {row[2]}
                            🏢 {row[0]}
                            📍 {row[3]}
                            
                            💰 {row[4]}
                            💵 مقدم {row[10]} | {row[9]}س
                            """
                            if st.button(card_html, key=f"c_{i+j}"):
                                st.session_state.selected_item = row.to_list()
                                st.session_state.page = 'details'
                                st.rerun()

            # أزرار التنقل
            st.markdown("---")
            n1, n2, n3 = st.columns([1, 2, 1])
            with n1:
                if st.session_state.current_page > 0:
                    if st.button("⬅️ السابق", key="prev_main"): st.session_state.current_page -= 1; st.rerun()
            with n2: st.markdown(f"<p style='text-align:center; font-weight:900;'>صفحة {st.session_state.current_page+1}/{total_pages}</p>", unsafe_allow_html=True)
            with n3:
                if st.session_state.current_page < total_pages - 1:
                    if st.button("التالي ➡️", key="next_main"): st.session_state.current_page += 1; st.rerun()

        with side_col:
            st.markdown("<h6 style='text-align:center; color:white; background:#d97706; padding:8px; border-radius:8px;'>🔥 أقوى 10 فرص</h6>", unsafe_allow_html=True)
            for idx, row in df.head(10).iterrows():
                st.markdown(f"""<div class="micro-card">
                    <div style="font-weight:900; font-size:0.85rem;">{row[2]}</div>
                    <div style="color:#059669; font-size:0.8rem; font-weight:700;">{row[4]}</div>
                </div>""", unsafe_allow_html=True)

    # --- صفحة المطور والتفاصيل ---
    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        dev_name = item[0]

        if st.button("🔙 عودة للقائمة"):
            st.session_state.page = 'main'
            st.rerun()

        # نبذة عن المطور
        st.markdown(f"""
            <div style="background:#001a33; color:white; padding:30px; border-radius:15px; margin-bottom:20px;">
                <h1 style="margin:0;">🏢 {dev_name}</h1>
                <hr style="border-color: rgba(255,255,255,0.2);">
                <p style="font-size:1.2rem;">تعتبر شركة {dev_name} من المطورين الرائدين، وتتميز بالالتزام بالتسليم والجودة العالية في كافة مشاريعها العقارية.</p>
            </div>
        """, unsafe_allow_html=True)

        # الزتونة الفنية
        st.error(f"### 💡 الزتونة الفنية لـ {item[2]}:\n\n**{item[11]}**")

        st.markdown("---")
        
        # مشاريع الشركة الأخرى
        st.markdown(f"### 🏗️ جميع مشاريع شركة {dev_name}:")
        others = df[df.iloc[:, 0] == dev_name]
        
        for i in range(0, len(others), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(others):
                    p = others.iloc[i + j]
                    with cols[j]:
                        st.info(f"**{p[2]}**\n\n📍 {p[3]}\n\n💰 {p[4]}")
