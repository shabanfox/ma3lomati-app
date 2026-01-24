import streamlit as st

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 3. CSS "Top-Centered Floating" UI ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding: 0px !important; margin: 0px !important; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.8)), 
                    url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
    }}

    .top-center-fixed {{
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 100%;
        max-width: 420px;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 30px;
        z-index: 100;
    }}

    .brand-title {{
        color: #f59e0b;
        font-size: 52px;
        font-weight: 900;
        margin: 0;
        text-shadow: 2px 4px 15px rgba(0,0,0,1);
        text-align: center;
    }}
    
    .brand-tagline {{
        color: #ffffff;
        font-size: 19px;
        font-weight: 400;
        margin-bottom: 30px;
        opacity: 0.95;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(0,0,0,0.5) !important;
        border-radius: 15px;
        justify-content: center !important;
        border: none !important;
        padding: 5px;
        margin-bottom: 20px;
    }}

    div.stTextInput input {{
        background: rgba(0, 0, 0, 0.8) !important;
        color: #fff !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 12px !important;
        height: 50px !important;
        text-align: center !important;
    }}

    .stButton button {{
        background: linear-gradient(90deg, #f59e0b, #d97706) !important;
        color: #000 !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        height: 52px !important;
        margin-top: 15px;
        border: none !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Login/Signup UI Logic ---
if not st.session_state.auth:
    st.markdown("<div class='top-center-fixed'>", unsafe_allow_html=True)
    
    st.markdown("<p class='brand-title'>MA3LOMATI PRO</p>", unsafe_allow_html=True)
    st.markdown("<p class='brand-tagline'>المنصة العقارية الذكية</p>", unsafe_allow_html=True)
    
    tab_in, tab_up = st.tabs(["🔐 دخول", "📝 اشتراك"])
    
    with tab_in:
        st.write("")
        u = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_log")
        p = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="p_log")
        if st.button("دخول آمن", use_container_width=True):
            if p == "2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("البيانات غير صحيحة")

    with tab_up:
        st.write("")
        # ملء بيانات صفحة الاشتراك
        full_name = st.text_input("Name", placeholder="الاسم بالكامل", label_visibility="collapsed", key="reg_name")
        phone = st.text_input("Phone", placeholder="رقم الواتساب", label_visibility="collapsed", key="reg_phone")
        email = st.text_input("Email", placeholder="البريد الإلكتروني", label_visibility="collapsed", key="reg_email")
        
        st.markdown("<p style='color: #bbb; font-size: 14px; margin-top: 10px;'>سيتم مراجعة طلبك وتفعيله من قبل الإدارة</p>", unsafe_allow_html=True)
        
        if st.button("إرسال طلب الانضمام", use_container_width=True):
            if full_name and phone:
                st.success("تم إرسال طلبك بنجاح! سنتواصل معك قريباً.")
            else:
                st.warning("يرجى ملء البيانات الأساسية (الاسم والهاتف)")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. الصفحة الداخلية (بعد الدخول) ---
else:
    st.title("مرحباً بك في لوحة التحكم")
    if st.button("خروج"):
        st.session_state.auth = False
        st.rerun()
