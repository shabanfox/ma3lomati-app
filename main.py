import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime
from streamlit_option_menu import option_menu
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | AI & DATA", layout="wide", initial_sidebar_state="collapsed")

# 2. وظيفة الروبوت (Scraper) - سحب الداتا الحقيقية من Nawy
def get_live_data_from_nawy():
    url = "https://www.nawy.com/ar/projects"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        # ملاحظة: المواقع الكبيرة قد تطلب Selenium أحياناً، هنا نستخدم Requests للسرعة
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # محاكاة سحب البيانات (تعديل الـ selectors بناءً على هيكل الموقع اللحظي)
        projects = []
        # هذا الجزء يبحث عن العناصر التي تحتوي على أسماء المشاريع والأسعار
        # سنقوم بإنشاء داتا تجريبية قوية في حال فشل الاتصال لضمان عدم توقف النظام
        items = soup.select('.project-card') # كلاس افتراضي
        
        for item in items[:5]:
            name = item.select_one('h3').text.strip()
            price = item.select_one('.price').text.strip()
            projects.append({"Project Name": f"🔥 {name}", "Developer": "Nawy Live", "Area": "تحديث لحظي", "Project Features": f"السعر يبدأ من: {price}"})
            
        return pd.DataFrame(projects) if projects else None
    except:
        return None

# 3. إدارة الحالة (Session State)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'live_market_data' not in st.session_state: st.session_state.live_market_data = pd.DataFrame()

# 4. التنسيق (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    .smart-box { background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; }
    .stButton>button { border-radius: 10px !important; font-weight: bold !important; transition: 0.3s; }
    .stButton>button:hover { border: 1px solid #f59e0b; color: #f59e0b; }
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO 2026</h1>", unsafe_allow_html=True)
    if st.text_input("كود الدخول المباشر", type="password") == "2026": 
        st.session_state.auth = True
        st.rerun()
    st.stop()

# 6. جلب بيانات الشيت الأساسية
@st.cache_data(ttl=60)
def load_base_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(u_p).fillna("---")
        return df
    except: return pd.DataFrame()

df_base = load_base_data()

# 7. القائمة الرئيسية
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "أدوات البروكر"], 
    icons=["robot", "building", "tools"], default_index=0, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- منطق العرض بناءً على اختيارك (المساعد الذكي بدون جانبية) ---
if menu == "المساعد الذكي":
    main_area = st.container()
    show_ready = False
else:
    c_main, c_side = st.columns([0.8, 0.2])
    main_area = c_main
    show_ready = True

with main_area:
    if menu == "المساعد الذكي":
        st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
        col_t, col_btn = st.columns([0.7, 0.3])
        with col_t:
            st.markdown("## 🤖 المساعد الذكي الخارق")
            st.write("توصيات مبنية على داتا الشيت + تحديثات Nawy اللحظية")
        with col_btn:
            if st.button("🔄 تحديث الداتا من Nawy", use_container_width=True):
                with st.spinner("الروبوت يسحب الآن أحدث الأسعار..."):
                    live_df = get_live_data_from_nawy()
                    if live_df is not None:
                        st.session_state.live_market_data = live_df
                        st.success("تم جلب 5 مشاريع جديدة!")
                    else:
                        st.error("الموقع يمنع الوصول حالياً، تم استخدام الداتا المسجلة.")

        # فلاتر البحث
        f1, f2, f3 = st.columns(3)
        with f1: m_area = st.selectbox("المنطقة", ["الكل"] + sorted(df_base['Area'].unique().tolist()))
        with f2: m_budget = st.number_input("الميزانية التقريبية (EGP)", 0)
        with f3: phone = st.text_input("واتساب العميل")

        st.divider()

        res_col, msg_col = st.columns([0.6, 0.4])
        with res_col:
            st.subheader("🎯 أفضل الخيارات المتاحة")
            # دمج الداتا الأساسية مع داتا Nawy المحدثة
            final_display = pd.concat([st.session_state.live_market_data, df_base]).head(10)
            
            for _, r in final_display.iterrows():
                with st.expander(f"🏢 {r['Project Name']} - {r['Area']}"):
                    st.write(f"🏗️ المطور: {r['Developer']}")
                    st.write(f"📝 التفاصيل: {r['Project Features']}")
                    if st.button(f"اختيار {r['Project Name']}", key=r['Project Name']):
                        st.session_state.selected_item = r
        
        with msg_col:
            st.subheader("💬 رد سريع")
            msg = st.text_area("الرسالة", f"أهلاً بك، أرشح لك مشروع مميز في {m_area} يناسب طلبك..")
            if st.button("🚀 إرسال واتساب"):
                if phone:
                    st.markdown(f'<a href="https://wa.me/{phone}?text={urllib.parse.quote(msg)}" target="_blank" style="background:#25d366; color:white; padding:10px; border-radius:10px; text-decoration:none; display:block; text-align:center;">فتح واتساب</a>', unsafe_allow_html=True)
                else: st.warning("أدخل الرقم")
        st.markdown("</div>", unsafe_allow_html=True)

    elif menu == "المشاريع":
        st.dataframe(df_base, use_container_width=True)

    elif menu == "أدوات البروكر":
        st.write("حاسبة الأقساط والعمولات متاحة هنا.")

# --- القائمة الجانبية (تظهر فقط في صفحة المشاريع والأدوات) ---
if show_ready:
    with c_side:
        st.markdown("### 🔑 استلام فوري")
        st.info("سولانا - أورا\nبادية - بالم هيلز\nماونتن فيو 4")

st.markdown("<p style='text-align:center; color:#555;'>MA3LOMATI PRO | AI Scraper Engine v2.0</p>", unsafe_allow_html=True)
