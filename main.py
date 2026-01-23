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
        "side_proj": "🏠 READY TO MOVE", "search": "Search...", "filter_area": "All Areas"
    },
    "AR": {
        "logout": "خروج", "back": "🏠 العودة", "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "side_proj": "🏠 استلام فوري", "search": "بحث...", "filter_area": "كل المناطق"
    }
}
L = trans[st.session_state.lang]
direction = "rtl" if st.session_state.lang == "AR" else "ltr"

# --- 3. CSS ---
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
        border-bottom: 2px solid #f59e0b; padding: 40px 20px; text-align: center;
        border-radius: 0 0 40px 40px; margin-bottom: 30px;
    }}
    [data-testid="stTextInput"], [data-testid="stSelectbox"] {{ margin-bottom: -15px !important; }}
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; color: #FFFFFF !important;
        border-left: 5px solid #f59e0b !important; border-radius: 15px !important;
        height: 200px !important; width: 100% !important; font-size: 16px !important;
    }}
    .detail-card, .tool-card {{
        background: rgba(20, 20, 20, 0.95); padding: 30px; border-radius: 20px;
        border: 1px solid #333; border-top: 5px solid #f59e0b;
    }}
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

# --- 5. Header ---
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

# --- 6. View Logic ---
if menu_selection in ["Tools", "الأدوات"]:
    st.info("Broker Tools Section")
elif menu_selection in ["AI Assistant", "المساعد الذكي"]:
    st.info("AI Assistant Section")
else:
    is_launch = menu_selection in ["Launches", "اللونشات"]
    if menu_selection in ["Projects", "المشاريع"]: active_df, col_main_name = df_p, 'Project Name'
    elif is_launch: active_df, col_main_name = df_l, 'Project'
    else: active_df, col_main_name = df_d, 'Developer'

    if st.session_state.view == "details":
        if st.button(L["back"]): st.session_state.view = "grid"; st.rerun()
        st.write(active_df.iloc[st.session_state.current_index])
    else:
        # --- تصليح سطر البحث والفلترة ---
        f_col1, f_col2, f_col3 = st.columns([0.4, 0.4, 0.2])
        with f_col1:
            search = st.text_input(L["search"], label_visibility="collapsed")
        
        # حماية: التأكد من وجود عمود Area
        has_area = 'Area' in active_df.columns
        area_filter = L["filter_area"]
        
        if has_area:
            with f_col2:
                areas = [L["filter_area"]] + sorted(active_df['Area'].unique().tolist())
                area_filter = st.selectbox("Area", areas, label_visibility="collapsed")

        # تنفيذ الفلترة مع التأكد من وجود الأعمدة
        filtered = active_df
        if search and col_main_name in filtered.columns:
            filtered = filtered[filtered[col_main_name].astype(str).str.contains(search, case=False)]
        if has_area and area_filter != L["filter_area"]:
            filtered = filtered[filtered['Area'] == area_filter]
        
        start_idx = st.session_state.page_num * ITEMS_PER_PAGE
        display_df = filtered.iloc[start_idx : start_idx + ITEMS_PER_PAGE]

        grid = st.columns(3 if is_launch else 2)
        for i, (orig_idx, r) in enumerate(display_df.iterrows()):
            with grid[i % (3 if is_launch else 2)]:
                label = r[col_main_name] if col_main_name in r else "N/A"
                area_label = r['Area'] if has_area else ""
                if st.button(f"{label}\n{area_label}", key=f"card_{orig_idx}"):
                    st.session_state.current_index, st.session_state.view = orig_idx, "details"; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
