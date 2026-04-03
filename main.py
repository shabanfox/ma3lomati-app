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
# استبدل هذا الرابط برابط الـ Web App الخاص بك من Google Apps Script
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'messages' not in st.session_state: st.session_state.messages = []

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- 4. وظائف الربط مع جوجل شيت ---
def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload, timeout=10)
        return response.text == "Success"
    except: return False

def login_user(user_input, pwd_input):
    try:
        # إضافة nocache لمنع المتصفح من كاش البيانات القديمة
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=15)
        if response.status_code == 200:
            users_list = response.json()
            user_input = str(user_input).strip().lower()
            pwd_input = str(pwd_input).strip()

            for user_data in users_list:
                # محاولة قراءة الأعمدة باختلاف حالة الأحرف (Name أو name)
                name_s = str(user_data.get('Name', user_data.get('name', ''))).strip()
                email_s = str(user_data.get('Email', user_data.get('email', ''))).strip()
                pass_s = str(user_data.get('Password', user_data.get('password', ''))).strip()

                if (user_input == name_s.lower() or user_input == email_s.lower()) and pwd_input == pass_s:
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

# --- 5. التصميم الجمالي CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}

    /* تصميم شاشة الدخول */
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: flex-start; width: 100%; padding-top: 50px; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 24px; font-weight: 900;
        text-align: center; z-index: 10; margin-bottom: -30px; min-width: 360px;
    }}
    .auth-card {{ background-color: #ffffff; width: 380px; padding: 55px 35px 30px 35px; border-radius: 30px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); }}
    .auth-card div.stTextInput input {{ background-color: #f8f9fa !important; color: #000 !important; border: 1px solid #ddd !important; border-radius: 12px !important; text-align: center !important; height: 45px !important; }}

    /* تصميم المحتوى الداخلي */
    .ticker-wrap {{ width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 20px; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 3px solid #f59e0b;
        padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 20px;
    }}
    
    .detail-card, .tool-card {{ background: rgba(20, 20, 20, 0.9); padding: 25px; border-radius: 20px; border-top: 5px solid #f59e0b; color: white; border: 1px solid #333; margin-bottom:20px; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 16px; margin-top: 10px; }}
    .val-white {{ color: white; font-size: 18px; border-bottom: 1px solid #333; padding-bottom:5px; margin-bottom: 10px; }}

    div.stButton > button {{ border-radius: 12px !important; font-family: 'Cairo', sans-serif !important; transition: 0.3s !important; }}
    div.stButton > button[key*="card_"] {{
        background-color: white !important; color: #111 !important;
        min-height: 140px !important; text-align: right !important;
        font-weight: bold !important; font-size: 15px !important;
        border: none !important; margin-bottom: 10px !important;
        display: block !important; width: 100% !important;
    }}
    div.stButton > button[key*="card_"]:hover {{ transform: translateY(-5px) !important; border-right: 8px solid #f59e0b !important; box-shadow: 0 10px 20px rgba(245,158,11,0.2) !important; }}
    
    .stSelectbox label, .stTextInput label, .stNumberInput label {{ color: #f59e0b !important; font-weight: bold !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. صفحة الدخول ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>MA3LOMATI PRO</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["🔐 تسجيل دخول", "📝 اشتراك جديد"])
    
    with tab_login:
        u_input = st.text_input("User", placeholder="الأسم أو الجيميل", label_visibility="collapsed", key="log_user")
        p_input = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="log_pass")
        if st.button("SIGN IN 🚀", use_container_width=True):
            if p_input == "2026": # كود دخول مباشر للطوارئ
                st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
            else:
                user_verified = login_user(u_input, p_input)
                if user_verified:
                    st.session_state.auth = True; st.session_state.current_user = user_verified; st.rerun()
                else: st.error("بيانات الدخول غير صحيحة")

    with tab_signup:
        reg_name = st.text_input("الأسم", placeholder="الاسم بالكامل")
        reg_pass = st.text_input("كلمة السر", type="password", placeholder="كلمة السر")
        reg_email = st.text_input("الجيميل", placeholder="الإيميل")
        reg_wa = st.text_input("الواتساب", placeholder="رقم الموبايل")
        reg_co = st.text_input("الشركة", placeholder="اسم الشركة")
        if st.button("تأكيد الاشتراك ✅", use_container_width=True):
            if reg_name and reg_pass and reg_email:
                if signup_user(reg_name, reg_pass, reg_email, reg_wa, reg_co):
                    st.success("تم تسجيلك بنجاح! جرب تسجيل الدخول الآن.")
                else: st.error("فشل الاتصال بالسيرفر")
            else: st.warning("يرجى ملء البيانات")
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 7. جلب البيانات ---
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

df_p, df_d, df_l = load_data()

# --- 8. الهيدر الداخلي ---
st.markdown(f"""
    <div class="royal-header">
        <h1 style="color: white; margin: 0; font-size: 45px; text-shadow: 2px 2px 10px rgba(0,0,0,0.5);">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-size: 18px;">أهلاً بك يا {st.session_state.current_user} في النسخة الاحترافية</p>
    </div>
""", unsafe_allow_html=True)

c_top1, c_top2 = st.columns([0.8, 0.2])
with c_top1:
    st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)
with c_top2:
    if st.button("🚪 خروج", use_container_width=True): st.session_state.auth = False; st.rerun()

# --- 9. القائمة الرئيسية ---
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["briefcase", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

if 'last_menu' not in st.session_state or menu != st.session_state.last_menu:
    st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu

# --- 10. محتوى الصفحات ---
if menu == "أدوات البروكر":
    st.markdown("<h2 style='text-align:center; color:#f59e0b;'>🛠️ أدوات البروكر</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.subheader("💳 حساب القسط")
            v = st.number_input("إجمالي السعر", 1000000)
            y = st.slider("عدد السنين", 1, 15, 8)
            st.metric("القسط الشهري", f"{v/(y*12):,.0f}")
    with c2:
        with st.container(border=True):
            st.subheader("💰 العمولة")
            deal = st.number_input("قيمة الصفقة", 1000000)
            pct = st.slider("النسبة %", 1.0, 5.0, 2.5)
            st.metric("صافي الربح", f"{deal*(pct/100):,.0f}")
    with c3:
        with st.container(border=True):
            st.subheader("📈 العائد ROI")
            buy = st.number_input("سعر الشراء", 1000000)
            rent = st.number_input("الإيجار السنوي", 100000)
            st.metric("نسبة العائد", f"{(rent/buy)*100:,.1f}%")

elif menu == "المساعد الذكي":
    st.markdown("<div class='detail-card'><h3>🤖 مساعد معلوماتي الذكي</h3></div>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    if pmt := st.chat_input("اسألني عن أي مشروع أو مطور..."):
        st.session_state.messages.append({"role": "user", "content": pmt})
        st.session_state.messages.append({"role": "assistant", "content": "جاري مراجعة قواعد البيانات... يفضل التركيز على المشاريع ذات التسليم القريب لضمان أعلى عائد."})
        st.rerun()

else:
    active_df = df_p if menu=="المشاريع" else (df_l if menu=="Launches" else df_d)
    if active_df.empty: st.error("لا توجد بيانات متاحة حالياً")
    else:
        col_main = active_df.columns[0]
        
        # عرض التفاصيل
        if st.session_state.view == "details":
            item = active_df.iloc[st.session_state.current_index]
            if st.button("⬅ عودة للقائمة", use_container_width=True):
                st.session_state.view = "grid"; st.rerun()
            
            c1, c2, c3 = st.columns(3)
            all_cols = active_df.columns
            n = len(all_cols)
            for i, col_set in enumerate([all_cols[:n//3+1], all_cols[n//3+1:2*n//3+1], all_cols[2*n//3+1:]]):
                with [c1, c2, c3][i]:
                    h = '<div class="detail-card">'
                    for k in col_set: h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                    st.markdown(h+'</div>', unsafe_allow_html=True)

        # عرض الشبكة (Grid)
        else:
            search = st.text_input("🔍 بحث سريع...")
            filt = active_df[active_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else active_df
            start = st.session_state.page_num * ITEMS_PER_PAGE
            disp = filt.iloc[start : start + ITEMS_PER_PAGE]
            
            main_c, side_c = st.columns([0.8, 0.2])
            with main_c:
                grid = st.columns(2)
                for i, (idx, r) in enumerate(disp.iterrows()):
                    with grid[i%2]:
                        name = r[col_main]
                        loc = r.get('Location', '---')
                        dev = r.get('Developer', '---')
                        if st.button(f"🏢 {name}\n📍 {loc}\n🏗️ {dev}", key=f"card_{idx}"):
                            st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()
            
            with side_c:
                st.markdown("<p style='color:#f59e0b; font-weight:bold;'>🏆 مقترحات</p>", unsafe_allow_html=True)
                for _, s in active_df.head(6).iterrows():
                    st.markdown(f"<div class='mini-side-card' style='background:rgba(255,255,255,0.05); padding:10px; border-radius:10px; margin-bottom:5px; border-right:3px solid #f59e0b;'>{s[col_main][:25]}</div>", unsafe_allow_html=True)
            
            # التنقل بين الصفحات
            st.write("---")
            p1, _, p2 = st.columns([1, 2, 1])
            if st.session_state.page_num > 0:
                if p1.button("⬅ السابق"): st.session_state.page_num -= 1; st.rerun()
            if (start + ITEMS_PER_PAGE) < len(filt):
                if p2.button("التالي ➡"): st.session_state.page_num += 1; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026 | جميع الحقوق محفوظة</p>", unsafe_allow_html=True)
