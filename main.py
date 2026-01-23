import streamlit as st

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False

# --- 3. CSS "Perfect Middle" UI ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding: 0px !important; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), 
                    url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    /* حاوية تضمن وجود كل شيء في منتصف الصفحة تماماً */
    .main-center-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        width: 100%;
        text-align: center;
    }}

    /* اسم المنصة في المنتصف */
    .brand-header {{
        color: #f59e0b;
        font-size: 55px;
        font-weight: 900;
        margin-bottom: 5px;
        text-shadow: 0 0 20px rgba(245, 158, 11, 0.4);
    }}
    
    .brand-subtext {{
        color: #ffffff;
        font-size: 22px;
        margin-bottom: 40px;
        opacity: 0.9;
    }}

    /* جعل التبويبات والخانات متمركزة */
    .stTabs {{
        width: 100%;
        max-width: 400px;
    }}
    
    div.stTextInput input {{
        text-align: center !important;
        border-radius: 15px !important;
        height: 50px !important;
        background: rgba(255,255,255,0.05) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
    }}

    .stButton button {{
        background: #f59e0b !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        height: 50px !important;
    }}
    </style>
""", unsafe_allow_html=True)

if not st.session_state.auth:
    st.markdown("<div class='main-center-container'>", unsafe_allow_html=True)
    
    st.markdown("<p class='brand-header'>MA3LOMATI PRO</p>", unsafe_allow_html=True)
    st.markdown("<p class='brand-subtext'>المنصة العقارية الذكية</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["دخول", "اشتراك"])
    with tab1:
        st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed")
        st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed")
        if st.button("دخول", use_container_width=True):
            st.session_state.auth = True
            st.rerun()
            
    st.markdown("</div>", unsafe_allow_html=True)
