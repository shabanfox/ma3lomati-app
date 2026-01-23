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
    "EN": {"back": "🏠 Back", "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"], "search": "Search..."},
    "AR": {"back": "🏠 العودة للقائمة", "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], "search": "بحث سريع..."}
}
L = trans[st.session_state.lang]
direction = "rtl" if st.session_state.lang == "AR" else "ltr"

# --- 3. THE FIXED CSS (Crucial Fix for Text Alignment) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.97), rgba(0,0,0,0.97)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {direction}; font-family: 'Cairo', sans-serif;
    }}

    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{HEADER_IMG}');
        background-size: cover; padding: 30px; text-align: center; border-radius: 0 0 40px 40px; border-bottom: 2px solid #f59e0b;
    }}

    /* الكارت الخارجي (الزرار) */
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.95) !important; color: white !important;
        border-left: 5px solid #f59e0b !important; border-radius: 12px !important;
        width: 100% !important; min-height: 160px !important; padding: 20px !important;
        text-align: {"right" if direction=="rtl" else "left"} !important;
        white-space: pre-line !important; font-size: 16px !important;
    }}

    /* كروت التفاصيل - حل مشكلة اختفاء النص */
    .detail-card-container {{
        background-color: rgba(25, 25, 25, 0.98) !important;
        border: 1px solid #444 !important;
        border-top: 5px solid #f59e0b !important;
        border-radius: 15px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
        position: relative !important; /* يضمن بقاء المحتوى داخل الكارت */
        display: block !important;
        width: 100% !important;
        min-height: 200px !important;
        color: white !important;
    }}
    
    .section-title {{ 
        color: #f59e0b !important; 
        font-weight: 900 !important; 
        font-size: 20px !important; 
        border-bottom: 1px solid #444 !important; 
        margin-bottom: 15px !important; 
        padding-bottom: 5px !important; 
    }}

    .data-row {{ margin-bottom: 12px !important; }}
    .label-gold {{ color: #f59e0b !important; font-weight: 700 !important; font-size: 14px !important; display: block; }}
    .val-white {{ color: #ffffff !important; font-size: 16px !important; font-weight: 400 !important; }}
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
        p, d, l = pd.read_csv(urls["P"]), pd.read_csv(urls["D"]), pd.read_csv(urls["L"])
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_all_data()

# --- 5. Navigation ---
st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900;">MA3LOMATI</h1></div>', unsafe_allow_html=True)
menu_selection = option_menu(None, L["menu"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if menu_selection != st.session_state.last_menu:
    st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu_selection
    st.rerun()

# --- 6. Main Logic ---
active_df = df_l if menu_selection in ["Launches", "اللونشات"] else (df_p if menu_selection in ["Projects", "المشاريع"] else df_d)

if not active_df.empty:
    cols = active_df.columns

    if st.session_state.view == "details":
        item = active_df.iloc[st.session_state.current_index]
        if st.button(L["back"], use_container_width=True): st.session_state.view = "grid"; st.rerun()
        
        # توزيع البيانات على 3 أعمدة (أكواد HTML داخل دالة Markdown لضمان الثبات)
        c1, c2, c3 = st.columns(3)
        split = max(1, len(cols) // 3)

        def create_card_html(title, start, end):
            content = f'<div class="detail-card-container"><div class="section-title">{title}</div>'
            for k in cols[start:end]:
                content += f'<div class="data-row"><span class="label-gold">{k}</span><span class="val-white">{item[k]}</span></div>'
            content += '</div>'
            return content

        with c1: st.markdown(create_card_html("💎 الأساسيات", 0, split), unsafe_allow_html=True)
        with c2: st.markdown(create_card_html("📍 الموقع", split, split*2), unsafe_allow_html=True)
        with c3: st.markdown(create_card_html("💰 إضافات", split*2, len(cols)), unsafe_allow_html=True)

    else:
        # واجهة الشبكة (Grid)
        search = st.text_input(L["search"])
        filtered = active_df[active_df.iloc[:,0].astype(str).str.contains(search, case=False)] if search else active_df
        display_df = filtered.iloc[st.session_state.page_num * ITEMS_PER_PAGE : (st.session_state.page_num+1) * ITEMS_PER_PAGE]

        g_cols = 3 if menu_selection in ["Launches", "اللونشات"] else 2
        grid = st.columns(g_cols)
        for i, (orig_idx, r) in enumerate(display_df.iterrows()):
            with grid[i % g_cols]:
                card_txt = f"✨ {r.iloc[0]}\n📍 {r.iloc[1] if len(r)>1 else ''}\n🏢 {r.iloc[2] if len(r)>2 else ''}"
                if st.button(card_txt, key=f"card_{orig_idx}"):
                    st.session_state.current_index, st.session_state.view = orig_idx, "details"; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
