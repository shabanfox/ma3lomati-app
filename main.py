import streamlit as st
import pandas as pd
import requests
import feedparser
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="KMT PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# تحديث الصفحة كل ثانية لمزامنة الساعة الحية
st_autorefresh(interval=1000, key="global_clock_refresh")

# 2. روابط البيانات والربط (Google Sheets)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"

# 3. إدارة حالة الجلسة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 4. التنسيق الجمالي (CSS) - تصميم ملكي يمين (أسود وذهبي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Orbitron:wght@500&display=swap');
    
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    
    /* شاشة الدخول */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 50px; }
    .stTabs [data-baseweb="tab"] { font-size: 28px !important; font-weight: 900 !important; color: #666 !important; }
    .stTabs [aria-selected="true"] { color: #f59e0b !important; border-bottom: 4px solid #f59e0b !important; }
    
    label { font-size: 22px !important; color: #f59e0b !important; font-weight: bold !important; text-align: right !important; display: block; margin-bottom: 10px; }
    input { font-size: 20px !important; text-align: right !important; background-color: #111 !important; color: white !important; border: 1px solid #333 !important; border-radius: 12px !important; height: 50px !important; }

    /* الأزرار الذهبية والمنيو */
    div.stButton > button { border-radius: 12px !important; font-weight: 900 !important; transition: 0.3s; width: 100% !important; }
    .login-btn button { height: 70px !important; font-size: 26px !important; background-color: #f59e0b !important; color: black !important; border: none !important; }
    .logout-btn button { background-color: #ff4b4b !important; color: white !important; font-size: 14px !important; height: 35px !important; border: none !important; }

    /* كروت المشاريع السوداء والذهبية */
    div.stButton > button[key*="card_"] {
        background-color: #111 !important; color: #f59e0b !important;
        min-height: 140px !important; text-align: right !important;
        border: 1px solid #222 !important; border-right: 10px solid #f59e0b !important;
        font-size: 18px !important; line-height: 1.6 !important;
    }
    div.stButton > button[key*="card_"]:hover { background-color: #1a1a1a !important; border-color: #f59e0b !important; transform: translateY(-3px); }

    /* شريط الأخبار البطيء */
    .ticker-wrap { width: 100%; background: #000; padding: 12px 0; overflow: hidden; border-bottom: 1px solid #222; margin: 10px 0; }
    .ticker { display: inline-block; animation: ticker 140s linear infinite; color: #f59e0b; font-size: 15px; font-weight: bold; white-space: nowrap; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    .smart-box { background: #111; border: 1px solid #222; padding: 25px; border-radius: 20px; border-right: 6px solid #f59e0b; color: white; }
    .side-card { background: #161616; padding: 10px; border-radius: 10px; border: 1px solid #222; margin-bottom: 8px; color: #f59e0b; font-weight: bold; }
    .tool-card { background: #0c0c0c; padding: 20px; border-radius: 15px; border-top: 5px solid #f59e0b; text-align: center; border: 1px solid #222; }
    </style>
""", unsafe_allow_html=True)

# 5. الوظائف البرمجية (Logic)
def login_user(u, p):
    try:
        # إضافة طابع زمني لمنع الكاش
        res = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=10)
        if res.status_code == 200:
            users_list = res.json()
            for user in users_list:
                db_u = str(user.get('Email', user.get('Name', ''))).strip().lower()
                db_p = str(user.get('Password', '')).strip()
                if (u.strip().lower() == db_u) and (p.strip() == db_p):
                    return user.get('Name', u)
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
def get_news():
    try:
        feed = feedparser.parse("https://www.youm7.com/rss/SectionRss?SectionID=297")
        return "  •  ".join([item.title for item in feed.entries[:12]])
    except: return "KMT PRO: منصة البروكر العقاري الأولى في مصر 2026"

# 6. شاشة الدخول (Login Page)
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:60px;'><h1 style='color:#f59e0b; font-size:80px; font-weight:900;'>KMT PRO</h1><p style='color:#555; font-size:20px;'>AUTHENTICATION REQUIRED</p></div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["SIGN IN", "CREATE ACCOUNT"])
    
    with tab1:
        _, c2, _ = st.columns([1, 1.6, 1])
        with c2:
            u_in = st.text_input("Username / Email", key="log_u")
            p_in = st.text_input("Password", type="password", key="log_p")
            st.markdown('<div class="login-btn">', unsafe_allow_html=True)
            if st.button("LOGIN TO KMT SYSTEM 🚀"):
                # كلمة السر للطوارئ للفحص هي 2026
                if p_in == "2026":
                    st.session_state.auth, st.session_state.current_user = True, "Admin"
                    st.rerun()
                else:
                    user_found = login_user(u_in, p_in)
                    if user_found:
                        st.session_state.auth, st.session_state.current_user = True, user_found
                        st.rerun()
                    else:
                        st.error("Access Denied: Please check your credentials or internet connection.")
            st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 7. الهيدر العلوي الذكي (الساعة + اليوزر + الخروج)
egypt_now = datetime.now(pytz.timezone('Africa/Cairo'))
c_h1, c_h2, c_h3 = st.columns([0.45, 0.4, 0.15])
with c_h1:
    st.markdown(f"<div style='color:#f59e0b; font-weight:bold; padding-top:10px; font-size:18px;'>👤 مرحباً: {st.session_state.current_user}</div>", unsafe_allow_html=True)
with c_h2:
    st.markdown(f"""<div style='text-align: left; padding-top: 8px;'>
        <span style='color: #f59e0b; font-size: 22px; font-weight: bold; font-family: "Orbitron";'>{egypt_now.strftime('%I:%M:%S %p')}</span>
        <span style='color: #444; margin: 0 10px;'>|</span>
        <span style='color: #888; font-size: 14px;'>{egypt_now.strftime('%d-%m-%Y')}</span>
    </div>""", unsafe_allow_html=True)
with c_h3:
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("Logout"): 
        st.session_state.auth = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# الهيدر الصوري الملكي
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 180px; background-size: cover; background-position: center; border-radius: 25px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 5px solid #f59e0b; margin-top:5px;">
        <h1 style="color: white; margin: 0; font-size: 55px; font-weight:900; letter-spacing: 4px;">KMT PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-size: 18px; letter-spacing: 2px;">REAL ESTATE INTELLIGENCE SYSTEM</p>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {get_news()}</div></div>', unsafe_allow_html=True)

# 8. المنيو الرئيسي والبيانات
df_p, df_d = load_data()
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "حقيبة البروكر"], 
    icons=["robot", "search", "building", "briefcase"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# 9. الصفحات والخدمات التفصيلية
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة للقائمة"): 
        st.session_state.selected_item = None
        st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"""<div class='smart-box'>
        <h2>{item.get('ProjectName', item.get('Developer'))}</h2>
        <hr>
        <p style='font-size:20px;'>📍 <b>الموقع:</b> {item.get('Location', '---')}</p>
        <p style='font-size:20px;'>🏗️ <b>المطور:</b> {item.get('Developer', '---')}</p>
        <p style='font-size:18px; color:#aaa;'>{item.get('Payment Plan', 'تواصل مع الإدارة لتفاصيل السداد')}</p>
    </div>""", unsafe_allow_html=True)

elif menu == "المشاريع":
    m_col, s_col = st.columns([0.7, 0.3])
    with s_col:
        st.markdown("<h4 style='color:#10b981; text-align:center;'>🔑 استلام فوري</h4>", unsafe_allow_html=True)
        # فلترة عشوائية للاستلام الفوري بناءً على الكلمات المفتاحية
        ready = df_p[df_p.astype(str).apply(lambda x: x.str.contains('فوري|جاهز', case=False)).any(axis=1)].head(10)
        for i, r in ready.iterrows():
            if st.button(f"✅ {r['ProjectName']}", key=f"ready_{i}"):
                st.session_state.selected_item = r
                st.rerun()
    with m_col:
        search = st.text_input("🔍 ابحث عن اسم المشروع...")
        dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
        for i in range(0, len(dff.head(8)), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(dff.head(8)):
                    row = dff.iloc[i+j]
                    if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}\n🏗️ {row.get('Developer','---')}", key=f"card_p_{i+j}"):
                        st.session_state.selected_item = row
                        st.rerun()

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
                        st.session_state.selected_item = row
                        st.rerun()

elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'><h3>🤖 المساعد العقاري KMT</h3><p>أدخل المنطقة المستهدفة وسأقوم بترشيح أفضل 3 مشاريع لك.</p></div>", unsafe_allow_html=True)
    loc = st.selectbox("📍 اختر المنطقة", sorted(df_p['Location'].unique().tolist()))
    if st.button("🎯 توليد الترشيحات الذكية"):
        res = df_p[df_p['Location'] == loc].head(3)
        if not res.empty:
            st.success(f"وجدنا لك {len(res)} مشاريع في {loc}")
            for _, r in res.iterrows():
                st.write(f"✅ **{r['ProjectName']}** - شركة {r['Developer']}")
        else: st.warning("لا توجد مشاريع مطابقة حالياً في هذه المنطقة.")

elif menu == "حقيبة البروكر":
    st.title("🛠️ حقيبة الأدوات الاحترافية")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='tool-card'><h3>💳 حساب القسط</h3>", unsafe_allow_html=True)
        total = st.number_input("إجمالي السعر (EGP)", 1000000)
        years = st.slider("عدد السنوات", 1, 15, 8)
        st.metric("القسط الشهري تقريباً", f"{total/(years*12):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='tool-card'><h3>💰 حساب العمولة</h3>", unsafe_allow_html=True)
        deal_v = st.number_input("قيمة البيع", 5000000)
        comm_p = st.number_input("نسبة العمولة %", 1.5)
        st.metric("عمولتك الصافية", f"{deal_v*(comm_p/100):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='tool-card'><h3>📏 تحويل المساحة</h3>", unsafe_allow_html=True)
        m2_val = st.number_input("المساحة بالمتر المربع", 120)
        st.write(f"المساحة بالقدم المربع: {m2_val*10.76:,.0f}")
        st.write(f"المساحة بالقصبة: {m2_val/12.5:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#333; margin-top:50px;'>KMT PRO © 2026 | النسخة الاحترافية</p>", unsafe_allow_html=True)
