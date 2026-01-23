import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- روابط الصور والبيانات ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
# رابط شيت المستخدمين (CSV)
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
ITEMS_PER_PAGE = 6

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'view' not in st.session_state: st.session_state.view = "grid" 
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'last_menu' not in st.session_state: st.session_state.last_menu = "Projects"
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 3. Authentication Logic ---
def check_auth(u, p):
    try:
        df_users = pd.read_csv(USER_SHEET_URL)
        df_users.columns = [c.strip() for c in df_users.columns]
        u_val, p_val = str(u).strip(), str(p).strip()
        if 'Name' in df_users.columns and 'Password' in df_users.columns:
            match = df_users[(df_users['Name'].astype(str).str.strip() == u_val) & 
                             (df_users['Password'].astype(str).str.strip() == p_val)]
            return not match.empty
        return False
    except: return False

# --- 4. Translations ---
trans = {
    "EN": {
        "login_tab": "Login", "signup_tab": "Sign Up", "user": "Name", "pass": "Password", "login_btn": "Sign In",
        "signup_btn": "Create Account", "email": "Email", "wa": "WhatsApp", "co": "Company",
        "logout": "Logout", "back": "🏠 Back", "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "side_proj": "🏠 READY", "search": "Search assets...", "next": "Next ➡", "prev": "⬅ Prev"
    },
    "AR": {
        "login_tab": "تسجيل الدخول", "signup_tab": "إنشاء حساب", "user": "الاسم", "pass": "كلمة المرور", "login_btn": "دخول",
        "signup_btn": "إرسال البيانات", "email": "الإيميل", "wa": "واتساب", "co": "الشركة",
        "logout": "خروج", "back": "🏠 العودة", "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "side_proj": "🏠 استلام فوري", "search": "بحث...", "next": "التالي ➡", "prev": "⬅ السابق"
    }
}
L = trans[st.session_state.lang]
direction = "rtl" if st.session_state.lang == "AR" else "ltr"

# --- 5. Custom CSS (Centered & Luxury) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {direction} !important; font-family: 'Cairo', sans-serif;
    }}
    /* Centering the Auth Card */
    .auth-wrapper {{
        display: flex; justify-content: center; align-items: center; min-height: 90vh;
    }}
    .auth-card {{
        background: rgba(255, 255, 255, 0.07); backdrop-filter: blur(15px);
        padding: 40px; border-radius: 25px; border: 1px solid rgba(245, 158, 11, 0.3);
        width: 100%; max-width: 450px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{HEADER_IMG}');
        background-size: cover; border-bottom: 2px solid #f59e0b; padding: 40px;
        text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 30px;
    }}
    div.stButton > button {{ border-radius: 10px !important; }}
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; color: white !important;
        border-left: 5px solid #f59e0b !important; height: 180px !important; width: 100% !important;
    }}
    .detail-card {{ background: rgba(20, 20, 20, 0.95); padding: 25px; border-radius: 15px; border-top: 5px solid #f59e0b; color: white; }}
    .mini-side-card {{ background: rgba(30, 30, 30, 0.8); padding: 10px; border-radius: 8px; border-right: 4px solid #f59e0b; margin-bottom: 8px; color: #f59e0b; font-size: 13px; }}
    .label-gold {{ color: #f59e0b; font-weight: 700; margin-top: 15px; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. AUTHENTICATION PAGE ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
        st.markdown("<h1 style='color:#f59e0b;'>MA3LOMATI</h1>", unsafe_allow_html=True)
        
        t_login, t_signup = st.tabs([L["login_tab"], L["signup_tab"]])
        
        with t_login:
            u_in = st.text_input(L["user"], key="u_login")
            p_in = st.text_input(L["pass"], type="password", key="p_login")
            if st.button(L["login_btn"], use_container_width=True, type="primary"):
                if check_auth(u_in, p_in):
                    st.session_state.auth = True; st.rerun()
                else: st.error("خطأ في البيانات")
        
        with t_signup:
            st.text_input(L["user"], key="s_name")
            st.text_input(L["email"], key="s_email")
            st.text_input(L["wa"], key="s_wa")
            st.text_input(L["co"], key="s_co")
            st.text_input(L["pass"], type="password", key="s_pass")
            if st.button(L["signup_btn"], use_container_width=True):
                st.success("تم إرسال طلبك للمراجعة بنجاح")
        
        st.write("---")
        if st.button("🌐 English / العربية", use_container_width=True):
            st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 7. MAIN PLATFORM (AFTER LOGIN) ---
else:
    @st.cache_data(ttl=60)
    def load_all_data():
        U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
        U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
        U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
        try:
            p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
            for df in [p, d, l]: df.columns = [c.strip() for c in df.columns]
            return p.fillna("---"), d.fillna("---"), l.fillna("---")
        except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    df_p, df_d, df_l = load_all_data()

    st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900;">MA3LOMATI</h1></div>', unsafe_allow_html=True)

    c_nav, c_out = st.columns([0.85, 0.15])
    with c_nav:
        menu = option_menu(None, L["menu"], default_index=2, orientation="horizontal",
            styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
        if menu != st.session_state.last_menu:
            st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu; st.rerun()
    with c_out:
        if st.button(f"🚪 {L['logout']}", use_container_width=True): st.session_state.auth = False; st.rerun()

    # --- Section Logic ---
    if menu in ["Tools", "الأدوات"]:
        st.markdown(f"<h2 style='color:#f59e0b; text-align:center;'>⚒️ Tools</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("🧮 Mortgage")
            p_v = st.number_input("Amount", 0); y_v = st.number_input("Years", 1, 20, 7)
            if p_v > 0: st.info(f"Monthly: {p_v/(y_v*12):,.2f}")
        with col2:
            st.subheader("📈 ROI")
            c_v = st.number_input("Cost", 1); r_v = st.number_input("Rent", 0)
            st.success(f"ROI: {(r_v/c_v)*100:.2f}%")
        with col3:
            st.subheader("📏 Area")
            sqm = st.number_input("SQM", 0.0)
            st.warning(f"SQFT: {sqm * 10.76:.2f}")

    elif menu in ["AI Assistant", "المساعد الذكي"]:
        st.markdown(f"<div class='detail-card'><h3>🤖 AI Advisor</h3></div>", unsafe_allow_html=True)
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.write(msg["content"])
        if p := st.chat_input("Ask something..."):
            st.session_state.messages.append({"role": "user", "content": p})
            st.session_state.messages.append({"role": "assistant", "content": f"Processing: {p}"})
            st.rerun()

    else:
        # Projects / Developers / Launches
        if menu in ["Projects", "المشاريع"]: active_df = df_p
        elif menu in ["Launches", "اللونشات"]: active_df = df_l
        else: active_df = df_d
        
        col_name = active_df.columns[0]

        if st.session_state.view == "details":
            item = active_df.iloc[st.session_state.current_index]
            if st.button(L["back"], use_container_width=True): st.session_state.view = "grid"; st.rerun()
            c1, c2 = st.columns(2)
            for i, c in enumerate(active_df.columns):
                with (c1 if i % 2 == 0 else c2):
                    st.markdown(f"<div class='detail-card'><p class='label-gold'>{c}</p><p>{item[c]}</p></div>", unsafe_allow_html=True)
        else:
            search = st.text_input(L["search"])
            filtered = active_df[active_df[col_name].astype(str).str.contains(search, case=False)]
            start = st.session_state.page_num * ITEMS_PER_PAGE
            display = filtered.iloc[start : start + ITEMS_PER_PAGE]

            main, side = st.columns([0.8, 0.2])
            with main:
                grid = st.columns(2)
                for i, (idx, r) in enumerate(display.iterrows()):
                    with grid[i % 2]:
                        if st.button(f"✨ {r[col_name]}\n📍 {r.get('Area','---')}", key=f"card_{idx}"):
                            st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()
            with side:
                st.markdown(f"<p style='color:#f59e0b;'>{L['side_proj']}</p>", unsafe_allow_html=True)
                for _, s in active_df.head(6).iterrows():
                    st.markdown(f"<div class='mini-side-card'>💎 {s[col_name][:22]}</div>", unsafe_allow_html=True)

            st.write("---")
            b1, b2 = st.columns(2)
            with b1:
                if st.session_state.page_num > 0:
                    if st.button(L["prev"], use_container_width=True): st.session_state.page_num -= 1; st.rerun()
            with b2:
                if (start + ITEMS_PER_PAGE) < len(filtered):
                    if st.button(L["next"], use_container_width=True): st.session_state.page_num += 1; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
