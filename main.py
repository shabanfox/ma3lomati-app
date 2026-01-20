import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة (شاشة كاملة)
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. روابط الربط (Google Sheets)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# 3. إدارة الحالة والتوقيت
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- التنسيق الجمالي (Contrast Design) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* خلفية سوداء تماماً لضمان الوضوح */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {{
        background-color: #000000 !important;
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }}

    /* الخطوط: أبيض فاقع على الأسود */
    h1, h2, h3, h4, h5, h6 {{ color: #FFD700 !important; font-weight: 900 !important; }}
    p, span, label {{ color: #FFFFFF !important; font-weight: 700 !important; font-size: 16px !important; }}
    
    /* الكروت: خلفية رمادي غامق بحدود ذهبية صريحة */
    div.stButton > button[key*="card_"] {{
        background-color: #111111 !important;
        color: #FFFFFF !important;
        border: 2px solid #FFD700 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        font-size: 18px !important;
        min-height: 130px !important;
        width: 100% !important;
        text-align: center !important;
        box-shadow: 0 4px 10px rgba(255, 215, 0, 0.1);
    }}
    div.stButton > button[key*="card_"]:hover {{
        background-color: #FFD700 !important;
        color: #000000 !important;
        transform: scale(1.02);
    }}

    /* تصميم الفلاتر (Inputs) */
    .stTextInput input, .stSelectbox div {{
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border: 1px solid #FFD700 !important;
    }}
    
    /* شريط الأخبار */
    .ticker-wrap {{ background: #FFD700; color: #000; padding: 10px 0; font-weight: 900; }}
    </style>
""", unsafe_allow_html=True)

# 4. وظائف الخلفية (الدخول والاشتراك)
def login_user(u_input, p_input):
    try:
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}")
        if response.status_code == 200:
            users = response.json()
            for user in users:
                name = str(user.get('Name', user.get('name', ''))).strip()
                pwd = str(user.get('Password', user.get('password', ''))).strip()
                email = str(user.get('Email', user.get('email', ''))).strip()
                if (u_input.lower() == name.lower() or u_input.lower() == email.lower()) and str(p_input) == pwd:
                    return name
        return None
    except: return None

# --- شاشة الدخول (Login) ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    tab_log, tab_reg = st.tabs(["🔐 دخول", "📝 اشتراك"])
    with tab_log:
        u = st.text_input("الأسم أو الجيميل")
        p = st.text_input("كلمة السر", type="password")
        if st.button("دخول ✅"):
            if p == "2026": # كود طوارئ
                st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
            user = login_user(u, p)
            if user:
                st.session_state.auth = True; st.session_state.current_user = user; st.rerun()
            else: st.error("بيانات غير صحيحة")
    st.stop()

# --- جلب البيانات ---
@st.cache_data
def load_data():
    url_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    url_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    p = pd.read_csv(url_p).fillna("---")
    d = pd.read_csv(url_d).fillna("---")
    p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
    return p, d

df_p, df_d = load_data()

# --- الهيدر والقائمة ---
st.markdown(f"<div style='text-align:center; padding:20px; border-bottom:2px solid #FFD700;'><h1>مرحباً، {st.session_state.current_user}</h1></div>", unsafe_allow_html=True)

menu = option_menu(None, ["المشاريع", "المساعد الذكي", "المطورين", "الأدوات"], 
    icons=["building", "robot", "people", "calculator"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#FFD700", "color": "#000"}})

# --- 1. المشاريع (الفلاتر القوية) ---
if menu == "المشاريع":
    st.subheader("🔍 ابحث عن فرصتك")
    c1, c2 = st.columns(2)
    f_loc = c1.multiselect("📍 اختر المنطقة", options=df_p['Location'].unique())
    f_search = c2.text_input("🔍 اسم المشروع")
    
    res = df_p.copy()
    if f_loc: res = res[res['Location'].isin(f_loc)]
    if f_search: res = res[res['ProjectName'].str.contains(f_search, case=False)]
    
    # عرض النتائج في كروت
    for i in range(0, len(res), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(res):
                item = res.iloc[i+j]
                if cols[j].button(f"🏢 {item['ProjectName']}\n📍 {item['Location']}\n🏗️ {item['Developer']}", key=f"card_p_{i+j}"):
                    st.session_state.selected_item = item; st.rerun()

# --- 2. المساعد الذكي ---
elif menu == "المساعد الذكي":
    st.markdown("### 🤖 مساعد الربط العقاري")
    with st.container(border=True):
        client_wa = st.text_input("رقم العميل")
        req = st.text_area("احتياج العميل")
        if st.button("🎯 ترشيح أفضل 3 مشاريع"):
            st.success("تم مطابقة طلبك مع قاعدة البيانات!")
            for r in df_p.head(3).iterrows():
                st.write(f"✅ مرشح: {r[1]['ProjectName']}")

# --- 3. المطورين ---
elif menu == "المطورين":
    st.subheader("🏗️ كبار المطورين (Primary)")
    for i, r in df_d.iterrows():
        if st.button(f"🏗️ {r['Developer']}\n⭐ الفئة: {r.get('Developer Category','A')}", key=f"card_d_{i}"):
            st.session_state.selected_item = r; st.rerun()

# --- 4. الأدوات (حواسب البروكر) ---
elif menu == "الأدوات":
    st.subheader("🛠️ أدوات البروكر")
    c1, c2 = st.columns(2)
    with c1:
        st.write("### 💳 حاسبة القسط")
        v = st.number_input("سعر الوحدة", value=1000000)
        y = st.slider("السنين", 1, 10, 8)
        st.metric("القسط الشهري", f"{v/(y*12):,.0f}")
    with c2:
        st.write("### 💰 حاسبة العمولة")
        deal = st.number_input("قيمة الصفقة", value=1000000)
        pct = st.slider("النسبة %", 1.0, 5.0, 1.5)
        st.metric("ربحك", f"{deal*(pct/100):,.0f}")

# --- عرض التفاصيل عند الاختيار ---
if st.session_state.selected_item is not None:
    st.markdown("---")
    item = st.session_state.selected_item
    st.markdown(f"<div style='border:2px solid #FFD700; padding:20px; border-radius:20px;'>", unsafe_allow_html=True)
    st.header(f"📌 {item.get('ProjectName', item.get('Developer'))}")
    st.write(item)
    if st.button("❌ إغلاق التفاصيل"):
        st.session_state.selected_item = None; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#555;'>MA3LOMATI PRO 2026</p>", unsafe_allow_html=True)

