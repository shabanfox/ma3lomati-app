import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. التصميم البصري (CSS) الفخم ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0rem !important; }
    [data-testid="stAppViewContainer"] {
        background: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }
    .royal-header { 
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover; background-position: center; border-bottom: 4px solid #f59e0b; padding: 50px 20px; text-align: center; border-radius: 0 0 50px 50px; margin-bottom: 0px;
    }
    .royal-header h1 { color: #f59e0b; font-size: 3.5rem; font-weight: 900; margin: 0; }
    .ticker-wrap {
        width: 100%; background: rgba(245, 158, 11, 0.1); border-bottom: 1px solid #333; overflow: hidden; white-space: nowrap; padding: 15px 0; margin-bottom: 25px;
    }
    .ticker { display: inline-block; animation: ticker 45s linear infinite; color: #f59e0b; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-150%); } }
    div.stButton > button[key*="card_"] { 
        background: white !important; color: #000 !important; border-right: 15px solid #f59e0b !important; border-radius: 15px !important; text-align: right !important; min-height: 140px !important; font-weight: 900 !important; font-size: 1.2rem !important;
    }
    div.stButton > button[key*="side_"] {
        background: #111 !important; color: #f59e0b !important; border: 1px solid #f59e0b !important; border-radius: 12px !important; margin-bottom: 8px !important;
    }
    .detail-card { background: #111; padding: 25px; border-radius: 20px; border-top: 6px solid #f59e0b; margin-bottom: 15px; }
    .label-gold { color: #f59e0b; font-weight: 900; }
    .val-white { color: white; font-size: 1.4rem; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# --- 3. البيانات والربط بالشيت ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

def format_p(val):
    try:
        v = float(val)
        return f"{v/1_000_000:,.2f} مليون ج.م" if v >= 1_000_000 else f"{v:,.0f} ج.م"
    except: return "اتصل للسعر"

@st.cache_data(ttl=300)
def load_all_data():
    urls = [
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv", # المشاريع
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv", # المطورين
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"  # لانش جديد
    ]
    dfs = []
    for u in urls:
        df = pd.read_csv(u)
        df.columns = [c.strip() for c in df.columns]
        df.rename(columns={'Area':'Location','الموقع':'Location','السعر':'Price','الاونر':'Owner','صاحب الشركة':'Owner'}, inplace=True, errors="ignore")
        if 'Price' in df.columns:
            df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
            df['Price'] = df['Price'].apply(lambda x: x * 1_000_000 if 0 < x < 1000 else x)
        dfs.append(df.fillna("---"))
    return dfs

def login_check(u, p):
    try:
        res = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=5)
        if res.status_code == 200:
            for user in res.json():
                if str(u).strip().lower() == str(user.get('Name','')).strip().lower() and str(p) == str(user.get('Password','')):
                    return user.get('Name')
    except: pass
    return None

# --- 4. الدخول ---
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h1 style='color:#f59e0b; text-align:center; padding-top:100px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    u = st.text_input("اسم المستخدم")
    p = st.text_input("كلمة المرور", type="password")
    if st.button("دخول 🚀"):
        user = "Admin" if p == "2026" else login_check(u, p)
        if user: st.session_state.auth, st.session_state.user = True, user; st.rerun()
    st.stop()

# --- 5. الهيكل والمنيو ---
df_p, df_d, df_l = load_all_data()
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b;">مرحباً {st.session_state.user} | 2026</p></div>', unsafe_allow_html=True)
st.markdown('<div class="ticker-wrap"><div class="ticker">🔥 جديد: مشاريع الساحل 2026 متوفرة الآن | 🏗️ استقرار أسعار التجمع والشروق | 💎 خصومات حصرية للمنصة</div></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "لانش جديد", "المشاريع"], 
    icons=["calculator", "building", "rocket", "search"], default_index=3, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

if 'view' not in st.session_state: st.session_state.view = "grid"

# --- 6. دالة العرض 70/30 ---
def render_ui(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0
    col_main, col_side = st.columns([0.7, 0.3])

    with col_main:
        if st.session_state.view == f"details_{prefix}":
            if st.button("⬅ عودة", key=f"bk_{prefix}"): st.session_state.view = "grid"; st.rerun()
            item = dataframe.iloc[st.session_state.current_index]
            st.markdown(f"<h2 style='color:#f59e0b;'>💎 {item.iloc[0]}</h2>", unsafe_allow_html=True)
            for c in dataframe.columns:
                v = format_p(item[c]) if c == 'Price' else item[c]
                st.markdown(f'<div class="detail-card"><p class="label-gold">{c}</p><p class="val-white">{v}</p></div>', unsafe_allow_html=True)
        else:
            search = st.text_input("🔍 بحث...", key=f"s_{prefix}")
            filt = dataframe[dataframe.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else dataframe
            start = st.session_state[pg_key] * 6
            disp = filt.iloc[start : start + 6]
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    lbl = f"🏗️ {r[0]}\n👤 الاونر: {r.get('Owner','---')}" if prefix=="d" else f"🏢 {r[0]}\n📍 {r.get('Location','---')}\n💰 {format_p(r.get('Price',0))}"
                    if st.button(lbl, key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
            if len(filt)>6:
                c1, c2 = st.columns(2)
                with c1: 
                    if st.session_state[pg_key]>0 and st.button("السابق", key=f"pr_{prefix}"): st.session_state[pg_key]-=1; st.rerun()
                with c2:
                    if (start+6)<len(filt) and st.button("التالي", key=f"nx_{prefix}"): st.session_state[pg_key]+=1; st.rerun()

    with col_side:
        st.markdown("<h3 style='color:#f59e0b;'>⭐ مقترحات</h3>", unsafe_allow_html=True)
        for s_idx, s_row in dataframe.head(8).iterrows():
            if st.button(f"📌 {s_row.iloc[0]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()

# --- 7. الأقسام ---
if menu == "المشاريع": render_ui(df_p, "p")
elif menu == "لانش جديد": render_ui(df_l, "l")
elif menu == "المطورين": render_ui(df_d, "d")
elif menu == "أدوات الحساب":
    cm, cs = st.columns([0.7, 0.3])
    with cm:
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ حاسبات البروكر</h2>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["💰 القسط", "📊 العمولة"])
        with t1:
            pr = st.number_input("السعر", value=5000000)
            yr = st.number_input("السنين", value=8)
            st.success(f"القسط الشهري: {(pr*0.9)/(yr*12):,.0f} ج.م")
        with t2:
            dl = st.number_input("قيمة الصفقة", value=5000000)
            st.success(f"العمولة (2.5%): {dl*0.025:,.0f} ج.م")
