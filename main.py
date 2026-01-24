import streamlit as st
import pandas as pd
import requests
import time
import io

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- الروابط ---
# رابط الـ Script URL الخاص بك (يجب أن يكون فعالاً لاستقبال POST)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
# رابط الشيت بصيغة CSV للقراءة
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 2. الحالة (Session State) ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'page' not in st.session_state: st.session_state.page = "login"

# --- 3. الدوال البرمجية ---

def get_users_df():
    """جلب البيانات من الشيت مع منع التخزين المؤقت"""
    try:
        response = requests.get(f"{USER_SHEET_URL}?v={time.time()}")
        df = pd.read_csv(io.StringIO(response.text))
        df.columns = [c.strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

def send_to_sheet(name, pwd, email, wa, comp):
    """إرسال البيانات الفعلية للشيت"""
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        return "Success" in response.text
    except:
        return False

# --- 4. التنسيق (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; padding-top: 50px; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 24px; font-weight: 900;
        text-align: center; margin-bottom: -30px; min-width: 360px; z-index: 10;
    }}
    .auth-card {{ 
        background-color: #ffffff; width: 400px; padding: 60px 40px 40px 40px; 
        border-radius: 30px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.5); 
    }}
    div.stButton > button {{ width: 100% !important; border-radius: 12px !important; font-weight: bold !important; }}
    .duplicate-msg {{ color: #721c24; background-color: #f8d7da; padding: 10px; border-radius: 10px; margin-bottom: 15px; font-size: 14px; border: 1px solid #f5c6cb; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. منطق الصفحات ---

if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>منصة معلوماتي العقارية</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)

    # --- أ: صفحة استعادة كلمة السر ---
    if st.session_state.page == "forgot":
        st.markdown("<h3 style='color:#333;'>🔑 استعادة الحساب</h3>", unsafe_allow_html=True)
        email_input = st.text_input("أدخل البريد الإلكتروني المسجل")
        if st.button("استرجاع كلمة السر"):
            df = get_users_df()
            if not df.empty and email_input in df['Email'].astype(str).values:
                password = df[df['Email'].astype(str) == email_input]['Password'].values[0]
                st.success(f"كلمة السر الخاصة بك هي: {password}")
            else:
                st.error("عذراً، هذا البريد غير موجود لدينا.")
        if st.button("العودة لتسجيل الدخول"):
            st.session_state.page = "login"
            st.rerun()

    # --- ب: صفحة الدخول والاشتراك ---
    else:
        tab1, tab2 = st.tabs(["🔐 تسجيل الدخول", "📝 اشتراك جديد"])
        
        with tab1:
            u_login = st.text_input("الاسم أو البريد الإلكتروني", key="l_u")
            p_login = st.text_input("كلمة المرور", type="password", key="l_p")
            if st.button("دخول", key="btn_login"):
                df = get_users_df()
                if p_login == "2026": # كود المطور
                    st.session_state.auth = True; st.rerun()
                elif not df.empty and not df[((df['Name']==u_login)|(df['Email']==u_login)) & (df['Password'].astype(str)==p_login)].empty:
                    st.session_state.auth = True; st.rerun()
                else:
                    st.error("بيانات الدخول غير صحيحة")
            
            if st.button("نسيت كلمة السر؟"):
                st.session_state.page = "forgot"
                st.rerun()

        with tab2:
            r_name = st.text_input("الاسم بالكامل", key="reg_n")
            r_email = st.text_input("البريد الإلكتروني", key="reg_e")
            r_wa = st.text_input("رقم الواتساب", key="reg_w")
            r_pass = st.text_input("كلمة السر", type="password", key="reg_p")
            r_comp = st.text_input("الشركة", key="reg_c")

            if st.button("إنشاء حساب جديد"):
                if r_name and r_email and r_pass:
                    with st.spinner("جاري التحقق من البيانات..."):
                        df = get_users_df()
                        # فحص التكرار
                        name_exists = r_name in df['Name'].astype(str).values if not df.empty else False
                        email_exists = r_email in df['Email'].astype(str).values if not df.empty else False
                        wa_exists = r_wa in df['WhatsApp'].astype(str).values if (not df.empty and 'WhatsApp' in df.columns) else False
                        
                        if name_exists or email_exists or wa_exists:
                            st.markdown(f"""
                            <div class='duplicate-msg'>
                                ⚠️ هذه البيانات (الاسم أو الإيميل أو الرقم) مسجلة مسبقاً!<br>
                                إذا كنت نسيت كلمة السر، يمكنك استعادتها الآن.
                            </div>
                            """, unsafe_allow_html=True)
                            if st.button("انتقل لاستعادة كلمة السر"):
                                st.session_state.page = "forgot"
                                st.rerun()
                        else:
                            if send_to_sheet(r_name, r_pass, r_email, r_wa, r_comp):
                                st.success("✅ تم الاشتراك بنجاح! يمكنك الدخول الآن.")
                                st.balloons()
                            else:
                                st.error("حدث خطأ في الاتصال، حاول مرة أخرى.")
                else:
                    st.warning("يرجى ملء الحقول المطلوبة.")

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 6. محتوى المنصة (يظهر بعد تسجيل الدخول) ---
st.markdown(f"<h2 style='color:gold; text-align:center;'>مرحباً بك في لوحة التحكم</h2>", unsafe_allow_html=True)
if st.button("تسجيل الخروج"):
    st.session_state.auth = False
    st.rerun()
