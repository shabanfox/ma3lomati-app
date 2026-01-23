import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CONSTANTS ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 2. Session State Initialization ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'view' not in st.session_state: st.session_state.view = "grid" 
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'last_menu' not in st.session_state: st.session_state.last_menu = "Projects"
if 'messages' not in st.session_state: st.session_state.messages = []

trans = {
    "EN": {
        "logout": "Logout", "back": "🏠 Back to List",
        "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "side_dev": "⭐ TOP DEVELOPERS", "side_proj": "🏠 READY TO MOVE", "search": "Search assets...",
        "det_title": "Project Specifications", "ai_welcome": "How can I help you today?",
        "tool_title": "Professional Broker Tools", "login": "Enter Passcode"
    },
    "AR": {
        "logout": "خروج", "back": "🏠 العودة للقائمة",
        "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "side_dev": "⭐ أفضل المطورين", "side_proj": "🏠 استلام فوري", "search": "بحث عن عقار...",
        "det_title": "مواصفات وتفاصيل المشروع", "ai_welcome": "كيف يمكنني مساعدتك اليوم؟",
        "tool_title": "أدوات البروكر المحترف", "login": "أدخل رمز الدخول"
    }
}

L = trans[st.session_state.lang]
direction = "rtl" if st.session_state.lang == "AR" else "ltr"

# --- 3. Luxury CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.97), rgba(0,0,0,0.97)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {direction} !important; text-align: {"right" if direction=="rtl" else "left"} !important; 
        font-family: 'Cairo', sans-serif;
    }}

    /* الهيدر الملكي مع الأزرار العلوية */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.7)), url('{HEADER_IMG}');
        background-size: cover; background-position: center;
        border-bottom: 2px solid #f59e0b; padding: 60px 20px; text-align: center;
        border-radius: 0 0 40px 40px; margin-bottom: 20px; position: relative;
    }}

    /* تصغير أزرار التحكم العلوية */
    .top-controls {{
        position: absolute; top: 15px; left: 20px; right: 20px;
        display: flex; justify-content: space-between; align-items: center;
    }}
    
    div.stButton > button {{ font-size: 12px !important; padding: 2px 10px !important; }}
    
    /* ستايل الكروت */
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; color: #FFFFFF !important;
        border-left: 5px solid #f59e0b !important; border-radius: 15px !important;
        height: 180px !important; width: 100% !important;
        text-align: {"right" if direction=="rtl" else "left"} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Logic: Authentication & Header Buttons ---

# شاشة الهيدر (تظهر دائماً)
st.markdown(f'''
    <div class="royal-header">
        <h1 style="color:#f59e0b; font-weight:900; font-size: 50px; margin:0;">MA3LOMATI</h1>
        <p style="color:white; letter-spacing: 5px;">PRO 2026</p>
    </div>
''', unsafe_allow_html=True)

# وضع الأزرار "فوق" الهيدر باستخدام أعمدة Streamlit في طبقة علوية
t_col1, t_col2, t_col3 = st.columns([0.2, 0.6, 0.2])

with t_col1:
    if st.button("🌐 EN/AR", key="lang_btn"):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()

with t_col3:
    if st.session_state.auth:
        if st.button(f"🚪 {L['logout']}", key="logout_btn"): st.session_state.auth = False; st.rerun()
    else:
        # خانة دخول صغيرة جداً في الركن
        passcode = st.text_input(L["login"], type="password", key="pass_input", label_visibility="collapsed", placeholder="****")
        if passcode == "2026": 
            st.session_state.auth = True; st.rerun()

# إذا لم يسجل الدخول، توقف هنا
if not st.session_state.auth:
    st.warning("⚠️ Please enter passcode to access the portal.")
    st.stop()

# --- 5. Data Loading (نفس الكود الخاص بك) ---
@st.cache_data(ttl=60)
def load_all_data():
    URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    URL_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(URL_P), pd.read_csv(URL_D), pd.read_csv(URL_L)
        for df in [p, d, l]: df.columns = [c.strip() for c in df.columns]
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_all_data()

# --- 6. Navigation Bar ---
menu_selection = option_menu(None, L["menu"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}, 
            "container": {"background-color": "rgba(0,0,0,0.5)", "border-radius": "20px"}})

if menu_selection != st.session_state.last_menu:
    st.session_state.view = "grid"
    st.session_state.page_num = 0
    st.session_state.last_menu = menu_selection
    st.rerun()

# --- 7. View Logic (استكمال نفس المنطق الخاص بك مع تحسينات طفيفة) ---
# [هنا نضع بقية الأقسام: الأدوات، المساعد الذكي، المشاريع...]

if menu_selection in ["Tools", "الأدوات"]:
    # ... (نفس كود الأدوات الخاص بك)
    st.markdown(f"<h2 style='color:#f59e0b; text-align:center;'>⚒️ {L['tool_title']}</h2>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    # ... (باقي الكود)
    with t1:
        with st.container(border=True):
            st.subheader("🧮 Mortgage / القسط")
            p_val = st.number_input("Amount", 0, key="mort_p")
            y_val = st.number_input("Years", 1, 20, 7)
            if p_val > 0: st.warning(f"Monthly: {p_val/(y_val*12):,.2f}")

# نفس المنطق للونشات والمشاريع
is_launch = menu_selection in ["Launches", "اللونشات"]
if not menu_selection in ["Tools", "الأدوات", "AI Assistant", "المساعد الذكي"]:
    if menu_selection in ["Projects", "المشاريع"]: 
        active_df, col_main_name = df_p, 'Project Name'
    elif is_launch: 
        active_df, col_main_name = df_l, 'Project'
    else: 
        active_df, col_main_name = df_d, 'Developer'

    # البحث وعرض الكروت (نفس كودك الأصلي)
    search = st.text_input(L["search"])
    # ... تكملة العرض
