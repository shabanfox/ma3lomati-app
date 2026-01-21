import streamlit as st
import pandas as pd
import requests
import feedparser
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الروابط الأساسية ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"

# --- 3. إدارة حالة الجلسة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# --- 4. وظائف جلب البيانات المسرعة (Cache) ---
@st.cache_data(ttl=1800) # تحديث كل 30 دقيقة لتسريع الدخول
def get_users_list():
    try:
        res = requests.get(SCRIPT_URL, timeout=5)
        return res.json() if res.status_code == 200 else []
    except: return []

@st.cache_data(ttl=600) # تحديث كل 10 دقائق
def load_main_data():
    try:
        p = pd.read_csv(URL_P).fillna("---")
        d = pd.read_csv(URL_D).fillna("---")
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True, errors='ignore')
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

def login_logic(u, p):
    if p == "2026": return "مدير النظام" # الدخول السريع جداً
    users = get_users_list()
    for user in users:
        if (u.lower() == str(user.get('Name','')).lower() or u.lower() == str(user.get('Email','')).lower()) and p == str(user.get('Password','')):
            return user.get('Name', 'User')
    return None

# --- 5. التصميم الجمالي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    
    .ticker-wrap { background: #111; padding: 10px 0; border-bottom: 1px solid #f59e0b; direction: ltr !important; }
    .ticker { display: inline-block; animation: ticker 100s linear infinite; color: white; white-space: nowrap; font-size: 15px; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    div.stButton > button[key*="card_"] {
        background: white !important; color: black !important; height: 110px !important; border-radius: 15px !important;
        font-weight: bold !important; font-size: 17px !important; width: 100% !important; border: none !important;
        box-shadow: 0 4px 15px rgba(255,255,255,0.1);
    }
    .smart-box { background: #161616; border: 1px solid #333; padding: 20px; border-radius: 15px; border-right: 5px solid #f59e0b; margin-bottom: 15px; }
    .tool-card { background: #1a1a1a; padding: 20px; border-radius: 15px; border-top: 4px solid #f59e0b; text-align: center; }
    input { text-align: right !important; direction: rtl !important; }
    .stTabs [data-baseweb="tab-list"] { justify-content: center; direction: ltr !important; }
    </style>
""", unsafe_allow_html=True)

# --- 6. شاشة الدخول (Centered & Fast) ---
if not st.session_state.auth:
    _, col_mid, _ = st.columns([1, 1.2, 1])
    with col_mid:
        st.markdown("<br><br><br><div style='text-align:center;'><h1 style='color:#f59e0b; font-size:55px; margin-bottom:0;'>MA3LOMATI</h1><p style='color:#777; letter-spacing:3px;'>PRO VERSION 2026</p></div>", unsafe_allow_html=True)
        u_in = st.text_input("اسم المستخدم", key="u_fast")
        p_in = st.text_input("كلمة المرور", type="password", key="p_fast")
        if st.button("دخول آمن 🚀", use_container_width=True):
            with st.spinner('جاري التحقق...'):
                user_name = login_logic(u_in, p_in)
                if user_name:
                    st.session_state.auth = True
                    st.session_state.current_user = user_name
                    st.rerun()
                else: st.error("عذراً، البيانات غير صحيحة")
    st.stop()

# --- 7. واجهة المستخدم بعد الدخول ---
df_p, df_d = load_main_data()

# الهيدر مع زر الخروج يساراً
c_out, c_empty = st.columns([0.15, 0.85])
with c_out:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 خروج", key="exit_btn"):
        st.session_state.auth = False; st.rerun()

st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab'); 
                height: 150px; background-size: cover; background-position: center; border-radius: 20px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b;">
        <h1 style="color: white; margin: 0; font-family: 'Cairo';">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold;">مرحباً بك: {st.session_state.current_user}</p>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 أهم الأخبار العقارية: طرح وحدات جديدة في الشيخ زايد • العاصمة الإدارية تسجل أعلى نسبة مبيعات لعام 2025 • بدء تسليم مشاريع التجمع الخامس • انخفاض أسعار مواد البناء • </div></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["briefcase", "building", "search", "robot"], default_index=3, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- 8. منطق الصفحات ---
if st.session_state.selected_item is not None:
    if st.button("➡️ عودة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"<div class='smart-box'><h2>{item.get('ProjectName', item.get('Developer'))}</h2><hr><p>📍 الموقع: {item.get('Location', '---')}</p></div>", unsafe_allow_html=True)

elif menu == "أدوات البروكر":
    st.markdown("<h2 style='text-align: center; color: #f59e0b; margin-bottom: 30px;'>🛠️ أدوات البروكر العقاري</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3); c4, c5, c6 = st.columns(3)
    tools = [(c1,"💳 القسط"), (c2,"💰 العمولة"), (c3,"📈 ROI"), (c4,"📐 المساحة"), (c5,"📝 الضريبة"), (c6,"🏦 التمويل")]
    for col, label in tools:
        with col:
            st.markdown(f"<div class='tool-card'><h4>{label}</h4></div>", unsafe_allow_html=True)
            st.number_input("أدخل الرقم", key=f"t_{label}")

elif menu == "المشاريع":
    m_col, s_col = st.columns([0.75, 0.25]) # المشاريع يمين، القائمة يسار
    with s_col:
        st.markdown("<h4 style='color:#f59e0b; text-align:center;'>🚀 استلام فوري</h4>", unsafe_allow_html=True)
        for i, r in df_p.head(6).iterrows():
            st.markdown(f"<div class='smart-box' style='padding:10px; font-size:14px;'>🏠 {r['ProjectName']}</div>", unsafe_allow_html=True)
    with m_col:
        search = st.text_input("🔍 ابحث في المشاريع...")
        dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
        page = dff.iloc[st.session_state.p_idx*6 : st.session_state.p_idx*6+6]
        for i in range(0, len(page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page):
                    row = page.iloc[i+j]
                    if cols[j].button(f"{row['ProjectName']}\n📍 {row['Location']}", key=f"card_p_{i+j}"):
                        st.session_state.selected_item = row; st.rerun()

elif menu == "المطورين":
    m_col, s_col = st.columns([0.75, 0.25]) # المطورين يمين، القائمة يسار
    with s_col:
        st.markdown("<h4 style='color:#f59e0b; text-align:center;'>🏆 كبار المطورين</h4>", unsafe_allow_html=True)
        for i, r in df_d.head(6).iterrows():
            st.markdown(f"<div class='smart-box' style='padding:10px; font-size:14px;'>🏢 {r['Developer']}</div>", unsafe_allow_html=True)
    with m_col:
        search_d = st.text_input("🔍 ابحث في المطورين...")
        dfd_f = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
        page_d = dfd_f.iloc[st.session_state.d_idx*6 : st.session_state.d_idx*6+6]
        for i in range(0, len(page_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page_d):
                    row = page_d.iloc[i+j]
                    if cols[j].button(f"{row['Developer']}\n⭐ مطور فئة A", key=f"card_d_{i+j}"):
                        st.session_state.selected_item = row; st.rerun()

elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'><h3>🤖 المساعد العقاري الذكي</h3><p>أدخل بيانات العميل ليقوم الذكاء الاصطناعي بترشيح أنسب المشاريع.</p></div>", unsafe_allow_html=True)
    st.text_area("أوصف طلب العميل هنا...")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
