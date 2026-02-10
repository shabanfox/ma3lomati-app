import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة الحالة والحفاظ على الجلسة ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.current_user = ""

if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0

# --- 3. الروابط والبيانات ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 4. الوظائف الأساسية ---
def logout():
    st.session_state.auth = False
    st.rerun()

@st.cache_data(ttl=60)
def fetch_data(url): 
    try:
        return pd.read_csv(url).fillna("---")
    except:
        return pd.DataFrame({"خطأ": ["تعذر تحميل البيانات"]})

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
        search = st.text_input(f"🔍 بحث سريع في {prefix}...", key=f"search_{prefix}")
        filt = dataframe[dataframe.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else dataframe
        start = st.session_state.page_num * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.76, 0.24])
        with m_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    card_text = f"🏠 {r[0]}\n🏗️ المطور: {r.get('Developer','---')}\n📍 الموقع: {r.get('Location','---')}"
                    if st.button(card_text, key=f"card_{prefix}_{idx}"):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            p1, p2, p3 = st.columns([1,2,1])
            with p1:
                if st.session_state.page_num > 0:
                    if st.button("⬅ السابق", key=f"p_{prefix}"): st.session_state.page_num -= 1; st.rerun()
            with p3:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالي ➡", key=f"n_{prefix}"): st.session_state.page_num += 1; st.rerun()
                    
        with s_c:
            st.markdown("<p style='color:#f59e0b; font-weight:900; font-size:22px; border-bottom:1px solid #333;'>🏆 مقترحات</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(10).iterrows():
                if st.button(f"📌 {str(s_row[0])[:20]}...", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()

# --- 5. التصميم CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.94), rgba(0,0,0,0.94)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{HEADER_IMG}');
        background-size: cover; background-position: center;
        height: 200px; display: flex; flex-direction: column; align-items: center; justify-content: center;
        border-bottom: 5px solid #f59e0b; border-radius: 0 0 50px 50px; margin-bottom: 20px;
    }}
    .oval-header-text {{
        background: #000; border: 3px solid #f59e0b; border-radius: 50px;
        padding: 10px 50px; color: #f59e0b; font-size: 32px; font-weight: 900;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.4);
    }}
    div.stButton > button[key*="card_"] {{
        background: linear-gradient(145deg, #ffffff, #f0f0f0) !important;
        color: #1a1a1a !important; border: none !important;
        border-right: 10px solid #f59e0b !important; border-radius: 20px !important;
        padding: 25px !important; text-align: right !important; font-size: 18px !important;
        font-weight: 800 !important; min-height: 150px !important; width: 100% !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2) !important;
    }}
    .detail-card {{ background: rgba(0,0,0,0.8); padding: 25px; border-radius: 20px; border: 1px solid #444; border-top: 6px solid #f59e0b; margin-bottom:15px; }}
    .label-gold {{ color: #f59e0b; font-weight: 700; font-size: 18px; margin:0; }}
    .val-white {{ color: white; font-size: 20px; font-weight: 800; border-bottom: 1px solid #333; margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. منطق تسجيل الدخول ---
if not st.session_state.auth:
    st.markdown('<div class="royal-header"><div class="oval-header-text">MA3LOMATI LOGIN</div></div>', unsafe_allow_html=True)
    _, col_log, _ = st.columns([1, 1, 1])
    with col_log:
        st.markdown('<div class="detail-card" style="text-align:center;">', unsafe_allow_html=True)
        user = st.text_input("اسم المستخدم")
        pw = st.text_input("كلمة المرور", type="password")
        if st.button("دخول النظام 🚀", use_container_width=True):
            if user != "" and pw == "2026": # كلمة المرور الافتراضية
                st.session_state.auth = True
                st.session_state.current_user = user
                st.rerun()
            else:
                st.error("خطأ في البيانات")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 7. الواجهة الرئيسية (بعد الدخول) ---
st.markdown(f'<div class="royal-header"><div class="oval-header-text">MA3LOMATI PRO</div></div>', unsafe_allow_html=True)

c_top1, c_top2, c_top3 = st.columns([0.3, 0.4, 0.3])
with c_top2:
    st.markdown(f"<p style='color:#f59e0b; text-align:center; font-weight:900; font-size:22px;'>مرحباً: {st.session_state.current_user}</p>", unsafe_allow_html=True)
    if st.button("🚪 تسجيل الخروج", use_container_width=True): logout()

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["briefcase", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={
        "container": {"background-color": "#000", "border": "1px solid #f59e0b", "border-radius": "15px"},
        "nav-link": {"font-size": "18px", "font-weight": "700", "color": "white"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}
    })

# تصفير الحالة عند تغيير القسم
if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.page_num, st.session_state.last_m = "grid", 0, menu

# --- الأقسام ---
if menu == "أدوات البروكر":
    ca, cb, cc = st.columns(3)
    with ca:
        st.markdown("<div class='detail-card'><h3>💰 القسط</h3>", unsafe_allow_html=True)
        pr = st.number_input("سعر الوحدة", value=5000000)
        dp = st.number_input("المقدم %", value=10)
        yr = st.number_input("السنين", value=8)
        st.markdown(f"<p class='label-gold'>الشهري:</p><p class='val-white'>{((pr-(pr*dp/100))/(yr*12) if yr>0 else 0):,.0f}</p></div>", unsafe_allow_html=True)
    with cb:
        st.markdown("<div class='detail-card'><h3>📊 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("الصفقة", value=5000000)
        pct = st.number_input("النسبة %", value=2.5)
        st.markdown(f"<p class='label-gold'>عمولتك:</p><p class='val-white'>{deal*(pct/100):,.0f}</p></div>", unsafe_allow_html=True)
    with cc:
        st.markdown("<div class='detail-card'><h3>📈 ROI</h3>", unsafe_allow_html=True)
        buy = st.number_input("الشراء", value=5000000)
        rent = st.number_input("الإيجار", value=40000)
        st.markdown(f"<p class='label-gold'>العائد السنوي:</p><p class='val-white'>{((rent*12)/buy*100 if buy>0 else 0):.2f} %</p></div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ جميع المشاريع", "🚀 اللونشات"])
    with t1: render_grid(fetch_data("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"), "proj")
    with t2: render_grid(fetch_data("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"), "launch")

elif menu == "المطورين":
    render_grid(fetch_data("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"), "dev")

st.markdown("<p style='text-align:center; color:#555; font-size:14px; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)

