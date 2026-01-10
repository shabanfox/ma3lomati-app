import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# تصميم CSS (إضافة مساحات وتنسيق الأزرار)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }
    .hero-banner { 
        background: #000; color: #f59e0b; padding: 20px; border-radius: 15px; 
        text-align: center; margin-bottom: 25px; border: 3px solid #f59e0b;
    }
    .custom-card {
        background: #ffffff; border: 3px solid #000; padding: 15px; 
        border-radius: 15px; margin-bottom: 15px; box-shadow: 6px 6px 0px #000;
    }
    .card-title { font-size: 1.5rem; font-weight: 900; color: #f59e0b; border-bottom: 2px solid #000; margin-bottom: 10px; }
    
    /* أزرار المطورين */
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 12px !important;
        box-shadow: 4px 4px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
        min-height: 60px !important; width: 100% !important;
    }
    div.stButton > button:hover { background-color: #f59e0b !important; color: #fff !important; }
    
    /* تنسيق أزرار التالي والسابق */
    .nav-btn button { background-color: #000 !important; color: #fff !important; }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات
@st.cache_data(ttl=300)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame(columns=['Developer'])

# تهيئة الحالة
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'page' not in st.session_state: st.session_state.page = 0

df = load_data()

# --- الصفحة الرئيسية ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى العقارية</h1></div>', unsafe_allow_html=True)
    col1, col2, empty_space = st.columns([1, 1, 1]) # جعل اليمين للأزرار واليسار فارغ
    with col1:
        if st.button("🏢 دليل المطورين", use_container_width=True): 
            st.session_state.view = 'comp'; st.rerun()
    with col2:
        if st.button("🛠️ أدوات البروكر", use_container_width=True): 
            st.session_state.view = 'tools'; st.rerun()

# --- صفحة دليل المطورين ---
elif st.session_state.view == 'comp':
    if st.session_state.selected_dev:
        # عرض تفاصيل الشركة (نفس الكود السابق)
        row = df[df['Developer'] == st.session_state.selected_dev].iloc[0]
        st.markdown(f'<div class="hero-banner"><h2>{row["Developer"]}</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للقائمة"): st.session_state.selected_dev = None; st.rerun()
        
        c_right, c_left = st.columns([2, 1]) # ترك مساحة يسار
        with c_right:
            st.markdown(f"""
                <div class="custom-card">
                    <div class="card-title">👤 المالك: {row.get('Owner','-')}</div>
                    <p>{row.get('Description','-')}</p>
                    <hr>
                    <p><b>المشاريع:</b> {row.get('Projects','-')}</p>
                    <p><b>التفاصيل:</b> {row.get('Detailed_Info','-')}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
        
        # تقسيم الصفحة: 70% للبيانات و 30% يسار فارغ كما طلبت
        col_main, col_empty = st.columns([0.7, 0.3])
        
        with col_main:
            if st.button("🏠 الرئيسية"): st.session_state.view = 'main'; st.session_state.page = 0; st.rerun()
            
            search = st.text_input("🔍 ابحث عن مطور...")
            dev_list = df['Developer'].unique()
            if search:
                dev_list = [d for d in dev_list if search.lower() in str(d).lower()]
            
            # --- نظام الـ 3×3 (9 شركات في الصفحة) ---
            limit = 9
            start = st.session_state.page * limit
            end = start + limit
            current_batch = dev_list[start:end]
            
            # عرض الأزرار في 3 أعمدة
            for i in range(0, len(current_batch), 3):
                grid = st.columns(3)
                for j in range(3):
                    if i + j < len(current_batch):
                        dev_name = current_batch[i+j]
                        if grid[j].button(dev_name, key=f"btn_{dev_name}"):
                            st.session_state.selected_dev = dev_name
                            st.rerun()
            
            # --- أزرار التنقل (السابق والتالي) ---
            st.write("---")
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            with nav1:
                if st.session_state.page > 0:
                    if st.button("⬅️ السابق"):
                        st.session_state.page -= 1
                        st.rerun()
            with nav3:
                if end < len(dev_list):
                    if st.button("التالي ➡️"):
                        st.session_state.page += 1
                        st.rerun()
            with nav2:
                st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.page + 1}</p>", unsafe_allow_html=True)

# --- صفحة الأدوات ---
elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر</h2></div>', unsafe_allow_html=True)
    if st.button("🏠 الرئيسية"): st.session_state.view = 'main'; st.rerun()
    st.info("جاري العمل على الحاسبات...")
