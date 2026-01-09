import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة والستايل الداكن
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* خلفية الصفحة غامقة */
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #020617; color: white;
    }

    /* الفلاتر والبحث */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background-color: #1e293b !important; color: white !important; border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }

    /* الكروت الصغيرة الغامقة */
    .mini-card {
        background: #0f172a; border-radius: 12px; padding: 12px;
        border-right: 6px solid #1e3a8a; margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        min-height: 180px; display: flex; flex-direction: column; justify-content: space-between;
        transition: 0.3s; border: 1px solid #1e293b;
    }
    .mini-card:hover { transform: translateY(-3px); border-color: #3b82f6; }

    /* نصوص الكارت */
    .card-dev { color: #ffffff !important; font-size: 1.1rem; font-weight: 900; line-height: 1.2; }
    .card-proj { color: #94a3b8 !important; font-size: 0.9rem; font-weight: 700; margin-top: 2px; }
    .card-price { color: #fbbf24 !important; font-size: 1.15rem; font-weight: 900; margin: 5px 0; }
    .card-meta { color: #cbd5e1; font-size: 0.8rem; font-weight: 600; }

    /* الأزرار */
    div.stButton > button {
        background-color: #1e3a8a !important; color: white !important;
        font-size: 0.85rem !important; height: 32px !important;
        border-radius: 6px !important; border: none !important; width: 100%;
    }
    div.stButton > button:hover { background-color: #3b82f6 !important; }
    
    /* تعديل حاوية الفلاتر */
    [data-testid="stVerticalBlock"] { gap: 0.5rem; }
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
        st.markdown("<h2 style='text-align:center; color:#3b82f6; font-weight:900;'>🏠 منصة معلوماتى العقارية</h2>", unsafe_allow_html=True)
        
        # البحث والفلاتر في صف واحد
        f1, f2, f3 = st.columns([2, 1, 1])
        with f1: s_query = st.text_input("🔍 بحث:", placeholder="المطور أو المشروع...")
        with f2: s_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df.iloc[:, 3].dropna().unique().tolist()))
        with f3: s_price = st.number_input("💰 أقصى سعر", value=0, step=1000000)

        f_df = df.copy()
        if s_query: f_df = f_df[f_df.iloc[:, 0].str.contains(s_query, na=False, case=False) | f_df.iloc[:, 2].str.contains(s_query, na=False, case=False)]
        if s_area != "الكل": f_df = f_df[f_df.iloc[:, 3] == s_area]
        if s_price > 0: f_df = f_df[f_df['price_val'] <= s_price]

        st.markdown("<hr style='border-color:#1e293b;'>", unsafe_allow_html=True)
        main_col, side_col = st.columns([3.3, 0.7])

        with main_col:
            items_per_page = 12
            total_pages = math.ceil(len(f_df) / items_per_page)
            start_idx = st.session_state.current_page * items_per_page
            current_items = f_df.iloc[start_idx : start_idx + items_per_page]

            for i in range(0, len(current_items), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_items):
                        row = current_items.iloc[i + j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="mini-card">
                                    <div>
                                        <div class="card-dev">{row[0]}</div>
                                        <div class="card-proj">✨ {row[2]}</div>
                                        <div class="card-meta">📍 {row[3]}</div>
                                    </div>
                                    <div>
                                        <div class="card-price">{row[4]}</div>
                                        <div class="card-meta">💳 مقدم {row[10]} | {row[9]}س</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button("التفاصيل", key=f"b_{start_idx+i+j}"):
                                st.session_state.selected_dev = row[0]
                                st.session_state.page = 'details'
                                st.rerun()

            # أزرار التنقل صغيرة
            st.markdown("<br>", unsafe_allow_html=True)
            n1, n2, n3 = st.columns([1, 1, 1])
            with n1: 
                if st.session_state.current_page > 0:
                    if st.button("⬅️ السابق"): st.session_state.current_page -= 1; st.rerun()
            with n2: st.markdown(f"<p style='text-align:center; font-size:0.9rem;'>{st.session_state.current_page+1} / {total_pages}</p>", unsafe_allow_html=True)
            with n3:
                if st.session_state.current_page < total_pages - 1:
                    if st.button("التالي ➡️"): st.session_state.current_page += 1; st.rerun()

        with side_col:
            st.markdown("<div style='background:#1e293b; padding:15px; border-radius:10px; border:1px solid #334155;'>", unsafe_allow_html=True)
            st.markdown("<h6 style='color:#fbbf24; text-align:center;'>⭐ قسم الإضافات</h6>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:0.8rem; color:#94a3b8;'>مساحة جاهزة لأي محتوى إضافي أو إحصائيات سريعة عن السوق.</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        dev = st.session_state.selected_dev
        projects = df[df.iloc[:, 0] == dev]
        if st.button("🔙 عودة للقائمة"): st.session_state.page = 'main'; st.rerun()
        st.markdown(f"<h2 style='color:#3b82f6;'>🏢 {dev}</h2>", unsafe_allow_html=True)
        for _, row in projects.iterrows():
            with st.expander(f"📍 {row[2]} - {row[4]}"):
                st.write(f"**الموقع:** {row[3]} | **نظام السداد:** مقدم {row[10]} | {row[9]} سنوات")
                st.error(f"**💡 الزتونة الفنية:** {row[11]}")
