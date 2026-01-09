import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة والستايل الفائق الوضوح
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الزوائد */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* الخلفية العامة */
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f1f5f9; 
    }

    /* تحويل زر الـ Streamlit إلى "كارت عقاري" كامل قابل للضغط */
    div.stButton > button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: none !important;
        border-right: 12px solid #000000 !important;
        border-radius: 15px !important;
        padding: 20px !important;
        width: 100% !important;
        min-height: 250px !important;
        text-align: right !important;
        display: block !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1) !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }

    /* تأثير عند تمرير الماوس فوق الكارت */
    div.stButton > button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 12px 24px rgba(0,0,0,0.2) !important;
        border-right-color: #166534 !important; /* يتغير اللون للأخضر عند الوقوف عليه */
    }

    /* تنسيق البحث والفلاتر */
    .stTextInput input {
        border: 3px solid #000000 !important;
        border-radius: 10px !important;
        font-weight: 900 !important;
        color: #000000 !important;
    }

    /* كروت الفرص ميكرو (يسار) */
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
        df['price_val'] = df.iloc[:, 4].apply(extract_num)
        df['down_val'] = df.iloc[:, 10].apply(extract_num)
        return df
    except: return None

df = get_data()

if df is not None:
    if 'page' not in st.session_state: st.session_state.page = 'main'
    if 'current_page' not in st.session_state: st.session_state.current_page = 0

    if st.session_state.page == 'main':
        st.markdown("<h1 style='text-align:center; color:#000000; font-weight:900;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        
        search_term = st.text_input("🔍 ابحث هنا...", placeholder="اسم المشروع أو المطور")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: s_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df.iloc[:, 3].unique().tolist()))
        with c2: s_type = st.selectbox("🏠 النوع", ["الكل"] + sorted(df.iloc[:, 7].unique().tolist()))
        with c3: m_price = st.number_input("💰 أقصى سعر", value=0)
        with c4: m_down = st.number_input("💵 أقصى مقدم", value=0)

        f_df = df.copy()
        if search_term:
            f_df = f_df[f_df.iloc[:, 0].str.contains(search_term, na=False, case=False) | f_df.iloc[:, 2].str.contains(search_term, na=False, case=False)]
        if s_area != "الكل": f_df = f_df[f_df.iloc[:, 3] == s_area]
        if s_type != "الكل": f_df = f_df[f_df.iloc[:, 7] == s_type]
        if m_price > 0: f_df = f_df[f_df['price_val'] <= m_price]
        if m_down > 0: f_df = f_df[f_df['down_val'] <= m_down]

        st.markdown("---")

        main_col, side_col = st.columns([3.1, 0.9])

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
                            # الكارت بالكامل هو عبارة عن زر
                            card_content = f"""
{row[2]}
🏢 {row[0]}
📍 {row[3]}

💰 {row[4]}
🕒 مقدم {row[10]} | {row[9]}س
                            """
                            if st.button(card_content, key=f"card_{i+j}"):
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
            st.markdown("<h5 style='text-align:center; color:#ffffff; background:#b45309; padding:8px; border-radius:10px; font-weight:900;'>🔥 أقوى 10 فرص</h5>", unsafe_allow_html=True)
            for idx, row in df.head(10).iterrows():
                st.markdown(f"""
                    <div class="micro-card">
                        <div style="color:#000000; font-weight:900; font-size:0.9rem;">#{idx+1} {row[2]}</div>
                        <div style="color:#166534; font-size:0.85rem; font-weight:700;">{row[4]}</div>
                    </div>
                """, unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        if st.button("🔙 العودة"): st.session_state.page = 'main'; st.rerun()
        st.markdown(f"<h1 style='color:#000000; font-weight:900;'>{item[2]}</h1>", unsafe_allow_html=True)
        st.error(f"### 💡 الزتونة الفنية:\n\n**{item[11]}**")
        st.success(f"المطور: {item[0]} | السعر: {item[4]} | المقدم: {item[10]} | التقسيط: {item[9]} سنوات")
