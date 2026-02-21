import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. التحسين البصري (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0rem !important; }
    [data-testid="stStatusWidget"] {display: none !important;}
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }

    /* هيدر ملكي */
    .royal-header { 
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80'); 
        border-bottom: 3px solid #f59e0b; padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 0px;
    }
    .royal-header h1 { color: #f59e0b; font-size: 3rem; font-weight: 900; margin: 0; }

    /* شريط الأخبار تحت الهيدر */
    .ticker-wrap {
        width: 100%; background: rgba(245, 158, 11, 0.1); border-bottom: 1px solid #f59e0b;
        overflow: hidden; white-space: nowrap; padding: 12px 0; margin-bottom: 20px;
    }
    .ticker {
        display: inline-block; animation: ticker 50s linear infinite;
        color: #f59e0b; font-weight: bold; font-size: 1.15rem;
    }
    .ticker:hover { animation-play-state: paused; }
    .news-msg { margin: 0 60px; }

    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-150%); }
    }

    div.stButton > button[key*="card_"] { background: white !important; color: black !important; border-right: 12px solid #f59e0b !important; border-radius: 15px !important; text-align: right !important; min-height: 150px !important; font-weight: 900 !important; font-size: 1.1rem !important; }
    .detail-card { background: rgba(30, 30, 30, 0.95); padding: 20px; border-radius: 15px; border: 1px solid #444; border-top: 6px solid #f59e0b; margin-bottom: 15px; }
    .label-gold { color: #f59e0b; font-weight: 900; font-size: 1rem; }
    .val-white { color: white; font-size: 1.25rem; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# --- 3. الوظائف التقنية وتسجيل الدخول ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

def login_user(u, p):
    try:
        res = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=5)
        if res.status_code == 200:
            for user in res.json():
                if str(u).strip().lower() == str(user.get('Name','')).strip().lower() and str(p) == str(user.get('Password','')):
                    return user.get('Name')
    except: pass
    return None

def format_price(val):
    try:
        v = float(val)
        if v >= 1_000_000:
            return f"{v/1_000_000:,.2f} مليون ج.م"
        return f"{v:,.0f} ج.م"
    except: return "اتصل للسعر"

# --- 4. تحميل البيانات ---
@st.cache_data(ttl=300, show_spinner=False)
def load_data():
    try:
        urls = [
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv",
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv",
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
        ]
        dfs = [pd.read_csv(u) for u in urls]
        for df in dfs:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price'}, inplace=True, errors="ignore")
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        return [d.fillna("---") for d in dfs]
    except: return [pd.DataFrame()]*3

df_p, df_d, df_l = load_data()

# --- 5. بوابة الدخول ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.current_user = "Guest"

if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("SIGN IN 🚀", use_container_width=True):
        user = "Admin" if p == "2026" else login_user(u, p)
        if user:
            st.session_state.auth, st.session_state.current_user = True, user
            st.rerun()
        else: st.error("بيانات الدخول غير صحيحة")
    st.stop()

# --- 6. العرض الرئيسي ---
# الهيدر أولاً
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b; font-weight:bold;">مرحباً {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

# شريط الأخبار ثانياً (تحت الهيدر)
st.markdown("""
    <div class="ticker-wrap">
        <div class="ticker">
            <span class="news-msg">🔥 عاجل: ارتفاع الطلب على الشقق السكنية في التجمع الخامس بنسبة 15%</span>
            <span class="news-msg">🟡 الذهب: سعر عيار 21 يسجل اليوم 3,650 ج.م للجرام</span>
            <span class="news-msg">🏗️ تطوير: إطلاق مشروع "تاج سيتي" المرحلة الجديدة بأسعار تبدأ من 4 مليون ج.م</span>
            <span class="news-msg">💵 العملات: استقرار سعر صرف الدولار مقابل الجنيه في كافة البنوك المصرية</span>
            <span class="news-msg">🏙️ العاصمة الإدارية: بدء تسليم وحدات الحي السكني الثالث R3 قريباً</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# القائمة
menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

# دالة العرض المحدثة بالأسعار (بالملايين)
def render_grid(dataframe, prefix):
    if st.session_state.get('view') == f"details_{prefix}":
        if st.button("⬅ عودة", key=f"b_{prefix}"): st.session_state.view = "grid"; st.rerun()
        item = dataframe.iloc[st.session_state.current_index]
        st.markdown(f"<h2 style='color:#f59e0b;'>💎 {item.iloc[0]}</h2>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, col in enumerate(dataframe.columns):
            with cols[i%3]:
                val = format_price(item[col]) if col == 'Price' else item[col]
                st.markdown(f'<div class="detail-card"><p class="label-gold">{col}</p><p class="val-white">{val}</p></div>', unsafe_allow_html=True)
    else:
        grid = st.columns(2)
        for i, (idx, r) in enumerate(dataframe.head(6).iterrows()):
            with grid[i%2]:
                price_txt = format_price(r['Price']) if 'Price' in r else ""
                if st.button(f"🏢 {r[0]}\n📍 {r.get('Location','---')}\n💰 {price_txt}", key=f"card_{prefix}_{idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()

if menu == "المشاريع":
    render_grid(df_p, "p")
elif menu == "المطورين":
    render_grid(df_d, "d")
elif menu == "أدوات الحساب":
    st.info("أدوات الحساب العقاري")

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
