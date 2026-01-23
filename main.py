import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CONSTANTS & LINKS ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
# رابط شيت المستخدمين الذي أرسلته
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
ITEMS_PER_PAGE = 6

# --- 2. Session State Initialization ---
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
        # مطابقة الاسم وكلمة المرور بناءً على الأعمدة التي ذكرتها
        match = df_users[(df_users['Name'].astype(str).str.strip() == u_val) & 
                         (df_users['Password'].astype(str).str.strip() == p_val)]
        return not match.empty
    except Exception as e:
        st.error("خطأ في الاتصال بقاعدة البيانات. تأكد من أعمدة Name و Password")
        return False

# --- 4. Translations ---
trans = {
    "EN": {
        "login_h": "PLATFORM ACCESS", "user": "Name", "pass": "Password", "login_btn": "Sign In", "lang_toggle": "العربية",
        "logout": "Logout", "back": "🏠 Back to List",
        "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "side_proj": "🏠 READY UNITS", "search": "Search assets...",
        "det_title": "Project Details", "ai_welcome": "How can I help you today?",
        "tool_title": "Professional Broker Tools", "next": "Next ➡", "prev": "⬅ Prev"
    },
    "AR": {
        "login_h": "بوابة دخول المحترفين", "user": "الاسم", "pass": "كلمة المرور", "login_btn": "تسجيل الدخول", "lang_toggle": "English",
        "logout": "خروج", "back": "🏠 العودة للقائمة",
        "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "side_proj": "🏠 استلام فوري", "search": "بحث عن عقار...",
        "det_title": "تفاصيل المشروع", "ai_welcome": "كيف يمكنني مساعدتك اليوم؟",
        "tool_title": "أدوات البروكر المحترف", "next": "التالي ➡", "prev": "⬅ السابق"
    }
}
L = trans[st.session_state.lang]
direction = "rtl" if st.session_state.lang == "AR" else "ltr"

# --- 5. Luxury CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {direction} !important; text-align: {"right" if direction=="rtl" else "left"} !important; 
        font-family: 'Cairo', sans-serif;
    }}
    .login-container {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(20px);
        padding: 50px; border-radius: 35px; border: 1px solid rgba(245, 158, 11, 0.3);
        max-width: 450px; margin: 80px auto; text-align: center; box-shadow: 0 30px 60px rgba(0,0,0,0.6);
    }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{HEADER_IMG}');
        background-size: cover; background-position: center;
        border-bottom: 2px solid #f59e0b; padding: 40px; text-align: center;
        border-radius: 0 0 50px 50px; margin-bottom: 30px;
    }}
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; color: white !important;
        border-left: 5px solid #f59e0b !important; border-radius: 15px !important;
        height: 180px !important; width: 100% !important; font-size: 16px !important;
    }}
    .mini-side-card {{
        background: rgba(40, 40, 40, 0.8); padding: 10px; border-radius: 10px;
        border-right: 4px solid #f59e0b; margin-bottom: 8px; color: #f59e0b; font-size: 13px; font-weight: bold;
    }}
    .detail-card, .tool-card {{
        background: rgba(20, 20, 20, 0.95); padding: 30px; border-radius: 20px;
        border-top: 5px solid #f59e0b; margin-top: 10px; color: white;
    }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 17px; margin-top: 10px; }}
    .val-white {{ color: white; font-size: 18px; margin-bottom: 5px; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. Flow Control ---

if not st.session_state.auth:
    # --- صفحة تسجيل الدخول ---
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='color:#f59e0b; font-size:45px; letter-spacing:2px;'>MA3LOMATI</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#aaa; margin-bottom:30px;'>{L['login_h']}</p>", unsafe_allow_html=True)
    
    u_name = st.text_input(L["user"], placeholder="Enter Name")
    u_pass = st.text_input(L["pass"], type="password", placeholder="Enter Password")
    
    st.write("")
    if st.button(L["login_btn"], use_container_width=True, type="primary"):
        if check_auth(u_name, u_pass):
            st.session_state.auth = True; st.rerun()
        else:
            st.error("Access Denied / الاسم أو الرقم السري خطأ")
            
    if st.button(L["lang_toggle"], use_container_width=True):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 7. Main Platform (After Login) ---
else:
    @st.cache_data(ttl=60)
    def load_platform_data():
        # روابط الشيتات الخاصة بالمشاريع والمطورين (الروابط الأصلية للمنصة)
        p = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv")
        d = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv")
        l = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")

    df_p, df_d, df_l = load_platform_data()

    st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900;">MA3LOMATI</h1></div>', unsafe_allow_html=True)

    # شريط التنقل
    c_nav, c_out = st.columns([0.85, 0.15])
    with c_nav:
        menu_selection = option_menu(None, L["menu"], default_index=2, orientation="horizontal",
            styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
        if menu_selection != st.session_state.last_menu:
            st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu_selection
            st.rerun()
    with c_out:
        if st.button(f"🚪 {L['logout']}", use_container_width=True):
            st.session_state.auth = False; st.rerun()

    # --- منطق الأقسام ---
    if menu_selection in ["Tools", "الأدوات"]:
        st.markdown(f"<div class='tool-card'><h2 style='text-align:center; color:#f59e0b;'>⚒️ {L['tool_title']}</h2></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("🧮 Mortgage")
            p_val = st.number_input("Property Value", 0)
            y_val = st.number_input("Years", 1, 30, 10)
            if p_val > 0: st.info(f"Monthly: {p_val/(y_val*12):,.0f}")
        with col2:
            st.subheader("📈 ROI")
            cost = st.number_input("Cost", 1); rent = st.number_input("Annual Rent", 0)
            st.success(f"ROI: {(rent/cost)*100:.2f}%")
        with col3:
            st.subheader("📏 Area")
            sqm = st.number_input("SQM", 0.0)
            st.warning(f"SQFT: {sqm * 10.764:.1f}")

    elif menu_selection in ["AI Assistant", "المساعد الذكي"]:
        st.markdown(f"<div class='detail-card'><h3>🤖 AI Advisor</h3><p>{L['ai_welcome']}</p></div>", unsafe_allow_html=True)
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]): st.write(msg["content"])
        if prompt := st.chat_input("Type your question..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": f"Consulting data for: {prompt}"})
            st.rerun()

    else:
        # عرض المشاريع / المطورين / اللونشات
        is_l = menu_selection in ["Launches", "اللونشات"]
        if menu_selection in ["Projects", "المشاريع"]: active_df = df_p
        elif is_l: active_df = df_l
        else: active_df = df_d

        if st.session_state.view == "details":
            # عرض التفاصيل
            item = active_df.iloc[st.session_state.current_index]
            if st.button(L["back"], use_container_width=True): st.session_state.view = "grid"; st.rerun()
            st.markdown(f"<div class='detail-card'><h2>{item[0]}</h2></div>", unsafe_allow_html=True)
            cols = active_df.columns
            c1, c2 = st.columns(2)
            for i, c in enumerate(cols):
                with (c1 if i % 2 == 0 else c2):
                    st.markdown(f"<p class='label-gold'>{c}</p><p class='val-white'>{item[c]}</p>", unsafe_allow_html=True)
        else:
            # عرض الشبكة
            search = st.text_input(L["search"])
            filtered = active_df[active_df.iloc[:,0].astype(str).str.contains(search, case=False)]
            start_idx = st.session_state.page_num * ITEMS_PER_PAGE
            display_df = filtered.iloc[start_idx : start_idx + ITEMS_PER_PAGE]

            main_col, side_col = st.columns([0.8, 0.2])
            with main_col:
                grid = st.columns(2)
                for i, (idx, row) in enumerate(display_df.iterrows()):
                    with grid[i % 2]:
                        if st.button(f"✨ {row[0]}\n📍 {row.get('Area','---')}", key=f"card_{idx}"):
                            st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()
            with side_col:
                st.markdown(f"<p style='color:#f59e0b;'>{L['side_proj']}</p>", unsafe_allow_html=True)
                for _, s in active_df.head(6).iterrows():
                    st.markdown(f"<div class='mini-side-card'>💎 {s[0][:22]}</div>", unsafe_allow_html=True)

            st.write("---")
            nav1, nav2 = st.columns(2)
            with nav1:
                if st.session_state.page_num > 0:
                    if st.button(L["prev"], use_container_width=True): st.session_state.page_num -= 1; st.rerun()
            with nav2:
                if (start_idx + ITEMS_PER_PAGE) < len(filtered):
                    if st.button(L["next"], use_container_width=True): st.session_state.page_num += 1; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
