import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS المدمج (الكارت هو الزر)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* هيدر مصغر */
    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 15px; border-radius: 15px; 
        text-align: center; margin-bottom: 20px; border: 3px solid #f59e0b;
        box-shadow: 6px 6px 0px #000;
    }
    .hero-banner h1 { font-size: 1.8rem !important; font-weight: 900; margin: 0; }

    /* دمج الكارت مع الزر - تحويل زر المطور لمربع كبير متساوٍ */
    div.stButton > button[key^="dev_"] {
        width: 100% !important;
        height: 145px !important; /* الحجم المصغر */
        background-color: #ffffff !important;
        border: 4px solid #000000 !important;
        border-radius: 15px !important;
        box-shadow: 6px 6px 0px #000000 !important;
        font-size: 1.2rem !important;
        font-weight: 900 !important;
        color: #000 !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        white-space: normal !important;
        line-height: 1.3 !important;
        transition: 0.2s !important;
    }

    div.stButton > button[key^="dev_"]:hover {
        transform: translate(-3px, -3px) !important;
        box-shadow: 9px 9px 0px #f59e0b !important;
        border-color: #f59e0b !important;
        color: #f59e0b !important;
    }

    /* زر العودة نانو أزرق */
    div.stButton > button[key^="back_"] {
        background-color: #007bff !important; color: white !important;
        font-size: 0.65rem !important; padding: 2px 6px !important;
        min-height: 22px !important; width: auto !important;
        border: none !important; border-radius: 4px !important;
        box-shadow: 2px 2px 0px #000 !important;
        margin-bottom: 10px !important;
    }

    /* أزرار الصفحة الرئيسية */
    div.stButton > button:not([key^="dev_"]):not([key^="back_"]) {
        border: 4px solid #000 !important; border-radius: 15px !important;
        box-shadow: 5px 5px 0px #000 !important; font-weight: 900 !important;
        height: 120px !important; font-size: 1.2rem !important;
    }

    /* كروت عرض النتائج في الأدوات */
    .tool-result-box {
        background: #fff; border: 3px solid #000; padding: 10px;
        border-radius: 15px; box-shadow: 5px 5px 0px #000;
        text-align: center; margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame(columns=['Developer', 'Project'])

if 'data' not in st.session_state: st.session_state.data = load_data()
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'page' not in st.session_state: st.session_state.page = 0

df = st.session_state.data
target_col = 'Developer' if 'Developer' in df.columns else df.columns[1]
proj_col = df.columns[0]

# --- الصفحة الرئيسية ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    _, mid_col, _ = st.columns([0.15, 0.7, 0.15])
    with mid_col:
        c1, c2 = st.columns(2, gap="medium")
        if c1.button("🏢\nدليل المطورين"): st.session_state.view = 'comp'; st.rerun()
        if c2.button("🛠️\nأدوات البروكر"): st.session_state.view = 'tools'; st.rerun()

# --- صفحة دليل المطورين (الكارت هو الزر) ---
elif st.session_state.view == 'comp':
    st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
    col_main, _ = st.columns([0.7, 0.3])
    
    with col_main:
        if st.button("🔙 عودة نانو", key="back_to_main"): st.session_state.view = 'main'; st.rerun()
        search = st.text_input("🔍 ابحث عن المطور...")
        
        unique_devs = df[target_col].dropna().unique()
        if search: unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]
        
        items = 9
        start = st.session_state.page * items
        current = unique_devs[start : start + items]

        # عرض الكروت كأزرار مدمجة
        for i in range(0, len(current), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(current):
                    name = current[i + j]
                    with cols[j]:
                        if st.button(name, key=f"dev_{name}"):
                            st.session_state.selected_dev = name
                            st.session_state.view = 'details'; st.rerun()

        # أزرار التنقل
        st.write("<br>", unsafe_allow_html=True)
        n1, n2 = st.columns(2)
        if n1.button("⬅️ السابق", key="back_p") and st.session_state.page > 0: st.session_state.page -= 1; st.rerun()
        if n2.button("التالي ➡️", key="next_p") and (start + items) < len(unique_devs): st.session_state.page += 1; st.rerun()

# --- صفحة التفاصيل ---
elif st.session_state.view == 'details':
    st.markdown(f'<div class="hero-banner"><h2>{st.session_state.selected_dev}</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة نانو", key="back_to_comp"): st.session_state.view = 'comp'; st.rerun()
    
    projs = df[df[target_col] == st.session_state.selected_dev][proj_col].unique()
    for p in projs:
        st.markdown(f'<div class="tool-result-box"><b>🔹 {p}</b></div>', unsafe_allow_html=True)
