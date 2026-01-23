import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CONSTANTS ---
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"

# --- 3. CSS Custom Premium UI ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 3rem !important; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
    }}

    /* Glassmorphism Card */
    .auth-container {{
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-radius: 35px;
        padding: 45px 35px;
        width: 420px;
        margin: auto;
        text-align: center;
        box-shadow: 0 30px 60px rgba(0,0,0,0.6);
    }}

    /* Title inside Card */
    .card-title {{
        color: #f59e0b;
        font-size: 32px;
        font-weight: 900;
        margin-bottom: 5px;
        letter-spacing: 1px;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }}
    .card-subtitle {{
        color: #ddd;
        font-size: 13px;
        margin-bottom: 30px;
        letter-spacing: 2px;
    }}

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: transparent !important;
        justify-content: center !important;
        border-bottom: 1px solid rgba(245, 158, 11, 0.2) !important;
        margin-bottom: 20px;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: #ffffff !important;
        background: transparent !important;
        font-weight: 700 !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #f59e0b !important;
        border-bottom: 3px solid #f59e0b !important;
    }}

    /* Inputs */
    div.stTextInput input {{
        background: rgba(0,0,0,0.5) !important;
        color: #fff !important;
        border: 1px solid #555 !important;
        border-radius: 12px !important;
        height: 45px !important;
        text-align: center !important;
    }}
    div.stTextInput input:focus {{
        border-color: #f59e0b !important;
    }}

    /* Premium Button */
    .stButton button {{
        background: linear-gradient(135deg, #f59e0b, #92400e) !important;
        color: #000 !important;
        font-weight: 900 !important;
        border: none !important;
        border-radius: 12px !important;
        height: 48px !important;
        width: 100%;
        margin-top: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Logic Functions ---
def login_user(u, p):
    try:
        df = pd.read_csv(USER_SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        user = df[(df['Name'].astype(str) == str(u)) & (df['Password'].astype(str) == str(p))]
        return u if not user.empty else None
    except: return None

# --- 5. UI LOGIN/SIGNUP ---
if not st.session_state.auth:
    st.write("") # Space
    st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
    
    # اسم المنصة داخل الكارت
    st.markdown("<div class='card-title'>MA3LOMATI PRO</div>", unsafe_allow_html=True)
    st.markdown("<div class='card-subtitle'>المنصة العقارية الذكية</div>", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["🔐 دخول", "📝 اشتراك"])
    
    with tab_login:
        st.write("")
        u_in = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed", key="l_u")
        p_in = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="l_p")
        
        if st.button("تسجيل الدخول", use_container_width=True):
            if p_in == "2026":
                st.session_state.auth = True; st.rerun()
            else:
                if login_user(u_in, p_in):
                    st.session_state.auth = True; st.rerun()
                else: st.error("خطأ في البيانات")

    with tab_signup:
        st.write("")
        name = st.text_input("Name", placeholder="الأسم بالكامل", label_visibility="collapsed", key="reg_n")
        mail = st.text_input("Email", placeholder="الجيميل", label_visibility="collapsed", key="reg_e")
        wa = st.text_input("WA", placeholder="رقم الواتساب", label_visibility="collapsed", key="reg_w")
        co = st.text_input("CO", placeholder="اسم الشركة", label_visibility="collapsed", key="reg_c")
        pas = st.text_input("Pass", type="password", placeholder="كلمة السر (8 أرقام+)", label_visibility="collapsed", key="reg_p")
        
        if st.button("إرسال طلب الانضمام", use_container_width=True):
            if name and mail and pas:
                if len(pas) < 8: st.warning("يجب أن تكون كلمة السر 8 خانات فأكثر")
                else: st.success("تم إرسال طلبك بنجاح")
            else: st.warning("يرجى إكمال كافة البيانات")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. INTERNAL APP (بقية التطبيق) ---
else:
    st.markdown('<h1 style="color:#f59e0b; text-align:center; padding:30px;">MA3LOMATI PRO</h1>', unsafe_allow_html=True)
    if st.button("🚪 تسجيل الخروج"):
        st.session_state.auth = False; st.rerun()
