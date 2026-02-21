import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. ستايلات CSS المحسنة ---
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
    .royal-header { 
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80'); 
        border-bottom: 3px solid #f59e0b; padding: 40px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 10px;
    }
    .royal-header h1 { color: #f59e0b; font-size: 2.5rem; font-weight: 900; margin: 0; }
    
    /* ستايل الأخبار */
    .news-bar { background: rgba(245, 158, 11, 0.1); border: 1px dashed #f59e0b; border-radius: 10px; padding: 10px; margin: 10px 0; display: flex; justify-content: space-around; flex-wrap: wrap; }
    .news-item { color: #fff; text-decoration: none; font-size: 0.85rem; font-weight: bold; padding: 5px 10px; }
    .news-item:hover { color: #f59e0b; }

    /* الكروت والتفاصيل */
    div.stButton > button[key*="card_"] { background: white !important; color: black !important; border-right: 12px solid #f59e0b !important; border-radius: 12px !important; text-align: right !important; min-height: 140px !important; font-weight: 900 !important; }
    div.stButton > button[key*="linkproj_"] { background: #f59e0b !important; color: #000 !important; font-weight: 900 !important; border-radius: 8px !important; }
    .detail-card { background: rgba(30, 30, 30, 0.95); padding: 15px; border-radius: 12px; border-top: 4px solid #f59e0b; margin-bottom: 10px; }
    .label-gold { color: #f59e0b; font-weight: 900; font-size: 0.9rem; margin-bottom: 5px; }
    .val-white { color: white; font-size: 1.1rem; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# --- 3. الوظائف التقنية ---
@st.cache_data(ttl=300, show_spinner=False)
def load_data():
    try:
        p = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv")
        d = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv")
        l = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv")
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price', 'المطور': 'Developer'}, inplace=True, errors="ignore")
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
                df['Price'] = df['Price'].apply(lambda x: x * 1_000_000 if 0 < x < 1000 else x)
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 4. إدارة الجلسة ---
if 'auth' not in st.session_state: st.session_state.auth = "u_session" in st.query_params
if 'view' not in st.session_state: st.session_state.view = "grid"

def logout():
    for key in list(st.session_state.keys()): del st.session_state[key]
    st.query_params.clear(); st.rerun()

# --- 5. دالة العرض الرئيسية مع ميزة الربط الذكي ---
def render_grid(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0

    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}", use_container_width=True): 
            st.session_state.view = "grid"; st.rerun()
        
        item = dataframe.iloc[st.session_state.current_index]
        main_name = str(item.iloc[0])
        st.markdown(f"<h2 style='color:#f59e0b;'>🏠 {main_name}</h2>", unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, col in enumerate(dataframe.columns):
            with cols[i % 3]:
                val = item[col]
                if col == 'Price': val = f"{int(val):,}" if float(val) > 0 else "اتصل"
                st.markdown(f'<div class="detail-card"><p class="label-gold">{col}</p><p class="val-white">{val}</p></div>', unsafe_allow_html=True)

        # --- ميزة الربط: عرض مشاريع المطور داخل صفحته ---
        if prefix == "d":
            st.markdown("<hr style='border:1px solid #333;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color:#f59e0b;'>🏗️ مشاريع المطور</h3>", unsafe_allow_html=True)
            all_projs = pd.concat([df_p, df_l]).drop_duplicates().reset_index(drop=True)
            related = all_projs[all_projs.apply(lambda row: row.astype(str).str.contains(main_name, case=False).any(), axis=1)]
            
            if not related.empty:
                r_grid = st.columns(2)
                for r_idx, (idx, r_row) in enumerate(related.iterrows()):
                    with r_grid[r_idx % 2]:
                        if st.button(f"🏢 {r_row.iloc[0]}\n📍 {r_row.get('Location','---')}", key=f"linkproj_{idx}", use_container_width=True):
                            # يمكن هنا إضافة توجيه لمشروع معين إذا لزم الأمر
                            pass
            else: st.info("لا توجد مشاريع مسجلة حالياً.")

    else:
        # الفلاتر
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        f1, f2 = st.columns([2, 1])
        with f1: search = st.text_input("🔍 بحث سريح...", key=f"s_{prefix}")
        with f2:
            locs = ["الكل"] + sorted([str(x) for x in dataframe['Location'].unique() if str(x) not in ["---", "nan", ""]]) if 'Location' in dataframe.columns else ["الكل"]
            sel_loc = st.selectbox("📍 الموقع", locs, key=f"l_{prefix}")
        st.markdown('</div>', unsafe_allow_html=True)

        filt = dataframe.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_loc != "الكل": filt = filt[filt['Location'].astype(str).str.contains(sel_loc, case=False, na=False)]

        start = st.session_state[pg_key] * 6
        disp = filt.iloc[start : start + 6]
        
        m_c, s_c = st.columns([0.8, 0.2])
        with m_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    p_v = f"{int(r['Price']):,}" if ('Price' in r and r['Price'] > 0) else "اتصل"
                    if st.button(f"🏢 {r[0]}\n📍 {r.get('Location','---')}\n💰 {p_v}", key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
            
            # التنقل
            st.write("")
            c_p, c_n = st.columns(2)
            with c_p: 
                if st.session_state[pg_key] > 0 and st.button("⬅ السابق", key=f"prev_{prefix}"): st.session_state[pg_key] -= 1; st.rerun()
            with c_n:
                if (start + 6) < len(filt) and st.button("التالي ➡", key=f"next_{prefix}"): st.session_state[pg_key] += 1; st.rerun()

# --- 6. بوابة الدخول ---
if not st.session_state.get('auth', False):
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    if st.text_input("Password", type="password") == "2026":
        st.session_state.auth = True; st.query_params["u_session"] = "Admin"; st.rerun()
    st.stop()

# --- 7. التطبيق الرئيسي ---
# شريط الأخبار الاقتصادي (بدلاً من الفواصل)
st.markdown("""
    <div class="news-bar">
        <a class="news-item" href="https://www.cnbcarabia.com/economy" target="_blank">📈 اقتصاد</a>
        <a class="news-item" href="https://www.gold-price-today.com/egypt/" target="_blank">🟡 الذهب الآن</a>
        <a class="news-item" href="https://www.sarrafah.com/" target="_blank">💵 الدولار</a>
        <a class="news-item" href="https://aqarmap.com.eg/ar/news/" target="_blank">🏠 أخبار العقارات</a>
    </div>
""", unsafe_allow_html=True)

# الهيدر وزر الخروج
c_h, c_l = st.columns([0.9, 0.1])
with c_h: st.markdown('<div class="royal-header"><h1>MA3LOMATI PRO</h1></div>', unsafe_allow_html=True)
with c_l: 
    if st.button("🚪"): logout()

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.last_m = "grid", menu

if menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ جميع المشاريع", "🚀 المشاريع الجديدة"])
    with t1: render_grid(df_p, "p")
    with t2: render_grid(df_l, "l")
elif menu == "المطورين":
    render_grid(df_d, "d")
elif menu == "أدوات الحساب":
    st.markdown("<div class='detail-card'><h3>🧮 حاسبة القسط السريع</h3>", unsafe_allow_html=True)
    price = st.number_input("السعر الإجمالي", value=1000000)
    down = st.number_input("المقدم (%)", value=10)
    years = st.slider("سنوات التقسيط", 1, 15, 8)
    monthly = (price * (1 - down/100)) / (years * 12)
    st.markdown(f"<p class='label-gold'>القسط الشهري التقريبي:</p><p class='val-white'>{monthly:,.0f} ج.م</p></div>", unsafe_allow_html=True)
elif menu == "المساعد الذكي":
    st.info("نظام تحليل السوق AI قيد التحديث لعام 2026.")

st.markdown("<p style='text-align:center; color:#555; font-weight:bold;'>MA3LOMATI PRO | 2026</p>", unsafe_allow_html=True)
