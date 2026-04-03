import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الروابط الأساسية ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 3. وظائف جلب البيانات (يجب أن تكون في البداية) ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]: 
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload, timeout=10)
        return response.text == "Success"
    except: return False

def login_user(user_input, pwd_input):
    try:
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=15)
        if response.status_code == 200:
            users_list = response.json()
            user_input = str(user_input).strip().lower()
            for user_data in users_list:
                name_s = str(user_data.get('Name', user_data.get('name', ''))).strip()
                email_s = str(user_data.get('Email', user_data.get('email', ''))).strip()
                pass_s = str(user_data.get('Password', user_data.get('password', ''))).strip()
                if (user_input == name_s.lower() or user_input == email_s.lower()) and str(pwd_input) == pass_s:
                    return name_s
        return None
    except: return None

@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى في مصر لعام 2026."

# --- 4. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'messages' not in st.session_state: st.session_state.messages = []

# تنفيذ جلب البيانات
df_p, df_d, df_l = load_data()
news_text = get_real_news()

# --- 5. التصميم الجمالي CSS (الكروت البيضاء والخط الأسود العريض) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.97), rgba(0,0,0,0.97)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}

    /* الكرت الأبيض الفخم */
    div.stButton > button[key*="card_"] {{
        background-color: #FFFFFF !important; 
        color: #000000 !important;
        border-right: 15px solid #f59e0b !important;
        border-radius: 20px !important;
        padding: 25px !important;
        height: 190px !important; /* ارتفاع ثابت للتناسق */
        width: 100% !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
        text-align: right !important;
        font-weight: 900 !important; /* خط أسود عريض جداً */
        font-size: 20px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
        margin-bottom: 20px !important;
    }}
    div.stButton > button[key*="card_"]:hover {{ transform: translateY(-5px) !important; background-color: #f8f9fa !important; }}

    /* شريط الأخبار الذهبي */
    .ticker-bar {{ background: #f59e0b; color: black; padding: 12px; font-weight: 900; text-align: center; border-radius: 0 0 25px 25px; }}
    .detail-card {{ background: rgba(30, 30, 30, 0.95); padding: 25px; border-radius: 20px; border-top: 5px solid #f59e0b; border: 1px solid #444; margin-bottom:20px; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 16px; }}
    .val-white {{ color: white; font-size: 20px; font-weight: 700; border-bottom: 1px solid #444; padding-bottom:5px; margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. صفحة الدخول ---
if not st.session_state.auth:
    _, center_col, _ = st.columns([1, 1.2, 1])
    with center_col:
        st.markdown("<div style='background:white; padding:40px; border-radius:30px; margin-top:80px; text-align:center;'>", unsafe_allow_html=True)
        st.markdown("<h1 style='color:black;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
        u = st.text_input("الأسم أو الجيميل", placeholder="User", key="log_u")
        p = st.text_input("كلمة السر", type="password", placeholder="Pass", key="log_p")
        if st.button("دخول آمن 🚀", use_container_width=True):
            if p == "2026": st.session_state.auth, st.session_state.current_user = True, "Admin"; st.rerun()
            else:
                res = login_user(u, p)
                if res: st.session_state.auth, st.session_state.current_user = True, res; st.rerun()
                else: st.error("خطأ في البيانات")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 7. الواجهة الداخلية ---
st.markdown(f'<div class="ticker-bar">🔥 {news_text}</div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["briefcase", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"}})

col_main, col_side = st.columns([0.78, 0.22])

# --- 8. محتوى الأدوات (9 أدوات) ---
if menu == "أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات البروكر (9 أدوات احترافية)</h2>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    with t1:
        with st.container(border=True):
            st.subheader("1. حاسبة القسط")
            v1 = st.number_input("السعر", 1000000, key="t1")
            y1 = st.number_input("السنين", 8, key="t1y")
            st.metric("شهرياً", f"{v1/(y1*12):,.0f}")
        with st.container(border=True):
            st.subheader("4. سعر المتر")
            v4 = st.number_input("الإجمالي", 3000000, key="t4")
            m4 = st.number_input("المساحة", 150, key="t4m")
            st.metric("المتر", f"{v4/m4:,.0f}")
        with st.container(border=True):
            st.subheader("7. مساحة التحميل")
            net = st.number_input("الصافي", 120, key="t7")
            gross = st.number_input("الإجمالي", 155, key="t7g")
            st.metric("نسبة التحميل", f"{((gross-net)/gross)*100:.1f}%")
    with t2:
        with st.container(border=True):
            st.subheader("2. حساب العمولة")
            v2 = st.number_input("الصفقة", 5000000, key="t2")
            c2 = st.slider("%", 1.0, 5.0, 2.5, key="t2c")
            st.metric("العمولة", f"{v2*(c2/100):,.0f}")
        with st.container(border=True):
            st.subheader("5. خصم الكاش")
            v5 = st.number_input("السعر الأصلي", 2000000, key="t5")
            d5 = st.slider("الخصم %", 0, 45, 20, key="t5d")
            st.metric("بعد الخصم", f"{v5*(1-d5/100):,.0f}")
        with st.container(border=True):
            st.subheader("8. الضريبة العقارية")
            v8 = st.number_input("القيمة", 2000000, key="t8")
            st.metric("الضريبة", f"{v8*0.001:,.0f}")
    with t3:
        with st.container(border=True):
            st.subheader("3. عائد ROI")
            v3 = st.number_input("الشراء", 3000000, key="t3")
            r3 = st.number_input("الإيجار السنوي", 300000, key="t3r")
            st.metric("العائد", f"{(r3/v3)*100:.1f}%")
        with st.container(border=True):
            st.subheader("6. التمويل العقاري")
            v6 = st.number_input("القرض", 1000000, key="t6")
            i6 = st.slider("الفائدة %", 5, 25, 12, key="t6i")
            st.metric("الفائدة السنوية", f"{v6*(i6/100):,.0f}")
        with st.container(border=True):
            st.subheader("9. زيادة القسط 5%")
            v9 = st.number_input("القسط الحالي", 10000, key="t9")
            st.metric("بعد 5 سنين", f"{v9*(1.05**5):,.0f}")

# --- 9. المشاريع (الكروت البيضاء المتناسقة) ---
elif menu == "المشاريع":
    with col_main:
        if st.session_state.view == "details":
            if st.button("⬅ عودة"): st.session_state.view = "grid"; st.rerun()
            item = df_p.iloc[st.session_state.current_index]
            st.markdown("<div class='detail-card'>", unsafe_allow_html=True)
            for k, v in item.items():
                st.markdown(f"<p class='label-gold'>{k}</p><p class='val-white'>{v}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            search = st.text_input("🔍 ابحث عن مشروع...")
            filt = df_p[df_p.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else df_p
            grid = st.columns(2)
            for i, (idx, r) in enumerate(filt.head(10).iterrows()):
                with grid[i%2]:
                    # الكرت الأبيض
                    txt = f"🏢 {r.iloc[0]}\n📍 {r.get('Location', '---')}\n🏗️ {r.get('Developer', '---')}"
                    if st.button(txt, key=f"card_{idx}"):
                        st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()

# --- 10. الجانب (المقترحات) ---
with col_side:
    st.markdown("<h3 style='color:#f59e0b; text-align:center;'>⭐ مقترحات</h3>", unsafe_allow_html=True)
    for _, r in df_p.head(10).iterrows():
        st.markdown(f"<div style='background:white; color:black; padding:12px; border-radius:12px; margin-bottom:8px; border-right:6px solid #f59e0b; font-weight:900;'>{r.iloc[0][:25]}</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
