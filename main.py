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

    /* --- شريط الأخبار المتحرك --- */
    .news-ticker-container {
        width: 100%; overflow: hidden; background: rgba(245, 158, 11, 0.1);
        border-bottom: 1px solid #f59e0b; padding: 10px 0; position: relative;
    }
    .ticker-text {
        display: inline-block; white-space: nowrap; padding-left: 100%;
        animation: ticker 40s linear infinite; color: #f59e0b; font-weight: bold; font-size: 1.1rem;
    }
    .ticker-text:hover { animation-play-state: paused; cursor: pointer; }
    @keyframes ticker {
        0% { transform: translateX(0); }
        100% { transform: translateX(-150%); }
    }
    .news-sep { margin: 0 40px; color: #fff; }

    .royal-header { 
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80'); 
        border-bottom: 3px solid #f59e0b; padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 15px;
    }
    .royal-header h1 { color: #f59e0b; font-size: 3rem; font-weight: 900; margin: 0; }

    /* ستايل الكروت والربط */
    div.stButton > button[key*="card_"] { background: white !important; color: black !important; border-right: 12px solid #f59e0b !important; border-radius: 15px !important; text-align: right !important; min-height: 150px !important; font-weight: 900 !important; }
    div.stButton > button[key*="linked_"] { background: #f59e0b !important; color: #000 !important; font-weight: 900 !important; border-radius: 10px !important; }
    .detail-card { background: rgba(30, 30, 30, 0.95); padding: 20px; border-radius: 15px; border-top: 6px solid #f59e0b; margin-bottom: 15px; }
    .label-gold { color: #f59e0b; font-weight: 900; font-size: 1rem; }
    .val-white { color: white; font-size: 1.25rem; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# --- 3. تحميل البيانات والوظائف التقنية ---
@st.cache_data(ttl=300, show_spinner=False)
def load_data():
    try:
        p = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv")
        d = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv")
        l = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv")
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price', 'المطور': 'Developer'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 4. إدارة الجلسة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'view' not in st.session_state: st.session_state.view = "grid"

# --- 5. دالة العرض الرئيسية مع "الربط الذكي" ---
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
        for i, col in enumerate(dataframe.columns):
            with cols[i % 3]:
                st.markdown(f'<div class="detail-card"><p class="label-gold">{col}</p><p class="val-white">{item[col]}</p></div>', unsafe_allow_html=True)
        
        # --- ميزة الربط (تظهر في صفحة المطورين فقط) ---
        if prefix == "d":
            st.markdown("<h3 style='color:#f59e0b; border-right:5px solid #f59e0b; padding-right:10px;'>🏗️ مشاريع المطور</h3>", unsafe_allow_html=True)
            # البحث عن اسم المطور في كل جداول المشاريع
            all_data = pd.concat([df_p, df_l]).drop_duplicates().reset_index(drop=True)
            related = all_data[all_data.apply(lambda row: row.astype(str).str.contains(main_name, case=False).any(), axis=1)]
            
            if not related.empty:
                r_cols = st.columns(2)
                for r_idx, (idx, r_row) in enumerate(related.iterrows()):
                    with r_cols[r_idx % 2]:
                        st.button(f"🏢 {r_row.iloc[0]} | 📍 {r_row.get('Location','---')}", key=f"linked_{idx}", use_container_width=True)
            else:
                st.info("لا توجد مشاريع مرتبطة حالياً.")

    else:
        search = st.text_input("🔍 بحث...", key=f"s_{prefix}")
        filt = dataframe[dataframe.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else dataframe
        
        start = st.session_state[pg_key] * 6
        disp = filt.iloc[start : start + 6]
        
        grid = st.columns(2)
        for i, (idx, r) in enumerate(disp.iterrows()):
            with grid[i%2]:
                if st.button(f"🏢 {r[0]}\n📍 {r.get('Location','---')}", key=f"card_{prefix}_{idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()

# --- 6. بوابة الدخول ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    if st.text_input("Password", type="password") == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- 7. التطبيق الرئيسي ---
# شريط الأخبار المتحرك (News Ticker)
st.markdown("""
    <div class="news-ticker-container">
        <div class="ticker-text">
            <span>🚀 عقارات: إطلاق المرحلة الجديدة في العاصمة الإدارية 2026</span><span class="news-sep">|</span>
            <span>💰 الذهب: استقرار عيار 21 عند مستويات قياسية اليوم</span><span class="news-sep">|</span>
            <span>💵 الدولار: تحديثات مستمرة لأسعار الصرف في البنوك المصرية</span><span class="news-sep">|</span>
            <span>🏗️ تطوير: شراكة عالمية جديدة لأكبر مطور عقاري في مصر</span><span class="news-sep">|</span>
            <span>📈 استثمار: ارتفاع عوائد الإيجار في التجمع الخامس بنسبة 15%</span>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="royal-header"><h1>MA3LOMATI PRO</h1></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

if menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ جميع المشاريع", "🚀 المشاريع الجديدة"])
    with t1: render_grid(df_p, "p")
    with t2: render_grid(df_l, "l")
elif menu == "المطورين":
    render_grid(df_d, "d")
elif menu == "أدوات الحساب":
    st.info("أدوات الحساب والتقسيط جاهزة.")

st.markdown("<p style='text-align:center; color:#555; margin-top:50px; font-weight:bold;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
