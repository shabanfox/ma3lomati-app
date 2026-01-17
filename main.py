import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. الرابط الخاص بك لربط الجوجل شيت (الـ Apps Script)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzT_YOHvummf-xi8iWzmdVeJSK-TKcvkHLtt5F91MoahqH-d-F2BOvvLF4D8Pjmzww-Ag/exec"

# 3. إدارة حالة الجلسة والتوقيت
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# 4. وظائف الربط مع جوجل شيت (تسجيل ودخول)
def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        return response.text == "Success"
    except: return False

def login_user(user_input, pwd_input):
    try:
        response = requests.get(SCRIPT_URL)
        if response.status_code == 200:
            users = response.json()
            for row in users[1:]:
                if len(row) >= 3:
                    name_s, pass_s, email_s = str(row[0]).strip(), str(row[1]).strip(), str(row[2]).strip()
                    if (user_input == name_s or user_input == email_s) and str(pwd_input) == pass_s:
                        return name_s
        return None
    except: return None

# 5. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    
    .ticker-wrap { width: 100%; background: transparent; padding: 5px 0; border-bottom: 1px solid #222; margin-bottom: 20px; overflow: hidden; }
    .ticker { display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; white-space: nowrap; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    div.stButton > button { border-radius: 12px !important; font-family: 'Cairo', sans-serif !important; transition: 0.3s !important; }
    div.stButton > button[key*="card_"] {
        background-color: white !important; color: #111 !important; min-height: 120px !important; 
        text-align: right !important; font-weight: bold !important; display: block !important; width: 100% !important;
    }
    .smart-box { background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; margin-bottom: 20px; }
    .tool-card { background: #1a1a1a; padding: 20px; border-radius: 15px; border-top: 4px solid #f59e0b; text-align: center; height: 100%; }
    .stSelectbox label, .stTextInput label { color: #f59e0b !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# 6. شاشة الدخول والاشتراك
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:50px;'><h1 style='color:#f59e0b; font-size:60px;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔐 تسجيل دخول", "📝 اشتراك جديد"])
    
    with tab1:
        _, col, _ = st.columns([1,1.5,1])
        with col:
            u_log = st.text_input("الأسم أو الجيميل", key="login_u")
            p_log = st.text_input("كلمة السر", type="password", key="login_p")
            if st.button("دخول للمنصة 🚀", use_container_width=True):
                user_name = login_user(u_log, p_log)
                if user_name:
                    st.session_state.auth = True
                    st.session_state.current_user = user_name
                    st.rerun()
                else: st.error("بيانات الدخول غير صحيحة")
    
    with tab2:
        _, col, _ = st.columns([1,1.5,1])
        with col:
            r_name = st.text_input("الأسم بالكامل")
            r_pass = st.text_input("كلمة السر المرجوة")
            r_mail = st.text_input("الجيميل")
            r_wa = st.text_input("رقم الواتساب")
            r_co = st.text_input("الشركة")
            if st.button("تأكيد الاشتراك ✅", use_container_width=True):
                if r_name and r_pass and r_mail:
                    if signup_user(r_name, r_pass, r_mail, r_wa, r_co):
                        st.success("تم تسجيلك! انتقل لتبويب تسجيل الدخول الآن.")
                    else: st.error("حدث خطأ في الاتصال بالجوجل شيت")
                else: st.warning("برجاء إدخال البيانات الأساسية")
    st.stop()

# --- محتوى المنصة بعد تسجيل الدخول ---

# 7. جلب بيانات العقارات والأخبار
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.rename(columns={'Area': 'Location', 'Project Name': 'ProjectName'}, inplace=True, errors='ignore')
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 8. الهيدر والترحيب
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 180px; background-size: cover; background-position: center; border-radius: 0 0 30px 30px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b;">
        <h1 style="color: white; margin: 0; font-size: 40px;">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold;">أهلاً بك يا {st.session_state.current_user} | {egypt_now.strftime('%I:%M %p')}</p>
    </div>
""", unsafe_allow_html=True)

# 9. المنيو الرئيسي
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], default_index=0, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# 10. عرض المحتوى بناءً على المنيو
if menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 مساعد الربط العقاري")
    c1, c2 = st.columns(2)
    loc = c1.selectbox("📍 المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()) if 'Location' in df_p.columns else ["الكل"])
    budget = c2.number_input("💰 الميزانية التقريبية (EGP)", 0)
    if st.button("🎯 استخراج الترشيحات"):
        st.write("جاري البحث في قاعدة البيانات...")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    search = st.text_input("🔍 ابحث عن مشروع...")
    dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
    
    start = st.session_state.p_idx * 6
    page = dff.iloc[start:start+6]
    
    for i in range(0, len(page), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(page):
                row = page.iloc[i+j]
                if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row.get('Location','---')}", key=f"card_p_{start+i+j}"):
                    st.session_state.selected_item = row
                    
    # أزرار التنقل
    c_p1, _, c_p2 = st.columns([1,3,1])
    if start > 0 and c_p1.button("⬅️ السابق"): st.session_state.p_idx -= 1; st.rerun()
    if start + 6 < len(dff) and c_p2.button("التالي ➡️"): st.session_state.p_idx += 1; st.rerun()

elif menu == "أدوات البروكر":
    st.title("🛠️ حقيبة الأدوات")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='tool-card'><h3>💳 حساب القسط</h3>", unsafe_allow_html=True)
        total = st.number_input("إجمالي السعر", 1000000)
        years = st.slider("عدد السنوات", 1, 15, 8)
        st.metric("القسط الشهري", f"{total/(years*12):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.auth = False
            st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
