import streamlit as st
import pandas as pd
import requests
import feedparser
import time
from streamlit_option_menu import option_menu

# --- 1. الإعدادات والجماليات (The Ultra UI) ---
st.set_page_config(page_title="MA3LOMATI PRO | Ultra", layout="wide", initial_sidebar_state="collapsed")

MAIN_COLOR = "#f59e0b" # البرتقالي الذهبي
BG_DARK = "#0a0a0a"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; }}
    .block-container {{ padding: 0 !important; }}
    
    /* منع السكرول في الدخول فقط */
    {'''
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        height: 100vh !important;
    }
    ''' if not st.session_state.get('auth', False) else ""}

    [data-testid="stAppViewContainer"] {{
        background-color: {BG_DARK};
        direction: rtl !important;
        font-family: 'Cairo', sans-serif;
    }}

    /* تصميم كارت الدخول الاحترافي */
    .auth-bg {{
        display: flex; justify-content: center; align-items: center;
        height: 100vh; background: radial-gradient(circle at center, #1a1a1a 0%, #000 100%);
    }}
    .modern-auth-card {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(245, 158, 11, 0.2);
        padding: 40px; border-radius: 32px;
        width: 100%; max-width: 400px;
        backdrop-filter: blur(20px); text-align: center;
        box-shadow: 0 30px 60px rgba(0,0,0,0.8);
    }}

    /* الأزرار المطورة */
    .stButton > button {{
        background: linear-gradient(90deg, #f59e0b, #d97706) !important;
        color: black !important; font-weight: 900 !important;
        border-radius: 16px !important; border: none !important;
        height: 54px !important; transition: 0.4s all ease !important;
        width: 100% !important;
    }}
    .stButton > button:hover {{ transform: scale(1.02); box-shadow: 0 10px 20px rgba(245,158,11,0.3); }}

    /* كروت المشاريع (Ultra Modern) */
    .project-card-ui {{
        background: #111; border: 1px solid #222;
        border-radius: 24px; padding: 0px; overflow: hidden;
        margin-bottom: 25px; transition: 0.3s;
    }}
    .project-card-ui:hover {{ border-color: {MAIN_COLOR}; transform: translateY(-5px); }}
    
    .card-header {{ background: {MAIN_COLOR}; color: black; padding: 10px 20px; font-weight: 900; }}
    .card-body {{ padding: 20px; color: white; }}

    /* المنيو العلوي */
    .nav-container {{ padding: 10px 0; background: #000; border-bottom: 1px solid #111; }}
    </style>
""", unsafe_allow_html=True)

# --- 2. إدارة الحالة والبيانات ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"

@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        p = pd.read_csv(U_P).fillna("---")
        p.columns = [c.strip() for c in p.columns]
        return p
    except: return pd.DataFrame()

# --- 3. واجهة تسجيل الدخول (Ultra Design) ---
if not st.session_state.auth:
    st.markdown('<div class="auth-bg">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="modern-auth-card">', unsafe_allow_html=True)
        st.markdown(f'<h1 style="color:{MAIN_COLOR}; font-weight:900; margin:0;">M</h1>', unsafe_allow_html=True)
        st.markdown('<h3 style="color:white; margin-top:0;">MA3LOMATI <span style="font-weight:300; opacity:0.7;">PRO</span></h3>', unsafe_allow_html=True)
        
        u = st.text_input("User", placeholder="اسم المستخدم", label_visibility="collapsed")
        p = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed")
        
        if st.button("دخول آمن"):
            if p == "2026" or p == "123":
                st.session_state.auth = True; st.session_state.current_user = u if u else "User"; st.rerun()
            else: st.error("بيانات الدخول غير صحيحة")
        
        st.markdown('<p style="color:#444; font-size:12px; margin-top:20px;">v4.0 Ultra Edition 2026</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 4. الهيكل الداخلي بعد الدخول ---
df = load_data()

# المنيو الاحترافي
selected = option_menu(None, ["لوحة التحكم", "استكشاف المشاريع", "أدوات الحساب", "المساعد الذكي"], 
    icons=['grid-fill', 'search', 'calculator', 'robot'], 
    menu_icon="cast", default_index=1, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#000"},
        "icon": {"color": MAIN_COLOR, "font-size": "18px"}, 
        "nav-link": {"color": "white", "font-size": "14px", "text-align": "center", "margin":"0px"},
        "nav-link-selected": {"background-color": "rgba(245,158,11,0.1)", "color": MAIN_COLOR, "border-bottom": f"2px solid {MAIN_COLOR}"}
    }
)

# --- 5. محتوى الصفحات المطورة ---
if selected == "لوحة التحكم":
    st.markdown(f"<h2 style='color:white; padding:20px;'>مرحباً، {st.session_state.current_user} 👋</h2>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("إجمالي المشاريع", len(df), "+3")
    c2.metric("المطورين", "45", "نشط")
    c3.metric("تحديثات اليوم", "12", "+5")
    c4.metric("حالة السوق", "مستقر", "Premium")

elif selected == "استكشاف المشاريع":
    st.markdown("<div style='padding:20px;'>", unsafe_allow_html=True)
    search_col, filter_col = st.columns([0.7, 0.3])
    with search_col:
        query = st.text_input("🔍 ابحث عن أي تفاصيل...", placeholder="اكتب اسم المشروع، المنطقة، أو المطور")
    with filter_col:
        sort_opt = st.selectbox("ترتيب حسب", ["الأحدث", "السعر: من الأقل", "السعر: من الأعلى"])

    filt_df = df[df.apply(lambda r: r.astype(str).str.contains(query, case=False).any(), axis=1)] if query else df
    
    # عرض المشاريع بشكل Ultra Cards
    grid = st.columns(3)
    for i, (idx, row) in enumerate(filt_df.head(12).iterrows()):
        with grid[i % 3]:
            st.markdown(f"""
                <div class="project-card-ui">
                    <div class="card-header">{row.iloc[0]}</div>
                    <div class="card-body">
                        <p style="margin:0; opacity:0.6; font-size:12px;">الموقع</p>
                        <p style="margin-bottom:10px; font-weight:bold;">📍 {row.get('Location', '---')}</p>
                        <p style="margin:0; opacity:0.6; font-size:12px;">المطور</p>
                        <p style="margin-bottom:0;">🏗️ {row.get('Developer', '---')}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("عرض التفاصيل", key=f"btn_{idx}"):
                st.toast(f"جاري تحميل {row.iloc[0]}...")
    st.markdown("</div>", unsafe_allow_html=True)

elif selected == "أدوات الحساب":
    st.markdown("<div style='padding:30px;'>", unsafe_allow_html=True)
    col_calc1, col_calc2 = st.columns(2)
    with col_calc1:
        st.markdown(f"<h4 style='color:{MAIN_COLOR}'>💳 حاسبة الأقساط الذكية</h4>", unsafe_allow_html=True)
        price = st.number_input("سعر الوحدة", 1000000, step=100000)
        down_payment = st.slider("المقدم (%)", 0, 50, 10)
        years = st.slider("سنوات التقسيط", 1, 15, 8)
        
        rem = price * (1 - down_payment/100)
        monthly = rem / (years * 12)
        st.info(f"القسط الشهري: {monthly:,.0f} ج.م")
    st.markdown("</div>", unsafe_allow_html=True)

# زر الخروج العائم
st.sidebar.markdown("---")
if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state.auth = False
    st.rerun()

st.markdown("<p style='text-align:center; color:#333; margin-top:50px;'>MA3LOMATI ULTRA ENGINE © 2026</p>", unsafe_allow_html=True)
