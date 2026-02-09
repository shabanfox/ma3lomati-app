import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة الحالة والحفاظ على الجلسة ---
if 'auth' not in st.session_state:
    if "u_session" in st.query_params:
        st.session_state.auth, st.session_state.current_user = True, st.query_params["u_session"]
    else:
        st.session_state.auth = False

if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0

# --- 3. الروابط والبيانات ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 4. الوظائف ---
def logout():
    st.session_state.auth = False
    st.query_params.clear()
    st.rerun()

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
        search = st.text_input(f"🔍 بحث ذكي في {prefix}...", key=f"search_{prefix}")
        filt = dataframe[dataframe.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else dataframe
        start = st.session_state.page_num * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.76, 0.24])
        with m_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    # كروت المشاريع الفخمة
                    card_html = f"""
                    <div style="border-right: 8px solid #f59e0b; padding: 10px; background: white; border-radius: 15px; margin-bottom: 5px;">
                        <h3 style="color: #1a1a1a; margin: 0; font-size: 22px;">🏠 {r[0]}</h3>
                        <p style="color: #666; margin: 5px 0; font-size: 18px; font-weight: bold;">🏗️ {r.get('Developer','---')}</p>
                        <p style="color: #f59e0b; margin: 0; font-size: 16px;">📍 {r.get('Location','---')}</p>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                    if st.button(f"عرض التفاصيل | {r[0]}", key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()

# --- 5. التصميم CSS المطور ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    /* الهيدر المطور */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{HEADER_IMG}');
        background-size: cover; background-position: center;
        height: 250px; display: flex; flex-direction: column; align-items: center; justify-content: center;
        border-bottom: 5px solid #f59e0b; border-radius: 0 0 50px 50px; margin-bottom: 20px;
    }}
    .oval-header-text {{
        background: #000; border: 3px solid #f59e0b; border-radius: 50px;
        padding: 10px 60px; color: #f59e0b; font-size: 40px; font-weight: 900;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.3);
    }}
    /* تفاصيل الكروت */
    .detail-card {{ background: rgba(0,0,0,0.85); padding: 30px; border-radius: 25px; border: 2px solid #333; border-top: 8px solid #f59e0b; }}
    .label-gold {{ color: #f59e0b; font-weight: 700; font-size: 22px; margin-bottom: 0px; }}
    .val-white {{ color: white; font-size: 26px; font-weight: 800; border-bottom: 1px solid #444; margin-bottom: 15px; padding-bottom: 5px; }}
    
    /* أزرار الخروج والتحكم */
    div.stButton > button[key="logout_top"] {{ background: #ff4b4b !important; color: white !important; font-size: 20px !important; border-radius: 15px !important; font-weight: 900 !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. الواجهة ---
if not st.session_state.auth: st.info("يرجى تسجيل الدخول"); st.stop()

# عرض الهيدر المطور
st.markdown(f"""
    <div class="royal-header">
        <div class="oval-header-text">MA3LOMATI PRO</div>
        <p style="color: white; font-size: 24px; font-weight: 700; margin-top: 15px;">مرحباً بك يا {st.session_state.current_user} ✨</p>
    </div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([0.4, 0.2, 0.4])
with c2:
    if st.button("🚪 تسجيل خروج", key="logout_top", use_container_width=True): logout()

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["briefcase", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={
        "container": {"background-color": "#111", "border": "1px solid #f59e0b"},
        "nav-link": {"font-size": "22px", "font-weight": "700", "color": "white"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}
    })

if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.page_num, st.session_state.last_m = "grid", 0, menu

# --- 7. الأقسام ---
@st.cache_data(ttl=60)
def fetch_data(url): return pd.read_csv(url).fillna("---")

if menu == "أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center; font-size:40px; font-weight:900;'>🛠️ آلات الحساب الذكية</h2>", unsafe_allow_html=True)
    ca, cb, cc = st.columns(3)
    with ca:
        st.markdown("<div class='detail-card'><h3>💰 القسط</h3>", unsafe_allow_html=True)
        pr = st.number_input("سعر الوحدة", value=5000000, step=100000, key="calc1")
        dp = st.number_input("المقدم %", value=10, key="calc2")
        yr = st.number_input("السنين", value=8, key="calc3")
        st.markdown(f"<p class='label-gold'>القسط الشهري:</p><p class='val-white'>{((pr-(pr*dp/100))/(yr*12) if yr>0 else 0):,.0f}</p></div>", unsafe_allow_html=True)
    with cb:
        st.markdown("<div class='detail-card'><h3>📊 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("الصفقة", value=5000000, step=100000, key="calc4")
        pct = st.number_input("النسبة %", value=2.5, step=0.1, key="calc5")
        st.markdown(f"<p class='label-gold'>عمولتك الصافية:</p><p class='val-white'>{deal*(pct/100):,.0f}</p></div>", unsafe_allow_html=True)
    with cc:
        st.markdown("<div class='detail-card'><h3>📈 الاستثمار</h3>", unsafe_allow_html=True)
        buy = st.number_input("سعر الشراء", value=5000000, key="calc6")
        rent = st.number_input("إيجار متوقع", value=40000, key="calc7")
        st.markdown(f"<p class='label-gold'>العائد السنوي ROI:</p><p class='val-white'>{((rent*12)/buy*100 if buy>0 else 0):.2f} %</p></div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ جميع المشاريع", "🚀 اللونشات"])
    with t1: render_grid(fetch_data("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"), "proj")
    with t2: render_grid(fetch_data("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"), "launch")

elif menu == "المطورين":
    render_grid(fetch_data("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"), "dev")

st.markdown("<p style='text-align:center; color:#555; font-size:20px; margin-top:50px; font-weight:bold;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
