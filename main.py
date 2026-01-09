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

    /* تصميم الكارت الكبير جداً (زر الدخول) */
    .entry-portal {
        background: linear-gradient(135deg, #001a33 0%, #1e3a8a 100%);
        color: white; padding: 100px 40px; border-radius: 25px;
        text-align: center; margin: 50px auto; max-width: 900px;
        box-shadow: 0 30px 60px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.2);
        cursor: pointer; transition: 0.4s;
    }
    .entry-portal:hover { transform: scale(1.02); box-shadow: 0 40px 80px rgba(0,0,0,0.4); }
    
    .portal-title { font-size: 3.5rem; font-weight: 900; margin-bottom: 10px; }
    .portal-desc { font-size: 1.5rem; opacity: 0.8; margin-bottom: 40px; }

    /* الهيدر الموحد (بدون فواصل) */
    .hero-section {
        background: linear-gradient(135deg, #001a33 0%, #1e3a8a 100%);
        padding: 30px 20px; border-radius: 0 0 30px 30px;
        margin-bottom: 25px; color: white; box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }

    /* الكروت النانو المعتمدة */
    .nano-card {
        background: white; border: 1px solid #cbd5e1; border-right: 6px solid #001a33;
        border-radius: 12px; padding: 15px; margin-bottom: 10px; min-height: 125px;
        display: flex; flex-direction: column; justify-content: space-between;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .c-dev { color: #000; font-size: 1.2rem; font-weight: 900; }
    .c-proj { color: #1e40af; font-size: 1rem; font-weight: 700; }
    .c-price { color: #166534; font-size: 1.25rem; font-weight: 900; }
    
    /* تصغير زر التفاصيل */
    div.stButton > button {
        background: #001a33 !important; color: white !important;
        font-size: 0.8rem !important; height: 26px !important;
        border-radius: 5px !important; width: 100%; font-weight: 700 !important;
    }

    /* ستايل زر الدخول الضخم */
    .stButton > button.entry-btn {
        height: 80px !important; font-size: 1.8rem !important; 
        background: #ffffff !important; color: #001a33 !important;
        border-radius: 15px !important; border: none !important;
    }
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

# إدارة التنقل
if 'step' not in st.session_state: st.session_state.step = 'portal'
if 'curr_p' not in st.session_state: st.session_state.curr_p = 0

if df is not None:
    # --- المرحلة الأولى: كارت الدخول الكبير ---
    if st.session_state.step == 'portal':
        st.markdown("""
            <div class="entry-portal">
                <div class="portal-title">🏠 منصة معلوماتى العقارية</div>
                <div class="portal-desc">اضغط أدناه لاستكشاف قاعدة بيانات المطورين والمشاريع</div>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1, 1.5, 1])
        with c2:
            if st.button("🚀 دخول إلى دليل الشركات", key="main_entry", use_container_width=True, help="اضغط للدخول"):
                st.session_state.step = 'app'
                st.rerun()

    # --- المرحلة الثانية: قاعدة البيانات ---
    elif st.session_state.step == 'app':
        # الهيدر الموحد المتصل بالفلاتر
        st.markdown('<div class="hero-section">', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align:center; margin-bottom:20px;">🔍 ابحث في دليل الشركات</h1>', unsafe_allow_html=True)
        cf1, cf2, cf3 = st.columns([2, 1, 1])
        with cf1: sq = st.text_input("بحث بالاسم", placeholder="اكتب اسم المطور أو المشروع...", label_visibility="collapsed")
        with cf2: sa = st.selectbox("المنطقة", ["الكل"] + sorted(df.iloc[:, 3].dropna().unique().tolist()), label_visibility="collapsed")
        with cf3: sp = st.number_input("السعر الأقصى", value=0, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        # التصفية
        f_df = df.copy()
        if sq: f_df = f_df[f_df.iloc[:, 0].str.contains(sq, na=False, case=False) | f_df.iloc[:, 2].str.contains(sq, na=False, case=False)]
        if sa != "الكل": f_df = f_df[f_df.iloc[:, 3] == sa]
        if sp > 0: f_df = f_df[f_df['p_val'] <= sp]

        # عرض الكروت الـ 9
        m_area, s_area = st.columns([3.4, 0.6])
        with m_area:
            items = 9
            total_p = math.ceil(len(f_df) / items)
            start = st.session_state.curr_p * items
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
                                        <div class="c-dev">{row[0]}</div>
                                        <div class="c-proj">🏢 {row[2]}</div>
                                    </div>
                                    <div>
                                        <div class="c-price">{row[4]}</div>
                                        <div style="font-size:0.85rem; color:#64748b;">📍 {row[3]} | 💳 مقدم {row[10]}</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button("تفاصيل", key=f"d_{start+i+j}"):
                                st.session_state.selected_dev = row[0]
                                st.session_state.step = 'details'
                                st.rerun()

            # أزرار الصفحات
            st.markdown("<br>", unsafe_allow_html=True)
            n1, n2, n3 = st.columns([1,1,1])
            with n1: 
                if st.session_state.curr_p > 0 and st.button("السابق"):
                    st.session_p -= 1; st.rerun()
            with n2: st.markdown(f"<p style='text-align:center; font-weight:900;'>{st.session_state.curr_p+1} / {total_p}</p>", unsafe_allow_html=True)
            with n3:
                if st.session_state.curr_p < total_p - 1 and st.button("التالي"):
                    st.session_state.curr_p += 1; st.rerun()

    # --- المرحلة الثالثة: التفاصيل ---
    elif st.session_state.step == 'details':
        if st.button("🔙 عودة"): st.session_state.step = 'app'; st.rerun()
        dev = st.session_state.selected_dev
        projs = df[df.iloc[:, 0] == dev]
        st.markdown(f"<h2 style='color:#001a33;'>🏢 {dev}</h2>", unsafe_allow_html=True)
        for _, r in projs.iterrows():
            with st.expander(f"📌 {r[2]} - {r[4]}", expanded=True):
                st.info(f"📍 الموقع: {r[3]} | 💳 المقدم: {r[10]}")
                st.error(f"💡 الزتونة الفنية:\n\n{r[11]}")
