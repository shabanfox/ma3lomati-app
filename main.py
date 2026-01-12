import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS) - تصميم سينمائي فخم
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; }
    
    /* زر الخروج */
    .stButton > button[key="logout_btn"] { background-color: #ff4b4b !important; color: white !important; border: none !important; padding: 5px 20px !important; border-radius: 8px !important; }

    /* الهيدر */
    .main-header { background: linear-gradient(90deg, #111 0%, #000 100%); padding: 20px; border-radius: 0 0 20px 20px; border-right: 15px solid #f59e0b; text-align: center; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .header-title { font-weight: 900; font-size: 32px !important; color: #f59e0b; margin: 0; }

    /* الكروت */
    .pro-card { 
        background: #111; border: 1px solid #222; border-top: 5px solid #f59e0b; 
        border-radius: 15px; padding: 20px; margin-bottom: 15px; text-align: center; 
        transition: 0.3s; height: 100%;
    }
    .pro-card:hover { transform: translateY(-5px); border-color: #f59e0b; box-shadow: 0 0 20px rgba(245, 158, 11, 0.2); }
    
    /* تفاصيل المطور */
    .dev-info-container {
        background: #0d0d0d; border: 2px solid #f59e0b; border-radius: 15px;
        padding: 30px; margin-bottom: 30px; animation: fadeIn 0.5s;
    }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

    /* الاستايل العام */
    .stat-text { color: #888; font-size: 14px; }
    .stat-value { color: #f59e0b; font-weight: bold; }
    .stButton button { background: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; font-weight: bold; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data.fillna("غير متوفر").astype(str)
    except: return pd.DataFrame()

df = load_data()

# 4. الترويسة
t_c1, t_c2 = st.columns([10, 1.5])
with t_c2:
    if st.button("تسجيل الخروج", key="logout_btn"):
        st.session_state.clear()
        st.rerun()

st.markdown('<div class="main-header"><h1 class="header-title">🏢 مـنـصـة مـعـلـومـاتـي PRO</h1></div>', unsafe_allow_html=True)

# 5. القائمة الرئيسية
selected = option_menu(
    menu_title=None, 
    options=["🛠️ الأدوات", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-vcard"], 
    orientation="horizontal",
    styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}}
)

# تهيئة الذاكرة (Session State)
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'd_page' not in st.session_state: st.session_state.d_page = 0
if 'active_dev' not in st.session_state: st.session_state.active_dev = None

# --- 🏗️ شاشة المشاريع ---
if selected == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع العقارية</h2>", unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    with f1: s_p = st.text_input("🔍 ابحث عن اسم المشروع...")
    with f2: a_p = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df['Area'].unique().tolist()))
    
    dff = df.copy()
    if s_p: dff = dff[dff['Project Name'].str.contains(s_p, case=False)]
    if a_p != "الكل": dff = dff[dff['Area'] == a_p]

    items = 6
    total_p = max(1, math.ceil(len(dff) / items))
    curr = dff.iloc[st.session_state.p_page * items : (st.session_state.p_page + 1) * items]

    for i in range(0, len(curr), 3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(curr):
                row = curr.iloc[i+j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="pro-card">
                            <h3 style="color:#f59e0b; margin-bottom:5px;">{row.get('Project Name')}</h3>
                            <p style="color:#666; font-size:14px; margin-bottom:15px;">{row.get('Developer')}</p>
                            <div style="text-align:right;">
                                <p class="stat-text">📍 الموقع: <span class="stat-value">{row.get('Area')}</span></p>
                                <p class="stat-text">📏 المساحة: <span class="stat-value">{row.get('Size (Acres)')} فدان</span></p>
                                <p class="stat-text">🏠 النوع: <span class="stat-value">{row.get('شقق/فيلات')}</span></p>
                            </div>
                            <div style="background:#1a150b; padding:10px; border-radius:10px; border:1px dashed #f59e0b; font-size:12px; color:#f59e0b; margin-top:10px;">
                                ⭐ {row.get('Competitive Advantage', '-')[:80]}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
    
    st.write("---")
    n1, n2, n3 = st.columns([1, 2, 1])
    if n3.button("التالي ⬅️", key="p_next"): st.session_state.p_page += 1; st.rerun()
    n2.markdown(f"<p style='text-align:center;'>{st.session_state.p_page + 1} / {total_p}</p>", unsafe_allow_html=True)
    if n1.button("➡️ السابق", key="p_prev") and st.session_state.p_page > 0: st.session_state.p_page -= 1; st.rerun()

# --- 🏢 شاشة المطورين (تطوير احترافي) ---
elif selected == "🏢 المطورين":
    devs_list = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
    
    # عرض التفاصيل في الأعلى إذا تم الضغط
    if st.session_state.active_dev:
        info = devs_list[devs_list['Developer'] == st.session_state.active_dev].iloc[0]
        st.markdown(f"""
            <div class="dev-info-container">
                <h2 style="color:#f59e0b; margin-top:0;">🏢 شركة: {info['Developer']}</h2>
                <h4 style="color:#fff;">👤 المالك: {info['Owner']}</h4>
                <hr style="border-color:#333">
                <p style="color:#ccc; line-height:1.8; font-size:16px;">{info['Detailed_Info']}</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("❌ إغلاق ملف الشركة", key="close_dev"):
            st.session_state.active_dev = None
            st.rerun()

    st.markdown("<h2 style='color:#f59e0b;'>🏢 دليل المطورين</h2>", unsafe_allow_html=True)
    search_d = st.text_input("🔍 ابحث عن مطور...")
    if search_d: devs_list = devs_list[devs_list['Developer'].str.contains(search_d, case=False)]

    for i in range(0, len(devs_list), 3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(devs_list):
                row = devs_list.iloc[i+j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="pro-card">
                            <h2 style="color:#f59e0b;">{row['Developer']}</h2>
                            <div style="background:#000; padding:15px; border-radius:10px; margin:15px 0;">
                                <p style="color:#888; font-size:12px; margin:0;">المالك</p>
                                <p style="color:#fff; font-weight:bold; font-size:18px; margin:0;">{row['Owner']}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"🔍 تفاصيل {row['Developer']}", key=f"d_{row['Developer']}"):
                        st.session_state.active_dev = row['Developer']
                        st.rerun()

# --- 🛠️ شاشة الأدوات ---
elif selected == "🛠️ الأدوات":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ الأدوات الذكية</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='pro-card'><h3>💰 حاسبة القسط</h3>", unsafe_allow_html=True)
        price = st.number_input("إجمالي السعر", value=1000000)
        years = st.slider("سنوات التقسيط", 1, 15, 7)
        st.markdown(f"<h1 style='color:#f59e0b; text-align:center;'>{price/(years*12):,.0f} ج.م</h1>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='pro-card'><h3>📏 محول المساحة</h3>", unsafe_allow_html=True)
        fadan = st.number_input("أدخل المساحة بالفدان", value=1.0)
        st.markdown(f"<h1 style='color:#f59e0b; text-align:center;'>{fadan*4200:,.0f} م²</h1>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
