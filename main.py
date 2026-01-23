import streamlit as st
import pandas as pd

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 3. CSS "STUCK TO TOP" UI ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء أي عناصر إضافية وحذف المسافات */
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding: 0px !important; margin: 0px !important; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.6)), 
                    url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
    }}

    /* الحاوية الرئيسية ملتصفة بالأعلى تماماً */
    .absolute-top-wrapper {{
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding-top: 20px; /* مسافة بسيطة جداً من الحافة العلوية */
    }}

    .login-container-width {{
        width: 100%;
        max-width: 420px;
        text-align: center;
    }}

    /* اسم المنصة - في القمة */
    .brand-title {{
        color: #f59e0b;
        font-size: 50px;
        font-weight: 900;
        margin: 0;
        text-shadow: 2px 2px 15px rgba(0,0,0,1);
    }}
    
    .brand-tagline {{
        color: #ffffff;
        font-size: 18px;
        font-weight: 400;
        margin-bottom: 20px;
        text-shadow: 1px 1px 5px rgba(0,0,0,0.8);
    }}

    /* تبويبات شفافة */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(0,0,0,0.4) !important;
        border-radius: 15px;
        justify-content: center !important;
        border: none !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: rgba(255,255,255,0.8) !important;
        font-weight: 700 !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #f59e0b !important;
    }}

    /* حقول الإدخال */
    div.stTextInput input {{
        background: rgba(0, 0, 0, 0.8) !important;
        color: #fff !important;
        border: 1px solid rgba(245, 158, 11, 0.5) !important;
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
        height: 50px !important;
        border: none !important;
        margin-top: 15px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Logic ---
if not st.session_state.auth:
    # استخدام الـ Wrapper اللاصق في الأعلى
    st.markdown("<div class='absolute-top-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='login-container-width'>", unsafe_allow_html=True)
    
    # المحتوى بيبدأ من فوق خالص
    st.markdown("<p class='brand-title'>MA3LOMATI PRO</p>", unsafe_allow_html=True)
    st.markdown("<p class='brand-tagline'>المنصة العقارية الذكية</p>", unsafe_allow_html=True)
    
    t_in, t_up = st.tabs(["🔒 دخول", "📧 اشتراك"])
    
    with t_in:
        st.write("")
        st.text_input("U", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_top")
        st.text_input("P", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="p_top")
        if st.button("تسجيل الدخول", use_container_width=True):
            st.session_state.auth = True; st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 5. الداخلية ---
else:
    st.write("أهلاً بك!")
    if st.button("خروج"):
        st.session_state.auth = False; st.rerun()
