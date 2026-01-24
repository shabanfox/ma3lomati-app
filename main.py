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
if 'page' not in st.session_state: st.session_state.page = "login"
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'view' not in st.session_state: st.session_state.view = "grid" 
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'last_menu' not in st.session_state: st.session_state.last_menu = "Launches"
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 3. Functions ---

def get_users_df():
    """جلب وتنظيف بيانات المستخدمين من الشيت"""
    try:
        response = requests.get(f"{USER_SHEET_URL}?v={time.time()}")
        df = pd.read_csv(io.StringIO(response.text))
        # تنظيف أسماء الأعمدة والبيانات من المسافات
        df.columns = [c.strip() for c in df.columns]
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    except:
        return pd.DataFrame()

def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        return "Success" in response.text
    except: return False

@st.cache_data(ttl=60)
def load_data():
    # روابط بيانات العقارات
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
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {direction} !important; font-family: 'Cairo', sans-serif;
    }}
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: flex-start; width: 100%; padding-top: 20px; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 24px; font-weight: 900;
        text-align: center; z-index: 10; margin-bottom: -30px; min-width: 360px;
    }}
    .auth-card {{ background-color: #ffffff; width: 380px; padding: 55px 35px 30px 35px; border-radius: 30px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); }}
    .auth-card div.stTextInput input {{ background-color: #000 !important; color: #fff !important; border: 1px solid #f59e0b !important; border-radius: 12px !important; text-align: center !important; }}
    .duplicate-msg {{ color: #721c24; background-color: #f8d7da; padding: 10px; border-radius: 10px; margin-bottom: 15px; font-size: 14px; text-align: right; }}
    
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 2px solid #f59e0b;
        padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 30px;
    }}
    .detail-card {{ background: rgba(20, 20, 20, 0.9); padding: 25px; border-radius: 20px; border-top: 5px solid #f59e0b; color: white; margin-bottom:20px; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; }}
    div.stButton > button {{ border-radius: 12px !important; font-weight: 700 !important; width: 100%; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. AUTH / LOGIN / REGISTER PAGE ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>منصة معلوماتي العقارية</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)

    if st.session_state.page == "forgot":
        st.subheader("🔑 استعادة الحساب")
        f_email = st.text_input("البريد الإلكتروني", key="forget_mail")
        if st.button("عرض كلمة السر"):
            df = get_users_df()
            if not df.empty and f_email.strip() in df['Email'].astype(str).values:
                pwd = df[df['Email'].astype(str) == f_email.strip()]['Password'].values[0]
                st.success(f"كلمة السر: {pwd}")
            else: st.error("الإيميل غير مسجل")
        if st.button("رجوع"):
            st.session_state.page = "login"; st.rerun()
    
    else:
        # هنا تم تعريف tab1 و tab2 بشكل صحيح داخل السياق
        tab1, tab2 = st.tabs(["🔐 دخول", "📝 اشتراك"])
        
        with tab1:
            u_input = st.text_input("المستخدم", placeholder="الاسم أو الإيميل", label_visibility="collapsed", key="l_u")
            p_input = st.text_input("كلمة المرور", type="password", placeholder="الباسورد", label_visibility="collapsed", key="l_p")
            if st.button("دخول للمنصة"):
                if p_input == "2026": 
                    st.session_state.auth = True; st.rerun()
                
                df_u = get_users_df()
                if not df_u.empty:
                    u_clean = u_input.strip()
                    p_clean = p_input.strip()
                    match = df_u[((df_u['Name']==u_clean)|(df_u['Email']==u_clean)) & (df_u['Password'].astype(str)==p_clean)]
                    if not match.empty:
                        st.session_state.auth = True; st.rerun()
                    else: st.error("بيانات الدخول خطأ")
                else: st.error("مشكلة في قاعدة البيانات")
            
            if st.button("نسيت كلمة السر؟"):
                st.session_state.page = "forgot"; st.rerun()

        with tab2:
            r_n = st.text_input("الاسم", key="rn")
            r_e = st.text_input("الإيميل", key="re")
            r_w = st.text_input("الواتساب", key="rw")
            r_p = st.text_input("الباسورد", type="password", key="rp")
            r_c = st.text_input("الشركة", key="rc")
            
            if st.button("تأكيد الاشتراك"):
                if r_n and r_e and r_p:
                    df_check = get_users_df()
                    # فحص دقيق للتكرار
                    name_ex = r_n.strip() in df_check['Name'].values if not df_check.empty else False
                    email_ex = r_e.strip() in df_check['Email'].values if not df_check.empty else False
                    
                    if name_ex or email_ex:
                        st.markdown("<div class='duplicate-msg'>⚠️ البيانات مسجلة مسبقاً! يرجى استخدام 'نسيت الباسورد' لاستعادة حسابك.</div>", unsafe_allow_html=True)
                    else:
                        if signup_user(r_n, r_p, r_e, r_w, r_c):
                            st.success("تم الاشتراك بنجاح!")
                            st.balloons()
                        else: st.error("فشل الإرسال")
                else: st.warning("أكمل البيانات")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 6. MAIN APP ---
df_p, df_d, df_l = load_data()
L = {"menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"]}
st.markdown('<div class="royal-header"><h1 style="color:#f59e0b;">MA3LOMATI</h1></div>', unsafe_allow_html=True)

m_col, o_col = st.columns([0.85, 0.15])
with m_col:
    menu = option_menu(None, L["menu"], default_index=4, orientation="horizontal", 
                       styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
with o_col:
    if st.button("🚪 Logout"): st.session_state.auth = False; st.rerun()

# بقية الكود لعرض الجريد والأدوات...
st.write(f"أهلاً بك في قسم {menu}")
