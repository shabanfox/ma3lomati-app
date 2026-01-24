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

# --- 2. الروابط (تأكد أن الرابط يعمل) ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'page_num' not in st.session_state: st.session_state.page_num = 0

# --- 4. وظائف الربط مع جوجل شيت (تم تحسينها للفحص) ---
def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload, timeout=10)
        return response.text == "Success"
    except: return False

def login_user(user_input, pwd_input):
    try:
        # جلب البيانات مع منع الكاش
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=15)
        if response.status_code == 200:
            users_list = response.json()
            
            # تنظيف مدخلات المستخدم
            user_input = str(user_input).strip().lower()
            pwd_input = str(pwd_input).strip()

            for user_data in users_list:
                # محاولة جلب القيم بغض النظر عن حالة الأحرف في الشيت
                # نقوم بتجربة Name, name, الاسم ... إلخ
                u_name = str(user_data.get('Name', user_data.get('name', user_data.get('الاسم', '')))).strip()
                u_email = str(user_data.get('Email', user_data.get('email', user_data.get('الايميل', '')))).strip()
                u_pass = str(user_data.get('Password', user_data.get('password', user_data.get('الباسورد', '')))).strip()

                # التحقق
                if (user_input == u_name.lower() or user_input == u_email.lower()) and pwd_input == u_pass:
                    return u_name
        return None
    except Exception as e:
        st.error(f"خطأ في الاتصال: {e}")
        return None

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
    .auth-card {{ background-color: #ffffff; width: 400px; padding: 40px; border-radius: 30px; text-align: center; margin: auto; }}
    .stTextInput input {{ text-align: center !important; border-radius: 10px !important; }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; padding: 40px; text-align: center; border-bottom: 3px solid #f59e0b; border-radius: 0 0 40px 40px;
    }}
    .detail-card {{ background: rgba(30, 30, 30, 0.9); padding: 20px; border-radius: 15px; border: 1px solid #444; color: white; margin-bottom: 10px; }}
    .label-gold {{ color: #f59e0b; font-weight: bold; margin-top: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. منطق تسجيل الدخول ---
if not st.session_state.auth:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    with st.container():
        _, center, _ = st.columns([1, 2, 1])
        with center:
            st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
            st.image("https://cdn-icons-png.flaticon.com/512/3064/3064197.png", width=80)
            st.markdown("<h2 style='color:black;'>MA3LOMATI PRO</h2>", unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["تسجيل دخول", "حساب جديد"])
            
            with tab1:
                u = st.text_input("الأسم أو الإيميل", key="l_u")
                p = st.text_input("كلمة السر", type="password", key="l_p")
                if st.button("دخول 🚀", use_container_width=True):
                    if p == "2026": # كود الطوارئ لضمان دخولك أنت دائماً
                        st.session_state.auth = True; st.session_state.current_user = "المشرف"; st.rerun()
                    else:
                        found_user = login_user(u, p)
                        if found_user:
                            st.session_state.auth = True; st.session_state.current_user = found_user; st.rerun()
                        else:
                            st.error("بيانات الدخول غير صحيحة أو لم يتم تحديث الشيت بعد")
            
            with tab2:
                n_u = st.text_input("الاسم بالكامل")
                n_e = st.text_input("الإيميل")
                n_p = st.text_input("كلمة السر")
                n_w = st.text_input("رقم الواتساب")
                if st.button("إنشاء حساب ✅", use_container_width=True):
                    if n_u and n_p and n_e:
                        if signup_user(n_u, n_p, n_e, n_w, "Company"):
                            st.success("تم الاشتراك! انتظر ثواني ثم سجل دخولك.")
                        else: st.error("فشل في إرسال البيانات")
            st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 7. جلب البيانات (المشاريع والمطورين) ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    try:
        p, d = pd.read_csv(U_P).fillna("---"), pd.read_csv(U_D).fillna("---")
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# --- 8. واجهة التطبيق الداخلية ---
st.markdown(f"""<div class='royal-header'><h1>MA3LOMATI PRO</h1><p>مرحباً بك: {st.session_state.current_user}</p></div>""", unsafe_allow_html=True)

menu = option_menu(None, ["المشاريع", "المطورين", "أدوات"], 
    icons=["house", "building", "tools"], orientation="horizontal")

if menu == "المشاريع":
    search = st.text_input("🔍 ابحث عن مشروع...")
    filt = df_p[df_p.iloc[:,0].str.contains(search, case=False)] if search else df_p
    
    # عرض الكروت
    cols = st.columns(2)
    for i, (idx, row) in enumerate(filt.head(10).iterrows()):
        with cols[i%2]:
            with st.container():
                st.markdown(f"""<div class='detail-card'>
                    <h3 style='color:#f59e0b;'>{row.iloc[0]}</h3>
                    <p>📍 الموقع: {row.get('Location', row.get('Area', '---'))}</p>
                    <p>🏗️ المطور: {row.get('Developer', '---')}</p>
                </div>""", unsafe_allow_html=True)

elif menu == "أدوات":
    st.title("🛠️ أدوات سريعة")
    val = st.number_input("قيمة العقار", value=1000000)
    st.write(f"العمولة المقدرة (2.5%): {val * 0.025:,.0f} ج.م")

if st.button("🚪 تسجيل خروج"):
    st.session_state.auth = False; st.rerun()
