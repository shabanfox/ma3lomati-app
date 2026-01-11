import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu 
import math

# 1. إعدادات النظام
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. هندسة التصميم (Premium Black & Gold)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }

    /* كارت المطور المطور للشبكة */
    .dev-card {
        background: linear-gradient(145deg, #111, #080808);
        border: 1px solid #222;
        border-top: 4px solid #f59e0b;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        height: 280px; /* توحيد الطول لجمال الشبكة */
        transition: 0.3s all;
        color: white;
        overflow: hidden;
    }
    .dev-card:hover { border-color: #f59e0b; transform: translateY(-5px); box-shadow: 0 5px 15px rgba(245, 158, 11, 0.1); }
    
    .dev-title { color: #f59e0b; font-size: 18px; font-weight: 900; margin-bottom: 10px; }
    .dev-owner { color: #888; font-size: 13px; margin-bottom: 10px; border-bottom: 1px solid #222; padding-bottom: 5px; }
    .dev-desc { color: #bbb; font-size: 12px; line-height: 1.5; height: 100px; overflow: hidden; }

    /* تنسيق أزرار التنقل */
    .stButton button {
        background-color: #1a1a1a !important; color: #f59e0b !important;
        border: 1px solid #f59e0b !important; border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=300)
def load_master_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except: return pd.DataFrame()

df = load_master_data()

# 4. القائمة العلوية
selected = option_menu(
    menu_title=None, 
    options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], 
    menu_icon="cast", 
    default_index=2, # جعل المطورين الصفحة الافتراضية للتجربة
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#000", "border-bottom": "3px solid #f59e0b"},
        "nav-link": {"font-size": "18px", "color":"white", "font-family": "Cairo"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"},
    }
)

# --- شاشة المطورين (نظام الشبكة 3×3) ---
if selected == "🏢 المطورين":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏢 قاعدة بيانات المطورين</h2>", unsafe_allow_html=True)
    
    if not df.empty and 'Developer' in df.columns:
        # تجهيز البيانات بدون تكرار
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        
        # محرك البحث
        search_d = st.text_input("🔍 ابحث عن اسم المطور...")
        if search_d:
            devs = devs[devs['Developer'].str.contains(search_d, case=False, na=False)]

        # --- منطق التقسيم (9 في الصفحة) ---
        items_per_page = 9
        total_pages = math.ceil(len(devs) / items_per_page)
        
        if 'dev_page' not in st.session_state:
            st.session_state.dev_page = 1

        start_idx = (st.session_state.dev_page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        current_devs = devs.iloc[start_idx:end_idx]

        # --- إنشاء الشبكة (Grid) ---
        # نقوم بتقسيم المطورين لمجموعات من 3 لعرضهم في صفوف
        for i in range(0, len(current_devs), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(current_devs):
                    row = current_devs.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="dev-card">
                                <div class="dev-title">🏢 {row['Developer']}</div>
                                <div class="dev-owner">👤 المالك: {row['Owner'] if pd.notna(row['Owner']) else 'غير مسجل'}</div>
                                <div class="dev-desc">
                                    <b>سابقة الأعمال:</b><br>
                                    {row['Detailed_Info'] if pd.notna(row['Detailed_Info']) else 'لا توجد تفاصيل إضافية حالياً.'}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        if st.button("عرض كامل التفاصيل", key=f"btn_{row['Developer']}"):
                            st.info(f"📄 **تفاصيل {row['Developer']}:** \n\n {row['Detailed_Info']}")

        # أزرار التنقل
        st.write("---")
        c_prev, c_page, c_next = st.columns([1, 2, 1])
        with c_prev:
            if st.session_state.dev_page > 1:
                if st.button("⬅️ السابق"):
                    st.session_state.dev_page -= 1
                    st.rerun()
        with c_page:
            st.markdown(f"<p style='text-align:center; color:#888;'>صفحة {st.session_state.dev_page} من {total_pages}</p>", unsafe_allow_html=True)
        with c_next:
            if st.session_state.dev_page < total_pages:
                if st.button("التالي ➡️"):
                    st.session_state.dev_page += 1
                    st.rerun()
    else:
        st.error("بيانات المطورين غير متوفرة.")

# --- بقية الشاشات (الأدوات والمشاريع كما هي) ---
elif selected == "🛠️ أدوات البروكر":
    st.info("قسم الأدوات يعمل كما في النسخة السابقة.")
elif selected == "🏗️ المشاريع":
    st.info("قسم المشاريع يعمل كما في النسخة السابقة.")
