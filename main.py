import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS احترافي للواجهة الرئيسية (الأزرار الكبيرة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header {visibility: hidden;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff;
    }

    /* هيدر المنصة */
    .main-banner { 
        background: #000; color: #f59e0b; padding: 30px; border-radius: 15px; 
        text-align: center; margin-bottom: 40px; border: 4px solid #f59e0b;
    }

    /* تنسيق الأزرار الكبيرة في الصفحة الرئيسية */
    div.stButton > button[key="btn_devs"], div.stButton > button[key="btn_tools"] {
        width: 100% !important;
        height: 250px !important;
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        border-radius: 25px !important;
        border: 4px solid #000 !important;
        transition: 0.3s;
        box-shadow: 10px 10px 0px #000 !important;
    }
    
    div.stButton > button[key="btn_devs"] { background-color: #f59e0b !important; color: #000 !important; }
    div.stButton > button[key="btn_tools"] { background-color: #000 !important; color: #f59e0b !important; }

    div.stButton > button:hover { transform: scale(1.02); box-shadow: 15px 15px 0px #f59e0b !important; }

    /* تنسيق كروت المطورين الصغيرة */
    div.stButton > button[key^="dev_grid_"] {
        width: 100% !important; height: 100px !important;
        background-color: white !important; border: 2px solid #000 !important;
        border-radius: 12px !important; font-weight: 800 !important;
        box-shadow: 4px 4px 0px #000 !important; margin-bottom: 10px;
    }

    .project-card { background: #f8f9fa; padding: 15px; border-radius: 10px; border-right: 5px solid #f59e0b; margin-bottom: 10px; font-weight: bold; }
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
    except: return pd.DataFrame()

df = load_data()

# إدارة التنقل (Navigation)
if 'main_page' not in st.session_state: st.session_state.main_page = "home"
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'page_num' not in st.session_state: st.session_state.page_num = 0

# --- الواجهة الرئيسية (الزرين الكبار) ---
if st.session_state.main_page == "home":
    st.markdown('<div class="main-banner"><h1>🚀 منصة معلوماتى العقارية الذكية</h1><p>اختر الوجهة المطلوبة للبدء</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        if st.button("🏢 الشركات (Developers)", key="btn_devs"):
            st.session_state.main_page = "devs_list"
            st.rerun()
            
    with col2:
        if st.button("🛠️ أدوات البروكر", key="btn_tools"):
            st.session_state.main_page = "tools_page"
            st.rerun()

# --- صفحة قائمة الشركات (Developers Grid) ---
elif st.session_state.main_page == "devs_list":
    if st.button("🔙 العودة للرئيسية"):
        st.session_state.main_page = "home"
        st.rerun()
    
    st.title("🏢 دليل المطورين (Developers)")
    search = st.text_input("🔍 ابحث عن مطور...")
    
    dev_col = df.columns[1]
    unique_devs = df[dev_col].dropna().unique()
    if search:
        unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

    # نظام الشبكة والصفحات
    items = 12
    start = st.session_state.page_num * items
    current_list = unique_devs[start:start+items]

    for i in range(0, len(current_list), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(current_list):
                name = current_list[i + j]
                with cols[j]:
                    if st.button(name, key=f"dev_grid_{name}"):
                        st.session_state.selected_dev = name
                        st.session_state.main_page = "dev_details"
                        st.rerun()
    
    # أزرار التنقل
    st.write("---")
    c1, c2, c3 = st.columns([1,2,1])
    if c1.button("⬅️ السابق") and st.session_state.page_num > 0:
        st.session_state.page_num -= 1; st.rerun()
    if c3.button("التالي ➡️") and (start + items) < len(unique_devs):
        st.session_state.page_num += 1; st.rerun()

# --- صفحة تفاصيل المطور ---
elif st.session_state.main_page == "dev_details":
    if st.button("🔙 العودة للقائمة"):
        st.session_state.main_page = "devs_list"
        st.rerun()
    
    dev = st.session_state.selected_dev
    st.header(f"🏢 مشاريع مطور: {dev}")
    
    proj_col = df.columns[0]
    dev_col = df.columns[1]
    projs = df[df[dev_col] == dev][proj_col].unique()
    
    p_cols = st.columns(2)
    for idx, p in enumerate(projs):
        with p_cols[idx % 2]:
            st.markdown(f'<div class="project-card">🔹 {p}</div>', unsafe_allow_html=True)

# --- صفحة أدوات البروكر ---
elif st.session_state.main_page == "tools_page":
    if st.button("🔙 العودة للرئيسية"):
        st.session_state.main_page = "home"
        st.rerun()
        
    st.title("🛠️ أدوات البروكر العقاري")
    st.info("حاسبة الأقساط والعوائد الاستثمارية قيد التشغيل...")
    # هنا تضع كود الحاسبات كما في النسخ السابقة
    p = st.number_input("سعر الوحدة", 1000000)
    y = st.slider("السنوات", 1, 15, 8)
    st.metric("القسط الشهري التقريبي", f"{(p/(y*12)):,.0f} ج.م")
