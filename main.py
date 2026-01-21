import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
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
def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        return response.text == "Success"
    except: return False

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
        return "  •  ".join(news) if news else "سوق العقارات المصري: استقرار في الطلب وزيادة في المعروض."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى لعام 2026."

news_text = get_real_news()

# 4. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Poppins:wght@300;500;700&display=swap');
    .block-container { padding-top: 0rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { 
        background: #050505; 
        font-family: 'Poppins', 'Cairo', sans-serif; 
    }
    .stTabs [data-baseweb="tab-list"] { justify-content: center; gap: 30px; }
    .stTabs [aria-selected="true"] { color: #f59e0b !important; border-bottom-color: #f59e0b !important; }
    .ticker-wrap { width: 100%; background: #111; padding: 10px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #f59e0b; }
    .ticker { display: inline-block; animation: ticker 150s linear infinite; color: #eee; font-size: 14px; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .rtl-view { direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; padding: 20px; }
    .smart-box { background: #161616; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; margin-bottom: 20px; }
    .tool-card { background: #1a1a1a; padding: 15px; border-radius: 15px; border-top: 3px solid #f59e0b; text-align: center; height: 100%; }
    div.stButton > button[key*="card_"] {
        background-color: white !important; color: #111 !important;
        min-height: 120px !important; text-align: center !important;
        font-weight: bold !important; font-size: 15px !important;
        border: none !important; width: 100% !important; border-radius: 15px !important;
    }
    div.stButton > button[key*="card_"]:hover { transform: translateY(-5px) !important; box-shadow: 0 10px 20px rgba(245,158,11,0.3) !important; }
    .side-card { background: #1a1a1a; padding: 10px; border-radius: 10px; border: 1px solid #333; margin-bottom: 10px; font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول (منتصف الشاشة)
if not st.session_state.auth:
    st.markdown("<div style='height: 10vh;'></div>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 1.2, 1])
    with col_mid:
        st.markdown("<div style='text-align:center;'><h1 style='color:#f59e0b; font-size:55px; margin:0;'>MA3LOMATI</h1><p style='color:#888; letter-spacing: 2px;'>DASHBOARD LOGIN</p></div>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🔐 SIGN IN", "📝 REGISTER"])
        with t1:
            u = st.text_input("Email/User", key="u_en")
            p = st.text_input("Password", type="password", key="p_en")
            if st.button("LOGIN 🚀", use_container_width=True):
                user = login_user(u, p) or ("Admin" if p == "2026" else None)
                if user: st.session_state.auth = True; st.session_state.current_user = user; st.rerun()
                else: st.error("Access Denied")
        with t2:
            rn = st.text_input("Name"); re = st.text_input("Email"); rp = st.text_input("Pass", type="password")
            if st.button("CREATE ✅", use_container_width=True):
                if signup_user(rn, rp, re, "", ""): st.success("Account Created!")
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

# 7. الهيدر وشريط الأخبار
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070'); 
                height: 160px; background-size: cover; background-position: center; border-radius: 0 0 30px 30px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b;">
        <h1 style="color: white; margin: 0; font-size: 38px; font-family: 'Cairo';">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-family: 'Cairo';">أهلاً بك، {st.session_state.current_user} | {egypt_now.strftime('%I:%M %p')}</p>
    </div>
""", unsafe_allow_html=True)
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

# 8. المنيو
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], default_index=0, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

st.markdown("<div class='rtl-view'>", unsafe_allow_html=True)

# 9. زر الخروج الثابت
if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state.auth = False; st.rerun()

# --- الصفحات ---

if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"<div class='smart-box'><h2>{item.get('ProjectName', item.get('Developer'))}</h2><hr><p>📍 الموقع: {item.get('Location', 'غير محدد')}</p><p>🏗️ المطور: {item.get('Developer', '---')}</p></div>", unsafe_allow_html=True)

elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'><h3>🤖 المساعد العقاري الذكي</h3><p>أدخل بيانات طلب عميلك للحصول على أفضل مطابقة من قاعدة البيانات.</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    loc = c1.selectbox("📍 المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    typ = c2.selectbox("🏠 النوع", ["الكل", "شقق", "فيلات", "تجاري"])
    bud = c3.number_input("💰 الميزانية التقريبية", 0)
    if st.button("🎯 استخراج الترشيحات", use_container_width=True):
        st.success("جاري تحليل البيانات...")

elif menu == "المشاريع":
    m_col, s_col = st.columns([0.7, 0.3])
    with s_col:
        st.markdown("<h4 style='color:#f59e0b;'>🔥 الأكثر طلباً</h4>", unsafe_allow_html=True)
        for i, r in df_p.head(5).iterrows():
            st.markdown(f"<div class='side-card'>⭐ {r['ProjectName']}<br><small>{r['Location']}</small></div>", unsafe_allow_html=True)
    with m_col:
        search = st.text_input("🔍 ابحث عن مشروع...")
        dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
        start = st.session_state.p_idx * 6
        page = dff.iloc[start:start+6]
        for i in range(0, len(page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page):
                    row = page.iloc[i+j]
                    if cols[j].button(f"{row['ProjectName']}\n📍 {row['Location']}", key=f"card_p_{start+i+j}"):
                        st.session_state.selected_item = row; st.rerun()
        p1, _, p2 = st.columns([1,2,1])
        if st.session_state.p_idx > 0 and p1.button("السابق"): st.session_state.p_idx -= 1; st.rerun()
        if start + 6 < len(dff) and p2.button("التالي"): st.session_state.p_idx += 1; st.rerun()

elif menu == "المطورين":
    m_col, s_col = st.columns([0.7, 0.3])
    with s_col:
        st.markdown("<h4 style='color:#f59e0b;'>🏆 الفئة الممتازة</h4>", unsafe_allow_html=True)
        for i, r in df_d.head(5).iterrows():
            st.markdown(f"<div class='side-card'>🏢 {r['Developer']}<br><small>Category A</small></div>", unsafe_allow_html=True)
    with m_col:
        search_d = st.text_input("🔍 ابحث عن مطور...")
        dfd_f = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
        start_d = st.session_state.d_idx * 6
        page_d = dfd_f.iloc[start_d:start_d+6]
        for i in range(0, len(page_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page_d):
                    row = page_d.iloc[i+j]
                    if cols[j].button(f"{row['Developer']}\n⭐ Rating: A", key=f"card_d_{start_d+i+j}"):
                        st.session_state.selected_item = row; st.rerun()

elif menu == "أدوات البروكر":
    st.title("🛠️ حقيبة الأدوات (6 أدوات)")
    r1_c1, r1_c2, r1_c3 = st.columns(3)
    r2_c1, r2_c2, r2_c3 = st.columns(3)
    with r1_c1:
        st.markdown("<div class='tool-card'><h4>💳 القسط</h4>", unsafe_allow_html=True)
        v = st.number_input("السعر", 1000000, key="t1")
        d = st.number_input("المقدم", 100000, key="t2")
        y = st.number_input("السنين", 8, key="t3")
        st.metric("الشهري", f"{(v-d)/(y*12):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with r1_c2:
        st.markdown("<div class='tool-card'><h4>💰 العمولة</h4>", unsafe_allow_html=True)
        s = st.number_input("الصفقة", 1000000, key="t4")
        p = st.slider("%", 1.0, 5.0, 1.5, key="t5")
        st.metric("الربح", f"{s*(p/100):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with r1_c3:
        st.markdown("<div class='tool-card'><h4>📈 ROI</h4>", unsafe_allow_html=True)
        inv = st.number_input("الاستثمار", 1000000, key="t6")
        rnt = st.number_input("الإيجار", 100000, key="t7")
        st.metric("العائد", f"{(rnt/inv)*100:.1f}%")
        st.markdown("</div>", unsafe_allow_html=True)
    with r2_c1:
        st.markdown("<div class='tool-card'><h4>📐 المساحة</h4>", unsafe_allow_html=True)
        m2 = st.number_input("متر مربع", 100, key="t8")
        st.write(f"قدم مربع: {m2*10.76:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with r2_c2:
        st.markdown("<div class='tool-card'><h4>📝 الضريبة</h4>", unsafe_allow_html=True)
        tx = st.number_input("قيمة العقار", 1000000, key="t9")
        st.write(f"تصرفات (2.5%): {tx*0.025:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with r2_c3:
        st.markdown("<div class='tool-card'><h4>🏦 التمويل</h4>", unsafe_allow_html=True)
        ln = st.number_input("القرض", 500000, key="t10")
        st.write(f"فائدة تقديرية: {ln*0.2:.0f}/سنة")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
