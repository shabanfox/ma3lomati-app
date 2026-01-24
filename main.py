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

# --- 4. CSS Design (Oval Design) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
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
    .status-msg {{ font-size: 13px; font-weight: bold; color: #ff4b4b; margin-top: -15px; margin-bottom: 10px; text-align: right; display: block; }}
    div.stButton > button {{ border-radius: 12px !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. LOGIN & REGISTER PAGE ---
if not st.session_state.auth:
    users_df = get_users_live()

    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>منصة معلوماتي العقارية</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    
    # --- واجهة استعادة كلمة السر ---
    if st.session_state.show_forgot:
        st.markdown("<h3 style='color:#333;'>🔑 استعادة الحساب</h3>", unsafe_allow_html=True)
        f_email = st.text_input("أدخل البريد الإلكتروني المسجل", key="forgot_email")
        if st.button("إظهار كلمة السر", use_container_width=True):
            if not users_df.empty and f_email in users_df['Email'].astype(str).values:
                u_pass = users_df[users_df['Email'].astype(str) == f_email]['Password'].values[0]
                st.info(f"كلمة السر الخاصة بك هي: **{u_pass}**")
            else:
                st.error("هذا البريد غير مسجل لدينا")
        if st.button("العودة للخلف"):
            st.session_state.show_forgot = False
            st.rerun()
    
    # --- واجهة الدخول والاشتراك ---
    else:
        tab1, tab2 = st.tabs(["🔐 دخول", "📝 اشتراك"])
        
        with tab1:
            u = st.text_input("User", placeholder="الاسم أو الإيميل", label_visibility="collapsed", key="log_u")
            p = st.text_input("Pass", type="password", placeholder="كلمة المرور", label_visibility="collapsed", key="log_p")
            
            if st.button("دخول للمنصة 🚀", use_container_width=True):
                if p == "2026": # كود المطور
                    st.session_state.auth = True; st.rerun()
                elif not users_df.empty and not users_df[((users_df['Name']==u)|(users_df['Email']==u))&(users_df['Password'].astype(str)==p)].empty:
                    st.session_state.auth = True; st.rerun()
                else:
                    st.error("بيانات الدخول غير صحيحة")
            
            # تم حذف الـ variant لتجنب الـ TypeError
            if st.button("نسيت كلمة السر؟"):
                st.session_state.show_forgot = True
                st.rerun()
        
        with tab2:
            # فحص الاسم
            r_n = st.text_input("الاسم بالكامل", key="reg_n", placeholder="Name")
            if r_n and not users_df.empty and r_n in users_df['Name'].astype(str).values:
                st.markdown("<span class='status-msg'>⚠️ الاسم موجود مسبقاً</span>", unsafe_allow_html=True)
            
            # فحص الإيميل
            r_e = st.text_input("البريد الإلكتروني", key="reg_e", placeholder="Email")
            if r_e and not users_df.empty and r_e in users_df['Email'].astype(str).values:
                st.markdown("<span class='status-msg'>⚠️ الإيميل مسجل مسبقاً</span>", unsafe_allow_html=True)
            
            # فحص الواتساب
            r_w = st.text_input("رقم الواتساب", key="reg_w", placeholder="WhatsApp")
            if r_w and not users_df.empty and 'WhatsApp' in users_df.columns:
                if r_w in users_df['WhatsApp'].astype(str).values:
                    st.markdown("<span class='status-msg'>⚠️ الرقم مسجل مسبقاً</span>", unsafe_allow_html=True)
            
            r_p = st.text_input("كلمة السر", type="password", key="reg_p", placeholder="Password")
            r_c = st.text_input("اسم الشركة", key="reg_c", placeholder="Company")
            
            if st.button("إنشاء حساب جديد ✅", use_container_width=True):
                # فحص نهائي للتكرار قبل الإرسال
                is_duplicate = False
                if not users_df.empty:
                    if r_n in users_df['Name'].astype(str).values or r_e in users_df['Email'].astype(str).values:
                        is_duplicate = True
                
                if is_duplicate:
                    st.error("لا يمكن التسجيل ببيانات موجودة مسبقاً")
                elif r_n and r_e and r_p:
                    if signup_user(r_n, r_p, r_e, r_w, r_c):
                        st.success("تم الاشتراك! يمكنك الدخول الآن.")
                        st.balloons()
                    else: st.error("فشل الاتصال بالشيت")
                else:
                    st.warning("يرجى إكمال البيانات")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 6. باقي كود المنصة (يتم وضعه هنا) ---
st.title("مرحباً بك في المنصة")
if st.button("خروج"):
    st.session_state.auth = False
    st.rerun()
