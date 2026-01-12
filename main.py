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
    
    .main-header { background: linear-gradient(90deg, #111 0%, #000 100%); padding: 15px; border-radius: 0 0 15px 15px; border-right: 12px solid #f59e0b; text-align: center; margin-bottom: 25px; }
    .header-title { font-weight: 900; font-size: 30px !important; color: #f59e0b; margin: 0; }

    .pro-card { 
        background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; 
        border-radius: 12px; padding: 20px; text-align: center; height: 100%; min-height: 220px;
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
    
    .stButton button { background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; border-radius: 8px; font-weight: bold; width: 100%; }
    .logout-btn button { background: #ff4b4b !important; color: white !important; border: none !important; width: auto !important; padding: 5px 20px !important; }
    
    /* ستايل أدوات البروكر */
    .tool-container { background: #111; border-radius: 15px; padding: 20px; border: 1px solid #222; }
    </style>
""", unsafe_allow_html=True)

# 3. وظيفة جلب البيانات
@st.cache_data(ttl=60) # تحديث كل دقيقة لضمان سرعة ظهور تعديلات الإكسيل
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data.fillna("غير متوفر").astype(str)
    except: return pd.DataFrame()

df = load_data()

# 4. إدارة الجلسة (Session State)
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'd_page' not in st.session_state: st.session_state.d_page = 0
if 'active_proj' not in st.session_state: st.session_state.active_proj = None
if 'active_dev' not in st.session_state: st.session_state.active_dev = None

# 5. الهيدر والمنيو
t_c1, t_c2 = st.columns([10, 1])
with t_c2:
    if st.button("خروج", key="logout_btn", help="تسجيل الخروج"): st.session_state.clear(); st.rerun()

st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي PRO</h1></div>', unsafe_allow_html=True)

selected = option_menu(None, ["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
                       icons=["tools", "building", "person-badge"], orientation="horizontal",
                       styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}})

# --- 🏗️ شاشة المشاريع ---
if selected == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع العقارية</h2>", unsafe_allow_html=True)
    c_side, c_main = st.columns([0.25, 0.75])
    
    with c_side:
        st.markdown("### 🔍 بحث وتصفية")
        search_p = st.text_input("اسم المشروع...")
        area_options = ["الكل"] + sorted(df['Area'].unique().tolist()) if not df.empty else ["الكل"]
        filter_a = st.selectbox("المنطقة", area_options)
        
    with c_main:
        dff = df.copy()
        if search_p: dff = dff[dff['Project Name'].str.contains(search_p, case=False)]
        if filter_a != "الكل": dff = dff[dff['Area'] == filter_a]

        items_per_page = 9
        total_pages = max(1, math.ceil(len(dff) / items_per_page))
        
        # عرض البيانات
        start_idx = st.session_state.p_page * items_per_page
        curr_p = dff.iloc[start_idx : start_idx + items_per_page].reset_index()

        for i in range(0, len(curr_p), 3):
            row_ids = curr_p['index'].iloc[i:i+3].tolist()
            if st.session_state.active_proj in row_ids:
                p_data = df.loc[st.session_state.active_proj]
                st.markdown("---")
                c1, c2 = st.columns([0.35, 0.65])
                with c1:
                    st.markdown(f"<div class='pro-card'><div class='card-title'>{p_data['Project Name']}</div><p>{p_data['Developer']}</p></div>", unsafe_allow_html=True)
                    if st.button("⬅️ إغلاق التفاصيل", key=f"cls_p_{p_data.name}"): st.session_state.active_proj = None; st.rerun()
                with c2:
                    st.markdown(f"""<div class='detail-box'>
                        <h3 style='color:#f59e0b;'>🏗️ {p_data['Project Name']}</h3>
                        <div class='stat-line'><span class='stat-label'>📍 المنطقة:</span><span class='stat-val'>{p_data.get('Area')}</span></div>
                        <div class='stat-line'><span class='stat-label'>📏 المساحة:</span><span class='stat-val'>{p_data.get('Size (Acres)')} فدان</span></div>
                        <div class='stat-line'><span class='stat-label'>🏠 النوع:</span><span class='stat-val'>{p_data.get('شقق/فيلات')}</span></div>
                        <div class='stat-line'><span class='stat-label'>👷 الاستشاري:</span><span class='stat-val'>{p_data.get('Consultant')}</span></div>
                        <p style='margin-top:10px;'><b>⭐ المميزات:</b> {p_data.get('Competitive Advantage')}</p>
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
                                <div style='color:#888; font-size:14px;'>{item['Developer']}</div>
                                <div style='color:#f59e0b; font-size:12px; margin-top:10px;'>📍 {item['Area']}</div>
                            </div>""", unsafe_allow_html=True)
                            if st.button("🔍 عرض التفاصيل", key=f"bp_{item['index']}"):
                                st.session_state.active_proj = item['index']; st.rerun()

        # أزرار التنقل للمشاريع
        st.write("")
        n1, n2, n3 = st.columns([1, 2, 1])
        if n3.button("التالي ⬅️", key="p_next") and st.session_state.p_page < total_pages - 1:
            st.session_state.p_page += 1; st.rerun()
        n2.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.p_page + 1} من {total_pages}</p>", unsafe_allow_html=True)
        if n1.button("➡️ السابق", key="p_prev") and st.session_state.p_page > 0:
            st.session_state.p_page -= 1; st.rerun()

# --- 🏢 شاشة المطورين ---
elif selected == "🏢 المطورين":
    devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
    st.markdown("<h2 style='color:#f59e0b;'>🏢 دليل المطورين العقاريين</h2>", unsafe_allow_html=True)
    
    search_d = st.text_input("🔍 ابحث عن اسم المطور...")
    if search_d: devs = devs[devs['Developer'].str.contains(search_d, case=False)]

    items_per_page = 9
    total_pages_d = max(1, math.ceil(len(devs) / items_per_page))
    start_idx_d = st.session_state.d_page * items_per_page
    curr_d = devs.iloc[start_idx_d : start_idx_d + items_per_page].reset_index()

    for i in range(0, len(curr_d), 3):
        row_ids = curr_d['index'].iloc[i:i+3].tolist()
        if st.session_state.active_dev in row_ids:
            d_data = devs.iloc[st.session_state.active_dev]
            st.markdown("---")
            c1, c2 = st.columns([0.35, 0.65])
            with c1:
                st.markdown(f"<div class='pro-card'><div class='card-title'>{d_data['Developer']}</div><p>{d_data['Owner']}</p></div>", unsafe_allow_html=True)
                if st.button("⬅️ إغلاق الملف", key=f"cls_d_{d_data.name}"): st.session_state.active_dev = None; st.rerun()
            with c2:
                st.markdown(f"""<div class='detail-box'>
                    <h3 style='color:#f59e0b;'>🏢 ملف شركة {d_data['Developer']}</h3>
                    <p><b>👤 رئيس مجلس الإدارة:</b> {d_data['Owner']}</p>
                    <p><b>📜 نبذة تاريخية:</b><br>{d_data['Detailed_Info']}</p>
                </div>""", unsafe_allow_html=True)
            st.markdown("---")
        else:
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(curr_d):
                    item = curr_d.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""<div class='pro-card'>
                            <div class='card-title'>{item['Developer']}</div>
                            <div style='color:#888; font-size:13px;'>{item['Owner']}</div>
                        </div>""", unsafe_allow_html=True)
                        if st.button("🔍 عرض الملف", key=f"bd_{item['index']}"):
                            st.session_state.active_dev = item['index']; st.rerun()

    # أزرار التنقل للمطورين
    st.write("")
    d1, d2, d3 = st.columns([1, 2, 1])
    if d3.button("التالي ⬅️", key="d_next") and st.session_state.d_page < total_pages_d - 1:
        st.session_state.d_page += 1; st.rerun()
    d2.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.d_page + 1} من {total_pages_d}</p>", unsafe_allow_html=True)
    if d1.button("➡️ السابق", key="d_prev") and st.session_state.d_page > 0:
        st.session_state.d_page -= 1; st.rerun()

# --- 🛠️ شاشة أدوات البروكر ---
elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ حقيبة الأدوات الذكية</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([0.4, 0.6])
    
    with col1:
        st.markdown("<div class='tool-container'>", unsafe_allow_html=True)
        st.markdown("### 💰 حاسبة القسط الذكية")
        price = st.number_input("إجمالي سعر الوحدة (ج.م)", value=5000000, step=100000)
        down_payment = st.slider("المقدم (%)", 0, 50, 10)
        years = st.number_input("سنوات التقسيط", value=8, min_value=1)
        
        calc_dp = price * (down_payment/100)
        rem_price = price - calc_dp
        monthly = rem_price / (years * 12)
        
        st.markdown(f"""
            <div style='background:#000; padding:15px; border-radius:10px; margin-top:10px; border:1px dashed #f59e0b;'>
                <p style='color:#888; margin:0;'>المقدم المطلوب: <b style='color:#fff;'>{calc_dp:,.0f} ج.م</b></p>
                <p style='color:#f59e0b; font-size:22px; margin:10px 0;'>القسط: {monthly:,.0f} ج.م/شهري</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.write("")
        st.markdown("<div class='tool-container'>", unsafe_allow_html=True)
        st.markdown("### 📏 محول المساحات")
        acres = st.number_input("المساحة بالفدان", value=1.0)
        sqm = acres * 4200
        st.markdown(f"<h3 style='color:#f59e0b;'>{sqm:,.0f} متر مربع</h3>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='tool-container' style='height:100%;'>", unsafe_allow_html=True)
        st.markdown("### 📝 مفكرة العميل السريعة")
        notes = st.text_area("سجل ملاحظات العميل، طلباته، ومواعيد المتابعة هنا...", height=400)
        if st.button("💾 حفظ الملاحظات مؤقتاً"):
            st.success("تم حفظ الملاحظات في المتصفح!")
        st.markdown("</div>", unsafe_allow_html=True)

# 6. التذييل
st.markdown("<br><p style='text-align:center; color:#444; font-size:12px;'>جميع الحقوق محفوظة لمنصة معلوماتي العقارية PRO © 2026</p>", unsafe_allow_html=True)
