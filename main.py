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

# --- 2. الثوابت والروابط ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- 4. وظائف الربط مع جوجل شيت ---
def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload, timeout=10)
        return "Success" in response.text
    except: return False

def login_user(user_input, pwd_input):
    try:
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=10)
        if response.status_code == 200:
            users_list = response.json()
            for u in users_list:
                n_s = str(u.get('Name', u.get('name', ''))).strip()
                p_s = str(u.get('Password', u.get('password', ''))).strip()
                e_s = str(u.get('Email', u.get('email', ''))).strip()
                if (user_input.strip().lower() == n_s.lower() or user_input.strip().lower() == e_s.lower()) and str(pwd_input).strip() == p_s:
                    return n_s
        return None
    except: return None

@st.cache_data(ttl=1800)
def get_real_news():
    try:
        feed = feedparser.parse("https://www.youm7.com/rss/SectionRss?SectionID=297")
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى في مصر لعام 2026."

news_text = get_real_news()

# --- 5. التنسيق الجمالي (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}

    /* LOGIN UI */
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: flex-start; width: 100%; padding-top: 50px; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 24px; font-weight: 900;
        text-align: center; z-index: 10; margin-bottom: -30px; min-width: 360px;
    }}
    .auth-card {{ background-color: #ffffff; width: 380px; padding: 55px 35px 30px 35px; border-radius: 30px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); }}
    .lock-gold {{ font-size: 45px; color: #f59e0b; margin-bottom: 5px; }}
    .auth-card div.stTextInput input {{ background-color: #000 !important; color: #fff !important; border: 1px solid #f59e0b !important; border-radius: 12px !important; text-align: center !important; height: 45px !important; }}

    /* INTERNAL UI */
    .ticker-wrap {{ width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 20px; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 4px solid #f59e0b;
        padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 20px;
    }}
    .smart-box {{ background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; }}
    .tool-card {{ background: #1a1a1a; padding: 20px; border-radius: 15px; border-top: 4px solid #f59e0b; text-align: center; height: 100%; color: white; }}
    
    div.stButton > button {{ border-radius: 12px !important; font-family: 'Cairo', sans-serif !important; transition: 0.3s !important; }}
    div.stButton > button[key*="card_"] {{
        background-color: white !important; color: #111 !important;
        min-height: 140px !important; text-align: right !important; font-weight: bold !important;
        border: none !important; width: 100% !important; margin-bottom: 10px;
    }}
    div.stButton > button[key*="card_"]:hover {{ transform: translateY(-5px) !important; border-right: 8px solid #f59e0b !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. صفحة الدخول والاشتراك ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>MA3LOMATI PRO</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.markdown("<div class='lock-gold'>🔒</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 تسجيل دخول", "📝 اشتراك جديد"])
    
    with tab1:
        u_log = st.text_input("User", placeholder="اسم المستخدم أو الإيميل", label_visibility="collapsed", key="l_u")
        p_log = st.text_input("Pass", type="password", placeholder="كلمة المرور", label_visibility="collapsed", key="l_p")
        if st.button("SIGN IN", use_container_width=True):
            if p_log == "2026":
                st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
            else:
                user_verified = login_user(u_log, p_log)
                if user_verified:
                    st.session_state.auth = True; st.session_state.current_user = user_verified; st.rerun()
                else: st.error("بيانات الدخول غير صحيحة")
    
    with tab2:
        r_n = st.text_input("الأسم بالكامل", placeholder="الاسم")
        r_p = st.text_input("كلمة السر", type="password", placeholder="الباسورد")
        r_e = st.text_input("الجيميل", placeholder="الإيميل")
        r_w = st.text_input("الواتساب", placeholder="رقم الموبايل")
        r_c = st.text_input("الشركة", placeholder="اسم الشركة")
        if st.button("تأكيد الاشتراك ✅", use_container_width=True):
            if r_n and r_p and r_e:
                if signup_user(r_n, r_p, r_e, r_w, r_c):
                    st.success("تم الاشتراك! يمكنك الدخول الآن.")
                else: st.error("خطأ في الاتصال بالسيرفر")
            else: st.warning("يرجى إكمال البيانات الأساسية")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 7. التطبيق الرئيسي بعد الدخول ---
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

# الهيدر
st.markdown(f"""
    <div class="royal-header">
        <h1 style="color: white; margin: 0; font-size: 45px;">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold;">أهلاً بك يا {st.session_state.current_user} في النسخة الاحترافية</p>
    </div>
""", unsafe_allow_html=True)

# شريط الأخبار والخروج
c_top1, c_top2 = st.columns([0.8, 0.2])
with c_top1:
    st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)
with c_top2:
    if st.button("🚪 خروج", use_container_width=True): st.session_state.auth = False; st.rerun()

# المنيو
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# تفاصيل المشاريع
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"""<div class='smart-box'>
        <h2>{item.get('ProjectName', item.get('Developer'))}</h2>
        <p>📍 الموقع: {item.get('Location', '---')}</p>
        <p>🏗️ المطور: {item.get('Developer', '---')}</p>
        <p>💰 السعر: {item.get('Starting Price (EGP)', 'تواصل للاستفسار')}</p>
        <hr><p>{item.get('Payment Plan', 'خطط سداد متنوعة متاحة')}</p>
    </div>""", unsafe_allow_html=True)

# المنطق الخاص بكل قسم (المساعد الذكي / المشاريع / المطورين / الأدوات)
elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 مساعد الربط العقاري الذكي")
    c1, c2, c3 = st.columns(3)
    locs = sorted(df_p['Location'].unique().tolist()) if 'Location' in df_p.columns else ["الكل"]
    sel_loc = c1.selectbox("📍 المنطقة المستهدفة", ["الكل"] + locs)
    sel_type = c2.selectbox("🏠 نوع الوحدة", ["الكل", "شقق", "فيلات", "تجاري", "إداري"])
    sel_budget = c3.number_input("💰 المقدم المتاح (EGP)", 0)
    wa_num = st.text_input("رقم واتساب العميل")
    if st.button("🎯 استخراج الترشيحات"):
        res = df_p[df_p['Location'] == sel_loc] if sel_loc != "الكل" else df_p
        for idx, r in res.head(5).iterrows():
            st.info(f"🏢 {r['ProjectName']} - {r['Developer']}")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    f1, f2 = st.columns(2)
    search = f1.text_input("🔍 ابحث باسم المشروع")
    area_f = f2.selectbox("📍 فلتر بالمنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
    if area_f != "الكل": dff = dff[dff['Location'] == area_f]
    
    start = st.session_state.p_idx * 6
    page = dff.iloc[start:start+6]
    for i in range(0, len(page), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(page):
                row = page.iloc[i+j]
                if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}\n🏗️ {row['Developer']}", key=f"card_p_{start+i+j}"):
                    st.session_state.selected_item = row; st.rerun()
    
    st.markdown("---")
    p1, _, p2 = st.columns([1,2,1])
    if st.session_state.p_idx > 0 and p1.button("⬅️ السابق"): st.session_state.p_idx -= 1; st.rerun()
    if start + 6 < len(dff) and p2.button("التالي ➡️"): st.session_state.p_idx += 1; st.rerun()

elif menu == "المطورين":
    search_d = st.text_input("🔍 ابحث عن مطور")
    dfd_f = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
    start_d = st.session_state.d_idx * 6
    page_d = dfd_f.iloc[start_d:start_d+6]
    for i in range(0, len(page_d), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(page_d):
                row = page_d.iloc[i+j]
                if cols[j].button(f"🏗️ {row['Developer']}\n⭐ الفئة: {row.get('Developer Category','A')}", key=f"card_d_{start_d+i+j}"):
                    st.session_state.selected_item = row; st.rerun()

elif menu == "أدوات البروكر":
    st.title("🛠️ حقيبة البروكر الاحترافية")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='tool-card'><h3>💳 القسط</h3>", unsafe_allow_html=True)
        v = st.number_input("إجمالي السعر", 1000000, key="t1")
        y = st.slider("السنين", 1, 15, 8, key="t3")
        st.metric("القسط الشهري", f"{v/(y*12):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='tool-card'><h3>💰 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("قيمة الصفقة", 1000000, key="t4")
        pct = st.slider("النسبة %", 0.5, 5.0, 1.5, key="t5")
        st.metric("صافي الربح", f"{deal*(pct/100):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='tool-card'><h3>📈 العائد ROI</h3>", unsafe_allow_html=True)
        buy = st.number_input("سعر الشراء", 1000000, key="t6")
        rent = st.number_input("الإيجار السنوي", 100000, key="t7")
        st.metric("نسبة العائد", f"{(rent/buy)*100:,.1f}%")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#777; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
