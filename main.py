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

# --- 2. الرابط الخاص بك (تأكد من عمل Deploy جديد كـ Anyone) ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzT_YOHvummf-xi8iWzmdVeJSK-TKcvkHLtt5F91MoahqH-d-F2BOvvLF4D8Pjmzww-Ag/exec"

# --- 3. إدارة حالة الجلسة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- 4. وظائف الربط (Backend) ---
def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        return response.text == "Success"
    except: return False

def login_user(user_input, pwd_input):
    try:
        # إضافة timestamp لمنع المتصفح من كاش البيانات القديمة
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}")
        if response.status_code == 200:
            users_list = response.json()
            for user_data in users_list:
                # جلب البيانات بناءً على أسماء الأعمدة في الشيت
                name_s = str(user_data.get('Name', '')).strip()
                pass_s = str(user_data.get('Password', '')).strip()
                email_s = str(user_data.get('Email', '')).strip()
                
                if (user_input.strip() == name_s or user_input.strip() == email_s) and str(pwd_input).strip() == pass_s:
                    return name_s
        return None
    except Exception as e:
        st.error(f"خطأ في الاتصال: {e}")
        return None

# --- 5. التصميم الجمالي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { background-color: #111; border-radius: 10px; color: white; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #f59e0b !important; color: black !important; }

    div.stButton > button { border-radius: 12px !important; font-family: 'Cairo', sans-serif !important; background-color: #f59e0b !important; color: black !important; font-weight: bold !important; width: 100%; }
    .smart-box { background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; }
    .stTextInput label { color: #f59e0b !important; }
    </style>
""", unsafe_allow_html=True)

# --- 6. نظام الدخول والاشتراك ---
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:50px;'><h1 style='color:#f59e0b; font-size:60px;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 تسجيل دخول", "📝 اشتراك جديد"])
    
    with tab1:
        _, col, _ = st.columns([1,1.5,1])
        with col:
            u_log = st.text_input("الأسم أو الجيميل", key="log_u")
            p_log = st.text_input("كلمة السر", type="password", key="log_p")
            if st.button("دخول آمن 🚀"):
                with st.spinner("جاري التحقق من البيانات..."):
                    user_name = login_user(u_log, p_log)
                    if user_name:
                        st.session_state.auth = True
                        st.session_state.current_user = user_name
                        st.rerun()
                    else:
                        st.error("بيانات الدخول غير صحيحة، تأكد من الاسم وكلمة السر")

    with tab2:
        _, col, _ = st.columns([1,1.5,1])
        with col:
            r_name = st.text_input("الأسم بالكامل")
            r_pass = st.text_input("كلمة السر المرجوة")
            r_mail = st.text_input("الجيميل")
            r_wa = st.text_input("رقم الواتساب")
            r_co = st.text_input("الشركة")
            if st.button("إرسال طلب الانضمام ✅"):
                if r_name and r_pass and r_mail:
                    if signup_user(r_name, r_pass, r_mail, r_wa, r_co):
                        st.success("تم تسجيلك بنجاح! يمكنك الآن العودة لخانة تسجيل الدخول")
                    else: st.error("حدث خطأ في الإرسال، جرب مرة أخرى")
                else: st.warning("برجاء ملء البيانات الأساسية")
    st.stop()

# --- 7. محتوى المنصة (يظهر بعد الدخول) ---

# جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        p.rename(columns={'Area': 'Location', 'Project Name': 'ProjectName'}, inplace=True, errors='ignore')
        return p
    except: return pd.DataFrame()

df_p = load_data()

# الهيدر
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 150px; background-size: cover; background-position: center; border-radius: 0 0 30px 30px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b;">
        <h1 style="color: white; margin: 0; font-size: 35px;">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b;">مرحباً بك يا {st.session_state.current_user} في منصة 2026</p>
    </div>
""", unsafe_allow_html=True)

# المنيو
menu = option_menu(None, ["المشاريع", "المساعد الذكي", "أدوات البروكر"], 
    icons=["building", "robot", "briefcase"], default_index=0, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if menu == "المشاريع":
    search = st.text_input("🔍 ابحث عن مشروع...")
    dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
    
    # عرض المشاريع بشكل كروت
    for i in range(0, len(dff.head(10)), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(dff):
                row = dff.iloc[i+j]
                with cols[j].container(border=True):
                    st.markdown(f"### {row['ProjectName']}")
                    st.write(f"📍 الموقع: {row.get('Location','---')}")
                    if st.button("عرض التفاصيل", key=f"btn_{i+j}"):
                        st.info(f"عرض بيانات مشروع: {row['ProjectName']}")

elif menu == "أدوات البروكر":
    if st.button("🚪 تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
