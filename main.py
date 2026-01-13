import streamlit as st
import pandas as pd
import math
import feedparser  # مكتبة سحب الأخبار التلقائية
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
        'dir': "rtl", 'align': "right", 'news_title': "🚀 أخبار السوق الآن:"
    },
    'English': {
        'title': "Ma3lomati Real Estate", 'projects': "🏗️ Projects", 'devs': "🏢 Developers", 
        'tools': "🛠️ Tools", 'logout': "🚪 Logout", 'search': "🔍 Search...", 
        'filter_area': "📍 Area Filter", 'details': "🔎 Details", 'next': "Next ➡️", 'prev': "⬅️ Prev", 
        'dir': "ltr", 'align': "left", 'news_title': "🚀 Market News:"
    }
}
T = ui[st.session_state.lang]

# 3. وظيفة جلب الأخبار الحقيقية تلقائياً
@st.cache_data(ttl=1800) # تحديث الأخبار كل 30 دقيقة
def get_real_news():
    # رابط أخبار العقارات والاقتصاد من مصدر مصري موثوق
    rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" # قسم العقارات/الاقتصاد
    feed = feedparser.parse(rss_url)
    news_items = [item.title for item in feed.entries[:10]] # جلب آخر 10 أخبار
    if not news_items:
        return ["جاري تحديث أخبار السوق المصري..."]
    return news_items

news_list = get_real_news()
news_text = "  •  ".join(news_list)

# 4. التنسيق (CSS) مع أنيميشن الشريط
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ 
        background-color: #050505; direction: {T['dir']} !important; 
        text-align: {T['align']} !important; font-family: 'Cairo', sans-serif; 
    }}
    .oval-header {{ background-color: #000; border: 3px solid #f59e0b; border-radius: 50px; padding: 10px 20px; width: fit-content; margin: 10px auto 5px auto; text-align: center; }}
    .header-title {{ color: #f59e0b; font-weight: 900; font-size: 22px !important; margin: 0; }}
    
    /* شريط الأخبار المتحرك */
    .ticker-wrap {{ width: 100%; background-color: #1a1a1a; border-bottom: 2px solid #f59e0b; padding: 6px 0; margin-bottom: 10px; overflow: hidden; white-space: nowrap; }}
    .ticker {{ display: inline-block; animation: ticker 40s linear infinite; color: #fff; font-size: 14px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    .ticker b {{ color: #f59e0b; margin-right: 10px; }}
    </style>
""", unsafe_allow_html=True)

# 5. جلب بيانات الشيت
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
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 6. تسجيل الدخول (بشكل مختصر)
if not st.session_state.auth:
    st.markdown(f'<div class="oval-header"><h1 class="header-title">{T["title"]}</h1></div>', unsafe_allow_html=True)
    if st.text_input("Pass", type="password") == "2026": 
        st.session_state.auth = True; st.rerun()
    st.stop()

# شريط التحكم
c1, c2 = st.columns([1, 1])
with c1: 
    if st.button(T['logout']): st.session_state.auth = False; st.rerun()
with c2:
    if st.button("🌐 EN/AR"): 
        st.session_state.lang = 'English' if st.session_state.lang == 'Arabic' else 'Arabic'
        st.rerun()

# الهيدر والشريط الإخباري
st.markdown(f'<div class="oval-header"><h1 class="header-title">{T["title"]}</h1></div>', unsafe_allow_html=True)

st.markdown(f"""
    <div class="ticker-wrap">
        <div class="ticker">
            <b>{T['news_title']}</b> {news_text} &nbsp;&nbsp;&nbsp;&nbsp; <b>{T['news_title']}</b> {news_text}
        </div>
    </div>
""", unsafe_allow_html=True)

# المنيو الرئيسي
menu = option_menu(None, [T['tools'], T['projects'], T['devs']], icons=["tools", "building", "person-vcard"], orientation="horizontal")

# التصميم الـ 70%
if st.session_state.lang == 'Arabic': main_col, _ = st.columns([0.7, 0.3])
else: _, main_col = st.columns([0.3, 0.7])

with main_col:
    if menu == T['projects']:
        st.markdown(f"<h2 style='color:#f59e0b;'>{T['projects']}</h2>", unsafe_allow_html=True)
        # هنا يوضع كود الشبكة وعرض المشاريع الذي أعددناه سابقاً...
        st.success("بيانات المشاريع جاهزة ومحدثة.")
