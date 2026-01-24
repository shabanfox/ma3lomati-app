import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import requests
import time
import io

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CONSTANTS ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
# رابط السكريبت المسؤول عن الكتابة في الشيت
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
# رابط الشيت للقراءة
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
ITEMS_PER_PAGE = 6

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'page' not in st.session_state: st.session_state.page = "login"
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'view' not in st.session_state: st.session_state.view = "grid" 
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'last_menu' not in st.session_state: st.session_state.last_menu = "Launches"
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 3. Functions ---

def get_users_df():
    """جلب بيانات المستخدمين من الشيت بشكل لحظي"""
    try:
        response = requests.get(f"{USER_SHEET_URL}?v={time.time()}")
        df = pd.read_csv(io.StringIO(response.text))
        df.columns = [c.strip() for c in df.columns]
        return df
    except: return pd.DataFrame()

def signup_user(name, pwd, email, wa, comp):
    """إرسال بيانات الاشتراك الجديد للسكريبت"""
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        return "Success" in response.text
    except: return False

@st.cache_data(ttl=60)
def load_data():
    # روابط بيانات المشاريع (تأكد من صحتها)
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]: df.columns = [c.strip() for c in df.columns]
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 4. CSS Luxury Design ---
direction = "rtl" if st.session_state.lang == "AR" else "ltr"
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {direction} !important; font-family: 'Cairo', sans-serif;
    }}
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; padding-top: 20px; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 24px; font-weight: 900;
        text-align: center; z-index: 10; margin-bottom: -30px; min-width: 360px;
    }}
    .auth-card {{ background-color: #ffffff; width: 380px; padding: 55px 35px 30px 35px; border-radius: 30px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); }}
    .auth-card div.stTextInput input {{ background-color: #000 !important; color: #fff !important; border: 1px solid #f59e0b !important; border-radius: 12px !important; text-align: center !important; }}
    .duplicate-msg {{ color: #721c24; background-color: #f8d7da; padding: 10px; border-radius: 10px; margin-bottom: 15px; font-size: 14px; text-align: center; border: 1px solid #f5c6cb; }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; border-bottom: 2px solid #f59e0b;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. AUTH PAGE ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>منصة معلوماتي العقارية</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)

    if st.session_state.page == "forgot":
        st.subheader("🔑 استعادة الحساب")
        f_email = st.text_input("البريد الإلكتروني المسجل")
        if st.button("استرجاع الباسورد", use_container_width=True):
            df = get_users_df()
            if not df.empty and f_email.strip() in df['Email'].astype(str).values:
                pwd = df[df['Email'].astype(str) == f_email.strip()]['Password'].values[0]
                st.success(f"كلمة السر هي: {pwd}")
            else: st.error("الإيميل غير مسجل لدينا")
        if st.button("العودة للدخول"):
            st.session_state.page = "login"; st.rerun()
    
    else:
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            u_log = st.text_input("User", placeholder="اسم المستخدم أو الإيميل", label_visibility="collapsed", key="l_u")
            p_log = st.text_input("Pass", type="password", placeholder="كلمة المرور", label_visibility="collapsed", key="l_p")
            if st.button("SIGN IN", use_container_width=True):
                if p_log == "2026": # كود المطور
                    st.session_state.auth = True; st.rerun()
                df_u = get_users_df()
                if not df_u.empty:
                    u_c, p_c = u_log.strip(), p_log.strip()
                    user = df_u[((df_u['Name']==u_c)|(df_u['Email']==u_c)) & (df_u['Password'].astype(str)==p_c)]
                    if not user.empty:
                        st.session_state.auth = True; st.rerun()
                    else: st.error("بيانات الدخول غير صحيحة")
            if st.button("نسيت كلمة السر؟"):
                st.session_state.page = "forgot"; st.rerun()

        with tab2:
            r_n = st.text_input("الاسم بالكامل", key="reg_n")
            r_e = st.text_input("البريد الإلكتروني", key="reg_e")
            r_w = st.text_input("رقم الواتساب", key="reg_w")
            r_p = st.text_input("كلمة السر", type="password", key="reg_p")
            r_c = st.text_input("الشركة", key="reg_c")
            
            if st.button("تأكيد الاشتراك الجديد", use_container_width=True):
                if r_n and r_e and r_p:
                    with st.spinner("جاري التحقق..."):
                        df_check = get_users_df()
                        # فحص التكرار (الاسم أو الإيميل أو الواتساب)
                        name_ex = r_n.strip() in df_check['Name'].astype(str).values if not df_check.empty else False
                        mail_ex = r_e.strip() in df_check['Email'].astype(str).values if not df_check.empty else False
                        wa_ex = r_w.strip() in df_check['WhatsApp'].astype(str).values if (not df_check.empty and 'WhatsApp' in df_check.columns) else False
                        
                        if name_ex or mail_ex or wa_ex:
                            st.markdown("<div class='duplicate-msg'>⚠️ هذه البيانات مسجلة مسبقاً!<br>استخدم خاصية استعادة الباسورد.</div>", unsafe_allow_html=True)
                        else:
                            if signup_user(r_n, r_p, r_e, r_w, r_c):
                                st.success("✅ تم الاشتراك بنجاح! يمكنك الدخول الآن.")
                                st.balloons()
                            else: st.error("حدث خطأ في الاتصال بالسيرفر")
                else: st.warning("يرجى إكمال البيانات الأساسية")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 6. MAIN APP ---
df_p, df_d, df_l = load_data()
L = {"menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"]}

st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900;">MA3LOMATI</h1></div>', unsafe_allow_html=True)

m_col, o_col = st.columns([0.85, 0.15])
with m_col:
    menu = option_menu(None, L["menu"], default_index=4, orientation="horizontal", 
                       styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
with o_col:
    if st.button("🚪 Logout", use_container_width=True): st.session_state.auth = False; st.rerun()

st.write(f"محتوى قسم: {menu}")
# (ضع هنا بقية منطق عرض الجريد والأدوات كما في كودك الأصلي)
