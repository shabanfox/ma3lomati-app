import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. روابط البيانات ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
URL_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- 4. وظائف الربط مع جوجل شيت ---
def login_user_from_sheet(u_in, p_in):
    try:
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}")
        if response.status_code == 200:
            users = response.json()
            for user in users:
                u_name = str(user.get('Name', user.get('name', ''))).strip().lower()
                u_email = str(user.get('Email', user.get('email', ''))).strip().lower()
                u_pass = str(user.get('Password', user.get('password', ''))).strip()
                if (u_in.strip().lower() == u_name or u_in.strip().lower() == u_email) and str(p_in).strip() == u_pass:
                    return user.get('Name', user.get('name', 'User'))
        return None
    except: return None

@st.cache_data(ttl=60)
def load_all_data():
    try:
        p = pd.read_csv(URL_P).fillna("---")
        d = pd.read_csv(URL_D).fillna("---")
        l = pd.read_csv(URL_L).fillna("---")
        for df in [p, d, l]: df.columns = df.columns.str.strip()
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d, l
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 5. التنسيق الجمالي (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    .main-header {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1600&q=80');
        height: 180px; background-size: cover; background-position: center;
        border-radius: 0 0 40px 40px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b; margin-bottom: 20px;
    }}

    div.stButton > button {{ border-radius: 12px !important; font-family: 'Cairo' !important; transition: 0.3s !important; }}
    div.stButton > button[key*="card_"] {{
        background: #161616 !important; color: white !important;
        min-height: 130px !important; border: 1px solid #333 !important;
        border-top: 5px solid #f59e0b !important; font-weight: bold !important;
        display: block !important; width: 100% !important; white-space: pre-line !important;
    }}
    div.stButton > button:hover {{ transform: translateY(-5px) !important; border-color: #f59e0b !important; }}

    .smart-box {{ background: #111; padding: 25px; border-radius: 20px; border-right: 6px solid #f59e0b; color: white; margin-bottom: 15px; }}
    .label {{ color: #f59e0b; font-weight: bold; font-size: 14px; margin-bottom: 2px; }}
    .value {{ color: #fff; font-size: 18px; margin-bottom: 15px; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. شاشة الدخول ---
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:60px;'><h1 style='color:#f59e0b; font-size:55px;'>MA3LOMATI</h1><p style='color:#777;'>PRO 2026</p></div>", unsafe_allow_html=True)
    _, col_mid, _ = st.columns([1, 1.4, 1])
    with col_mid:
        u_input = st.text_input("اسم المستخدم أو الإيميل")
        p_input = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للمنصة 🚀", use_container_width=True):
            if p_input == "2026": 
                st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
            else:
                user_name = login_user_from_sheet(u_input, p_input)
                if user_name:
                    st.session_state.auth = True; st.session_state.current_user = user_name; st.rerun()
                else: st.error("بيانات الدخول غير صحيحة")
    st.stop()

# --- 7. التحميل والعرض ---
df_p, df_d, df_l = load_all_data()

st.markdown(f'<div class="main-header"><h1>MA3LOMATI PRO</h1><p>مرحباً بك يا {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

c_logout, _ = st.columns([0.15, 0.85])
with c_logout:
    if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], 
    icons=["briefcase", "building", "search", "robot", "rocket"], 
    default_index=4, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- 8. منطق عرض التفاصيل ---
if st.session_state.selected_item is not None:
    it = st.session_state.selected_item
    if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
    
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    # التحقق من نوع البيانات المعروضة (مشروع، مطور، أو لونش)
    title = it.get('ProjectName', it.get('Project', it.get('Developer', 'التفاصيل')))
    st.markdown(f"<h1 style='color:#f59e0b;'>{title}</h1>", unsafe_allow_html=True)
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        if 'Developer' in it: st.markdown(f"<p class='label'>🏢 المطور</p><p class='value'>{it['Developer']}</p>", unsafe_allow_html=True)
        if 'Location' in it: st.markdown(f"<p class='label'>📍 الموقع</p><p class='value'>{it['Location']}</p>", unsafe_allow_html=True)
    with col_d2:
        if 'Price & Payment' in it: st.markdown(f"<p class='label'>💰 السعر والسداد</p><p class='value'>{it['Price & Payment']}</p>", unsafe_allow_html=True)
        if 'Developer Category' in it: st.markdown(f"<p class='label'>⭐ الفئة</p><p class='value'>{it['Developer Category']}</p>", unsafe_allow_html=True)
    
    # عرض الـ USP أو الملاحظات إن وجدت
    usp = it.get('Unique Selling Points (USP)', it.get('Notes', '---'))
    if usp != '---':
        st.markdown(f"<hr style='border-color:#333;'><p class='label'>🌟 تفاصيل إضافية</p><p style='font-size:17px; line-height:1.7;'>{usp}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 9. منطق القوائم ---
else:
    if menu == "اللونشات":
        st.markdown("<h2 style='text-align:center;'>🚀 أحدث لونشات 2026</h2>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, r in df_l.iterrows():
            with cols[i % 3]:
                if st.button(f"🏢 {r['Developer']}\n{r['Project']}\n📍 {r['Location']}", key=f"card_l_{i}"):
                    st.session_state.selected_item = r; st.rerun()

    elif menu == "المشاريع":
        m_col, s_col = st.columns([0.7, 0.3])
        with s_col: st.markdown("<div class='smart-box'><h4>📌 مناطق ساخنة</h4><p>التجمع<br>العاصمة<br>أكتوبر</p></div>", unsafe_allow_html=True)
        with m_col:
            search = st.text_input("🔍 ابحث عن مشروع")
            dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
            start = st.session_state.p_idx * 6
            grid = st.columns(2)
            for i, r in dff.iloc[start:start+6].reset_index().iterrows():
                with grid[i % 2]:
                    if st.button(f"🏗️ {r['ProjectName']}\n📍 {r['Location']}\n🏢 {r['Developer']}", key=f"card_p_{i}"):
                        st.session_state.selected_item = r; st.rerun()
            if len(dff) > 6:
                c1, c2 = st.columns(2)
                if start > 0 and c1.button("السابق"): st.session_state.p_idx -= 1; st.rerun()
                if start+6 < len(dff) and c2.button("التالي"): st.session_state.p_idx += 1; st.rerun()

    elif menu == "المطورين":
        m_col_d, s_col_d = st.columns([0.7, 0.3])
        with s_col_d: st.markdown("<div class='smart-box'><h4>🏆 الأفضل</h4><p>مطورين الفئة A</p></div>", unsafe_allow_html=True)
        with m_col_d:
            search_d = st.text_input("🔍 ابحث عن مطور")
            dfd = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
            start_d = st.session_state.d_idx * 6
            grid_d = st.columns(2)
            for i, r in dfd.iloc[start_d:start_d+6].reset_index().iterrows():
                with grid_d[i % 2]:
                    if st.button(f"🏗️ {r['Developer']}\n⭐ الفئة: {r.get('Developer Category','A')}", key=f"card_d_{i}"):
                        st.session_state.selected_item = r; st.rerun()
            if len(dfd) > 6:
                c1, c2 = st.columns(2)
                if start_d > 0 and c1.button("السابق "): st.session_state.d_idx -= 1; st.rerun()
                if start_d+6 < len(dfd) and c2.button("التالي "): st.session_state.d_idx += 1; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
