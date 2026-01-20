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

# 3. إدارة الحالة ودعم الريفريش (Persistence)
query_params = st.query_params
if 'auth' not in st.session_state:
    if "u" in query_params:
        st.session_state.auth = True
        st.session_state.current_user = query_params["u"]
    else:
        st.session_state.auth = False

if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- وظائف الخلفية ---
def login_user(u, p):
    try:
        res = requests.get(f"{SCRIPT_URL}?nocache={time.time()}").json()
        for user in res:
            if (u.lower() == str(user.get('Name')).lower()) and str(p) == str(user.get('Password')): return user.get('Name')
        return None
    except: return None

@st.cache_data(ttl=60)
def load_data():
    try:
        u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
        u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
        p = pd.read_csv(u_p).fillna("---"); d = pd.read_csv(u_d).fillna("---")
        p.rename(columns={'Area': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 4. التنسيق الجمالي (Black Background + Yellow Frame + White Text)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    /* الصفحة كاملة أسود */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {{
        background-color: #000000 !important;
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Cairo', sans-serif;
    }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}

    /* الكتابة أبيض ناصع */
    p, span, div, label, li {{ color: #FFFFFF !important; font-weight: 700 !important; font-size: 17px !important; }}
    h1, h2, h3, h4 {{ color: #FFFF00 !important; font-weight: 900 !important; }}

    /* الأزرار: أسود والفريم أصفر */
    div.stButton > button {{
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFF00 !important;
        border-radius: 10px !important;
        font-weight: 900 !important;
        transition: 0.3s !important;
    }}
    div.stButton > button:hover {{
        background-color: #FFFF00 !important;
        color: #000000 !important;
    }}
    
    /* كروت المشاريع والمطورين */
    div.stButton > button[key*="card_"] {{
        min-height: 120px !important;
        font-size: 18px !important;
        margin-bottom: 10px !important;
    }}

    /* الصناديق والأدوات */
    .smart-box {{ 
        background-color: #000000 !important; 
        border: 2px solid #FFFF00 !important; 
        padding: 20px; 
        border-radius: 15px; 
        margin-bottom: 20px;
    }}
    
    /* المدخلات (Inputs) */
    .stTextInput input, .stSelectbox div, .stNumberInput input {{
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFF00 !important;
        font-weight: bold !important;
    }}
    
    /* شريط الأخبار */
    .ticker-wrap {{ background: #000; border-bottom: 2px solid #FFFF00; padding: 10px 0; }}
    .ticker {{ color: #FFFF00 !important; font-weight: 900; font-size: 15px; }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:50px;'><h1>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    with st.container():
        u = st.text_input("الأسم")
        p = st.text_input("كلمة السر", type="password")
        if st.button("دخول للمنصة"):
            user = "Admin" if p == "2026" else login_user(u, p)
            if user:
                st.session_state.auth = True; st.session_state.current_user = user
                st.query_params["u"] = user; st.rerun()
            else: st.error("خطأ في البيانات")
    st.stop()

# 6. الهيدر والساعة الحية (تحديث كل دقيقة - بدون ثواني)
st.markdown(f"<div class='smart-box' style='text-align:center;'><h1>MA3LOMATI PRO</h1><p>أهلاً بك، {st.session_state.current_user}</p></div>", unsafe_allow_html=True)

c1, c2 = st.columns([0.7, 0.3])
with c1:
    st.markdown(f'<div class="ticker-wrap">🔥 سوق العقارات: متابعة مستمرة لأحدث المشروعات</div>', unsafe_allow_html=True)
with c2:
    st.markdown(f"""
        <div style='text-align: left; padding: 5px; color: #FFFF00; font-size: 15px; font-weight:900;'>
            📅 {egypt_now.strftime('%Y-%m-%d')} | 🕒 <span id="clock">{egypt_now.strftime('%I:%M %p')}</span>
        </div>
        <script>
            function updateClock() {{
                const now = new Date();
                const opt = {{ timeZone: 'Africa/Cairo', hour: '2-digit', minute: '2-digit', hour12: true }};
                document.getElementById('clock').innerHTML = now.toLocaleTimeString('en-US', opt);
            }}
            setInterval(updateClock, 60000);
        </script>
    """, unsafe_allow_html=True)
    if st.button("🚪 خروج"): st.session_state.auth = False; st.query_params.clear(); st.rerun()

# 7. المنيو الرئيسي
menu = option_menu(None, ["المشاريع", "المساعد الذكي", "المطورين", "الأدوات"], 
    icons=["building", "robot", "people", "calculator"], orientation="horizontal",
    styles={
        "container": {"background-color": "#000", "border": "1px solid #FFFF00"},
        "nav-link": {"color": "#FFF"},
        "nav-link-selected": {"background-color": "#FFFF00", "color": "#000", "font-weight": "bold"}
    })

# 8. محتوى الصفحات
if menu == "المشاريع":
    f1, f2 = st.columns(2)
    s = f1.text_input("🔍 ابحث")
    l = f2.selectbox("📍 المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    res = df_p[df_p['ProjectName'].str.contains(s, case=False)] if s else df_p
    if l != "الكل": res = res[res['Location'] == l]
    
    for i, row in res.head(8).iterrows():
        if st.button(f"🏢 {row['ProjectName']} | 📍 {row['Location']}", key=f"card_p_{i}"):
            st.session_state.selected_item = row; st.rerun()

elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'><h3>🤖 المساعد الذكي</h3><p>أدخل طلب العميل لاستخراج الترشيحات...</p></div>", unsafe_allow_html=True)

elif menu == "المطورين":
    for i, r in df_d.head(10).iterrows():
        if st.button(f"🏗️ {r['Developer']}", key=f"card_d_{i}"):
            st.session_state.selected_item = r; st.rerun()

elif menu == "الأدوات":
    st.markdown("<div class='smart-box'><h3>🛠️ حاسبة البروكر</h3>", unsafe_allow_html=True)
    v = st.number_input("السعر", 1000000)
    st.metric("القسط (8 سنين)", f"{v/96:,.0f}")
    st.markdown("</div>", unsafe_allow_html=True)

# عرض التفاصيل
if st.session_state.selected_item is not None:
    st.markdown("---")
    if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
    st.markdown(f"<div class='smart-box'><h2>التفاصيل الكاملة</h2><p>{st.session_state.selected_item}</p></div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
