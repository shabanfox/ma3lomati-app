import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. SESSION MANAGEMENT ---
if 'auth' not in st.session_state:
    if "u_session" in st.query_params:
        st.session_state.auth = True
        st.session_state.current_user = st.query_params["u_session"]
    else:
        st.session_state.auth = False

for key in ['current_user', 'view', 'current_index', 'page_num', 'messages']:
    if key not in st.session_state: 
        st.session_state[key] = None if key == 'current_user' else ("grid" if key == 'view' else ([] if key == 'messages' else 0))

# --- 3. CONSTANTS ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 4. CSS DESIGN ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Poppins:wght@300;600&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    /* Auth Styling */
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; padding-top: 50px; }}
    .oval-header {{ background: #000; border: 2px solid #f59e0b; border-radius: 50px; padding: 10px 40px; color: #f59e0b; font-size: 22px; font-weight: 900; margin-bottom: -25px; z-index: 10; font-family: 'Poppins'; }}
    .auth-card {{ background: white; width: 350px; padding: 40px 30px; border-radius: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
    /* Main UI */
    .royal-header {{ background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('{HEADER_IMG}'); background-size: cover; border-bottom: 3px solid #f59e0b; padding: 40px; text-align: center; border-radius: 0 0 30px 30px; }}
    .detail-card {{ background: rgba(30, 30, 30, 0.6); padding: 20px; border-radius: 15px; border: 1px solid #444; margin-bottom: 10px; }}
    .label-gold {{ color: #f59e0b; font-weight: bold; font-size: 14px; margin-bottom: 2px; }}
    .val-white {{ color: #eee; font-size: 16px; border-bottom: 1px solid #333; padding-bottom: 5px; margin-bottom: 12px; }}
    /* Buttons */
    div.stButton > button {{ border-radius: 10px !important; transition: 0.3s; }}
    div.stButton > button[key*="card_"] {{ 
        background: #fff !important; color: #222 !important; border-right: 8px solid #f59e0b !important; 
        text-align: right !important; height: auto !important; min-height: 120px !important; padding: 15px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. FUNCTIONS ---
def logout():
    st.session_state.auth = False
    st.query_params.clear()
    st.rerun()

def render_grid(dataframe, prefix):
    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ Back to List", key=f"back_{prefix}", use_container_width=True): 
            st.session_state.view = "grid"; st.rerun()
        
        item = dataframe.iloc[st.session_state.current_index]
        cols = st.columns(3)
        all_cols = dataframe.columns
        for i, chunk in enumerate([all_cols[j:j+5] for j in range(0, len(all_cols), 5)]):
            with cols[i % 3]:
                h = '<div class="detail-card">'
                for k in chunk: h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                st.markdown(h+'</div>', unsafe_allow_html=True)
    else:
        search = st.text_input("🔍 Search Database...", key=f"search_{prefix}", placeholder="Type developer, location, or project name...")
        filt = dataframe[dataframe.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else dataframe
        
        start = st.session_state.page_num * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.75, 0.25])
        with m_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    card_content = f"🏘️ {r[0]}\n📍 {r.get('Location','N/A')}\n🏢 {r.get('Developer','N/A')}"
                    if st.button(card_content, key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
            
            # Pagination
            p1, p_info, p2 = st.columns([1, 2, 1])
            if st.session_state.page_num > 0:
                with p1: 
                    if st.button("Previous", key=f"prev_{prefix}"): st.session_state.page_num -= 1; st.rerun()
            with p_info: st.markdown(f"<p style='text-align:center; color:#f59e0b;'>Page {st.session_state.page_num + 1}</p>", unsafe_allow_html=True)
            if (start + ITEMS_PER_PAGE) < len(filt):
                with p2: 
                    if st.button("Next", key=f"next_{prefix}"): st.session_state.page_num += 1; st.rerun()

        with s_c:
            st.markdown("<p style='color:#f59e0b; font-weight:bold; border-bottom:1px solid #333;'>⭐ Featured</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(8).iterrows():
                if st.button(f"📌 {str(s_row[0])[:20]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()

# --- 6. LOGIN ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'><div class='oval-header'>MA3LOMATI PRO</div><div class='auth-card'>", unsafe_allow_html=True)
    u = st.text_input("Username", key="log_u")
    p = st.text_input("Password", type="password", key="log_p")
    if st.button("ACCESS SYSTEM 🚀", use_container_width=True):
        if p == "2026" or p == "admin": 
            st.session_state.auth, st.session_state.current_user = True, "Admin"
            st.rerun()
        else: st.error("Invalid Credentials")
    st.markdown("</div></div>", unsafe_allow_html=True); st.stop()

# --- 7. DATA LOADING ---
@st.cache_data(ttl=60)
def load_all_data():
    try:
        urls = {
            "p": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv",
            "d": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv",
            "l": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
        }
        p, d, l = pd.read_csv(urls["p"]), pd.read_csv(urls["d"]), pd.read_csv(urls["l"])
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_all_data()

# --- 8. MAIN INTERFACE ---
st.markdown(f'<div class="royal-header"><h1 style="color:white; margin:0;">MA3LOMATI PRO</h1><p style="color:#f59e0b;">Welcome, {st.session_state.current_user} | 2026 Edition</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["Brokerage Tools", "Developers", "Projects", "AI Assistant"], 
    icons=["calculator", "building", "grid-3x3", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link": {"font-family": "Poppins", "font-size": "14px"}, "nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.page_num, st.session_state.last_m = "grid", 0, menu

# --- 9. SECTIONS ---
if menu == "Brokerage Tools":
    st.markdown("<h3 style='color:#f59e0b; text-align:center;'>Financial Calculators</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='detail-card'><h4>💰 Mortgage</h4>", unsafe_allow_html=True)
        price = st.number_input("Property Price", value=5000000)
        down_p = st.number_input("Down Payment %", value=10)
        years = st.number_input("Years", value=8)
        monthly = (price - (price * down_p/100)) / (years * 12) if years > 0 else 0
        st.markdown(f"<p class='label-gold'>Monthly Installment</p><p class='val-white'>{monthly:,.0f} EGP</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='detail-card'><h4>📊 Commission</h4>", unsafe_allow_html=True)
        deal = st.number_input("Deal Value", value=5000000)
        comm_pct = st.number_input("Commission %", value=2.5)
        st.markdown(f"<p class='label-gold'>Your Profit</p><p class='val-white'>{deal*(comm_pct/100):,.0f} EGP</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='detail-card'><h4>📈 ROI</h4>", unsafe_allow_html=True)
        inv = st.number_input("Investment", value=5000000)
        rent = st.number_input("Monthly Rent", value=40000)
        roi = ((rent * 12) / inv) * 100 if inv > 0 else 0
        st.markdown(f"<p class='label-gold'>Annual Yield</p><p class='val-white'>{roi:.2f} %</p></div>", unsafe_allow_html=True)

elif menu == "Projects":
    t1, t2 = st.tabs(["🏗️ All Projects", "🚀 New Launches"])
    with t1: render_grid(df_p, "proj")
    with t2: render_grid(df_l, "launch")

elif menu == "Developers":
    render_grid(df_d, "dev")

elif menu == "AI Assistant":
    st.markdown("<div class='detail-card'><h4>🤖 Real Estate AI Intelligence</h4><p style='font-size:12px; color:#888;'>Powered by Gemini 2026 - Data Driven Analysis</p></div>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.write(msg["content"])
    
    if prompt := st.chat_input("Ask me anything about the projects..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)
        with st.chat_message("assistant"):
            response = f"I am currently indexing {len(df_p)} projects to answer your question about: {prompt}"
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if st.button("Logout"): logout()
st.markdown("<p style='text-align:center; color:#444; margin-top:30px; font-family:Poppins;'>MA3LOMATI PRO © 2026 | Digital Excellence</p>", unsafe_allow_html=True)
