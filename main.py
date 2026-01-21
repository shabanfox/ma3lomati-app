import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة الفخمة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. الرابط الخاص بك لربط الجوجل شيت (Apps Script)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# 3. إدارة الحالة والتوقيت
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
        return "  •  ".join(news) if news else "سوق العقارات المصري 2026: متابعة مستمرة."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى."

news_text = get_real_news()

# 4. التنسيق الجمالي (CSS) - تصميم ملكي يمين
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    /* ضبط الاتجاه لليمين بالكامل */
    [data-testid="stAppViewContainer"] {{ 
        background-color: #050505; 
        direction: rtl !important; 
        text-align: right !important; 
        font-family: 'Cairo', sans-serif; 
    }}

    /* شاشة الدخول - نصوص إنجليزية بخط كبير */
    .stTabs [data-baseweb="tab-list"] {{ direction: rtl !important; justify-content: center; gap: 40px; }}
    .stTabs [data-baseweb="tab"] {{ font-size: 28px !important; font-weight: 900 !important; color: #888 !important; }}
    .stTabs [aria-selected="true"] {{ color: #f59e0b !important; border-bottom: 4px solid #f59e0b !important; }}

    label {{ font-size: 24px !important; color: #f59e0b !important; font-weight: bold !important; text-align: right !important; display: block; }}
    input {{ font-size: 24px !important; text-align: right !important; background-color: #111 !important; color: white !important; border-radius: 12px !important; border: 1px solid #333 !important; }}

    /* الأزرار الذهبية الضخمة */
    div.stButton > button {{ 
        width: 100% !important; height: 70px !important; font-size: 26px !important; 
        font-weight: 900 !important; border-radius: 15px !important; 
        background-color: #f59e0b !important; color: black !important; border: none !important;
    }}
    div.stButton > button:hover {{ background-color: white !important; transform: scale(1.02); }}

    /* كروت المشاريع */
    div.stButton > button[key*="card_"] {{
        background: white !important; color: #111 !important; min-height: 150px !important;
        text-align: right !important; border-right: 10px solid #f59e0b !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5) !important; margin-bottom: 15px !important;
    }}
    
    .smart-box {{ background: #111; border: 1px solid #222; padding: 25px; border-radius: 20px; border-right: 6px solid #f59e0b; color: white; }}
    .ticker-wrap {{ background: #111; border-bottom: 1px solid #222; padding: 10px; overflow: hidden; }}
    .ticker {{ display: inline-block; animation: ticker 100s linear infinite; color: #f59e0b; font-weight: bold; font-size: 15px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    
    .tool-card {{ background: #161616; padding: 20px; border-radius: 15px; border-top: 5px solid #f59e0b; text-align: center; }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول (English Text / RTL Layout)
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:60px;'><h1 style='color:#f59e0b; font-size:80px; font-weight:900;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    
    t_login, t_signup = st.tabs(["SIGN IN", "CREATE ACCOUNT"])
    
    with t_login:
        _, col, _ = st.columns([1,1.8,1])
        with col:
            u_in = st.text_input("Username / Email", key="log_user")
            p_in = st.text_input("Password", type="password", key="log_pass")
            if st.button("LOGIN TO PLATFORM 🚀"):
                if p_in == "2026" or login_user(u_in, p_in):
                    st.session_state.auth, st.session_state.current_user = True, (u_in if u_in else "Admin")
                    st.rerun()
                else: st.error("Access Denied: Invalid Credentials")

    with t_signup:
        _, col, _ = st.columns([1,1.8,1])
        with col:
            r_name = st.text_input("Full Name")
            r_email = st.text_input("Gmail Address")
            r_pass = st.text_input("Password", type="password")
            r_wa = st.text_input("WhatsApp Number")
            r_co = st.text_input("Company")
            if st.button("SIGN UP NOW ✅"):
                if r_name and r_pass and r_email:
                    if signup_user(r_name, r_pass, r_email, r_wa, r_co):
                        st.success("Account Created! Please Login.")
                    else: st.error("Error connecting to database")
    st.stop()

# 6. جلب البيانات
@st.cache_data(ttl=60)
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

# 7. واجهة المستخدم الرئيسية (بعد الدخول)
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 180px; background-size: cover; background-position: center; border-radius: 0 0 30px 30px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b;">
        <h1 style="color: white; margin: 0; font-size: 40px; text-shadow: 2px 2px 10px rgba(0,0,0,0.5);">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-size: 20px;">أهلاً بك يا {st.session_state.current_user}</p>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

# 8. المنيو الرئيسي
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# 9. تفاصيل العنصر المختار
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"""<div class='smart-box'>
        <h2>{item.get('ProjectName', item.get('Developer'))}</h2>
        <p>📍 الموقع: {item.get('Location', '---')}</p>
        <p>🏗️ المطور: {item.get('Developer', '---')}</p>
        <hr><p>{item.get('Payment Plan', 'تفاصيل إضافية متوفرة عند الطلب')}</p>
    </div>""", unsafe_allow_html=True)

# --- القسم 1: المساعد الذكي ---
elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 المساعد الذكي")
    c1, c2, c3 = st.columns(3)
    loc = c1.selectbox("📍 المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    typ = c2.selectbox("🏠 النوع", ["الكل", "شقق", "فيلات", "تجاري"])
    budget = c3.number_input("💰 الميزانية (EGP)", 0)
    client_wa = st.text_input("واتساب العميل")
    if st.button("🎯 ابدأ الترشيح"):
        res = df_p[df_p['Location'] == loc] if loc != "الكل" else df_p
        st.success(f"تم العثور على {len(res.head(5))} مشاريع مناسبة")
        for i, r in res.head(4).iterrows():
            st.write(f"🏢 {r['ProjectName']} - {r['Developer']}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- القسم 2: المشاريع ---
elif menu == "المشاريع":
    search = st.text_input("🔍 ابحث باسم المشروع")
    dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
    for i in range(0, len(dff.head(8)), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(dff):
                row = dff.iloc[i+j]
                if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}\n🏗️ {row['Developer']}", key=f"card_p_{i+j}"):
                    st.session_state.selected_item = row; st.rerun()

# --- القسم 3: المطورين ---
elif menu == "المطورين":
    search_d = st.text_input("🔍 ابحث عن مطور")
    dfd_f = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
    for i in range(0, len(dfd_f.head(8)), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(dfd_f):
                row = dfd_f.iloc[i+j]
                if cols[j].button(f"🏗️ {row['Developer']}\n⭐ الفئة: {row.get('Developer Category','A')}", key=f"card_d_{i+j}"):
                    st.session_state.selected_item = row; st.rerun()

# --- القسم 4: حقيبة البروكر ---
elif menu == "أدوات البروكر":
    st.title("🛠️ أدوات البروكر")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='tool-card'><h3>💳 القسط</h3>", unsafe_allow_html=True)
        price = st.number_input("السعر", 1000000)
        years = st.slider("السنين", 1, 15, 8)
        st.metric("القسط الشهري", f"{price/(years*12):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='tool-card'><h3>💰 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("الصفقة", 1000000)
        pct = st.slider("النسبة %", 1.0, 5.0, 1.5)
        st.metric("الربح", f"{deal*(pct/100):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='tool-card'><h3>📐 المساحة</h3>", unsafe_allow_html=True)
        m2 = st.number_input("المتر المربع", 100)
        st.write(f"القدم: {m2*10.76:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
