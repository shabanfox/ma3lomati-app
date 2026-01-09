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
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* ضغط الحاويات الرئيسية */
    .stMainBlockContainer { padding: 0.2rem 0.5rem !important; }
    [data-testid="stVerticalBlock"] { gap: 0rem !important; }
    [data-testid="stHorizontalBlock"] { gap: 0.2rem !important; }

    /* كروت نانو - نحيفة جداً وقريبة من بعضها */
    .nano-card {
        background: #ffffff; 
        border: 1px solid #eeeeee; 
        border-right: 3px solid #001a33; 
        border-radius: 4px; 
        padding: 5px 8px;
        margin-bottom: 2px; 
        min-height: 95px; 
        display: flex; 
        flex-direction: column; 
        justify-content: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }

    .t-dev { color: #000000 !important; font-size: 0.85rem; font-weight: 900; line-height: 1; }
    .t-proj { color: #1e40af !important; font-size: 0.75rem; font-weight: 700; margin: 1px 0; }
    .t-price { color: #166534 !important; font-size: 0.9rem; font-weight: 900; }
    .t-info { color: #555555; font-size: 0.7rem; font-weight: 600; margin-top: 1px; }

    /* زر التفاصيل - أصغر حجم ممكن */
    div.stButton > button {
        background-color: #001a33 !important; color: white !important;
        font-size: 0.65rem !important; height: 20px !important;
        border-radius: 2px !important; width: 100%; border: none !important;
        font-weight: 700 !important; padding: 0 !important; margin-top: 2px !important;
    }

    /* تصغير الفلاتر */
    .stTextInput input, .stSelectbox div { height: 28px !important; font-size: 0.8rem !important; }
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
        # سطر فلاتر مدمج جداً
        c1, c2, c3, c4 = st.columns([1.5, 1, 1, 0.5])
        with c1: sq = st.text_input("بحث", placeholder="المطور/المشروع", label_visibility="collapsed")
        with c2: sa = st.selectbox("المنطقة", ["الكل"] + sorted(df.iloc[:, 3].dropna().unique().tolist()), label_visibility="collapsed")
        with c3: sp = st.number_input("السعر", value=0, label_visibility="collapsed")
        with c4: st.markdown(f"<p style='font-size:0.7rem; margin-top:5px;'>{len(df)} عقار</p>", unsafe_allow_html=True)

        f_df = df.copy()
        if sq: f_df = f_df[f_df.iloc[:, 0].str.contains(sq, na=False, case=False) | f_df.iloc[:, 2].str.contains(sq, na=False, case=False)]
        if sa != "الكل": f_df = f_df[f_df.iloc[:, 3] == sa]
        if sp > 0: f_df = f_df[f_df['p_val'] <= sp]

        items = 18 # عرض 18 كارت في الصفحة الواحدة
        total = math.ceil(len(f_df) / items)
        start = st.session_state.curr * items
        curr_items = f_df.iloc[start : start + items]

        # شبكة الكروت
        for i in range(0, len(curr_items), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(curr_items):
                    row = curr_items.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="nano-card">
                                <div class="t-dev">{row[0]}</div>
                                <div class="t-proj">{row[2]}</div>
                                <div class="t-price">{row[4]}</div>
                                <div class="t-info">📍 {row[3]} | 💳 {row[10]}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        if st.button("تفاصيل", key=f"b_{start+i+j}"):
                            st.session_state.selected_dev = row[0]
                            st.session_state.page = 'details'
                            st.rerun()

        # أزرار تنقل
        n1, n2, n3 = st.columns([1,1,1])
        with n1: 
            if st.session_state.curr > 0:
                if st.button("السابق"): st.session_state.curr -= 1; st.rerun()
        with n2: st.markdown(f"<p style='text-align:center; font-size:0.6rem; margin:0;'>{st.session_state.curr+1}/{total}</p>", unsafe_allow_html=True)
        with n3:
            if st.session_state.curr < total - 1:
                if st.button("التالي"): st.session_state.curr += 1; st.rerun()

    elif st.session_state.page == 'details':
        dev = st.session_state.selected_dev
        projs = df[df.iloc[:, 0] == dev]
        if st.button("🔙 عودة"): st.session_state.page = 'main'; st.rerun()
        st.markdown(f"<h6>🏢 {dev}</h6>", unsafe_allow_html=True)
        for _, r in projs.iterrows():
            with st.expander(f"📍 {r[2]} - {r[4]}"):
                st.info(f"{r[11]}")
