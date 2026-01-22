import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- FIXED IMAGES & CONSTANTS ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

trans = {
    "EN": {
        "logout": "Logout", "back": "← Back", "next": "Next Page →", "prev": "← Previous",
        "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "side_dev": "⭐ TOP DEVELOPERS", "side_proj": "🏠 READY TO MOVE", "search": "Search..."
    },
    "AR": {
        "logout": "خروج", "back": "← عودة", "next": "الصفحة التالية ←", "prev": "← الصفحة السابقة",
        "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "side_dev": "⭐ أفضل المطورين", "side_proj": "🏠 استلام فوري", "search": "بحث..."
    }
}

L = trans[st.session_state.lang]
direction = "rtl" if st.session_state.lang == "AR" else "ltr"

# --- 3. CSS (70/30 Layout & Styling) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {direction} !important; text-align: {"right" if direction=="rtl" else "left"} !important; 
        font-family: 'Cairo', sans-serif;
    }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{HEADER_IMG}');
        background-size: cover; background-position: center;
        border-bottom: 3px solid #f59e0b; padding: 40px 20px; text-align: center;
        border-radius: 0 0 50px 50px; margin-bottom: 25px;
    }}
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; color: #FFFFFF !important;
        border: 1px solid #444 !important; border-top: 4px solid #f59e0b !important;
        border-radius: 12px !important; height: 110px !important; width: 100% !important;
        font-size: 18px !important; font-weight: 900 !important;
    }}
    .sidebar-box {{
        background: rgba(245, 158, 11, 0.05); padding: 15px; border-radius: 15px;
        border: 1px solid rgba(245, 158, 11, 0.3); margin-bottom: 10px;
    }}
    .page-btn button {{ background: #111 !important; color: #f59e0b !important; border: 1px solid #f59e0b !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Data Loading ---
@st.cache_data(ttl=60)
def load_all_data():
    try:
        p = pd.read_csv(URL_P).fillna("---")
        d = pd.read_csv(URL_D).fillna("---")
        l = pd.read_csv(URL_L).fillna("---")
        p.rename(columns={'Area': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d, l
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_all_data()

# --- 5. Main Interface ---
st.markdown(f'<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900;">MA3LOMATI</h1><p style="color:white;">{L["subtitle"] if "subtitle" in L else ""}</p></div>', unsafe_allow_html=True)

c_menu, c_lang, c_out = st.columns([0.7, 0.15, 0.15])
with c_menu:
    menu = option_menu(None, L["menu"], default_index=2, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
with c_lang:
    if st.button("🌐 EN/AR", use_container_width=True):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()
with c_out:
    if st.button(f"🚪 {L['logout']}", use_container_width=True): st.session_state.auth = False; st.rerun()

# --- 6. 70/30 Layout Logic ---
col_main, col_side = st.columns([0.7, 0.3])

# --- Content Selection ---
if menu in ["Projects", "المشاريع"]: 
    active_df = df_p
    side_title = L["side_proj"]
    side_items = df_p[df_p['Location'].str.contains("Zayed|Settlement", case=False)].head(5) # Sample logic for "Ready"
elif menu in ["Launches", "اللونشات"]: 
    active_df = df_l
    side_title = "🔥 NEW"
    side_items = df_l.head(5)
else: 
    active_df = df_d
    side_title = L["side_dev"]
    side_items = df_d.head(5)

# --- MAIN SECTION (70%) ---
with col_main:
    search = st.text_input(L["search"], key="main_search")
    col_name = 'ProjectName' if 'ProjectName' in active_df.columns else ('Project' if 'Project' in active_df.columns else 'Developer')
    filtered = active_df[active_df[col_name].str.contains(search, case=False)] if search else active_df
    
    # Pagination Logic
    start_idx = st.session_state.page_num * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    display_df = filtered.iloc[start_idx:end_idx]

    # Grid Display (6 Items)
    grid = st.columns(2)
    for i, (orig_idx, r) in enumerate(display_df.iterrows()):
        with grid[i % 2]:
            if st.button(f"🏢 {r[col_name]}\n📍 {r.get('Location', 'HQ')}", key=f"card_{i}"):
                st.session_state.selected_item = r
    
    # Navigation Buttons
    st.write("---")
    nb1, nb2 = st.columns(2)
    with nb1:
        if st.session_state.page_num > 0:
            if st.button(L["prev"], key="prev_page", use_container_width=True):
                st.session_state.page_num -= 1; st.rerun()
    with nb2:
        if end_idx < len(filtered):
            if st.button(L["next"], key="next_page", use_container_width=True):
                st.session_state.page_num += 1; st.rerun()

# --- SIDE SECTION (30%) ---
with col_side:
    st.markdown(f"<h3 style='color:#f59e0b;'>{side_title}</h3>", unsafe_allow_html=True)
    for _, s_item in side_items.iterrows():
        s_name = s_item.get('ProjectName', s_item.get('Project', s_item.get('Developer')))
        st.markdown(f"""
            <div class="sidebar-box">
                <b style="color:white;">{s_name}</b><br>
                <small style="color:#aaa;">{s_item.get('Location', 'Premium')}</small>
            </div>
        """, unsafe_allow_html=True)

# --- Detail Overlay ---
if st.session_state.selected_item is not None:
    it = st.session_state.selected_item
    st.divider()
    if st.button(L["back"]): st.session_state.selected_item = None; st.rerun()
    st.info(f"Viewing: {it[col_name]}")
    # (Detail expansion here...)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
