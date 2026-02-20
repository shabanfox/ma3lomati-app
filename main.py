import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة الحالة (Persistence) ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if 'current_user' not in st.session_state: 
    st.session_state.current_user = None

if 'view' not in st.session_state: 
    st.session_state.view = "grid"

if 'current_index' not in st.session_state: 
    st.session_state.current_index = 0

if 'page_num' not in st.session_state: 
    st.session_state.page_num = 0

# --- 3. الروابط والصور ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 4. وظائف النظام ---
def logout():
    st.session_state.auth = False
    st.session_state.current_user = None
    st.rerun()

@st.cache_data(ttl=60)
def load_data():
    try:
        U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
        U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
        U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
        
        p = pd.read_csv(U_P)
        d = pd.read_csv(U_D)
        l = pd.read_csv(U_L)
        
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except Exception as e:
        st.error(f"حدث خطأ في تحميل البيانات: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def render_grid(dataframe, prefix):
    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}", use_container_width=True):
            st.session_state.view = "grid"
            st.rerun()
        
        item = dataframe.iloc[st.session_state.current_index]
        st.markdown(f"<div class='detail-card'><h3 style='color:#f59e0b;'>🔍 {item[0]}</h3></div>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        cols = dataframe.columns
        split = len(cols)//3 + 1
        
        with c1:
            for k in cols[:split]:
                st.markdown(f"<p class='label-gold'>{k}</p><p class='val-white'>{item[k]}</p>", unsafe_allow_html=True)
        with c2:
            for k in cols[split:2*split]:
                st.markdown(f"<p class='label-gold'>{k}</p><p class='val-white'>{item[k]}</p>", unsafe_allow_html=True)
        with c3:
            for k in cols[2*split:]:
                st.markdown(f"<p class='label-gold'>{k}</p><p class='val-white'>{item[k]}</p>", unsafe_allow_html=True)
    else:
        search = st.text_input(f"🔍 بحث...", key=f"search_{prefix}")
        filt = dataframe[dataframe.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else dataframe
        
        start = st.session_state.page_num * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.75, 0.25])
        with m_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    card_content = f"🏠 {r[0]}\n🏗️ {r.get('Developer','---')}\n📍 {r.get('Location','---')}"
                    if st.button(card_content, key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index = idx
                        st.session_state.view = f"details_{prefix}"
                        st.rerun()
        
        with s_c:
            st.markdown("<p style='color:#f59e0b; font-weight:bold;'>📌 مقترحات</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(6).iterrows():
                if st.button(f"⭐ {str(s_row[0])[:15]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state.current_index = s_idx
                    st.session_state.view = f"details_{prefix}"
                    st.rerun()

# --- 5. CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; height: 0px; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)), url('{BG_IMG}');
        background-size: cover; direction: rtl; text-align: right; font-family: 'Cairo', sans-serif;
    }}
    .royal-header {{ background: rgba(0,0,0,0.6); border-bottom: 3px solid #f59e0b; padding: 30px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 20px; }}
    .label-gold {{ color: #f59e0b; font-weight: bold; margin-bottom: -5px; font-size: 14px; }}
    .val-white {{ color: white; font-size: 16px; border-bottom: 1px solid #333; padding-bottom: 5px; margin-bottom: 10px; }}
    div.stButton > button[key*="card_"] {{ background: white !important; color: black !important; border-right: 6px solid #f59e0b !important; min-height: 100px !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. تسجيل الدخول ---
if not st.session_state.auth:
    _, center, _ = st.columns([1, 2, 1])
    with center:
        st.markdown("<h1 style='color:#f59e0b; text-align:center;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة السر", type="password")
        if st.button("دخول", use_container_width=True):
            if p == "2026":
                st.session_state.auth = True
                st.session_state.current_user = u
                st.rerun()
            else:
                st.error("كلمة السر خطأ")
    st.stop()

# --- 7. عرض المنصة ---
df_p, df_d, df_l = load_data()

st.markdown(f'<div class="royal-header"><h1 style="margin:0; color:white;">MA3LOMATI PRO</h1><p style="color:#f59e0b;">مرحباً {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["briefcase", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

if menu == "أدوات البروكر":
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("💰 حاسبة القسط")
        price = st.number_input("السعر", value=1000000)
        years = st.number_input("السنين", value=7)
        st.write(f"القسط الشهري: { (price/years/12) if years>0 else 0 :,.0f}")
    with c2:
        st.info("📊 العمولات")
        deal = st.number_input("الصفقة", value=1000000)
        st.write(f"العمولة (2.5%): { (deal * 0.025) :,.0f}")
    with c3:
        st.info("📈 العائد ROI")
        st.write("احسب العائد الاستثماري لعميلك هنا")

elif menu == "المشاريع":
    t1, t2, t3 = st.tabs(["🏗️ الكل", "🚀 لونش", "⚖️ مقارنة"])
    with t1: render_grid(df_p, "proj")
    with t2: render_grid(df_l, "launch")
    with t3:
        p1 = st.selectbox("المشروع الأول", df_p.iloc[:,0].tolist(), key="comp1")
        p2 = st.selectbox("المشروع الثاني", df_p.iloc[:,0].tolist(), key="comp2")
        if p1 and p2:
            st.write("---")
            st.table(pd.concat([df_p[df_p.iloc[:,0]==p1].T, df_p[df_p.iloc[:,0]==p2].T], axis=1))

elif menu == "المساعد الذكي":
    st.success("🤖 ابحث بذكاء في بيانات 2026")
    q = st.text_input("عن ماذا تبحث؟")
    if q:
        st.dataframe(df_p[df_p.apply(lambda r: r.astype(str).str.contains(q, case=False).any(), axis=1)])

if st.button("🚪 خروج"): logout()
