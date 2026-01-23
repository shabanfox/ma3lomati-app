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
if 'messages' not in st.session_state: st.session_state.messages = []

trans = {
    "EN": {
        "logout": "Logout", "back": "🏠 Back to List",
        "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "side_dev": "⭐ TOP DEVS", "side_proj": "🏠 READY", "search": "Search assets...",
        "det_title": "Project Specifications", "ai_welcome": "How can I help you today?",
        "tool_title": "Professional Broker Tools", "next": "Next ➡", "prev": "⬅ Prev"
    },
    "AR": {
        "logout": "خروج", "back": "🏠 العودة للقائمة",
        "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "side_dev": "⭐ المطورين", "side_proj": "🏠 استلام فوري", "search": "بحث عن عقار...",
        "det_title": "مواصفات وتفاصيل المشروع", "ai_welcome": "كيف يمكنني مساعدتك اليوم؟",
        "tool_title": "أدوات البروكر المحترف", "next": "التالي ➡", "prev": "⬅ السابق"
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
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; color: #FFFFFF !important;
        border-left: 5px solid #f59e0b !important; border-radius: 15px !important;
        height: 200px !important; width: 100% !important;
        text-align: {"right" if direction=="rtl" else "left"} !important;
        font-size: 16px !important; line-height: 1.6 !important;
    }}
    .detail-card, .tool-card {{
        background: rgba(20, 20, 20, 0.95); padding: 30px; border-radius: 20px;
        border: 1px solid #333; border-top: 5px solid #f59e0b; margin-top: 10px;
        color: white; min-height: 200px;
    }}
    /* كلاس مصغر مخصص فقط للجانب */
    .mini-side-card {{
        background: rgba(30, 30, 30, 0.8); padding: 10px; border-radius: 10px;
        border: 1px solid #444; border-right: 4px solid #f59e0b;
        margin-bottom: 8px; color: #f59e0b; font-size: 13px; font-weight: bold;
    }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 18px; margin-top: 20px; }}
    .val-white {{ color: white; font-size: 20px; margin-bottom: 10px; }}
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

c_menu, c_lang, c_out = st.columns([0.7, 0.15, 0.15])
with c_menu:
    menu_selection = option_menu(None, L["menu"], default_index=2, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
    
    if menu_selection != st.session_state.last_menu:
        st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu_selection
        st.rerun()

with c_lang:
    if st.button("🌐 EN/AR", use_container_width=True):
        st.session_state.lang = "AR" if st.session_state.lang == "EN" else "EN"; st.rerun()
with c_out:
    if st.button(f"🚪 {L['logout']}", use_container_width=True): st.session_state.auth = False; st.rerun()

# --- 6. View Logic ---

if menu_selection in ["Tools", "الأدوات"]:
    st.markdown(f"<h2 style='color:#f59e0b; text-align:center;'>⚒️ {L['tool_title']}</h2>", unsafe_allow_html=True)
    t1, t2, t3 = st.columns(3)
    with t1:
        with st.container(border=True):
            st.subheader("🧮 Mortgage / القسط")
            p_val = st.number_input("Amount", 0, key="t1_p")
            y_val = st.number_input("Years", 1, 20, 7)
            if p_val > 0: st.warning(f"Monthly: {p_val/(y_val*12):,.2f}")
        with st.container(border=True):
            st.subheader("📏 Area / المساحة")
            m_val = st.number_input("SQM / متر", 0.0)
            st.info(f"SQFT: {m_val * 10.76:.2f}")
    with t2:
        with st.container(border=True):
            st.subheader("📈 ROI / العائد")
            c_val = st.number_input("Cost", 1)
            r_val = st.number_input("Annual Rent", 0)
            st.warning(f"ROI: {(r_val/c_val)*100:.2f}%")
        with st.container(border=True):
            st.subheader("💰 Commission / العمولة")
            v_val = st.number_input("Deal Value", 0)
            perc_val = st.slider("%", 1.0, 5.0, 2.5)
            st.info(f"Earn: {v_val*(perc_val/100):,.0f}")
    with t3:
        with st.container(border=True):
            st.subheader("🌍 Currency / العملة")
            u_val = st.number_input("USD Amount", 0.0)
            rate_val = st.number_input("Rate", 40.0, 70.0, 50.0)
            st.warning(f"EGP: {u_val*rate_val:,.2f}")
        with st.container(border=True):
            st.subheader("✍️ AI Script / نص بيعي")
            proj_val = st.text_input("Project Name")
            if st.button("Create Script"): st.code(f"Invest now in {proj_val}! Exclusive luxury units available.")

elif menu_selection in ["AI Assistant", "المساعد الذكي"]:
    st.markdown(f"<div class='tool-card'><h3>🤖 MA3LOMATI AI</h3><p>{L['ai_welcome']}</p></div>", unsafe_allow_html=True)
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])
    if prompt := st.chat_input("Ask about market trends..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.messages.append({"role": "assistant", "content": f"Analyzing market data for: {prompt}..."})
        st.rerun()

else:
    is_launch = menu_selection in ["Launches", "اللونشات"]
    if menu_selection in ["Projects", "المشاريع"]: 
        active_df, col_main_name = df_p, 'Project Name' if 'Project Name' in df_p.columns else df_p.columns[0]
    elif is_launch: 
        active_df, col_main_name = df_l, 'Project' if 'Project' in df_l.columns else df_l.columns[0]
    else: 
        active_df, col_main_name = df_d, 'Developer' if 'Developer' in df_d.columns else df_d.columns[0]

    if st.session_state.view == "details":
        item = active_df.iloc[st.session_state.current_index]
        cols = active_df.columns
        if st.button(L["back"], use_container_width=True): st.session_state.view = "grid"; st.rerun()
        c1, c2, c3 = st.columns(3)
        split = max(1, len(cols) // 3)
        with c1:
            h1 = f'<div class="detail-card"><h3 style="color:#f59e0b;">💎 Info</h3>'
            for k in cols[:split]: h1 += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
            st.markdown(h1+'</div>', unsafe_allow_html=True)
        with c2:
            h2 = f'<div class="detail-card"><h3 style="color:#f59e0b;">📍 Details</h3>'
            for k in cols[split:split*2]: h2 += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
            st.markdown(h2+'</div>', unsafe_allow_html=True)
        with c3:
            h3 = f'<div class="detail-card"><h3 style="color:#f59e0b;">💰 More</h3>'
            for k in cols[split*2:]: h3 += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
            st.markdown(h3+'</div>', unsafe_allow_html=True)
    else:
        search = st.text_input(L["search"])
        filtered = active_df[active_df[col_main_name].astype(str).str.contains(search, case=False)] if search else active_df
        start_idx = st.session_state.page_num * ITEMS_PER_PAGE
        display_df = filtered.iloc[start_idx : start_idx + ITEMS_PER_PAGE]

        if is_launch:
            grid = st.columns(3)
            for i, (orig_idx, r) in enumerate(display_df.iterrows()):
                with grid[i % 3]:
                    if st.button(f"🚀 {r[col_main_name]}\n📍 {r.get('Area','---')}\n🏢 {r.get('Developer','---')}", key=f"card_{orig_idx}"):
                        st.session_state.current_index, st.session_state.view = orig_idx, "details"; st.rerun()
        else:
            # تم تعديل النسبة لتصغير العمود الجانبي أكثر
            c_main, c_side = st.columns([0.8, 0.2])
            with c_main:
                grid = st.columns(2)
                for i, (orig_idx, r) in enumerate(display_df.iterrows()):
                    with grid[i % 2]:
                        if st.button(f"✨ {r[col_main_name]}\n📍 {r.get('Area','---')}\n🏢 {r.get('Developer','---')}", key=f"card_{orig_idx}"):
                            st.session_state.current_index, st.session_state.view = orig_idx, "details"; st.rerun()
            with c_side:
                st.markdown(f"<p style='color:#f59e0b; font-weight:bold; font-size:14px;'>{L['side_dev'] if menu_selection=='Developers' else L['side_proj']}</p>", unsafe_allow_html=True)
                for _, s in active_df.head(6).iterrows():
                    # استخدام التصميم المصغر الجديد هنا
                    st.markdown(f"<div class='mini-side-card'>💎 {s[col_main_name][:20]}</div>", unsafe_allow_html=True)

        st.write("---")
        nav_c1, nav_c2 = st.columns(2)
        with nav_c1:
            if st.session_state.page_num > 0:
                if st.button(L["prev"], use_container_width=True):
                    st.session_state.page_num -= 1; st.rerun()
        with nav_c2:
            if (start_idx + ITEMS_PER_PAGE) < len(filtered):
                if st.button(L["next"], use_container_width=True):
                    st.session_state.page_num += 1; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
