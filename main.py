import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- روابط الصور والخلفيات ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# الرابط الذي أرسلته (يجب أن يكون Published as CSV)
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 3. دالة التحقق (تم تقويتها لتجنب الأخطاء) ---
def check_auth(u, p):
    try:
        # قراءة البيانات مع إلغاء الكاش لضمان التحديث
        df_users = pd.read_csv(USER_SHEET_URL)
        
        # تنظيف أسماء الأعمدة من المسافات المخفية
        df_users.columns = [str(c).strip() for c in df_users.columns]
        
        u_val = str(u).strip()
        p_val = str(p).strip()
        
        # التأكد من وجود الأعمدة المطلوبة
        if 'Name' not in df_users.columns or 'Password' not in df_users.columns:
            st.error(f"❌ خطأ في الشيت: لم أجد أعمدة باسم 'Name' و 'Password'. الموجود: {list(df_users.columns)}")
            return False
            
        # البحث عن مطابقة
        match = df_users[(df_users['Name'].astype(str).str.strip() == u_val) & 
                         (df_users['Password'].astype(str).str.strip() == p_val)]
        return not match.empty
    except Exception as e:
        st.error(f"⚠️ فشل الاتصال بالشيت: تأكد من 'النشر على الويب' بصيغة CSV")
        return False

# --- 4. الترجمة وتنسيق الصفحة ---
trans = {
    "EN": {"login_h": "PLATFORM ACCESS", "u": "Name", "p": "Password", "btn": "Sign In", "err": "Wrong Name or Pass"},
    "AR": {"login_h": "بوابة دخول المحترفين", "u": "الاسم", "p": "كلمة المرور", "btn": "تسجيل الدخول", "err": "الاسم أو كلمة المرور خطأ"}
}
L = trans[st.session_state.lang]
direction = "rtl" if st.session_state.lang == "AR" else "ltr"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)), url('{BG_IMG}');
        background-size: cover; font-family: 'Cairo', sans-serif;
        direction: {direction} !important;
    }}
    .login-card {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        padding: 40px; border-radius: 30px; border: 1px solid rgba(245, 158, 11, 0.3);
        max-width: 400px; margin: 100px auto; text-align: center;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. منطق العرض ---
if not st.session_state.auth:
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#f59e0b;'>MA3LOMATI</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#aaa;'>{L['login_h']}</p>", unsafe_allow_html=True)
    
    u = st.text_input(L["u"])
    p = st.text_input(L["p"], type="password")
    
    if st.button(L["btn"], use_container_width=True, type="primary"):
        if check_auth(u, p):
            st.session_state.auth = True
            st.rerun()
        else:
            st.warning(L["err"])
            
    if st.button("🌐 EN/AR", use_container_width=True):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # ضع هنا كود "داخل المنصة" بالكامل (الذي أرسلته لي في الرسالة السابقة)
    st.success("تم تسجيل الدخول بنجاح! جاري تحميل المنصة...")
    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()
