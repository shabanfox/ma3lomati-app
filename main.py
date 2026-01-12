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

    .dev-card { 
        background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; 
        border-radius: 12px; padding: 20px; text-align: center; min-height: 180px;
    }
    .owner-box { background: #000; border: 1px solid #222; border-radius: 8px; padding: 10px; margin-top: 10px; }
    
    .detail-container {
        background: #0a0a0a; border: 2px solid #f59e0b; border-radius: 15px;
        padding: 25px; margin: 20px 0; color: #eee; line-height: 1.8;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
    }
    .detail-header { color: #f59e0b; font-weight: 900; font-size: 22px; border-bottom: 1px solid #333; margin-bottom: 15px; padding-bottom: 10px; }
    
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
selected = option_menu(None, ["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], icons=["tools", "building", "person-badge"], orientation="horizontal", 
                       styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}})

# إدارة الحالة (State)
if 'd_p' not in st.session_state: st.session_state.d_p = 0
if 'view_dev' not in st.session_state: st.session_state.view_dev = None

# --- 🏢 شاشة المطورين ---
if selected == "🏢 المطورين":
    if not df.empty:
        devs_list = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            # 1. عرض تفاصيل المطور المختار في الأعلى (إذا وجد)
            if st.session_state.view_dev:
                dev_info = devs_list[devs_list['Developer'] == st.session_state.view_dev].iloc[0]
                projs = df[df['Developer'] == st.session_state.view_dev]['Project Name'].unique()
                
                st.markdown(f"""
                    <div class="detail-container">
                        <div class="detail-header">🏢 ملف شركة: {dev_info['Developer']}</div>
                        <p style="font-size:18px;"><b>👤 المالك:</b> <span style="color:#f59e0b;">{dev_info['Owner']}</span></p>
                        <p><b>📜 نبذة عن الشركة:</b><br>{dev_info['Detailed_Info']}</p>
                        <p><b>🏗️ قائمة المشاريع:</b> {', '.join(projs)}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("⬅️ إغلاق الملف والعودة للقائمة"):
                    st.session_state.view_dev = None
                    st.rerun()
                st.write("---")

            # 2. عرض الشبكة
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
                            st.markdown(f"""
                                <div class="dev-card">
                                    <div style="color:#f59e0b; font-size:18px; font-weight:900;">{row['Developer']}</div>
                                    <div class="owner-box">
                                        <div style="color:#888; font-size:11px;">المالك</div>
                                        <div style="color:#fff;">{row['Owner']}</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            # الحل: ربط الزر بتغيير الحالة مباشرة
                            if st.button(f"🔍 تفاصيل", key=f"v_{row['Developer']}"):
                                st.session_state.view_dev = row['Developer']
                                st.rerun()

            # 3. أزرار التنقل
            st.write("---")
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            with nav3:
                if (st.session_state.d_p + 1) < total_pages:
                    if st.button("التالي ⬅️", key="dn"): st.session_state.d_p += 1; st.rerun()
            with nav2: st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.d_p + 1} من {total_pages}</p>", unsafe_allow_html=True)
            with nav1:
                if st.session_state.d_p > 0:
                    if st.button("➡️ السابق", key="dp"): st.session_state.d_p -= 1; st.rerun()

# --- (باقي الأقسام كالمعتاد) ---
elif selected == "🏗️ المشاريع":
    st.info("قسم المشاريع يعمل بكفاءة.")
elif selected == "🛠️ أدوات البروكر":
    st.info("أدوات الحساب جاهزة.")
