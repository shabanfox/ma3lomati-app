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
        "logout": "Logout", "back": "🏠 Back to List",
        "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "side_dev": "⭐ TOP DEVELOPERS", "side_proj": "🏠 READY TO MOVE", "search": "Search assets...",
        "det_title": "Developer Profile",
        "owner": "👤 Owner / Chairman", "details": "🏢 Company Details", "projects": "🏗️ Key Projects"
    },
    "AR": {
        "logout": "خروج", "back": "🏠 العودة للقائمة",
        "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "side_dev": "⭐ أفضل المطورين", "side_proj": "🏠 استلام فوري", "search": "بحث عن عقار...",
        "det_title": "ملف المطور العقاري",
        "owner": "👤 المالك / رئيس مجلس الإدارة", "details": "🏢 تفاصيل الشركة", "projects": "🏗️ أهم المشاريع"
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
        border-bottom: 2px solid #f59e0b; padding: 40px 20px; text-align: center;
        border-radius: 0 0 40px 40px; margin-bottom: 30px;
    }}
    .detail-card {{
        background: rgba(25, 25, 25, 0.95); padding: 35px; border-radius: 20px;
        border: 1px solid #444; border-top: 5px solid #f59e0b; margin-top: 10px;
    }}
    .section-label {{
        color: #f59e0b; font-size: 1.2rem; font-weight: 900;
        margin-top: 25px; margin-bottom: 8px; border-bottom: 1px solid #333;
        display: inline-block; padding-bottom: 5px;
    }}
    .section-value {{
        color: #ffffff; font-size: 1.1rem; line-height: 1.7; margin-bottom: 15px;
    }}
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; color: #FFFFFF !important;
        border-left: 5px solid #f59e0b !important; border-radius: 15px !important;
        height: 150px !important; width: 100% !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Data Loading ---
@st.cache_data(ttl=60)
def load_all_data():
    URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    URL_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(URL_P), pd.read_csv(URL_D), pd.read_csv(URL_L)
        for df in [p, d, l]: df.columns = [c.strip() for c in df.columns]
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_all_data()

# --- 5. Navigation ---
st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900;">MA3LOMATI</h1></div>', unsafe_allow_html=True)
c_menu, c_lang, c_out = st.columns([0.7, 0.15, 0.15])
with c_menu:
    menu_selection = option_menu(None, L["menu"], default_index=1, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
    if menu_selection != st.session_state.last_menu:
        st.session_state.view = "grid"; st.session_state.page_num = 0; st.session_state.last_menu = menu_selection; st.rerun()

# --- 6. Content Logic ---
is_dev_page = menu_selection in ["Developers", "المطورين"]

if menu_selection == "Projects" or menu_selection == "المشاريع":
    active_df, col_name = df_p, 'Project Name'
elif menu_selection == "Launches" or menu_selection == "اللونشات":
    active_df, col_name = df_l, 'Project'
else:
    active_df, col_name = df_d, 'Developer'

if st.session_state.view == "details":
    item = active_df.iloc[st.session_state.current_index]
    if st.button(L["back"], use_container_width=True): st.session_state.view = "grid"; st.rerun()
    
    # --- التنسيق المطلوب لصفحة المطورين ---
    if is_dev_page:
        st.markdown(f"""
        <div class="detail-card">
            <h1 style="color:#f59e0b; margin-bottom:0;">{item[col_name]}</h1>
            <p style="color:#777; font-size:0.9rem; margin-bottom:20px;">{L['det_title']}</p>
            
            <div class="section-label">{L['owner']}</div>
            <div class="section-value">{item.get('Owner / Chairman', '---')}</div>
            
            <div class="section-label">{L['details']}</div>
            <div class="section-value">{item.get('Company Details', '---')}</div>
            
            <div class="section-label">{L['projects']}</div>
            <div class="section-value">{item.get('Key Projects', '---')}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # تفاصيل باقي الصفحات (Projects & Launches)
        st.markdown(f'<div class="detail-card"><h1 style="color:#f59e0b;">{item[col_name]}</h1><hr>', unsafe_allow_html=True)
        for col in active_df.columns:
            if col != col_name:
                st.markdown(f'<p><span style="color:#f59e0b; font-weight:bold;">{col}:</span> <span style="color:white;">{item[col]}</span></p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # GRID VIEW
    search = st.text_input(L["search"])
    filtered = active_df[active_df[col_name].astype(str).str.contains(search, case=False)] if search else active_df
    start_idx = st.session_state.page_num * ITEMS_PER_PAGE
    display_df = filtered.iloc[start_idx : start_idx + ITEMS_PER_PAGE]

    grid = st.columns(2)
    for i, (orig_idx, r) in enumerate(display_df.iterrows()):
        with grid[i % 2]:
            if st.button(f"✨ {r[col_name]}\n📍 {r.get('Area', 'Egypt')}", key=f"card_{orig_idx}"):
                st.session_state.current_index = orig_idx; st.session_state.view = "details"; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
