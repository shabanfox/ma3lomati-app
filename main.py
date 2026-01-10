import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (تثبيت حجم الكروت وتوحيدها)
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
    .hero-banner h1 { font-weight: 900; color: #f59e0b !important; margin: 0; }

    /* تثبيت حجم كارت المطور (غير متوافق مع طول الاسم لضمان التناسق) */
    div.stButton > button[key^="dev_btn_"] {
        height: 160px !important; /* حجم ثابت وموحد لكل الكروت */
        width: 100% !important;
        background-color: #ffffff !important;
        border: 5px solid #000 !important;
        border-radius: 25px !important;
        box-shadow: 10px 10px 0px #000 !important;
        font-size: 1.6rem !important;
        font-weight: 900 !important;
        color: #000 !important;
        transition: 0.2s;
        white-space: normal !important; /* السماح للاسم بالنزول لسطر جديد لو طويل */
        line-height: 1.2 !important;
    }
    div.stButton > button[key^="dev_btn_"]:hover {
        transform: translate(-3px, -3px);
        box-shadow: 13px 13px 0px #f59e0b !important;
        border-color: #f59e0b !important;
    }

    /* كروت المشاريع في الصفحة الداخلية */
    .project-card {
        background: #ffffff; border: 3px solid #000; padding: 15px;
        border-radius: 15px; margin-bottom: 12px; box-shadow: 6px 6px 0px #000;
        font-weight: 900; font-size: 1.3rem;
    }

    /* أزرار العودة والتحكم */
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 12px !important;
        box-shadow: 5px 5px 0px #000 !important; font-weight: 700 !important;
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
# تحديد الأعمدة بناءً على وصفك (Developer)
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
    
    col_main, _ = st.columns([0.7, 0.3]) # حصر العرض في 70%
    
    with col_main:
        if st.button("🔙 عودة للرئيسية"): 
            st.session_state.view = 'main'; st.rerun()
        
        search = st.text_input("🔍 ابحث عن المطور...")
        unique_devs = df[dev_col].dropna().unique()
        
        if search:
            unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]
        
        items_per_page = 9
        start_idx = st.session_state.page * items_per_page
        current_devs = unique_devs[start_idx : start_idx + items_per_page]

        # شبكة المطورين 3x3 بحجم كروت ثابت
        for i in range(0, len(current_devs), 3):
            grid_cols = st.columns(3)
            for j in range(3):
                if i + j < len(current_devs):
                    dev_name = current_devs[i + j]
                    with grid_cols[j]:
                        if st.button(dev_name, key=f"dev_btn_{dev_name}"):
                            st.session_state.selected_dev = dev_name
                            st.session_state.view = 'dev_details'
                            st.rerun()

        # أزرار التنقل
        st.write("<br>", unsafe_allow_html=True)
        n_prev, n_next = st.columns(2)
        with n_prev:
            if st.session_state.page > 0:
                if st.button("⬅️ السابق"): st.session_state.page -= 1; st.rerun()
        with n_next:
            if (start_idx + items_per_page) < len(unique_devs):
                if st.button("التالي ➡️"): st.session_state.page += 1; st.rerun()

elif st.session_state.view == 'dev_details':
    dev_name = st.session_state.selected_dev
    st.markdown(f'<div class="hero-banner"><h2>{dev_name}</h2></div>', unsafe_allow_html=True)
    
    col_det, _ = st.columns([0.7, 0.3])
    with col_det:
        if st.button("🔙 عودة للقائمة"): 
            st.session_state.view = 'comp'; st.rerun()
        
        st.write(f"### 🏗️ مشاريع المطور:")
        dev_projects = df[df[dev_col] == dev_name][proj_col].unique()
        
        for proj in dev_projects:
            st.markdown(f'<div class="project-card">🔹 {proj}</div>', unsafe_allow_html=True)

# (صفحة الأدوات تتبع نفس التنسيق في الكود الأصلي لديك)
