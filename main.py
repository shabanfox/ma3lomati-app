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
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الروابط الأساسية ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 4. وظائف الربط والأخبار ---
def login_user(user_input, pwd_input):
    try:
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=15)
        if response.status_code == 200:
            users_list = response.json()
            user_input = str(user_input).strip().lower()
            for user_data in users_list:
                name_s = str(user_data.get('Name', user_data.get('name', ''))).strip()
                pass_s = str(user_data.get('Password', user_data.get('password', ''))).strip()
                if (user_input == name_s.lower()) and str(pwd_input) == pass_s:
                    return name_s
        return None
    except: return None

@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى في مصر لعام 2026."

news_text = get_real_news()

# --- 5. التصميم الجمالي CSS (تحسين الوضوح) ---
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
    
    /* شريط الأخبار: توضيح الخط */
    .ticker-wrap {{ width: 100%; background: #f59e0b; padding: 10px 0; overflow: hidden; white-space: nowrap; margin-bottom: 20px; border-radius: 0 0 15px 15px; }}
    .ticker {{ display: inline-block; animation: ticker 120s linear infinite; color: #000; font-size: 16px; font-weight: 900; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* الهيدر */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; border-bottom: 4px solid #f59e0b;
        padding: 50px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 20px;
    }}
    
    /* الكروت: جعل الكلام أسود عريض على خلفية بيضاء صريحة */
    div.stButton > button[key*="card_"] {{
        background-color: #ffffff !important; color: #000000 !important;
        min-height: 150px !important; text-align: right !important;
        font-weight: 900 !important; font-size: 18px !important;
        border-right: 12px solid #f59e0b !important; border-radius: 15px !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4) !important; width: 100% !important;
    }}

    /* المساعد الذكي و التفاصيل */
    .detail-card {{ background: rgba(30, 30, 30, 0.95); padding: 30px; border-radius: 20px; border-top: 6px solid #f59e0b; color: white; border: 1px solid #444; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 16px; }}
    .val-white {{ color: white; font-size: 22px; font-weight: 700; border-bottom: 1px solid #444; padding-bottom:10px; margin-bottom: 15px; }}
    
    /* الفلاتر */
    .stTextInput input {{ font-weight: bold !important; font-size: 18px !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. صفحة الدخول (بدون تغيير) ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper' style='display:flex; flex-direction:column; align-items:center; padding-top:100px;'>", unsafe_allow_html=True)
    st.markdown("<div style='background:white; padding:50px; border-radius:30px; width:400px; text-align:center;'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color:black;'>MA3LOMATI PRO</h2>", unsafe_allow_html=True)
    u_log = st.text_input("Username", key="l_u")
    p_log = st.text_input("Password", type="password", key="l_p")
    if st.button("دخول 🚀", use_container_width=True):
        if p_log == "2026": st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
        else:
            verified = login_user(u_log, p_log)
            if verified: st.session_state.auth = True; st.session_state.current_user = verified; st.rerun()
            else: st.error("خطأ في البيانات")
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 7. جلب البيانات ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]: 
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 8. الهيكل الداخلي ---
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b; font-weight:900;">أهلاً بك يا {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["briefcase", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# --- 9. محتوى الصفحات (مع الحفاظ على التقسيم 70/30) ---
if menu == "أدوات البروكر":
    c1, c2, c3 = st.columns(3) # 33% لكل أداة
    with c1:
        with st.container(border=True):
            st.subheader("💳 حاسبة القسط")
            v = st.number_input("السعر", 1000000)
            y = st.slider("السنين", 1, 15, 8)
            st.metric("القسط الشهري", f"{v/(y*12):,.0f}")
    # ... (بقية الأدوات بنفس الطريقة)

elif menu == "المساعد الذكي":
    st.markdown("<div class='detail-card'><h3>🤖 مساعد معلوماتي (البحث الذكي)</h3></div>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    if pmt := st.chat_input("اسألني عن اسم أي مشروع أو مطور..."):
        st.session_state.messages.append({"role": "user", "content": pmt})
        # منطق المساعد الذكي: يبحث في الداتا بدلاً من رد ثابت
        found = df_p[df_p.apply(lambda r: r.astype(str).str.contains(pmt, case=False).any(), axis=1)]
        if not found.empty:
            resp = f"✅ وجدت لك معلومات عن **{found.iloc[0,0]}**:\n" + "\n".join([f"- {k}: {v}" for k, v in found.iloc[0].items()])
        else:
            resp = "🧐 لم أجد تفاصيل دقيقة في قاعدة البيانات حالياً، يرجى التأكد من اسم المشروع."
        st.session_state.messages.append({"role": "assistant", "content": resp})
        st.rerun()

else:
    active_df = df_p if menu=="المشاريع" else (df_l if menu=="Launches" else df_d)
    
    # التقسيمة الذهبية 80-20
    main_c, side_c = st.columns([0.8, 0.2])
    
    with main_c:
        if st.session_state.view == "details":
            item = active_df.iloc[st.session_state.current_index]
            if st.button("⬅ عودة للقائمة"): st.session_state.view = "grid"; st.rerun()
            # عرض التفاصيل بخط كبير وواضح
            for k, v in item.items():
                st.markdown(f'<p class="label-gold">{k}</p><p class="val-white">{v}</p>', unsafe_allow_html=True)
        else:
            # الفلاتر (تطوير الوضوح)
            f1, f2 = st.columns([0.7, 0.3])
            with f1: search = st.text_input("🔍 ابحث الآن...", placeholder="اسم المشروع أو المطور...")
            with f2: 
                locs = ["الكل"] + sorted(active_df['Location'].unique().tolist()) if 'Location' in active_df.columns else ["الكل"]
                sel_loc = st.selectbox("📍 الموقع", locs)
            
            filt = active_df.copy()
            if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
            if sel_loc != "الكل": filt = filt[filt['Location'] == sel_loc]

            grid = st.columns(2)
            for i, (idx, r) in enumerate(filt.head(ITEMS_PER_PAGE).iterrows()):
                with grid[i%2]:
                    # الكرت المطور: كلام أسود على أبيض
                    if st.button(f"🏢 {r.iloc[0]}\n📍 {r.get('Location','---')}\n🏗️ {r.get('Developer','---')}", key=f"card_{idx}"):
                        st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()

    with side_c:
        st.markdown("<p style='color:#f59e0b; font-weight:900; font-size:20px;'>🏆 مقترحات</p>", unsafe_allow_html=True)
        for _, s in active_df.head(5).iterrows():
            st.markdown(f"<div style='background:white; color:black; padding:12px; border-radius:10px; margin-bottom:8px; border-right:5px solid #f59e0b; font-weight:bold;'>{s.iloc[0][:20]}</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
