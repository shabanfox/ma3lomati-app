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

    /* الهيدر الرئيسي */
    .main-header {
        text-align: center; color: #001a33; font-weight: 900; 
        font-size: 1.8rem; margin-bottom: 10px; padding: 10px;
        border-bottom: 2px solid #f1f5f9;
    }

    /* كروت نانو - نحيفة وقريبة */
    .nano-card {
        background: #ffffff; 
        border: 1px solid #eeeeee; 
        border-right: 4px solid #001a33; 
        border-radius: 4px; 
        padding: 6px 10px;
        margin-bottom: 4px; 
        min-height: 100px; 
        display: flex; 
        flex-direction: column; 
        justify-content: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }

    .t-dev { color: #000000 !important; font-size: 0.9rem; font-weight: 900; line-height: 1.1; }
    .t-proj { color: #1e40af !important; font-size: 0.8rem; font-weight: 700; margin: 2px 0; }
    .t-price { color: #166534 !important; font-size: 1rem; font-weight: 900; }
    .t-info { color: #555555; font-size: 0.75rem; font-weight: 600; }

    /* أزرار التفاصيل */
    div.stButton > button {
        background-color: #001a33 !important; color: white !important;
        font-size: 0.7rem !important; height: 24px !important;
        border-radius: 3px !important; width: 100%; border: none !important;
        font-weight: 700 !important; margin-top: 4px !important;
    }

    /* تقليل المسافات */
    .stMainBlockContainer { padding: 1rem 2rem !important; }
    [data-testid="stHorizontalBlock"] { gap: 0.3rem !important; }
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
        # الهيدر الذي طلبته
        st.markdown('<div class="main-header">🏠 منصة معلوماتى العقارية</div>', unsafe_allow_html=True)
        
        # سطر فلاتر مدمج
        f1, f2, f3 = st.columns([2, 1, 1])
        with f1: sq = st.text_input("بحث بالاسم أو المطور", placeholder="اكتب هنا...", label_visibility="collapsed")
        with f2: sa = st.selectbox("المنطقة", ["الكل"] + sorted(df.iloc[:, 3].dropna().unique().tolist()), label_visibility="collapsed")
        with f3: sp = st.number_input("أقصى سعر", value=0, label_visibility="collapsed")

        f_df = df.copy()
        if sq: f_df = f_df[f_df.iloc[:, 0].str.contains(sq, na=False, case=False) | f_df.iloc[:, 2].str.contains(sq, na=False, case=False)]
        if sa != "الكل": f_df = f_df[f_df.iloc[:, 3] == sa]
        if sp > 0: f_df = f_df[f_df['p_val'] <= sp]

        # تقسيم الصفحة: 3 أعمدة للكروت (جهة اليمين) وعمود للإضافات (جهة اليسار)
        main_area, side_area = st.columns([3.3, 0.7])

        with main_area:
            items = 9  # عرض 9 كروت فقط كما طلبت
            total = math.ceil(len(f_df) / items)
            start = st.session_state.curr * items
            curr_items = f_df.iloc[start : start + items]

            # شبكة الكروت (3 أعمدة)
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
                            if st.button("التفاصيل", key=f"b_{start+i+j}"):
                                st.session_state.selected_dev = row[0]
                                st.session_state.page = 'details'
                                st.rerun()

            # أزرار تنقل
            st.markdown("<br>", unsafe_allow_html=True)
            n1, n2, n3 = st.columns([1,1,1])
            with n1: 
                if st.session_state.curr > 0:
                    if st.button("السابق"): st.session_state.curr -= 1; st.rerun()
            with n2: st.markdown(f"<p style='text-align:center; font-size:0.8rem;'>{st.session_state.curr+1} / {total}</p>", unsafe_allow_html=True)
            with n3:
                if st.session_state.curr < total - 1:
                    if st.button("التالي"): st.session_state.curr += 1; st.rerun()

        with side_area:
            st.markdown("<div style='border-right:2px solid #001a33; padding:10px; background:#f8fafc; border-radius:5px;'>", unsafe_allow_html=True)
            st.markdown("<p style='font-weight:900; font-size:0.9rem; color:#001a33;'>⭐ إضافات</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:0.8rem;'>يمكنك هنا وضع روابط سريعة، نصائح عقارية، أو تحديثات السوق.</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        dev = st.session_state.selected_dev
        projs = df[df.iloc[:, 0] == dev]
        if st.button("🔙 عودة للقائمة"): st.session_state.page = 'main'; st.rerun()
        st.markdown(f"<h2 style='color:#001a33;'>🏢 {dev}</h2>", unsafe_allow_html=True)
        for _, r in projs.iterrows():
            with st.expander(f"📍 {r[2]} - {r[4]}"):
                st.error(f"**💡 الزتونة:** {r[11]}")
