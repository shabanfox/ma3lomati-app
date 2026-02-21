import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. التصميم البصري الكامل (CSS) ---
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
        width: 100%; background: rgba(245, 158, 11, 0.15); border-bottom: 1px solid #f59e0b;
        overflow: hidden; white-space: nowrap; padding: 12px 0; margin-bottom: 20px;
    }
    .ticker { display: inline-block; animation: ticker 40s linear infinite; color: #f59e0b; font-weight: bold; font-size: 1.1rem; }
    .news-msg { margin: 0 60px; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-150%); } }

    /* الكروت */
    div.stButton > button[key*="card_"] { 
        background: white !important; color: black !important; border-right: 12px solid #f59e0b !important; 
        border-radius: 15px !important; text-align: right !important; min-height: 140px !important; 
        font-weight: 900 !important; font-size: 1.1rem !important; white-space: pre-wrap !important; 
    }
    .detail-card { 
        background: rgba(30, 30, 30, 0.95); padding: 20px; border-radius: 15px; 
        border: 1px solid #444; border-top: 6px solid #f59e0b; margin-bottom: 15px; 
    }
    .label-gold { color: #f59e0b; font-weight: 900; font-size: 1rem; }
    .val-white { color: white; font-size: 1.25rem; font-weight: 700; }
    .filter-box { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 20px; border: 1px solid #333; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. الوظائف والبيانات ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

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
        results = []
        for url in urls:
            df = pd.read_csv(url)
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area':'Location','الموقع':'Location','السعر':'Price','المالك':'Owner','الاونر':'Owner'}, inplace=True, errors="ignore")
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
                df['Price'] = df['Price'].apply(lambda x: x * 1_000_000 if 0 < x < 1000 else x)
            results.append(df.fillna("---"))
        return results
    except: return [pd.DataFrame()]*3

df_p, df_d, df_l = load_data()

# --- 4. بوابة الدخول ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:80px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("SIGN IN 🚀", use_container_width=True):
        if p == "2026": # كلمة السر السريعة
            st.session_state.auth, st.session_state.current_user = True, u if u else "Admin"
            st.rerun()
    st.stop()

# --- 5. الهيكل الرئيسي ---
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b; font-weight:bold;">مرحباً {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

st.markdown("""
    <div class="ticker-wrap"><div class="ticker">
        <span class="news-msg">🔥 عاجل: ارتفاع الطلب على الساحل الشمالي بنسبة 20% في صيف 2026</span>
        <span class="news-msg">🏢 تطوير: إطلاق مشاريع جديدة بمقدم يبدأ من 5% وأقساط حتى 10 سنوات</span>
        <span class="news-msg">🟡 الذهب: سعر عيار 21 يسجل استقراراً ملحوظاً عند 3,640 ج.م اليوم</span>
        <span class="news-msg">🏗️ تنويه: تحديث قوائم أسعار مشاريع أورا وسوديك في القائمة الرئيسية</span>
    </div></div>
""", unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000", "font-weight": "900"}})

if 'view' not in st.session_state: st.session_state.view = "grid"

# --- 6. دالة العرض المخصصة ---
def render_page(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0

    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة", key=f"back_{prefix}"): st.session_state.view = "grid"; st.rerun()
        item = dataframe.iloc[st.session_state.current_index]
        st.markdown(f"<h2 style='color:#f59e0b; text-align:right;'>💎 {item.iloc[0]}</h2>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, col in enumerate(dataframe.columns):
            with cols[i%3]:
                val = format_price_millions(item[col]) if col == 'Price' else item[col]
                st.markdown(f'<div class="detail-card"><p class="label-gold">{col}</p><p class="val-white">{val}</p></div>', unsafe_allow_html=True)
    else:
        # فلاتر
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        c1, c2 = st.columns([2, 1])
        with c1: search = st.text_input("🔍 بحث...", key=f"search_{prefix}")
        with c2: 
            loc_list = ["الكل"] + sorted(list(dataframe['Location'].unique())) if 'Location' in dataframe.columns else ["الكل"]
            sel_loc = st.selectbox("📍 الموقع", loc_list, key=f"loc_{prefix}")
        st.markdown('</div>', unsafe_allow_html=True)

        filt = dataframe.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_loc != "الكل" and 'Location' in filt.columns: filt = filt[filt['Location'] == sel_loc]

        start = st.session_state[pg_key] * 6
        disp = filt.iloc[start : start + 6]
        
        grid = st.columns(2)
        for i, (idx, r) in enumerate(disp.iterrows()):
            with grid[i%2]:
                if prefix == "d": # كارت المطور: الاسم + الأونر
                    lbl = f"🏗️ المطور: {r[0]}\n👤 الاونر: {r.get('Owner', '---')}"
                else: # كارت المشروع: الاسم + الموقع + السعر بالملايين
                    p_txt = format_price_millions(r['Price']) if 'Price' in r else ""
                    lbl = f"🏢 {r[0]}\n📍 {r.get('Location','---')}\n💰 {p_txt}"
                
                if st.button(lbl, key=f"card_{prefix}_{idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()

# --- 7. عرض الأقسام ---
if menu == "المشاريع":
    render_page(df_p, "p")
elif menu == "المطورين":
    render_page(df_d, "d")
elif menu == "أدوات الحساب":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات البروكر</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='detail-card'><h3>💰 القسط</h3>", unsafe_allow_html=True)
        pr = st.number_input("السعر", value=5000000, step=100000)
        dp = st.number_input("المقدم (%)", value=10)
        yr = st.number_input("السنين", value=8)
        res = (pr - (pr * dp/100)) / (yr * 12) if yr > 0 else 0
        st.markdown(f"<p class='label-gold'>الشهري:</p><p class='val-white'>{res:,.0f} ج.م</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='detail-card'><h3>📊 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("الصفقة", value=5000000, step=100000)
        pct = st.number_input("النسبة (%)", value=2.5)
        st.markdown(f"<p class='label-gold'>العمولة:</p><p class='val-white'>{deal*(pct/100):,.0f} ج.م</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='detail-card'><h3>📈 ROI</h3>", unsafe_allow_html=True)
        buy = st.number_input("الشراء", value=5000000, step=100000)
        rent = st.number_input("الإيجار", value=40000, step=1000)
        roi = ((rent * 12) / buy) * 100 if buy > 0 else 0
        st.markdown(f"<p class='label-gold'>العائد السنوي:</p><p class='val-white'>{roi:.2f} %</p></div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
