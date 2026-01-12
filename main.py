import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="معلوماتي PRO | العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي المتطور (Modern CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800;900&display=swap');
    
    .block-container { padding-top: 1rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top right, #0a0a0a, #050505);
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }

    /* شريط المهام العلوي */
    .top-info {
        display: flex; justify-content: space-between; align-items: center;
        background: rgba(255, 255, 255, 0.03); padding: 10px 25px;
        border-radius: 15px; border: 1px solid rgba(245, 158, 11, 0.1); margin-bottom: 20px;
    }

    /* زر الخروج بتصميم عصري */
    .stButton > button[key="logout_btn"] {
        background: linear-gradient(45deg, #ff4b4b, #b91c1c) !important;
        color: white !important; border: none !important; border-radius: 8px !important;
        font-weight: bold !important; transition: 0.3s !important;
    }

    /* الهيدر الرئيسي */
    .header-box {
        text-align: center; padding: 20px; margin-bottom: 30px;
        border-bottom: 2px solid #f59e0b; background: linear-gradient(180deg, rgba(245, 158, 11, 0.1) 0%, transparent 100%);
    }
    .header-title { font-weight: 900; font-size: 38px !important; color: #f59e0b; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }

    /* الكروت الاحترافية */
    .pro-card { 
        background: #111; border: 1px solid #222; border-radius: 15px; 
        padding: 25px; margin-bottom: 15px; transition: all 0.4s ease;
        position: relative; overflow: hidden;
    }
    .pro-card:hover { 
        border-color: #f59e0b; transform: translateY(-8px);
        box-shadow: 0 10px 25px rgba(245, 158, 11, 0.15);
    }
    .pro-card::before {
        content: ""; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: #f59e0b;
    }
    
    .card-tag {
        background: #f59e0b; color: #000; font-size: 10px; font-weight: 800;
        padding: 3px 10px; border-radius: 5px; float: left;
    }

    /* صندوق التفاصيل المطور */
    .detail-container {
        background: #0d0d0d; border-right: 6px solid #f59e0b;
        border-radius: 12px; padding: 30px; margin-bottom: 30px;
        box-shadow: inset 0 0 20px rgba(245, 158, 11, 0.05);
    }
    
    .stat-row { display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 14px; border-bottom: 1px solid #1a1a1a; padding-bottom: 6px; }
    .stat-label { color: #888; }
    .stat-value { color: #f59e0b; font-weight: 700; }

    /* تحسين شكل المدخلات */
    div[data-baseweb="input"] { background-color: #111 !important; border-radius: 10px !important; }
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

# 4. شريط المعلومات العلوي
st.markdown(f"""
    <div class="top-info">
        <div style="color: #f59e0b; font-weight: bold;">📅 {datetime.now().strftime('%Y-%m-%d')} | نظام إدارة المعلومات</div>
        <div style="color: #666; font-size: 12px;">مرحباً بك في لوحة التحكم البروكر</div>
    </div>
""", unsafe_allow_html=True)

# 5. القائمة الجانبية (زر الخروج)
with st.sidebar:
    st.markdown("### الإعدادات")
    if st.button("تسجيل الخروج", key="logout_btn"):
        st.session_state.clear()
        st.rerun()

# 6. الهيدر والقائمة
st.markdown('<div class="header-box"><h1 class="header-title">🏢 مـنـصـة مـعـلـومـاتـي PRO</h1></div>', unsafe_allow_html=True)

selected = option_menu(
    menu_title=None, 
    options=["🛠️ الأدوات", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["cpu", "buildings", "person-badge-fill"], 
    orientation="horizontal",
    styles={
        "container": {"background-color": "transparent", "padding": "0"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "5px", "--hover-color": "#222", "color": "#888"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "#000", "font-weight": "bold"},
    }
)

# تهيئة الـ State
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'd_page' not in st.session_state: st.session_state.d_page = 0
if 'view_dev' not in st.session_state: st.session_state.view_dev = None

# --- 🏗️ قسم المشاريع ---
if selected == "🏗️ المشاريع":
    if not df.empty:
        col_main, col_filter = st.columns([0.75, 0.25])
        with col_filter:
            st.markdown("#### 🔍 تصفية البحث")
            s_p = st.text_input("اسم المشروع")
            a_p = st.selectbox("المنطقة", ["الكل"] + sorted(df['Area'].unique().tolist()))
            
        with col_main:
            dff = df.copy()
            if s_p: dff = dff[dff['Project Name'].str.contains(s_p, case=False)]
            if a_p != "الكل": dff = dff[dff['Area'] == a_p]

            items = 6
            total_p = max(1, math.ceil(len(dff) / items))
            curr = dff.iloc[st.session_state.p_page * items : (st.session_state.p_page + 1) * items]

            for i in range(0, len(curr), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i+j < len(curr):
                        row = curr.iloc[i+j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="pro-card">
                                    <span class="card-tag">{row.get('شقق/فيلات', 'عقاري')}</span>
                                    <div style="color:#f59e0b; font-size:22px; font-weight:800; margin:10px 0;">{row.get('Project Name')}</div>
                                    <div style="color:#888; margin-bottom:15px;">{row.get('Developer')}</div>
                                    <div class="stat-row"><span class="stat-label">📍 الموقع</span><span class="stat-value">{row.get('Area')}</span></div>
                                    <div class="stat-row"><span class="stat-label">📏 المساحة</span><span class="stat-value">{row.get('Size (Acres)')} فدان</span></div>
                                    <div class="stat-row"><span class="stat-label">👷 الاستشاري</span><span class="stat-value">{row.get('Consultant')}</span></div>
                                    <div style="background:rgba(245,158,11,0.05); padding:10px; border-radius:8px; font-size:12px; color:#f59e0b; border:1px dashed #f59e0b;">
                                        🎯 {row.get('Competitive Advantage', 'تواصل للمزيد')}
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)

            # أزرار التنقل
            st.write("---")
            b1, b2, b3 = st.columns([1, 1, 1])
            if b3.button("الصفحة التالية ⬅️", key="pn"): st.session_state.p_page += 1; st.rerun()
            b2.markdown(f"<center> {st.session_state.p_page + 1} / {total_p} </center>", unsafe_allow_html=True)
            if b1.button("➡️ الصفحة السابقة", key="pp") and st.session_state.p_page > 0: st.session_state.p_page -= 1; st.rerun()

# --- 🏢 قسم المطورين ---
elif selected == "🏢 المطورين":
    if not df.empty:
        devs_list = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        
        if st.session_state.view_dev:
            dev_data = devs_list[devs_list['Developer'] == st.session_state.view_dev].iloc[0]
            st.markdown(f"""
                <div class="detail-container">
                    <h2 style="color:#f59e0b; font-weight:900;">🏢 {dev_data['Developer']}</h2>
                    <p style="font-size:20px;"><b>👤 رئيس مجلس الإدارة:</b> {dev_data['Owner']}</p>
                    <hr style="border-color:#222">
                    <p><b>📜 عن الشركة:</b><br>{dev_data['Detailed_Info']}</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("❌ إغلاق الملف"): st.session_state.view_dev = None; st.rerun()
        
        st.markdown("### قائمة المطورين المعتمدين")
        s_d = st.text_input("🔍 ابحث عن اسم المطور...")
        if s_d: devs_list = devs_list[devs_list['Developer'].str.contains(s_d, case=False)]

        for i in range(0, len(devs_list), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(devs_list):
                    row = devs_list.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="pro-card" style="min-height:150px; text-align:right;">
                                <div style="color:#f59e0b; font-size:20px; font-weight:800;">{row['Developer']}</div>
                                <div style="color:#666; font-size:13px;">المالك: {row['Owner']}</div>
                            </div>
                        """, unsafe_allow_html=True)
                        if st.button(f"🔍 فتح ملف {row['Developer']}", key=f"dev_{row['Developer']}"):
                            st.session_state.view_dev = row['Developer']; st.rerun()

# --- 🛠️ قسم الأدوات ---
elif selected == "🛠️ الأدوات":
    st.markdown("### 🛠️ الأدوات المساعدة للبروكر")
    t1, t2, t3 = st.tabs(["💰 حاسبة القسط", "📏 محول المساحات", "📝 مفكرة العميل"])
    
    with t1:
        st.markdown("<div class='pro-card'>", unsafe_allow_html=True)
        price = st.number_input("سعر الوحدة الإجمالي", value=1000000)
        years = st.slider("عدد سنوات التقسيط", 1, 15, 7)
        down_payment = st.number_input("المقدم المدفوع", value=0)
        monthly = (price - down_payment) / (years * 12)
        st.markdown(f"<h1 style='color:#f59e0b; text-align:center;'>{monthly:,.0f} ج.م / شهرياً</h1>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with t2:
        st.markdown("<div class='pro-card'>", unsafe_allow_html=True)
        acres = st.number_input("أدخل المساحة بالفدان", value=1.0)
        st.markdown(f"<h1 style='color:#f59e0b; text-align:center;'>{acres * 4200:,.0f} متر مربع</h1>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with t3:
        st.text_area("سجل ملاحظاتك مع العميل هنا، وقم بنسخها لاحقاً...", height=300)
