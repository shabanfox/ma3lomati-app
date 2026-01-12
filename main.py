import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; }
    
    .stButton > button[key="logout_btn"] { background-color: #ff4b4b !important; color: white !important; border: none !important; padding: 5px 20px !important; border-radius: 5px !important; width: auto !important; }

    .main-header { background: linear-gradient(90deg, #111 0%, #000 100%); padding: 15px 35px; border-radius: 0 0 15px 15px; border-right: 12px solid #f59e0b; text-align: center; margin-bottom: 25px; }
    .header-title { font-weight: 900; font-size: 30px !important; color: #f59e0b; margin: 0; }

    /* تصميم كارت المطور المطور */
    .dev-card { 
        background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; 
        border-radius: 12px; padding: 20px; text-align: center; 
        min-height: 200px; display: flex; flex-direction: column; justify-content: center;
        transition: 0.3s;
    }
    .dev-card:hover { border-color: #f59e0b; transform: translateY(-5px); }
    .owner-box { background: #000; border: 1px solid #222; border-radius: 8px; padding: 10px; margin-top: 15px; }
    
    /* أزرار التنقل وعرض التفاصيل */
    .stButton button { width: 100%; background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; font-weight: bold; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# 3. شريط الخروج
t1, t2 = st.columns([10, 1])
with t2:
    if st.button("خروج", key="logout_btn"): st.session_state.clear(); st.rerun()

# 4. جلب البيانات
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data.fillna("غير متوفر").astype(str)
    except: return pd.DataFrame()

df = load_data()

# 5. القائمة
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
selected = option_menu(None, ["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], icons=["tools", "building", "person-badge"], orientation="horizontal", styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}})

if 'p_p' not in st.session_state: st.session_state.p_p = 0
if 'd_p' not in st.session_state: st.session_state.d_p = 0

# --- 🏢 شاشة المطورين (النظام الجديد: كارت + تفاصيل عند الضغط) ---
if selected == "🏢 المطورين":
    if not df.empty:
        # استخلاص بيانات المطورين الفريدة
        devs_list = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            st.markdown("<h2 style='color:#f59e0b;'>🏢 دليل المطورين</h2>", unsafe_allow_html=True)
            search_d = st.text_input("🔍 ابحث عن مطور...")
            if search_d: devs_list = devs_list[devs_list['Developer'].str.contains(search_d, case=False)]

            items = 9
            total_pages = max(1, math.ceil(len(devs_list) / items))
            curr_devs = devs_list.iloc[st.session_state.d_p * items : (st.session_state.d_p + 1) * items]

            for i in range(0, len(curr_devs), 3):
                grid = st.columns(3)
                for j in range(len(grid)):
                    if i + j < len(curr_devs):
                        row = curr_devs.iloc[i + j]
                        with grid[j]:
                            # الكارت المختصر
                            st.markdown(f"""
                                <div class="dev-card">
                                    <div style="color:#f59e0b; font-size:20px; font-weight:900;">{row['Developer']}</div>
                                    <div class="owner-box">
                                        <div style="color:#888; font-size:11px;">المالك / رئيس مجلس الإدارة</div>
                                        <div style="color:#fff; font-weight:bold;">{row['Owner']}</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # زر عرض التفاصيل
                            if st.button(f"تفاصيل {row['Developer']}", key=f"btn_{row['Developer']}"):
                                @st.dialog(f"🏢 بطاقة المطور: {row['Developer']}")
                                def show_details(data):
                                    st.markdown(f"### 👤 المالك: {data['Owner']}")
                                    st.write("---")
                                    st.markdown("#### 📄 نبذة وتفاصيل الشركة:")
                                    st.info(data['Detailed_Info'])
                                    st.write("---")
                                    # إظهار مشاريع هذا المطور تلقائياً من الشيت
                                    projects = df[df['Developer'] == data['Developer']]['Project Name'].unique()
                                    st.markdown("#### 🏗️ أهم المشاريع في المنصة:")
                                    for p in projects:
                                        st.markdown(f"* {p}")
                                
                                show_details(row)

            # أزرار التنقل
            st.write("---")
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            with nav3:
                if (st.session_state.d_p + 1) < total_pages:
                    if st.button("التالي ⬅️", key="dn"): st.session_state.d_p += 1; st.rerun()
            with nav2: st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.d_p + 1} من {total_pages}</p>", unsafe_allow_html=True)
            with nav1:
                if st.session_state.d_p > 0:
                    if st.button("➡️ السابق", key="dp"): st.session_state.d_p -= 1; st.rerun()

# --- 🏗️ شاشة المشاريع ---
elif selected == "🏗️ المشاريع":
    # الكود الخاص بالمشاريع يظل كما هو لضمان استقرار العرض
    st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
    # ... (باقي كود المشاريع الذي أرسلته سابقاً) ...
    st.info("استخدم البحث بالأعلى للوصول السريع للمشروع.")

# --- 🛠️ شاشة الأدوات ---
elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ الأدوات</h2>", unsafe_allow_html=True)
    # ... (باقي كود الأدوات) ...
