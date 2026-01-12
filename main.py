import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 
from datetime import datetime

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS) - النسخة الـ Ultra
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container { padding-top: 1rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top right, #0a0a0a, #050505);
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }

    /* الهيدر الرئيسي */
    .main-header {
        background: rgba(255, 255, 255, 0.02);
        padding: 20px; border-radius: 15px;
        border-right: 10px solid #f59e0b;
        text-align: center; margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .header-title { font-weight: 900; font-size: 35px !important; color: #f59e0b; margin: 0; }

    /* الكروت المطورة */
    .pro-card { 
        background: #111; border: 1px solid #222; border-radius: 15px; 
        padding: 20px; margin-bottom: 15px; transition: 0.3s;
        min-height: 250px; display: flex; flex-direction: column; justify-content: space-between;
    }
    .pro-card:hover { border-color: #f59e0b; transform: translateY(-5px); box-shadow: 0 5px 15px rgba(245, 158, 11, 0.1); }
    .card-title { color: #f59e0b; font-size: 20px !important; font-weight: 900; }
    
    /* صندوق التفاصيل الجانبي */
    .detail-box {
        background: #0d0d0d; border: 1px solid #f59e0b; border-radius: 15px;
        padding: 25px; position: sticky; top: 20px; color: #fff;
    }
    
    .stat-line { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #1a1a1a; font-size: 14px; }
    .stat-label { color: #888; }
    .stat-value { color: #f59e0b; font-weight: bold; }

    /* الأزرار والمدخلات */
    .stButton button { width: 100%; background: #1a1a1a !important; color: #f59e0b !important; border-radius: 10px !important; border: 1px solid #333 !important; font-weight: bold !important; height: 45px; }
    .stButton button:hover { background: #f59e0b !important; color: #000 !important; }
    input, select, textarea { background-color: #111 !important; color: white !important; border: 1px solid #333 !important; border-radius: 8px !important; }
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

# 4. واجهة المستخدم العلوية
c1, c2 = st.columns([10, 1.5])
with c1:
    st.markdown('<div class="main-header"><h1 class="header-title">🏢 مـعـلـومـاتـي PRO</h1></div>', unsafe_allow_html=True)
with c2:
    if st.button("🚪 خروج", key="logout_btn"):
        st.session_state.clear()
        st.rerun()

selected = option_menu(
    menu_title=None, 
    options=["🛠️ الأدوات", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["cpu", "building-up", "person-badge-fill"], 
    orientation="horizontal",
    styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}}
)

# إدارة الحالة
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'd_page' not in st.session_state: st.session_state.d_page = 0
if 'view_dev' not in st.session_state: st.session_state.view_dev = None

# --- 🏗️ شاشة المشاريع ---
if selected == "🏗️ المشاريع":
    st.markdown("<h3 style='color:#f59e0b;'>🏗️ دليل المشاريع الذكي</h3>", unsafe_allow_html=True)
    f_col1, f_col2 = st.columns(2)
    s_p = f_col1.text_input("🔍 ابحث عن مشروع...")
    a_p = f_col2.selectbox("📍 تصفية حسب المنطقة", ["الكل"] + sorted(df['Area'].unique().tolist()))
    
    dff = df.copy()
    if s_p: dff = dff[dff['Project Name'].str.contains(s_p, case=False)]
    if a_p != "الكل": dff = dff[dff['Area'] == a_p]

    items = 6
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
                            <div class="card-title">{row.get('Project Name')}</div>
                            <div style="color:#888; font-size:12px;">{row.get('Developer')}</div>
                            <div style="margin:15px 0;">
                                <div class="stat-line"><span class="stat-label">📍 الموقع:</span><span class="stat-value">{row.get('Area')}</span></div>
                                <div class="stat-line"><span class="stat-label">📏 المساحة:</span><span class="stat-value">{row.get('Size (Acres)')} فدان</span></div>
                                <div class="stat-line"><span class="stat-label">🏠 النوع:</span><span class="stat-value">{row.get('شقق/فيلات')}</span></div>
                            </div>
                            <div style="background:rgba(245,158,11,0.1); padding:8px; border-radius:8px; font-size:11px; color:#f59e0b;">
                                ⭐ {row.get('Competitive Advantage', '-')[:70]}...
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
    
    # التنقل
    p1, p2, p3 = st.columns([1, 2, 1])
    if p3.button("التالي ⬅️", key="p_next"): st.session_state.p_page += 1; st.rerun()
    p2.markdown(f"<p style='text-align:center;'>{st.session_state.p_page + 1} / {total_p}</p>", unsafe_allow_html=True)
    if p1.button("➡️ السابق", key="p_prev") and st.session_state.p_page > 0: st.session_state.p_page -= 1; st.rerun()

# --- 🏢 شاشة المطورين ---
elif selected == "🏢 المطورين":
    devs_list = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
    
    col_list, col_detail = st.columns([0.6, 0.4])
    
    with col_list:
        st.markdown("<h3 style='color:#f59e0b;'>🏢 قائمة المطورين</h3>", unsafe_allow_html=True)
        s_d = st.text_input("🔍 ابحث عن شركة...")
        if s_d: devs_list = devs_list[devs_list['Developer'].str.contains(s_d, case=False)]
        
        for i in range(0, len(devs_list), 2):
            rows = st.columns(2)
            for j in range(2):
                if i+j < len(devs_list):
                    row = devs_list.iloc[i+j]
                    with rows[j]:
                        st.markdown(f"""
                            <div class="pro-card" style="min-height:150px;">
                                <div class="card-title">{row['Developer']}</div>
                                <div style="color:#888;">👤 المالك: {row['Owner']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        if st.button("عرض الملف الكامل", key=f"btn_{row['Developer']}"):
                            st.session_state.view_dev = row['Developer']
                            st.rerun()

    with col_detail:
        if st.session_state.view_dev:
            info = devs_list[devs_list['Developer'] == st.session_state.view_dev].iloc[0]
            projs = df[df['Developer'] == st.session_state.view_dev]['Project Name'].unique()
            st.markdown(f"""
                <div class="detail-box">
                    <h2 style="color:#f59e0b; margin-top:0;">{info['Developer']}</h2>
                    <p><b>👤 صاحب الشركة:</b> {info['Owner']}</p>
                    <hr style="border-color:#333">
                    <p><b>📜 نبذة تاريخية:</b><br>{info['Detailed_Info']}</p>
                    <p><b>🏗️ أهم المشاريع:</b><br>{', '.join(projs)}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("❌ إغلاق ملف الشركة"):
                st.session_state.view_dev = None
                st.rerun()
        else:
            st.info("💡 اختر مطوراً من القائمة لعرض تفاصيله بالكامل هنا.")

# --- 🛠️ شاشة الأدوات ---
elif selected == "🛠️ الأدوات":
    st.markdown("<h3 style='color:#f59e0b; text-align:center;'>🛠️ حزمة أدوات البروكر</h3>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["💰 حاسبة الأقساط", "📐 محولات المساحة"])
    
    with t1:
        st.markdown("<div class='pro-card'>", unsafe_allow_html=True)
        price = st.number_input("سعر الوحدة الإجمالي", value=2000000, step=500000)
        down = st.slider("نسبة المقدم (%)", 0, 50, 10)
        years = st.slider("مدة التقسيط (سنوات)", 1, 15, 8)
        
        net_price = price * (1 - down/100)
        monthly = net_price / (years * 12)
        
        st.markdown(f"""
            <div style='text-align:center; padding:20px; border:1px dashed #f59e0b; border-radius:10px;'>
                <p style='margin:0; color:#888;'>القسط الشهري المتوقع</p>
                <h1 style='color:#f59e0b; margin:0;'>{monthly:,.0f} ج.م</h1>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with t2:
        st.markdown("<div class='pro-card'>", unsafe_allow_html=True)
        val = st.number_input("أدخل القيمة بالفدان", value=1.0)
        st.markdown(f"<h2 style='color:#f59e0b; text-align:center;'>= {val * 4200:,.0f} متر مربع</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
