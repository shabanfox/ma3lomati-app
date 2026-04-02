import streamlit as st
import pandas as pd

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 3. CSS "The Invisible UI" ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.85)), 
                    url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
    }}

    /* حاوية عائمة في منتصف الشاشة بدون كروت */
    .floating-auth-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        width: 100%;
        max-width: 450px;
        margin: auto;
    }}

    /* اسم المنصة عائم بتوهج خفيف */
    .brand-glow {{
        color: #f59e0b;
        font-size: 50px;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 0 30px rgba(245, 158, 11, 0.4);
        text-align: center;
    }}
    
    .brand-tagline-floating {{
        color: #ffffff;
        font-size: 20px;
        font-weight: 400;
        margin-bottom: 40px;
        letter-spacing: 2px;
        opacity: 0.9;
        text-align: center;
    }}

    /* جعل التبويبات شفافة بالكامل */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: transparent !important;
        justify-content: center !important;
        border: none !important;
        margin-bottom: 20px;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: rgba(255,255,255,0.6) !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        background: transparent !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: #f59e0b !important;
        border-bottom: 3px solid #f59e0b !important;
    }}

    /* حقول الإدخال عائمة ومستديرة بنعومة */
    div.stTextInput input {{
        background: rgba(255, 255, 255, 0.05) !important;
        color: #fff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        height: 55px !important;
        text-align: center !important;
        backdrop-filter: blur(10px);
        font-size: 16px !important;
    }}
    div.stTextInput input:focus {{
        border-color: #f59e0b !important;
        background: rgba(255, 255, 255, 0.1) !important;
    }}

    /* زرار الدخول بتأثير زجاجي ذهبي */
    .stButton button {{
        background: linear-gradient(90deg, #f59e0b, #d97706) !important;
        color: #000 !important;
        font-weight: 900 !important;
        border-radius: 20px !important;
        height: 55px !important;
        width: 100%;
        margin-top: 20px;
        border: none !important;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.2);
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Floating UI Logic ---
if not st.session_state.auth:
    # بدء الحاوية العائمة
    st.markdown("<div class='floating-auth-container'>", unsafe_allow_html=True)
    
    # اسم الموقع والوصف عائمين فوق الخلفية مباشرة
    st.markdown("<p class='brand-glow'>MA3LOMATI PRO</p>", unsafe_allow_html=True)
    st.markdown("<p class='brand-tagline-floating'>المنصة العقارية الذكية</p>", unsafe_allow_html=True)
    
    tab_log, tab_reg = st.tabs(["🔐 دخول", "📝 اشتراك"])
    
    with tab_log:
        st.write("")
        u = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_in")
        p = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="p_in")
        
        if st.button("دخول للمنصة", use_container_width=True):
            if p == "2026":
                st.session_state.auth = True; st.rerun()
            else:
                st.error("البيانات غير صحيحة")

    with tab_reg:
        st.write("")
        st.text_input("Name", placeholder="الأسم بالكامل", label_visibility="collapsed", key="r1")
        st.text_input("Phone", placeholder="رقم الهاتف", label_visibility="collapsed", key="r2")
        if st.button("طلب تفعيل", use_container_width=True):
            st.success("تم الإرسال!")

    st.markdown("</div>", unsafe_allow_html=True) # قفل الحاوية
    st.stop()

# --- 5. التطبيق بعد الدخول ---
else:
    st.markdown('<h1 style="color:#f59e0b; text-align:center; padding-top:50px;">MA3LOMATI PRO</h1>', unsafe_allow_html=True)
    if st.sidebar.button("خروج"):
        st.session_state.auth = False; st.rerun()
