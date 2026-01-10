import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS الموحد (المشاريع والأدوات)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000;
    }
    .hero-banner h1, .hero-banner h2 { font-weight: 900; color: #f59e0b !important; margin: 0; }

    /* ستايل الكروت الموحد - حجم ثابت كبير */
    .custom-card {
        background: #ffffff; border: 4px solid #000; padding: 20px; 
        border-radius: 20px; margin-bottom: 10px; box-shadow: 8px 8px 0px #000;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        text-align: center; height: 200px; /* حجم ثابت */
    }
    .card-title { font-size: 1.5rem; font-weight: 900; color: #000; margin-bottom: 10px; }
    .card-val { font-size: 2.2rem; font-weight: 900; color: #f59e0b; margin-top: 10px; }

    /* زر التفاصيل داخل الكارت */
    div.stButton > button[key^="details_"] {
        background-color: #000 !important; color: #f59e0b !important;
        border: 2px solid #f59e0b !important; border-radius: 10px !important;
        font-size: 0.9rem !important; padding: 5px 15px !important;
        width: 100% !important;
    }

    /* زر العودة نانو أزرق */
    div.stButton > button[key^="back_"] {
        background-color: #007bff !important; color: white !important;
        font-size: 0.7rem !important; padding: 2px 8px !important;
        min-height: 25px !important; width: auto !important;
        border: none !important; border-radius: 5px !important;
        box-shadow: 2px 2px 0px #000 !important;
    }

    /* أزرار التنقل الرئيسية */
    div.stButton > button:not([key^="details_"]):not([key^="back_"]) {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 5px 5px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
    }
    
    input { border: 3px solid #000 !important; border-radius: 10px !important; }
    label { font-weight: 900 !important; }
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
    st.write("<div style='height:80px;'></div>", unsafe_allow_html=True)
    _, mid_col, _ = st.columns([0.1, 0.8, 0.1])
    with mid_col:
        c1, c2 = st.columns(2, gap="large")
        if c1.button("🏢\nدليل المطورين", use_container_width=True): st.session_state.view = 'comp'; st.rerun()
        if c2.button("🛠️\nأدوات البروكر", use_container_width=True): st.session_state.view = 'tools'; st.rerun()

# --- صفحة دليل المطورين ---
elif st.session_state.view == 'comp':
    st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
    col_main, _ = st.columns([0.7, 0.3])
    
    with col_main:
        if st.button("🔙 عودة", key="back_to_main"): st.session_state.view = 'main'; st.rerun()
        
        search = st.text_input("🔍 ابحث عن المطور...")
        unique_devs = df[target_col].dropna().unique()
        if search: unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]
        
        items_per_page = 9
        start_idx = st.session_state.page * items_per_page
        current_devs = unique_devs[start_idx : start_idx + items_per_page]

        for i in range(0, len(current_devs), 3):
            grid_cols = st.columns(3)
            for j in range(3):
                if i + j < len(current_devs):
                    dev_name = current_devs[i+j]
                    with grid_cols[j]:
                        # الكارت
                        st.markdown(f'<div class="custom-card"><div class="card-title">{dev_name}</div></div>', unsafe_allow_html=True)
                        # زر التفاصيل أسفل الكارت مباشرة
                        if st.button("عرض التفاصيل", key=f"details_{dev_name}"):
                            st.session_state.selected_dev = dev_name
                            st.session_state.view = 'details'; st.rerun()

        # أزرار التنقل
        st.write("<br>", unsafe_allow_html=True)
        n1, n2 = st.columns(2)
        if n1.button("⬅️ السابق") and st.session_state.page > 0: st.session_state.page -= 1; st.rerun()
        if n2.button("التالي ➡️") and (start_idx + items_per_page) < len(unique_devs): st.session_state.page += 1; st.rerun()

# --- صفحة التفاصيل ---
elif st.session_state.view == 'details':
    st.markdown(f'<div class="hero-banner"><h2>{st.session_state.selected_dev}</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة", key="back_to_comp"): st.session_state.view = 'comp'; st.rerun()
    
    projs = df[df[target_col] == st.session_state.selected_dev][proj_col].unique()
    for p in projs:
        st.markdown(f'<div class="custom-card" style="height:auto; min-height:60px; margin-bottom:10px;"><b>🔹 {p}</b></div>', unsafe_allow_html=True)

# --- صفحة الأدوات ---
elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة", key="back_main_tool"): st.session_state.view = 'main'; st.rerun()
    # (بقية كود الحاسبات كما هو في التصميم السابق)
