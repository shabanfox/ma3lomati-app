import streamlit as st
import pandas as pd
import requests
import feedparser
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة
st.set_page_config(page_title="KMT PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# تحديث الصفحة كل ثانية لمزامنة الساعة
st_autorefresh(interval=1000, key="datetimerefresh")

# 2. روابط البيانات (Google Sheets)
# رابط الـ Script الخاص بك للتعامل مع تسجيل المستخدمين
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
# روابط ملفات CSV للمشاريع والمطورين
URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"

# 3. إدارة حالة الجلسة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 4. التنسيق الجمالي الشامل (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Orbitron:wght@500&display=swap');
    
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    
    /* نصوص تسجيل الدخول */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 50px; }
    .stTabs [data-baseweb="tab"] { font-size: 30px !important; font-weight: 900 !important; color: #666 !important; }
    .stTabs [aria-selected="true"] { color: #f59e0b !important; border-bottom: 4px solid #f59e0b !important; }
    
    label { font-size: 24px !important; color: #f59e0b !important; font-weight: bold !important; text-align: right !important; display: block; }
    input { font-size: 22px !important; background-color: #111 !important; color: white !important; border: 1px solid #333 !important; border-radius: 10px !important; }

    /* الأزرار الذهبية */
    div.stButton > button { border-radius: 15px !important; font-weight: 900 !important; transition: 0.3s; width: 100% !important; }
    .login-btn button { height: 75px !important; font-size: 28px !important; background-color: #f59e0b !important; color: black !important; }
    .logout-btn button { background-color: #ff4b4b !important; color: white !important; font-size: 14px !important; height: 40px !important; }

    /* كروت المشاريع (أسود فخم) */
    div.stButton > button[key*="card_"] {
        background-color: #111 !important; color: #f59e0b !important;
        min-height: 150px !important; text-align: right !important;
        border: 1px solid #222 !important; border-right: 10px solid #f59e0b !important;
        font-size: 18px !important; margin-bottom: 10px !important;
    }
    div.stButton > button[key*="card_"]:hover { background-color: #1a1a1a !important; border-color: #f59e0b !important; }

    /* شريط الأخبار البطيء */
    .ticker-wrap { width: 100%; background: #000; padding: 10px 0; overflow: hidden; border-bottom: 1px solid #222; margin: 15px 0; }
    .ticker { display: inline-block; animation: ticker 150s linear infinite; color: #f59e0b; font-size: 16px; font-weight: bold; white-space: nowrap; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    .smart-box { background: #111; border: 1px solid #222; padding: 25px; border-radius: 20px; border-right: 6px solid #f59e0b; color: white; }
    .side-card { background: #161616; padding: 12px; border-radius: 12px; border: 1px solid #222; margin-bottom: 8px; color: #f59e0b; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 5. وظائف النظام (دخول / بيانات / أخبار)
def login_user(u, p):
    try:
        res = requests.get(f"{SCRIPT_URL}?nocache={time.time()}")
        if res.status_code == 200:
            for user in res.json():
                if (str(user.get('Email')).lower() == u.lower() or str(user.get('Name')).lower() == u.lower()) and str(user.get('Password')) == p:
                    return user.get('Name')
        return None
    except: return None

@st.cache_data(ttl=600)
def load_data():
    try:
        p = pd.read_csv(URL_PROJECTS).fillna("---")
        d = pd.read_csv(URL_DEVELOPERS).fillna("---")
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

@st.cache_data(ttl=3600)
def fetch_news():
    try:
        feed = feedparser.parse("https://www.youm7.com/rss/SectionRss?SectionID=297")
        return "  •  ".join([item.title for item in feed.entries[:10]])
    except: return "KMT PRO: بوابة العقارات المصرية الذكية"

# 6. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:50px;'><h1 style='color:#f59e0b; font-size:80px; font-weight:900;'>KMT PRO</h1></div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["SIGN IN", "CREATE ACCOUNT"])
    with tab1:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            u_in = st.text_input("Username / Email")
            p_in = st.text_input("Password", type="password")
            st.markdown('<div class="login-btn">', unsafe_allow_html=True)
            if st.button("LOGIN TO SYSTEM 🚀"):
                if p_in == "2026": # كلمة سر للمطور
                    st.session_state.auth, st.session_state.current_user = True, "Admin"
                    st.rerun()
                else:
                    user_name = login_user(u_in, p_in)
                    if user_name:
                        st.session_state.auth, st.session_state.current_user = True, user_name
                        st.rerun()
                    else: st.error("Invalid Credentials")
            st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 7. الهيدر العلوي (الساعة واليوزر)
egypt_now = datetime.now(pytz.timezone('Africa/Cairo'))
c_h1, c_h2, c_h3 = st.columns([0.5, 0.35, 0.15])
with c_h1:
    st.markdown(f"<div style='color:#f59e0b; font-weight:bold; padding-top:10px;'>👤 {st.session_state.current_user}</div>", unsafe_allow_html=True)
with c_h2:
    st.markdown(f"""<div style='text-align: left; padding-top: 8px;'>
        <span style='color: #f59e0b; font-size: 22px; font-weight: bold; font-family: "Orbitron";'>{egypt_now.strftime('%I:%M:%S %p')}</span>
        <span style='color: #444; margin: 0 10px;'>|</span>
        <span style='color: #888; font-size: 14px;'>{egypt_now.strftime('%Y-%m-%d')}</span>
    </div>""", unsafe_allow_html=True)
with c_h3:
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("Logout"): st.session_state.auth = False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# الهيدر الصوري
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 180px; background-size: cover; background-position: center; border-radius: 25px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 5px solid #f59e0b; margin-top:5px;">
        <h1 style="color: white; margin: 0; font-size: 55px; font-weight:900; letter-spacing: 5px;">KMT PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-size: 18px;">EGYPTIAN REAL ESTATE INTELLIGENCE</p>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {fetch_news()}</div></div>', unsafe_allow_html=True)

# 8. المنيو الرئيسي والبيانات
df_p, df_d = load_data()
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "حقيبة البروكر"], 
    icons=["robot", "search", "building", "briefcase"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# 9. الصفحات والخدمات
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"<div class='smart-box'><h2>{item.get('ProjectName', item.get('Developer'))}</h2><hr><p>📍 الموقع: {item.get('Location', '---')}</p><p>🏗️ المطور: {item.get('Developer', '---')}</p><p>💰 تفاصيل: {item.get('Payment Plan', 'متوفرة عند الطلب')}</p></div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    m_col, s_col = st.columns([0.7, 0.3])
    with s_col:
        st.markdown("<h4 style='color:#10b981; text-align:center;'>🔑 استلام فوري</h4>", unsafe_allow_html=True)
        ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(10)
        for i, r in ready.iterrows():
            if st.button(f"✅ {r['ProjectName']}", key=f"ready_{i}"): st.session_state.selected_item = r; st.rerun()
    with m_col:
        search = st.text_input("🔍 ابحث عن اسم مشروع...")
        dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
        for i in range(0, len(dff.head(6)), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(dff.head(6)):
                    row = dff.iloc[i+j]
                    if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}", key=f"card_p_{i+j}"):
                        st.session_state.selected_item = row; st.rerun()

elif menu == "المطورين":
    m_col, s_col = st.columns([0.7, 0.3])
    with s_col:
        st.markdown("<h4 style='color:#f59e0b; text-align:center;'>🏆 أفضل المطورين</h4>", unsafe_allow_html=True)
        for i, r in df_d.head(10).iterrows():
            st.markdown(f"<div class='side-card'>{i+1}. {r['Developer']}</div>", unsafe_allow_html=True)
    with m_col:
        search_d = st.text_input("🔍 ابحث عن مطور...")
        dfd_f = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
        for i in range(0, len(dfd_f.head(6)), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(dfd_f.head(6)):
                    row = dfd_f.iloc[i+j]
                    if cols[j].button(f"🏗️ {row['Developer']}\n⭐ الفئة: {row.get('Developer Category','A')}", key=f"card_d_{i+j}"):
                        st.session_state.selected_item = row; st.rerun()

elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'><h3>🤖 المساعد الذكي KMT</h3><p>اختر المنطقة ودع النظام يرشح لك أفضل المشاريع.</p></div>", unsafe_allow_html=True)
    loc = st.selectbox("📍 المنطقة", sorted(df_p['Location'].unique().tolist()))
    if st.button("🎯 ترشيح أفضل الوحدات"): st.success("جاري البحث في قاعدة البيانات...")

elif menu == "حقيبة البروكر":
    st.title("🛠️ أدوات البروكر")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='tool-card'><h3>💳 حساب القسط</h3>", unsafe_allow_html=True)
        v = st.number_input("السعر", 1000000)
        st.metric("شهرياً (8 سنوات)", f"{v/(8*12):,.0f}")
    with c2:
        st.markdown("<div class='tool-card'><h3>💰 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("الصفقة", 1000000)
        st.metric("صافي الربح", f"{deal*0.015:,.0f}")
    with c3:
        st.markdown("<div class='tool-card'><h3>📐 المساحة</h3>", unsafe_allow_html=True)
        m2 = st.number_input("بالمتر", 100)
        st.write(f"بالقدم: {m2*10.76:,.0f}")

st.markdown("<p style='text-align:center; color:#333; margin-top:50px;'>KMT PRO © 2026 | Powered by AI</p>", unsafe_allow_html=True)
