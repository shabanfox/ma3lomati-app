import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CONSTANTS ---
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"

# --- 3. CSS (Mini & Top Aligned Design) ---
direction = "rtl" if st.session_state.lang == "AR" else "ltr"
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 1rem !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {direction} !important; font-family: 'Cairo', sans-serif;
    }}

    /* تصميم تسجيل الدخول المصغر وفي الأعلى */
    .auth-wrapper {{ 
        display: flex; flex-direction: column; align-items: center; 
        justify-content: flex-start; width: 100%; padding-top: 20px; 
    }}
    .oval-header {{
        background-color: #000; border: 2px solid #f59e0b; border-radius: 40px;
        padding: 8px 30px; color: #f59e0b; font-size: 18px; font-weight: 900;
        text-align: center; z-index: 10; margin-bottom: -18px; min-width: 250px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }}
    .auth-card {{ 
        background-color: #ffffff; width: 320px; padding: 35px 25px 20px 25px; 
        border-radius: 25px; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }}
    
    /* تصغير حقول الإدخال */
    div.stTextInput input {{ 
        background-color: #000 !important; color: #fff !important; 
        border: 1px solid #f59e0b !important; border-radius: 10px !important; 
        text-align: center !important; height: 38px !important; font-size: 14px !important;
    }}
    
    /* تصغير الأزرار */
    .stButton button {{ 
        background-color: #000 !important; color: #f59e0b !important; 
        border: 1.5px solid #f59e0b !important; border-radius: 10px !important;
        font-weight: 700 !important; height: 40px !important; font-size: 14px !important;
    }}

    /* إخفاء أي خطوط أو كروت بيضاء إضافية */
    div[data-testid="stExpander"], div[data-testid="stTabs"] {{ 
        background: transparent !important; border: none !important; 
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Logic Functions ---
def check_auth(u, p):
    try:
        df = pd.read_csv(USER_SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        return not df[(df['Name'].astype(str).str.strip() == str(u).strip()) & 
                     (df['Password'].astype(str).str.strip() == str(p).strip())].empty
    except: return False

# --- 5. UI: LOGIN & REGISTER ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>منصة معلوماتي</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    
    # اختيار بسيط بدون كروت بيضاء
    mode = st.radio("Choose", ["Login", "Join"], label_visibility="collapsed", horizontal=True)
    
    if mode == "Login":
        st.write("")
        u_log = st.text_input("U", placeholder="User", label_visibility="collapsed", key="u_l")
        p_log = st.text_input("P", type="password", placeholder="Pass", label_visibility="collapsed", key="p_l")
        if st.button("SIGN IN", use_container_width=True):
            if check_auth(u_log, p_log): st.session_state.auth = True; st.rerun()
            else: st.error("Wrong info")
    else:
        # فورم الاشتراك الكامل
        r_name = st.text_input("N", placeholder="Full Name", key="r1")
        r_email = st.text_input("E", placeholder="Email", key="r2")
        r_wa = st.text_input("W", placeholder="WhatsApp", key="r3")
        r_comp = st.text_input("C", placeholder="Company", key="r4")
        r_pass = st.text_input("P", type="password", placeholder="Pass (Min 8)", key="r5")
        
        if st.button("SUBMIT JOIN", use_container_width=True):
            if not all([r_name, r_email, r_wa, r_comp, r_pass]):
                st.error("Fill all fields!")
            elif len(r_pass) < 8:
                st.error("Min 8 characters!")
            else:
                join_date = datetime.now().strftime("%Y-%m-%d")
                st.success(f"Success! Joined on {join_date}")

    st.markdown("</div>", unsafe_allow_html=True)
    
    # زر اللغة المصغر تحت الكارت
    st.write("")
    if st.button("🌐 Change Language", key="lang_btn"):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. INTERNAL APP ---
else:
    # سيتم تحميل صفحة اللونشات مباشرة
    st.markdown('<h2 style="color:#f59e0b; text-align:center;">MA3LOMATI PRO</h2>', unsafe_allow_html=True)
    
    menu = option_menu(None, ["Tools", "Developers", "Projects", "AI Assistant", "Launches"], 
                       default_index=4, orientation="horizontal",
                       styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
    
    if st.button("🚪 Logout"):
        st.session_state.auth = False; st.rerun()
    
    st.success(f"Welcome! Current Page: {menu}")
