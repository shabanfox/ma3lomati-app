import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) المطور
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0rem !important;
        padding-left: 5% !important;
        padding-right: 5% !important;
    }

    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f0f4f8; 
    }

    /* هيدر احترافي بصورة عقارات */
    .hero-header {
        background-image: linear-gradient(to left, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.2)), 
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center;
        height: 130px;
        border-radius: 0 0 30px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 40px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin-bottom: 25px;
        position: relative;
    }

    /* اسم المنصة - أزرق وأقصى اليمين */
    .platform-name {
        color: #0044ff !important;
        font-size: 2rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 1px 1px 1px rgba(255,255,255,0.5);
    }

    /* تنسيق أزرار التنقل (أعلى اليسار) */
    .stButton > button {
        background-color: #001a33 !important;
        color: white !important;
        border-radius: 10px !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: bold !important;
        height: 40px !important;
        padding: 0 25px !important;
        border: 2px solid #0044ff !important;
        transition: 0.4s !important;
        margin-top: -65px; /* رفع الأزرار للأعلى */
    }

    .stButton > button:hover {
        background-color: #0044ff !important;
        box-shadow: 0 4px 15px rgba(0,68,255,0.4);
        transform: translateY(-3px);
    }

    /* كروت الشركات في الوسط */
    .dev-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #e2e8f0;
        border-right: 6px solid #0044ff;
        margin-bottom: 12px;
        transition: 0.3s;
    }
    .dev-card:hover { border-right-color: #001a33; box-shadow: 0 8px 15px rgba(0,0,0,0.05); }

    /* قائمة الكبار (الجانبية) */
    .sidebar-title {
        color: #001a33;
        font-weight: 900;
        font-size: 1.2rem;
        border-bottom: 3px solid #0044ff;
        padding-bottom: 8px;
        margin-bottom: 15px;
        text-align: center;
    }
    
    .top-company-btn div.stButton > button {
        background-color: white !important;
        color: #001a33 !important;
        border: 1px solid #e2e8f0 !important;
        text-align: right !important;
        margin-top: 0px !important; /* إلغاء الرفع للأزرار الجانبية */
        margin-bottom: 5px !important;
        height: 45px !important;
    }
    
    .top-company-btn div.stButton > button:hover {
        border-color: #0044ff !important;
        background-color: #f0f7ff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except: return None

df = load_data()

# 4. بناء الهيدر
st.markdown('<div class="hero-header"><div class="platform-name">منصة معلوماتى العقارية</div></div>', unsafe_allow_html=True)

# وضع الأزرار في أعلى اليسار
nav_col1, nav_col2, nav_empty = st.columns([1.2, 1.2, 5])
with nav_col1:
    if st.button("🏠 الرئيسية"):
        st.session_state.page = 'main'; st.session_state.search_query = ""; st.rerun()
with nav_col2:
    if st.button("👤 دخول"):
        st.toast("مرحباً بك.. نافذة الدخول قريباً")

# 5. إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'search_query' not in st.session_state: st.session_state.search_query = ""

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main' and df is not None:
    col_main, col_side = st.columns([2.3, 1])

    with col_main:
        # البحث بستايل أنيق
        st.markdown('<p style="font-weight:bold; color:#64748b; margin-bottom:0;">ابحث عن مطورك المفضل:</p>', unsafe_allow_html=True)
        st.session_state.search_query = st.text_input("", value=st.session_state.search_query, placeholder="اكتب اسم الشركة هنا...", label_visibility="collapsed")
        
        f_df = df.copy()
        if st.session_state.search_query:
            f_df = f_df[f_df['Developer'].astype(str).str.contains(st.session_state.search_query, case=False, na=False)]

        # عرض الكروت
        for idx, (i, row) in enumerate(f_df.head(8).reset_index().iterrows()):
            st.markdown(f"""
                <div class="dev-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="font-weight: 900; color: #001a33; font-size: 1.2rem;">{row['Developer']}</div>
                            <div style="color: #64748b; font-size: 0.9rem;">📍 {row['Area']}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"استكشاف مشروعات {row['Developer']}", key=f"main_btn_{i}"):
                st.session_state.selected_item = row.to_dict(); st.session_state.page = 'details'; st.rerun()

    with col_side:
        # قائمة الكبار بتعديل الاسم والتصميم
        st.markdown('<div style="background:white; padding:20px; border-radius:20px; border:1px solid #e2e8f0;">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title">نخبة المطورين</div>', unsafe_allow_html=True)
        
        top_list = ["Mountain View", "SODIC", "Emaar", "TMG", "Palm Hills", "Ora Developers", "Hassan Allam", "Misr Italia"]
        for comp in top_list:
            st.markdown('<div class="top-company-btn">', unsafe_allow_html=True)
            if st.button(f"🏢 {comp}", key=f"side_{comp}"):
                st.session_state.search_query = comp; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# صفحة التفاصيل
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    st.markdown(f"""
        <div style="background:white; padding:40px; border-radius:25px; border:1px solid #e2e8f0; text-align:right; box-shadow: 0 15px 35px rgba(0,0,0,0.05);">
            <h1 style="color:#0044ff; font-weight:900; font-size:2.5rem; margin-bottom:5px;">{item['Developer']}</h1>
            <p style="color:#64748b; font-size:1.2rem;">نطاق العمل: {item['Area']}</p>
            <div style="width:100px; height:5px; background:#001a33; margin:20px 0;"></div>
            <p style="font-size:1.3rem; line-height:2; color:#1e293b;">{item.get('Company_Bio', 'معلومات المطور العقاري قيد التجهيز حالياً.. انتظرونا.')}</p>
        </div>
    """, unsafe_allow_html=True)
