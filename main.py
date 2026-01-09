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

    /* الكارت الترحيبي الكبير */
    .landing-card {
        background: linear-gradient(135deg, #001a33 0%, #1e3a8a 100%);
        color: white; padding: 60px; border-radius: 30px;
        text-align: center; margin: 10% auto; max-width: 800px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        border: 2px solid rgba(255,255,255,0.1);
    }
    .landing-title { font-size: 3rem; font-weight: 900; margin-bottom: 20px; }
    .landing-subtitle { font-size: 1.2rem; opacity: 0.9; margin-bottom: 30px; }

    /* الهيدر الموحد داخل المنصة */
    .hero-section {
        background: linear-gradient(135deg, #001a33 0%, #1e3a8a 100%);
        padding: 20px; border-radius: 0 0 20px 20px;
        margin-bottom: 20px; color: white; box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }

    /* الكروت الصغيرة المطورة */
    .premium-nano-card {
        background: white; border: 1px solid #cbd5e1; border-right: 6px solid #001a33;
        border-radius: 10px; padding: 12px; margin-bottom: 8px; min-height: 120px;
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .c-dev { color: #000; font-size: 1.1rem; font-weight: 900; }
    .c-proj { color: #1d4ed8; font-size: 0.9rem; font-weight: 700; }
    .c-price { color: #15803d; font-size: 1.1rem; font-weight: 900; }
    </style>
""", unsafe_allow_html=True)

# دالة استخراج الأرقام وتحميل البيانات
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

# إدارة التنقل بين الصفحات
if 'view' not in st.session_state: st.session_state.view = 'landing'
if 'curr_p' not in st.session_state: st.session_state.curr_p = 0

if df is not None:
    # --- 1. الصفحة الترحيبية (الكارت الكبير) ---
    if st.session_state.view == 'landing':
        st.markdown(f"""
            <div class="landing-card">
                <div class="landing-title">🏠 منصة معلوماتى العقارية</div>
                <div class="landing-subtitle">دليلك الشامل لأكبر المطورين والمشاريع العقارية في مصر.<br>كل البيانات والتحليلات الفنية في مكان واحد.</div>
            </div>
        """, unsafe_allow_html=True)
        
        c_left, c_mid, c_right = st.columns([1,1,1])
        with c_mid:
            if st.button("🚀 استعراض كافة الشركات والمشاريع", use_container_width=True):
                st.session_state.view = 'main_app'
                st.rerun()

    # --- 2. لوحة التحكم الرئيسية (قاعدة البيانات) ---
    elif st.session_state.view == 'main_app':
        # الهيدر والفلاتر قطعة واحدة
        st.markdown('<div class="hero-section">', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align:center; margin:0 0 15px 0;">🔍 ابحث في قاعدة البيانات</h2>', unsafe_allow_html=True)
        col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
        with col_f1: sq = st.text_input("المطور أو المشروع", placeholder="اكتب للبحث...", label_visibility="collapsed")
        with col_f2: sa = st.selectbox("المنطقة", ["الكل"] + sorted(df.iloc[:, 3].dropna().unique().tolist()), label_visibility="collapsed")
        with col_f3: sp = st.number_input("أقصى سعر", value=0, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        # زر العودة للكارت الكبير
        if st.sidebar.button("🔙 العودة للرئيسية"):
            st.session_state.view = 'landing'
            st.rerun()

        # توزيع المحتوى (9 كروت)
        f_df = df.copy()
        if sq: f_df = f_df[f_df.iloc[:, 0].str.contains(sq, na=False, case=False) | f_df.iloc[:, 2].str.contains(sq, na=False, case=False)]
        if sa != "الكل": f_df = f_df[f_df.iloc[:, 3] == sa]
        if sp > 0: f_df = f_df[f_df['p_val'] <= sp]

        m_area, s_area = st.columns([3.3, 0.7])
        with m_area:
            items, total = 9, math.ceil(len(f_df) / 9)
            start = st.session_state.curr_p * items
            curr_items = f_df.iloc[start : start + items]

            for i in range(0, len(curr_items), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(curr_items):
                        row = curr_items.iloc[i + j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="premium-nano-card">
                                    <div>
                                        <div class="c-dev">{row[0]}</div>
                                        <div class="c-proj">🏢 {row[2]}</div>
                                    </div>
                                    <div>
                                        <div class="c-price">{row[4]}</div>
                                        <div class="c-meta" style="font-size:0.8rem; background:#f1f5f9; padding:2px 5px; border-radius:4px;">📍 {row[3]}</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button("التفاصيل", key=f"btn_{start+i+j}"):
                                st.session_state.selected_dev = row[0]
                                st.session_state.view = 'details'
                                st.rerun()

            # أزرار التنقل
            st.markdown("<br>", unsafe_allow_html=True)
            n1, n2, n3 = st.columns([1,1,1])
            with n1: 
                if st.session_state.curr_p > 0 and st.button("⬅️ السابق"):
                    st.session_state.curr_p -= 1; st.rerun()
            with n2: st.markdown(f"<p style='text-align:center; font-weight:900;'>{st.session_state.curr_p+1} / {total}</p>", unsafe_allow_html=True)
            with n3:
                if st.session_state.curr_p < total - 1 and st.button("التالي ➡️"):
                    st.session_state.curr_p += 1; st.rerun()

    # --- 3. صفحة التفاصيل ---
    elif st.session_state.view == 'details':
        if st.button("🔙 عودة للنتائج"):
            st.session_state.view = 'main_app'
            st.rerun()
        dev = st.session_state.selected_dev
        projs = df[df.iloc[:, 0] == dev]
        st.markdown(f"<h2 style='background:#001a33; color:white; padding:15px; border-radius:10px;'>🏢 {dev}</h2>", unsafe_allow_html=True)
        for _, r in projs.iterrows():
            with st.expander(f"📌 {r[2]} - {r[4]}", expanded=True):
                st.success(f"📍 الموقع: {r[3]} | 💳 المقدم: {r[10]}")
                st.error(f"💡 الزتونة الفنية:\n\n{r[11]}")
