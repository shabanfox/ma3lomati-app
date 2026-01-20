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

# 2. الرابط الخاص بك لربط الجوجل شيت (الـ Apps Script)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# 3. إدارة الحالة الذكية لدعم الريفريش (Session Persistence)
query_params = st.query_params
if 'auth' not in st.session_state:
    if "u" in query_params:
        st.session_state.auth = True
        st.session_state.current_user = query_params["u"]
    else:
        st.session_state.auth = False

if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- وظائف الربط مع جوجل شيت (الخلفية) ---
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

# جلب الأخبار العقارية
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى في مصر لعام 2026."

news_text = get_real_news()

# 4. التنسيق الجمالي (CSS) - الألوان الأصلية مع وضوح فائق
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    .ticker-wrap {{ width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 20px; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #FFFFFF; font-size: 13px; font-weight: bold; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    p, span, div, label {{ color: #FFFFFF !important; font-weight: 600 !important; }}
    h1, h2, h3 {{ color: #f59e0b !important; font-weight: 900 !important; }}

    div.stButton > button {{ border-radius: 12px !important; font-family: 'Cairo', sans-serif !important; transition: 0.3s !important; }}
    div.stButton > button[key*="card_"] {{
        background-color: white !important; color: #111 !important;
        min-height: 140px !important; text-align: right !important;
        font-weight: bold !important; font-size: 15px !important;
        border: none !important; margin-bottom: 10px !important;
        display: block !important; width: 100% !important;
    }}
    div.stButton > button[key*="card_"]:hover {{ transform: translateY(-5px) !important; border-right: 8px solid #f59e0b !important; box-shadow: 0 10px 20px rgba(245,158,11,0.2) !important; }}
    
    .smart-box {{ background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; }}
    .side-card {{ background: #161616; padding: 15px; border-radius: 15px; border: 1px solid #222; margin-bottom: 10px; }}
    .tool-card {{ background: #1a1a1a; padding: 20px; border-radius: 15px; border-top: 4px solid #f59e0b; text-align: center; height: 100%; }}
    .stSelectbox label, .stTextInput label, .stNumberInput label {{ color: #f59e0b !important; font-weight: bold !important; }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول والاشتراك
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:50px;'><h1 style='color:#f59e0b; font-size:60px;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    tab_login, tab_signup = st.tabs(["🔐 تسجيل دخول", "📝 اشتراك جديد"])
    
    with tab_login:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            u_input = st.text_input("الأسم أو الجيميل", key="log_user")
            p_input = st.text_input("كلمة السر", type="password", key="log_pass")
            if st.button("دخول للمنصة 🚀"):
                user_name = "Admin" if p_input == "2026" else login_user(u_input, p_input)
                if user_name:
                    st.session_state.auth = True
                    st.session_state.current_user = user_name
                    st.query_params["u"] = user_name 
                    st.rerun()
                else: st.error("بيانات الدخول غير صحيحة")
    with tab_signup:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            reg_name = st.text_input("الأسم بالكامل")
            reg_pass = st.text_input("كلمة السر", type="password")
            reg_email = st.text_input("الجيميل")
            reg_wa = st.text_input("رقم الواتساب")
            reg_co = st.text_input("الشركة")
            if st.button("تأكيد الاشتراك ✅"):
                if signup_user(reg_name, reg_pass, reg_email, reg_wa, reg_co):
                    st.success("تم تسجيلك بنجاح!")
                else: st.error("حدث خطأ في الاتصال بالسيرفر")
    st.stop()

# 6. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.rename(columns={'Area': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 7. الهيدر
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 200px; background-size: cover; background-position: center; border-radius: 0 0 30px 30px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b;">
        <h1 style="color: white; margin: 0; font-size: 45px;">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold;">أهلاً بك يا {st.session_state.current_user}</p>
    </div>
""", unsafe_allow_html=True)

# 8. شريط المعلومات والساعة الحية
c_top1, c_top2 = st.columns([0.7, 0.3])
with c_top1:
    st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)
with c_top2:
    st.markdown(f"""
        <div style='text-align: left; padding: 5px; color: #aaa; font-size: 14px;'>
            📅 {egypt_now.strftime('%Y-%m-%d')} | 🕒 <span id="live-clock">{egypt_now.strftime('%I:%M:%S %p')}</span>
        </div>
        <script>
            function updateClock() {{
                const now = new Date();
                const options = {{ timeZone: 'Africa/Cairo', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true }};
                document.getElementById('live-clock').innerHTML = now.toLocaleTimeString('en-US', options);
            }}
            setInterval(updateClock, 1000);
        </script>
    """, unsafe_allow_html=True)
    if st.button("🚪 خروج", key="logout"): 
        st.session_state.auth = False
        st.query_params.clear()
        st.rerun()

# 9. المنيو الرئيسي
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# 10. تفاصيل المشروع
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"<div class='smart-box'><h2>{item.get('ProjectName', '---')}</h2><p>📍 الموقع: {item.get('Location', '---')}</p></div>", unsafe_allow_html=True)

# --- صفحات المحتوى ---
elif menu == "المشاريع":
    f1, f2 = st.columns(2)
    search = f1.text_input("🔍 ابحث باسم المشروع")
    area_f = f2.selectbox("📍 المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
    if area_f != "الكل": dff = dff[dff['Location'] == area_f]
    page = dff.iloc[st.session_state.p_idx*6 : (st.session_state.p_idx+1)*6]
    for i in range(0, len(page), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(page):
                row = page.iloc[i+j]
                if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}", key=f"card_p_{i+j}"):
                    st.session_state.selected_item = row; st.rerun()

elif menu == "أدوات البروكر":
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='tool-card'><h3>💳 القسط</h3>", unsafe_allow_html=True)
        v = st.number_input("السعر", 1000000); y = st.slider("السنين", 1, 15, 8)
        st.metric("القسط الشهري", f"{v/(y*12):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='tool-card'><h3>💰 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("الصفقة", 1000000); pct = st.slider("النسبة", 0.5, 5.0, 1.5)
        st.metric("ربحك", f"{deal*(pct/100):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#888; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)


