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
    "AR": {"logout": "خروج", "back": "🏠 العودة للقائمة", "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], "search": "بحث سريح..."}
}
L = trans[st.session_state.lang]
direction = "rtl" if st.session_state.lang == "AR" else "ltr"

# --- 3. Luxury Style ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.97), rgba(0,0,0,0.97)), url('{BG_IMG}');
        background-size: cover; direction: {direction}; font-family: 'Cairo', sans-serif;
    }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{HEADER_IMG}');
        background-size: cover; padding: 40px; text-align: center; border-radius: 0 0 40px 40px; border-bottom: 2px solid #f59e0b;
    }}
    /* الكارت الأساسي بسيط ومنظم */
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; color: white !important;
        border-left: 5px solid #f59e0b !important; border-radius: 15px !important;
        height: 160px !important; width: 100% !important;
        text-align: {"right" if direction=="rtl" else "left"} !important;
        font-size: 16px !important; line-height: 1.6 !important;
    }}
    /* كروت التفاصيل المقسمة */
    .detail-card {{
        background: rgba(25, 25, 25, 0.95); padding: 25px; border-radius: 15px;
        border: 1px solid #444; border-top: 4px solid #f59e0b; margin-bottom: 20px;
        min-height: 350px;
    }}
    .section-title {{ color: #f59e0b; font-weight: 900; font-size: 18px; margin-bottom: 15px; border-bottom: 1px solid #444; padding-bottom: 8px; }}
    .info-label {{ color: #f59e0b; font-weight: bold; font-size: 13px; margin-top: 10px; }}
    .info-val {{ color: white; font-size: 16px; margin-bottom: 5px; }}
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

if not active_df.empty:
    cols = active_df.columns
    main_col = cols[0]

    if st.session_state.view == "details":
        item = active_df.iloc[st.session_state.current_index]
        if st.button(L["back"]): st.session_state.view = "grid"; st.rerun()
        
        # تقسيم ذكي للأعمدة إلى 3 مجموعات لملء الكروت
        total_cols = len(cols)
        split = total_cols // 3 if total_cols > 3 else 1
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="detail-card"><div class="section-title">💎 المعلومات الأساسية</div>', unsafe_allow_html=True)
            for k in cols[:max(2, split)]:
                st.markdown(f'<p class="info-label">{k}</p><p class="info-val">{item[k]}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c2:
            st.markdown(f'<div class="detail-card"><div class="section-title">📍 الموقع والمواصفات</div>', unsafe_allow_html=True)
            for k in cols[max(2, split):max(4, split*2)]:
                st.markdown(f'<p class="info-label">{k}</p><p class="info-val">{item[k]}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c3:
            st.markdown(f'<div class="detail-card"><div class="section-title">💰 تفاصيل إضافية</div>', unsafe_allow_html=True)
            for k in cols[max(4, split*2):]:
                st.markdown(f'<p class="info-label">{k}</p><p class="info-val">{item[k]}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        # --- الكروت الأساسية (بسيطة ومنظمة) ---
        search = st.text_input(L["search"])
        filtered = active_df[active_df[main_col].astype(str).str.contains(search, case=False)] if search else active_df
        display_df = filtered.iloc[st.session_state.page_num * ITEMS_PER_PAGE : (st.session_state.page_num+1) * ITEMS_PER_PAGE]

        grid_cols = 3 if menu_selection in ["Launches", "اللونشات"] else 2
        grid = st.columns(grid_cols)
        for i, (idx, row) in enumerate(display_df.iterrows()):
            with grid[i % grid_cols]:
                # عرض بسيط: اسم العنصر، اللوكيشن (لو موجود)، والمطور (لو موجود)
                txt = f"✨ {row[0]}\n"
                if len(cols) > 1: txt += f"📍 {row[1]}\n"
                if len(cols) > 2: txt += f"🏢 {row[2]}"
                
                if st.button(txt, key=f"card_{idx}"):
                    st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
