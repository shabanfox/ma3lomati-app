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
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f0f2f5; 
    }

    /* هيدر نحيف جداً */
    .compact-header {
        text-align: center; color: #ffffff; background: #001a33;
        font-weight: 900; font-size: 1.2rem; padding: 5px;
        border-radius: 5px; margin-bottom: 5px;
    }

    /* شريط البحث المطور */
    .search-bar-container {
        background: white; padding: 10px; border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 10px;
        display: flex; gap: 10px; align-items: center;
    }

    /* كروت نانو مطورة */
    .nano-card {
        background: #ffffff; border: 1px solid #e5e7eb; 
        border-right: 4px solid #1e40af; border-radius: 6px; 
        padding: 6px 10px; margin-bottom: 4px; 
        min-height: 90px; display: flex; flex-direction: column; justify-content: space-between;
    }

    .t-dev { color: #000 !important; font-size: 0.85rem; font-weight: 900; line-height: 1; }
    .t-proj { color: #2563eb !important; font-size: 0.75rem; font-weight: 700; }
    .t-price { color: #059669 !important; font-size: 0.95rem; font-weight: 900; }
    .t-info { color: #64748b; font-size: 0.7rem; font-weight: 600; margin-top: 1px; }

    /* زر تفاصيل ميكرو */
    div.stButton > button {
        background: #0f172a !important; color: white !important;
        font-size: 0.65rem !important; height: 18px !important;
        border-radius: 3px !important; width: 100%; border: none !important;
        font-weight: 700 !important; padding: 0 !important; margin-top: 2px !important;
        line-height: 18px !important;
    }

    /* تصغير المدخلات */
    .stTextInput > div > div > input, .stSelectbox > div > div > div {
        height: 30px !important; font-size: 0.8rem !important;
    }
    
    /* ضغط مساحة العمل */
    .stMainBlockContainer { padding: 0.5rem 1.5rem !important; }
    [data-testid="stVerticalBlock"] { gap: 0rem !important; }
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
        st.markdown('<div class="compact-header">🏠 منصة معلوماتى العقارية</div>', unsafe_allow_html=True)
        
        # شريط البحث والفلاتر في سطر واحد مضغوط
        col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
        with col_s1: sq = st.text_input("بحث", placeholder="المطور أو المشروع...", label_visibility="collapsed")
        with col_s2: sa = st.selectbox("المكان", ["الكل"] + sorted(df.iloc[:, 3].dropna().unique().tolist()), label_visibility="collapsed")
        with col_s3: sp = st.number_input("السعر", value=0, label_visibility="collapsed")

        f_df = df.copy()
        if sq: f_df = f_df[f_df.iloc[:, 0].str.contains(sq, na=False, case=False) | f_df.iloc[:, 2].str.contains(sq, na=False, case=False)]
        if sa != "الكل": f_df = f_df[f_df.iloc[:, 3] == sa]
        if sp > 0: f_df = f_df[f_df['p_val'] <= sp]

        # توزيع الصفحة (يمين للكروت، يسار للإضافات)
        main_area, side_area = st.columns([3.4, 0.6])

        with main_area:
            items = 9 
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
                                <div class="nano-card">
                                    <div>
                                        <div class="t-dev">{row[0]}</div>
                                        <div class="t-proj">{row[2]}</div>
                                    </div>
                                    <div>
                                        <div class="t-price">{row[4]}</div>
                                        <div class="t-info">📍 {row[3]} | 💳 {row[10]}</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button("تفاصيل", key=f"b_{start+i+j}"):
                                st.session_state.selected_dev = row[0]
                                st.session_state.page = 'details'
                                st.rerun()

            # أزرار تنقل مدمجة
            n1, n2, n3 = st.columns([1,2,1])
            with n1: 
                if st.session_state.curr > 0:
                    if st.button("السابق", key="prev"): st.session_state.curr -= 1; st.rerun()
            with n2: st.markdown(f"<p style='text-align:center; font-size:0.7rem; font-weight:700;'>{st.session_state.curr+1} / {total}</p>", unsafe_allow_html=True)
            with n3:
                if st.session_state.curr < total - 1:
                    if st.button("التالي", key="next"): st.session_state.curr += 1; st.rerun()

        with side_area:
            st.markdown("<div style='border-right:2px solid #001a33; padding:5px; font-size:0.75rem;'>", unsafe_allow_html=True)
            st.markdown("**⭐ إضافات:**")
            st.markdown("مساحة مخصصة للتنبيهات السريعة.")
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        if st.button("⬅️ عودة"): st.session_state.page = 'main'; st.rerun()
        dev = st.session_state.selected_dev
        projs = df[df.iloc[:, 0] == dev]
        st.markdown(f"<h6>🏢 {dev}</h6>", unsafe_allow_html=True)
        for _, r in projs.iterrows():
            with st.expander(f"{r[2]} - {r[4]}"):
                st.info(f"**الزتونة:** {r[11]}")
