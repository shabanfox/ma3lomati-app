import streamlit as st
import pandas as pd
import requests
import feedparser
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. الرابط الخاص بك
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# 3. إدارة حالة الجلسة (لضمان الثبات)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- وظائف الجلب ---
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

@st.cache_data(ttl=1800)
def get_real_news():
    try:
        feed = feedparser.parse("https://www.youm7.com/rss/SectionRss?SectionID=297")
        return "  •  ".join([item.title for item in feed.entries[:10]])
    except: return "MA3LOMATI PRO 2026: بوابة العقارات الذكية"

# 4. التنسيق الجمالي (CSS الشامل)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container { padding-top: 0rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; }
    
    /* فرض الـ RTL في كل مكان */
    [data-testid="stAppViewContainer"] { 
        background-color: #050505; 
        direction: rtl !important; 
        text-align: right !important; 
        font-family: 'Cairo', sans-serif;
    }

    /* شريط الأخبار (يتحرك لليسار لسهولة القراءة) */
    .ticker-wrap { background: #111; padding: 10px 0; border-bottom: 1px solid #f59e0b; direction: ltr !important; }
    .ticker { display: inline-block; animation: ticker 150s linear infinite; color: white; font-size: 14px; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    /* تنسيق الكروت */
    div.stButton > button[key*="card_"] {
        background: white !important; color: black !important;
        height: 120px !important; border-radius: 15px !important;
        font-weight: bold !important; font-size: 16px !important;
        border: none !important; width: 100% !important;
    }
    
    .smart-box { background: #161616; border: 1px solid #333; padding: 20px; border-radius: 15px; border-right: 5px solid #f59e0b; color: white; margin-bottom: 15px; }
    .tool-card { background: #1a1a1a; padding: 15px; border-radius: 15px; border-top: 3px solid #f59e0b; text-align: center; }
    
    /* جعل التبويبات سنتر */
    .stTabs [data-baseweb="tab-list"] { justify-content: center; direction: ltr !important; }
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول (Centered)
if not st.session_state.auth:
    _, col_mid, _ = st.columns([1, 1.2, 1])
    with col_mid:
        st.markdown("<br><br><br><div style='text-align:center;'><h1 style='color:#f59e0b; font-size:50px;'>MA3LOMATI</h1><p style='color:#888;'>PRO 2026</p></div>", unsafe_allow_html=True)
        u_in = st.text_input("Username", key="u_login")
        p_in = st.text_input("Password", type="password", key="p_login")
        if st.button("LOGIN 🚀", use_container_width=True):
            if p_in == "2026" or u_in == "admin": # مثال بسيط للتجربة
                st.session_state.auth = True
                st.session_state.current_user = u_in
                st.rerun()
    st.stop()

# 6. الهيدر وزر الخروج (اليسار)
col_logout, col_empty = st.columns([0.2, 0.8])
with col_logout:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 خروج", key="logout_btn"):
        st.session_state.auth = False; st.rerun()

st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab'); 
                height: 140px; background-size: cover; background-position: center; border-radius: 25px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b;">
        <h1 style="color: white; margin: 0;">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b;">مرحباً بك يا {st.session_state.current_user}</p>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {get_real_news()}</div></div>', unsafe_allow_html=True)

# 7. المنيو الرئيسي
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["briefcase", "building", "search", "robot"], default_index=3, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# 8. عرض المحتوى
if st.session_state.selected_item is not None:
    if st.button("➡️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
    st.markdown(f"<div class='smart-box'><h2>{st.session_state.selected_item.get('ProjectName', 'التفاصيل')}</h2></div>", unsafe_allow_html=True)

elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'><h3>🤖 المساعد العقاري الذكي</h3><p>أدخل بيانات طلب العميل...</p></div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    m_col, s_col = st.columns([0.75, 0.25]) # المشاريع يمين، القائمة يسار
    with s_col: # العمود الأيسر
        st.markdown("<h4 style='color:#f59e0b; text-align:center;'>🚀 استلام فوري</h4>", unsafe_allow_html=True)
        for i, r in df_p.head(5).iterrows():
            st.markdown(f"<div class='smart-box' style='padding:10px;'>{r['ProjectName']}</div>", unsafe_allow_html=True)
    with m_col: # العمود الأيمن
        search = st.text_input("🔍 ابحث عن مشروع...")
        dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
        page = dff.iloc[st.session_state.p_idx*6 : st.session_state.p_idx*6+6]
        for i in range(0, len(page), 2):
            c = st.columns(2)
            for j in range(2):
                if i+j < len(page):
                    row = page.iloc[i+j]
                    if c[j].button(f"{row['ProjectName']}\n📍 {row['Location']}", key=f"card_p_{i+j}"):
                        st.session_state.selected_item = row; st.rerun()

elif menu == "المطورين":
    m_col, s_col = st.columns([0.75, 0.25]) # المطورين يمين، القائمة يسار
    with s_col: # العمود الأيسر
        st.markdown("<h4 style='color:#f59e0b; text-align:center;'>🏆 كبار المطورين</h4>", unsafe_allow_html=True)
        for i, r in df_d.head(5).iterrows():
            st.markdown(f"<div class='smart-box' style='padding:10px;'>{r['Developer']}</div>", unsafe_allow_html=True)
    with m_col: # العمود الأيمن
        search_d = st.text_input("🔍 ابحث عن مطور...")
        dfd_f = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
        page_d = dfd_f.iloc[st.session_state.d_idx*6 : st.session_state.d_idx*6+6]
        for i in range(0, len(page_d), 2):
            c = st.columns(2)
            for j in range(2):
                if i+j < len(page_d):
                    row = page_d.iloc[i+j]
                    if c[j].button(f"{row['Developer']}\n⭐ Rating: A", key=f"card_d_{i+j}"):
                        st.session_state.selected_item = row; st.rerun()

elif menu == "أدوات البروكر":
    st.markdown("<h2 style='text-align: center; color: #f59e0b;'>🛠️ أدوات البروكر العقاري</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)
    tools = [c1, c2, c3, c4, c5, c6]
    labels = ["💳 القسط", "💰 العمولة", "📈 ROI", "📐 المساحة", "📝 الضريبة", "🏦 التمويل"]
    for i, tool in enumerate(tools):
        with tool:
            st.markdown(f"<div class='tool-card'><h4>{labels[i]}</h4></div>", unsafe_allow_html=True)
            st.number_input("أدخل القيمة", key=f"tool_{i}")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
