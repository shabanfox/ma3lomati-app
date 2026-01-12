import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم الواجهة (CSS) المطور
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; 
        text-align: right; 
        font-family: 'Cairo', sans-serif;
    }

    /* شريط المهام العلوي (Top Bar) */
    .top-bar {
        background-color: #111;
        padding: 10px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #222;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
    }
    
    .user-info { color: #888; font-size: 14px; }
    
    /* الهيدر الجمالي - أضفنا margin-top لتعويض شريط المهام */
    .main-header {
        background: linear-gradient(90deg, #111 0%, #000 100%);
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #222;
        border-right: 10px solid #f59e0b;
        text-align: center;
        margin-top: 60px; /* مسافة عشان التوب بار */
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .header-title { font-weight: 900; font-size: 45px !important; color: #f59e0b; margin: 0; }

    /* كروت الشبكة */
    .grid-card {
        background: linear-gradient(145deg, #111, #080808);
        border: 1px solid #222;
        border-top: 5px solid #f59e0b;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 15px;
        min-height: 400px;
        transition: 0.3s all;
        direction: rtl;
    }
    
    .card-title { color: #f59e0b; font-size: 30px !important; font-weight: 900 !important; margin-bottom: 8px; }
    .card-subtitle { color: #ffffff; font-size: 22px !important; font-weight: 700 !important; border-bottom: 2px solid #333; padding-bottom: 8px; margin-bottom: 15px; }

    /* تنسيق زر الخروج ليكون صغير وفي مكانه */
    .stButton > button[key="logout_btn"] {
        background-color: transparent !important;
        color: #ff4b4b !important;
        border: 1px solid #ff4b4b !important;
        width: 100px !important;
        height: 30px !important;
        font-size: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. شريط المهام العلوي (بأزرار Streamlit الفعلية)
t1, t2 = st.columns([8, 1])
with t1:
    st.markdown('<p class="user-info">مرحباً بك، <b>المستخدم المتميز</b> | آخر تحديث: 2026-01-12</p>', unsafe_allow_html=True)
with t2:
    if st.button("تسجيل الخروج", key="logout_btn"):
        st.session_state.clear()
        st.rerun()

# 4. عرض الهيدر الأساسي
st.markdown("""
    <div class="main-header">
        <h1 class="header-title">🏢 منصة معلوماتي العقارية</h1>
        <div class="header-subtitle">إصدار المحترفين PRO 2026</div>
    </div>
""", unsafe_allow_html=True)

# 5. جلب البيانات
@st.cache_data(ttl=300)
def load_all_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except:
        return pd.DataFrame()

df = load_all_data()

# 6. القائمة العلوية
selected = option_menu(
    menu_title=None, 
    options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], 
    orientation="horizontal",
    styles={
        "container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"},
        "nav-link": {"font-size": "18px", "color":"white", "font-family": "Cairo"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"},
    }
)

# --- محتوى الصفحات (بقية الكود السابق) ---
if selected == "🏗️ المشاريع":
    if not df.empty:
        # نظام عرض المشاريع كما هو في الكود السابق
        st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
        # ... (باقي كود عرض المشاريع والمطورين)
        
elif selected == "🏢 المطورين":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏢 سجل المطورين</h2>", unsafe_allow_html=True)
    # ... (باقي كود عرض المطورين)

elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدواتك الاحترافية</h2>", unsafe_allow_html=True)
    # ... (باقي كود الحاسبة)
