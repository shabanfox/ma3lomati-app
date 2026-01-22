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
        "logout": "Logout", "back": "🏠 Back", "search": "Search...",
        "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "ai_msg": "How can I help you today with market data?",
        "tool_title": "Broker Business Tools"
    },
    "AR": {
        "logout": "خروج", "back": "🏠 عودة", "search": "بحث...",
        "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "ai_msg": "كيف يمكنني مساعدتك اليوم في تحليل البيانات؟",
        "tool_title": "أدوات البروكر المحترف"
    }
}

L = trans[st.session_state.lang]

# --- 3. Luxury CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.97), rgba(0,0,0,0.97)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {"rtl" if st.session_state.lang == "AR" else "ltr"} !important;
        font-family: 'Cairo', sans-serif;
    }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{HEADER_IMG}');
        background-size: cover; background-position: center;
        border-bottom: 2px solid #f59e0b; padding: 40px 20px; text-align: center;
        border-radius: 0 0 40px 40px; margin-bottom: 30px;
    }}
    /* Tool & Project Cards */
    div.stButton > button {{
        background: rgba(30, 30, 30, 0.9) !important; color: white !important;
        border-radius: 12px !important; border: 1px solid #444 !important;
    }}
    div.stButton > button[key*="card_"] {{
        border-left: 5px solid #f59e0b !important; height: 180px !important; width: 100% !important;
    }}
    .tool-box {{
        background: rgba(245, 158, 11, 0.05); padding: 20px; border-radius: 15px;
        border: 1px solid #f59e0b; margin-bottom: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Load Data ---
@st.cache_data(ttl=60)
def load_data():
    URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    URL_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(URL_P), pd.read_csv(URL_D), pd.read_csv(URL_L)
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 5. Navigation ---
st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900;">MA3LOMATI</h1></div>', unsafe_allow_html=True)
c_menu, c_lang, c_out = st.columns([0.7, 0.15, 0.15])
with c_menu:
    menu = option_menu(None, L["menu"], default_index=2, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
    if menu != st.session_state.last_menu:
        st.session_state.view = "grid"; st.session_state.last_menu = menu; st.rerun()
with c_lang:
    if st.button("🌐 EN/AR", use_container_width=True):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()
with c_out:
    if st.button(f"🚪 {L['logout']}", use_container_width=True): st.session_state.auth = False; st.rerun()

# --- 6. Content Routing ---

# --- SECTION: TOOLS (6 Working Tools) ---
if menu in ["Tools", "الأدوات"]:
    st.markdown(f"<h2 style='color:#f59e0b; text-align:center;'>⚒️ {L['tool_title']}</h2>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    with t1:
        with st.expander("🧮 Mortgage Calc / حاسبة القسط", expanded=True):
            price = st.number_input("Price", 0)
            years = st.number_input("Years", 1, 20, 7)
            if price > 0: st.info(f"Monthly: {price/(years*12):,.2f}")
        with st.expander("🏢 Area Converter / محول المساحات"):
            sqm = st.number_input("SQM / متر", 0.0)
            st.write(f"SQFT: {sqm * 10.76:.2f}")

    with t2:
        with st.expander("📈 ROI Calc / العائد الاستثماري", expanded=True):
            cost = st.number_input("Total Cost", 1)
            rent = st.number_input("Annual Rent", 0)
            st.success(f"ROI: {(rent/cost)*100:.2f}%")
        with st.expander("💰 Commission / حساب العمولات"):
            deal = st.number_input("Deal Value", 0)
            perc = st.slider("%", 1.0, 10.0, 2.5)
            st.warning(f"Commission: {deal*(perc/100):,.0f}")

    with t3:
        with st.expander("🌍 Currency / العملات (EGP/USD)", expanded=True):
            usd = st.number_input("Amount in USD", 0.0)
            rate = st.number_input("Rate", 48.0, 70.0, 50.0)
            st.info(f"Total EGP: {usd*rate:,.2f}")
        with st.expander("✍️ AI Script / مولد نصوص بيعية"):
            p_name = st.text_input("Project Name")
            if st.button("Generate"): st.code(f"Special Offer in {p_name}! Luxury units available now.")

# --- SECTION: AI ASSISTANT ---
elif menu in ["AI Assistant", "المساعد الذكي"]:
    st.markdown(f"<div class='tool-box'><h3>🤖 MA3LOMATI AI</h3><p>{L['ai_msg']}</p></div>", unsafe_allow_html=True)
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])
    if prompt := st.chat_input("Ask me about any project..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": f"I am analyzing the market for: {prompt}. Please wait..."})
        st.rerun()

# --- SECTION: DATA (Projects/Devs/Launches) ---
else:
    if st.session_state.view == "details":
        # Details logic (same as before)
        active_df = df_p if menu == "Projects" or menu == "المشاريع" else (df_l if "Launch" in menu or "لونش" in menu else df_d)
        item = active_df.iloc[st.session_state.current_index]
        if st.button(L["back"]): st.session_state.view = "grid"; st.rerun()
        st.markdown(f"<div class='tool-box'><h1>{item.iloc[0]}</h1><p>{item.to_string()}</p></div>", unsafe_allow_html=True)
    else:
        # Grid logic with 70/30 (same as before)
        col_m, col_s = st.columns([0.7, 0.3])
        with col_m:
            active_df = df_p if menu in ["Projects", "المشاريع"] else (df_l if "Launch" in menu or "لونش" in menu else df_d)
            start = st.session_state.page_num * 6
            grid = st.columns(2)
            for i, (idx, r) in enumerate(active_df.iloc[start:start+6].iterrows()):
                with grid[i%2]:
                    if st.button(f"✨ {r.iloc[0]}\n📍 {r.get('Area','---')}", key=f"card_{idx}"):
                        st.session_state.current_index = idx; st.session_state.view = "details"; st.rerun()
            # Pagination buttons below grid
            st.write("---")
            if st.button("Next Page ⮕"): st.session_state.page_num += 1; st.rerun()
        with col_s:
            st.markdown("### ⭐ Recommendations")
            for i in range(3): st.markdown(f"<div class='tool-box'>Premium {menu} {i+1}</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
