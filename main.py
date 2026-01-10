import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (التثبيت القسري للأحجام والترتيب)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء القوائم الافتراضية */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000;
    }

    /* الكروت: تثبيت هندسي مطلق (ارتفاع وعرض ثابت) */
    div.stButton > button[key^="dev_btn_"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        
        /* المقاس الموحد تماماً */
        height: 160px !important; 
        width: 100% !important;
        min-height: 160px !important;
        max-height: 160px !important;
        
        background-color: #ffffff !important;
        border: 5px solid #000000 !important;
        border-radius: 25px !important;
        box-shadow: 10px 10px 0px #000000 !important;
        
        font-size: 1.5rem !important;
        font-weight: 900 !important;
        color: #000000 !important;
        white-space: normal !important;
        transition: 0.2s;
    }

    div.stButton > button[key^="dev_btn_"]:hover {
        transform: translate(-3px, -3px);
        box-shadow: 13px 13px 0px #f59e0b !important;
        border-color: #f59e0b !important;
    }

    /* موازنة المسافات بين الأعمدة */
    [data-testid="column"] {
        padding: 0 10px !important;
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
    
    col_main, _ = st.columns([0.7, 0.3]) # حصر العرض في 70% كما طلبت
    
    with col_main:
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
        search = st.text_input("🔍 ابحث عن المطور (بحث سريع)...")
        
        unique_devs = df[dev_col].dropna().unique()
        if search:
            unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]
        
        items_per_page = 9
        start_idx = st.session_state.page * items_per_page
        current_devs = unique_devs[start_idx : start_idx + items_per_page]

        # --- ترتيب الكروت جنب بعضها في صفوف 3x3 ---
        for i in range(0, len(current_devs), 3):
            cols = st.columns(3) # إنشاء 3 أعمدة متساوية جنب بعض
            for j in range(3):
                if i + j < len(current_devs):
                    dev_name = current_devs[i + j]
                    with cols[j]:
                        if st.button(dev_name, key=f"dev_btn_{dev_name}"):
                            st.session_state.selected_dev = dev_name
                            st.session_state.view = 'dev_details'
                            st.rerun()

        # أزرار التنقل
        st.write("<br>", unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        with p1:
            if st.session_state.page > 0:
                if st.button("⬅️ السابق"): st.session_state.page -= 1; st.rerun()
        with p2:
            if (start_idx + items_per_page) < len(unique_devs):
                if st.button("التالي ➡️"): st.session_state.page += 1; st.rerun()

elif st.session_state.view == 'dev_details':
    # (صفحة المشاريع بنفس التنسيق المعتاد)
    st.markdown(f'<div class="hero-banner"><h2>{st.session_state.selected_dev}</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للقائمة"): st.session_state.view = 'comp'; st.rerun()
    # ... كود المشاريع ...
