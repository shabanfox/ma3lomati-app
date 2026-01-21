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
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# تحديث تلقائي كل 30 ثانية لمزامنة الساعة والأخبار
st_autorefresh(interval=30000, key="auto_refresh_clock")

# 2. الروابط الأساسية
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"

# 3. إدارة الجلسة والتوقيت
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_now = datetime.now(pytz.timezone('Africa/Cairo'))

# --- وظائف الاتصال ---
def login_check(u, p):
    # الدخول الطارئ للمطور
    if p == "2026": return "المطور"
    try:
        # الاتصال بجوجل شيت مع منع الكاش
        res = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=10)
        if res.status_code == 200:
            users = res.json()
            for user in users:
                db_u = str(user.get('Email', user.get('Name', ''))).strip().lower()
                db_p = str(user.get('Password', '')).strip()
                if u.strip().lower() == db_u and p.strip() == db_p:
                    return user.get('Name')
    except: pass
    return None

@st.cache_data(ttl=600)
def load_all_data():
    try:
        p = pd.read_csv(URL_PROJECTS).fillna("---")
        d = pd.read_csv(URL_DEVELOPERS).fillna("---")
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True, errors='ignore')
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

@st.cache_data(ttl=1800)
def get_news():
    try:
        feed = feedparser.parse("https://www.youm7.com/rss/SectionRss?SectionID=297")
        titles = [item.title for item in feed.entries[:15]]
        return "  •  ".join(titles) if titles else "MA3LOMATI PRO: سوق العقارات المصري 2026"
    except: return "MA3LOMATI PRO: منصتك العقارية الذكية"

# 4. التنسيق الجمالي (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Orbitron:wght@500&display=swap');
    
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    /* شريط الأخبار البطيء الواضح */
    .ticker-wrap {{ background: #000; border-bottom: 2px solid #f59e0b; padding: 15px 0; overflow: hidden; margin-top: 10px; }}
    .ticker {{ display: inline-block; animation: ticker 200s linear infinite; color: #f59e0b; font-weight: 900; font-size: 18px; white-space: nowrap; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* أزرار تسجيل الدخول والخروج */
    .login-box input {{ font-size: 20px !important; }}
    .stButton > button {{ border-radius: 12px !important; font-weight: 900 !important; transition: 0.3s; }}
    .logout-container button {{ background-color: #ff4b4b !important; color: white !important; border: none !important; width: 100px !important; height: 35px !important; }}
    
    /* كروت المشاريع والمطورين */
    div.stButton > button[key*="card_"] {{
        background: #111 !important; color: #f59e0b !important; min-height: 130px !important;
        border: 1px solid #222 !important; border-right: 10px solid #f59e0b !important;
        text-align: right !important; margin-bottom: 15px !important; font-size: 18px !important;
    }}
    div.stButton > button[key*="card_"]:hover {{ background: #1a1a1a !important; transform: scale(1.01); }}

    .smart-card {{ background: #111; border: 1px solid #222; padding: 25px; border-radius: 20px; border-right: 6px solid #f59e0b; color: white; }}
    .tool-box {{ background: #0c0c0c; padding: 20px; border-radius: 15px; border-top: 5px solid #f59e0b; border: 1px solid #222; text-align: center; }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة تسجيل الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b; font-size:75px; font-weight:900;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["SIGN IN", "CREATE ACCOUNT"])
    with t1:
        _, col, _ = st.columns([1, 1.5, 1])
        with col:
            u_in = st.text_input("Username / Email", key="user")
            p_in = st.text_input("Password", type="password", key="pass")
            if st.button("LOGIN TO SYSTEM 🚀"):
                user_name = login_check(u_in, p_in)
                if user_name:
                    st.session_state.auth = True
                    st.session_state.current_user = user_name
                    st.rerun()
                else:
                    st.error("Access Denied: Check your connection or use 2026 for Dev Access.")
    st.stop()

# 6. الهيدر العلوي (يوزر، ساعة، خروج)
c_h1, c_h2, c_h3 = st.columns([0.4, 0.45, 0.15])
with c_h1:
    st.markdown(f"<p style='color:#f59e0b; font-weight:bold; font-size:18px; padding-top:10px;'>👤 {st.session_state.current_user}</p>", unsafe_allow_html=True)
with c_h2:
    st.markdown(f"<p style='color:#777; font-family:Orbitron; padding-top:10px; font-size:16px;'>🕒 {egypt_now.strftime('%I:%M %p')} | {egypt_now.strftime('%d/%m/%Y')}</p>", unsafe_allow_html=True)
with c_h3:
    st.markdown('<div class="logout-container">', unsafe_allow_html=True)
    if st.button("Logout"): st.session_state.auth = False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# شريط الأخبار البطيء جداً
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {get_news()}</div></div>', unsafe_allow_html=True)

# 7. المنيو والبيانات
df_p, df_d = load_all_data()
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# 8. عرض التفاصيل
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"""<div class='smart-card'>
        <h2>{item.get('ProjectName', item.get('Developer'))}</h2><hr>
        <p style='font-size:20px;'>📍 الموقع: {item.get('Location', '---')}</p>
        <p style='font-size:20px;'>🏗️ المطور: {item.get('Developer', '---')}</p>
        <p style='font-size:20px;'>💰 السعر: {item.get('Price', 'غير محدد')}</p>
        <div style='background:#1a1a1a; padding:15px; border-radius:10px; border:1px solid #333;'>
            <b>تفاصيل إضافية:</b><br>{item.get('Payment Plan', 'خطط السداد متوفرة عند التواصل')}
        </div>
    </div>""", unsafe_allow_html=True)

# --- صفحة المساعد الذكي الكاملة ---
elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-card'><h3>🤖 المساعد العقاري الذكي KMT</h3><p>قم بفلترة النتائج للوصول لأفضل الخيارات لعميلك</p></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    loc_f = col1.selectbox("📍 المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    dev_f = col2.selectbox("🏗️ المطور", ["الكل"] + sorted(df_d['Developer'].unique().tolist()))
    search_f = col3.text_input("🔍 كلمة بحث (مثلاً: فوري، شقة)")
    
    if st.button("🎯 ابدأ البحث الذكي"):
        res = df_p.copy()
        if loc_f != "الكل": res = res[res['Location'] == loc_f]
        if dev_f != "الكل": res = res[res['Developer'] == dev_f]
        if search_f: res = res[res.astype(str).apply(lambda x: x.str.contains(search_f, case=False)).any(axis=1)]
        
        if not res.empty:
            st.success(f"تم العثور على {len(res.head(8))} خيار مناسب")
            for i in range(0, len(res.head(8)), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i+j < len(res):
                        row = res.iloc[i+j]
                        if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}", key=f"card_smart_{i+j}"):
                            st.session_state.selected_item = row; st.rerun()
        else: st.warning("لم نجد نتائج مطابقة، جرب تغيير الفلاتر.")

# --- صفحة المشاريع ---
elif menu == "المشاريع":
    s_query = st.text_input("🔍 ابحث عن اسم المشروع أو المنطقة")
    dff = df_p[df_p['ProjectName'].str.contains(s_query, case=False)] if s_query else df_p
    for i in range(0, len(dff.head(10)), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(dff):
                row = dff.iloc[i+j]
                if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}\n🏗️ {row['Developer']}", key=f"card_p_{i+j}"):
                    st.session_state.selected_item = row; st.rerun()

# --- صفحة المطورين ---
elif menu == "المطورين":
    s_dev = st.text_input("🔍 ابحث عن المطور")
    dfd_f = df_d[df_d['Developer'].str.contains(s_dev, case=False)] if s_dev else df_d
    for i in range(0, len(dfd_f.head(10)), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(dfd_f):
                row = dfd_f.iloc[i+j]
                if cols[j].button(f"🏗️ {row['Developer']}\n⭐ الفئة: {row.get('Developer Category','A')}", key=f"card_d_{i+j}"):
                    st.session_state.selected_item = row; st.rerun()

# --- صفحة أدوات البروكر ---
elif menu == "أدوات البروكر":
    st.title("🛠️ حقيبة البروكر الاحترافية")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='tool-box'><h3>💳 الأقساط</h3>", unsafe_allow_html=True)
        val = st.number_input("قيمة الوحدة", 1000000)
        years = st.slider("السنين", 1, 15, 8)
        st.metric("القسط الشهري", f"{val/(years*12):,.0f} EGP")
    with c2:
        st.markdown("<div class='tool-box'><h3>💰 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("قيمة البيع", 5000000)
        per = st.slider("النسبة %", 1.0, 5.0, 1.5)
        st.metric("ربحك الصافي", f"{deal*(per/100):,.0f} EGP")
    with c3:
        st.markdown("<div class='tool-box'><h3>📐 المساحات</h3>", unsafe_allow_html=True)
        sqm = st.number_input("المساحة بالمتر", 150)
        st.write(f"بالقدم المربع: {sqm*10.76:,.0f}")
        st.write(f"بالقصبة: {sqm/12.5:.2f}")

st.markdown("<p style='text-align:center; color:#333; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
