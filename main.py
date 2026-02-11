import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة الحالة ---
if 'auth' not in st.session_state:
    if "u_session" in st.query_params:
        st.session_state.auth, st.session_state.current_user = True, st.query_params["u_session"]
    else: st.session_state.auth = False

if 'view' not in st.session_state: st.session_state.view = "grid"
if 'page_num' not in st.session_state: st.session_state.page_num = 0

# --- 3. الروابط الأساسية ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 4. وظائف البيانات ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def logout():
    st.session_state.auth = False
    st.query_params.clear()
    st.rerun()

# --- 5. التصميم الرهيب (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* حذف المساحات البيضاء العلوية تماماً */
    header, [data-testid="stHeader"] {{ visibility: hidden; height: 0px; }}
    .block-container {{ padding-top: 0rem !important; padding-bottom: 0rem !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.93), rgba(0,0,0,0.93)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}

    /* تصميم الهيدر الجديد */
    .royal-header {{
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.3), rgba(0,0,0,0.85)), url('{HEADER_IMG}');
        background-size: cover; background-position: center;
        border-bottom: 5px solid #f59e0b; padding: 70px 20px; text-align: center;
        border-radius: 0 0 60px 60px; margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.7);
    }}
    .royal-header h1 {{ color: #f59e0b; font-size: 4rem; font-weight: 900; margin: 0; text-shadow: 3px 3px 10px #000; }}
    .royal-header p {{ color: #fff; font-size: 1.5rem; font-weight: 700; }}

    /* تكبير وتوضيح الخط في الكروت */
    div.stButton > button {{ 
        font-size: 1.2rem !important; 
        font-weight: 900 !important;
        transition: 0.3s;
    }}
    div.stButton > button[key*="card_"] {{ 
        background: #ffffff !important; 
        color: #111 !important; 
        border-right: 10px solid #f59e0b !important; 
        border-radius: 15px !important; 
        padding: 20px !important; 
        min-height: 140px !important; 
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }}
    div.stButton > button:hover {{ transform: scale(1.02); border-color: #fff !important; }}

    /* تفاصيل الكارت */
    .detail-card {{ background: rgba(25, 25, 25, 0.95); padding: 30px; border-radius: 25px; border: 1px solid #444; border-top: 6px solid #f59e0b; color: white; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 1.1rem; margin-bottom: 5px; }}
    .val-white {{ color: #fff; font-size: 1.3rem; font-weight: 700; border-bottom: 1px solid #333; margin-bottom: 15px; padding-bottom: 8px; }}
    
    /* منع الـ Scroll العشوائي */
    html {{ scroll-behavior: smooth; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. دالة العرض ---
def render_grid(dataframe, prefix):
    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}", use_container_width=True): 
            st.session_state.view = "grid"; st.rerun()
        item = dataframe.iloc[st.session_state.current_index]
        c1, c2, c3 = st.columns(3)
        cols = dataframe.columns
        for i, cs in enumerate([cols[:len(cols)//3+1], cols[len(cols)//3+1:2*len(cols)//3+1], cols[2*len(cols)//3+1:]]):
            with [c1, c2, c3][i]:
                h = '<div class="detail-card">'
                for k in cs: h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                st.markdown(h+'</div>', unsafe_allow_html=True)
    else:
        # فلاتر البحث
        f1, f2, f3 = st.columns([2, 2, 3])
        with f1: search = st.text_input("🔍 ابحث عن أي شيء...", key=f"s_{prefix}")
        with f2:
            loc_col = 'Location' if 'Location' in dataframe.columns else None
            sel_area = st.selectbox("📍 اختار المنطقة", ["الكل"] + sorted(dataframe[loc_col].unique().tolist()), key=f"l_{prefix}") if loc_col else "الكل"
        with f3:
            price_col = 'Price' if 'Price' in dataframe.columns else None
            if price_col:
                dataframe[price_col] = pd.to_numeric(dataframe[price_col].astype(str).str.replace(r'[^\d]', '', regex=True), errors='coerce').fillna(0)
                price_range = st.slider("💰 ميزانيتك (ج.م)", int(dataframe[price_col].min()), int(dataframe[price_col].max()), (int(dataframe[price_col].min()), int(dataframe[price_col].max())), key=f"p_{prefix}")
            else: price_range = None

        filt = dataframe.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_area != "الكل": filt = filt[filt[loc_col] == sel_area]
        if price_range: filt = filt[(filt[price_col] >= price_range[0]) & (filt[price_col] <= price_range[1])]

        start = st.session_state.page_num * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.78, 0.22])
        with m_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    if prefix == "dev":
                        owner = r.get('Owner', r.get('المالك', '---'))
                        txt = f"🏢 {r[0]}\n👤 المالك: {owner}"
                    else:
                        p_txt = f"{int(r['Price']):,}" if 'Price' in r else "---"
                        txt = f"🏠 {r[0]}\n📍 {r.get('Location','---')}\n💵 السعر: {p_txt}"
                    if st.button(txt, key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
            
            # التنقل
            st.write("---")
            p1, p_info, p2 = st.columns([1, 2, 1])
            with p1: 
                if st.session_state.page_num > 0:
                    if st.button("⬅ السابق", key=f"prev_{prefix}"): st.session_state.page_num -= 1; st.rerun()
            with p_info: st.markdown(f"<p style='text-align:center; color:#f59e0b; font-weight:900; font-size:1.2rem;'>صفحة {st.session_state.page_num + 1}</p>", unsafe_allow_html=True)
            with p2:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالي ➡", key=f"next_{prefix}"): st.session_state.page_num += 1; st.rerun()
        with s_c:
            st.markdown("<p style='color:#f59e0b; font-weight:900; font-size:1.3rem; border-bottom:2px solid #f59e0b;'>⭐ مقترحات</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(8).iterrows():
                if st.button(f"📌 {str(s_row[0])[:18]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()

# --- 7. التشغيل الرئيسي ---
if not st.session_state.auth:
    # (كود تسجيل الدخول هنا - كما هو في النسخة السابقة)
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO 2026</h1><p style='color:white;'>يرجى تسجيل الدخول</p></div>", unsafe_allow_html=True)
    st.stop()

df_p, df_d, df_l = load_data()

# الهيدر الملكي (بدون مساحة علوية)
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p>أهلاً بك يا {st.session_state.current_user} في عالمك العقاري</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "house", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000", "font-weight": "900"}})

if menu == "أدوات الحساب":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات البروكر الذكية</h2>", unsafe_allow_html=True)
    # (كود الحاسبات هنا)
elif menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ قاعدة البيانات الشاملة", "🚀 المشاريع الجديدة"])
    with t1: render_grid(df_p, "proj")
    with t2: render_grid(df_l, "launch")
elif menu == "المطورين":
    render_grid(df_d, "dev")
elif menu == "المساعد الذكي":
    st.info("نظام تحليل البيانات بالذكاء الاصطناعي قيد التحديث.")

st.write("<br><br>", unsafe_allow_html=True)
if st.button("🚪 تسجيل الخروج"): logout()
st.markdown("<p style='text-align:center; color:#666; font-weight:bold;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
