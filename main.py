import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CONSTANTS & LINKS ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# رابط الشيت الذي أرسلته (المنشور كـ CSV)
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
        # قراءة شيت المستخدمين
        df_users = pd.read_csv(USER_SHEET_URL)
        df_users.columns = [c.strip() for c in df_users.columns]
        
        u_val = str(u).strip()
        p_val = str(p).strip()
        
        # التأكد من مطابقة الاسم والرقم السري في الشيت
        if 'Name' in df_users.columns and 'Password' in df_users.columns:
            match = df_users[(df_users['Name'].astype(str).str.strip() == u_val) & 
                             (df_users['Password'].astype(str).str.strip() == p_val)]
            return not match.empty
        return False
    except:
        return False

# --- 4. Translations ---
trans = {
    "EN": {
        "login_h": "PLATFORM ACCESS", "user": "Name", "pass": "Password", "login_btn": "Sign In", "lang_toggle": "العربية",
        "logout": "Logout", "back": "🏠 Back to List",
        "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "side_dev": "⭐ TOP DEVS", "side_proj": "🏠 READY", "search": "Search assets...",
        "det_title": "Project Specifications", "ai_welcome": "How can I help you today?",
        "tool_title": "Professional Broker Tools", "next": "Next ➡", "prev": "⬅ Prev"
    },
    "AR": {
        "login_h": "بوابة دخول المحترفين", "user": "الاسم", "pass": "كلمة المرور", "login_btn": "تسجيل الدخول", "lang_toggle": "English",
        "logout": "خروج", "back": "🏠 العودة للقائمة",
        "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "side_dev": "⭐ المطورين", "side_proj": "🏠 استلام فوري", "search": "بحث عن عقار...",
        "det_title": "مواصفات وتفاصيل المشروع", "ai_welcome": "كيف يمكنني مساعدتك اليوم؟",
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
        background: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {direction} !important; text-align: {"right" if direction=="rtl" else "left"} !important; 
        font-family: 'Cairo', sans-serif;
    }}
    .login-container {{
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
        padding: 50px; border-radius: 30px; border: 1px solid rgba(245, 158, 11, 0.3);
        max-width: 450px; margin: 80px auto; text-align: center; box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }}
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
        font-size: 16px !important; line-height: 1.6 !important;
    }}
    .detail-card, .tool-card {{
        background: rgba(20, 20, 20, 0.95); padding: 30px; border-radius: 20px;
        border: 1px solid #333; border-top: 5px solid #f59e0b; margin-top: 10px; color: white;
    }}
    .mini-side-card {{
        background: rgba(30, 30, 30, 0.8); padding: 10px; border-radius: 10px;
        border-right: 4px solid #f59e0b; margin-bottom: 8px; color: #f59e0b; font-size: 13px; font-weight: bold;
    }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 18px; margin-top: 20px; }}
    .val-white {{ color: white; font-size: 20px; margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. Flow Control (Login Logic) ---
if not st.session_state.auth:
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='color:#f59e0b; font-size:42px;'>MA3LOMATI</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#aaa; margin-bottom:30px;'>{L['login_h']}</p>", unsafe_allow_html=True)
    
    u_input = st.text_input(L["user"], placeholder="Enter Name")
    p_input = st.text_input(L["pass"], type="password", placeholder="Enter Password")
    
    if st.button(L["login_btn"], use_container_width=True, type="primary"):
        if check_auth(u_input, p_input):
            st.session_state.auth = True; st.rerun()
        else:
            st.error("Access Denied / الاسم أو كلمة المرور خطأ")
    
    if st.button(L["lang_toggle"], use_container_width=True):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 7. Main Platform (After Success Login) ---
else:
    @st.cache_data(ttl=60)
    def load_all_data():
        # روابط بيانات المشاريع (تأكد أنها منشورة كـ CSV أيضاً)
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

    c_menu, c_out = st.columns([0.85, 0.15])
    with c_menu:
        menu_selection = option_menu(None, L["menu"], default_index=2, orientation="horizontal",
            styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
        if menu_selection != st.session_state.last_menu:
            st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu_selection
            st.rerun()
    with c_out:
        if st.button(f"🚪 {L['logout']}", use_container_width=True):
            st.session_state.auth = False; st.rerun()

    # --- View Logic ---
    if menu_selection in ["Tools", "الأدوات"]:
        st.markdown(f"<h2 style='color:#f59e0b; text-align:center;'>⚒️ {L['tool_title']}</h2>", unsafe_allow_html=True)
        t1, t2, t3 = st.columns(3)
        with t1:
            with st.container(border=True):
                st.subheader("🧮 Mortgage")
                p_v = st.number_input("Amount", 0); y_v = st.number_input("Years", 1, 20, 7)
                if p_v > 0: st.warning(f"Monthly: {p_v/(y_v*12):,.2f}")
        with t2:
            with st.container(border=True):
                st.subheader("📈 ROI")
                c_v = st.number_input("Cost", 1); r_v = st.number_input("Rent", 0)
                st.warning(f"ROI: {(r_v/c_v)*100:.2f}%")
        with t3:
            with st.container(border=True):
                st.subheader("🌍 Currency")
                u_v = st.number_input("USD Amount", 0.0); rate_v = st.number_input("Rate", 40.0, 70.0, 50.0)
                st.warning(f"EGP: {u_v*rate_v:,.2f}")

    elif menu_selection in ["AI Assistant", "المساعد الذكي"]:
        st.markdown(f"<div class='tool-card'><h3>🤖 AI Advisor</h3><p>{L['ai_welcome']}</p></div>", unsafe_allow_html=True)
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.write(m["content"])
        if prompt := st.chat_input("Ask me something..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": f"Analyzing: {prompt}..."})
            st.rerun()

    else:
        is_launch = menu_selection in ["Launches", "اللونشات"]
        if menu_selection in ["Projects", "المشاريع"]: active_df, col_main = df_p, df_p.columns[0]
        elif is_launch: active_df, col_main = df_l, df_l.columns[0]
        else: active_df, col_main = df_d, df_d.columns[0]

        if st.session_state.view == "details":
            item = active_df.iloc[st.session_state.current_index]
            if st.button(L["back"], use_container_width=True): st.session_state.view = "grid"; st.rerun()
            c1, c2, c3 = st.columns(3)
            cols = active_df.columns
            split = max(1, len(cols) // 3)
            for i, chunk in enumerate([cols[:split], cols[split:split*2], cols[split*2:]]):
                with [c1, c2, c3][i]:
                    h = f'<div class="detail-card">'
                    for k in chunk: h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                    st.markdown(h+'</div>', unsafe_allow_html=True)
        else:
            search = st.text_input(L["search"])
            filtered = active_df[active_df[col_main].astype(str).str.contains(search, case=False)]
            start_idx = st.session_state.page_num * ITEMS_PER_PAGE
            display_df = filtered.iloc[start_idx : start_idx + ITEMS_PER_PAGE]

            c_main, c_side = st.columns([0.8, 0.2])
            with c_main:
                grid = st.columns(2)
                for i, (orig_idx, r) in enumerate(display_df.iterrows()):
                    with grid[i % 2]:
                        if st.button(f"✨ {r[col_main]}\n📍 {r.get('Area','---')}\n🏢 {r.get('Developer','---')}", key=f"card_{orig_idx}"):
                            st.session_state.current_index, st.session_state.view = orig_idx, "details"; st.rerun()
            with c_side:
                st.markdown(f"<p style='color:#f59e0b; font-weight:bold;'>{L['side_proj']}</p>", unsafe_allow_html=True)
                for _, s in active_df.head(6).iterrows():
                    st.markdown(f"<div class='mini-side-card'>💎 {s[col_main][:20]}</div>", unsafe_allow_html=True)

            st.write("---")
            b1, b2 = st.columns(2)
            if st.session_state.page_num > 0:
                with b1:
                    if st.button(L["prev"], use_container_width=True): st.session_state.page_num -= 1; st.rerun()
            if (start_idx + ITEMS_PER_PAGE) < len(filtered):
                with b2:
                    if st.button(L["next"], use_container_width=True): st.session_state.page_num += 1; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
