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

    .royal-header { 
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80'); 
        border-bottom: 3px solid #f59e0b; padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 0px;
    }
    .royal-header h1 { color: #f59e0b; font-size: 3rem; font-weight: 900; margin: 0; }

    .ticker-wrap {
        width: 100%; background: rgba(245, 158, 11, 0.15); border-bottom: 1px solid #f59e0b;
        overflow: hidden; white-space: nowrap; padding: 12px 0; margin-bottom: 20px;
    }
    .ticker { display: inline-block; animation: ticker 50s linear infinite; color: #f59e0b; font-weight: bold; font-size: 1.1rem; }
    .news-msg { margin: 0 600px; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-150%); } }

    div.stButton > button[key*="card_"] { background: white !important; color: black !important; border-right: 12px solid #f59e0b !important; border-radius: 15px !important; text-align: right !important; min-height: 150px !important; font-weight: 900 !important; font-size: 1.1rem !important; white-space: pre-wrap !important; }
    div.stButton > button[key*="linked_"] { background: rgba(245, 158, 11, 0.2) !important; color: #f59e0b !important; border: 1px solid #f59e0b !important; font-weight: bold !important; border-radius: 10px !important; }
    .detail-card { background: rgba(30, 30, 30, 0.95); padding: 20px; border-radius: 15px; border: 1px solid #444; border-top: 6px solid #f59e0b; margin-bottom: 15px; }
    .label-gold { color: #f59e0b; font-weight: 900; font-size: 1rem; }
    .val-white { color: white; font-size: 1.25rem; font-weight: 700; }
    .filter-box { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 20px; border: 1px solid #333; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. إدارة الجلسة والبيانات ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

if 'auth' not in st.session_state:
    st.session_state.auth = "u_session" in st.query_params
    st.session_state.current_user = st.query_params.get("u_session", "Guest")
if 'view' not in st.session_state: st.session_state.view = "grid"

def format_price_millions(val):
    try:
        v = float(val)
        if v >= 1_000_000: return f"{v/1_000_000:,.2f} مليون ج.م"
        return f"{v:,.0f} ج.م"
    except: return "اتصل للسعر"

@st.cache_data(ttl=300, show_spinner=False)
def load_data():
    try:
        urls = [
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv",
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv",
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
        ]
        dfs = []
        for u in urls:
            df = pd.read_csv(u)
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price', 'سعر': 'Price', 'المالك': 'Owner', 'صاحب الشركة': 'Owner'}, inplace=True, errors="ignore")
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
                df['Price'] = df['Price'].apply(lambda x: x * 1_000_000 if 0 < x < 1000 else x)
            dfs.append(df.fillna("---"))
        return dfs
    except: return [pd.DataFrame()]*3

df_p, df_d, df_l = load_data()

# --- 4. دالة العرض الرئيسية (المعدلة للمطورين) ---
def render_grid(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0

    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}", use_container_width=True): 
            st.session_state.view = "grid"; st.rerun()
        
        item = dataframe.iloc[st.session_state.current_index]
        main_name = str(item.iloc[0])
        st.markdown(f"<h2 style='color:#f59e0b; text-align:right;'>💎 {main_name}</h2>", unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, col_name in enumerate(dataframe.columns):
            with cols[i % 3]:
                val = format_price_millions(item[col_name]) if col_name == 'Price' else item[col_name]
                st.markdown(f'<div class="detail-card"><p class="label-gold">{col_name}</p><p class="val-white">{val}</p></div>', unsafe_allow_html=True)
        
        if prefix == "d":
            st.markdown("<h3 style='color:#f59e0b; border-right:5px solid #f59e0b; padding-right:10px; margin-top:30px;'>🏗️ مشاريع المطور</h3>", unsafe_allow_html=True)
            all_p = pd.concat([df_p, df_l]).drop_duplicates().reset_index(drop=True)
            related = all_p[all_p.apply(lambda row: row.astype(str).str.contains(main_name, case=False).any(), axis=1)]
            if not related.empty:
                r_grid = st.columns(2)
                for r_idx, (idx, r_row) in enumerate(related.iterrows()):
                    with r_grid[r_idx % 2]:
                        st.button(f"🏢 {r_row.iloc[0]} | 📍 {r_row.get('Location','---')}", key=f"linked_{idx}", use_container_width=True)
    else:
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        f1, f2 = st.columns([2, 1])
        with f1: search = st.text_input("🔍 ابحث...", key=f"s_{prefix}")
        with f2:
            locs = ["الكل"] + sorted([str(x) for x in dataframe['Location'].unique() if str(x) not in ["---", "nan", ""]]) if 'Location' in dataframe.columns else ["الكل"]
            sel_loc = st.selectbox("📍 الموقع", locs, key=f"l_{prefix}")
        st.markdown('</div>', unsafe_allow_html=True)

        filt = dataframe.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_loc != "الكل" and 'Location' in filt.columns: filt = filt[filt['Location'].astype(str).str.contains(sel_loc, case=False, na=False)]

        start = st.session_state[pg_key] * 6
        disp = filt.iloc[start : start + 6]
        
        grid = st.columns(2)
        for i, (idx, r) in enumerate(disp.iterrows()):
            with grid[i%2]:
                # --- تعديل محتوى الكارت بناءً على النوع ---
                if prefix == "d": # كارت المطور
                    owner = r.get('Owner', '---')
                    label = f"🏗️ المطور: {r[0]}\n👤 الاونر: {owner}"
                else: # كارت المشروع
                    p_v = format_price_millions(r['Price']) if 'Price' in r else ""
                    label = f"🏢 {r[0]}\n📍 {r.get('Location','---')}\n💰 {p_v}"
                
                if st.button(label, key=f"card_{prefix}_{idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
        
        # أزرار التنقل
        st.write("")
        p1, px, p2 = st.columns([1, 1, 1])
        with p1: 
            if st.session_state[pg_key] > 0 and st.button("⬅ السابق", key=f"prev_{prefix}"): st.session_state[pg_key] -= 1; st.rerun()
        with px: st.markdown(f"<p style='text-align:center; color:#f59e0b;'>صفحة {st.session_state[pg_key]+1}</p>", unsafe_allow_html=True)
        with p2:
            if (start + 6) < len(filt) and st.button("التالي ➡", key=f"next_{prefix}"): st.session_state[pg_key] += 1; st.rerun()

# --- 5. التطبيق والواجهة ---
if not st.session_state.get('auth', False):
    # (كود صفحة تسجيل الدخول يوضع هنا كما في النسخ السابقة)
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("SIGN IN"):
        if p == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b; font-weight:bold;">مرحباً {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

st.markdown("""
    <div class="ticker-wrap"><div class="ticker">
        <span class="news-msg">🏗️ عقارات: أسعار المشاريع الجديدة تبدأ من 4.5 مليون ج.م في العاصمة الإدارية</span>
        <span class="news-msg">🟡 الذهب: عيار 21 يسجل استقراراً عند 3,640 ج.م اليوم</span>
        <span class="news-msg">🏢 تطوير: إطلاق المرحلة الجديدة من كمبوند "تاج سيتي" بمقدم 5%</span>
    </div></div>
""", unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000", "font-weight": "900"}})

if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.last_m = "grid", menu

if menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ جميع المشاريع", "🚀 المشاريع الجديدة"])
    with t1: render_grid(df_p, "p")
    with t2: render_grid(df_l, "l")
elif menu == "المطورين":
    render_grid(df_d, "d")
elif menu == "أدوات الحساب":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات البروكر</h2>", unsafe_allow_html=True)
    # (كود الحاسبة يوضع هنا)
