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

# 2. روابط الربط (الـ Apps Script والجوجل شيت)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# 3. إدارة الحالة والتوقيت
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

# جلب الأخبار
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى في مصر لعام 2026."

news_text = get_real_news()

# 4. التنسيق الجمالي عالي الوضوح (High Contrast CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* الخلفية سوداء تماماً لبروز الخطوط */
    [data-testid="stAppViewContainer"] {{ background-color: #000000; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}

    /* وضوح النصوص: أبيض ناصع بدلاً من الرمادي */
    p, span, div, label, li {{ color: #FFFFFF !important; font-weight: 700 !important; font-size: 16px !important; }}
    
    /* العناوين: ذهبي ساطع جداً */
    h1, h2, h3, h4 {{ color: #FFD700 !important; font-weight: 900 !important; }}

    /* شريط الأخبار */
    .ticker-wrap {{ width: 100%; background: #111; padding: 10px 0; border-bottom: 2px solid #FFD700; margin-bottom: 20px; }}
    .ticker {{ color: #FFFFFF !important; font-weight: 900; }}

    /* الكروت: خلفية بيضاء وخط أسود للوضوح المطلق */
    div.stButton > button[key*="card_"] {{
        background-color: #FFFFFF !important; 
        color: #000000 !important; 
        min-height: 140px !important; 
        text-align: right !important;
        font-weight: 900 !important; 
        font-size: 18px !important;
        border: 3px solid #FFD700 !important;
        border-radius: 15px !important;
        margin-bottom: 10px !important;
        width: 100% !important;
    }}
    
    /* الصناديق والأدوات */
    .smart-box {{ background: #111; border: 2px solid #FFD700; padding: 25px; border-radius: 20px; color: white; }}
    .tool-card {{ background: #1a1a1a; padding: 20px; border-radius: 15px; border: 2px solid #FFD700; text-align: center; }}
    
    /* المدخلات (Inputs) */
    .stTextInput input, .stSelectbox div, .stNumberInput input {{
        background-color: #1a1a1a !important;
        color: #FFFFFF !important;
        border: 2px solid #FFD700 !important;
        font-size: 17px !important;
        font-weight: bold !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول والاشتراك
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:50px;'><h1 style='font-size:60px;'>MA3LOMATI PRO</h1><p style='color:white; font-size:20px;'>سجل دخولك للوصول للبيانات</p></div>", unsafe_allow_html=True)
    tab_login, tab_signup = st.tabs(["🔐 تسجيل دخول", "📝 اشتراك جديد"])
    with tab_login:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            u_input = st.text_input("الأسم أو الجيميل", key="log_user")
            p_input = st.text_input("كلمة السر", type="password", key="log_pass")
            if st.button("دخول للمنصة 🚀"):
                if p_input == "2026":
                    st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
                else:
                    user_verified = login_user(u_input, p_input)
                    if user_verified:
                        st.session_state.auth = True; st.session_state.current_user = user_verified; st.rerun()
                    else: st.error("بيانات الدخول غير صحيحة")
    with tab_signup:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            reg_name = st.text_input("الأسم بالكامل")
            reg_pass = st.text_input("كلمة السر المرجوة", type="password")
            reg_email = st.text_input("الجيميل")
            reg_wa = st.text_input("رقم الواتساب")
            reg_co = st.text_input("الشركة")
            if st.button("تأكيد الاشتراك ✅"):
                if reg_name and reg_pass and reg_email:
                    if signup_user(reg_name, reg_pass, reg_email, reg_wa, reg_co):
                        st.success("تم تسجيلك بنجاح! انتقل للدخول.")
                    else: st.error("حدث خطأ في الاتصال")
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

# 7. الهيدر
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 180px; background-size: cover; background-position: center; border-radius: 0 0 30px 30px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 5px solid #FFD700;">
        <h1 style="margin: 0; font-size: 40px;">MA3LOMATI PRO</h1>
        <p style="color: #FFD700 !important; font-weight: bold;">أهلاً بك، {st.session_state.current_user}</p>
    </div>
""", unsafe_allow_html=True)

# 8. شريط المعلومات
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)
if st.button("🚪 خروج الآمن"): st.session_state.auth = False; st.rerun()

# 9. المنيو الرئيسي
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#FFD700", "color": "black", "font-weight": "bold"}})

# 10. تفاصيل المشروع
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"""<div class='smart-box'>
        <h2>{item.get('ProjectName', item.get('Developer'))}</h2>
        <p>📍 الموقع: {item.get('Location', '---')}</p>
        <p>🏗️ المطور: {item.get('Developer', '---')}</p>
        <p>💰 السعر: {item.get('Starting Price (EGP)', 'تواصل للاستفسار')}</p>
    </div>""", unsafe_allow_html=True)

# --- 11. المساعد الذكي ---
elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 المساعد العقاري الذكي")
    c1, c2 = st.columns(2)
    locs = sorted(df_p['Location'].unique().tolist())
    sel_loc = c1.selectbox("📍 المنطقة المستهدفة", ["الكل"] + locs)
    client_wa = st.text_input("رقم واتساب العميل (بدون أصفار)")
    if st.button("🎯 استخراج الترشيحات"):
        res = df_p[df_p['Location'] == sel_loc] if sel_loc != "الكل" else df_p
        st.success(f"وجدنا {len(res.head(5))} مشاريع مناسبة!")
        for _, r in res.head(5).iterrows():
            st.write(f"🏢 **{r['ProjectName']}** | {r['Developer']}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 12. المشاريع ---
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

# --- 14. أدوات البروكر ---
elif menu == "أدوات البروكر":
    st.title("🛠️ حقيبة الأدوات الاحترافية")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='tool-card'><h3>💳 حاسبة القسط</h3>", unsafe_allow_html=True)
        v = st.number_input("إجمالي السعر", 1000000)
        y = st.slider("السنين", 1, 15, 8)
        st.metric("القسط الشهري", f"{v/(y*12):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='tool-card'><h3>💰 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("قيمة الصفقة", 1000000)
        pct = st.slider("النسبة %", 0.5, 5.0, 1.5)
        st.metric("صافي الربح", f"{deal*(pct/100):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='tool-card'><h3>📝 الضرائب</h3>", unsafe_allow_html=True)
        tax = st.number_input("سعر العقار", 1000000, key="tax")
        st.write(f"تصرفات عقارية (2.5%):")
        st.subheader(f"{tax*0.025:,.0f} ج.م")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#888; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
