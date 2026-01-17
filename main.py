import streamlit as st
import pandas as pd
import feedparser
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu
import gspread
from google.oauth2.service_account import Credentials

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. وظيفة الاتصال بجوجل شيت (قاعدة بيانات المستخدمين)
def get_user_sheet():
    try:
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        # سيتم جلب البيانات من st.secrets التي سأشرحها لك لاحقاً
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        # اسم الملف في جوجل شيت يجب أن يكون Users_DB
        return client.open("Users_DB").sheet1
    except Exception as e:
        return None

# 3. إدارة حالة الجلسة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# 4. التنسيق الجمالي (CSS) - كودك الأصلي
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
    div.stButton > button[key*="card_"] {{
        background-color: white !important; color: #111 !important;
        min-height: 140px !important; text-align: right !important;
        font-weight: bold !important; font-size: 15px !important;
        border: none !important; margin-bottom: 10px !important;
        display: block !important; width: 100% !important;
    }}
    .smart-box {{ background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; }}
    .tool-card {{ background: #1a1a1a; padding: 20px; border-radius: 15px; border-top: 4px solid #f59e0b; text-align: center; height: 100%; }}
    .stSelectbox label, .stTextInput label, .stNumberInput label {{ color: #f59e0b !important; font-weight: bold !important; }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول والاشتراك المحدثة
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:50px;'><h1 style='color:#f59e0b; font-size:60px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    
    _, c2, _ = st.columns([1,2,1])
    with c2:
        mode = st.radio("القائمة الرئيسية", ["تسجيل دخول", "إنشاء حساب بروكر جديد"], horizontal=True)
        sheet = get_user_sheet()
        
        if mode == "تسجيل دخول":
            login_user = st.text_input("الأسم بالكامل أو الجيميل")
            login_pwd = st.text_input("كلمة السر", type="password")
            if st.button("دخول للنظام 🚀", use_container_width=True):
                if sheet:
                    users_df = pd.DataFrame(sheet.get_all_records())
                    # التحقق من الاسم أو الإيميل مع الباسورد
                    check = users_df[((users_df['Full Name'] == login_user) | (users_df['Email'] == login_user)) & (users_df['Password'] == str(login_pwd))]
                    if not check.empty:
                        st.session_state.auth = True
                        st.session_state.current_user = check.iloc[0]['Full Name']
                        st.rerun()
                    else: st.error("بيانات الدخول غير صحيحة")
                else: st.error("مشكلة في الاتصال بقاعدة البيانات")

        else:
            st.markdown("### 📝 استمارة انضمام بروكر")
            reg_name = st.text_input("الأسم بالكامل")
            reg_pwd = st.text_input("كلمة السر المرجوة")
            reg_email = st.text_input("البريد الإلكتروني (Gmail)")
            reg_wa = st.text_input("رقم الواتساب (بالكود الدولي)")
            reg_comp = st.text_input("الشركة العقارية")
            
            if st.button("إتمام التسجيل ✅", use_container_width=True):
                if reg_name and reg_pwd and reg_email and reg_wa:
                    if sheet:
                        users_df = pd.DataFrame(sheet.get_all_records())
                        if reg_email in users_df['Email'].values:
                            st.warning("هذا الإيميل مسجل مسبقاً!")
                        else:
                            sheet.append_row([reg_name, reg_pwd, reg_email, reg_wa, reg_comp, datetime.now().strftime("%Y-%m-%d")])
                            st.success("تم تسجيلك بنجاح! انتقل الآن لخانة تسجيل الدخول.")
                    else: st.error("عفواً، قاعدة البيانات غير متصلة")
                else: st.warning("برجاء ملء كافة البيانات")
    st.stop()

# 6. جلب بيانات العقارات (كودك الأصلي)
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        p.rename(columns={'Area': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 7. الهيدر والباقي (نفس كودك تماماً)
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 200px; background-size: cover; background-position: center; border-radius: 0 0 30px 30px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b;">
        <h1 style="color: white; margin: 0; font-size: 45px; text-shadow: 2px 2px 10px rgba(0,0,0,0.5);">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-size: 18px;">أهلاً بك يا {st.session_state.current_user}</p>
    </div>
""", unsafe_allow_html=True)

# 8. المنيو الرئيسي
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], default_index=0, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# --- هنا تضع باقي كود الأقسام (المساعد، المشاريع، المطورين، الأدوات) كما هي في كودك الأصلي ---
if menu == "المساعد الذكي":
    st.info("قسم المساعد الذكي جاهز للعمل")
# (أكمل باقي الأقسام كما في الكود السابق لديك...)
