import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. ستايلات CSS الملكية ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0rem !important; }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }
    .royal-header { 
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80'); 
        padding: 45px 20px; text-align: center; border-bottom: 3px solid #f59e0b; border-radius: 0 0 40px 40px; margin-bottom: 15px;
    }
    .royal-header h1 { color: #f59e0b; font-size: 3rem; font-weight: 900; margin: 0; }
    
    /* ستايل الكروت */
    div.stButton > button[key*="card_"] { background: white !important; color: black !important; border-right: 12px solid #f59e0b !important; border-radius: 15px !important; text-align: right !important; min-height: 120px !important; font-weight: 900 !important; }
    div.stButton > button[key*="linked_"] { background: rgba(245, 158, 11, 0.1) !important; color: #f59e0b !important; border: 1px solid #f59e0b !important; border-radius: 10px !important; font-weight: 700 !important; }
    
    .detail-card { background: rgba(30, 30, 30, 0.95); padding: 15px; border-radius: 15px; border-top: 5px solid #f59e0b; margin-bottom: 10px; }
    .label-gold { color: #f59e0b; font-weight: 900; font-size: 0.9rem; }
    .val-white { color: white; font-size: 1.1rem; font-weight: 700; }
    .section-title { color: #f59e0b; border-right: 5px solid #f59e0b; padding-right: 10px; margin: 30px 0 15px 0; font-weight: 900; font-size: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

# --- 3. تحميل البيانات ---
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
if 'current_index' not in st.session_state: st.session_state.current_index = 0

# --- 5. دالة العرض الرئيسية مع الربط الذكي ---
def render_grid(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0

    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}", use_container_width=True): 
            st.session_state.view = "grid"; st.rerun()
        
        item = dataframe.iloc[st.session_state.current_index]
        main_name = str(item.iloc[0])
        
        st.markdown(f"<h2 style='color:#f59e0b;'>💎 {main_name}</h2>", unsafe_allow_html=True)
        
        # عرض التفاصيل في كروت
        cols = st.columns(3)
        for i, col in enumerate(dataframe.columns):
            with cols[i % 3]:
                st.markdown(f'<div class="detail-card"><p class="label-gold">{col}</p><p class="val-white">{item[col]}</p></div>', unsafe_allow_html=True)
        
        # --- التعديل الجوهري: ربط المطور بمشاريعه ---
        if prefix == "d":
            st.markdown("<h3 class='section-title'>🏗️ مشاريع هذا المطور</h3>", unsafe_allow_html=True)
            # دمج مشاريع "جميع المشاريع" و "المشاريع الجديدة" للبحث فيها
            all_projs = pd.concat([df_p, df_l]).drop_duplicates().reset_index(drop=True)
            
            # البحث عن اسم المطور في كل الأعمدة (لضمان الدقة)
            related = all_projs[all_projs.apply(lambda row: row.astype(str).str.contains(main_name, case=False).any(), axis=1)]
            
            if not related.empty:
                r_grid = st.columns(2)
                for r_idx, (idx, r_row) in enumerate(related.iterrows()):
                    with r_grid[r_idx % 2]:
                        # كرت صغير للمشروع المرتبط
                        if st.button(f"🏢 {r_row.iloc[0]}\n📍 {r_row.get('Location','---')}", key=f"linked_{idx}", use_container_width=True):
                            # إذا ضغط عليه يفتح تفاصيله في قسم المشاريع
                            st.session_state.current_index = idx
                            st.session_state.view = "details_p"
                            st.rerun()
            else:
                st.warning("لم يتم العثور على مشاريع مسجلة لهذا المطور حالياً.")

    else:
        # البحث والفلترة
        search = st.text_input("🔍 ابحث هنا...", key=f"search_{prefix}")
        filt = dataframe[dataframe.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else dataframe
        
        start = st.session_state[pg_key] * 6
        disp = filt.iloc[start : start + 6]
        
        grid = st.columns(2)
        for i, (idx, r) in enumerate(disp.iterrows()):
            with grid[i%2]:
                if st.button(f"🏢 {r.iloc[0]}\n📍 {r.get('Location','---')}", key=f"card_{prefix}_{idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()

# --- 6. التطبيق الرئيسي ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    if st.text_input("Pass", type="password") == "2026": 
        st.session_state.auth = True; st.rerun()
    st.stop()

# زر الخروج العلوي
if st.button("🚪 تسجيل الخروج"):
    st.session_state.auth = False; st.rerun()

st.markdown('<div class="royal-header"><h1>MA3LOMATI PRO</h1></div>', unsafe_allow_html=True)

menu = option_menu(None, ["المطورين", "المشاريع", "أدوات الحساب"], 
    icons=["building", "search", "calculator"], default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000", "font-weight": "900"}})

# تغيير التاب يصفر العرض
if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.last_m = "grid", menu

if menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ جميع المشاريع", "🚀 المشاريع الجديدة"])
    with t1: render_grid(df_p, "p")
    with t2: render_grid(df_l, "l")
elif menu == "المطورين":
    render_grid(df_d, "d")
elif menu == "أدوات الحساب":
    st.info("أدوات الحساب والتقسيط")

st.markdown("<p style='text-align:center; color:#555; margin-top:50px; font-weight:bold;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
