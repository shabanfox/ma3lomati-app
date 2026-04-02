import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CONSTANTS ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
ITEMS_PER_PAGE = 6

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'view' not in st.session_state: st.session_state.view = "grid" 
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'last_menu' not in st.session_state: st.session_state.last_menu = "Launches"
if 'messages' not in st.session_state: st.session_state.messages = []
if 'current_user' not in st.session_state: st.session_state.current_user = None

# --- 3. CSS Luxury Design (Compact & Top Aligned) ---
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

    /* تخصيص التبويبات لإلغاء المربعات البيضاء الخلفية */
    .stTabs [data-baseweb="tab-panel"] {{
        background: transparent !important;
        border: none !important;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        background: transparent !important;
        border-bottom: 2px solid #f59e0b !important;
        gap: 10px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #f8f9fa !important;
        border-radius: 10px 10px 0 0 !important;
        color: #000 !important;
        font-weight: bold !important;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #f59e0b !important;
        color: #000 !important;
    }}

    /* Auth UI Styling */
    .auth-card-wrap {{
        background-color: #ffffff; padding: 30px; border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4); margin-top: -20px;
    }}
    
    div.stTextInput input {{ 
        background-color: #000 !important; color: #fff !important; 
        border: 1px solid #f59e0b !important; border-radius: 10px !important; 
        height: 42px !important; text-align: center !important;
    }}
    
    .stButton button {{ 
        background-color: #000 !important; color: #f59e0b !important; 
        border: 2px solid #f59e0b !important; border-radius: 10px !important;
        font-weight: 900 !important; transition: 0.3s; width: 100%;
    }}

    /* Internal App UI */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; padding: 40px; text-align: center; 
        border-bottom: 3px solid #f59e0b; border-radius: 0 0 40px 40px; margin-bottom: 25px;
    }}
    .detail-card {{ background: rgba(20, 20, 20, 0.95); padding: 25px; border-radius: 20px; border-top: 5px solid #f59e0b; border: 1px solid #333; }}
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

def signup_user(name, pas, mail, wa, co):
    # محاكاة لنجاح التسجيل (يرتبط لاحقاً بـ API لإضافة صف للجوجل شيت)
    return True

@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    u_l = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(u_p), pd.read_csv(u_d), pd.read_csv(u_l)
        for df in [p, d, l]: df.columns = [c.strip() for c in df.columns]
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 5. شاشة الدخول والاشتراك (تم دمجها بربط الجوجل شيت) ---
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:30px;'><h1 style='color:#f59e0b; font-size:50px; font-weight:900;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    
    _, center_col, _ = st.columns([1, 1.2, 1])
    
    with center_col:
        st.markdown("<div class='auth-card-wrap'>", unsafe_allow_html=True)
        tab_login, tab_signup = st.tabs(["🔐 تسجيل دخول", "📝 اشتراك جديد"])
        
        with tab_login:
            st.write("")
            u_input = st.text_input("الأسم أو الجيميل", key="log_user", placeholder="Username / Email")
            p_input = st.text_input("كلمة السر", type="password", key="log_pass", placeholder="Password")
            
            if st.button("دخول للمنصة 🚀"):
                if p_input == "2026": # الكود المباشر للأدمن
                    st.session_state.auth = True
                    st.session_state.current_user = "Admin"
                    st.rerun()
                else:
                    user_verified = login_user(u_input, p_input)
                    if user_verified:
                        st.session_state.auth = True
                        st.session_state.current_user = user_verified
                        st.rerun()
                    else:
                        st.error("بيانات الدخول غير صحيحة")

        with tab_signup:
            st.write("")
            reg_name = st.text_input("الأسم بالكامل", placeholder="Full Name")
            reg_pass = st.text_input("كلمة السر المرجوة", type="password", placeholder="Min 8 characters")
            reg_email = st.text_input("الجيميل", placeholder="Email")
            reg_wa = st.text_input("رقم الواتساب", placeholder="WhatsApp Number")
            reg_co = st.text_input("الشركة", placeholder="Company Name")
            
            if st.button("تأكيد الاشتراك ✅"):
                if reg_name and reg_pass and reg_email:
                    if len(reg_pass) < 8:
                        st.error("كلمة السر يجب ألا تقل عن 8 أرقام")
                    elif signup_user(reg_name, reg_pass, reg_email, reg_wa, reg_co):
                        st.success("تم تسجيل طلبك بنجاح! راجع الإدارة لتفعيل الحساب.")
                    else: st.error("حدث خطأ في الاتصال")
                else: st.warning("يرجى ملء الاسم وكلمة السر والإيميل")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. MAIN APP ---
df_p, df_d, df_l = load_data()
L = {"menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"]}

st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900; margin:0;">MA3LOMATI</h1></div>', unsafe_allow_html=True)

menu = option_menu(None, L["menu"], default_index=4, orientation="horizontal", 
                   styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if menu != st.session_state.last_menu:
    st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu
    st.rerun()

# --- 7. CONTENT DISPLAY ---
active_df = df_p if menu=="Projects" else (df_l if menu=="Launches" else df_d)

if menu == "Tools":
    st.info("Tools section is being updated...")
elif menu == "AI Assistant":
    st.chat_message("assistant").write("How can I help you today?")
else:
    if active_df.empty:
        st.error("No Data Found")
    else:
        col_main = active_df.columns[0]
        if st.session_state.view == "details":
            # تفاصيل العنصر
            if st.button("⬅ Back"): st.session_state.view = "grid"; st.rerun()
            item = active_df.iloc[st.session_state.current_index]
            st.markdown(f"<div class='detail-card'><h2>{item[col_main]}</h2><hr>", unsafe_allow_html=True)
            st.write(item)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            # عرض الشبكة (Grid)
            search = st.text_input("🔍 Search")
            filt = active_df[active_df[col_main].astype(str).str.contains(search, case=False)] if search else active_df
            start = st.session_state.page_num * ITEMS_PER_PAGE
            disp = filt.iloc[start : start + ITEMS_PER_PAGE]
            
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    if st.button(f"🏢 {r[col_main]}", key=f"card_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()

# Logout Sidebar
if st.sidebar.button("Logout"):
    st.session_state.auth = False; st.rerun()
