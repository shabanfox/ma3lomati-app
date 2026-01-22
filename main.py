import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- FIXED IMAGES LINKS ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 2. Data Links ---
URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
URL_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"

# --- 3. Session State & Logic ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'selected_idx' not in st.session_state: st.session_state.selected_idx = None
if 'messages' not in st.session_state: st.session_state.messages = []

trans = {
    "EN": {
        "subtitle": "LUXURY REAL ESTATE INTELLIGENCE",
        "logout": "Logout", "back": "🏠 Back to List", "next": "Next Project ⮕", "prev": "⬅ Previous Project",
        "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "fields": ["📍 Location", "💰 Payment Plan", "🏢 Developer", "📝 Details"],
        "search": "🔍 Search here...", "ai_title": "AI Assistant"
    },
    "AR": {
        "subtitle": "ذكاء السوق العقاري الفاخر",
        "logout": "خروج", "back": "🏠 العودة للقائمة", "next": "المشروع التالي ⮕", "prev": "⬅ المشروع السابق",
        "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "fields": ["📍 الموقع", "💰 نظام السداد", "🏢 المطور", "📝 التفاصيل"],
        "search": "🔍 ابحث هنا...", "ai_title": "المساعد الذكي"
    }
}

L = trans[st.session_state.lang]
direction = "rtl" if st.session_state.lang == "AR" else "ltr"

# --- 4. Professional CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {direction} !important; text-align: {"right" if direction=="rtl" else "left"} !important; 
        font-family: 'Cairo', sans-serif;
    }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{HEADER_IMG}');
        background-size: cover; background-position: center;
        border-bottom: 3px solid #f59e0b; padding: 50px 20px; text-align: center;
        border-radius: 0 0 50px 50px; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }}
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; color: #FFFFFF !important;
        border: 1px solid #444 !important; border-top: 4px solid #f59e0b !important;
        border-radius: 15px !important; height: 130px !important; width: 100% !important;
        font-size: 18px !important; font-weight: 900 !important;
    }}
    div.stButton > button:hover {{ transform: scale(1.02); background: #f59e0b !important; color: #000 !important; }}
    .info-card {{ background: rgba(0,0,0,0.85); padding: 30px; border-radius: 20px; border: 1px solid #333; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 16px; margin-top: 15px; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. Data Function ---
@st.cache_data(ttl=60)
def get_data():
    try:
        p = pd.read_csv(URL_P).fillna("---")
        d = pd.read_csv(URL_D).fillna("---")
        l = pd.read_csv(URL_L).fillna("---")
        p.rename(columns={'Area': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d, l
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = get_data()

# --- 6. Auth ---
if not st.session_state.auth:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div style='height:150px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='info-card' style='text-align:center;'><h1 style='color:#f59e0b;'>MA3LOMATI</h1><p>{L['subtitle']}</p>", unsafe_allow_html=True)
        pwd = st.text_input("Access Key", type="password")
        if st.button("🔓 Enter"):
            if pwd == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- 7. Main Interface ---
st.markdown(f"""
    <div class="royal-header">
        <h1 style="color: #f59e0b; font-size: 60px; margin: 0; font-weight: 900;">MA3LOMATI</h1>
        <p style="color: #fff; letter-spacing: 4px;">{L['subtitle']}</p>
    </div>
""", unsafe_allow_html=True)

c_menu, c_lang, c_out = st.columns([0.7, 0.15, 0.15])
with c_menu:
    menu = option_menu(None, L["menu"], default_index=2, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
with c_lang:
    if st.button("🌐 EN/AR", use_container_width=True):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()
with c_out:
    if st.button(f"🚪 {L['logout']}", use_container_width=True): st.session_state.auth = False; st.rerun()

# --- 8. Page Content ---
# Determine active dataframe
if menu in ["Projects", "المشاريع"]: active_df = df_p
elif menu in ["Launches", "اللونشات"]: active_df = df_l
else: active_df = df_d

# --- 8a. Details View (With Prev/Next Logic) ---
if st.session_state.selected_idx is not None:
    idx = st.session_state.selected_idx
    it = active_df.iloc[idx]
    
    # Navigation Buttons
    nb1, nb2, nb3 = st.columns([0.25, 0.5, 0.25])
    with nb1:
        if idx > 0:
            if st.button(L["prev"], use_container_width=True): st.session_state.selected_idx -= 1; st.rerun()
    with nb2:
        if st.button(L["back"], use_container_width=True): st.session_state.selected_idx = None; st.rerun()
    with nb3:
        if idx < len(active_df) - 1:
            if st.button(L["next"], use_container_width=True): st.session_state.selected_idx += 1; st.rerun()

    # Content Display
    st.markdown(f"""<div class="info-card">
        <h1 style="color:#f59e0b;">✨ {it.get('ProjectName', it.get('Project', it.get('Developer')))}</h1>
        <hr style="opacity:0.2">
        <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px;">
            <div>
                <p class="label-gold">{L['fields'][0]}</p><h3>{it.get('Location','---')}</h3>
                <p class="label-gold">{L['fields'][3]}</p><p style="font-size:18px; line-height:1.6;">{it.get('Unique Selling Points (USP)', it.get('Notes','---'))}</p>
            </div>
            <div style="border-left: 1px solid #444; padding-left: 20px;">
                <p class="label-gold">{L['fields'][1]}</p><h4>{it.get('Price & Payment','---')}</h4>
                <p class="label-gold">{L['fields'][2]}</p><h4>{it.get('Developer','---')}</h4>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

# --- 8b. Menu Views ---
else:
    if menu in ["AI Assistant", "المساعد الذكي"]:
        st.markdown(f"<div class='info-card'><h2>🤖 {L['ai_title']}</h2>", unsafe_allow_html=True)
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.write(m["content"])
        
        if prompt := st.chat_input("How can I help you today?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Simple Bot Response (Can be connected to OpenAI)
            st.session_state.messages.append({"role": "assistant", "content": f"I'm analyzing your request about: '{prompt}'. Currently, I'm in beta mode."})
            st.rerun()

    elif menu in ["Tools", "الأدوات"]:
        st.title("⚒️ Real Estate Tools")
        t1, t2 = st.columns(2)
        with t1:
            with st.expander("🧮 Mortgage Calculator", expanded=True):
                price = st.number_input("Property Price", value=1000000)
                down = st.number_input("Down Payment", value=100000)
                months = st.slider("Installment Months", 12, 120, 60)
                if st.button("Calculate"):
                    res = (price - down) / months
                    st.success(f"Monthly Installment: {res:,.2f}")
        with t2:
            st.button("📈 Market ROI Tracker", use_container_width=True)
            st.button("📄 PDF Brochure Generator", use_container_width=True)
            st.button("🌍 Currency Converter", use_container_width=True)

    else:
        search = st.text_input(L["search"])
        # Filter Logic
        col_name = 'ProjectName' if 'ProjectName' in active_df.columns else ('Project' if 'Project' in active_df.columns else 'Developer')
        filtered = active_df[active_df[col_name].str.contains(search, case=False)] if search else active_df
        
        grid = st.columns(3)
        for i, (orig_idx, r) in enumerate(filtered.iterrows()):
            with grid[i % 3]:
                title = r[col_name]
                sub = r.get('Developer', r.get('Location', 'Premium Partner'))
                icon = "🏗️" if menu in ["Projects", "المشاريع"] else ("🚀" if menu in ["Launches", "اللونشات"] else "🏆")
                if st.button(f"{icon} {title}\n───\n{sub}", key=f"card_{i}"):
                    st.session_state.selected_idx = orig_idx; st.rerun()

st.markdown("<br><p style='text-align:center; color:#555;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
