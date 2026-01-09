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
    
    /* خلفية بيضاء ونصوص سوداء واضحة */
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #fcfcfc; color: #000000;
    }

    /* كروت ميكرو - أصغر حجم ممكن */
    .micro-card {
        background: #ffffff; border-radius: 8px; padding: 10px;
        border: 1px solid #d1d5db; border-right: 6px solid #000000;
        margin-bottom: 8px; min-height: 140px;
        display: flex; flex-direction: column; justify-content: space-between;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    /* نصوص سوداء وكحلية شديدة الوضوح */
    .txt-dev { color: #000000 !important; font-size: 1.1rem; font-weight: 900; line-height: 1.1; }
    .txt-proj { color: #1e3a8a !important; font-size: 0.9rem; font-weight: 700; margin-top: 2px; }
    .txt-price { color: #166534 !important; font-size: 1.1rem; font-weight: 900; margin: 4px 0; }
    .txt-meta { color: #4b5563 !important; font-size: 0.8rem; font-weight: 600; }

    /* أزرار صغيرة جداً */
    div.stButton > button {
        background-color: #000000 !important; color: white !important;
        font-size: 0.75rem !important; height: 28px !important;
        border-radius: 4px !important; width: 100%; padding: 0 !important;
    }
    
    /* تصغير الفراغات بين العناصر */
    .stMainBlockContainer { padding-top: 1rem !important; }
    [data-testid="stVerticalBlock"] { gap: 0.3rem !important; }
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
        df['price_val'] = df.iloc[:, 4].apply(extract_num)
        return df
    except: return None

df = get_data()

if df is not None:
    if 'page' not in st.session_state: st.session_state.page = 'main'
    if 'current_page' not in st.session_state: st.session_state.current_page = 0

    if st.session_state.page == 'main':
        st.markdown("<h3 style='text-align:center; font-weight:900;'>🏠 منصة معلوماتى العقارية</h3>", unsafe_allow_html=True)
        
        # البحث والفلاتر بشكل مدمج جداً
        f1, f2, f3 = st.columns([2, 1, 1])
        with f1: s_query = st.text_input("🔍 بحث:", placeholder="المطور/المشروع", label_visibility="collapsed")
        with f2: s_area = st.selectbox("المكان", ["الكل"] + sorted(df.iloc[:, 3].dropna().unique().tolist()), label_visibility="collapsed")
        with f3: s_price = st.number_input("السعر", value=0, step=1000000, label_visibility="collapsed")

        f_df = df.copy()
        if s_query: f_df = f_df[f_df.iloc[:, 0].str.contains(s_query, na=False, case=False) | f_df.iloc[:, 2].str.contains(s_query, na=False, case=False)]
        if s_area != "الكل": f_df = f_df[f_df.iloc[:, 3] == s_area]
        if s_price > 0: f_df = f_df[f_df['price_val'] <= s_price]

        main_col, side_col = st.columns([3.4, 0.6])

        with main_col:
            items_per_page = 12
            total_pages = math.ceil(len(f_df) / items_per_page)
            start_idx = st.session_state.current_page * items_per_page
            current_items = f_df.iloc[start_idx : start_idx + items_per_page]

            # شبكة 3 أعمدة
            for i in range(0, len(current_items), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_items):
                        row = current_items.iloc[i + j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="micro-card">
                                    <div>
                                        <div class="txt-dev">{row[0]}</div>
                                        <div class="txt-proj">{row[2]}</div>
                                        <div class="txt-meta">📍 {row[3]}</div>
                                    </div>
                                    <div>
                                        <div class="txt-price">{row[4]}</div>
                                        <div class="txt-meta">💳 {row[10]} | {row[9]}س</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button("التفاصيل", key=f"b_{start_idx+i+j}"):
                                st.session_state.selected_dev = row[0]
                                st.session_state.page = 'details'
                                st.rerun()

            # تحكم بسيط في الصفحات
            n1, n2, n3 = st.columns([1, 1, 1])
            with n1: 
                if st.session_state.current_page > 0:
                    if st.button("السابق"): st.session_state.current_page -= 1; st.rerun()
            with n2: st.markdown(f"<p style='text-align:center; font-size:0.8rem;'>{st.session_state.current_page+1}/{total_pages}</p>", unsafe_allow_html=True)
            with n3:
                if st.session_state.current_page < total_pages - 1:
                    if st.button("التالي"): st.session_state.current_page += 1; st.rerun()

        with side_col:
            st.markdown("<div style='border:1px solid #ddd; padding:10px; border-radius:5px;'>", unsafe_allow_html=True)
            st.markdown("<p style='font-weight:900; font-size:0.8rem; margin:0;'>📢 تنبيهات</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:0.75rem;'>مساحة جانبية للإضافات.</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        dev = st.session_state.selected_dev
        projects = df[df.iloc[:, 0] == dev]
        if st.button("🔙 عودة"): st.session_state.page = 'main'; st.rerun()
        st.markdown(f"<h2>🏢 {dev}</h2>", unsafe_allow_html=True)
        for _, row in projects.iterrows():
            with st.expander(f"📍 {row[2]} - {row[4]}"):
                st.write(f"**الموقع:** {row[3]} | **السداد:** {row[10]} | {row[9]} سنوات")
                st.error(f"**الزتونة:** {row[11]}")
