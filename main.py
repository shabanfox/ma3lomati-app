import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق (CSS)
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

    /* تنسيق الكروت الجانبية */
    .dev-card {
        background: #111;
        border-right: 5px solid #f59e0b;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 12px;
        border: 1px solid #222;
        border-right: 8px solid #f59e0b;
    }
    .dev-title { color: #f59e0b; font-size: 22px !important; font-weight: 900; margin-bottom: 5px; }
    .dev-owner { color: #fff; font-size: 16px; margin-bottom: 10px; border-bottom: 1px solid #333; padding-bottom: 5px; }
    
    /* تنسيق الأزرار */
    .stButton button { width: 100%; border-radius: 5px; }
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

# --- شاشة المطورين (30% يمين | 70% يسار) ---
if selected == "🏢 المطورين":
    if not df.empty:
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        
        # هنا قمنا بعكس الترتيب: العمود الأول 0.3 (يمين) والثاني 0.7 (يسار)
        col_cards, col_empty = st.columns([0.3, 0.7])
        
        with col_cards:
            st.markdown("<h3 style='color:#f59e0b; border-bottom:1px solid #333;'>🏢 المطورين</h3>", unsafe_allow_html=True)
            search_d = st.text_input("🔍 بحث...")
            if search_d:
                devs = devs[devs['Developer'].str.contains(search_d, case=False, na=False)]

            # نظام الـ 9 كروت
            items_per_page = 9
            total_pages = math.ceil(len(devs) / items_per_page)
            if 'dev_page' not in st.session_state: st.session_state.dev_page = 1
            
            start_idx = (st.session_state.dev_page - 1) * items_per_page
            current_devs = devs.iloc[start_idx : start_idx + items_per_page]

            for _, row in current_devs.iterrows():
                st.markdown(f"""
                    <div class="dev-card">
                        <div class="dev-title">{row['Developer']}</div>
                        <div class="dev-owner">👤 {row['Owner']}</div>
                    </div>
                """, unsafe_allow_html=True)
                with st.expander("🔍 التفاصيل"):
                    st.info(f"المالك: {row['Owner']}")
                    st.write(row['Detailed_Info'])
            
            # أزرار التنقل
            st.write("---")
            p1, p2 = st.columns(2)
            with p1:
                if st.session_state.dev_page > 1:
                    if st.button("➡️ السابقة"):
                        st.session_state.dev_page -= 1
                        st.rerun()
            with p2:
                if st.session_state.dev_page < total_pages:
                    if st.button("التالية ⬅️"):
                        st.session_state.dev_page += 1
                        st.rerun()

        with col_empty:
            # الجانب الأيسر فارغ بنسبة 70%
            st.markdown("<div style='margin-top:250px; text-align:center; opacity:0.1;'><h1>MANSETY PRO</h1></div>", unsafe_allow_html=True)

# --- شاشة المشاريع ---
elif selected == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
    # (باقي كود المشاريع يوضع هنا)

# --- شاشة أدوات البروكر ---
elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات البروكر</h2>", unsafe_allow_html=True)
    # (باقي كود الأدوات يوضع هنا)
