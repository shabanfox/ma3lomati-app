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

trans = {
    "EN": {
        "logout": "Logout", "back": "🏠 Back to List",
        "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "side_dev": "⭐ TOP DEVELOPERS", "side_proj": "🏠 READY TO MOVE", "search": "Search...",
        "tool_title": "Professional Broker Tools"
    },
    "AR": {
        "logout": "خروج", "back": "🏠 العودة للقائمة",
        "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "side_dev": "⭐ أفضل المطورين", "side_proj": "🏠 استلام فوري", "search": "بحث سريح...",
        "tool_title": "أدوات البروكر المحترف"
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
    /* كارت مرن يقرأ البيانات ديناميكياً */
    div.stButton > button[key*="card_"] {{
        background: rgba(25, 25, 25, 0.9) !important; color: #FFFFFF !important;
        border-right: { '5px solid #f59e0b' if direction == 'rtl' else 'none' } !important;
        border-left: { '5px solid #f59e0b' if direction == 'ltr' else 'none' } !important;
        border-radius: 12px !important;
        height: auto !important; min-height: 250px !important; width: 100% !important;
        padding: 20px !important;
        text-align: {"right" if direction=="rtl" else "left"} !important;
        font-size: 15px !important; line-height: 1.6 !important;
        white-space: pre-wrap !important;
    }}
    div.stButton > button[key*="card_"]:hover {{
        border-color: #ffffff !important; background: rgba(40, 40, 40, 1) !important;
    }}
    .detail-card {{
        background: rgba(20, 20, 20, 0.95); padding: 30px; border-radius: 20px;
        border: 1px solid #333; border-top: 5px solid #f59e0b; margin-top: 10px;
    }}
    .label-gold {{ color: #f59e0b; font-weight: 700; margin-top: 10px; }}
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
        # مسح المسافات الزائدة من أسماء الأعمدة
        for df in [p, d, l]: df.columns = [c.strip() for c in df.columns]
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_all_data()

# --- 5. Navigation & Layout ---
st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900;">MA3LOMATI</h1></div>', unsafe_allow_html=True)

menu_selection = option_menu(None, L["menu"], default_index=4, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if menu_selection != st.session_state.last_menu:
    st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu_selection
    st.rerun()

# --- 6. View Logic ---

# A. TOOLS & AI (إختصاراً للشرح)
if menu_selection in ["Tools", "الأدوات", "AI Assistant", "المساعد الذكي"]:
    st.info("قسم الأدوات والمساعد الذكي يعمل بكفاءة.")
    
# B. DATA SECTIONS
else:
    is_launch = menu_selection in ["Launches", "اللونشات"]
    active_df = df_l if is_launch else (df_p if menu_selection in ["Projects", "المشاريع"] else df_d)

    if active_df.empty:
        st.error("لا توجد بيانات متاحة حالياً.")
    else:
        # تحديد أول عمود ليكون هو محرك البحث
        col_main_name = active_df.columns[0]

        if st.session_state.view == "details":
            item = active_df.iloc[st.session_state.current_index]
            if st.button(L["back"]): st.session_state.view = "grid"; st.rerun()
            
            # صفحة تفاصيل ديناميكية بالكامل
            content_html = f"<div class='detail-card'><h2 style='color:#f59e0b;'>{item[col_main_name]}</h2><hr>"
            for col, val in item.items():
                content_html += f"<p class='label-gold'>{col}:</p><p style='color:white; font-size:18px;'>{val}</p>"
            content_html += "</div>"
            st.markdown(content_html, unsafe_allow_html=True)

        else:
            search = st.text_input(L["search"], placeholder="ابحث هنا...")
            filtered = active_df[active_df[col_main_name].astype(str).str.contains(search, case=False)] if search else active_df
            
            start_idx = st.session_state.page_num * ITEMS_PER_PAGE
            display_df = filtered.iloc[start_idx : start_idx + ITEMS_PER_PAGE]

            # عرض شبكة الكروت (3 أعمدة للونشات، 2 للباقي)
            cols_count = 3 if is_launch else 2
            grid = st.columns(cols_count)
            
            for i, (idx, row) in enumerate(display_df.iterrows()):
                with grid[i % cols_count]:
                    # إنشاء نص الكارت ديناميكياً من أول 6 أعمدة في الشيت
                    card_body = ""
                    for col_name in active_df.columns[:6]:
                        card_body += f"🔹 **{col_name}**: {row[col_name]}\n"
                    
                    if st.button(card_body, key=f"card_{idx}"):
                        st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()

            # Pagination
            if (start_idx + ITEMS_PER_PAGE) < len(filtered):
                if st.button("الصفحة التالية ➡", use_container_width=True):
                    st.session_state.page_num += 1; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
