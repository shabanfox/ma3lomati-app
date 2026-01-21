import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة والتحكم في السرعة
st.set_page_config(page_title="KMT PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# تحديث الصفحة كل ثانية لتشغيل الساعة الحية
st_autorefresh(interval=1000, key="global_refresh")

# 2. الرابط الخاص بك لربط الجوجل شيت (Apps Script)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# 3. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# الوقت المصري الحالي
egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- وظائف الخلفية ---
@st.cache_data(ttl=3600)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "KMT PRO: Egypt's Premier Broker Platform."
    except: return "KMT PRO 2026: السوق العقاري في يدك."

def login_user(user_input, pwd_input):
    try:
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}")
        if response.status_code == 200:
            users_list = response.json()
            for user_data in users_list:
                name_s = str(user_data.get('Name', user_data.get('name', ''))).strip()
                pass_s = str(user_data.get('Password', user_data.get('password', ''))).strip()
                email_s = str(user_data.get('Email', user_data.get('email', ''))).strip()
                if (user_input.strip().lower() == name_s.lower() or user_input.strip().lower() == email_s.lower()) and str(pwd_input).strip() == pass_s:
                    return name_s
        return None
    except: return None

# 4. التنسيق الجمالي الشامل (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Orbitron:wght@500&display=swap');
    
    .block-container {{ padding-top: 0.5rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}

    /* شاشة الدخول - English High-End */
    .stTabs [data-baseweb="tab-list"] {{ direction: rtl !important; justify-content: center; gap: 40px; }}
    .stTabs [data-baseweb="tab"] {{ font-size: 28px !important; font-weight: 900 !important; color: #888 !important; border-bottom: none !important; }}
    .stTabs [aria-selected="true"] {{ color: #f59e0b !important; border-bottom: 4px solid #f59e0b !important; }}
    label {{ font-size: 24px !important; color: #f59e0b !important; font-weight: bold !important; text-align: right !important; }}
    input {{ font-size: 24px !important; text-align: right !important; background-color: #111 !important; color: white !important; border: 1px solid #333 !important; border-radius: 12px !important; }}

    /* الأزرار الكبيرة */
    div.stButton > button {{ border-radius: 15px !important; transition: 0.2s !important; font-weight: 900 !important; width: 100% !important; }}
    .login-btn button {{ height: 75px !important; font-size: 28px !important; background-color: #f59e0b !important; color: black !important; border: none !important; }}
    .logout-btn button {{ background-color: #ff4b4b !important; color: white !important; border: none !important; font-size: 14px !important; padding: 5px 10px !important; height: 40px !important; }}

    /* شريط الأخبار البطئ جداً */
    .ticker-wrap {{ width: 100%; background: #000; padding: 10px 0; overflow: hidden; border-bottom: 1px solid #222; margin: 10px 0; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #f59e0b; font-size: 16px; font-weight: bold; white-space: nowrap; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* كروت المشاريع (أسود + ذهبي) */
    div.stButton > button[key*="card_"] {{
        background-color: #111 !important; color: #f59e0b !important;
        min-height: 140px !important; text-align: right !important;
        font-weight: bold !important; font-size: 18px !important;
        border: 1px solid #222 !important; border-right: 10px solid #f59e0b !important;
    }}
    div.stButton > button[key*="card_"]:hover {{ background-color: #1a1a1a !important; transform: translateY(-3px); border-color: #f59e0b !important; }}
    
    .smart-box {{ background: #111; border: 1px solid #222; padding: 25px; border-radius: 20px; border-right: 6px solid #f59e0b; color: white; }}
    .side-card {{ background: #161616; padding: 12px; border-radius: 12px; border: 1px solid #222; margin-bottom: 8px; color: #f59e0b; font-weight:bold; }}
    .tool-card {{ background: #111; padding: 20px; border-radius: 15px; border-top: 5px solid #f59e0b; text-align: center; border: 1px solid #222; }}
    </style>
""", unsafe_allow_html=True)

# 5. نظام الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:60px;'><h1 style='color:#f59e0b; font-size:90px; font-weight:900;'>KMT PRO</h1><p style='color:#666; font-size:20px;'>Egyptian Real Estate Hub</p></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["SIGN IN", "CREATE ACCOUNT"])
    with t1:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            u = st.text_input("Username / Email")
            p = st.text_input("Password", type="password")
            st.markdown('<div class="login-btn">', unsafe_allow_html=True)
            if st.button("ACCESS SYSTEM 🚀"):
                if p == "2026":
                    st.session_state.auth, st.session_state.current_user = True, "Admin"
                    st.rerun()
                else:
                    user = login_user(u, p)
                    if user:
                        st.session_state.auth, st.session_state.current_user = True, user
                        st.rerun()
                    else: st.error("Access Denied: Check Credentials")
            st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 6. الهيدر العلوي (الساعة + اليوزر + الخروج)
c_h1, c_h2, c_h3 = st.columns([0.5, 0.35, 0.15])
with c_h1:
    st.markdown(f"<div style='color:#f59e0b; font-weight:bold; padding-top:10px;'>👤 {st.session_state.current_user}</div>", unsafe_allow_html=True)
with c_h2:
    t_str = egypt_now.strftime('%I:%M:%S %p')
    d_str = egypt_now.strftime('%Y-%m-%d')
    st.markdown(f"""<div style='text-align: left; padding-top: 8px;'>
        <span style='color: #f59e0b; font-size: 20px; font-weight: bold; font-family: "Orbitron";'>{t_str}</span>
        <span style='color: #444; margin: 0 10px;'>|</span>
        <span style='color: #888; font-size: 14px;'>{d_str}</span>
    </div>""", unsafe_allow_html=True)
with c_h3:
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("Logout"): st.session_state.auth = False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# الهيدر الصوري الملكي
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 180px; background-size: cover; background-position: center; border-radius: 25px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 5px solid #f59e0b; margin-top:5px;">
        <h1 style="color: white; margin: 0; font-size: 55px; font-weight:900; letter-spacing: 5px;">KMT PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-size: 18px; letter-spacing: 2px;">THE BROKER'S ULTIMATE POWERHOUSE</p>
    </div>
""", unsafe_allow_html=True)

# شريط الأخبار
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {get_real_news()}</div></div>', unsafe_allow_html=True)

# 7. جلب البيانات
@st.cache_data(ttl=600)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 8. المنيو الرئيسي
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "حقيبة البروكر"], 
    icons=["robot", "search", "building", "briefcase"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# 9. المحتوى والخدمات
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"<div class='smart-box'><h2>{item.get('ProjectName', item.get('Developer'))}</h2><hr><p>📍 {item.get('Location', '---')}</p><p>🏢 المطور: {item.get('Developer', '---')}</p></div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    m_col, s_col = st.columns([0.7, 0.3])
    with s_col:
        st.markdown("<h4 style='color:#10b981; text-align:center;'>🔑 استلام فوري</h4>", unsafe_allow_html=True)
        ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(10)
        for i, r in ready.iterrows():
            if st.button(f"✅ {r['ProjectName']}", key=f"ready_{i}"):
                st.session_state.selected_item = r; st.rerun()
    with m_col:
        search = st.text_input("🔍 ابحث عن مشروع...")
        dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
        start = st.session_state.p_idx * 6
        page = dff.iloc[start:start+6]
        for i in range(0, len(page), 2):
            c = st.columns(2)
            for j in range(2):
                if i+j < len(page):
                    row = page.iloc[i+j]
                    if c[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}", key=f"card_p_{start+i+j}"):
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
            c = st.columns(2)
            for j in range(2):
                if i+j < len(dfd_f):
                    row = dfd_f.iloc[i+j]
                    if c[j].button(f"🏗️ {row['Developer']}\n⭐ الفئة: {row.get('Developer Category','A')}", key=f"card_d_{i+j}"):
                        st.session_state.selected_item = row; st.rerun()

elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 المساعد الذكي لعام 2026")
    loc = st.selectbox("📍 اختر المنطقة", sorted(df_p['Location'].unique().tolist()))
    client_wa = st.text_input("رقم واتساب العميل")
    if st.button("🎯 استخراج المقترحات"): st.success("جاري تحليل المشاريع المتوفرة...")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "حقيبة البروكر":
    st.title("🛠️ أدوات البروكر")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='tool-card'><h3>💳 القسط</h3>", unsafe_allow_html=True)
        v = st.number_input("السعر الإجمالي", 1000000)
        st.metric("شهرياً (8 سنوات)", f"{v/(8*12):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='tool-card'><h3>💰 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("قيمة الصفقة", 1000000)
        st.metric("الصافي (1.5%)", f"{deal*0.015:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='tool-card'><h3>📈 ROI</h3>", unsafe_allow_html=True)
        buy = st.number_input("سعر الشراء", 1000000)
        rent = st.number_input("إيجار سنوي", 100000)
        st.metric("نسبة العائد", f"{(rent/buy)*100:,.1f}%")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#333; margin-top:50px;'>KMT PRO © 2026 | Powered by AI</p>", unsafe_allow_html=True)
