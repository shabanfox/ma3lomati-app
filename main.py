import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق (CSS) لضبط الأبعاد الجديدة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }

    /* الهيدر */
    .main-header {
        background: linear-gradient(90deg, #111 0%, #000 100%);
        padding: 15px 35px; border-radius: 0 0 15px 15px;
        border: 1px solid #222; border-right: 12px solid #f59e0b;
        text-align: center; margin-bottom: 25px;
    }
    .header-title { font-weight: 900; font-size: 35px !important; color: #f59e0b; margin: 0; }

    /* كارت المطور في الشبكة الواسعة */
    .dev-grid-card {
        background: #111;
        border: 1px solid #222;
        border-top: 4px solid #f59e0b;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        min-height: 200px;
        transition: 0.3s;
        text-align: center;
    }
    .dev-grid-card:hover { border-color: #f59e0b; transform: translateY(-5px); }
    .dev-name { color: #f59e0b; font-size: 24px !important; font-weight: 900; margin-bottom: 10px; }
    .dev-owner { color: #ffffff; font-size: 16px; margin-bottom: 15px; opacity: 0.8; }
    
    /* تحسين شكل الأزرار */
    .stButton button { background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

# 4. جلب البيانات
@st.cache_data(ttl=300)
def load_all_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except: return pd.DataFrame()

df = load_all_data()

# 5. قائمة التنقل
selected = option_menu(
    menu_title=None, options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], orientation="horizontal",
    styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}}
)

# --- شاشة المطورين (70% يمين شبكة | 30% يسار فارغ) ---
if selected == "🏢 المطورين":
    if not df.empty:
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        
        # التقسيم المطلوب: 70% يمين للشبكة | 30% يسار فارغ
        col_main_grid, col_side_space = st.columns([0.7, 0.3])
        
        with col_main_grid:
            st.markdown("<h2 style='color:#f59e0b; margin-bottom:20px;'>🏢 شبكة المطورين المعتمدين</h2>", unsafe_allow_html=True)
            
            # البحث
            search_d = st.text_input("🔍 ابحث عن مطور عقاري...")
            if search_d:
                devs = devs[devs['Developer'].str.contains(search_d, case=False, na=False)]

            # نظام الـ 9 كروت (3 في كل صف)
            items_per_page = 9
            total_pages = math.ceil(len(devs) / items_per_page)
            if 'dev_page' not in st.session_state: st.session_state.dev_page = 1
            
            start_idx = (st.session_state.dev_page - 1) * items_per_page
            current_devs = devs.iloc[start_idx : start_idx + items_per_page]

            # إنشاء الشبكة 3×3 في مساحة الـ 70%
            for i in range(0, len(current_devs), 3):
                grid_cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_devs):
                        row = current_devs.iloc[i + j]
                        with grid_cols[j]:
                            st.markdown(f"""
                                <div class="dev-grid-card">
                                    <div class="dev-name">{row['Developer']}</div>
                                    <div class="dev-owner">👤 {row['Owner']}</div>
                                </div>
                            """, unsafe_allow_html=True)
                            with st.expander("🔍 عرض سابقة الأعمال"):
                                st.write(row['Detailed_Info'])
            
            # أزرار التنقل بين الصفحات
            st.write("---")
            p1, p2, p3 = st.columns([1,2,1])
            with p1:
                if st.session_state.dev_page > 1:
                    if st.button("➡️ الصفحة السابقة"): st.session_state.dev_page -= 1; st.rerun()
            with p2:
                st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.dev_page} من {total_pages}</p>", unsafe_allow_html=True)
            with p3:
                if st.session_state.dev_page < total_pages:
                    if st.button("الصفحة التالية ⬅️"): st.session_state.dev_page += 1; st.rerun()

        with col_side_space:
            # مساحة الـ 30% اليسار فارغة تماماً
            st.markdown("<div style='border-right: 1px solid #222; height: 800px; margin-right: 20px; opacity: 0.1;'></div>", unsafe_allow_html=True)

# (باقي كود شاشات المشاريع والأدوات)
