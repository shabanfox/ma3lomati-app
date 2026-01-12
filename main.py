import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS) - ضبط المحاذاة لليمين 100%
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; }
    .main-header { background: linear-gradient(90deg, #111 0%, #000 100%); padding: 15px; border-radius: 0 0 15px 15px; border-right: 12px solid #f59e0b; text-align: center; margin-bottom: 25px; }
    .header-title { font-weight: 900; font-size: 30px !important; color: #f59e0b; margin: 0; }
    
    /* تنسيق الكروت */
    .pro-card { background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; border-radius: 12px; padding: 20px; text-align: right; height: 100%; min-height: 200px; }
    .card-title { color: #f59e0b; font-size: 19px !important; font-weight: 900; margin-bottom: 10px; }
    
    /* صناديق التفاصيل */
    .detail-box { background: #0d0d0d; border-right: 6px solid #f59e0b; border-radius: 12px; padding: 25px; color: #eee; border: 1px solid #222; text-align: right; }
    
    /* أدوات البروكر */
    .tool-container { background: #111; border-radius: 15px; padding: 20px; border: 1px solid #222; margin-bottom: 20px; text-align: right; }
    
    /* العناوين الجانبية */
    .right-title { color: #f59e0b; text-align: right; font-weight: 900; margin-bottom: 20px; border-bottom: 2px solid #222; padding-bottom: 10px; }
    
    /* الأزرار */
    .stButton button { background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; border-radius: 8px; font-weight: bold; width: 100%; }
    
    /* إخفاء عناصر ستريمليت الافتراضية */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. وظيفة جلب ودمج البيانات
@st.cache_data(ttl=60)
def load_combined_data():
    urls = [
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv",
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    ]
    all_dfs = []
    for url in urls:
        try:
            temp_df = pd.read_csv(url)
            temp_df.columns = [str(c).strip() for c in temp_df.columns]
            all_dfs.append(temp_df)
        except: continue
    if not all_dfs: return pd.DataFrame()
    return pd.concat(all_dfs, ignore_index=True).fillna("غير متوفر").astype(str)

df = load_combined_data()

# 4. إدارة الجلسة
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'd_page' not in st.session_state: st.session_state.d_page = 0
if 'active_proj' not in st.session_state: st.session_state.active_proj = None
if 'active_dev' not in st.session_state: st.session_state.active_dev = None

# الهيدر والمنيو
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي العقارية PRO</h1></div>', unsafe_allow_html=True)

selected = option_menu(None, ["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
                       icons=["tools", "building", "person-badge"], orientation="horizontal",
                       styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}})

# --- 🏗️ قسم المشاريع ---
if selected == "🏗️ المشاريع":
    st.markdown("<h2 class='right-title'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
    
    search_p = st.text_input("🔍 ابحث باسم المشروع، المطور، أو المنطقة...")
    dff = df.copy()
    if search_p:
        dff = dff[dff.apply(lambda row: search_p.lower() in row.astype(str).str.lower().values, axis=1)]

    items_p = 6
    total_p = max(1, math.ceil(len(dff) / items_p))
    start_idx = st.session_state.p_page * items_p
    curr_p = dff.iloc[start_idx : start_idx + items_p].reset_index()

    for i in range(0, len(curr_p), 2): # عرض 2 في كل صف لراحة العين
        row_ids = curr_p['index'].iloc[i:i+2].tolist()
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(curr_p):
                item = curr_p.iloc[i+j]
                with cols[j]:
                    st.markdown(f"""<div class='pro-card'>
                        <div class='card-title'>{item['Project Name']}</div>
                        <p style='color:#888;'>🏢 {item['Developer']}</p>
                        <p style='color:#f59e0b; font-size:14px;'>📍 {item['Area']}</p>
                    </div>""", unsafe_allow_html=True)
                    if st.button("🔍 عرض التفاصيل الكاملة", key=f"btn_p_{item['index']}"):
                        st.session_state.active_proj = item['index']

        # عرض التفاصيل أسفل الكارت المختار
        if st.session_state.active_proj in row_ids:
            p_data = df.loc[st.session_state.active_proj]
            st.markdown(f"""<div class='detail-box'>
                <h3 style='color:#f59e0b;'>📋 {p_data['Project Name']}</h3>
                <p><b>📏 المساحة:</b> {p_data['Size (Acres)']} فدان | <b>👷 الاستشاري:</b> {p_data['Consultant']}</p>
                <p><b>⭐ المميزات:</b> {p_data['Competitive Advantage']}</p>
                <p><b>👤 المالك:</b> {p_data['Owner']}</p>
                <hr style='border-color:#222'>
                <p><b>📜 نبذة:</b> {p_data['Detailed_Info']}</p>
            </div>""", unsafe_allow_html=True)
            if st.button("⬅️ إغلاق التفاصيل", key="close_p"):
                st.session_state.active_proj = None; st.rerun()

    # أزرار التنقل
    st.write("---")
    n1, n2, n3 = st.columns([1, 2, 1])
    if n3.button("التالي ⬅️", key="p_next") and st.session_state.p_page < total_p - 1:
        st.session_state.p_page += 1; st.rerun()
    n2.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.p_page + 1} من {total_p}</p>", unsafe_allow_html=True)
    if n1.button("➡️ السابق", key="p_prev") and st.session_state.p_page > 0:
        st.session_state.p_page -= 1; st.rerun()

# --- 🏢 قسم المطورين ---
elif selected == "🏢 المطورين":
    st.markdown("<h2 class='right-title'>🏢 دليل المطورين</h2>", unsafe_allow_html=True)
    devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
    
    search_d = st.text_input("🔍 ابحث عن اسم المطور...")
    if search_d: devs = devs[devs['Developer'].str.contains(search_d, case=False)]

    items_d = 6
    total_d = max(1, math.ceil(len(devs) / items_d))
    curr_d = devs.iloc[st.session_state.d_page * items_d : (st.session_state.d_page + 1) * items_d].reset_index()

    for i in range(0, len(curr_d), 2):
        row_indices = curr_d['index'].iloc[i:i+2].tolist()
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(curr_d):
                item = curr_d.iloc[i+j]
                with cols[j]:
                    st.markdown(f"<div class='pro-card'><div class='card-title'>{item['Developer']}</div><p>👤 {item['Owner']}</p></div>", unsafe_allow_html=True)
                    if st.button("📂 عرض الملف الضريبي والفني", key=f"btn_d_{item['index']}"):
                        st.session_state.active_dev = item['index']

        if st.session_state.active_dev in row_indices:
            d_data = devs.iloc[st.session_state.active_dev]
            st.markdown(f"""<div class='detail-box'>
                <h3 style='color:#f59e0b;'>🏢 شركة {d_data['Developer']}</h3>
                <p><b>👤 رئيس مجلس الإدارة:</b> {d_data['Owner']}</p>
                <p><b>📜 التاريخ والمشاريع:</b><br>{d_data['Detailed_Info']}</p>
            </div>""", unsafe_allow_html=True)
            if st.button("⬅️ إغلاق الملف", key="close_d"):
                st.session_state.active_dev = None; st.rerun()

    st.write("---")
    d1, d2, d3 = st.columns([1, 2, 1])
    if d3.button("التالي ⬅️", key="d_next") and st.session_state.d_page < total_d - 1:
        st.session_state.d_page += 1; st.rerun()
    d2.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.d_page + 1} من {total_d}</p>", unsafe_allow_html=True)
    if d1.button("➡️ السابق", key="d_prev") and st.session_state.d_page > 0:
        st.session_state.d_page -= 1; st.rerun()

# --- 🛠️ قسم الأدوات بالكامل ---
elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 class='right-title'>🛠️ حقيبة أدوات البروكر الذكية</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([0.5, 0.5])
    
    with col1:
        st.markdown("<div class='tool-container'>", unsafe_allow_html=True)
        st.markdown("### 💰 حاسبة الأقساط المتقدمة")
        price = st.number_input("إجمالي السعر (ج.م)", value=5000000, step=100000)
        down = st.slider("المقدم (%)", 0, 50, 10)
        years = st.number_input("عدد سنوات التقسيط", value=8, min_value=1)
        
        dp_val = price * (down/100)
        monthly = (price - dp_val) / (years * 12)
        st.markdown(f"<div style='background:#000; padding:10px; border-radius:10px;'><h4>المقدم: {dp_val:,.0f}</h4><h2 style='color:#f59e0b;'>{monthly:,.0f} ج.م/شهري</h2></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='tool-container'>", unsafe_allow_html=True)
        st.markdown("### 📏 محول المساحات")
        ac = st.number_input("المساحة بالفدان", value=1.0)
        st.markdown(f"<h2 style='color:#f59e0b;'>{ac * 4200:,.0f} متر مربع</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='tool-container'>", unsafe_allow_html=True)
        st.markdown("### 📝 مفكرة متابعة العملاء")
        st.text_area("سجل هنا ملاحظاتك، اتصالاتك، ومواعيد المعاينات...", height=420)
        st.button("💾 حفظ الملاحظات (مؤقت)")
        st.markdown("</div>", unsafe_allow_html=True)
