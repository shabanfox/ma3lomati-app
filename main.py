import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- الثوابت والروابط ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# رابط شيت المستخدمين الخاص بك (تم ربطه)
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1849129596&single=true&output=csv"
ITEMS_PER_PAGE = 6

# --- 2. إدارة الجلسة (Session State) ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'view' not in st.session_state: st.session_state.view = "grid" 
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'last_menu' not in st.session_state: st.session_state.last_menu = "Projects"

# --- 3. دالة التحقق من الدخول ---
def check_auth(username, password):
    try:
        df_users = pd.read_csv(USER_SHEET_URL)
        # التأكد من وجود أعمدة باسم Username و Password في الشيت
        match = df_users[(df_users['Username'].astype(str) == str(username)) & 
                         (df_users['Password'].astype(str) == str(password))]
        return not match.empty
    except Exception as e:
        st.error(f"Error connecting to users database: {e}")
        return False

# --- 4. القاموس والترجمة ---
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

# --- 5. تنسيقات CSS الفاخرة ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {dir_attr} !important; font-family: 'Cairo', sans-serif;
    }}

    /* تصميم صفحة الدخول الزجاجي */
    .login-container {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        padding: 60px 40px; border-radius: 35px;
        border: 1px solid rgba(245, 158, 11, 0.2);
        box-shadow: 0 30px 60px rgba(0,0,0,0.7);
        max-width: 450px; margin: 100px auto; text-align: center;
    }}
    
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('{HEADER_IMG}');
        background-size: cover; background-position: center;
        border-bottom: 3px solid #f59e0b; padding: 50px 20px; text-align: center;
        border-radius: 0 0 50px 50px; margin-bottom: 30px;
    }}

    /* أزرار الكروت الكبيرة (لم تتغير) */
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; color: white !important;
        border-left: 6px solid #f59e0b !important; height: 180px !important;
        text-align: {"right" if dir_attr=="rtl" else "left"} !important; font-size: 17px !important;
    }}

    .mini-side-card {{
        background: rgba(40, 40, 40, 0.8); padding: 12px; border-radius: 10px;
        border-right: 4px solid #f59e0b; margin-bottom: 10px; color: #f59e0b; font-size: 13px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 6. منطق العرض والتوجيه ---

# أ- صفحة تسجيل الدخول (التصميم الجديد)
if not st.session_state.auth:
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='color:#f59e0b; font-size:45px; margin-bottom:0; letter-spacing:2px;'>MA3LOMATI</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#888; margin-bottom:40px; font-weight:bold;'>{L['login_h']}</p>", unsafe_allow_html=True)
    
    u_input = st.text_input(L["user"], placeholder="Type Username...")
    p_input = st.text_input(L["pass"], type="password", placeholder="Type Password...")
    
    st.write("")
    if st.button(L["login_btn"], use_container_width=True, type="primary"):
        if check_auth(u_input, p_input):
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Access Denied / بيانات الدخول غير صحيحة")
    
    # تبديل اللغة حصري في صفحة الدخول كما طلبت
    if st.button(L["lang_toggle"], use_container_width=True):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"
        st.rerun()
        
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ب- المنصة الرئيسية (تفتح بعد تسجيل الدخول بنجاح)
else:
    @st.cache_data(ttl=60)
    def load_data():
        p = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv")
        d = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv")
        l = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")

    df_p, df_d, df_l = load_data()

    # الهيدر الملكي
    st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900;">MA3LOMATI</h1></div>', unsafe_allow_html=True)

    # شريط التنقل العلوي (تم إزالة زر اللغة منه)
    c_nav, c_out = st.columns([0.88, 0.12])
    with c_nav:
        menu_selection = option_menu(None, L["menu"], default_index=2, orientation="horizontal",
            styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
    with c_out:
        if st.button(f"🚪 {L['logout']}", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    # --- منطق عرض المحتوى (البحث، الكروت، الاستلام الفوري المصغر) ---
    if menu_selection in ["Projects", "المشاريع"]: active_df = df_p
    elif menu_selection in ["Launches", "اللونشات"]: active_df = df_l
    else: active_df = df_d

    col_n = active_df.columns[0]
    search_q = st.text_input(L["search"])
    filtered_df = active_df[active_df[col_n].astype(str).str.contains(search_q, case=False)]
    
    start_at = st.session_state.page_num * ITEMS_PER_PAGE
    display_df = filtered_df.iloc[start_at : start_at + ITEMS_PER_PAGE]

    # تقسيم الصفحة: الرئيسي والجانبي المصغر
    c_main, c_side = st.columns([0.8, 0.2])
    
    with c_main:
        grid = st.columns(2)
        for i, (idx, r) in enumerate(display_df.iterrows()):
            with grid[i % 2]:
                # الكروت الكبيرة الفخمة كما هي
                if st.button(f"✨ {r[0]}\n📍 {r.get('Area','---')}\n🏢 {r.get('Developer','---')}", key=f"card_{idx}"):
                    st.session_state.current_index, st.session_state.view = idx, "details"
    
    with c_side:
        st.markdown(f"<p style='color:#f59e0b; font-weight:bold;'>{L['side_proj']}</p>", unsafe_allow_html=True)
        for _, s in active_df.head(6).iterrows():
            st.markdown(f"<div class='mini-side-card'>💎 {s[0][:20]}</div>", unsafe_allow_html=True)

    # أزرار التنقل (السابق والتالي)
    st.write("---")
    b1, b2 = st.columns(2)
    with b1:
        if st.session_state.page_num > 0:
            if st.button(L["prev"], use_container_width=True): st.session_state.page_num -= 1; st.rerun()
    with b2:
        if (start_at + ITEMS_PER_PAGE) < len(filtered_df):
            if st.button(L["next"], use_container_width=True): st.session_state.page_num += 1; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
