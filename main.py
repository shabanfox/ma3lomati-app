import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (هندسة الكروت الثابتة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* الهيدر الملكي */
    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000;
    }

    /* الكروت: إجبار المقاس الثابت (مربع 1:1 أو مستطيل محدد) */
    div.stButton > button[key^="dev_btn_"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        
        /* المقاسات القسرية */
        height: 180px !important; 
        min-height: 180px !important;
        max-height: 180px !important;
        width: 100% !important;
        
        background-color: #ffffff !important;
        border: 5px solid #000000 !important;
        border-radius: 25px !important;
        box-shadow: 10px 10px 0px #000000 !important;
        
        font-size: 1.4rem !important;
        font-weight: 900 !important;
        color: #000000 !important;
        white-space: normal !important; /* للسماح بالالتفاف داخل المربع الثابت */
        overflow: hidden !important;
        transition: 0.2s;
        padding: 15px !important;
    }

    div.stButton > button[key^="dev_btn_"]:hover {
        transform: translate(-3px, -3px);
        box-shadow: 13px 13px 0px #f59e0b !important;
        border-color: #f59e0b !important;
    }

    /* تحسين شكل الشبكة لمنع الفراغات */
    [data-testid="column"] {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
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
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None

df = st.session_state.data
dev_col = 'Developer' if 'Developer' in df.columns else df.columns[1]
proj_col = df.columns[0]

# --- منطق العرض ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    st.write("<div style='height:60px;'></div>", unsafe_allow_html=True)
    _, mid_col, _ = st.columns([0.1, 0.8, 0.1])
    with mid_col:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            if st.button("🏢\nدليل المطورين", use_container_width=True, key="m1"): 
                st.session_state.view = 'comp'; st.rerun()
        with c2:
            if st.button("🛠️\nأدوات البروكر", use_container_width=True, key="m2"): 
                st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'comp':
    st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
    col_main, _ = st.columns([0.7, 0.3]) 
    
    with col_main:
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
        search = st.text_input("🔍 ابحث عن المطور...")
        unique_devs = df[dev_col].dropna().unique()
        if search:
            unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]
        
        items_per_page = 9
        start_idx = st.session_state.page * items_per_page
        current_devs = unique_devs[start_idx : start_idx + items_per_page]

        # الشبكة 3x3
        for i in range(0, len(current_devs), 3):
            grid_cols = st.columns(3)
            for j in range(3):
                if i + j < len(current_devs):
                    name = current_devs[i + j]
                    with grid_cols[j]:
                        # الزر الآن يمتثل لقواعد الطول الثابت 180px
                        if st.button(str(name), key=f"dev_btn_{name}"):
                            st.session_state.selected_dev = name
                            st.session_state.view = 'dev_details'
                            st.rerun()
        
        # أزرار التنقل ممركزة
        st.write("<br>", unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1:
            if st.session_state.page > 0:
                if st.button("⬅️ السابق"): st.session_state.page -= 1; st.rerun()
        with p2:
            if (start_idx + items_per_page) < len(unique_devs):
                if st.button("التالي ➡️"): st.session_state.page += 1; st.rerun()

elif st.session_state.view == 'dev_details':
    dev_name = st.session_state.selected_dev
    st.markdown(f'<div class="hero-banner"><h2>{dev_name}</h2></div>', unsafe_allow_html=True)
    col_det, _ = st.columns([0.7, 0.3])
    with col_det:
        if st.button("🔙 عودة للقائمة"): st.session_state.view = 'comp'; st.rerun()
        st.write("### 🏗️ المشاريع:")
        dev_projects = df[df[dev_col] == dev_name][proj_col].unique()
        for proj in dev_projects:
            st.markdown(f'<div style="background:#fff; border:3px solid #000; padding:15px; border-radius:15px; margin-bottom:12px; box-shadow:6px 6px 0px #000; font-weight:900;">🔹 {proj}</div>', unsafe_allow_html=True)
