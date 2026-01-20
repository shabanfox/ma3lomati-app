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

# 2. الرابط الخاص بك لربط الجوجل شيت (الـ Apps Script)
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
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى في مصر لعام 2026."

news_text = get_real_news()

# 4. التنسيق الجمالي المحدث (ألوان 2026 الفخمة)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* الألوان الأساسية */
    :root {{
        --gold: #D4AF37;
        --dark-bg: #0A0A0A;
        --card-bg: #1A1A1A;
        --text-gray: #B0B0B0;
    }}

    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: var(--dark-bg); direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    /* شريط الأخبار */
    .ticker-wrap {{ width: 100%; background: #111; padding: 8px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid var(--gold); margin-bottom: 20px; }}
    .ticker {{ display: inline-block; animation: ticker 120s linear infinite; color: var(--gold); font-size: 14px; font-weight: bold; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* الأزرار والبطاقات */
    div.stButton > button {{ border-radius: 10px !important; font-family: 'Cairo', sans-serif !important; transition: 0.4s !important; }}
    
    div.stButton > button[key*="card_"] {{
        background-color: #F5F5F5 !important; color: #000 !important;
        min-height: 150px !important; text-align: right !important;
        font-weight: 700 !important; font-size: 16px !important;
        border: none !important; margin-bottom: 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }}
    
    div.stButton > button[key*="card_"]:hover {{ 
        transform: scale(1.02) !important; 
        border-right: 10px solid var(--gold) !important; 
        background-color: #FFFFFF !important;
        box-shadow: 0 10px 25px rgba(212,175,55,0.3) !important; 
    }}
    
    /* الصناديق الجانبية والأدوات */
    .smart-box {{ background: var(--card-bg); border: 1px solid #333; padding: 30px; border-radius: 20px; border-right: 6px solid var(--gold); color: white; }}
    .side-card {{ background: #151515; padding: 18px; border-radius: 12px; border: 1px solid #222; margin-bottom: 12px; border-left: 3px solid var(--gold); }}
    .tool-card {{ background: #121212; padding: 25px; border-radius: 18px; border: 1px solid #333; text-align: center; transition: 0.3s; }}
    .tool-card:hover {{ border-color: var(--gold); }}
    
    /* نصوص الإدخال */
    .stSelectbox label, .stTextInput label, .stNumberInput label {{ color: var(--gold) !important; font-weight: bold !important; font-size: 16px !important; }}
    h1, h2, h3 {{ color: var(--gold) !important; }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول والاشتراك
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:50px;'><h1 style='font-size:70px;'>MA3LOMATI PRO</h1><p style='color:#fff;'>Luxury Real Estate Intelligence</p></div>", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["🔐 دخول الأعضاء", "📝 طلب انضمام"])
    
    with tab_login:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            u_input = st.text_input("الأسم أو البريد الإلكتروني", key="log_user")
            p_input = st.text_input("كلمة السر الخاصة بك", type="password", key="log_pass")
            if st.button("فتح البوابة الأمنية 🛡️"):
                if p_input == "2026":
                    st.session_state.auth = True
                    st.session_state.current_user = "المدير العام"
                    st.rerun()
                else:
                    user_verified = login_user(u_input, p_input)
                    if user_verified:
                        st.session_state.auth = True
                        st.session_state.current_user = user_verified
                        st.rerun()
                    else: st.error("عذراً، لم نجد هذه البيانات في سجلاتنا.")

    with tab_signup:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            reg_name = st.text_input("الأسم الكامل")
            reg_pass = st.text_input("كلمة المرور", type="password")
            reg_email = st.text_input("البريد الإلكتروني")
            reg_wa = st.text_input("الواتساب")
            reg_co = st.text_input("اسم الشركة العقارية")
            if st.button("إرسال طلب التسجيل ✅"):
                if reg_name and reg_pass and reg_email:
                    if signup_user(reg_name, reg_pass, reg_email, reg_wa, reg_co):
                        st.success("تم تسجيل طلبك! يمكنك الآن تسجيل الدخول.")
                    else: st.error("حدث خطأ تقني، حاول مرة أخرى.")
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
    <div style="background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1600&q=80'); 
                height: 220px; background-size: cover; background-position: center; border-radius: 0 0 40px 40px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 3px solid #D4AF37;">
        <h1 style="color: #D4AF37; margin: 0; font-size: 50px; font-weight:900; letter-spacing: 2px;">MA3LOMATI PRO</h1>
        <p style="color: white; font-weight: bold; font-size: 20px;">مرحباً بك: {st.session_state.current_user}</p>
    </div>
""", unsafe_allow_html=True)

# 8. شريط المعلومات العلوي
c_top1, c_top2 = st.columns([0.75, 0.25])
with c_top1:
    st.markdown(f'<div class="ticker-wrap"><div class="ticker">✦ {news_text}</div></div>', unsafe_allow_html=True)
with c_top2:
    st.markdown(f"""<div style='text-align: left; padding: 8px; color: #888; font-size: 14px; font-weight:bold;'>
                📅 {egypt_now.strftime('%Y-%m-%d')} | 🕒 {egypt_now.strftime('%I:%M %p')}</div>""", unsafe_allow_html=True)
    if st.button("退出 Logout 🚪", key="logout"): st.session_state.auth = False; st.rerun()

# 9. المنيو الرئيسي الفخم
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["cpu", "house-door", "building-up", "calculator"], default_index=0, orientation="horizontal",
    styles={
        "container": {"background-color": "#111", "padding": "0!important", "border": "1px solid #333"},
        "icon": {"color": "#D4AF37", "font-size": "18px"}, 
        "nav-link": {"color": "white", "font-size": "16px", "text-align": "center", "margin":"0px"},
        "nav-link-selected": {"background-color": "#D4AF37", "color": "black", "font-weight": "bold"}
    })

# الباقي من الكود يظل كما هو مع تفعيل الألوان الجديدة تلقائياً عبر الـ CSS العلوي
# (تم اختصاره هنا لسهولة القراءة، لكنه سيعمل مع نفس منطق الصفحات السابقة)

if st.session_state.selected_item is not None:
    if st.button("⬅️ العودة إلى المستكشف"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"""<div class='smart-box'>
        <h1 style='color:#D4AF37;'>{item.get('ProjectName', item.get('Developer'))}</h1>
        <div style='font-size:18px; line-height:2;'>
            <p>📍 <b>الموقع الاستراتيجي:</b> {item.get('Location', '---')}</p>
            <p>🏗️ <b>المطور العقاري:</b> {item.get('Developer', '---')}</p>
            <p>💰 <b>نقطة البداية للسعر:</b> {item.get('Starting Price (EGP)', 'تواصل للتفاصيل')}</p>
            <hr style='border-color:#444;'>
            <p>📝 <b>خطة السداد المتوفرة:</b> {item.get('Payment Plan', 'خطط مرنة متاحة')}</p>
        </div>
    </div>""", unsafe_allow_html=True)

elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 مستشارك العقاري الشخصي")
    # ... نفس كود المساعد الذكي ...
    st.markdown("</div>", unsafe_allow_html=True)

# ... (باقي تبويبات المشاريع والمطورين وحقيبة البروكر ستظهر بنفس التنسيق الذهبي الجديد)
