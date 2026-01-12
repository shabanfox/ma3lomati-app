import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS) - تصميم فخم واحترافي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; }
    
    /* الهيدر وزر الخروج */
    .stButton > button[key="logout_btn"] { background-color: #ff4b4b !important; color: white !important; border: none !important; padding: 5px 20px !important; border-radius: 5px !important; width: auto !important; }
    .main-header { background: linear-gradient(90deg, #111 0%, #000 100%); padding: 15px 35px; border-radius: 0 0 15px 15px; border-right: 12px solid #f59e0b; text-align: center; margin-bottom: 25px; }
    .header-title { font-weight: 900; font-size: 30px !important; color: #f59e0b; margin: 0; }

    /* كروت المشاريع والمطورين */
    .pro-card { 
        background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; 
        border-radius: 12px; padding: 20px; margin-bottom: 10px; text-align: center; min-height: 280px;
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .card-title { color: #f59e0b; font-size: 19px !important; font-weight: 900; margin-bottom: 5px; }
    .stat-row { display: flex; justify-content: space-between; font-size: 13px; margin-top: 8px; color: #ccc; border-bottom: 1px solid #1a1a1a; padding-bottom: 5px; }
    .stat-val { color: #f59e0b; font-weight: bold; }
    
    /* صندوق التفاصيل */
    .detail-container {
        background: #0a0a0a; border: 2px solid #f59e0b; border-radius: 15px;
        padding: 25px; margin: 20px 0; color: #eee; line-height: 1.8;
    }
    .info-box { background: #1a150b; color: #f59e0b; font-size: 12px; padding: 10px; border-radius: 8px; border: 1px dashed #f59e0b; margin-top: 10px; }

    /* الأزرار العامة */
    .stButton button { width: 100%; background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; font-weight: bold; border-radius: 8px; }
    input, textarea { background-color: #111 !important; color: #fff !important; border: 1px solid #333 !important; }
    </style>
""", unsafe_allow_html=True)

# 3. وظيفة جلب البيانات (سريعة مع كاش)
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data.fillna("غير متوفر").astype(str)
    except: return pd.DataFrame()

df = load_data()

# 4. شريط الخروج العلوي
t_col1, t_col2 = st.columns([10, 1])
with t_col2:
    if st.button("خروج", key="logout_btn"): st.session_state.clear(); st.rerun()

# 5. الهيدر والقائمة الرئيسية
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي العقارية PRO</h1></div>', unsafe_allow_html=True)

selected = option_menu(
    menu_title=None, 
    options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], 
    orientation="horizontal",
    styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}}
)

# إدارة الحالات (States)
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'd_page' not in st.session_state: st.session_state.d_page = 0
if 'view_dev' not in st.session_state: st.session_state.view_dev = None

# --- 🏗️ شاشة المشاريع ---
if selected == "🏗️ المشاريع":
    if not df.empty:
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
            f1, f2 = st.columns(2)
            with f1: s_p = st.text_input("🔍 ابحث عن اسم المشروع...")
            with f2: a_p = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df['Area'].unique().tolist()))
            
            dff = df.copy()
            name_col = 'Project Name' if 'Project Name' in df.columns else 'Projects'
            if s_p: dff = dff[dff[name_col].str.contains(s_p, case=False)]
            if a_p != "الكل": dff = dff[dff['Area'] == a_p]

            items = 9
            total_p = max(1, math.ceil(len(dff) / items))
            curr = dff.iloc[st.session_state.p_page * items : (st.session_state.p_page + 1) * items]

            for i in range(0, len(curr), 3):
                grid = st.columns(3)
                for j in range(len(grid)):
                    if i+j < len(curr):
                        row = curr.iloc[i+j]
                        with grid[j]:
                            st.markdown(f"""
                                <div class="pro-card">
                                    <div>
                                        <div class="card-title">{row.get(name_col)}</div>
                                        <div style="color:#888; font-size:13px; margin-bottom:10px;">{row.get('Developer')}</div>
                                        <div class="stat-row"><span>👷 الاستشاري:</span><span class="stat-val">{row.get('Consultant')}</span></div>
                                        <div class="stat-row"><span>📏 المساحة:</span><span class="stat-val">{row.get('Size (Acres)')} فدان</span></div>
                                        <div class="stat-row"><span>🏠 النوع:</span><span class="stat-val">{row.get('شقق/فيلات')}</span></div>
                                    </div>
                                    <div class="info-box"><b>⭐ ميزة:</b> {row.get('Competitive Advantage', '-')[:80]}...</div>
                                </div>
                            """, unsafe_allow_html=True)
            
            # أزرار تنقل المشاريع
            st.write("---")
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            if nav3.button("التالي ⬅️", key="p_n"): st.session_state.p_page += 1; st.rerun()
            nav2.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.p_page + 1} من {total_p}</p>", unsafe_allow_html=True)
            if nav1.button("➡️ السابق", key="p_p") and st.session_state.p_page > 0: st.session_state.p_page -= 1; st.rerun()

# --- 🏢 شاشة المطورين (النظام المطور) ---
elif selected == "🏢 المطورين":
    if not df.empty:
        devs_list = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            # عرض التفاصيل إذا تم الاختيار
            if st.session_state.view_dev:
                dev_info = devs_list[devs_list['Developer'] == st.session_state.view_dev].iloc[0]
                projs = df[df['Developer'] == st.session_state.view_dev]['Project Name'].unique()
                st.markdown(f"""
                    <div class="detail-container">
                        <div style="color:#f59e0b; font-size:22px; font-weight:900; border-bottom:1px solid #333; margin-bottom:15px;">🏢 ملف: {dev_info['Developer']}</div>
                        <p><b>👤 المالك:</b> {dev_info['Owner']}</p>
                        <p><b>📜 التفاصيل:</b> {dev_info['Detailed_Info']}</p>
                        <p><b>🏗️ المشاريع:</b> {', '.join(projs)}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("❌ إغلاق الملف والعودة"): st.session_state.view_dev = None; st.rerun()

            st.markdown("<h2 style='color:#f59e0b;'>🏢 دليل المطورين</h2>", unsafe_allow_html=True)
            search_d = st.text_input("🔍 ابحث عن مطور...")
            if search_d: devs_list = devs_list[devs_list['Developer'].str.contains(search_d, case=False)]

            items = 9
            total_d = max(1, math.ceil(len(devs_list) / items))
            curr_devs = devs_list.iloc[st.session_state.d_page * items : (st.session_state.d_page + 1) * items]

            for i in range(0, len(curr_devs), 3):
                cols = st.columns(3)
                for j in range(len(cols)):
                    if i+j < len(curr_devs):
                        row = curr_devs.iloc[i+j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="pro-card" style="min-height:200px;">
                                    <div class="card-title">{row['Developer']}</div>
                                    <div style="background:#000; padding:10px; border-radius:8px; margin-top:10px;">
                                        <div style="color:#888; font-size:11px;">المالك</div>
                                        <div style="color:#fff;">{row['Owner']}</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button("🔍 عرض الملف", key=f"v_{row['Developer']}"):
                                st.session_state.view_dev = row['Developer']; st.rerun()

            # أزرار تنقل المطورين
            st.write("---")
            d1, d2, d3 = st.columns([1, 2, 1])
            if d3.button("التالي ⬅️", key="d_n"): st.session_state.d_page += 1; st.rerun()
            d2.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.d_page + 1} من {total_d}</p>", unsafe_allow_html=True)
            if d1.button("➡️ السابق", key="d_p") and st.session_state.d_page > 0: st.session_state.d_page -= 1; st.rerun()

# --- 🛠️ شاشة أدوات البروكر ---
elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ الأدوات الذكية</h2>", unsafe_allow_html=True)
    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        st.markdown("<div class='pro-card'><h3>💰 حاسبة القسط</h3>", unsafe_allow_html=True)
        price = st.number_input("السعر الإجمالي", value=1000000)
        years = st.number_input("سنوات التقسيط", value=7, min_value=1)
        st.markdown(f"<h2 style='color:#f59e0b;'>{price/(years*12):,.0f} ج/شهري</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with row1_c2:
        st.markdown("<div class='pro-card'><h3>📏 محول المساحة</h3>", unsafe_allow_html=True)
        acre = st.number_input("المساحة بالفدان", value=1.0)
        st.markdown(f"<h2 style='color:#f59e0b;'>{acre*4200:,.0f} متر مربع</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='pro-card' style='min-height:150px;'><h3>📝 مفكرة سريعة</h3>", unsafe_allow_html=True)
    st.text_area("اكتب ملاحظات العميل هنا...", height=100)
    st.markdown("</div>", unsafe_allow_html=True)
