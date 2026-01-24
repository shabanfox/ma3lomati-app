import streamlit as st
import pandas as pd
import requests
import time
import io

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- الروابط ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 2. الحالة (Session State) ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'show_forgot' not in st.session_state: st.session_state.show_forgot = False

# --- 3. الدوال البرمجية ---

def get_users_live():
    """جلب أحدث نسخة من البيانات من الشيت"""
    try:
        # استخدام time.time لمنع الـ caching نهائياً
        response = requests.get(f"{USER_SHEET_URL}?v={time.time()}")
        df = pd.read_csv(io.StringIO(response.text))
        df.columns = [c.strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

def signup_user(name, pwd, email, wa, comp):
    """إرسال البيانات بعد التأكد التام من عدم التكرار"""
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        return "Success" in response.text
    except:
        return False

# --- 4. التنسيق الجمالي ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; padding-top: 20px; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 24px; font-weight: 900;
        text-align: center; margin-bottom: -30px; min-width: 360px;
    }}
    .auth-card {{ background-color: #ffffff; width: 380px; padding: 55px 35px 30px 35px; border-radius: 30px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); }}
    .error-tag {{ color: white; background: #ff4b4b; padding: 2px 10px; border-radius: 10px; font-size: 12px; margin-bottom: 10px; display: inline-block; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. واجهة الدخول والاشتراك ---
if not st.session_state.auth:
    # جلب البيانات الحالية للفحص
    current_users_df = get_users_live()

    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>منصة معلوماتي العقارية</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    
    if st.session_state.show_forgot:
        st.subheader("🔑 استعادة الحساب")
        f_email = st.text_input("أدخل البريد المسجل")
        if st.button("إظهار الباسورد", use_container_width=True):
            if not current_users_df.empty and f_email in current_users_df['Email'].astype(str).values:
                u_p = current_users_df[current_users_df['Email'].astype(str) == f_email]['Password'].values[0]
                st.info(f"كلمة السر هي: {u_p}")
            else: st.error("الإيميل غير مسجل")
        if st.button("رجوع"):
            st.session_state.show_forgot = False; st.rerun()
    
    else:
        tab1, tab2 = st.tabs(["🔐 دخول", "📝 اشتراك جديد"])
        
        with tab1:
            u_log = st.text_input("اسم المستخدم أو الإيميل", key="log_u")
            p_log = st.text_input("كلمة المرور", type="password", key="log_p")
            if st.button("دخول للمنصة 🚀", use_container_width=True):
                if p_log == "2026":
                    st.session_state.auth = True; st.rerun()
                elif not current_users_df.empty and not current_users_df[((current_users_df['Name']==u_log)|(current_users_df['Email']==u_log))&(current_users_df['Password'].astype(str)==p_log)].empty:
                    st.session_state.auth = True; st.rerun()
                else: st.error("بيانات غير صحيحة")
            if st.button("نسيت كلمة السر؟"):
                st.session_state.show_forgot = True; st.rerun()
        
        with tab2:
            r_name = st.text_input("الاسم بالكامل", key="r_n")
            # فحص الاسم فوراً
            name_exists = not current_users_df.empty and r_name in current_users_df['Name'].astype(str).values
            if name_exists: st.markdown("<div class='error-tag'>⚠️ هذا الاسم مسجل بالفعل</div>", unsafe_allow_html=True)
            
            r_email = st.text_input("البريد الإلكتروني", key="r_e")
            # فحص الإيميل فوراً
            email_exists = not current_users_df.empty and r_email in current_users_df['Email'].astype(str).values
            if email_exists: st.markdown("<div class='error-tag'>⚠️ الإيميل مسجل بالفعل</div>", unsafe_allow_html=True)
            
            r_wa = st.text_input("رقم الواتساب", key="r_w")
            # فحص الواتساب فوراً
            wa_exists = False
            if not current_users_df.empty and 'WhatsApp' in current_users_df.columns:
                wa_exists = r_wa in current_users_df['WhatsApp'].astype(str).values
            if wa_exists: st.markdown("<div class='error-tag'>⚠️ رقم الواتساب مسجل بالفعل</div>", unsafe_allow_html=True)
            
            r_pass = st.text_input("كلمة السر", type="password", key="r_p")
            r_comp = st.text_input("الشركة", key="r_c")
            
            if st.button("تأكيد التسجيل ✅", use_container_width=True):
                # القفل النهائي: إذا كان أي شيء مكرر، ارفض العملية تماماً
                if name_exists or email_exists or wa_exists:
                    st.error("❌ لا يمكن إتمام التسجيل: بعض البيانات مكررة في سجلاتنا!")
                elif not (r_name and r_email and r_pass):
                    st.warning("يرجى ملء الحقول الأساسية")
                else:
                    with st.spinner("جاري الحفظ..."):
                        if signup_user(r_name, r_pass, r_email, r_wa, r_comp):
                            st.success("تم الاشتراك بنجاح!")
                            st.balloons()
                            time.sleep(2)
                            st.rerun()
                        else: st.error("حدث خطأ أثناء الإرسال")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 6. التطبيق من الداخل ---
st.write(f"مرحباً بك يا {st.session_state.get('user', 'أيها المشترك')}")
