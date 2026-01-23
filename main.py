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
    "EN": {"logout": "Logout", "back": "🏠 Back", "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"], "search": "Search..."},
    "AR": {"logout": "خروج", "back": "🏠 العودة للقائمة", "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], "search": "بحث سريع..."}
}
L = trans[st.session_state.lang]
direction = "rtl" if st.session_state.lang == "AR" else "ltr"

# --- 3. Fixed Luxury CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.97), rgba(0,0,0,0.97)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {direction} !important; font-family: 'Cairo', sans-serif;
    }}

    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{HEADER_IMG}');
        background-size: cover; padding: 40px; text-align: center; border-radius: 0 0 40px 40px; border-bottom: 2px solid #f59e0b;
    }}

    /* تعديل الكارت الأساسي لضمان ظهور النص بالداخل */
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.95) !important; 
        color: white !important;
        border: none !important;
        border-left: 5px solid #f59e0b !important; 
        border-radius: 12px !important;
        width: 100% !important;
        min-height: 180px !important;
        height: auto !important;
        padding: 20px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        text-align: {"right" if direction=="rtl" else "left"} !important;
        white-space: pre-line !important; /* يحافظ على تنسيق السطور */
        font-size: 16px !important;
        line-height: 1.6 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }}

    /* كروت التفاصيل */
    .detail-card-dynamic {{
        background: rgba(20, 20, 20, 0.98); 
        padding: 25px; 
        border-radius: 15px;
        border: 1px solid #444; 
        border-top: 4px solid #f59e0b; 
        margin-bottom: 20px;
        color: white;
        min-height: 200px;
        word-wrap: break-word;
    }}
    
    .section-title {{ color: #f59e0b; font-weight: 900; font-size: 19px; border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 15px; }}
    .label-gold {{ color: #f59e0b; font-weight: 700; font-size: 14px; margin-top: 10px; }}
    .val-white {{ color: #ffffff; font-size: 16px; margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Data Loading ---
@st.cache_data(ttl=60)
def load_all_data():
    urls = {
        "P": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv",
        "D": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv",
        "L": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    }
    try:
        p = pd.read_csv(urls["P"]).fillna("---")
        d = pd.read_csv(urls["D"]).fillna("---")
        l = pd.read_csv(urls["L"]).fillna("---")
        for df in [p, d, l]: df.columns = [str(c).strip() for c in df.columns]
        return p, d, l
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

if not active_df.empty:
    cols = active_df.columns
    main_col = cols[0]

    if st.session_state.view == "details":
        item = active_df.iloc[st.session_state.current_index]
        if st.button(L["back"], use_container_width=True): st.session_state.view = "grid"; st.rerun()
        
        c1, c2, c3 = st.columns(3)
        num_cols = len(cols)
        s = max(1, num_cols // 3)

        with c1:
            st.markdown('<div class="detail-card-dynamic"><div class="section-title">💎 الأساسيات</div>', unsafe_allow_html=True)
            for k in cols[:s]:
                st.markdown(f'<p class="label-gold">{k}</p><div class="val-white">{item[k]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="detail-card-dynamic"><div class="section-title">📍 المواصفات</div>', unsafe_allow_html=True)
            for k in cols[s:s*2]:
                st.markdown(f'<p class="label-gold">{k}</p><div class="val-white">{item[k]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="detail-card-dynamic"><div class="section-title">💰 إضافات</div>', unsafe_allow_html=True)
            for k in cols[s*2:]:
                st.markdown(f'<p class="label-gold">{k}</p><div class="val-white">{item[k]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        search = st.text_input(L["search"])
        filtered = active_df[active_df[main_col].astype(str).str.contains(search, case=False)] if search else active_df
        display_df = filtered.iloc[st.session_state.page_num * ITEMS_PER_PAGE : (st.session_state.page_num+1) * ITEMS_PER_PAGE]

        grid_size = 3 if menu_selection in ["Launches", "اللونشات"] else 2
        grid = st.columns(grid_size)
        
        for i, (orig_idx, r) in enumerate(display_df.iterrows()):
            with grid[i % grid_size]:
                # بناء النص بشكل سليم ليظهر داخل الزرار
                card_text = f"✨ {r.iloc[0]}\n📍 {r.iloc[1] if len(r)>1 else '---'}\n🏢 {r.iloc[2] if len(r)>2 else '---'}"
                if st.button(card_text, key=f"card_{orig_idx}"):
                    st.session_state.current_index, st.session_state.view = orig_idx, "details"; st.rerun()

        if (st.session_state.page_num + 1) * ITEMS_PER_PAGE < len(filtered):
            if st.button("الصفحة التالية ➡", use_container_width=True):
                st.session_state.page_num += 1; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
