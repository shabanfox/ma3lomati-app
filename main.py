import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CONSTANTS & LINKS ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# رابط شيت المستخدمين (يرجى التأكد من وجود أعمدة: Username, Password)
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1849129596&single=true&output=csv"

# --- 2. Session State Initialization ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'view' not in st.session_state: st.session_state.view = "grid" 
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'last_menu' not in st.session_state: st.session_state.last_menu = "Projects"
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 3. Authentication Logic ---
def check_login(u, p):
    try:
        df_users = pd.read_csv(USER_SHEET_URL)
        # التأكد من مطابقة اسم المستخدم وكلمة المرور
        user_match = df_users[(df_users['Username'].astype(str) == u) & (df_users['Password'].astype(str) == p)]
        return not user_match.empty
    except:
        return False

# --- 4. Translations ---
trans = {
    "EN": {
        "login_title": "Broker Access", "user": "Username", "pass": "Password", "login_btn": "Sign In",
        "logout": "Logout", "back": "🏠 Back to List",
        "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "side_dev": "⭐ TOP DEVS", "side_proj": "🏠 READY", "search": "Search assets...",
        "tool_title": "Professional Broker Tools", "next": "Next ➡", "prev": "⬅ Prev"
    },
    "AR": {
        "login_title": "دخول المحترفين", "user": "اسم المستخدم", "pass": "كلمة المرور", "login_btn": "دخول",
        "logout": "خروج", "back": "🏠 العودة للقائمة",
        "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "side_dev": "⭐ المطورين", "side_proj": "🏠 استلام فوري", "search": "بحث عن عقار...",
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
        background: linear-gradient(rgba(0,0,0,0.97), rgba(0,0,0,0.97)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {direction} !important; text-align: {"right" if direction=="rtl" else "left"} !important; 
        font-family: 'Cairo', sans-serif;
    }}
    .login-box {{
        background: rgba(20, 20, 20, 0.9); padding: 40px; border-radius: 20px;
        border: 2px solid #f59e0b; max-width: 400px; margin: 100px auto; text-align: center;
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
        height: 200px !important; width: 100% !important; text-align: { "right" if direction=="rtl" else "left" } !important;
    }}
    .mini-side-card {{
        background: rgba(30, 30, 30, 0.8); padding: 10px; border-radius: 10px;
        border: 1px solid #444; border-right: 4px solid #f59e0b; margin-bottom: 8px; 
        color: #f59e0b; font-size: 13px; font-weight: bold;
    }}
    .detail-card, .tool-card {{
        background: rgba(20, 20, 20, 0.95); padding: 30px; border-radius: 20px;
        border: 1px solid #333; border-top: 5px solid #f59e0b; margin-top: 10px; color: white;
    }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 18px; }}
    .val-white {{ color: white; font-size: 20px; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. PAGE ROUTING ---

# أ- صفحة تسجيل الدخول
if not st.session_state.auth:
    st.markdown(f"<div class='login-box'>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='color:#f59e0b;'>MA3LOMATI</h1><h3 style='color:white;'>{L['login_title']}</h3>", unsafe_allow_html=True)
    user = st.text_input(L["user"])
    pw = st.text_input(L["pass"], type="password")
    
    col_l, col_r = st.columns(2)
    with col_l:
        if st.button(L["login_btn"], use_container_width=True):
            if check_login(user, pw):
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid Credentials / بيانات خطأ")
    with col_r:
        if st.button("🌐 EN/AR", use_container_width=True):
            st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"
            st.rerun()
    
    st.markdown("<p style='color:#555; margin-top:20px;'>Contact admin for registration</p></div>", unsafe_allow_html=True)
    st.stop()

# ب- المنصة الرئيسية (تظهر فقط بعد الـ Auth)
else:
    # (كود تحميل البيانات)
    @st.cache_data(ttl=60)
    def load_all_data():
        URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
        URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
        URL_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
        try:
            p, d, l = pd.read_csv(URL_P), pd.read_csv(URL_D), pd.read_csv(URL_L)
            return p.fillna("---"), d.fillna("---"), l.fillna("---")
        except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    df_p, df_d, df_l = load_all_data()

    st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900;">MA3LOMATI</h1></div>', unsafe_allow_html=True)

    c_menu, c_lang, c_out = st.columns([0.7, 0.15, 0.15])
    with c_menu:
        menu_selection = option_menu(None, L["menu"], default_index=2, orientation="horizontal",
            styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
        if menu_selection != st.session_state.last_menu:
            st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu_selection
            st.rerun()

    with c_lang:
        if st.button("🌐 EN/AR", use_container_width=True):
            st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()
    with c_out:
        if st.button(f"🚪 {L['logout']}", use_container_width=True): st.session_state.auth = False; st.rerun()

    # --- تكملة كود عرض البيانات (نفس الكود السابق مع الاستلامات المصغرة) ---
    # [هنا نضع بقية منطق العرض Logic View الذي قمنا ببرمجته سابقاً]
    # ... (Logic الخاص بالـ Tools و AI Assistant و Projects)
    # ملاحظة: تم وضع `st.stop()` في صفحة الدخول لضمان عدم تنفيذ أي كود بالأسفل إلا للمسجلين.

    # الجزء الخاص بعرض المشاريع والبحث (مثال سريع لضمان عمل الكود)
    is_launch = menu_selection in ["Launches", "اللونشات"]
    if menu_selection in ["Projects", "المشاريع"]: active_df = df_p
    elif is_launch: active_df = df_l
    else: active_df = df_d
    
    col_main_name = active_df.columns[0]
    search = st.text_input(L["search"])
    filtered = active_df[active_df[col_main_name].astype(str).str.contains(search, case=False)] if search else active_df
    start_idx = st.session_state.page_num * ITEMS_PER_PAGE
    display_df = filtered.iloc[start_idx : start_idx + ITEMS_PER_PAGE]

    c_main, c_side = st.columns([0.8, 0.2])
    with c_main:
        grid = st.columns(2)
        for i, (orig_idx, r) in enumerate(display_df.iterrows()):
            with grid[i % 2]:
                if st.button(f"✨ {r[0]}\n📍 {r.get('Area','---')}", key=f"card_{orig_idx}"):
                    pass # الانتقال للتفاصيل
    with c_side:
        st.markdown(f"<p style='color:#f59e0b; font-weight:bold;'>{L['side_proj']}</p>", unsafe_allow_html=True)
        for _, s in active_df.head(6).iterrows():
            st.markdown(f"<div class='mini-side-card'>💎 {s[0][:20]}</div>", unsafe_allow_html=True)

    # أزرار التنقل
    st.write("---")
    nav1, nav2 = st.columns(2)
    with nav1:
        if st.session_state.page_num > 0:
            if st.button(L["prev"], use_container_width=True): st.session_state.page_num -= 1; st.rerun()
    with nav2:
        if (start_idx + ITEMS_PER_PAGE) < len(filtered):
            if st.button(L["next"], use_container_width=True): st.session_state.page_num += 1; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
