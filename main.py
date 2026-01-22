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
if 'view' not in st.session_state: st.session_state.view = "grid" # grid or details
if 'current_index' not in st.session_state: st.session_state.current_index = 0

trans = {
    "EN": {
        "logout": "Logout", "back": "🏠 Back to Grid", "next": "Next →", "prev": "← Previous",
        "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "side_dev": "⭐ TOP DEVELOPERS", "side_proj": "🏠 READY TO MOVE", "search": "Search assets...",
        "det_title": "Project Specifications"
    },
    "AR": {
        "logout": "خروج", "back": "🏠 العودة للشبكة", "next": "التالي ←", "prev": "← السابق",
        "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "side_dev": "⭐ أفضل المطورين", "side_proj": "🏠 استلام فوري", "search": "بحث عن عقار...",
        "det_title": "مواصفات وتفاصيل المشروع"
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

    /* Luxury Card Grid */
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important;
        color: #FFFFFF !important;
        border-left: 5px solid #f59e0b !important;
        border-radius: 15px !important;
        height: 200px !important;
        width: 100% !important;
        text-align: {"right" if direction=="rtl" else "left"} !important;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }}
    
    /* Details Page Styling */
    .detail-card {{
        background: rgba(20, 20, 20, 0.9);
        padding: 40px; border-radius: 25px;
        border: 1px solid #333; border-top: 5px solid #f59e0b;
        margin-top: 20px;
    }}
    
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 18px; margin-top: 20px; }}
    .val-white {{ color: white; font-size: 20px; margin-bottom: 10px; }}
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
st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900;">MA3LOMATI</h1></div>', unsafe_allow_html=True)

c_menu, c_lang, c_out = st.columns([0.7, 0.15, 0.15])
with c_menu:
    menu = option_menu(None, L["menu"], default_index=2, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
with c_lang:
    if st.button("🌐 EN/AR", use_container_width=True):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()
with c_out:
    if st.button(f"🚪 {L['logout']}", use_container_width=True): st.session_state.auth = False; st.rerun()

# --- 6. Active Dataset Selection ---
if menu in ["Projects", "المشاريع"]: 
    active_df, col_main_name = df_p, 'Project Name' if 'Project Name' in df_p.columns else df_p.columns[0]
elif menu in ["Launches", "اللونشات"]: 
    active_df, col_main_name = df_l, 'Project' if 'Project' in df_l.columns else df_l.columns[0]
else: 
    active_df, col_main_name = df_d, 'Developer' if 'Developer' in df_d.columns else df_d.columns[0]

# --- 7. MAIN VIEW LOGIC ---

# A. DETAILS VIEW
if st.session_state.view == "details":
    item = active_df.iloc[st.session_state.current_index]
    
    # Nav Buttons: Back | Prev | Next
    b1, b2, b3 = st.columns([0.3, 0.4, 0.3])
    with b1: 
        if st.button(L["back"], use_container_width=True): st.session_state.view = "grid"; st.rerun()
    with b2:
        prev_col, next_col = st.columns(2)
        with prev_col:
            if st.session_state.current_index > 0:
                if st.button(L["prev"], use_container_width=True): st.session_state.current_index -= 1; st.rerun()
        with next_col:
            if st.session_state.current_index < len(active_df) - 1:
                if st.button(L["next"], use_container_width=True): st.session_state.current_index += 1; st.rerun()

    # Layout for Full Details
    st.markdown(f"""
    <div class="detail-card">
        <h1 style="color:#f59e0b; margin-bottom:0;">{item[col_main_name]}</h1>
        <p style="color:#888; font-size:18px;">{L['det_title']}</p>
        <hr style="border: 0.5px solid #333;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
            <div>
                <p class="label-gold">📍 Location / المنطقة</p><p class="val-white">{item.get('Area', item.get('Location', '---'))}</p>
                <p class="label-gold">🏢 Developer / المطور</p><p class="val-white">{item.get('Developer', '---')}</p>
                <p class="label-gold">💰 Price & Payment / السعر ونظام السداد</p><p class="val-white">{item.get('Price & Payment', '---')}</p>
            </div>
            <div>
                <p class="label-gold">📝 Full Details / التفاصيل الكاملة</p>
                <p class="val-white" style="line-height:1.8;">{item.get('Unique Selling Points (USP)', item.get('Notes', '---'))}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# B. GRID VIEW (70/30)
else:
    col_main, col_side = st.columns([0.7, 0.3])
    
    with col_main:
        search = st.text_input(L["search"])
        filtered = active_df[active_df[col_main_name].astype(str).str.contains(search, case=False)] if search else active_df
        
        start_idx = st.session_state.page_num * ITEMS_PER_PAGE
        display_df = filtered.iloc[start_idx : start_idx + ITEMS_PER_PAGE]

        grid = st.columns(2)
        for i, (orig_idx, r) in enumerate(display_df.iterrows()):
            with grid[i % 2]:
                card_text = f"✨ {r[col_main_name]}\n📍 {r.get('Area', 'Premium Area')}\n🏢 {r.get('Developer', 'Elite')}\n💰 Click for more..."
                if st.button(card_text, key=f"card_{orig_idx}"):
                    st.session_state.current_index = orig_idx
                    st.session_state.view = "details"
                    st.rerun()

        # Pagination for Grid
        st.write("---")
        p1, p2 = st.columns(2)
        with p1:
            if st.session_state.page_num > 0:
                if st.button("⬅ Previous Page", use_container_width=True): st.session_state.page_num -= 1; st.rerun()
        with p2:
            if (start_idx + ITEMS_PER_PAGE) < len(filtered):
                if st.button("Next Page ➡", use_container_width=True): st.session_state.page_num += 1; st.rerun()

    with col_side:
        st.markdown(f"<h3 style='color:#f59e0b;'>{L['side_dev'] if menu=='Developers' else L['side_proj']}</h3>", unsafe_allow_html=True)
        # Display side items (static for luxury feel)
        for _, s_item in active_df.head(4).iterrows():
            st.markdown(f"""<div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:12px; border:1px solid #333; margin-bottom:10px;">
                <b style="color:white;">💎 {s_item[col_main_name]}</b><br><small style="color:#f59e0b;">Verified Property</small></div>""", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
