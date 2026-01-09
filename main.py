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
    
    /* خلفية بيضاء صافية */
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* كروت ميكرو - عرض نحيف وطول صغير */
    .micro-card {
        background: #ffffff; 
        border: 1px solid #e2e8f0; 
        border-right: 5px solid #001a33; 
        border-radius: 6px; 
        padding: 8px;
        margin-bottom: 5px; 
        min-height: 110px; /* تقليل الطول لأقصى درجة */
        display: flex; 
        flex-direction: column; 
        justify-content: space-between;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* نصوص كحلية وسوداء واضحة جداً */
    .txt-dev { color: #000000 !important; font-size: 0.95rem; font-weight: 900; line-height: 1; }
    .txt-proj { color: #1e40af !important; font-size: 0.8rem; font-weight: 700; margin-top: 2px; }
    .txt-price { color: #166534 !important; font-size: 1rem; font-weight: 900; margin: 2px 0; }
    
    /* صندوق بيانات صغير */
    .info-box {
        background: #f8fafc; color: #334155; 
        font-size: 0.75rem; font-weight: 600;
        padding: 2px 5px; border-radius: 3px;
        border: 1px solid #f1f5f9; margin-top: 3px;
    }

    /* زر التفاصيل - نحيف وصغير */
    div.stButton > button {
        background-color: #001a33 !important; color: white !important;
        font-size: 0.7rem !important; height: 24px !important;
        border-radius: 3px !important; width: 100%; border: none !important;
        font-weight: 700 !important; line-height: 1 !important;
    }

    /* تقليل مساحة الحواف في الصفحة */
    .stMainBlockContainer { padding: 0.5rem 1rem !important; }
    [data-testid="stVerticalBlock"] { gap: 0.1rem !important; }
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
        st.markdown("<h4 style='text-align:center; font-weight:900; color:#001a33; margin:0;'>🏠 منصة معلوماتى العقارية</h4>", unsafe_allow_html=True)
        
        # سطر فلاتر نحيف جداً
        f1, f2, f3 = st.columns([2, 1, 1])
        with f1: sq = st.text_input("بحث", placeholder="المطور/المشروع", label_visibility="collapsed")
        with f2: sa = st.selectbox("المنطقة", ["الكل"] + sorted(df.iloc[:, 3].dropna().unique().tolist()), label_visibility="collapsed")
        with f3: sp = st.number_input("السعر", value=0, label_visibility="collapsed")

        f_df = df.copy()
        if sq: f_df = f_df[f_df.iloc[:, 0].str.contains(sq, na=False, case=False) | f_df.iloc[:, 2].str.contains(sq, na=False, case=False)]
        if sa != "الكل": f_df = f_df[f_df.iloc[:, 3] == sa]
        if sp > 0: f_df = f_df[f_df['p_val'] <= sp]

        # استخدام مساحة العرض بالكامل للكروت
        main_col, side_col = st.columns([3.6, 0.4])

        with main_col:
            items = 15 # زيادة العدد في الصفحة لأن الحجم صغر
            total = math.ceil(len(f_df) / items)
            start = st.session_state.curr * items
            curr_items = f_df.iloc[start : start + items]

            # شبكة 3 أعمدة
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
                                        <div class="txt-proj">{row[2]}</div>
                                    </div>
                                    <div>
                                        <div class="txt-price">{row[4]}</div>
                                        <div class="info-box">📍 {row[3]} | 💳 {row[10]}</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button("التفاصيل", key=f"b_{start+i+j}"):
                                st.session_state.selected_dev = row[0]
                                st.session_state.page = 'details'
                                st.rerun()

            # أزرار تنقل
            n1, n2, n3 = st.columns([1,1,1])
            with n1: 
                if st.session_state.curr > 0:
                    if st.button("السابق"): st.session_state.curr -= 1; st.rerun()
            with n2: st.markdown(f"<p style='text-align:center; font-size:0.7rem;'>{st.session_state.curr+1}/{total}</p>", unsafe_allow_html=True)
            with n3:
                if st.session_state.curr < total - 1:
                    if st.button("التالي"): st.session_state.curr += 1; st.rerun()

    elif st.session_state.page == 'details':
        dev = st.session_state.selected_dev
        projs = df[df.iloc[:, 0] == dev]
        if st.button("🔙 عودة"): st.session_state.page = 'main'; st.rerun()
        st.markdown(f"<h3 style='color:#001a33;'>🏢 {dev}</h3>", unsafe_allow_html=True)
        for _, r in projs.iterrows():
            with st.expander(f"📍 {r[2]} - {r[4]}"):
                st.info(f"**الزتونة:** {r[11]}")
