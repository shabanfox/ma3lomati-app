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

    /* كارت "شركات" الرئيسي - فخم جداً */
    .folder-card {
        background: white;
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        border: 1px solid #e2e8f0;
        border-top: 10px solid #001a33;
        box-shadow: 0 15px 35px rgba(0,0,0,0.05);
        cursor: pointer;
        transition: 0.3s ease;
        margin: 5% auto;
        max-width: 400px;
    }
    .folder-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.1);
        border-top-color: #1e40af;
    }
    .folder-icon { font-size: 4rem; margin-bottom: 20px; }
    .folder-title { font-size: 2rem; font-weight: 900; color: #001a33; }
    .folder-desc { color: #64748b; font-size: 1rem; margin-top: 10px; }

    /* الهيدر الموحد داخل صفحة الشركات */
    .hero-section {
        background: linear-gradient(135deg, #001a33 0%, #1e3a8a 100%);
        padding: 25px; border-radius: 0 0 20px 20px;
        margin-bottom: 20px; color: white; box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }

    /* الكروت الصغيرة */
    .nano-card {
        background: white; border: 1px solid #cbd5e1; border-right: 6px solid #001a33;
        border-radius: 10px; padding: 12px; margin-bottom: 8px; min-height: 115px;
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .c-dev { color: #000; font-size: 1.1rem; font-weight: 900; }
    .c-proj { color: #1e40af; font-size: 0.9rem; font-weight: 700; }
    .c-price { color: #15803d; font-size: 1.1rem; font-weight: 900; }
    
    /* زر التفاصيل الميكرو */
    div.stButton > button {
        background: #001a33 !important; color: white !important;
        font-size: 0.75rem !important; height: 24px !important;
        border-radius: 4px !important; width: 100%; font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# وظائف البيانات
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

# إدارة حالة العرض
if 'view_state' not in st.session_state: st.session_state.view_state = 'landing'
if 'page_num' not in st.session_state: st.session_state.page_num = 0

if df is not None:
    # --- الصفحة الأولى: كارت الشركات الرئيسي ---
    if st.session_state.view_state == 'landing':
        st.markdown("<h1 style='text-align:center; color:#001a33; margin-top:50px; font-weight:900;'>🏠 منصة معلوماتى</h1>", unsafe_allow_html=True)
        
        # كارت "شركات" الكبير
        st.markdown("""
            <div class="folder-card">
                <div class="folder-icon">🏢</div>
                <div class="folder-title">الشركات</div>
                <div class="folder-desc">استعرض كافة المطورين العقاريين والمشاريع المتاحة</div>
            </div>
        """, unsafe_allow_html=True)
        
        # جعل الكارت يعمل كزر
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            if st.button("فتح قسم الشركات", use_container_width=True):
                st.session_state.view_state = 'browse'
                st.rerun()

    # --- الصفحة الثانية: عرض كل الشركات (الـ 9 كروت) ---
    elif st.session_state.view_state == 'browse':
        # الهيدر الموحد
        st.markdown('<div class="hero-section">', unsafe_allow_html=True)
        col_back, col_title = st.columns([0.5, 3.5])
        with col_back:
            if st.button("🔙 رجوع"):
                st.session_state.view_state = 'landing'
                st.rerun()
        with col_title:
            st.markdown('<h2 style="margin:0; text-align:center;">🔍 دليل الشركات العقارية</h2>', unsafe_allow_html=True)
        
        # سطر الفلاتر
        st.markdown("<br>", unsafe_allow_html=True)
        f1, f2, f3 = st.columns([2, 1, 1])
        with f1: sq = st.text_input("بحث بالاسم", placeholder="اكتب اسم الشركة...", label_visibility="collapsed")
        with f2: sa = st.selectbox("المنطقة", ["الكل"] + sorted(df.iloc[:, 3].dropna().unique().tolist()), label_visibility="collapsed")
        with f3: sp = st.number_input("أقصى سعر", value=0, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        # فلترة وعرض
        f_df = df.copy()
        if sq: f_df = f_df[f_df.iloc[:, 0].str.contains(sq, na=False, case=False) | f_df.iloc[:, 2].str.contains(sq, na=False, case=False)]
        if sa != "الكل": f_df = f_df[f_df.iloc[:, 3] == sa]
        if sp > 0: f_df = f_df[f_df['p_val'] <= sp]

        m_col, s_col = st.columns([3.3, 0.7])
        with m_col:
            items = 9
            total_pages = math.ceil(len(f_df) / items)
            start_idx = st.session_state.page_num * items
            current_batch = f_df.iloc[start_idx : start_idx + items]

            for i in range(0, len(current_batch), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_batch):
                        row = current_batch.iloc[i + j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="nano-card">
                                    <div>
                                        <div class="c-dev">{row[0]}</div>
                                        <div class="c-proj">🏢 {row[2]}</div>
                                    </div>
                                    <div>
                                        <div class="c-price">{row[4]}</div>
                                        <div style="font-size:0.8rem; color:#64748b;">📍 {row[3]} | 💳 مقدم {row[10]}</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button("تفاصيل", key=f"det_{start_idx+i+j}"):
                                st.session_state.selected_dev = row[0]
                                st.session_state.view_state = 'details'
                                st.rerun()

            # أزرار التنقل
            st.markdown("<br>", unsafe_allow_html=True)
            n1, n2, n3 = st.columns([1,1,1])
            with n1: 
                if st.session_state.page_num > 0 and st.button("⬅️ السابق"):
                    st.session_state.page_num -= 1; st.rerun()
            with n2: st.markdown(f"<p style='text-align:center; font-weight:900;'>{st.session_state.page_num+1} / {total_pages}</p>", unsafe_allow_html=True)
            with n3:
                if st.session_state.page_num < total_pages - 1 and st.button("التالي ➡️"):
                    st.session_state.page_num += 1; st.rerun()

    # --- الصفحة الثالثة: التفاصيل الفنية ---
    elif st.session_state.view_state == 'details':
        if st.button("🔙 عودة للشركات"):
            st.session_state.view_state = 'browse'
            st.rerun()
        dev = st.session_state.selected_dev
        projs = df[df.iloc[:, 0] == dev]
        st.markdown(f"<h2 style='background:#001a33; color:white; padding:15px; border-radius:10px;'>🏢 {dev}</h2>", unsafe_allow_html=True)
        for _, r in projs.iterrows():
            with st.expander(f"📌 {r[2]} - {r[4]}", expanded=True):
                st.info(f"📍 الموقع: {r[3]} | 💳 المقدم: {row[10]}")
                st.error(f"💡 الزتونة الفنية:\n\n{r[11]}")
