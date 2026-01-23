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

trans = {
    "EN": {
        "logout": "Logout", "back": "🏠 Back", "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "side_dev": "⭐ TOP DEVS", "side_proj": "🏠 READY", "search": "Search...",
        "next": "Next ➡", "prev": "⬅ Prev"
    },
    "AR": {
        "logout": "خروج", "back": "🏠 عودة", "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "side_dev": "⭐ المطورين", "side_proj": "🏠 استلام فوري", "search": "بحث سريع...",
        "next": "التالي ➡", "prev": "⬅ السابق"
    }
}

L = trans[st.session_state.lang]
direction = "rtl" if st.session_state.lang == "AR" else "ltr"

# --- 3. Luxury CSS (Original Style Restored) ---
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
    /* الكروت الأساسية بنمطك المفضل */
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; color: #FFFFFF !important;
        border-left: 5px solid #f59e0b !important; border-radius: 15px !important;
        height: 180px !important; width: 100% !important;
        text-align: {"right" if direction=="rtl" else "left"} !important;
        font-size: 15px !important; line-height: 1.5 !important;
    }}
    /* تصغير كروت الجانب جداً */
    .side-card-mini {{
        background: rgba(20, 20, 20, 0.8); padding: 8px; border-radius: 10px;
        border: 1px solid #333; margin-bottom: 8px; color: #f59e0b; font-size: 11px;
    }}
    .detail-card {{
        background: rgba(20, 20, 20, 0.95); padding: 25px; border-radius: 20px;
        border: 1px solid #333; border-top: 5px solid #f59e0b; margin-top: 10px;
        color: white;
    }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 16px; margin-top: 15px; }}
    .val-white {{ color: white; font-size: 18px; margin-bottom: 8px; }}
    
    /* تصغير خانة البحث */
    div[data-testid="stTextInput"] {{ max-width: 300px !important; }}
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

# --- 5. Main Layout ---
st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900;">MA3LOMATI</h1></div>', unsafe_allow_html=True)
menu_selection = option_menu(None, L["menu"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if menu_selection != st.session_state.last_menu:
    st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu_selection
    st.rerun()

# --- 6. View Logic ---
active_df = df_l if menu_selection in ["Launches", "اللونشات"] else (df_p if menu_selection in ["Projects", "المشاريع"] else df_d)
col_main_name = active_df.columns[0]

if st.session_state.view == "details":
    item = active_df.iloc[st.session_state.current_index]
    if st.button(L["back"], use_container_width=True): st.session_state.view = "grid"; st.rerun()
    cols = active_df.columns
    c1, c2, c3 = st.columns(3)
    s = max(1, len(cols) // 3)
    for i, col in enumerate([c1, c2, c3]):
        with col:
            h = f'<div class="detail-card">'
            for k in cols[i*s : (i+1)*s if i<2 else len(cols)]:
                h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
            st.markdown(h+'</div>', unsafe_allow_html=True)

else:
    # خانة البحث المصغرة
    search = st.text_input(L["search"])
    filtered = active_df[active_df[col_main_name].astype(str).str.contains(search, case=False)] if search else active_df
    
    start_idx = st.session_state.page_num * ITEMS_PER_PAGE
    display_df = filtered.iloc[start_idx : start_idx + ITEMS_PER_PAGE]

    col_main, col_side = st.columns([0.75, 0.25])
    with col_main:
        grid_cols = 3 if menu_selection in ["Launches", "اللونشات"] else 2
        grid = st.columns(grid_cols)
        for i, (orig_idx, r) in enumerate(display_df.iterrows()):
            with grid[i % grid_cols]:
                txt = f"✨ {r.iloc[0]}\n📍 {r.get('Area', r.iloc[1] if len(r)>1 else '')}\n🏢 {r.get('Developer', r.iloc[2] if len(r)>2 else '')}"
                if st.button(txt, key=f"card_{orig_idx}"):
                    st.session_state.current_index, st.session_state.view = orig_idx, "details"; st.rerun()
        
        # أزرار التنقل تحت الكروت مباشرة
        st.markdown("---")
        btn_prev, btn_page, btn_next = st.columns([1, 1, 1])
        with btn_prev:
            if st.session_state.page_num > 0:
                if st.button(L["prev"], use_container_width=True): st.session_state.page_num -= 1; st.rerun()
        with btn_page:
            st.markdown(f"<p style='text-align:center; color:#f59e0b; padding-top:10px;'>{st.session_state.page_num + 1} / {((len(filtered)-1)//ITEMS_PER_PAGE)+1}</p>", unsafe_allow_html=True)
        with btn_next:
            if (start_idx + ITEMS_PER_PAGE) < len(filtered):
                if st.button(L["next"], use_container_width=True): st.session_state.page_num += 1; st.rerun()

    with col_side:
        st.markdown(f"<h4 style='color:#f59e0b; font-size:14px;'>{L['side_dev'] if 'Dev' in menu_selection else L['side_proj']}</h4>", unsafe_allow_html=True)
        for _, s_item in active_df.head(6).iterrows():
            st.markdown(f"<div class='side-card-mini'>💎 {s_item.iloc[0][:20]}</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
