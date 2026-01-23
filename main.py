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
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'last_menu' not in st.session_state: st.session_state.last_menu = "Projects"

trans = {
    "EN": {
        "menu": ["Tools", "Developers", "Projects", "AI Assistant", "Launches"],
        "back": "⬅ Back", "search": "Search...",
        "owner": "Chairman / Owner", "about": "Company Details", "projects": "Key Projects"
    },
    "AR": {
        "menu": ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"],
        "back": "⬅ العودة للقائمة", "search": "ابحث عن المطور أو المشروع...",
        "owner": "المالك / رئيس مجلس الإدارة", "about": "عن الشركة", "projects": "أهم المشاريع"
    }
}
L = trans[st.session_state.lang]
direction = "rtl" if st.session_state.lang == "AR" else "ltr"

# --- 3. Custom CSS (The Cards) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)), url('{BG_IMG}');
        background-size: cover; direction: {direction}; font-family: 'Cairo', sans-serif;
    }}
    /* The Developer Card Styling */
    .dev-card {{
        background: rgba(30, 30, 30, 0.8);
        border: 1px solid #444;
        border-right: 5px solid #f59e0b;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        transition: 0.3s;
    }}
    .dev-card:hover {{
        background: rgba(45, 45, 45, 1);
        transform: translateY(-5px);
        border-color: #f59e0b;
    }}
    .dev-card-title {{ color: #f59e0b; font-size: 22px; font-weight: 900; margin-bottom: 5px; }}
    .dev-card-owner {{ color: #bbb; font-size: 14px; }}
    
    /* Detail Page Container */
    .detail-container {{
        background: rgba(20, 20, 20, 0.95);
        padding: 40px; border-radius: 20px;
        border-top: 6px solid #f59e0b;
    }}
    .detail-section-title {{
        color: #f59e0b; font-size: 20px; font-weight: 700;
        margin-top: 30px; margin-bottom: 10px;
        display: flex; align-items: center; gap: 10px;
    }}
    .detail-text {{ color: #fff; font-size: 18px; line-height: 1.8; text-align: justify; }}
    
    /* Buttons Customization */
    div.stButton > button {{ width: 100% !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Load Data ---
@st.cache_data(ttl=60)
def load_data():
    URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    try:
        df = pd.read_csv(URL_D).fillna("---")
        df.columns = [c.strip() for c in df.columns]
        return df
    except: return pd.DataFrame()

df_d = load_data()

# --- 5. Navigation ---
menu_selection = option_menu(None, L["menu"], default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if menu_selection != st.session_state.last_menu:
    st.session_state.view = "grid"; st.session_state.last_menu = menu_selection; st.rerun()

# --- 6. View Logic ---
if menu_selection in ["Developers", "المطورين"]:
    
    if st.session_state.view == "details":
        # صفحة التفاصيل المقسمة
        item = df_d.iloc[st.session_state.current_index]
        if st.button(L["back"]): st.session_state.view = "grid"; st.rerun()
        
        st.markdown(f"""
        <div class="detail-container">
            <h1 style="color:#f59e0b; text-align:center; font-size:40px;">{item.get('Developer', '---')}</h1>
            <hr style="border-color:#333;">
            
            <div class="detail-section-title">👤 {L['owner']}</div>
            <div class="detail-text">{item.get('Owner / Chairman', '---')}</div>
            
            <div class="detail-section-title">🏢 {L['about']}</div>
            <div class="detail-text">{item.get('Company Details', '---')}</div>
            
            <div class="detail-section-title">🏗️ {L['projects']}</div>
            <div class="detail-text">{item.get('Key Projects', '---')}</div>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        # صفحة الكروت (Grid)
        search = st.text_input(L["search"])
        filtered = df_d[df_d['Developer'].astype(str).str.contains(search, case=False)] if search else df_d
        
        cols = st.columns(2)
        for i, (orig_idx, row) in enumerate(filtered.iterrows()):
            with cols[i % 2]:
                # رسم الكارت باستخدام HTML
                st.markdown(f"""
                <div class="dev-card">
                    <div class="dev-card-title">{row['Developer']}</div>
                    <div class="dev-card-owner">📍 {row.get('Owner / Chairman', '---')[:50]}...</div>
                </div>
                """, unsafe_allow_html=True)
                # زر الشفافية فوق الكارت للدخول للتفاصيل
                if st.button(f"عرض تفاصيل {row['Developer']}", key=f"btn_{orig_idx}"):
                    st.session_state.current_index = orig_idx
                    st.session_state.view = "details"
                    st.rerun()

else:
    st.warning("هذا القسم قيد التجهيز بمجرد ربط الشيتات الأخرى.")
