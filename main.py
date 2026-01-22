
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CONSTANTS ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'view' not in st.session_state: st.session_state.view = "grid" 
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'last_menu' not in st.session_state: st.session_state.last_menu = "Projects"
if 'messages' not in st.session_state: st.session_state.messages = []

trans = {
    "EN": {
        "logout": "Logout", "back": "🏠 Back", "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "side_dev": "⭐ TOP DEVELOPERS", "side_proj": "🏠 READY TO MOVE", "search": "Search..."
    },
    "AR": {
        "logout": "خروج", "back": "🏠 عودة", "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "side_dev": "⭐ أفضل المطورين", "side_proj": "🏠 استلام فوري", "search": "بحث..."
    }
}
L = trans[st.session_state.lang]

# --- 3. Luxury CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.97), rgba(0,0,0,0.97)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {"rtl" if st.session_state.lang == "AR" else "ltr"} !important;
        font-family: 'Cairo', sans-serif;
    }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{HEADER_IMG}');
        background-size: cover; background-position: center;
        border-bottom: 2px solid #f59e0b; padding: 40px 20px; text-align: center;
        border-radius: 0 0 40px 40px; margin-bottom: 30px;
    }}
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; color: white !important;
        border-left: 5px solid #f59e0b !important; border-radius: 15px !important;
        height: 180px !important; width: 100% !important; text-align: right !important;
    }}
    .tool-card {{
        background: rgba(20, 20, 20, 0.95); padding: 20px; border-radius: 15px;
        border: 1px solid #333; border-top: 4px solid #f59e0b; margin-bottom: 15px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Data Loading ---
@st.cache_data(ttl=60)
def load_all():
    URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    URL_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(URL_P), pd.read_csv(URL_D), pd.read_csv(URL_L)
        for df in [p, d, l]: df.columns = [c.strip() for c in df.columns]
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_all()

# --- 5. Navigation ---
st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900;">MA3LOMATI</h1></div>', unsafe_allow_html=True)
c_menu, c_lang, c_out = st.columns([0.7, 0.15, 0.15])
with c_menu:
    menu = option_menu(None, L["menu"], default_index=2, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
    if menu != st.session_state.last_menu:
        st.session_state.view = "grid"; st.session_state.page_num = 0; st.session_state.last_menu = menu; st.rerun()

# --- 6. Content Logic ---

# A. TOOLS & AI (Same logic as before)
if menu in ["Tools", "الأدوات"]:
    st.title(f"⚒️ {L['menu'][0]}")
    t1, t2, t3 = st.columns(3)
    with t1:
        with st.container(border=True):
            p = st.number_input("Price", 0)
            if p > 0: st.write(f"Monthly: {p/(7*12):,.0f}")
    # ... بقية الأدوات (موجودة في الكود السابق)

elif menu in ["AI Assistant", "المساعد الذكي"]:
    st.chat_message("assistant").write("I am your AI assistant. How can I help?")
    if p := st.chat_input(): st.chat_message("user").write(p)

# B. DATA SECTIONS
else:
    # تحديد البيانات والعمود الرئيسي
    is_launch = menu in ["Launches", "اللونشات"]
    if is_launch:
        active_df, col_main = df_l, ('Project' if 'Project' in df_l.columns else df_l.columns[0])
    elif menu in ["Projects", "المشاريع"]:
        active_df, col_main = df_p, ('Project Name' if 'Project Name' in df_p.columns else df_p.columns[0])
    else:
        active_df, col_main = df_d, ('Developer' if 'Developer' in df_d.columns else df_d.columns[0])

    if st.session_state.view == "details":
        item = active_df.iloc[st.session_state.current_index]
        if st.button(L["back"]): st.session_state.view = "grid"; st.rerun()
        st.markdown(f"<div class='tool-card'><h2>{item[col_main]}</h2><p>{item.to_string()}</p></div>", unsafe_allow_html=True)
    else:
        search = st.text_input(L["search"])
        filtered = active_df[active_df[col_main].astype(str).str.contains(search, case=False)] if search else active_df
        start = st.session_state.page_num * ITEMS_PER_PAGE
        display_df = filtered.iloc[start : start + ITEMS_PER_PAGE]

        # --- الـ Logic الخاص بالعرض الكامل 100% ---
        if is_launch:
            # صفحة اللونشات: عرض كامل (بدون عمود جانبي)
            grid = st.columns(3) # عرض 3 كروت في الصف الواحد لأن المساحة 100%
            for i, (orig_idx, r) in enumerate(display_df.iterrows()):
                with grid[i % 3]:
                    if st.button(f"🚀 {r[col_main]}\n📍 {r.get('Area','---')}\n💰 Launching Now", key=f"card_{orig_idx}"):
                        st.session_state.current_index = orig_idx; st.session_state.view = "details"; st.rerun()
        else:
            # المشاريع والمطورين: تقسيم 70/30
            c_main, c_side = st.columns([0.7, 0.3])
            with c_main:
                grid = st.columns(2)
                for i, (orig_idx, r) in enumerate(display_df.iterrows()):
                    with grid[i % 2]:
                        if st.button(f"✨ {r[col_main]}\n📍 {r.get('Area','---')}\n🏢 Details", key=f"card_{orig_idx}"):
                            st.session_state.current_index = orig_idx; st.session_state.view = "details"; st.rerun()
            with c_side:
                st.markdown(f"### {L['side_dev'] if menu=='Developers' else L['side_proj']}")
                for _, s in active_df.head(4).iterrows():
                    st.markdown(f"<div class='tool-card'>💎 {s[col_main]}</div>", unsafe_allow_html=True)

        # Pagination (Same for both)
        if (start + ITEMS_PER_PAGE) < len(filtered):
            if st.button("Next Page ➡", use_container_width=True): st.session_state.page_num += 1; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
