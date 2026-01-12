import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة والتنسيق
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; }
    
    .main-header { background: linear-gradient(90deg, #111 0%, #000 100%); padding: 15px; border-radius: 0 0 15px 15px; border-right: 12px solid #f59e0b; text-align: center; margin-bottom: 25px; }
    .header-title { font-weight: 900; font-size: 30px !important; color: #f59e0b; margin: 0; }

    .pro-card { 
        background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; 
        border-radius: 12px; padding: 20px; text-align: center; height: 100%; min-height: 220px;
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .detail-box {
        background: #0d0d0d; border-right: 6px solid #f59e0b; border-radius: 12px;
        padding: 25px; color: #eee; border: 1px solid #222; animation: fadeIn 0.4s;
    }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    
    .card-title { color: #f59e0b; font-size: 19px !important; font-weight: 900; }
    .stat-line { display: flex; justify-content: space-between; border-bottom: 1px solid #1a1a1a; padding: 5px 0; font-size: 14px; }
    .stat-label { color: #888; }
    .stat-val { color: #f59e0b; font-weight: bold; }
    
    .stButton button { background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; border-radius: 8px; font-weight: bold; }
    .logout-btn button { background: #ff4b4b !important; color: white !important; border: none !important; width: auto !important; }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data.fillna("غير متوفر").astype(str)
    except: return pd.DataFrame()

df = load_data()

# 3. الهيدر
t_c1, t_c2 = st.columns([10, 1])
with t_c2:
    if st.button("خروج", key="logout_btn"): st.session_state.clear(); st.rerun()
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي PRO</h1></div>', unsafe_allow_html=True)

selected = option_menu(None, ["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
                       icons=["tools", "building", "person-badge"], orientation="horizontal",
                       styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}})

# إدارة الحالات
for key in ['p_page', 'd_page', 'active_dev', 'active_proj']:
    if key not in st.session_state: st.session_state[key] = 0 if 'page' in key else None

# --- 🏗️ شاشة المشاريع (داتا كاملة + تفاصيل جانبية) ---
if selected == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
    col_main, col_filter = st.columns([0.7, 0.3])
    
    with col_filter:
        st.markdown("🔍 **فلترة سريعة**")
        s_p = st.text_input("بحث بالاسم...")
        area_list = ["الكل"] + sorted(df['Area'].unique().tolist()) if 'Area' in df.columns else ["الكل"]
        a_p = st.selectbox("المنطقة", area_list)

    with col_main:
        dff = df.copy()
        if s_p: dff = dff[dff['Project Name'].str.contains(s_p, case=False)]
        if a_p != "الكل": dff = dff[dff['Area'] == a_p]

        items = 9
        total_p = max(1, math.ceil(len(dff) / items))
        curr_p = dff.iloc[st.session_state.p_page * items : (st.session_state.p_page + 1) * items].reset_index()

        for i in range(0, len(curr_p), 3):
            row_indices = curr_p['index'].iloc[i:i+3].tolist()
            if st.session_state.active_proj in row_indices:
                p_data = df.loc[st.session_state.active_proj]
                st.markdown("---")
                c1, c2 = st.columns([0.3, 0.7])
                with c1:
                    st.markdown(f"<div class='pro-card'><div class='card-title'>{p_data['Project Name']}</div><p>{p_data['Developer']}</p></div>", unsafe_allow_html=True)
                    if st.button("⬅️ إغلاق", key=f"cp_{p_data.name}"): st.session_state.active_proj = None; st.rerun()
                with c2:
                    st.markdown(f"""<div class='detail-box'>
                        <h3 style='color:#f59e0b;'>🏗️ تفاصيل {p_data['Project Name']}</h3>
                        <div class='stat-line'><span class='stat-label'>📍 المنطقة:</span><span class='stat-val'>{p_data.get('Area')}</span></div>
                        <div class='stat-line'><span class='stat-label'>🏠 النوع:</span><span class='stat-val'>{p_data.get('شقق/فيلات')}</span></div>
                        <div class='stat-line'><span class='stat-label'>📏 المساحة:</span><span class='stat-val'>{p_data.get('Size (Acres)')} فدان</span></div>
                        <div class='stat-line'><span class='stat-label'>👷 الاستشاري:</span><span class='stat-val'>{p_data.get('Consultant')}</span></div>
                        <p style='margin-top:15px;'><b>⭐ المميزات:</b><br>{p_data.get('Competitive Advantage')}</p>
                    </div>""", unsafe_allow_html=True)
                st.markdown("---")
            else:
                cols = st.columns(3)
                for j in range(3):
                    if i+j < len(curr_p):
                        item = curr_p.iloc[i+j]
                        with cols[j]:
                            st.markdown(f"""<div class='pro-card'>
                                <div class='card-title'>{item['Project Name']}</div>
                                <div style='font-size:13px; color:#888;'>{item['Developer']}</div>
                                <div style='font-size:12px; margin-top:10px; color:#aaa;'>📍 {item['Area']}</div>
                            </div>""", unsafe_allow_html=True)
                            if st.button("🔍 التفاصيل", key=f"bp_{item['index']}"):
                                st.session_state.active_proj = item['index']; st.rerun()

# --- 🏢 شاشة المطورين (نفس النظام المستقر) ---
elif selected == "🏢 المطورين":
    devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
    st.markdown("<h2 style='color:#f59e0b;'>🏢 دليل المطورين</h2>", unsafe_allow_html=True)
    
    search_d = st.text_input("🔍 ابحث عن مطور...")
    if search_d: devs = devs[devs['Developer'].str.contains(search_d, case=False)]

    items = 9
    total_d = max(1, math.ceil(len(devs) / items))
    curr_d = devs.iloc[st.session_state.d_page * items : (st.session_state.d_page + 1) * items].reset_index()

    for i in range(0, len(curr_d), 3):
        row_ids = curr_d['index'].iloc[i:i+3].tolist()
        if st.session_state.active_dev in row_ids:
            d_data = devs.iloc[st.session_state.active_dev]
            st.markdown("---")
            c1, c2 = st.columns([0.3, 0.7])
            with c1:
                st.markdown(f"<div class='pro-card'><div class='card-title'>{d_data['Developer']}</div></div>", unsafe_allow_html=True)
                if st.button("⬅️ إغلاق", key=f"cd_{d_data.name}"): st.session_state.active_dev = None; st.rerun()
            with c2:
                st.markdown(f"""<div class='detail-box'>
                    <h3 style='color:#f59e0b;'>🏢 ملف {d_data['Developer']}</h3>
                    <p><b>👤 المالك:</b> {d_data['Owner']}</p>
                    <p><b>📜 النبذة:</b> {d_data['Detailed_Info']}</p>
                </div>""", unsafe_allow_html=True)
            st.markdown("---")
        else:
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(curr_d):
                    item = curr_d.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='pro-card'><div class='card-title'>{item['Developer']}</div><p style='font-size:13px; color:#888;'>{item['Owner'][:40]}...</p></div>", unsafe_allow_html=True)
                        if st.button("🔍 عرض الملف", key=f"bd_{item['index']}"):
                            st.session_state.active_dev = item['index']; st.rerun()

# --- 🛠️ شاشة الأدوات (70/30) ---
elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b;'>🛠️ الأدوات الذكية</h2>", unsafe_allow_html=True)
    c_tools, c_note = st.columns([0.3, 0.7])
    with c_tools:
        st.markdown("<div class='detail-box'>", unsafe_allow_html=True)
        pr = st.number_input("السعر", value=1000000)
        yr = st.slider("السنوات", 1, 15, 7)
        st.markdown(f"<h3 style='color:#f59e0b; text-align:center;'>{pr/(yr*12):,.0f} ج.م/شهري</h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with c_note:
        st.text_area("📝 مفكرة العميل السريعة", height=250, placeholder="سجل هنا متطلبات العميل...")
