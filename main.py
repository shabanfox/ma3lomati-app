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
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f0f4f8; 
    }

    /* الكارت الأزرق الميكرو */
    .micro-card {
        background: #3b82f6; /* أزرق فاتح */
        border-radius: 10px; padding: 10px;
        margin-bottom: 8px; min-height: 130px;
        display: flex; flex-direction: column; justify-content: space-between;
        box-shadow: 0 3px 6px rgba(59, 130, 246, 0.2);
        color: white; /* خط أبيض على الأزرق */
    }

    /* تبادل الألوان للبيانات */
    .white-box {
        background: white; color: #1e40af; /* خط أزرق على الأبيض */
        padding: 2px 8px; border-radius: 5px;
        font-size: 0.85rem; font-weight: 900;
        margin-top: 5px; text-align: center;
    }

    .txt-dev { font-size: 1.05rem; font-weight: 900; line-height: 1.1; color: white; }
    .txt-proj { font-size: 0.85rem; font-weight: 700; color: #dbeafe; }
    .txt-price { font-size: 1.1rem; font-weight: 900; color: #ffffff; margin: 3px 0; }

    /* أزرار صغيرة جداً بيضاء */
    div.stButton > button {
        background-color: white !important; color: #3b82f6 !important;
        font-size: 0.75rem !important; height: 26px !important;
        border-radius: 4px !important; width: 100%; border: none !important;
        font-weight: 900 !important;
    }
    div.stButton > button:hover { background-color: #dbeafe !important; }

    /* تقليل الفراغات */
    .stMainBlockContainer { padding: 1rem 2rem !important; }
    [data-testid="stVerticalBlock"] { gap: 0.2rem !important; }
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
        return df
    except: return None

df = get_data()

if df is not None:
    if 'page' not in st.session_state: st.session_state.page = 'main'
    if 'curr' not in st.session_state: st.session_state.curr = 0

    if st.session_state.page == 'main':
        st.markdown("<h3 style='text-align:center; font-weight:900; color:#1e40af;'>🏠 منصة معلوماتى العقارية</h3>", unsafe_allow_html=True)
        
        # سطر البحث والفلاتر
        f1, f2, f3 = st.columns([2, 1, 1])
        with f1: sq = st.text_input("بحث", placeholder="المطور/المشروع", label_visibility="collapsed")
        with f2: sa = st.selectbox("المنطقة", ["الكل"] + sorted(df.iloc[:, 3].dropna().unique().tolist()), label_visibility="collapsed")
        with f3: sp = st.number_input("السعر", value=0, label_visibility="collapsed")

        f_df = df.copy()
        if sq: f_df = f_df[f_df.iloc[:, 0].str.contains(sq, na=False, case=False) | f_df.iloc[:, 2].str.contains(sq, na=False, case=False)]
        if sa != "الكل": f_df = f_df[f_df.iloc[:, 3] == sa]
        if sp > 0: f_df = f_df[f_df['p_val'] <= sp]

        m_col, s_col = st.columns([3.5, 0.5])

        with m_col:
            items = 12
            total = math.ceil(len(f_df) / items)
            start = st.session_state.curr * items
            curr_items = f_df.iloc[start : start + items]

            for i in range(0, len(curr_items), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(curr_items):
                        row = curr_items.iloc[i + j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="micro-card">
                                    <div>
                                        <div class="txt-dev">{row[0]}</div>
                                        <div class="txt-proj">🏢 {row[2]}</div>
                                    </div>
                                    <div>
                                        <div class="txt-price">{row[4]}</div>
                                        <div class="white-box">📍 {row[3]} | 💳 {row[10]}</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button("التفاصيل", key=f"b_{start+i+j}"):
                                st.session_state.selected_dev = row[0]
                                st.session_state.page = 'details'
                                st.rerun()

            # أزرار تنقل صغيرة
            n1, n2, n3 = st.columns([1,1,1])
            with n1: 
                if st.session_state.curr > 0:
                    if st.button("السابق"): st.session_state.curr -= 1; st.rerun()
            with n2: st.markdown(f"<p style='text-align:center; font-size:0.8rem;'>{st.session_state.curr+1}/{total}</p>", unsafe_allow_html=True)
            with n3:
                if st.session_state.curr < total - 1:
                    if st.button("التالي"): st.session_state.curr += 1; st.rerun()

        with s_col:
            st.markdown("<div style='font-size:0.7rem; border-right:2px solid #3b82f6; padding-right:5px;'>إضافات</div>", unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        dev = st.session_state.selected_dev
        projs = df[df.iloc[:, 0] == dev]
        if st.button("🔙 عودة"): st.session_state.page = 'main'; st.rerun()
        st.markdown(f"<h2 style='color:#1e40af;'>🏢 {dev}</h2>", unsafe_allow_html=True)
        for _, r in projs.iterrows():
            with st.expander(f"📍 {r[2]} - {r[4]}"):
                st.info(f"**الزتونة:** {r[11]}")
