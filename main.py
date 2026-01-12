import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide")

# 2. وظيفة جلب البيانات من الرابط الجديد
@st.cache_data(ttl=60)
def load_data():
    # الرابط الذي أرسلته (محول بصيغة CSV للقراءة)
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        data = pd.read_csv(url)
        # تنظيف أسماء الأعمدة من أي مسافات زائدة
        data.columns = [str(c).strip() for c in data.columns]
        return data.fillna("غير متوفر").astype(str)
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")
        return pd.DataFrame()

df = load_data()

# 3. واجهة المستخدم والتنسيق (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    body { direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #050505; color: white; }
    .main-header { background: linear-gradient(90deg, #111 0%, #000 100%); padding: 20px; border-radius: 15px; border-right: 10px solid #f59e0b; margin-bottom: 20px; text-align: center; }
    .pro-card { background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; border-radius: 12px; padding: 15px; margin-bottom: 10px; height: 180px; }
    .detail-box { background: #0d0d0d; border-right: 6px solid #f59e0b; padding: 20px; border-radius: 12px; border: 1px solid #222; }
    .stat-line { display: flex; justify-content: space-between; border-bottom: 1px solid #1a1a1a; padding: 8px 0; }
    .stat-label { color: #888; }
    .stat-val { color: #f59e0b; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 4. إدارة الصفحات والتنقل
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'active_proj' not in st.session_state: st.session_state.active_proj = None

st.markdown('<div class="main-header"><h1 style="color:#f59e0b;">🏗️ نظام معلومات العقارات الذكي</h1></div>', unsafe_allow_html=True)

# المنيو الرئيسي
selected = option_menu(None, ["المشاريع", "المطورين", "حاسبة القرض"], 
    icons=["building", "person-badge", "calculator"], orientation="horizontal")

if selected == "المشاريع":
    st.subheader("🔍 استعراض المشاريع من قاعدة البيانات")
    
    # فلترة سريعة
    search_q = st.text_input("ابحث باسم المشروع أو المطور...")
    dff = df.copy()
    if search_q:
        dff = dff[dff['Project Name'].str.contains(search_q, case=False) | dff['Developer'].str.contains(search_q, case=False)]

    # نظام الترقيم (Pagination)
    items_per_page = 6
    total_pages = math.ceil(len(dff) / items_per_page)
    start_idx = st.session_state.p_page * items_per_page
    curr_items = dff.iloc[start_idx : start_idx + items_per_page]

    # عرض المشاريع
    for idx, row in curr_items.iterrows():
        with st.container():
            col_card, col_det = st.columns([0.3, 0.7])
            with col_card:
                st.markdown(f"""<div class="pro-card">
                    <h3 style="color:#f59e0b;">{row['Project Name']}</h3>
                    <p>🏢 {row['Developer']}</p>
                    <p style="font-size:12px; color:#666;">📍 {row['Area']}</p>
                </div>""", unsafe_allow_html=True)
                if st.button(f"تفاصيل {row['Project Name']}", key=f"btn_{idx}"):
                    st.session_state.active_proj = idx
            
            with col_det:
                if st.session_state.active_proj == idx:
                    st.markdown(f"""<div class="detail-box">
                        <h4>📋 تفاصيل المشروع والمطور</h4>
                        <div class="stat-line"><span class="stat-label">👷 الاستشاري:</span><span class="stat-val">{row['Consultant']}</span></div>
                        <div class="stat-line"><span class="stat-label">📏 المساحة:</span><span class="stat-val">{row['Size (Acres)']} فدان</span></div>
                        <div class="stat-line"><span class="stat-label">⭐ الميزة التنافسية:</span><span class="stat-val">{row['Competitive Advantage']}</span></div>
                        <div class="stat-line"><span class="stat-label">👤 المالك:</span><span class="stat-val">{row['Owner']}</span></div>
                        <p style="margin-top:10px;"><b>ℹ️ عن المطور:</b> {row['Detailed_Info']}</p>
                    </div>""", unsafe_allow_html=True)

    # أزرار التالي والسابق
    st.write("---")
    b1, b2, b3 = st.columns([1, 2, 1])
    if b1.button("➡️ السابق") and st.session_state.p_page > 0:
        st.session_state.p_page -= 1; st.rerun()
    b2.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.p_page + 1} من {total_pages}</p>", unsafe_allow_html=True)
    if b3.button("التالي ⬅️") and st.session_state.p_page < total_pages - 1:
        st.session_state.p_page += 1; st.rerun()

elif selected == "حاسبة القرض":
    st.subheader("💰 الحاسبة العقارية")
    # (هنا تضع كود الحاسبة السابق كما هو)
    st.info("تم ربط هذه الحاسبة ببيانات الأسعار في الشيت قريباً.")
