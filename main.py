import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CONSTANTS & LINKS ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# الرابط الجديد الذي أرسلته
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
ITEMS_PER_PAGE = 6

# --- 2. Session State Initialization ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'view' not in st.session_state: st.session_state.view = "grid" 
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'last_menu' not in st.session_state: st.session_state.last_menu = "Projects"

# --- 3. Authentication Logic ---
def check_auth(u, p):
    try:
        # قراءة الشيت مع إلغاء الكاش لضمان التحديث اللحظي
        df_users = pd.read_csv(USER_SHEET_URL)
        df_users.columns = [c.strip() for c in df_users.columns]
        
        u_val = str(u).strip()
        p_val = str(p).strip()
        
        # البحث عن تطابق (يفترض وجود أعمدة Username و Password)
        match = df_users[(df_users['Username'].astype(str).str.strip() == u_val) & 
                         (df_users['Password'].astype(str).str.strip() == p_val)]
        return not match.empty
    except Exception as e:
        st.error(f"⚠️ خطأ في الاتصال: تأكد من تسمية الأعمدة Username و Password")
        return False

# --- 4. Translations ---
trans = {
    "EN": {
        "login_h": "PLATFORM ACCESS", "user": "Username", "pass": "Password", "login_btn": "Sign In",
        "logout": "Logout", "back": "🏠 Back", "search": "Search assets...",
        "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "side_proj": "🏠 READY UNITS", "next": "Next ➡", "prev": "⬅ Prev", "lang_toggle": "العربية"
    },
    "AR": {
        "login_h": "بوابة دخول المحترفين", "user": "اسم المستخدم", "pass": "كلمة المرور", "login_btn": "تسجيل الدخول",
        "logout": "خروج", "back": "🏠 عودة", "search": "بحث عن عقار...",
        "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "side_proj": "🏠 استلام فوري", "next": "التالي ➡", "prev": "⬅ السابق", "lang_toggle": "English"
    }
}
L = trans[st.session_state.lang]
dir_attr = "rtl" if st.session_state.lang == "AR" else "ltr"

# --- 5. Luxury CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {dir_attr} !important; font-family: 'Cairo', sans-serif;
    }}

    /* صفحة تسجيل الدخول الزجاجية */
    .login-container {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        padding: 50px; border-radius: 30px;
        border: 1px solid rgba(245, 158, 11, 0.3);
        max-width: 450px; margin: 80px auto; text-align: center;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }}
    
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('{HEADER_IMG}');
        background-size: cover; background-position: center;
        border-bottom: 3px solid #f59e0b; padding: 40px; text-align: center;
        border-radius: 0 0 50px 50px; margin-bottom: 30px;
    }}

    div.stButton > button[key*="card_"] {{
        background: rgba(35, 35, 35, 0.9) !important; color: white !important;
        border-left: 6px solid #f59e0b !important; height: 180px !important;
        text-align: {"right" if dir_attr=="rtl" else "left"} !important; font-size: 16px !important;
    }}

    .mini-side-card {{
        background: rgba(40, 40, 40, 0.8); padding: 10px; border-radius: 10px;
        border-right: 4px solid #f59e0b; margin-bottom: 8px; color: #f59e0b; font-size: 13px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 6. Flow Control ---

if not st.session_state.auth:
    # عرض صفحة تسجيل الدخول فقط
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='color:#f59e0b; font-size:42px; margin-bottom:0;'>MA3LOMATI</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#aaa; margin-bottom:30px;'>{L['login_h']}</p>", unsafe_allow_html=True)
    
    user_in = st.text_input(L["user"], placeholder="User...")
    pass_in = st.text_input(L["pass"], type="password", placeholder="Pass...")
    
    st.write("")
    if st.button(L["login_btn"], use_container_width=True, type="primary"):
        if check_auth(user_in, pass_in):
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("❌ " + ("بيانات غير صحيحة" if st.session_state.lang=="AR" else "Invalid Login"))
    
    if st.button(L["lang_toggle"], use_container_width=True):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

else:
    # المحتوى الداخلي للمنصة بعد تسجيل الدخول
    @st.cache_data(ttl=60)
    def load_main_data():
        # روابط بيانات المشاريع (المستخدمة مسبقاً)
        p = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv")
        d = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv")
        l = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")

    df_p, df_d, df_l = load_main_data()

    st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900;">MA3LOMATI</h1></div>', unsafe_allow_html=True)

    # المنيو بدون زر لغة
    c_nav, c_out = st.columns([0.88, 0.12])
    with c_nav:
        menu_selection = option_menu(None, L["menu"], default_index=2, orientation="horizontal",
            styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
    with c_out:
        if st.button(f"🚪 {L['logout']}", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # تحديد الشيت النشط
    if menu_selection in ["Projects", "المشاريع"]: active_df = df_p
    elif menu_selection in ["Launches", "اللونشات"]: active_df = df_l
    else: active_df = df_d

    col_main = active_df.columns[0]
    search = st.text_input(L["search"])
    filtered = active_df[active_df[col_main].astype(str).str.contains(search, case=False)]
    start = st.session_state.page_num * ITEMS_PER_PAGE
    display_df = filtered.iloc[start : start + ITEMS_PER_PAGE]

    # العرض الرئيسي مع الجانب المصغر
    c_main, c_side = st.columns([0.8, 0.2])
    with c_main:
        grid = st.columns(2)
        for i, (idx, r) in enumerate(display_df.iterrows()):
            with grid[i % 2]:
                if st.button(f"✨ {r[0]}\n📍 {r.get('Area','---')}\n🏢 {r.get('Developer','---')}", key=f"card_{idx}"):
                    pass # سيتم فتح التفاصيل هنا
    with c_side:
        st.markdown(f"<p style='color:#f59e0b; font-weight:bold;'>{L['side_proj']}</p>", unsafe_allow_html=True)
        for _, s in active_df.head(6).iterrows():
            st.markdown(f"<div class='mini-side-card'>💎 {s[0][:22]}</div>", unsafe_allow_html=True)

    # التنقل
    st.write("---")
    b1, b2 = st.columns(2)
    with b1:
        if st.session_state.page_num > 0:
            if st.button(L["prev"], use_container_width=True): st.session_state.page_num -= 1; st.rerun()
    with b2:
        if (start + ITEMS_PER_PAGE) < len(filtered):
            if st.button(L["next"], use_container_width=True): st.session_state.page_num += 1; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
