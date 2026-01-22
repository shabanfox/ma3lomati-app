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
        "side_dev": "⭐ TOP DEVELOPERS", "side_proj": "🏠 READY TO MOVE", "search": "Search assets..."
    },
    "AR": {
        "logout": "خروج", "back": "← عودة", "next": "الصفحة التالية ←", "prev": "← الصفحة السابقة",
        "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "side_dev": "⭐ أفضل المطورين", "side_proj": "🏠 استلام فوري", "search": "بحث عن عقار..."
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
        background: linear-gradient(rgba(0,0,0,0.97), rgba(0,0,0,0.97)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {direction} !important; text-align: {"right" if direction=="rtl" else "left"} !important; 
        font-family: 'Cairo', sans-serif;
    }}
    
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{HEADER_IMG}');
        background-size: cover; background-position: center;
        border-bottom: 2px solid #f59e0b; padding: 45px 20px; text-align: center;
        border-radius: 0 0 40px 40px; margin-bottom: 30px; box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }}

    /* Luxury Card Styling */
    div.stButton > button[key*="card_"] {{
        background: rgba(25, 25, 25, 0.95) !important;
        color: #FFFFFF !important;
        border: 1px solid #333 !important;
        border-left: 5px solid #f59e0b !important;
        border-radius: 15px !important;
        height: 180px !important;
        width: 100% !important;
        padding: 20px !important;
        transition: 0.4s all ease-in-out;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
        display: block !important;
    }}
    
    div.stButton > button:hover {{
        transform: translateY(-8px);
        background: #f59e0b !important;
        color: #000 !important;
        border-color: #f59e0b !important;
    }}

    .sidebar-box {{
        background: rgba(255, 255, 255, 0.03); padding: 18px; border-radius: 12px;
        border: 1px solid rgba(245, 158, 11, 0.2); margin-bottom: 15px;
    }}
    
    .price-tag {{ color: #f59e0b; font-weight: bold; font-size: 14px; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Data Loading ---
@st.cache_data(ttl=60)
def load_all_data():
    URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    URL_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(URL_P), pd.read_csv(URL_D), pd.read_csv(URL_L)
        for df in [p, d, l]: df.columns = [c.strip() for c in df.columns]
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_all_data()

# --- 5. Navigation & Header ---
st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900; letter-spacing:3px;">MA3LOMATI</h1></div>', unsafe_allow_html=True)

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

if menu in ["Projects", "المشاريع"]: 
    active_df, side_title = df_p, L["side_proj"]
    col_name = 'Project Name' if 'Project Name' in df_p.columns else df_p.columns[0]
    side_items = df_p.head(5)
elif menu in ["Launches", "اللونشات"]: 
    active_df, side_title = df_l, "🔥 NEW LAUNCH"
    col_name = 'Project' if 'Project' in df_l.columns else df_l.columns[0]
    side_items = df_l.head(5)
else: 
    active_df, side_title = df_d, L["side_dev"]
    col_name = 'Developer' if 'Developer' in df_d.columns else df_d.columns[0]
    side_items = df_d.head(5)

# --- MAIN SECTION (70%) ---
with col_main:
    search = st.text_input(L["search"])
    filtered = active_df[active_df[col_name].astype(str).str.contains(search, case=False)] if search else active_df
    
    start_idx = st.session_state.page_num * ITEMS_PER_PAGE
    display_df = filtered.iloc[start_idx : start_idx + ITEMS_PER_PAGE]

    grid = st.columns(2)
    for i, (orig_idx, r) in enumerate(display_df.iterrows()):
        with grid[i % 2]:
            # Construct Luxury Label
            title = r[col_name]
            loc = r.get('Area', r.get('Location', 'Premium District'))
            dev = r.get('Developer', 'Elite Partner')
            price = r.get('Price & Payment', 'Price on Request')
            
            # This is the "Full Details" luxury card label
            card_label = f"✨ {title}\n📍 {loc}\n🏢 {dev}\n💰 {price}"
            
            if st.button(card_label, key=f"card_{i}"):
                st.session_state.selected_item = r

    # Pagination
    st.write("---")
    nb1, nb2 = st.columns(2)
    with nb1:
        if st.session_state.page_num > 0:
            if st.button(L["prev"], use_container_width=True): st.session_state.page_num -= 1; st.rerun()
    with nb2:
        if (start_idx + ITEMS_PER_PAGE) < len(filtered):
            if st.button(L["next"], use_container_width=True): st.session_state.page_num += 1; st.rerun()

# --- SIDE SECTION (30%) ---
with col_side:
    st.markdown(f"<h3 style='color:#f59e0b; border-bottom: 1px solid #333;'>{side_title}</h3>", unsafe_allow_html=True)
    for _, s_item in side_items.iterrows():
        st.markdown(f"""
            <div class="sidebar-box">
                <b style="color:white;">💎 {s_item[col_name]}</b><br>
                <small style="color:#f59e0b;">{s_item.get('Developer', 'Elite Developer')}</small>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
