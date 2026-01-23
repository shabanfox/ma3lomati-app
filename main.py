import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", initial_sidebar_state="collapsed")

# --- CONSTANTS & LINKS ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
ITEMS_PER_PAGE = 6

# --- 2. Session State Initialization ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'view' not in st.session_state: st.session_state.view = "grid" 
if 'current_index' not in st.session_state: st.session_state.current_index = 0
# تم تغيير الافتراضي هنا إلى Launches
if 'last_menu' not in st.session_state: st.session_state.last_menu = "Launches"
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

# --- 4. Translations (English Menu Titles) ---
trans = {
    "EN": {
        "logout": "Logout", "back": "🏠 Back to List",
        "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "side_dev": "⭐ TOP DEVS", "side_proj": "🏠 READY", "search": "Search assets...",
        "det_title": "Project Specifications", "ai_welcome": "How can I help you today?",
        "tool_title": "Professional Broker Tools", "next": "Next ➡", "prev": "⬅ Prev"
    },
    "AR": {
        "logout": "خروج", "back": "🏠 العودة للقائمة",
        # تعديل أسماء القائمة لتكون إنجليزية دائماً
        "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "side_dev": "⭐ المطورين", "side_proj": "🏠 استلام فوري", "search": "بحث عن عقار...",
        "det_title": "مواصفات وتفاصيل المشروع", "ai_welcome": "كيف يمكنني مساعدتك اليوم؟",
        "tool_title": "أدوات البروكر المحترف", "next": "التالي ➡", "prev": "⬅ السابق"
    }
}

L = trans[st.session_state.lang]
direction = "rtl" if st.session_state.lang == "AR" else "ltr"

# --- 5. Custom CSS ---
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

    /* LOGIN UI */
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: flex-start; width: 100%; padding-top: 20px; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 50px;
        padding: 15px 40px; color: #f59e0b; font-size: 22px; font-weight: 900;
        text-align: center; z-index: 10; margin-bottom: -25px; min-width: 340px;
    }}
    .auth-card {{ background-color: #ffffff; width: 380px; padding: 50px 30px 30px 30px; border-radius: 25px; text-align: center; }}
    .lock-gold {{ font-size: 40px; color: #f59e0b; margin-bottom: 10px; }}
    div[data-testid="stVerticalBlock"] div.stTextInput input {{
        background-color: #111 !important; color: #fff !important;
        border: 1px solid #f59e0b !important; border-radius: 10px !important;
        text-align: center !important; height: 42px !important;
    }}

    /* INTERNAL UI */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{HEADER_IMG}');
        background-size: cover; background-position: center;
        border-bottom: 2px solid #f59e0b; padding: 40px 20px; text-align: center;
        border-radius: 0 0 40px 40px; margin-bottom: 30px;
    }}
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; color: #FFFFFF !important;
        border-left: 5px solid #f59e0b !important; border-radius: 15px !important;
        height: 200px !important; width: 100% !important;
        text-align: {"right" if direction=="rtl" else "left"} !important;
    }}
    .detail-card, .tool-card {{ background: rgba(20, 20, 20, 0.95); padding: 30px; border-radius: 20px; border-top: 5px solid #f59e0b; color: white; }}
    .mini-side-card {{ background: rgba(30, 30, 30, 0.8); padding: 10px; border-radius: 10px; border-right: 4px solid #f59e0b; margin-bottom: 8px; color: #f59e0b; font-size: 13px; font-weight: bold; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 18px; margin-top: 20px; }}
    .val-white {{ color: white; font-size: 20px; margin-bottom: 10px; }}
    
    .auth-card .stButton button {{ background-color: #000 !important; color: #f59e0b !important; border: 2px solid #f59e0b !important; font-weight: 900 !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. AUTHENTICATION PAGE ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>منصة معلوماتي العقارية</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.markdown("<div class='lock-gold'>🔒</div>", unsafe_allow_html=True)
    
    t_login, t_register = st.tabs(["تسجيل الدخول", "طلب اشتراك"])
    
    with t_login:
        st.write("")
        u_in = st.text_input("Username", placeholder="اسم المستخدم", label_visibility="collapsed", key="log_u")
        p_in = st.text_input("Password", type="password", placeholder="كلمة المرور", label_visibility="collapsed", key="log_p")
        if st.button("دخول الآن", use_container_width=True):
            if check_auth(u_in, p_in):
                st.session_state.auth = True; st.rerun()
            else: st.error("بيانات الدخول غير صحيحة")
                
    with t_register:
        st.write("")
        st.text_input("Name", placeholder="الاسم الكامل", label_visibility="collapsed", key="reg_n")
        st.text_input("WhatsApp", placeholder="رقم الواتساب", label_visibility="collapsed", key="reg_w")
        st.text_input("Company", placeholder="اسم الشركة", label_visibility="collapsed", key="reg_c")
        if st.button("إرسال طلب الانضمام", use_container_width=True): st.success("تم إرسال طلبك بنجاح")
            
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 7. MAIN APP ---
else:
    @st.cache_data(ttl=60)
    def load_all_data():
        URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
        URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
        URL_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
        try:
            p, d, l = pd.read_csv(URL_P), pd.read_csv(URL_D), pd.read_csv(URL_L)
            for df in [p, d, l]: df.columns = [c.strip() for c in df.columns]
            return p.fillna("---"), d.fillna("---"), l.fillna("---")
        except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    df_p, df_d, df_l = load_all_data()

    st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900;">MA3LOMATI</h1></div>', unsafe_allow_html=True)

    c_menu, c_lang, c_out = st.columns([0.7, 0.15, 0.15])
    with c_menu:
        # القائمة تفتح افتراضياً على Launches (Index 4)
        menu_selection = option_menu(None, L["menu"], default_index=4, orientation="horizontal",
            styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
        
        if menu_selection != st.session_state.last_menu:
            st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu_selection
            st.rerun()

    with c_lang:
        if st.button("🌐 EN/AR", use_container_width=True):
            st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()
    with c_out:
        if st.button(f"🚪 {L['logout']}", use_container_width=True): st.session_state.auth = False; st.rerun()

    # --- logic عرض الصفحات ---
    if menu_selection == "Tools":
        st.markdown(f"<h2 style='color:#f59e0b; text-align:center;'>⚒️ {L['tool_title']}</h2>", unsafe_allow_html=True)
        t1, t2, t3 = st.columns(3)
        with t1:
            with st.container(border=True):
                st.subheader("🧮 Mortgage / القسط")
                p_val = st.number_input("Amount", 0, key="t1_p")
                y_val = st.number_input("Years", 1, 20, 7)
                if p_val > 0: st.warning(f"Monthly: {p_val/(y_val*12):,.2f}")
        # (باقي كود الأدوات كما هو...)

    elif menu_selection == "AI Assistant":
        st.markdown(f"<div class='tool-card'><h3>🤖 MA3LOMATI AI</h3><p>{L['ai_welcome']}</p></div>", unsafe_allow_html=True)
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.write(m["content"])
        if prompt := st.chat_input("Ask about market trends..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": f"Analyzing..."})
            st.rerun()

    else:
        is_launch = menu_selection == "Launches"
        if menu_selection == "Projects": 
            active_df, col_main_name = df_p, 'Project Name' if 'Project Name' in df_p.columns else df_p.columns[0]
        elif is_launch: 
            active_df, col_main_name = df_l, 'Project' if 'Project' in df_l.columns else df_l.columns[0]
        else: 
            active_df, col_main_name = df_d, 'Developer' if 'Developer' in df_d.columns else df_d.columns[0]

        if st.session_state.view == "details":
            item = active_df.iloc[st.session_state.current_index]
            if st.button(L["back"], use_container_width=True): st.session_state.view = "grid"; st.rerun()
            # (عرض التفاصيل...)
        else:
            search = st.text_input(L["search"])
            filtered = active_df[active_df[col_main_name].astype(str).str.contains(search, case=False)] if search else active_df
            start_idx = st.session_state.page_num * ITEMS_PER_PAGE
            display_df = filtered.iloc[start_idx : start_idx + ITEMS_PER_PAGE]

            if is_launch:
                grid = st.columns(3)
                for i, (orig_idx, r) in enumerate(display_df.iterrows()):
                    with grid[i % 3]:
                        if st.button(f"🚀 {r[col_main_name]}\n📍 {r.get('Area','---')}\n🏢 {r.get('Developer','---')}", key=f"card_{orig_idx}"):
                            st.session_state.current_index, st.session_state.view = orig_idx, "details"; st.rerun()
            else:
                c_main, c_side = st.columns([0.8, 0.2])
                with c_main:
                    grid = st.columns(2)
                    for i, (orig_idx, r) in enumerate(display_df.iterrows()):
                        with grid[i % 2]:
                            if st.button(f"✨ {r[col_main_name]}\n📍 {r.get('Area','---')}\n🏢 {r.get('Developer','---')}", key=f"card_{orig_idx}"):
                                st.session_state.current_index, st.session_state.view = orig_idx, "details"; st.rerun()
                with c_side:
                    st.markdown(f"<p style='color:#f59e0b; font-weight:bold; font-size:14px;'>{L['side_dev'] if menu_selection=='Developers' else L['side_proj']}</p>", unsafe_allow_html=True)
                    for _, s in active_df.head(6).iterrows():
                        st.markdown(f"<div class='mini-side-card'>💎 {s[col_main_name][:20]}</div>", unsafe_allow_html=True)

            st.write("---")
            # (نظام التنقل بين الصفحات...)

    st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
