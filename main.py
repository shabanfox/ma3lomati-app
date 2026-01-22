import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Data URLs ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
URL_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"

# --- 3. Multi-Language Dictionary ---
if 'lang' not in st.session_state: st.session_state.lang = "EN"

text = {
    "EN": {
        "title": "MA3LOMATI",
        "subtitle": "THE REAL ESTATE INTELLIGENCE",
        "logout": "Logout",
        "menu": ["Broker Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "back": "← Back",
        "search": "Search Projects...",
        "dev_search": "Search Developers...",
        "loc": "Location",
        "payment": "Price & Payment",
        "dev": "Developer",
        "details": "Details & USP",
        "login_btn": "Enter Platform",
        "pass_label": "Access Password"
    },
    "AR": {
        "title": "معلوماتي",
        "subtitle": "ذكاء السوق العقاري",
        "logout": "خروج",
        "menu": ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "back": "→ عودة",
        "search": "ابحث عن مشروع...",
        "dev_search": "ابحث عن مطور...",
        "loc": "الموقع",
        "payment": "السعر ونظام السداد",
        "dev": "المطور",
        "details": "التفاصيل والمميزات",
        "login_btn": "دخول المنصة",
        "pass_label": "كلمة مرور النظام"
    }
}

L = text[st.session_state.lang]
direction = "rtl" if st.session_state.lang == "AR" else "ltr"

# --- 4. Enhanced UI CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}

    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), 
        url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1920&q=80');
        background-size: cover; background-attachment: fixed;
        direction: {direction} !important; text-align: {"right" if direction=="rtl" else "left"} !important; 
        font-family: 'Cairo', sans-serif;
    }

    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)),
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80');
        background-size: cover; background-position: center;
        border-bottom: 3px solid #f59e0b;
        padding: 60px 20px; text-align: center;
        border-radius: 0 0 50px 50px; margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
    }}

    div.stButton > button[key*="card_"] {{
        background: rgba(15, 15, 15, 0.95) !important;
        color: #FFFFFF !important;
        border: 1px solid #333 !important;
        border-top: 5px solid #f59e0b !important;
        border-radius: 15px !important;
        min-height: 140px !important;
        width: 100% !important;
        font-size: 18px !important;
        font-weight: 900 !important;
        text-shadow: 2px 2px 4px #000;
    }}
    
    div.stButton > button:hover {{
        transform: translateY(-8px);
        border-color: #f59e0b !important;
        background: #222 !important;
    }}

    .info-card {{ background: rgba(0,0,0,0.8); padding: 25px; border-radius: 20px; border: 1px solid #222; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 14px; text-transform: uppercase; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. Logic & Data ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

@st.cache_data(ttl=60)
def load_data():
    try:
        p = pd.read_csv(URL_P).fillna("---")
        d = pd.read_csv(URL_D).fillna("---")
        l = pd.read_csv(URL_L).fillna("---")
        p.rename(columns={'Area': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d, l
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 6. Login ---
if not st.session_state.auth:
    _, col_login, _ = st.columns([1, 1.2, 1])
    with col_login:
        st.markdown("<div style='height:120px;'></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='info-card' style='text-align:center;'><h1 style='color:#f59e0b;'>{L['title']} PRO</h1>", unsafe_allow_html=True)
        p_in = st.text_input(L['pass_label'], type="password")
        if st.button(L['login_btn'], use_container_width=True):
            if p_in == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- 7. Main App ---
df_p, df_d, df_l = load_data()

# Header Image & Titles
st.markdown(f"""
    <div class="royal-header">
        <h1 style="color: #f59e0b; font-size: 60px; margin: 0; font-weight: 900; text-shadow: 3px 3px 15px #000;">{L['title']}</h1>
        <p style="color: #fff; letter-spacing: 5px; font-weight: bold;">{L['subtitle']}</p>
    </div>
""", unsafe_allow_html=True)

# Top Bar: Lang Switch | Menu | Logout
c_lang, c_menu, c_out = st.columns([0.1, 0.75, 0.15])
with c_lang:
    if st.button("🌐 EN/AR"):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"
        st.rerun()
with c_menu:
    menu = option_menu(None, L["menu"], default_index=4, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
with c_out:
    if st.button(L["logout"], key="logout_btn", use_container_width=True):
        st.session_state.auth = False; st.rerun()

# --- 8. Content ---
if st.session_state.selected_item is not None:
    it = st.session_state.selected_item
    if st.button(L["back"]): st.session_state.selected_item = None; st.rerun()
    
    c1, c2 = st.columns([0.7, 0.3])
    with c1:
        st.markdown(f"""<div class="info-card">
            <h1 style="color:#f59e0b;">{it.get('ProjectName', it.get('Project', it.get('Developer')))}</h1>
            <p class="label-gold">{L['loc']}</p><h3>{it.get('Location','---')}</h3>
            <p class="label-gold">{L['details']}</p><p style="font-size:20px;">{it.get('Unique Selling Points (USP)', it.get('Notes','---'))}</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="info-card">
            <p class="label-gold">{L['payment']}</p><h4>{it.get('Price & Payment','---')}</h4>
            <p class="label-gold">{L['dev']}</p><h4>{it.get('Developer','---')}</h4>
        </div>""", unsafe_allow_html=True)

else:
    if menu in ["Launches", "اللونشات"]:
        cols = st.columns(3)
        for i, r in df_l.iterrows():
            with cols[i % 3]:
                if st.button(f"🚀 {r['Project']}\n{r['Developer']}", key=f"card_l_{i}"):
                    st.session_state.selected_item = r; st.rerun()

    elif menu in ["Projects", "المشاريع"]:
        c_m, c_s = st.columns([0.7, 0.3])
        with c_s:
            search = st.text_input(L["search"])
        with c_m:
            dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
            grid = st.columns(2)
            for i, r in dff.head(10).reset_index().iterrows():
                with grid[i % 2]:
                    if st.button(f"🏗️ {r['ProjectName']}\n📍 {r['Location']}", key=f"card_p_{i}"):
                        st.session_state.selected_item = r; st.rerun()

    elif menu in ["Developers", "المطورين"]:
        c_m, c_s = st.columns([0.7, 0.3])
        with c_s:
            search_d = st.text_input(L["dev_search"])
        with c_m:
            dfd = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
            grid_d = st.columns(2)
            for i, r in dfd.head(10).reset_index().iterrows():
                with grid_d[i % 2]:
                    if st.button(f"🏆 {r['Developer']}", key=f"card_d_{i}"):
                        st.session_state.selected_item = r; st.rerun()

st.markdown(f"<p style='text-align:center; color:#444; margin-top:50px;'>{L['title']} PRO © 2026</p>", unsafe_allow_html=True)
