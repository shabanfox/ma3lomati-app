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

    /* كروت الصفحة الرئيسية */
    .main-gate-card {
        background: white; border-radius: 20px; padding: 30px; text-align: center;
        border: 1px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        transition: 0.3s ease; height: 250px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; margin-bottom: 10px;
    }
    .main-gate-card:hover { transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
    .card-companies { border-top: 10px solid #001a33; }
    .card-tools { border-top: 10px solid #f59e0b; }
    .gate-icon { font-size: 3.5rem; margin-bottom: 10px; }
    .gate-title { font-size: 1.8rem; font-weight: 900; color: #001a33; }

    /* الهيدر الموحد لصفحة الشركات */
    .hero-section {
        background: linear-gradient(135deg, #001a33 0%, #1e3a8a 100%);
        padding: 25px; border-radius: 0 0 25px 25px;
        margin-bottom: 20px; color: white; box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }

    /* الكروت الصغيرة (9 كروت) */
    .premium-nano-card {
        background: #ffffff; border: 1px solid #cbd5e1; border-right: 6px solid #001a33;
        border-radius: 10px; padding: 12px; margin-bottom: 8px; min-height: 125px;
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .c-dev { color: #000000 !important; font-size: 1.15rem; font-weight: 900; line-height: 1.2; }
    .c-proj { color: #1d4ed8 !important; font-size: 0.95rem; font-weight: 700; }
    .c-price { color: #15803d !important; font-size: 1.25rem; font-weight: 900; }
    .c-meta { color: #475569; font-size: 0.85rem; font-weight: 600; background: #f1f5f9; padding: 2px 8px; border-radius: 5px; }

    /* أزرار التفاصيل */
    div.stButton > button {
        background: #001a33 !important; color: white !important;
        font-size: 0.8rem !important; height: 28px !important;
        border-radius: 6px !important; width: 100%; border: none !important;
        font-weight: 900 !important; margin-top: 5px !important;
    }

    /* تنسيق الفلاتر داخل الهيرو */
    label { color: white !important; font-weight: 700 !important; }
    </style>
""", unsafe_allow_html=True)

# دالة معالجة البيانات
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

# إدارة حالات التنقل
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'page_idx' not in st.session_state: st.session_state.page_idx = 0

if df is not None:
    # --- 1. الصفحة الرئيسية (البوابة) ---
    if st.session_state.view == 'main':
        st.markdown("<h1 style='text-align:center; color:#001a33; margin:40px 0; font-weight:900;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="main-gate-card card-companies"><div class="gate-icon">🏢</div><div class="gate-title">الشركات</div></div>', unsafe_allow_html=True)
            if st.button("فتح قسم الشركات", use_container_width=True):
                st.session_state.view = 'companies'
                st.rerun()
        with col2:
            st.markdown('<div class="main-gate-card card-tools"><div class="gate-icon">🛠️</div><div class="gate-title">أدوات البروكر</div></div>', unsafe_allow_html=True)
            if st.button("فتح أدوات البروكر", use_container_width=True):
                st.session_state.view = 'tools'
                st.rerun()

    # --- 2. صفحة الشركات (الفلاتر + 9 كروت) ---
    elif st.session_state.view == 'companies':
        st.markdown('<div class="hero-section">', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"):
            st.session_state.view = 'main'; st.rerun()
        
        st.markdown('<h2 style="text-align:center; margin-bottom:20px;">🔍 ابحث في الشركات والمشاريع</h2>', unsafe_allow_html=True)
        cf1, cf2, cf3 = st.columns([2, 1, 1])
        with cf1: sq = st.text_input("بحث بالاسم", placeholder="اكتب اسم المطور أو المشروع...", label_visibility="collapsed")
        with cf2: sa = st.selectbox("المنطقة", ["الكل"] + sorted(df.iloc[:, 3].dropna().unique().tolist()), label_visibility="collapsed")
        with cf3: sp = st.number_input("السعر الأقصى", value=0, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

        f_df = df.copy()
        if sq: f_df = f_df[f_df.iloc[:, 0].str.contains(sq, na=False, case=False) | f_df.iloc[:, 2].str.contains(sq, na=False, case=False)]
        if sa != "الكل": f_df = f_df[f_df.iloc[:, 3] == sa]
        if sp > 0: f_df = f_df[f_df['p_val'] <= sp]

        m_area, s_area = st.columns([3.3, 0.7])
        with m_area:
            items = 9
            total_p = math.ceil(len(f_df) / items)
            start = st.session_state.page_idx * items
            curr_items = f_df.iloc[start : start + items]

            for i in range(0, len(curr_items), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(curr_items):
                        row = curr_items.iloc[i + j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="premium-nano-card">
                                    <div><div class="c-dev">{row[0]}</div><div class="c-proj">🏢 {row[2]}</div></div>
                                    <div><div class="c-price">{row[4]}</div><div class="c-meta">📍 {row[3]}</div></div>
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
                if st.session_state.page_idx > 0 and st.button("⬅️ السابق"):
                    st.session_state.page_idx -= 1; st.rerun()
            with n2: st.markdown(f"<p style='text-align:center; font-weight:900;'>{st.session_state.page_idx+1} / {total_p}</p>", unsafe_allow_html=True)
            with n3:
                if st.session_state.page_idx < total_p - 1 and st.button("التالي ➡️"):
                    st.session_state.page_idx += 1; st.rerun()

    # --- 3. صفحة التفاصيل ---
    elif st.session_state.view == 'details':
        if st.button("🔙 عودة للشركات"):
            st.session_state.view = 'companies'; st.rerun()
        dev = st.session_state.selected_dev
        projs = df[df.iloc[:, 0] == dev]
        st.markdown(f"<h2 style='background:#001a33; color:white; padding:15px; border-radius:10px;'>🏢 {dev}</h2>", unsafe_allow_html=True)
        for _, r in projs.iterrows():
            with st.expander(f"📌 {r[2]} - {r[4]}", expanded=True):
                st.info(f"📍 الموقع: {r[3]} | 💳 المقدم: {r[10]}")
                st.error(f"💡 الزتونة الفنية:\n\n{r[11]}")

    # --- 4. صفحة أدوات البروكر ---
    elif st.session_state.view == 'tools':
        if st.button("🔙 عودة للرئيسية"):
            st.session_state.view = 'main'; st.rerun()
        st.title("🛠️ أدوات البروكر")
        st.write("هنا سيتم إضافة الحاسبات والنماذج لاحقاً.")
