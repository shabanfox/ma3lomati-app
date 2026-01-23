import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- الثوابت والروابط ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# تم تعديل الرابط لضمان القراءة الصحيحة بصيغة CSV
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1849129596&output=csv"

# --- 2. إدارة الجلسة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"

# --- 3. دالة التحقق المحدثة (لحل خطأ 400) ---
def check_auth(username, password):
    try:
        # استخدام الرابط المباشر مع تحديد نوع الملف
        df_users = pd.read_csv(USER_SHEET_URL)
        
        # تنظيف أسماء الأعمدة من أي مسافات مخفية
        df_users.columns = [c.strip() for c in df_users.columns]
        
        # تحويل المدخلات والبيانات لنصوص ومقارنتها بعد حذف المسافات
        u_input = str(username).strip()
        p_input = str(password).strip()
        
        # البحث عن مطابقة
        match = df_users[
            (df_users['Username'].astype(str).str.strip() == u_input) & 
            (df_users['Password'].astype(str).str.strip() == p_input)
        ]
        return not match.empty
    except Exception as e:
        # إظهار رسالة خطأ مفهومة للمسؤول
        st.error(f"⚠️ اتصال قاعدة البيانات: تأكد من نشر الشيت (Publish to Web) بصيغة CSV")
        return False

# --- 4. القاموس واللغات ---
trans = {
    "EN": {
        "login_h": "PLATFORM ACCESS", "user": "Username", "pass": "Password", "login_btn": "Sign In",
        "logout": "Logout", "lang_toggle": "العربية", "error": "Invalid Username or Password"
    },
    "AR": {
        "login_h": "بوابة دخول المحترفين", "user": "اسم المستخدم", "pass": "كلمة المرور", "login_btn": "تسجيل الدخول",
        "logout": "خروج", "lang_toggle": "English", "error": "اسم المستخدم أو كلمة المرور غير صحيحة"
    }
}
L = trans[st.session_state.lang]

# --- 5. CSS (نفس التصميم الزجاجي الرائع) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.9)), url('{BG_IMG}');
        background-size: cover; font-family: 'Cairo', sans-serif;
    }}
    .login-container {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        padding: 50px; border-radius: 30px; border: 1px solid rgba(245, 158, 11, 0.3);
        max-width: 400px; margin: 100px auto; text-align: center;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 6. عرض صفحة الدخول ---
if not st.session_state.auth:
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#f59e0b;'>MA3LOMATI</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#ccc;'>{L['login_h']}</p>", unsafe_allow_html=True)
    
    u = st.text_input(L["user"])
    p = st.text_input(L["pass"], type="password")
    
    if st.button(L["login_btn"], use_container_width=True, type="primary"):
        if check_auth(u, p):
            st.session_state.auth = True
            st.rerun()
        else:
            st.warning(L["error"])
            
    if st.button(L["lang_toggle"], use_container_width=True):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- بعد الدخول (بقية كود المنصة الخاص بك يوضع هنا) ---
st.success("تم تسجيل الدخول بنجاح!")
if st.button(L["logout"]):
    st.session_state.auth = False
    st.rerun()
