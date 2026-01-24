import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import requests
import time
import io

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CONSTANTS & URLS ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"

HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'view' not in st.session_state: st.session_state.view = "grid" 
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'last_menu' not in st.session_state: st.session_state.last_menu = "Launches"
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 3. Functions (Auth, Signup & Validation) ---

def get_all_users():
    """جلب قائمة المستخدمين الحالية من الشيت"""
    try:
        response = requests.get(f"{USER_SHEET_URL}?nocache={time.time()}")
        df = pd.read_csv(io.StringIO(response.text))
        df.columns = [c.strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

def check_auth(u, p):
    df = get_all_users()
    if df.empty: return False
    user_row = df[((df['Name'].astype(str) == str(u)) | (df['Email'].astype(str) == str(u))) & 
                  (df['Password'].astype(str) == str(p))]
    return not user_row.empty

def signup_user(name, pwd, email, wa, comp):
    # 1. التحقق من عدم التكرار قبل الإرسال
    df = get_all_users()
    if not df.empty:
        # فحص الاسم
        if str(name) in df['Name'].astype(str).values:
            return "Error: Name exists"
        # فحص الإيميل
        if str(email) in df['Email'].astype(str).values:
            return "Error: Email exists"
        # فحص الواتساب (بشرط وجود عمود WhatsApp في الشيت)
        if 'WhatsApp' in df.columns:
            if str(wa) in df['WhatsApp'].astype(str).values:
                return "Error: WhatsApp exists"

    # 2. إذا لم يوجد تكرار، يتم الإرسال
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        return "Success" if "Success" in response.text else "Failed"
    except: return "Connection Error"

@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]: df.columns = [c.strip() for c in df.columns]
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 4. CSS Design (نفس التصميم الفخم) ---
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
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: flex-start; width: 100%; padding-top: 20px; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 24px; font-weight: 900;
        text-align: center; z-index: 10; margin-bottom: -30px; min-width: 360px;
    }}
    .auth-card {{ background-color: #ffffff; width: 380px; padding: 55px 35px 30px 35px; border-radius: 30px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); }}
    .lock-gold {{ font-size: 45px; color: #f59e0b; margin-bottom: 5px; }}
    .auth-card div.stTextInput input {{ background-color: #f1f1f1 !important; color: #000 !important; border: 1px solid #ddd !important; border-radius: 12px !important; text-align: center !important; height: 45px !important; }}
    
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 2px solid #f59e0b;
        padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 30px;
    }}
    .detail-card, .tool-card {{ background: rgba(20, 20, 20, 0.9); padding: 25px; border-radius: 20px; border-top: 5px solid #f59e0b; color: white; border: 1px solid #333; margin-bottom:20px; }}
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; color: #FFFFFF !important;
        border-left: 5px solid #f59e0b !important; height: 180px !important; width: 100% !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIN & REGISTER PAGE ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>منصة معلوماتي العقارية</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.markdown("<div class='lock-gold'>🔒</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["تسجيل الدخول", "اشتراك جديد"])
    
    with tab1:
        u = st.text_input("Username", placeholder="الاسم أو الإيميل", label_visibility="collapsed", key="login_u")
        p = st.text_input("Password", type="password", placeholder="كلمة المرور", label_visibility="collapsed", key="login_p")
        if st.button("SIGN IN", use_container_width=True):
            if p == "2026": # كود المطور
                st.session_state.auth = True; st.rerun()
            elif check_auth(u, p): 
                st.session_state.auth = True; st.rerun()
            else: 
                st.error("بيانات الدخول غير صحيحة")
    
    with tab2:
        reg_n = st.text_input("Full Name", placeholder="الاسم بالكامل", key="r_n")
        reg_e = st.text_input("Email", placeholder="البريد الإلكتروني", key="r_e")
        reg_p = st.text_input("Password", type="password", placeholder="كلمة السر", key="r_p")
        reg_wa = st.text_input("WhatsApp", placeholder="رقم الواتساب", key="r_w")
        reg_c = st.text_input("Company", placeholder="اسم الشركة", key="r_c")
        
        if st.button("CREATE ACCOUNT", use_container_width=True):
            if reg_n and reg_e and reg_p and reg_wa:
                with st.spinner("جاري التحقق والتسجيل..."):
                    result = signup_user(reg_n, reg_p, reg_e, reg_wa, reg_c)
                    
                    if result == "Success":
                        st.success("✅ تم الاشتراك بنجاح! يمكنك الآن الدخول.")
                        st.balloons()
                    elif "Name exists" in result:
                        st.error("⚠️ هذا الاسم مسجل مسبقاً، اختر اسماً آخر.")
                    elif "Email exists" in result:
                        st.error("⚠️ هذا البريد الإلكتروني مسجل مسبقاً.")
                    elif "WhatsApp exists" in result:
                        st.error("⚠️ رقم الواتساب هذا مسجل مسبقاً.")
                    else:
                        st.error(f"❌ خطأ: {result}")
            else:
                st.warning("يرجى ملء كافة الحقول الأساسية")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 6. MAIN APP ---
df_p, df_d, df_l = load_data()
st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900;">MA3LOMATI</h1></div>', unsafe_allow_html=True)

# استكمال باقي محرك المنصة (الأدوات، المطورين، الخ) كما هو في الكود السابق...
L = {"menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"]}
m_col, o_col = st.columns([0.85, 0.15])
with m_col:
    menu = option_menu(None, L["menu"], default_index=4, orientation="horizontal", 
                       styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
with o_col:
    if st.button("🚪 Logout", use_container_width=True): st.session_state.auth = False; st.rerun()

# (بقية الكود الخاص بعرض الجريد والتفاصيل يوضع هنا كما هو)
st.write(f"أهلاً بك في قسم: {menu}")
