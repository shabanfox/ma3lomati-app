import streamlit as st

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 3. CSS "Top-Centered Floating" UI ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الهيدر الافتراضي وتصفير المسافات */
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

    /* الحاوية: سنتر عرضاً وملتصقة فوق طولاً */
    .top-center-fixed {{
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%); /* لضمان السنترة العرضية بدقة */
        width: 100%;
        max-width: 420px;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 20px; /* مسافة بسيطة من السقف لراحة العين */
        z-index: 100;
    }}

    /* اسم المنصة */
    .brand-title {{
        color: #f59e0b;
        font-size: 52px;
        font-weight: 900;
        margin: 0;
        text-shadow: 2px 4px 15px rgba(0,0,0,1);
        text-align: center;
        white-space: nowrap;
    }}
    
    .brand-tagline {{
        color: #ffffff;
        font-size: 20px;
        font-weight: 400;
        margin-bottom: 30px;
        text-shadow: 1px 1px 10px rgba(0,0,0,0.8);
        opacity: 0.95;
    }}

    /* التبويبات الشفافة */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(0,0,0,0.5) !important;
        border-radius: 15px;
        justify-content: center !important;
        border: none !important;
        padding: 5px;
        margin-bottom: 20px;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: rgba(255,255,255,0.7) !important;
        font-weight: 700 !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #f59e0b !important;
    }}

    /* حقول الإدخال */
    div.stTextInput input {{
        background: rgba(0, 0, 0, 0.8) !important;
        color: #fff !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        border-radius: 12px !important;
        height: 50px !important;
        text-align: center !important;
    }}

    /* الزرار */
    .stButton button {{
        background: linear-gradient(90deg, #f59e0b, #d97706) !important;
        color: #000 !important;
        font-weight: 900 !important;
        border-radius: 12px !important;
        height: 52px !important;
        border: none !important;
        margin-top: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Login Logic ---
if not st.session_state.auth:
    # استخدام الحاوية العلوية المركزية
    st.markdown("<div class='top-center-fixed'>", unsafe_allow_html=True)
    
    # اسم المنصة في القمة
    st.markdown("<p class='brand-title'>MA3LOMATI PRO</p>", unsafe_allow_html=True)
    st.markdown("<p class='brand-tagline'>المنصة العقارية الذكية</p>", unsafe_allow_html=True)
    
    tab_in, tab_up = st.tabs(["🔐 دخول", "📝 اشتراك"])
    
    with tab_in:
        st.write("")
        u = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_final")
        p = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="p_final")
        if st.button("دخول آمن", use_container_width=True):
            if p == "2026":
                st.session_state.auth = True; st.rerun()
            else:
                st.error("البيانات غير صحيحة")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. الصفحة الداخلية ---
else:
    st.success("تم تسجيل الدخول بنجاح")
    if st.button("تسجيل الخروج"):
        st.session_state.auth = False; st.rerun()
