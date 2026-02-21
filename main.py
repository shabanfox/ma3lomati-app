import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. التحسين البصري وشريط الأخبار المتحرك (CSS) ---
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

    /* --- شريط الأخبار المتحرك (News Ticker) --- */
    .ticker-wrap {
        width: 100%; background: rgba(245, 158, 11, 0.1); border-bottom: 1px solid #f59e0b;
        overflow: hidden; white-space: nowrap; padding: 10px 0;
    }
    .ticker {
        display: inline-block; animation: ticker 45s linear infinite;
        color: #f59e0b; font-weight: bold; font-size: 1.1rem;
    }
    .ticker:hover { animation-play-state: paused; cursor: pointer; }
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    .news-item { margin: 0 40px; }

    .royal-header { 
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80'); 
        border-bottom: 3px solid #f59e0b; padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 15px;
    }
    .royal-header h1 { color: #f59e0b; font-size: 3rem; font-weight: 900; margin: 0; }

    div.stButton > button[key*="card_"] { background: white !important; color: black !important; border-right: 12px solid #f59e0b !important; border-radius: 15px !important; text-align: right !important; min-height: 150px !important; font-weight: 900 !important; font-size: 1.1rem !important; }
    div.stButton > button[key*="linked_"] { background: rgba(245, 158, 11, 0.2) !important; color: #f59e0b !important; border: 1px solid #f59e0b !important; font-weight: bold !important; border-radius: 10px !important; }
    
    .detail-card { background: rgba(30, 30, 30, 0.95); padding: 20px; border-radius: 15px; border: 1px solid #444; border-top: 6px solid #f59e0b; margin-bottom: 15px; }
    .label-gold { color: #f59e0b; font-weight: 900; font-size: 1rem; }
    .val-white { color: white; font-size: 1.25rem; font-weight: 700; }
    .filter-box { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 20px; border: 1px solid #333; margin-bottom: 20px; }
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

# --- 5. تحميل البيانات ---
@st.cache_data(ttl=300, show_spinner=False)
def load_data():
    try:
        p = pd.read_csv(URL_PROJECTS)
        d = pd.read_csv(URL_DEVELOPERS)
        l = pd.read_csv(URL_LAUNCHES)
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price', 'المطور': 'Developer'}, inplace=True, errors="ignore")
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 6. دالة العرض الرئيسية مع (الفلاتر + الربط الذكي) ---
def render_grid(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0

    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}", use_container_width=True): 
            st.session_state.view = "grid"; st.rerun()
        
        item = dataframe.iloc[st.session_state.current_index]
        main_name = str(item.iloc[0])
        st.markdown(f"<h2 style='color:#f59e0b; text-align:right;'>🏠 {main_name}</h2>", unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, col_name in enumerate(dataframe.columns):
            with cols[i % 3]:
                val = item[col_name]
                if col_name == 'Price': val = f"{int(val):,}" if float(val) > 0 else "اتصل للسعر"
                st.markdown(f'<div class="detail-card"><p class="label-gold">{col_name}</p><p class="val-white">{val}</p></div>', unsafe_allow_html=True)
        
        # --- إضافة ميزة الربط داخل صفحة المطور ---
        if prefix == "d":
            st.markdown("<h3 style='color:#f59e0b; border-right:5px solid #f59e0b; padding-right:10px; margin-top:30px;'>🏗️ مشاريع المطور</h3>", unsafe_allow_html=True)
            all_projs = pd.concat([df_p, df_l]).drop_duplicates().reset_index(drop=True)
            related = all_projs[all_projs.apply(lambda row: row.astype(str).str.contains(main_name, case=False).any(), axis=1)]
            if not related.empty:
                r_cols = st.columns(2)
                for r_idx, (idx, r_row) in enumerate(related.iterrows()):
                    with r_cols[r_idx % 2]:
                        st.button(f"🏢 {r_row.iloc[0]} | 📍 {r_row.get('Location','---')}", key=f"linked_{idx}", use_container_width=True)
            else: st.info("لا توجد مشاريع مسجلة حالياً.")

    else:
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
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    p_v = f"{int(r['Price']):,}" if ('Price' in r and r['Price'] > 0) else "اتصل للسعر"
                    if st.button(f"🏢 {r[0]}\n📍 {r.get('Location','---')}\n💰 {p_v}", key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
            
            # التنقل
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

# --- 7. بوابة الدخول (بنفس منطق كودك) ---
if not st.session_state.get('auth', False):
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    u = st.text_input("Username", key="log_u")
    p = st.text_input("Password", type="password", key="log_p")
    if st.button("SIGN IN 🚀", use_container_width=True):
        if p == "2026": st.session_state.auth = True; st.rerun()
        else: st.error("خطأ في كلمة السر")
    st.stop()

# --- 8. التطبيق الرئيسي ---
# شريط الأخبار المتحرك
st.markdown("""
    <div class="ticker-wrap">
        <div class="ticker">
            <span class="news-item">🟡 الذهب: عيار 21 يسجل استقراراً في الأسواق اليوم</span>
            <span class="news-item">💵 الدولار: تحديثات أسعار الصرف متوفرة الآن بالبنوك</span>
            <span class="news-item">🏗️ عقارات: طروحات جديدة في الساحل الشمالي صيف 2026</span>
            <span class="news-item">🚀 اقتصاد: ارتفاع مؤشرات الاستثمار العقاري بنسبة 12%</span>
            <span class="news-item">🏙️ مدينة المستقبل: تسليم المرحلة الأولى لعدد من المشاريع الكبرى</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# الهيدر وزر الخروج
c_out1, c_out2 = st.columns([0.1, 0.9])
with c_out1: 
    if st.button("🚪 خروج"): logout()

st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b; font-weight:bold;">مرحباً {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000", "font-weight": "900"}})

if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.last_m = "grid", menu

if menu == "أدوات الحساب":
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
