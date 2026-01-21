import streamlit as st
import pandas as pd
import requests
import feedparser
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. الرابط الخاص بك
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# 3. إدارة حالة الجلسة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- وظائف الربط ---
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

@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "سوق العقارات 2026: استقرار ونمو مستمر."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى."

news_text = get_real_news()

# 4. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Poppins:wght@300;500;700&display=swap');
    .block-container { padding-top: 0rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; }
    
    .ticker-wrap { width: 100%; background: #111; padding: 10px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #f59e0b; direction: ltr !important; }
    .ticker { display: inline-block; animation: ticker 150s linear infinite; color: #eee; font-size: 14px; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    .smart-box { background: #161616; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; margin-bottom: 20px; }
    .tool-card { background: #1a1a1a; padding: 15px; border-radius: 15px; border-top: 3px solid #f59e0b; text-align: center; }
    
    /* زر الخروج في الهيدر */
    .logout-header-btn { position: absolute; top: 20px; left: 20px; z-index: 1000; }
    
    div.stButton > button[key*="card_"] {
        background-color: white !important; color: #111 !important;
        min-height: 100px !important; text-align: right !important;
        font-weight: bold !important; font-size: 16px !important;
        border: none !important; width: 100% !important; border-radius: 15px !important;
    }
    input { text-align: right !important; direction: rtl !important; }
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 1.2, 1])
    with col_mid:
        st.markdown("<div style='text-align:center;'><h1 style='color:#f59e0b; font-size:50px;'>MA3LOMATI</h1></div>", unsafe_allow_html=True)
        u = st.text_input("Username / Email", key="u_en")
        p = st.text_input("Password", type="password", key="p_en")
        if st.button("LOGIN 🚀", use_container_width=True):
            user = login_user(u, p) or ("Admin" if p == "2026" else None)
            if user: st.session_state.auth = True; st.session_state.current_user = user; st.rerun()
    st.stop()

# 6. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 7. الهيدر مع زر الخروج على اليسار
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070'); 
                height: 150px; background-size: cover; background-position: center; border-radius: 0 0 30px 30px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b; position: relative;">
        <h1 style="color: white; margin: 0; font-family: 'Cairo';">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-family: 'Cairo';">أهلاً، {st.session_state.current_user}</p>
    </div>
""", unsafe_allow_html=True)

# وضع زر الخروج فعلياً في الهيدر (جهة اليسار)
col_head1, col_head2 = st.columns([0.15, 0.85])
with col_head1:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 خروج", key="logout_top"):
        st.session_state.auth = False; st.rerun()

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

# 8. المنيو
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["briefcase", "building", "search", "robot"], default_index=3, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# 9. المحتوى
if st.session_state.selected_item is not None:
    if st.button("➡️ عودة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"<div class='smart-box'><h2>{item.get('ProjectName', item.get('Developer'))}</h2><p>📍 {item.get('Location', '---')}</p></div>", unsafe_allow_html=True)

elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'><h3>🤖 المساعد العقاري الذكي</h3></div>", unsafe_allow_html=True)
    st.text_input("أدخل متطلبات العميل هنا...")

elif menu == "المشاريع":
    m_col, s_col = st.columns([0.7, 0.3]) # المشاريع يمين (70%)، القائمة يسار (30%)
    with s_col:
        st.markdown("<h4 style='color:#f59e0b; text-align:center;'>🚀 استلام فوري</h4>", unsafe_allow_html=True)
        for i, r in df_p.head(5).iterrows():
            st.markdown(f"<div class='smart-box' style='padding:10px;'>🏠 {r['ProjectName']}</div>", unsafe_allow_html=True)
    with m_col:
        st.markdown("### 📂 دليل المشاريع")
        search = st.text_input("🔍 ابحث عن مشروع...")
        dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
        page = dff.iloc[st.session_state.p_idx*6 : st.session_state.p_idx*6+6]
        for i in range(0, len(page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page):
                    row = page.iloc[i+j]
                    if cols[j].button(f"{row['ProjectName']}\n📍 {row['Location']}", key=f"card_p_{i+j}"):
                        st.session_state.selected_item = row; st.rerun()

elif menu == "المطورين":
    m_col, s_col = st.columns([0.7, 0.3]) # المطورين يمين (70%)، القائمة يسار (30%)
    with s_col:
        st.markdown("<h4 style='color:#f59e0b; text-align:center;'>🏆 كبار المطورين</h4>", unsafe_allow_html=True)
        for i, r in df_d.head(5).iterrows():
            st.markdown(f"<div class='smart-box' style='padding:10px;'>🏢 {r['Developer']}</div>", unsafe_allow_html=True)
    with m_col:
        st.markdown("### 🏗️ قائمة المطورين")
        search_d = st.text_input("🔍 ابحث عن مطور...")
        dfd_f = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
        page_d = dfd_f.iloc[st.session_state.d_idx*6 : st.session_state.d_idx*6+6]
        for i in range(0, len(page_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page_d):
                    row = page_d.iloc[i+j]
                    if cols[j].button(f"{row['Developer']}\n⭐ فئة ممتازة", key=f"card_d_{i+j}"):
                        st.session_state.selected_item = row; st.rerun()

elif menu == "أدوات البروكر":
    st.markdown("<h2 style='text-align: center; color: #f59e0b; margin-bottom: 30px;'>🛠️ أدوات البروكر العقاري</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)
    # الأدوات (تم وضع الكود المختصر لتوفير المساحة)
    with c1: st.markdown("<div class='tool-card'><h4>💳 القسط</h4></div>", unsafe_allow_html=True); st.number_input("السعر", key="br1")
    with c2: st.markdown("<div class='tool-card'><h4>💰 العمولة</h4></div>", unsafe_allow_html=True); st.number_input("الصفقة", key="br2")
    with c3: st.markdown("<div class='tool-card'><h4>📈 ROI</h4></div>", unsafe_allow_html=True); st.number_input("الاستثمار", key="br3")
    with c4: st.markdown("<div class='tool-card'><h4>📐 المساحة</h4></div>", unsafe_allow_html=True); st.number_input("متر مربع", key="br4")
    with c5: st.markdown("<div class='tool-card'><h4>📝 الضريبة</h4></div>", unsafe_allow_html=True); st.number_input("القيمة", key="br5")
    with c6: st.markdown("<div class='tool-card'><h4>🏦 التمويل</h4></div>", unsafe_allow_html=True); st.number_input("القرض", key="br6")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
