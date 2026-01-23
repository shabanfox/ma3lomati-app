import streamlit as st
import pandas as pd

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 3. CSS "Ultra-Modern Liquid Dark" UI ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    /* خلفية سينمائية ثابتة مع تعتيم قوي */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
    }}

    /* حاوية تجعل المحتوى في منتصف الشاشة */
    .auth-wrapper {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 95vh;
        width: 100%;
    }}

    /* الكارت الزجاجي العملاق */
    .glass-portal {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 50px;
        padding: 60px 50px;
        width: 450px;
        text-align: center;
        box-shadow: 0 50px 100px rgba(0,0,0,0.9);
        transition: 0.5s ease;
    }}
    .glass-portal:hover {{
        border: 1px solid rgba(245, 158, 11, 0.6);
        box-shadow: 0 50px 120px rgba(245, 158, 11, 0.1);
    }}

    /* اسم المنصة - تأثير التوهج الذهبي */
    .brand-title {{
        color: #f59e0b;
        font-size: 45px;
        font-weight: 900;
        margin: 0;
        letter-spacing: -1px;
        text-shadow: 0 0 25px rgba(245, 158, 11, 0.5);
    }}
    
    .brand-desc {{
        color: #ffffff;
        font-size: 19px;
        font-weight: 400;
        margin-bottom: 45px;
        opacity: 0.8;
        letter-spacing: 3px;
    }}

    /* تخصيص التبويبات بشكل مخفي */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 20px !important;
        padding: 8px !important;
        margin-bottom: 30px !important;
        gap: 10px;
    }}
    .stTabs [data-baseweb="tab"] {{
        color: #999 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 15px !important;
        transition: 0.3s;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #f59e0b !important;
        color: #000 !important;
    }}

    /* مدخلات البيانات - تصميم عائم */
    div.stTextInput input {{
        background: rgba(0,0,0,0.5) !important;
        color: #fff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 18px !important;
        height: 55px !important;
        text-align: center !important;
        font-size: 16px !important;
        transition: 0.4s;
    }}
    div.stTextInput input:focus {{
        border-color: #f59e0b !important;
        background: rgba(0,0,0,0.7) !important;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.2) !important;
    }}

    /* الزرار الاحترافي */
    .stButton button {{
        background: linear-gradient(135deg, #f59e0b, #d97706) !important;
        color: #000 !important;
        font-weight: 900 !important;
        font-size: 18px !important;
        border: none !important;
        border-radius: 18px !important;
        height: 58px !important;
        width: 100%;
        margin-top: 20px;
        box-shadow: 0 15px 30px rgba(217, 119, 6, 0.3);
        transition: 0.3s;
    }}
    .stButton button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(217, 119, 6, 0.4);
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Login Logic ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    
    # الكارت الجديد بالكامل
    st.markdown("<div class='glass-portal'>", unsafe_allow_html=True)
    
    # اسم المنصة والوصف داخل قلب الكارت
    st.markdown("<p class='brand-title'>MA3LOMATI PRO</p>", unsafe_allow_html=True)
    st.markdown("<p class='brand-desc'>المنصة العقارية الذكية</p>", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["🔒 دخول", "📧 اشتراك"])
    
    with tab_login:
        st.write("")
        u_val = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed", key="log_u")
        p_val = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="log_p")
        
        if st.button("اكتشف العقارات الآن ➔", use_container_width=True):
            if p_val == "2026":
                st.session_state.auth = True; st.rerun()
            else:
                st.error("بيانات غير صحيحة")

    with tab_signup:
        st.write("")
        st.markdown("<p style='color:#ddd; margin-bottom:20px;'>سجل بياناتك للانضمام إلى نخبة العقاريين</p>", unsafe_allow_html=True)
        st.text_input("Full Name", placeholder="الاسم بالكامل", label_visibility="collapsed", key="s1")
        st.text_input("WhatsApp", placeholder="رقم الواتساب", label_visibility="collapsed", key="s2")
        if st.button("تقديم طلب عضوية", use_container_width=True):
            st.success("تم استلام طلبك، سنتواصل معك قريباً")

    st.markdown("</div>", unsafe_allow_html=True) # End glass-portal
    st.markdown("</div>", unsafe_allow_html=True) # End auth-wrapper
    st.stop()

# --- 5. التطبيق من الداخل ---
else:
    st.markdown('<h1 style="color:#f59e0b; text-align:center; padding-top:100px; font-size:50px;">MA3LOMATI PRO</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:white; text-align:center; font-size:20px;">مرحباً بك في عالمك الجديد</p>', unsafe_allow_html=True)
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.auth = False; st.rerun()
