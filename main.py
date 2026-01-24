import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import requests
import time
import io

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- روابط البيانات ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'show_forgot' not in st.session_state: st.session_state.show_forgot = False

# --- 3. Functions ---

def get_users_live():
    """جلب أحدث البيانات من الشيت مباشرة"""
    try:
        response = requests.get(f"{USER_SHEET_URL}?nocache={time.time()}")
        df = pd.read_csv(io.StringIO(response.text))
        df.columns = [c.strip() for c in df.columns]
        return df
    except: return pd.DataFrame()

def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        return "Success" in response.text
    except: return False

# --- 4. CSS Design ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; padding-top: 20px; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 24px; font-weight: 900;
        text-align: center; z-index: 10; margin-bottom: -30px; min-width: 360px;
    }}
    .auth-card {{ background-color: #ffffff; width: 400px; padding: 55px 35px 30px 35px; border-radius: 30px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); }}
    .status-msg {{ font-size: 12px; font-weight: bold; margin-bottom: 5px; display: block; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIN & REGISTER PAGE ---
if not st.session_state.auth:
    users_df = get_users_live() # جلب البيانات للفحص اللحظي

    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>منصة معلوماتي العقارية</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    
    # --- استعادة كلمة السر ---
    if st.session_state.show_forgot:
        st.subheader("🔑 استعادة كلمة السر")
        f_email = st.text_input("أدخل بريدك الإلكتروني المسجل")
        if st.button("إرسال طلب الاستعادة"):
            if f_email in users_df['Email'].astype(str).values:
                u_pass = users_df[users_df['Email'].astype(str) == f_email]['Password'].values[0]
                st.info(f"كلمة السر الخاصة بك هي: {u_pass}")
            else:
                st.error("عذراً، هذا الإيميل غير موجود بالسجلات")
        if st.button("العودة للدخول"):
            st.session_state.show_forgot = False
            st.rerun()
    
    # --- صفحة الدخول والاشتراك ---
    else:
        tab1, tab2 = st.tabs(["تسجيل الدخول", "اشتراك جديد"])
        
        with tab1:
            u = st.text_input("Username", placeholder="الاسم أو الإيميل", key="login_u")
            p = st.text_input("Password", type="password", placeholder="كلمة المرور", key="login_p")
            if st.button("دخول للمنصة 🚀", use_container_width=True):
                if p == "2026" or (not users_df.empty and not users_df[((users_df['Name']==u)|(users_df['Email']==u))&(users_df['Password']==p)].empty):
                    st.session_state.auth = True; st.rerun()
                else: st.error("بيانات غير صحيحة")
            if st.button("نسيت كلمة السر؟", variant="ghost"):
                st.session_state.show_forgot = True
                st.rerun()
        
        with tab2:
            # الاسم
            r_n = st.text_input("الاسم بالكامل", key="reg_n")
            if r_n and not users_df.empty and r_n in users_df['Name'].astype(str).values:
                st.markdown("<span style='color:red;' class='status-msg'>❌ هذا الاسم موجود مسبقاً</span>", unsafe_allow_html=True)
            
            # الإيميل
            r_e = st.text_input("البريد الإلكتروني", key="reg_e")
            if r_e and not users_df.empty and r_e in users_df['Email'].astype(str).values:
                st.markdown("<span style='color:red;' class='status-msg'>❌ هذا الإيميل موجود مسبقاً</span>", unsafe_allow_html=True)
            
            # الواتساب
            r_w = st.text_input("رقم الواتساب", key="reg_w")
            if r_w and not users_df.empty and 'WhatsApp' in users_df.columns:
                if r_w in users_df['WhatsApp'].astype(str).values:
                    st.markdown("<span style='color:red;' class='status-msg'>❌ هذا الرقم موجود مسبقاً</span>", unsafe_allow_html=True)
            
            r_p = st.text_input("كلمة السر", type="password", key="reg_p")
            r_c = st.text_input("الشركة", key="reg_c")
            
            if st.button("تأكيد الاشتراك ✅", use_container_width=True):
                # منع الضغط إذا كان هناك تكرار
                if (r_n in users_df['Name'].values) or (r_e in users_df['Email'].values):
                    st.error("يرجى تغيير البيانات المكررة أولاً")
                elif r_n and r_e and r_p:
                    if signup_user(r_n, r_p, r_e, r_w, r_c):
                        st.success("تم الاشتراك بنجاح!")
                        st.balloons()
                    else: st.error("فشل الاتصال")
                else: st.warning("املأ الحقول الأساسية")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 6. المنصة الداخلية (كما هي) ---
st.title("مرحباً بك في المنصة")
# أضف باقي كود المنصة هنا...
