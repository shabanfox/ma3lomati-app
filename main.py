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
    else:
        st.session_state.auth = False

if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0

# --- 3. الروابط والبيانات ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
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
        search = st.text_input(f"🔍 بحث...", key=f"search_{prefix}")
        filt = dataframe[dataframe.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else dataframe
        start = st.session_state.page_num * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        m_c, s_c = st.columns([0.76, 0.24])
        with m_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    # تكبير خط الكروت الأساسية
                    card_text = f"🏠 {r[0]}\n🏗️ المطور: {r.get('Developer','---')}\n📍 الموقع: {r.get('Location','---')}"
                    if st.button(card_text, key=f"card_{prefix}_{idx}"):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
        with s_c:
            st.markdown("<p style='color:#f59e0b; font-weight:bold; font-size:20px; border-bottom:1px solid #333;'>🏆 مقترحات</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(10).iterrows():
                if st.button(f"📌 {str(s_row[0])[:25]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()

# --- 5. التصميم CSS (تعديل أحجام الخطوط) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    .royal-header {{ background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}'); background-size: cover; padding: 40px 20px; text-align: center; border-radius: 0 0 40px 40px; border-bottom: 3px solid #f59e0b; }}
    .royal-header h1 {{ font-size: 50px !important; font-weight: 900 !important; color: white; }}
    
    /* تكبير خط الكروت */
    div.stButton > button {{ font-size: 20px !important; font-weight: 700 !important; font-family: 'Cairo', sans-serif !important; }}
    div.stButton > button[key*="card_"] {{ padding: 25px !important; line-height: 1.6 !important; }}

    /* تكبير خط التفاصيل والعدادات */
    .detail-card {{ background: rgba(20, 20, 20, 0.95); padding: 30px; border-radius: 20px; border-top: 6px solid #f59e0b; border: 1px solid #333; }}
    .detail-card h3 {{ font-size: 28px !important; color: #f59e0b; font-weight: 800; border-bottom: 2px solid #333; margin-bottom: 20px; }}
    .label-gold {{ color: #f59e0b; font-weight: 700; font-size: 20px; margin-bottom: 5px; }}
    .val-white {{ color: white; font-size: 24px; font-weight: 800; margin-bottom: 20px; padding-bottom: 8px; border-bottom: 1px solid #444; }}
    
    /* تكبير نصوص المدخلات */
    .stNumberInput label {{ font-size: 22px !important; color: #f59e0b !important; font-weight: 700 !important; }}
    input {{ font-size: 22px !important; font-weight: bold !important; }}
    
    /* القوائم والتبويبات */
    .nav-link {{ font-size: 22px !important; font-weight: 700 !important; }}
    .stTabs [data-baseweb="tab"] {{ font-size: 22px !important; font-weight: 700 !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. الواجهة الرئيسية ---
if not st.session_state.auth:
    st.warning("يرجى تسجيل الدخول"); st.stop()

st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1></div>', unsafe_allow_html=True)

c_user1, c_user2, c_user3 = st.columns([0.3, 0.4, 0.3])
with c_user2:
    st.markdown(f"<p style='color:#f59e0b; text-align:center; font-weight:900; font-size:26px;'>مرحباً {st.session_state.current_user}</p>", unsafe_allow_html=True)
    if st.button("🚪 تسجيل خروج", key="logout_top", use_container_width=True): logout()

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["briefcase", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={
        "nav-link": {"font-size": "20px", "font-weight": "700"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}
    })

if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.page_num, st.session_state.last_m = "grid", 0, menu

# --- 7. الأقسام ---
if menu == "أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center; font-size:35px; font-weight:900;'>🛠️ أدوات الحساب</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='detail-card'><h3>💰 القسط</h3>", unsafe_allow_html=True)
        pr = st.number_input("السعر", value=5000000, step=100000, key="n1")
        dp = st.number_input("المقدم %", value=10, key="n2")
        yr = st.number_input("السنين", value=8, key="n3")
        res = (pr - (pr * dp/100)) / (yr * 12) if yr > 0 else 0
        st.markdown(f"<p class='label-gold'>القسط الشهري:</p><p class='val-white'>{res:,.0f}</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='detail-card'><h3>📊 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("الصفقة", value=5000000, step=100000, key="n4")
        pct = st.number_input("النسبة %", value=2.5, step=0.1, key="n5")
        st.markdown(f"<p class='label-gold'>العمولة:</p><p class='val-white'>{deal * (pct/100):,.0f}</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='detail-card'><h3>📈 العائد ROI</h3>", unsafe_allow_html=True)
        buy = st.number_input("سعر الشراء", value=5000000, key="n6")
        rent = st.number_input("إيجار شهري", value=40000, key="n7")
        roi = ((rent * 12) / buy) * 100 if buy > 0 else 0
        st.markdown(f"<p class='label-gold'>العائد السنوي:</p><p class='val-white'>{roi:.2f} %</p></div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ جميع المشاريع", "🚀 اللونشات الحالية"])
    with t1: render_grid(pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv").fillna("---"), "proj")
    with t2: render_grid(pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv").fillna("---"), "launch")

elif menu == "المطورين":
    render_grid(pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv").fillna("---"), "dev")

st.markdown("<p style='text-align:center; color:#666; font-size:18px; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
