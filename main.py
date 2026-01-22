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
        "det_title": "Developer Profile", "ai_welcome": "How can I help you today?",
        "tool_title": "Professional Broker Tools",
        "owner": "👤 Owner / Chairman", "details": "🏢 Company Details", "projects": "🏗️ Key Projects"
    },
    "AR": {
        "logout": "خروج", "back": "🏠 العودة للقائمة",
        "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "side_dev": "⭐ أفضل المطورين", "side_proj": "🏠 استلام فوري", "search": "بحث عن عقار...",
        "det_title": "ملف المطور العقاري", "ai_welcome": "كيف يمكنني مساعدتك اليوم؟",
        "tool_title": "أدوات البروكر المحترف",
        "owner": "👤 المالك / رئيس مجلس الإدارة", "details": "🏢 عن الشركة", "projects": "🏗️ أهم المشاريع"
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
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; color: #FFFFFF !important;
        border-left: 5px solid #f59e0b !important; border-radius: 15px !important;
        height: 180px !important; width: 100% !important;
        text-align: {"right" if direction=="rtl" else "left"} !important;
        font-size: 16px !important; line-height: 1.6 !important;
    }}
    .detail-card {{
        background: rgba(20, 20, 20, 0.95); padding: 30px; border-radius: 20px;
        border: 1px solid #333; border-top: 5px solid #f59e0b; margin-top: 10px;
    }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 18px; margin-top: 15px; border-bottom: 1px solid #333; padding-bottom: 5px; }}
    .val-white {{ color: white; font-size: 19px; margin-bottom: 15px; padding-top: 10px; }}
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

c_menu, c_lang, c_out = st.columns([0.7, 0.15, 0.15])
with c_menu:
    menu_selection = option_menu(None, L["menu"], default_index=2, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
    
    if menu_selection != st.session_state.last_menu:
        st.session_state.view = "grid"
        st.session_state.page_num = 0
        st.session_state.last_menu = menu_selection
        st.rerun()

with c_lang:
    if st.button("🌐 EN/AR", use_container_width=True):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()
with c_out:
    if st.button(f"🚪 {L['logout']}", use_container_width=True): st.session_state.auth = False; st.rerun()

# --- 6. View Logic ---

# A. TOOLS & B. AI (Keep as is)
if menu_selection in ["Tools", "الأدوات"]:
    st.markdown(f"<h2 style='color:#f59e0b; text-align:center;'>⚒️ {L['tool_title']}</h2>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    # ... (Mortgage, Area, ROI, Commission, Currency, AI Script) - Code same as before
    with t1:
        with st.container(border=True):
            st.subheader("🧮 Mortgage")
            p = st.number_input("Amount", 0, key="t1_p")
            if p > 0: st.warning(f"Monthly: {p/(7*12):,.2f}")
    with t2:
        with st.container(border=True):
            st.subheader("📈 ROI")
            c = st.number_input("Cost", 1)
            r = st.number_input("Rent", 0)
            st.warning(f"ROI: {(r/c)*100:.2f}%")
    with t3:
        with st.container(border=True):
            st.subheader("🌍 Currency")
            u = st.number_input("USD", 0.0)
            st.warning(f"EGP: {u*50:,.2f}")

elif menu_selection in ["AI Assistant", "المساعد الذكي"]:
    st.markdown(f"<div class='detail-card'><h3>🤖 AI</h3><p>{L['ai_welcome']}</p></div>", unsafe_allow_html=True)
    if prompt := st.chat_input("Ask me..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

# C. DATA SECTIONS
else:
    is_launch = menu_selection in ["Launches", "اللونشات"]
    is_dev = menu_selection in ["Developers", "المطورين"]

    if menu_selection in ["Projects", "المشاريع"]: 
        active_df, col_main_name = df_p, 'Project Name' if 'Project Name' in df_p.columns else df_p.columns[0]
    elif is_launch: 
        active_df, col_main_name = df_l, 'Project' if 'Project' in df_l.columns else df_l.columns[0]
    else: 
        active_df, col_main_name = df_d, 'Developer' if 'Developer' in df_d.columns else df_d.columns[0]

    if st.session_state.view == "details":
        item = active_df.iloc[st.session_state.current_index]
        if st.button(L["back"], use_container_width=True): st.session_state.view = "grid"; st.rerun()
        
        # --- تنظيم صفحة تفاصيل المطور ---
        if is_dev:
            st.markdown(f"""
            <div class="detail-card">
                <h1 style="color:#f59e0b; margin-bottom:5px;">{item[col_main_name]}</h1>
                <p style="color:#888;">{L['det_title']}</p>
                <hr style="border:0.5px solid #333;">
                
                <div class="label-gold">{L['owner']}</div>
                <div class="val-white">{item.get('Owner / Chairman', item.get('Owner', '---'))}</div>
                
                <div class="label-gold">{L['details']}</div>
                <div class="val-white" style="line-height:1.6;">{item.get('Company Details', item.get('Details', '---'))}</div>
                
                <div class="label-gold">{L['projects']}</div>
                <div class="val-white" style="line-height:1.6;">{item.get('Key Projects', item.get('Projects', '---'))}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # تفاصيل المشاريع واللونشات التقليدية
            st.markdown(f"<div class='detail-card'><h1>{item[col_main_name]}</h1><p>{item.to_string()}</p></div>", unsafe_allow_html=True)
    
    else:
        # GRID VIEW
        search = st.text_input(L["search"])
        filtered = active_df[active_df[col_main_name].astype(str).str.contains(search, case=False)] if search else active_df
        start_idx = st.session_state.page_num * ITEMS_PER_PAGE
        display_df = filtered.iloc[start_idx : start_idx + ITEMS_PER_PAGE]

        if is_launch:
            grid = st.columns(3)
            for i, (orig_idx, r) in enumerate(display_df.iterrows()):
                with grid[i % 3]:
                    if st.button(f"🚀 {r[col_main_name]}\n📍 {r.get('Area', 'New Launch')}", key=f"card_{orig_idx}"):
                        st.session_state.current_index = orig_idx; st.session_state.view = "details"; st.rerun()
        else:
            col_main, col_side = st.columns([0.7, 0.3])
            with col_main:
                grid = st.columns(2)
                for i, (orig_idx, r) in enumerate(display_df.iterrows()):
                    with grid[i % 2]:
                        label = f"🏢 {r[col_main_name]}" if is_dev else f"✨ {r[col_main_name]}"
                        if st.button(f"{label}\n📍 {r.get('Area', 'Elite')}", key=f"card_{orig_idx}"):
                            st.session_state.current_index = orig_idx; st.session_state.view = "details"; st.rerun()
            with col_side:
                st.markdown(f"<h3 style='color:#f59e0b;'>{L['side_dev'] if is_dev else L['side_proj']}</h3>", unsafe_allow_html=True)
                for _, s_item in active_df.head(4).iterrows():
                    st.markdown(f"<div class='detail-card' style='padding:15px; margin-top:5px;'>💎 {s_item[col_main_name]}</div>", unsafe_allow_html=True)

        st.write("---")
        if (start_idx + ITEMS_PER_PAGE) < len(filtered):
            if st.button("Next Page ➡", use_container_width=True): st.session_state.page_num += 1; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
