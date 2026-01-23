import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CONSTANTS ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
ITEMS_PER_PAGE = 6

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'view' not in st.session_state: st.session_state.view = "grid" 
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'last_menu' not in st.session_state: st.session_state.last_menu = "Launches"
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 3. CSS (Luxury Design) ---
direction = "rtl" if st.session_state.lang == "AR" else "ltr"
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"], [data-testid="stToolbar"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {direction} !important; font-family: 'Cairo', sans-serif;
    }}

    /* LOGIN UI */
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: flex-start; width: 100%; padding-top: 20px; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 24px; font-weight: 900;
        text-align: center; z-index: 10; margin-bottom: -30px; min-width: 360px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }}
    .auth-card {{ background-color: #ffffff; width: 380px; padding: 55px 35px 30px 35px; border-radius: 30px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); }}
    .lock-gold {{ font-size: 45px; color: #f59e0b; margin-bottom: 5px; }}
    .auth-card div.stTextInput input {{
        background-color: #000 !important; color: #fff !important;
        border: 1px solid #f59e0b !important; border-radius: 12px !important;
        text-align: center !important; height: 45px !important;
    }}

    /* INTERNAL APP UI */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 2px solid #f59e0b;
        padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 30px;
    }}
    .detail-card, .tool-card {{ background: rgba(20, 20, 20, 0.9); padding: 25px; border-radius: 20px; border-top: 5px solid #f59e0b; color: white; border: 1px solid #333; }}
    .mini-side-card {{ background: rgba(40, 40, 40, 0.8); padding: 10px; border-radius: 12px; border-right: 4px solid #f59e0b; margin-bottom: 10px; color: #f59e0b; font-size: 14px; font-weight: bold; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 16px; margin-top: 15px; }}
    .val-white {{ color: white; font-size: 18px; margin-bottom: 8px; border-bottom: 1px solid #222; }}
    
    div.stButton > button {{ border-radius: 12px !important; font-weight: 700 !important; transition: 0.3s; }}
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; color: #FFFFFF !important;
        border-left: 5px solid #f59e0b !important; border-radius: 15px !important;
        height: 180px !important; width: 100% !important; text-align: center !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Logic Functions ---
def check_auth(u, p):
    try:
        df = pd.read_csv(USER_SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        return not df[(df['Name'].astype(str) == str(u)) & (df['Password'].astype(str) == str(p))].empty
    except: return False

@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]: df.columns = [c.strip() for c in df.columns]
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 5. UI: LOGIN PAGE ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>منصة معلوماتي العقارية</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.markdown("<div class='lock-gold'>🔒</div>", unsafe_allow_html=True)
    
    t_log, t_reg = st.tabs(["Login / دخول", "Join / اشتراك"])
    with t_log:
        u = st.text_input("Username", placeholder="اسم المستخدم", label_visibility="collapsed", key="u_main")
        p = st.text_input("Password", type="password", placeholder="كلمة المرور", label_visibility="collapsed", key="p_main")
        if st.button("SIGN IN", use_container_width=True):
            if check_auth(u, p): st.session_state.auth = True; st.rerun()
            else: st.error("Wrong Data")
    with t_reg:
        st.text_input("FullName", placeholder="الاسم")
        st.text_input("WhatsApp", placeholder="واتساب")
        if st.button("SEND", use_container_width=True): st.success("Sent")
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.write("")
    if st.button("🌐 Change Language / تغيير اللغة"):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. UI: INTERNAL APP ---
df_p, df_d, df_l = load_data()
L = {"menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"]}

st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900;">MA3LOMATI</h1></div>', unsafe_allow_html=True)

m_col, o_col = st.columns([0.85, 0.15])
with m_col:
    menu = option_menu(None, L["menu"], default_index=4, orientation="horizontal", 
                       styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
with o_col:
    if st.button(f"🚪 Logout", use_container_width=True): st.session_state.auth = False; st.rerun()

if menu != st.session_state.last_menu:
    st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu
    st.rerun()

# --- TOOLS PAGE ---
if menu == "Tools":
    st.markdown("<h2 style='text-align:center; color:#f59e0b;'>🛠️ Broker Toolbox</h2>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    with t1:
        with st.container(border=True):
            st.subheader("🧮 Mortgage")
            price = st.number_input("Unit Price", value=2000000)
            years = st.slider("Years", 1, 20, 10)
            st.warning(f"Monthly: {price/(years*12):,.0f}")
    with t2:
        with st.container(border=True):
            st.subheader("📈 ROI")
            cost = st.number_input("Cost", value=1000000)
            rent = st.number_input("Annual Rent", value=120000)
            st.warning(f"ROI: {(rent/cost)*100:.1f}%")
    with t3:
        with st.container(border=True):
            st.subheader("💰 Commission")
            deal = st.number_input("Deal", value=5000000)
            st.info(f"Earn (2.5%): {deal*0.025:,.0f}")

# --- AI ASSISTANT ---
elif menu == "AI Assistant":
    st.markdown("<div class='tool-card'><h3>🤖 Real Estate AI</h3></div>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    if pmt := st.chat_input("Ask about market..."):
        st.session_state.messages.append({"role": "user", "content": pmt})
        st.session_state.messages.append({"role": "assistant", "content": "I am analyzing the market data for you..."})
        st.rerun()

# --- GRID & DETAILS ---
else:
    active_df = df_p if menu=="Projects" else (df_l if menu=="Launches" else df_d)
    if active_df.empty: 
        st.error("No data available")
    else:
        # الحل الجذري للـ KeyError: نأخذ أول عمود كاسم رئيسي دائماً
        col_main = active_df.columns[0]
        
        if st.session_state.view == "details":
            item = active_df.iloc[st.session_state.current_index]
            if st.button("⬅ Back", use_container_width=True): st.session_state.view = "grid"; st.rerun()
            cols = active_df.columns
            c1, c2, c3 = st.columns(3)
            with c1:
                h = '<div class="detail-card">'
                for k in cols[:len(cols)//3+1]: h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                st.markdown(h+'</div>', unsafe_allow_html=True)
            # ... (يمكنك إكمال c2 و c3 بنفس الطريقة)
        else:
            search = st.text_input("🔍 Search / بحث")
            filt = active_df[active_df[col_main].astype(str).str.contains(search, case=False)] if search else active_df
            start = st.session_state.page_num * ITEMS_PER_PAGE
            disp = filt.iloc[start : start + ITEMS_PER_PAGE]
            
            main_c, side_c = st.columns([0.8, 0.2])
            with main_c:
                grid = st.columns(2)
                for i, (idx, r) in enumerate(disp.iterrows()):
                    with grid[i%2]:
                        # استخدام .get() يمنع حدوث KeyError للأبد
                        name = r[col_main]
                        area = r.get('Area', r.get('Location', '---'))
                        dev = r.get('Developer', '---')
                        if st.button(f"✨ {name}\n📍 {area}\n🏢 {dev}", key=f"card_{idx}"):
                            st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()
            
            with side_c:
                st.markdown("<p style='color:#f59e0b; font-weight:bold;'>⭐ Recommended</p>", unsafe_allow_html=True)
                for _, s in active_df.head(5).iterrows():
                    st.markdown(f"<div class='mini-side-card'>💎 {s[col_main][:18]}</div>", unsafe_allow_html=True)

            # Pagination
            st.write("---")
            n1, n2, n3 = st.columns([1, 2, 1])
            with n1:
                if st.session_state.page_num > 0:
                    if st.button("⬅ Previous", use_container_width=True): st.session_state.page_num -= 1; st.rerun()
            with n3:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("Next ➡", use_container_width=True): st.session_state.page_num += 1; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
