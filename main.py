import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة الحالة (Session State) ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'last_m' not in st.session_state: st.session_state.last_m = "المشاريع"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'search_query' not in st.session_state: st.session_state.search_query = ""

# --- 3. الروابط ---
URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 4. وظائف البيانات ---
@st.cache_data(ttl=60)
def load_all_data():
    try:
        p = pd.read_csv(URL_PROJECTS).fillna("---")
        d = pd.read_csv(URL_DEVELOPERS).fillna("---")
        l = pd.read_csv(URL_LAUNCHES).fillna("---")
        return p, d, l
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def jump_to(menu_name, search_val):
    st.session_state.last_m = menu_name
    st.session_state.search_query = search_val
    st.session_state.view = "grid"
    st.rerun()

# --- 5. دالة العرض الذكية ---
def render_pro_grid(df, prefix):
    if st.session_state.view == f"details_{prefix}":
        # صفحة التفاصيل
        if st.button("⬅ عودة للقائمة", use_container_width=True):
            st.session_state.view = "grid"; st.rerun()
        
        item = df.iloc[st.session_state.current_index]
        st.markdown(f"<h2 style='color:#f59e0b; text-align:right;'>🏠 {item.iloc[0]}</h2>", unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, col in enumerate(df.columns):
            with cols[i % 3]:
                val = str(item[col])
                st.markdown('<div class="detail-card">', unsafe_allow_html=True)
                st.markdown(f'<p class="label-gold">{col}</p>', unsafe_allow_html=True)
                
                # ربط تفاعلي: إذا ضغطت على اسم المطور في صفحة المشروع
                if col in ['Developer', 'المطور'] and val != "---":
                    if st.button(f"🏢 ملف: {val}", key=f"btn_jump_{i}"):
                        jump_to("المطورين", val)
                
                # ربط تفاعلي: إذا ضغطت على اسم الشركة في صفحة المطور لمشاهدة مشاريعها
                elif col in ['Company', 'الشركة'] and prefix == "dev":
                    if st.button(f"🔍 مشاريع {val}", key=f"btn_proj_{i}"):
                        jump_to("المشاريع", val)
                
                else:
                    st.markdown(f'<p class="val-white">{val}</p>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # صفحة الشبكة (Grid)
        search = st.text_input("🔍 بحث ذكي...", value=st.session_state.search_query, key=f"search_{prefix}")
        st.session_state.search_query = "" # تصغير الكاش بعد الاستخدام
        
        filt = df[df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else df
        
        c_grid = st.columns(2)
        for i, (idx, r) in enumerate(filt.head(10).iterrows()):
            with c_grid[i % 2]:
                logo = r.get('Logo_URL', '')
                if logo and logo != "---":
                    st.markdown(f'<div style="background:white; text-align:center; border-radius:15px 15px 0 0; margin-bottom:-10px; padding:5px; border-right:10px solid #f59e0b;"><img src="{logo}" style="height:40px;"></div>', unsafe_allow_html=True)
                
                txt = f"🏢 {r[0]}\n📍 {r.get('Location', r.get('الموقع', '---'))}"
                if st.button(txt, key=f"card_{prefix}_{idx}", use_container_width=True):
                    st.session_state.current_index = idx
                    st.session_state.view = f"details_{prefix}"
                    st.rerun()

# --- 6. التصميم CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    .detail-card {{ background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; border-top: 4px solid #f59e0b; margin-bottom: 10px; }}
    .label-gold {{ color: #f59e0b; font-size: 14px; margin-bottom: 5px; }}
    .val-white {{ color: white; font-size: 18px; font-weight: 700; }}
    div.stButton > button {{ border-radius: 10px !important; font-weight: 700 !important; }}
    div.stButton > button[key*="card_"] {{ background: white !important; color: black !important; border-right: 10px solid #f59e0b !important; min-height: 100px !important; text-align: right !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 7. التنفيذ الرئيسي ---
if not st.session_state.auth:
    # صفحة دخول مبسطة
    _, cent, _ = st.columns([1,2,1])
    with cent:
        st.markdown("<h1 style='text-align:center; color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
        pwd = st.text_input("كلمة المرور", type="password")
        if st.button("دخول", use_container_width=True):
            if pwd == "2026": 
                st.session_state.auth = True
                st.rerun()
    st.stop()

df_p, df_d, df_l = load_all_data()

menu_list = ["المشاريع", "المطورين", "اللونشات", "أدوات الحساب"]
idx_start = menu_list.index(st.session_state.last_m)

menu = option_menu(None, menu_list, 
    icons=["search", "building", "rocket", "calculator"], 
    default_index=idx_start, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

if menu != st.session_state.last_m:
    st.session_state.last_m = menu
    st.session_state.view = "grid"
    st.rerun()

if menu == "المشاريع": render_pro_grid(df_p, "proj")
elif menu == "المطورين": render_pro_grid(df_d, "dev")
elif menu == "اللونشات": render_pro_grid(df_l, "lnch")
elif menu == "أدوات الحساب": st.write("قسم الحسابات")

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
