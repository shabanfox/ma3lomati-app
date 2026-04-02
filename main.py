
import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الثوابت التصميمية ---
GOLD_COLOR = "#D4AF37"
GOLD_GRADIENT = "linear-gradient(135deg, #D4AF37 0%, #F9E29C 50%, #B8860B 100%)"
DARK_BG = "#0a0a0a"

# --- 3. إدارة حالة الجلسة (Session State) ---
if 'auth' not in st.session_state:
    if "u_session" in st.query_params:
        st.session_state.auth = True
        st.session_state.current_user = st.query_params["u_session"]
    else:
        st.session_state.auth = False

if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0

# --- 4. الروابط والثوابت (جوجل شيت) ---
URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
ITEMS_PER_PAGE = 6

# --- 5. الوظائف التقنية ---
def login_user(user_input, pwd_input):
    try:
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=10)
        if response.status_code == 200:
            users_list = response.json()
            user_input = str(user_input).strip().lower()
            for user_data in users_list:
                name_s = str(user_data.get('Name', user_data.get('name', ''))).strip()
                pass_s = str(user_data.get('Password', user_data.get('password', ''))).strip()
                if user_input == name_s.lower() and str(pwd_input) == pass_s:
                    return name_s
        return None
    except: return None

@st.cache_data(ttl=60)
def load_data():
    try:
        p = pd.read_csv(URL_PROJECTS)
        d = pd.read_csv(URL_DEVELOPERS)
        l = pd.read_csv(URL_LAUNCHES)
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price', 'سعر': 'Price', 'المطور': 'Developer'}, inplace=True, errors="ignore")
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
                df['Price'] = df['Price'].apply(lambda x: x * 1_000_000 if 0 < x < 1000 else x)
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 6. محرك التصميم المتقدم (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{ background: {DARK_BG} !important; color: white !important; direction: rtl !important; font-family: 'Cairo', sans-serif; }}

    .royal-header {{
        background: linear-gradient(to bottom, rgba(0,0,0,0.8), rgba(0,0,0,0.9)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 1px solid rgba(212, 175, 55, 0.4);
        padding: 60px 20px; text-align: center; border-radius: 0 0 50px 50px; margin-bottom: 30px;
    }}
    .royal-header h1 {{ background: {GOLD_GRADIENT}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3.5rem; font-weight: 900; margin: 0; }}

    .modern-card {{
        background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(212, 175, 55, 0.15);
        border-radius: 24px; padding: 25px; margin-bottom: 15px; transition: all 0.3s;
    }}
    .modern-card:hover {{ border-color: {GOLD_COLOR}; background: rgba(212, 175, 55, 0.08); transform: translateY(-5px); }}

    div.stButton > button {{
        background: {GOLD_GRADIENT} !important; color: #000 !important; border: none !important;
        border-radius: 15px !important; font-weight: 800 !important; width: 100% !important;
    }}

    .detail-card {{ background: rgba(20, 20, 20, 0.8); border-radius: 20px; border: 1px solid #333; padding: 20px; margin-bottom: 15px; border-right: 5px solid {GOLD_COLOR}; }}
    .label-gold {{ color: {GOLD_COLOR}; font-weight: 900; font-size: 1rem; margin:0; }}
    .val-white {{ color: #fff; font-size: 1.2rem; font-weight: 700; margin:0; }}

    .stTabs [aria-selected="true"] {{ background: {GOLD_GRADIENT} !important; color: black !important; font-weight: 900 !important; border-radius: 12px !important; }}
    
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; padding-top: 80px; }}
    .auth-card {{ background: #fff; width: 400px; padding: 50px; border-radius: 35px; text-align: center; box-shadow: 0 25px 60px rgba(0,0,0,0.8); }}
    </style>
""", unsafe_allow_html=True)

# --- 7. دالة العرض الرئيسية (تم حل مشكلة الـ ID) ---
def render_grid(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0

    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ العودة للقائمة", key=f"back_btn_{prefix}"):
            st.session_state.view = "grid"; st.rerun()
        
        try:
            item = dataframe.iloc[st.session_state.current_index]
            st.markdown(f"<h1 style='color:{GOLD_COLOR}; text-align:right;'>🏠 {item.iloc[0]}</h1>", unsafe_allow_html=True)
            st.divider()
            cols = st.columns(3)
            for i, col_name in enumerate(dataframe.columns):
                with cols[i % 3]:
                    val = item[col_name]
                    if col_name == 'Price': val = f"{int(val):,}" if float(val) > 0 else "اتصل للسعر"
                    st.markdown(f'<div class="detail-card"><p class="label-gold">{col_name}</p><p class="val-white">{val}</p></div>', unsafe_allow_html=True)
        except: st.session_state.view = "grid"; st.rerun()
            
    else:
        # الفلاتر
        st.markdown('<div style="background:rgba(255,255,255,0.03); padding:20px; border-radius:20px; margin-bottom:20px;">', unsafe_allow_html=True)
        f1, f2 = st.columns([2, 1])
        with f1: search = st.text_input("🔍 ابحث هنا...", key=f"search_input_{prefix}")
        with f2:
            loc_list = ["الكل"] + sorted([str(x).strip() for x in dataframe['Location'].unique() if str(x).strip() not in ["---", "nan", ""]]) if 'Location' in dataframe.columns else ["الكل"]
            sel_area = st.selectbox("📍 الموقع", loc_list, key=f"loc_select_{prefix}")
        st.markdown("</div>", unsafe_allow_html=True)

        filt = dataframe.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_area != "الكل": filt = filt[filt['Location'].astype(str).str.contains(sel_area, case=False, na=False)]

        start = st.session_state[pg_key] * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.75, 0.25])
        with m_c:
            if filt.empty: st.warning("لا توجد نتائج.")
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    p_val = f"{int(r['Price']):,}" if ('Price' in r and r['Price'] > 0) else "اتصل للسعر"
                    st.markdown(f"""
                        <div class="modern-card">
                            <div style="font-size:1.4rem; font-weight:900; color:{GOLD_COLOR};">🏢 {str(r[0])}</div>
                            <p style="margin:10px 0; color:#ccc;">📍 {r.get('Location','---')}<br>💰 <span style="color:{GOLD_COLOR}">{p_val} ج.م</span></p>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"تفاصيل {str(r[0])[:12]}", key=f"grid_btn_{prefix}_{idx}"):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
            
            # أزرار التنقل (تم تصحيحها بـ keys فريدة)
            st.write("")
            p1, px, p2 = st.columns([1, 1, 1])
            with p1: 
                if st.session_state[pg_key] > 0:
                    if st.button("⬅ السابق", key=f"prev_pg_{prefix}"): st.session_state[pg_key] -= 1; st.rerun()
            with px: st.markdown(f"<p style='text-align:center; color:{GOLD_COLOR}; font-weight:bold;'>صفحة {st.session_state[pg_key]+1}</p>", unsafe_allow_html=True)
            with p2:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالي ➡", key=f"next_pg_{prefix}"): st.session_state[pg_key] += 1; st.rerun()

        with s_c:
            st.markdown(f"<div style='background:rgba(212,175,55,0.05); padding:15px; border-radius:20px; border:1px solid rgba(212,175,55,0.2);'>", unsafe_allow_html=True)
            st.markdown(f"<p style='color:{GOLD_COLOR}; font-weight:900; text-align:center;'>⭐ مقترحات</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(10).iterrows():
                if st.button(f"📌 {str(s_row[0])[:15]}", key=f"side_link_{prefix}_{s_idx}"):
                    st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

# --- 8. بوابة الدخول ---
if not st.session_state.get('auth', False):
    st.markdown("<div class='auth-wrapper'><div class='auth-card'>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='color:#000; font-weight:900;'>MA3LOMATI <span style='color:{GOLD_COLOR}'>PRO</span></h2>", unsafe_allow_html=True)
    u = st.text_input("", placeholder="User", key="user_in")
    p = st.text_input("", type="password", placeholder="Pass", key="pass_in")
    if st.button("LOGIN 🚀"):
        if p == "2026": 
            st.session_state.auth, st.session_state.current_user = True, "Admin"
            st.query_params["u_session"] = "Admin"; st.rerun()
        else:
            user = login_user(u, p)
            if user:
                st.session_state.auth, st.session_state.current_user = True, user
                st.query_params["u_session"] = user; st.rerun()
            else: st.error("خطأ!")
    st.markdown("</div></div>", unsafe_allow_html=True); st.stop()

# --- 9. تحميل البيانات والتشغيل ---
df_p, df_d, df_l = load_data()

st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:{GOLD_COLOR}; font-weight:bold;">نخبة المستشارين العقاريين | {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"container": {"background-color": "transparent"}, "nav-link-selected": {"background": GOLD_GRADIENT, "color": "black", "font-weight": "900"}})

if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.last_m = "grid", menu

if menu == "أدوات الحساب":
    st.markdown(f"<h2 style='color:{GOLD_COLOR}; text-align:center;'>🛠️ الحاسبة العقارية</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='detail-card'><h3>💰 القسط</h3>", unsafe_allow_html=True)
        pr = st.number_input("السعر", value=5000000, step=100000)
        dp = st.number_input("المقدم %", value=10)
        yr = st.number_input("السنين", value=8)
        res = (pr - (pr * dp/100)) / (yr * 12) if yr > 0 else 0
        st.markdown(f"<p class='label-gold'>الشهري:</p><p class='val-white'>{res:,.0f} ج.م</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='detail-card'><h3>📊 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("الصفقة", value=5000000)
        pct = st.number_input("النسبة %", value=2.5)
        st.markdown(f"<p class='label-gold'>الصافي:</p><p class='val-white'>{deal*(pct/100):,.0f} ج.م</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='detail-card'><h3>📈 ROI</h3>", unsafe_allow_html=True)
        buy = st.number_input("الشراء", value=5000000)
        rent = st.number_input("الإيجار", value=40000)
        roi = ((rent * 12) / buy) * 100 if buy > 0 else 0
        st.markdown(f"<p class='label-gold'>العائد:</p><p class='val-white'>{roi:.2f} %</p></div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ المشاريع", "🚀 اللونشات"])
    with t1: render_grid(df_p, "p")
    with t2: render_grid(df_l, "l")

elif menu == "المطورين":
    render_grid(df_d, "d")

elif menu == "المساعد الذكي":
    st.info("نظام AI 2026 قيد التطوير.")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
