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
        "logout": "Logout", "back": "🏠 Back", "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "side_dev": "⭐ TOP DEVELOPERS", "side_proj": "🏠 READY TO MOVE", "search": "Search...",
        "det_title": "Specifications", "ai_welcome": "How can I help you?", "tool_title": "Broker Tools", "login": "Passcode"
    },
    "AR": {
        "logout": "خروج", "back": "🏠 العودة", "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "side_dev": "⭐ أفضل المطورين", "side_proj": "🏠 استلام فوري", "search": "بحث...",
        "det_title": "التفاصيل", "ai_welcome": "كيف يمكنني مساعدتك؟", "tool_title": "أدوات البروكر", "login": "رمز الدخول"
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
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {direction} !important; text-align: {"right" if direction=="rtl" else "left"} !important; 
        font-family: 'Cairo', sans-serif;
    }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.8)), url('{HEADER_IMG}');
        background-size: cover; background-position: center;
        border-bottom: 2px solid #f59e0b; padding: 50px 20px; text-align: center;
        border-radius: 0 0 40px 40px; margin-bottom: 10px;
    }}
    /* تصغير أزرار اللغات والدخول */
    div.stButton > button {{ 
        font-size: 11px !important; padding: 0px 5px !important; height: 30px !important;
        background-color: rgba(245, 158, 11, 0.2) !important; color: white !important;
        border: 1px solid #f59e0b !important;
    }}
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; height: 160px !important; 
        font-size: 14px !important; border-left: 5px solid #f59e0b !important;
    }}
    .tool-card {{ background: rgba(20,20,20,0.8); padding: 15px; border-radius: 15px; border: 1px solid #333; margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Top Bar (Language & Auth) ---
st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900; margin:0;">MA3LOMATI</h1><p style="color:white; font-size:12px;">PRO 2026</p></div>', unsafe_allow_html=True)

t_col1, t_col2, t_col3 = st.columns([0.2, 0.6, 0.2])
with t_col1:
    if st.button("🌐 EN/AR", key="btn_lang"):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()

with t_col3:
    if not st.session_state.auth:
        pass_input = st.text_input("🔑", type="password", placeholder=L["login"], label_visibility="collapsed")
        if pass_input == "2026": st.session_state.auth = True; st.rerun()
    else:
        if st.button(L["logout"], key="btn_out"): st.session_state.auth = False; st.rerun()

if not st.session_state.auth:
    st.info("🔒 Restricted Access / دخول مقيد")
    st.stop()

# --- 5. Data Loading ---
@st.cache_data(ttl=60)
def load_all_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_all_data()

# --- 6. Navigation ---
menu_selection = option_menu(None, L["menu"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}, "container": {"background-color": "transparent"}})

# --- 7. Main Content Logic ---
if menu_selection in ["Tools", "الأدوات"]:
    st.markdown(f"### ⚒️ {L['tool_title']}")
    tc1, tc2, tc3 = st.columns(3)
    with tc1:
        with st.container(border=True):
            amt = st.number_input("Unit Price / السعر", 0)
            yrs = st.slider("Years / سنوات", 1, 15, 8)
            if amt > 0: st.success(f"Monthly: {amt/(yrs*12):,.0f}")
    with tc2:
        with st.container(border=True):
            sqm = st.number_input("Area / مساحة متر", 0.0)
            st.info(f"SQFT: {sqm*10.76:,.0f}")
    with tc3:
        with st.container(border=True):
            usd = st.number_input("USD", 0.0)
            st.warning(f"EGP (50): {usd*50:,.0f}")

elif menu_selection in ["AI Assistant", "المساعد الذكي"]:
    st.chat_message("assistant").write(L["ai_welcome"])
    if pmt := st.chat_input("..."): st.chat_message("user").write(pmt)

else:
    # Logic for Projects/Devs/Launches
    if menu_selection in ["Projects", "المشاريع"]: active_df, col_name = df_p, 'Project Name'
    elif menu_selection in ["Launches", "اللونشات"]: active_df, col_name = df_l, 'Project'
    else: active_df, col_name = df_d, 'Developer'

    if st.session_state.view == "details":
        item = active_df.iloc[st.session_state.current_index]
        if st.button(L["back"]): st.session_state.view = "grid"; st.rerun()
        st.subheader(item.get(col_name, "---"))
        st.write(f"📍 Location: {item.get('Area','---')}")
        st.write(f"📝 Notes: {item.get('Notes','---')}")
    else:
        search = st.text_input(L["search"])
        filt = active_df[active_df[col_name].astype(str).str.contains(search, case=False)] if search else active_df
        
        main_c, side_c = st.columns([0.7, 0.3])
        with main_c:
            grd = st.columns(2)
            for i, (idx, r) in enumerate(filt.head(ITEMS_PER_PAGE).iterrows()):
                with grd[i % 2]:
                    if st.button(f"🏠 {r[col_name]}\n📍 {r.get('Area','---')}", key=f"card_{idx}"):
                        st.session_state.current_index = idx; st.session_state.view = "details"; st.rerun()
        with side_c:
            st.markdown(f"**{L['side_proj']}**")
            ready = df_p.head(5)
            for _, r in ready.iterrows():
                st.markdown(f"<div class='tool-card'>🔑 {r['Project Name']}</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:30px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
