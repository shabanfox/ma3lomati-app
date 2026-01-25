import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | Luxury Edition", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الهوية البصرية الجديدة ---
# الألوان: ذهبي ملكي، أسود عميق، رمادي فحمي
MAIN_COLOR = "#D4AF37"  # Golden
ACCENT_COLOR = "#FFDF00" # Bright Gold
BG_DARK = "#0a0a0a"
CARD_BG = "rgba(28, 28, 28, 0.75)"

HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'lang' not in st.session_state: st.session_state.lang = "Arabic"
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0

# --- 4. الوظائف ---
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "MA3LOMATI: الرائد في العقارات."
    except: return "MA3LOMATI PRO 2026"

news_text = get_real_news()

# --- 5. التصميم الجمالي المطور (Lux UI) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;700;900&display=swap');
    
    /* إخفاء العناصر الافتراضية */
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stSidebar"] {{ background-color: {BG_DARK}; }}
    
    .block-container {{ padding: 0rem !important; }}
    
    /* الخلفية العامة */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover; background-position: center;
        direction: {"rtl" if st.session_state.lang == "Arabic" else "ltr"} !important;
        font-family: 'Cairo', sans-serif;
    }}

    /* كارت الدخول الزجاجي */
    .auth-top-zone {{ display: flex; justify-content: center; align-items: center; min-height: 80vh; }}
    .mobile-card {{
        background: {CARD_BG}; border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 30px;
        padding: 40px 30px; width: 90%; max-width: 420px;
        backdrop-filter: blur(15px); box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }}

    /* الهيدر الملكي */
    .royal-header {{
        background: rgba(0,0,0,0.6); backdrop-filter: blur(10px);
        border-bottom: 1px solid {MAIN_COLOR}; padding: 30px 10px;
        text-align: center; margin-bottom: 25px;
    }}
    .royal-header h1 {{ 
        font-weight: 900 !important; letter-spacing: 2px;
        background: linear-gradient(to bottom, #FFFFFF 0%, {MAIN_COLOR} 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}

    /* الحقول بتصميم مودرن */
    div.stTextInput input, div.stNumberInput input {{
        background-color: rgba(255,255,255,0.05) !important; color: white !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important; border-radius: 15px !important;
        padding: 12px !important; transition: 0.4s;
    }}
    div.stTextInput input:focus {{ border-color: {MAIN_COLOR} !important; box-shadow: 0 0 10px rgba(212, 175, 55, 0.2); }}

    /* أزرار مذهبة */
    .stButton > button {{
        background: linear-gradient(135deg, {MAIN_COLOR}, #8C6A1A) !important;
        color: white !important; border-radius: 15px !important; font-weight: bold !important;
        border: none !important; padding: 10px 20px !important; transition: 0.3s;
    }}
    .stButton > button:hover {{ transform: translateY(-3px); box-shadow: 0 10px 20px rgba(212, 175, 55, 0.3); }}

    /* كروت المشاريع */
    div.stButton > button[key*="card_"] {{
        background: rgba(255, 255, 255, 0.03) !important; border: 1px solid rgba(255,255,255,0.1) !important;
        border-left: 5px solid {MAIN_COLOR} !important; color: #fff !important;
        border-radius: 15px !important; text-align: right !important; padding: 20px !important;
    }}
    div.stButton > button[key*="card_"]:hover {{ background: rgba(212, 175, 55, 0.1) !important; border-color: {MAIN_COLOR} !important; }}

    /* شريط الأخبار الرفيع */
    .ticker-wrap {{ background: rgba(212, 175, 55, 0.1); border-bottom: 1px solid rgba(212, 175, 55, 0.2); padding: 5px; }}
    .ticker {{ color: #EEE; font-size: 13px; }}
    
    /* بطاقة التفاصيل */
    .detail-card {{
        background: {CARD_BG}; border-radius: 25px; padding: 30px;
        border: 1px solid rgba(212, 175, 55, 0.2); margin: 10px;
    }}
    .label-gold {{ color: {MAIN_COLOR}; font-weight: bold; font-size: 12px; opacity: 0.8; }}
    .val-white {{ color: white; font-size: 18px; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.05); }}
    </style>
""", unsafe_allow_html=True)

# --- 6. واجهة تسجيل الدخول ---
if not st.session_state.auth:
    st.markdown('<div class="auth-top-zone">', unsafe_allow_html=True)
    with st.container():
        st.markdown(f'<div class="mobile-card">', unsafe_allow_html=True)
        st.markdown(f'<h1 style="color:{MAIN_COLOR}; font-size:35px; margin-bottom:5px;">M</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:white; letter-spacing:3px; font-size:12px; margin-bottom:30px;">MA3LOMATI PRO</p>', unsafe_allow_html=True)
        
        tab_log, tab_reg = st.tabs(["دخول", "اشتراك جديد"])
        with tab_log:
            u = st.text_input("Username", placeholder="الاسم أو الإيميل", label_visibility="collapsed")
            p = st.text_input("Password", type="password", placeholder="كلمة السر", label_visibility="collapsed")
            if st.button("LOG IN"):
                if p == "2026" or p == "123": 
                    st.session_state.auth = True; st.session_state.current_user = "Luxury User"; st.rerun()
                else: st.error("خطأ في البيانات")
        
        with tab_reg:
            st.text_input("Full Name", placeholder="الاسم الكامل")
            st.text_input("WhatsApp", placeholder="رقم الواتساب")
            if st.button("REGISTER NOW"): st.success("جاري المراجعة...")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- 7. جلب البيانات (محاكاة أو فعلية) ---
@st.cache_data(ttl=60)
def load_data():
    # روابط الداتا الخاصة بك
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        p = pd.read_csv(U_P).fillna("---")
        p.columns = [c.strip() for c in p.columns]
        return p
    except: return pd.DataFrame({"Project": ["Test 1", "Test 2"], "Location": ["Cairo", "Giza"]})

df_p = load_data()

# --- 8. الهيكل الداخلي ---
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:{MAIN_COLOR}; font-size:14px;">The Prestige Real Estate Guide</p></div>', unsafe_allow_html=True)

# شريط الأخبار
st.markdown(f'<div class="ticker-wrap"><marquee class="ticker">{news_text}</marquee></div>', unsafe_allow_html=True)

# أزرار خروج وتغيير لغة في الأعلى
col_top1, col_top2 = st.columns([0.85, 0.15])
with col_top2:
    if st.button("🚪 Logout"): st.session_state.auth = False; st.rerun()

# --- 9. القائمة الرئيسية المودرن ---
menu = option_menu(None, ["أدوات", "المطورين", "المشاريع", "المساعد", "Launches"], 
    icons=["sliders", "building", "house-gold", "robot", "megaphone"], 
    default_index=2, orientation="horizontal", 
    styles={
        "container": {"background-color": "transparent", "padding": "0!important"},
        "nav-link": {"font-size": "12px", "color": "white", "text-transform": "uppercase"},
        "nav-link-selected": {"background-color": MAIN_COLOR, "color": "black", "font-weight": "bold"}
    })

# --- 10. محتوى الصفحات ---
if menu == "أدوات":
    st.markdown(f"<h3 style='text-align:center; color:{MAIN_COLOR};'>Calculator</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        with st.container():
            st.markdown('<div class="detail-card">', unsafe_allow_html=True)
            v = st.number_input("سعر العقار", 5000000)
            y = st.slider("سنوات التقسيط", 1, 15, 8)
            st.metric("القسط الشهري", f"{v/(y*12):,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)

elif menu == "المشاريع":
    if st.session_state.view == "details":
        item = df_p.iloc[st.session_state.current_index]
        if st.button("⬅ العودة للقائمة"): st.session_state.view = "grid"; st.rerun()
        
        st.markdown('<div class="detail-card">', unsafe_allow_html=True)
        for k, v in item.items():
            st.markdown(f'<p class="label-gold">{k}</p><p class="val-white">{v}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        search = st.text_input("🔍 ابحث عن الفخامة...", placeholder="ابحث بالمنطقة أو اسم المطور")
        filt = df_p[df_p.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else df_p
        
        # عرض الكروت
        disp = filt.iloc[st.session_state.page_num*ITEMS_PER_PAGE : (st.session_state.page_num+1)*ITEMS_PER_PAGE]
        for idx, r in disp.iterrows():
            if st.button(f"🏢 {r.iloc[0]} \n 📍 {r.get('Location', '---')}", key=f"card_{idx}", use_container_width=True):
                st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()

st.markdown(f"<p style='text-align:center; color:#444; font-size:11px; margin-top:50px;'>EST. 2026 | ROYAL MA3LOMATI INTERFACE</p>", unsafe_allow_html=True)

