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

# --- 3. Session State & Language ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

trans = {
    "EN": {
        "title": "MA3LOMATI", "subtitle": "LUXURY REAL ESTATE INTELLIGENCE",
        "logout": "Logout", "back": "← Back", "search": "Search projects...",
        "dev_search": "Search developers...", "login": "Login", "pass": "Password",
        "menu": ["Tools", "Developers", "Projects", "AI", "Launches"],
        "fields": ["Location", "Payment Plan", "Developer", "Project Details"]
    },
    "AR": {
        "title": "معلوماتي", "subtitle": "ذكاء السوق العقاري الفاخر",
        "logout": "خروج", "back": "→ عودة", "search": "ابحث عن مشروع...",
        "dev_search": "ابحث عن شركة...", "login": "دخول", "pass": "كلمة المرور",
        "menu": ["الأدوات", "المطورين", "المشاريع", "الذكاء الاصطناعي", "اللونشات"],
        "fields": ["الموقع", "نظام السداد", "المطور", "تفاصيل المشروع"]
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
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {direction} !important; 
        text-align: {"right" if direction=="rtl" else "left"} !important; 
        font-family: 'Cairo', sans-serif;
    }}

    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('{HEADER_IMG}');
        background-size: cover; background-position: center;
        border-bottom: 3px solid #f59e0b;
        padding: 55px 20px; text-align: center;
        border-radius: 0 0 50px 50px; margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }}

    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.95) !important;
        color: #FFFFFF !important;
        border: 1px solid #444 !important;
        border-top: 4px solid #f59e0b !important;
        border-radius: 12px !important;
        height: 110px !important;
        width: 100% !important;
        font-size: 20px !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 4px #000;
        transition: 0.3s ease-in-out;
    }}
    
    div.stButton > button:hover {{
        transform: translateY(-5px);
        background: #f59e0b !important;
        color: #000 !important;
        border-color: #f59e0b !important;
        text-shadow: none;
    }}

    .info-card {{ background: rgba(0,0,0,0.8); padding: 30px; border-radius: 20px; border: 1px solid #333; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 14px; }}
    
    .stButton > button[key="logout_btn"] {{
        background: transparent !important; color: #ff4b4b !important;
        border: 1px solid #ff4b4b !important; border-radius: 10px !important;
    }}
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

# --- 6. Auth ---
if not st.session_state.auth:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div style='height:150px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='info-card' style='text-align:center;'><h1 style='color:#f59e0b;'>{L['title']}</h1>", unsafe_allow_html=True)
        pwd = st.text_input(L['pass'], type="password")
        if st.button(L['login'], use_container_width=True):
            if pwd == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- 7. Layout ---
df_p, df_d, df_l = get_data()

st.markdown(f"""
    <div class="royal-header">
        <h1 style="color: #f59e0b; font-size: 55px; margin: 0; font-weight: 900; text-shadow: 2px 2px 10px #000;">{L['title']}</h1>
        <p style="color: #fff; letter-spacing: 4px; font-weight: bold;">{L['subtitle']}</p>
    </div>
""", unsafe_allow_html=True)

# شريط التنقل - تم إصلاح الأقواس هنا (Single brackets for Python)
col_menu, col_lang, col_out = st.columns([0.7, 0.15, 0.15])
with col_menu:
    menu = option_menu(None, L["menu"], default_index=4, orientation="horizontal",
        styles={
            "nav-link-selected": {"background-color": "#f59e0b", "color": "black"},
            "nav-link": {"font-weight": "bold"}
        })
with col_lang:
    if st.button("🌐 EN/AR", use_container_width=True):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"
        st.rerun()
with col_out:
    if st.button(L["logout"], key="logout_btn", use_container_width=True):
        st.session_state.auth = False; st.rerun()

# --- 8. Content View ---
if st.session_state.selected_item is not None:
    it = st.session_state.selected_item
    if st.button(L["back"]): st.session_state.selected_item = None; st.rerun()
    
    c1, c2 = st.columns([0.7, 0.3])
    with c1:
        st.markdown(f"""<div class="info-card">
            <h1 style="color:#f59e0b;">{it.get('ProjectName', it.get('Project', it.get('Developer')))}</h1>
            <p class="label-gold">{L['fields'][0]}</p><h3>{it.get('Location','---')}</h3>
            <p class="label-gold">{L['fields'][3]}</p><p style="font-size:20px; line-height:1.7;">{it.get('Unique Selling Points (USP)', it.get('Notes','---'))}</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="info-card">
            <p class="label-gold">{L['fields'][1]}</p><h4>{it.get('Price & Payment','---')}</h4>
            <p class="label-gold">{L['fields'][2]}</p><h4>{it.get('Developer','---')}</h4>
        </div>""", unsafe_allow_html=True)

else:
    if menu in ["Launches", "اللونشات"]:
        grid = st.columns(3)
        for i, r in df_l.iterrows():
            with grid[i % 3]:
                if st.button(f"{r['Project']}", key=f"card_l_{i}"):
                    st.session_state.selected_item = r; st.rerun()

    elif menu in ["Projects", "المشاريع"]:
        c_m, c_s = st.columns([0.8, 0.2])
        with c_s: search = st.text_input(L["search"])
        with c_m:
            dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
            grid = st.columns(3)
            for i, r in dff.head(15).reset_index().iterrows():
                with grid[i % 3]:
                    if st.button(f"{r['ProjectName']}", key=f"card_p_{i}"):
                        st.session_state.selected_item = r; st.rerun()

    elif menu in ["Developers", "المطورين"]:
        c_m, c_s = st.columns([0.8, 0.2])
        with c_s: d_search = st.text_input(L["dev_search"])
        with c_m:
            dfd = df_d[df_d['Developer'].str.contains(d_search, case=False)] if d_search else df_d
            grid_d = st.columns(3)
            for i, r in dfd.head(15).reset_index().iterrows():
                with grid_d[i % 3]:
                    if st.button(f"{r['Developer']}", key=f"card_d_{i}"):
                        st.session_state.selected_item = r; st.rerun()

st.markdown(f"<p style='text-align:center; color:#555; margin-top:50px;'>{L['title']} PRO © 2026</p>", unsafe_allow_html=True)
