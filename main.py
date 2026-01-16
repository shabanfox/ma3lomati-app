import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة حالة الجلسة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'live_market_data' not in st.session_state: st.session_state.live_market_data = pd.DataFrame()

# 3. وظيفة الروبوت لسحب البيانات (Nawy Scraper)
def get_live_data_from_nawy():
    url = "https://www.nawy.com/ar/projects"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        projects = []
        # محاولة سحب العناوين والأسعار
        for item in soup.select('.project-card')[:5]:
            name = item.select_one('h3').text.strip() if item.select_one('h3') else "مشروع جديد"
            projects.append({"Project Name": f"🔥 {name}", "Developer": "Nawy Live", "Area": "تحديث لحظي"})
        return pd.DataFrame(projects)
    except: return None

# 4. التنسيق الجمالي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    body, .stApp { background-color: #050505; color: white; font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .smart-box { background: #111; padding: 20px; border-radius: 15px; border-right: 5px solid #f59e0b; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    if st.text_input("كود الدخول", type="password") == "2026":
        st.session_state.auth = True; st.rerun()
    st.stop()

# 6. جلب بيانات الشيت
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try: return pd.read_csv(u_p).fillna("---")
    except: return pd.DataFrame()

df_p = load_data()

# 7. المنيو الرئيسي (تأكد من وجود كل الخيارات هنا)
selected = option_menu(
    menu_title=None,
    options=["المساعد الذكي", "قاعدة المشاريع", "أدوات البروكر"],
    icons=["robot", "building", "tools"],
    default_index=0,
    orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}}
)

# 8. عرض المحتوى بناءً على الاختيار
if selected == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 المساعد الذكي")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        m_area = st.selectbox("حدد المنطقة", ["الكل"] + sorted(df_p['Area'].unique().tolist()) if not df_p.empty else ["الكل"])
        if st.button("🔄 تحديث من Nawy (Data Scraper)"):
            live = get_live_data_from_nawy()
            if live is not None: st.session_state.live_market_data = live; st.success("تم التحديث!")
    
    with col2:
        phone = st.text_input("رقم واتساب العميل")
        broker = st.text_input("اسمك المرسل", "Agent")

    st.divider()
    
    # عرض النتائج
    res_df = pd.concat([st.session_state.live_market_data, df_p]).head(10)
    for _, r in res_df.iterrows():
        with st.expander(f"🏢 {r.get('Project Name')} | {r.get('Area')}"):
            st.write(f"المطور: {r.get('Developer')}")
            if st.button(f"إرسال تفاصيل {r.get('Project Name')}", key=r.get('Project Name')):
                msg = f"أهلاً بك، أرشح لك مشروع {r.get('Project Name')} في {r.get('Area')}. مع تحياتي {broker}"
                link = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
                st.markdown(f"[✅ اضغط هنا للإرسال لواتساب]({link})")
    st.markdown("</div>", unsafe_allow_html=True)

elif selected == "قاعدة المشاريع":
    st.title("📂 جميع المشاريع المسجلة")
    search = st.text_input("🔍 ابحث عن مشروع محدد بالاسم")
    if search:
        display_df = df_p[df_p['Project Name'].str.contains(search, case=False)]
    else:
        display_df = df_p
    st.dataframe(display_df, use_container_width=True)

elif selected == "أدوات البروكر":
    st.title("🛠️ حقيبة الأدوات")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("💳 حاسبة الأقساط")
        price = st.number_input("السعر الإجمالي", value=1000000)
        down = st.number_input("المقدم", value=100000)
        years = st.slider("السنين", 1, 15, 8)
        st.metric("القسط الشهري", f"{(price-down)/(years*12):,.0f}")
    with c2:
        st.subheader("📏 محول مساحات")
        meters = st.number_input("بالمتر المربع", value=100.0)
        st.write(f"تساوي: {meters * 10.76:.2f} قدم مربع")
