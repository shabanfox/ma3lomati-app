import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = 'Arabic'

# نصوص الواجهة
ui = {
    'Arabic': {
        'title': "منصة معلوماتي العقارية", 'projects': "🏗️ المشاريع", 'devs': "🏢 المطورين", 
        'tools': "🛠️ الأدوات", 'logout': "🚪 خروج", 'search': "🔍 بحث...", 
        'filter_area': "📍 المنطقة", 'details': "🔎 التفاصيل", 'next': "التالي ⬅️", 'prev': "➡️ السابق", 
        'dir': "rtl", 'align': "right", 'news_title': "🔥 آخر الأخبار:"
    },
    'English': {
        'title': "Ma3lomati Real Estate", 'projects': "🏗️ Projects", 'devs': "🏢 Developers", 
        'tools': "🛠️ Tools", 'logout': "🚪 Logout", 'search': "🔍 Search...", 
        'filter_area': "📍 Area Filter", 'details': "🔎 Details", 'next': "Next ➡️", 'prev': "⬅️ Prev", 
        'dir': "ltr", 'align': "left", 'news_title': "🔥 Latest News:"
    }
}
T = ui[st.session_state.lang]

# 3. التنسيق المتقدم (CSS) - أضفنا كود الشريط الإخباري
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ 
        background-color: #050505; direction: {T['dir']} !important; 
        text-align: {T['align']} !important; font-family: 'Cairo', sans-serif; 
    }}
    .oval-header {{ background-color: #000; border: 3px solid #f59e0b; border-radius: 50px; padding: 10px 30px; width: fit-content; margin: 10px auto 5px auto; text-align: center; }}
    .header-title {{ color: #f59e0b; font-weight: 900; font-size: 24px !important; margin: 0; }}
    
    /* تصميم شريط الأخبار */
    .ticker-wrap {{ width: 100%; overflow: hidden; background-color: #1a1a1a; border-bottom: 2px solid #f59e0b; padding: 5px 0; margin-bottom: 15px; }}
    .ticker {{ display: inline-block; white-space: nowrap; animation: ticker 30s linear infinite; color: #fff; font-size: 14px; }}
    .ticker-item {{ display: inline-block; padding: 0 50px; }}
    .ticker-title {{ background: #f59e0b; color: #000; padding: 5px 15px; font-weight: bold; position: absolute; z-index: 2; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    
    .grid-card {{ background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; border-radius: 12px; padding: 15px; min-height: 150px; }}
    .stButton button {{ background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; }}
    </style>
""", unsafe_allow_html=True)

# 4. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        df_p = pd.read_csv(u_p).fillna("").astype(str)
        df_d = pd.read_csv(u_d).fillna("").astype(str)
        df_p.columns = df_p.columns.str.strip()
        df_d.columns = df_d.columns.str.strip()
        return df_p, df_d
    except:
        return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 5. نظام الدخول
if not st.session_state.auth:
    st.markdown(f'<div class="oval-header"><h1 class="header-title">{T["title"]}</h1></div>', unsafe_allow_html=True)
    pwd = st.text_input("Pass", type="password")
    if st.button("OK"):
        if pwd == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# شريط التحكم العلوي
top_l, top_r = st.columns([1, 1])
with top_l:
    if st.button(T['logout']): st.session_state.auth = False; st.rerun()
with top_r:
    if st.button("🇺🇸 EN / 🇪🇬 AR"):
        st.session_state.lang = 'English' if st.session_state.lang == 'Arabic' else 'Arabic'
        st.rerun()

# الهيدر الأساسي
st.markdown(f'<div class="oval-header"><h1 class="header-title">{T["title"]}</h1></div>', unsafe_allow_html=True)

# --- 📢 الشريط الإخباري المتحرك ---
news_list = [
    "زيادة متوقعة في أسعار العقارات بنسبة 15% بداية من الشهر القادم",
    "فتح باب الحجز في المرحلة الجديدة من مشاريع العاصمة الإدارية",
    "مجموعة طلعت مصطفى تعلن عن مشروع ضخم جديد في الساحل الشمالي",
    "انخفاض طفيف في أسعار الحديد يؤثر إيجاباً على تكلفة الإنشاءات"
]
news_text = "  •  ".join(news_list)

st.markdown(f"""
    <div class="ticker-wrap">
        <div class="ticker">
            <span class="ticker-item"><b>{T['news_title']}</b> {news_text}</span>
            <span class="ticker-item"><b>{T['news_title']}</b> {news_text}</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# المنيو
menu = option_menu(None, [T['tools'], T['projects'], T['devs']], icons=["tools", "building", "person-vcard"], orientation="horizontal")

if st.session_state.lang == 'Arabic': main_col, _ = st.columns([0.7, 0.3])
else: _, main_col = st.columns([0.3, 0.7])

with main_col:
    if menu == T['projects']:
        st.markdown(f"<h2 style='color:#f59e0b;'>{T['projects']}</h2>", unsafe_allow_html=True)
        # (باقي كود المشاريع كما هو في الرد السابق...)
        st.info("قسم المشاريع مفعل وجاهز للعرض.")
        # ... يمكنك وضع كود عرض الشبكة هنا
        
    elif menu == T['devs']:
        st.markdown(f"<h2 style='color:#f59e0b;'>{T['devs']}</h2>", unsafe_allow_html=True)
        # (باقي كود المطورين...)
        
    elif menu == T['tools']:
        st.markdown(f"<h2 style='color:#f59e0b;'>{T['tools']}</h2>", unsafe_allow_html=True)
        # (باقي كود الأدوات...)
