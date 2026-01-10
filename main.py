import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (نفس ألوان وشكل الصورة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    @import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #1a1a1a; /* خلفية داكنة مثل الصورة */
    }

    /* الهيدر العلوي */
    .main-header {
        background: #000; color: #f59e0b; padding: 15px; text-align: center;
        border-bottom: 4px solid #f59e0b; font-weight: 900; font-size: 2rem;
    }

    /* تصميم الكروت (الأزرار) */
    div.stButton > button {
        width: 100% !important; 
        height: 220px !important; /* طول الكارت مثل الصورة */
        border: none !important;
        border-radius: 15px !important; /* حواف دائرية */
        margin: 5px !important;
        transition: 0.3s;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3) !important;
    }

    /* توزيع الألوان بالتبادل (أبيض وأصفر) */
    /* الكروت الفردية باللون الأبيض */
    div.stButton > button[key*="ev_0"], div.stButton > button[key*="ev_2"], 
    div.stButton > button[key*="ev_4"], div.stButton > button[key*="ev_6"] {
        background-color: #ffffff !important; color: #000 !important;
    }
    /* الكروت الزوجية باللون الأصفر */
    div.stButton > button[key*="ev_1"], div.stButton > button[key*="ev_3"], 
    div.stButton > button[key*="ev_5"], div.stButton > button[key*="ev_7"] {
        background-color: #f59e0b !important; color: #000 !important;
    }

    div.stButton > button:hover {
        transform: translateY(-10px) !important;
        filter: brightness(1.1);
    }

    /* تنسيق النص داخل الكارت */
    .dev-label { font-size: 1.4rem !important; font-weight: 900 !important; margin-top: 10px; }
    .dev-icon { font-size: 3rem !important; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    df = pd.read_csv(url)
    df.columns = [str(c).strip() for c in df.columns]
    return df

df = load_data()
dev_col = 'Developer' if 'Developer' in df.columns else df.columns[1]

if 'view' not in st.session_state: st.session_state.view = 'home'
if 'page' not in st.session_state: st.session_state.page = 0

# --- التطبيق ---

if st.session_state.view == 'home':
    st.markdown('<div class="main-header">🏠 منصة معلوماتى العقارية</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢\nدليل المطورين"): st.session_state.view = 'companies'; st.rerun()
    with c2:
        if st.button("🛠️\nأدوات البروكر"): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'companies':
    st.markdown(f'<div class="main-header">🏢 دليل المطورين</div>', unsafe_allow_html=True)
    
    # البحث
    if st.button("🔙 عودة"): st.session_state.view = 'home'; st.rerun()
    search = st.text_input("", placeholder="🔍 ابحث عن مطور...")

    # فلترة
    unique_devs = df[dev_col].unique()
    if search:
        unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

    # الشبكة (4 أعمدة كما في الصورة)
    col_grid, col_empty = st.columns([0.8, 0.2]) # مساحة أكبر للشبكة

    with col_grid:
        items = 8
        start = st.session_state.page * items
        current_batch = unique_devs[start : start + items]

        # رسم الشبكة
        for i in range(0, len(current_batch), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(current_batch):
                    dev_name = current_batch[i + j]
                    with cols[j]:
                        # محاكاة اللوجو بأيقونة عشوائية بناءً على الحرف الأول
                        icon = "bi-building" if (i+j) % 2 == 0 else "bi-house-heart"
                        # كتابة النص بشكل HTML داخل الزر
                        btn_label = f"{dev_name}"
                        if st.button(btn_label, key=f"dev_{start+i+j}"):
                            st.sidebar.success(f"مطور: {dev_name}")

        # التنقل
        n1, n2, n3 = st.columns([1,1,1])
        if n1.button("⬅️ السابق") and st.session_state.page > 0:
            st.session_state.page -= 1; st.rerun()
        if n3.button("التالي ➡️") and (start + items) < len(unique_devs):
            st.session_state.page += 1; st.rerun()
