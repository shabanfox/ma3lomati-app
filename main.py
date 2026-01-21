import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu
# إضافة مكتبة التحديث التلقائي للساعة
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# تحديث الصفحة كل ثانية لضمان دقة الساعة
st_autorefresh(interval=1000, key="clock_refresh")

# 2. الرابط الخاص بك لربط الجوجل شيت
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# 3. إدارة الحالة والتوقيت المصري
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- وظائف الربط مع جوجل شيت ---
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
        return "  •  ".join(news) if news else "Real Estate Egypt 2026: Latest Updates."
    except: return "MA3LOMATI PRO: Your #1 Real Estate Platform in Egypt."

news_text = get_real_news()

# 4. التنسيق الجمالي (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    .ticker-wrap {{ width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 20px; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    div.stButton > button {{ border-radius: 12px !important; font-family: 'Cairo', sans-serif !important; transition: 0.3s !important; }}
    .smart-box {{ background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; }}
    .stSelectbox label, .stTextInput label, .stNumberInput label {{ color: #f59e0b !important; font-weight: bold !important; }}
    /* جعل حقول الإدخال في صفحة الدخول تبدو واضحة بالإنجليزية */
    [data-testid="stForm"] {{ direction: ltr !important; text-align: left !important; }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول والاشتراك (English Version)
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:50px;'><h1 style='color:#f59e0b; font-size:60px;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["🔐 SIGN IN", "📝 SIGN UP"])
    
    with tab_login:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            u_input = st.text_input("Username or Email", key="log_user")
            p_input = st.text_input("Password", type="password", key="log_pass")
            if st.button("LOGIN TO PLATFORM 🚀"):
                if p_input == "2026": 
                    st.session_state.auth = True
                    st.session_state.current_user = "Admin"
                    st.rerun()
                else:
                    user_verified = login_user(u_input, p_input)
                    if user_verified:
                        st.session_state.auth = True
                        st.session_state.current_user = user_verified
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please try again.")

    with tab_signup:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            reg_name = st.text_input("Full Name")
            reg_pass = st.text_input("Password", type="password")
            reg_email = st.text_input("Email (Gmail)")
            reg_wa = st.text_input("WhatsApp Number")
            reg_co = st.text_input("Company")
            if st.button("CREATE ACCOUNT ✅"):
                if reg_name and reg_pass and reg_email:
                    if signup_user(reg_name, reg_pass, reg_email, reg_wa, reg_co):
                        st.success("Account created successfully! Please go to Sign In tab.")
                    else: st.error("Connection error. Please check your internet.")
                else: st.warning("Name, Password and Email are required.")
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
        d.columns = d.columns.str.strip()
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 7. الهيدر البصري
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 200px; background-size: cover; background-position: center; border-radius: 0 0 30px 30px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b;">
        <h1 style="color: white; margin: 0; font-size: 45px; text-shadow: 2px 2px 10px rgba(0,0,0,0.5);">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-size: 18px;">أهلاً بك يا {st.session_state.current_user} في النسخة الاحترافية</p>
    </div>
""", unsafe_allow_html=True)

# 8. شريط المعلومات (ساعة محدثة تلقائياً)
c_top1, c_top2 = st.columns([0.7, 0.3])
with c_top1:
    st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)
with c_top2:
    st.markdown(f"""<div style='text-align: left; padding: 5px; color: #aaa; font-size: 14px;'>
                📅 {egypt_now.strftime('%Y-%m-%d')} | 🕒 {egypt_now.strftime('%I:%M:%S %p')} 
                </div>""", unsafe_allow_html=True)
    if st.button("🚪 خروج", key="logout"): st.session_state.auth = False; st.rerun()

# 9. المنيو الرئيسي
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], default_index=0, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# 10. تفاصيل المشروع
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"""<div class='smart-box'>
        <h2>{item.get('ProjectName', item.get('Developer'))}</h2>
        <p>📍 الموقع: {item.get('Location', '---')}</p>
        <p>🏗️ المطور: {item.get('Developer', '---')}</p>
        <p>💰 تفاصيل السعر: {item.get('Starting Price (EGP)', 'تواصل للاستفسار')}</p>
        <hr><p>{item.get('Payment Plan', 'خطط سداد متنوعة متاحة عند التواصل')}</p>
    </div>""", unsafe_allow_html=True)

# --- باقي الأقسام (المساعد، المشاريع، المطورين، الأدوات) ---
elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 مساعد الربط العقاري الذكي")
    col_f1, col_f2, col_f3 = st.columns(3)
    locs = sorted(df_p['Location'].unique().tolist()) if 'Location' in df_p.columns else ["الكل"]
    sel_loc = col_f1.selectbox("📍 المنطقة المستهدفة", ["الكل"] + locs)
    sel_budget = col_f3.number_input("💰 المقدم المتاح (EGP)", 0, step=50000)
    client_wa = st.text_input("رقم واتساب العميل")
    if st.button("🎯 استخراج أفضل الترشيحات"):
        res = df_p.copy()
        if sel_loc != "الكل": res = res[res['Location'] == sel_loc]
        if not res.empty:
            for idx, r in res.head(6).iterrows():
                with st.container(border=True):
                    c_txt, c_btn = st.columns([0.8, 0.2])
                    c_txt.write(f"🏢 **{r['ProjectName']}** | {r['Developer']}")
                    link = f"https://wa.me/{client_wa}?text=I recommend {r['ProjectName']}"
                    c_btn.markdown(f"[📲 Send]({link})")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    m_col, s_col = st.columns([0.7, 0.3])
    with m_col:
        search = st.text_input("🔍 Search Project Name")
        dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
        start = st.session_state.p_idx * 6
        page = dff.iloc[start:start+6]
        for i in range(0, len(page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page):
                    row = page.iloc[i+j]
                    if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}", key=f"card_p_{start+i+j}"):
                        st.session_state.selected_item = row; st.rerun()

elif menu == "المطورين":
    search_d = st.text_input("🔍 Search Developer")
    dfd_f = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
    start_d = st.session_state.d_idx * 6
    page_d = dfd_f.iloc[start_d:start_d+6]
    for i in range(0, len(page_d), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(page_d):
                row = page_d.iloc[i+j]
                if cols[j].button(f"🏗️ {row['Developer']}", key=f"card_d_{start_d+i+j}"):
                    st.session_state.selected_item = row; st.rerun()

elif menu == "أدوات البروكر":
    st.title("🛠️ Broker Tools")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='tool-card'><h3>💳 Installments</h3>", unsafe_allow_html=True)
        v = st.number_input("Total Price", 1000000)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
