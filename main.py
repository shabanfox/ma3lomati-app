import streamlit as st
import pandas as pd
import requests
import time

# --- 1. تعريف الـ Session State (يجب أن يكون في بداية الملف) ---
if 'auth' not in st.session_state: 
    st.session_state.auth = False
if 'current_user' not in st.session_state: 
    st.session_state.current_user = None

# --- روابط الربط (تأكد من صحتها) ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 2. وظائف الربط مع الشيت ---
def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        return response.text == "Success"
    except: return False

def login_user(u_input, pwd_input):
    try:
        # إضافة nocache لضمان جلب أحدث البيانات من الشيت
        response = requests.get(f"{USER_SHEET_URL}?nocache={time.time()}")
        if response.status_code == 200:
            import io
            df = pd.read_csv(io.StringIO(response.text))
            df.columns = df.columns.str.strip()
            user_row = df[((df['Name'].astype(str).str.lower() == str(u_input).lower().strip()) | 
                           (df['Email'].astype(str).str.lower() == str(u_input).lower().strip())) & 
                          (df['Password'].astype(str) == str(pwd_input).strip())]
            if not user_row.empty:
                return user_row.iloc[0]['Name']
        return None
    except: return None

# --- 3. التنسيق (CSS) لصفحة الدخول الفخمة ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 50px; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 28px; font-weight: 900;
        text-align: center; z-index: 10; margin-bottom: -35px; min-width: 380px;
        box-shadow: 0 10px 30px rgba(245,158,11,0.3);
    }}
    .auth-card {{ 
        background-color: #ffffff; width: 400px; padding: 60px 35px 35px 35px; 
        border-radius: 40px; text-align: center; box-shadow: 0 25px 60px rgba(0,0,0,0.5); 
    }}
    .auth-card input {{
        background-color: #f8f9fa !important; color: #000 !important;
        border: 1px solid #ddd !important; border-radius: 15px !important;
        text-align: center !important; height: 45px !important; font-weight: bold;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. عرض صفحة الدخول والاشتراك ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>MA3LOMATI PRO</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:#333; margin-bottom:20px;'>مرحباً بك</h2>", unsafe_allow_html=True)
    
    tab_log, tab_reg = st.tabs(["🔐 تسجيل دخول", "📝 حساب جديد"])
    
    with tab_log:
        u = st.text_input("الأسم أو الإيميل", key="log_u", label_visibility="collapsed", placeholder="اسم المستخدم")
        p = st.text_input("كلمة السر", type="password", key="log_p", label_visibility="collapsed", placeholder="كلمة المرور")
        if st.button("دخول للمنصة 🚀", use_container_width=True):
            if p == "2026": # الدخول السريع
                st.session_state.auth, st.session_state.current_user = True, "Admin"
                st.rerun()
            else:
                user = login_user(u, p)
                if user:
                    st.session_state.auth, st.session_state.current_user = True, user
                    st.rerun()
                else: st.error("بيانات الدخول غير صحيحة")
    
    with tab_reg:
        # الربط الكامل بالشيت
        reg_n = st.text_input("الاسم بالكامل", key="reg_name")
        reg_e = st.text_input("البريد الإلكتروني", key="reg_email")
        reg_p = st.text_input("كلمة السر المرجوة", type="password", key="reg_pass")
        reg_w = st.text_input("رقم الواتساب", key="reg_wa")
        reg_c = st.text_input("الشركة", key="reg_comp")
        
        if st.button("تأكيد الاشتراك ✅", use_container_width=True):
            if reg_n and reg_e and reg_p:
                if signup_user(reg_n, reg_p, reg_e, reg_w, reg_c):
                    st.success("تم تسجيل بياناتك بنجاح في الشيت!")
                    st.info("يمكنك الآن الدخول من تبويب 'تسجيل دخول'")
                else: st.error("فشل الاتصال بـ Google Script")
            else: st.warning("يرجى ملء الاسم والإيميل وكلمة السر")
            
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 5. بداية كود المنصة الداخلي (لا يتم تعديله) ---
st.write(f"مرحباً بك يا {st.session_state.current_user}")
# ... بقية كود المنصة الخاص بك ...
