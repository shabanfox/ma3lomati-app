import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق (CSS) لتقليل الفراغات وضبط الشبكة المصغرة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }

    .main-header {
        background: linear-gradient(90deg, #111 0%, #000 100%);
        padding: 15px 35px; border-radius: 0 0 15px 15px;
        border: 1px solid #222; border-right: 12px solid #f59e0b;
        text-align: center; margin-bottom: 20px;
    }
    .header-title { font-weight: 900; font-size: 35px !important; color: #f59e0b; margin: 0; }

    /* كارت الشبكة الصغير جداً ليناسب الـ 30% */
    .mini-card {
        background: #111;
        border: 1px solid #222;
        border-top: 3px solid #f59e0b;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 8px;
        min-height: 140px;
        text-align: center;
    }
    .mini-title { color: #f59e0b; font-size: 16px !important; font-weight: 900; margin-bottom: 5px; }
    .mini-owner { color: #888; font-size: 12px; }
    
    /* تصغير أزرار التنقل والبحث */
    .stButton button { width: 100%; font-size: 11px !important; height: 30px !important; }
    .stTextInput input { height: 35px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

# 4. تحميل البيانات
@st.cache_data(ttl=300)
def load_all_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except: return pd.DataFrame()

df = load_all_data()

# 5. القائمة العلوية
selected = option_menu(
    menu_title=None, options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], orientation="horizontal",
    styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}}
)

# --- شاشة المطورين (70% يمين فارغ | 30% يسار شبكة) ---
if selected == "🏢 المطورين":
    if not df.empty:
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        
        # التقسيم: العمود الأول (يمين) 70% فارغ، العمود الثاني (يسار) 30% للكروت
        col_empty, col_grid = st.columns([0.7, 0.3])
        
        with col_empty:
            # مساحة الـ 70% اليمين (فارغة)
            st.markdown("<div style='margin-top:250px; text-align:center; opacity:0.05;'><h1>MANSETY PRO</h1></div>", unsafe_allow_html=True)

        with col_grid:
            st.markdown("<h4 style='color:#f59e0b; border-bottom:1px solid #333; padding-bottom:5px;'>🏢 شبكة المطورين (3x3)</h4>", unsafe_allow_html=True)
            search_d = st.text_input("🔍 بحث...")
            if search_d:
                devs = devs[devs['Developer'].str.contains(search_d, case=False, na=False)]

            # نظام الـ 9 كروت (شبكة 3 في 3)
            items_per_page = 9
            total_pages = math.ceil(len(devs) / items_per_page)
            if 'dev_page' not in st.session_state: st.session_state.dev_page = 1
            
            start_idx = (st.session_state.dev_page - 1) * items_per_page
            current_devs = devs.iloc[start_idx : start_idx + items_per_page]

            # عرض الشبكة داخل عمود الـ 30% اليسار
            for i in range(0, len(current_devs), 3):
                inner_cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_devs):
                        row = current_devs.iloc[i + j]
                        with inner_cols[j]:
                            st.markdown(f"""
                                <div class="mini-card">
                                    <div class="mini-title">{row['Developer']}</div>
                                    <div class="mini-owner">👤 {row['Owner']}</div>
                                </div>
                            """, unsafe_allow_html=True)
                            with st.expander("🔍 التفاصيل"):
                                st.caption(f"المالك: {row['Owner']}")
                                st.write(row['Detailed_Info'])
            
            # أزرار التنقل صغيرة أسفل الشبكة
            st.write("---")
            nav1, nav2, nav3 = st.columns([1,1,1])
            with nav1:
                if st.session_state.dev_page > 1:
                    if st.button("السابق"): st.session_state.dev_page -= 1; st.rerun()
            with nav2:
                st.markdown(f"<p style='text-align:center; font-size:10px; padding-top:10px;'>{st.session_state.dev_page}/{total_pages}</p>", unsafe_allow_html=True)
            with nav3:
                if st.session_state.dev_page < total_pages:
                    if st.button("التالي"): st.session_state.dev_page += 1; st.rerun()

# (باقي كود شاشات المشاريع والأدوات)
