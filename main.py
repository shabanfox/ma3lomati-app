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
        st.session_state.auth = True
        st.session_state.current_user = st.query_params["u_session"]
    else:
        st.session_state.auth = False

if 'current_user' not in st.session_state: st.session_state.current_user = None
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
            st.session_state.view = "grid"
            st.rerun()
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
        m_col, s_col = st.columns([0.76, 0.24])
        with m_col:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    card_text = f"🏠 {r[0]}\n🏗️ المطور: {r.get('Developer','---')}\n📍 الموقع: {r.get('Location','---')}"
                    if st.button(card_text, key=f"card_{prefix}_{idx}"):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"
                        st.rerun()

# --- 5. التصميم CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    .royal-header {{ background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}'); background-size: cover; background-position: center; border-bottom: 3px solid #f59e0b; padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 10px; }}
    div.stButton > button[key*="card_"] {{ background: linear-gradient(145deg, #ffffff, #f9f9f9) !important; color: #1a1a1a !important; border-right: 6px solid #f59e0b !important; border-radius: 15px !important; padding: 20px !important; text-align: right !important; min-height: 160px !important; width: 100% !important; }}
    .detail-card {{ background: rgba(20, 20, 20, 0.9); padding: 25px; border-radius: 20px; border-top: 5px solid #f59e0b; color: white; border: 1px solid #333; margin-bottom: 10px; min-height: 400px; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; margin-bottom: 2px; }}
    .val-white {{ color: white; font-size: 20px; font-weight: bold; margin-bottom: 15px; border-bottom: 1px solid #333; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. تسجيل الدخول ---
if not st.session_state.auth:
    st.title("MA3LOMATI PRO - Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("دخول"):
        if p == "2026":
            st.session_state.auth, st.session_state.current_user = True, u
            st.query_params["u_session"] = u
            st.rerun()
    st.stop()

# --- 7. تحميل البيانات ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
    for df in [p, d, l]: df.columns = [c.strip() for c in df.columns]
    return p.fillna("---"), d.fillna("---"), l.fillna("---")

df_p, df_d, df_l = load_data()

# --- 8. الواجهة ---
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b;">مرحباً {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["briefcase", "building", "search", "robot"], default_index=0, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

if menu == "أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات الحساب الدقيقة</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='detail-card'>", unsafe_allow_html=True)
        st.subheader("💰 حساب القسط")
        price = st.number_input("سعر الوحدة", value=5000000, step=100000, key="calc_p")
        down_pct = st.number_input("نسبة المقدم (%)", value=10, key="calc_d")
        years = st.number_input("سنين التقسيط", value=8, key="calc_y")
        
        dp_val = price * (down_pct / 100)
        rem_val = price - dp_val
        monthly = rem_val / (years * 12) if years > 0 else 0
        
        st.markdown(f"<p class='label-gold'>المقدم المطلوب:</p><p class='val-white'>{dp_val:,.0f}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='label-gold'>القسط الشهري:</p><p class='val-white'>{monthly:,.0f}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='label-gold'>القسط الربع سنوي:</p><p class='val-white'>{monthly*3:,.0f}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='detail-card'>", unsafe_allow_html=True)
        st.subheader("📊 حساب العمولة")
        deal_v = st.number_input("قيمة الصفقة", value=5000000, step=100000, key="comm_v")
        comm_p = st.number_input("نسبة العمولة (%)", value=2.5, step=0.1, key="comm_p")
        
        c_val = deal_v * (comm_p / 100)
        tax = c_val * 0.14
        
        st.markdown(f"<p class='label-gold'>العمولة قبل الضريبة:</p><p class='val-white'>{c_val:,.0f}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='label-gold'>خصم ضريبة (14%):</p><p class='val-white'>{tax:,.0f}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='label-gold'>صافي الربح:</p><p class='val-white'>{c_val - tax:,.0f}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='detail-card'>", unsafe_allow_html=True)
        st.subheader("📈 حساب الاستثمار")
        b_p = st.number_input("سعر الشراء", value=5000000, key="inv_b")
        r_p = st.number_input("الإيجار الشهري", value=40000, key="inv_r")
        inc = st.number_input("الزيادة السنوية (%)", value=15, key="inv_i")
        
        roi = ((r_p * 12) / b_p) * 100 if b_p > 0 else 0
        f_val = b_p * (1 + inc/100)
        
        st.markdown(f"<p class='label-gold'>العائد الإيجاري السنوي:</p><p class='val-white'>{roi:.2f} %</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='label-gold'>قيمة العقار بعد سنة:</p><p class='val-white'>{f_val:,.0f}</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='label-gold'>إجمالي الربح المتوقع:</p><p class='val-white'>{(r_p*12)+(f_val-b_p):,.0f}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ المشاريع", "🚀 اللونشات"])
    with t1: render_grid(df_p, "proj")
    with t2: render_grid(df_l, "launch")

elif menu == "المطورين":
    render_grid(df_d, "dev")

elif menu == "المساعد الذكي":
    st.chat_input("اسألني عن أي حاجة...")

if st.button("🚪 خروج"): logout()
