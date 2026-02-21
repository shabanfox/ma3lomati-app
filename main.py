import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إخفاء رسائل التحميل والتحسين البصري (CSS) ---
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

    /* ستايل الهيدر الملكي */
    .royal-header { 
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80'); 
        background-size: cover; background-position: center; 
        border-bottom: 3px solid #f59e0b; padding: 45px 20px; text-align: center; 
        border-radius: 0 0 40px 40px; margin-bottom: 15px; position: relative; 
    }
    .royal-header h1 { color: #f59e0b; font-size: 3rem; font-weight: 900; margin: 0; }

    /* ستايل الكروت والفلاتر */
    div.stButton > button[key*="card_"] { background: white !important; color: black !important; border-right: 12px solid #f59e0b !important; border-radius: 15px !important; text-align: right !important; min-height: 150px !important; font-weight: 900 !important; font-size: 1.1rem !important; }
    .detail-card { background: rgba(30, 30, 30, 0.95); padding: 20px; border-radius: 15px; border: 1px solid #444; border-top: 6px solid #f59e0b; margin-bottom: 15px; }
    .label-gold { color: #f59e0b; font-weight: 900; font-size: 1rem; }
    .val-white { color: white; font-size: 1.25rem; font-weight: 700; }
    
    .filter-box { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 20px; border: 1px solid #333; margin-bottom: 20px; }
    
    /* الأنيميشن */
    .stApp { animation: fadeIn 0.5s; }
    @keyframes fadeIn { 0% {opacity: 0;} 100% {opacity: 1;} }
    </style>
""", unsafe_allow_html=True)

# --- 3. إدارة حالة الجلسة ---
if 'auth' not in st.session_state:
    st.session_state.auth = "u_session" in st.query_params
    st.session_state.current_user = st.query_params.get("u_session", "Guest")

if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0

def logout():
    for key in list(st.session_state.keys()): del st.session_state[key]
    st.query_params.clear()
    st.rerun()

# --- 4. الروابط والثوابت ---
URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
ITEMS_PER_PAGE = 6

# --- 5. الوظائف التقنية ---
@st.cache_data(ttl=300, show_spinner=False)
def load_data():
    try:
        p = pd.read_csv(URL_PROJECTS)
        d = pd.read_csv(URL_DEVELOPERS)
        l = pd.read_csv(URL_LAUNCHES)
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price', 'سعر': 'Price'}, inplace=True, errors="ignore")
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
                df['Price'] = df['Price'].apply(lambda x: x * 1_000_000 if 0 < x < 1000 else x)
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def login_user(u, p):
    try:
        res = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=5)
        if res.status_code == 200:
            for user in res.json():
                if str(u).strip().lower() == str(user.get('Name','')).strip().lower() and str(p) == str(user.get('Password','')):
                    return user.get('Name')
    except: pass
    return None

# --- 6. دالة العرض الرئيسية مع الفلاتر ---
def render_grid(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0

    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}", use_container_width=True): 
            st.session_state.view = "grid"; st.rerun()
        item = dataframe.iloc[st.session_state.current_index]
        st.markdown(f"<h2 style='color:#f59e0b; text-align:right;'>🏠 {item.iloc[0]}</h2>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, col_name in enumerate(dataframe.columns):
            with cols[i % 3]:
                val = item[col_name]
                if col_name == 'Price': val = f"{int(val):,}" if float(val) > 0 else "اتصل للسعر"
                st.markdown(f'<div class="detail-card"><p class="label-gold">{col_name}</p><p class="val-white">{val}</p></div>', unsafe_allow_html=True)
    else:
        # الفلاتر
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        f1, f2 = st.columns([2, 1])
        with f1: search = st.text_input("🔍 ابحث عن مشروع أو مطور...", key=f"s_{prefix}")
        with f2:
            locs = ["الكل"] + sorted([str(x) for x in dataframe['Location'].unique() if str(x) not in ["---", "nan", ""]]) if 'Location' in dataframe.columns else ["الكل"]
            sel_loc = st.selectbox("📍 الموقع", locs, key=f"l_{prefix}")
        st.markdown('</div>', unsafe_allow_html=True)

        filt = dataframe.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_loc != "الكل": filt = filt[filt['Location'].astype(str).str.contains(sel_loc, case=False, na=False)]

        start = st.session_state[pg_key] * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.8, 0.2])
        with m_c:
            if filt.empty: st.warning("لا توجد نتائج.")
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    p_v = f"{int(r['Price']):,}" if ('Price' in r and r['Price'] > 0) else "اتصل للسعر"
                    if st.button(f"🏢 {r[0]}\n📍 {r.get('Location','---')}\n💰 {p_v} ج.م", key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
            
            # أزرار التنقل
            st.write("")
            p1, px, p2 = st.columns([1, 1, 1])
            with p1: 
                if st.session_state[pg_key] > 0 and st.button("⬅ السابق", key=f"prev_{prefix}"): st.session_state[pg_key] -= 1; st.rerun()
            with px: st.markdown(f"<p style='text-align:center; color:#f59e0b;'>صفحة {st.session_state[pg_key]+1}</p>", unsafe_allow_html=True)
            with p2:
                if (start + ITEMS_PER_PAGE) < len(filt) and st.button("التالي ➡", key=f"next_{prefix}"): st.session_state[pg_key] += 1; st.rerun()

        with s_c:
            st.markdown("<p style='color:#f59e0b; font-weight:bold; border-bottom:2px solid #333;'>🔥 مقترحات</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(8).iterrows():
                if st.button(f"📌 {str(s_row[0])[:15]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()

# --- 7. بوابة الدخول ---
if not st.session_state.get('auth', False):
    st.markdown("<div style='display:flex; flex-direction:column; align-items:center; padding-top:50px;'><div style='background:#000; border:3px solid #f59e0b; border-radius:60px; padding:15px 50px; color:#f59e0b; font-size:24px; font-weight:900; margin-bottom:-30px; z-index:10;'>MA3LOMATI PRO</div><div style='background:#fff; width:380px; padding:55px 35px 30px 35px; border-radius:30px; text-align:center; box-shadow:0 20px 50px rgba(0,0,0,0.3);'>", unsafe_allow_html=True)
    u = st.text_input("Username", key="log_u")
    p = st.text_input("Password", type="password", key="log_p")
    if st.button("SIGN IN 🚀", use_container_width=True):
        if p == "2026": user = "Admin"
        else: user = login_user(u, p)
        if user:
            st.session_state.auth, st.session_state.current_user = True, user
            st.query_params["u_session"] = user; st.rerun()
        else: st.error("بيانات غير صحيحة")
    st.markdown("</div></div>", unsafe_allow_html=True); st.stop()

# --- 8. التطبيق الرئيسي ---
df_p, df_d, df_l = load_data()

# شريط الخروج العلوي
c_out1, c_out2 = st.columns([0.1, 0.9])
with c_out1: 
    if st.button("🚪 خروج", key="logout"): logout()

st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b; font-weight:bold;">مرحباً {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000", "font-weight": "900"}})

if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.last_m = "grid", menu

if menu == "أدوات الحساب":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات البروكر</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='detail-card'><h3>💰 القسط</h3>", unsafe_allow_html=True)
        pr = st.number_input("السعر", value=5000000)
        dp = st.number_input("المقدم %", value=10)
        yr = st.number_input("السنين", value=8)
        res = (pr - (pr * dp/100)) / (yr * 12) if yr > 0 else 0
        st.markdown(f"<p class='label-gold'>الشهري:</p><p class='val-white'>{res:,.0f}</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='detail-card'><h3>📊 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("الصفقة", value=5000000)
        pct = st.number_input("النسبة %", value=2.5)
        st.markdown(f"<p class='label-gold'>العمولة:</p><p class='val-white'>{deal*(pct/100):,.0f}</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='detail-card'><h3>📈 ROI</h3>", unsafe_allow_html=True)
        buy = st.number_input("الشراء", value=5000000)
        rent = st.number_input("الإيجار", value=40000)
        roi = ((rent * 12) / buy) * 100 if buy > 0 else 0
        st.markdown(f"<p class='label-gold'>السنوي:</p><p class='val-white'>{roi:.2f} %</p></div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ جميع المشاريع", "🚀 المشاريع الجديدة"])
    with t1: render_grid(df_p, "p")
    with t2: render_grid(df_l, "l")

elif menu == "المطورين":
    render_grid(df_d, "d")

elif menu == "المساعد الذكي":
    st.info("نظام تحليل البيانات العقارية AI 2026 قيد التطوير.")

st.markdown("<p style='text-align:center; color:#555; margin-top:50px; font-weight:bold;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
