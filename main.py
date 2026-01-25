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

# --- 2. الروابط واللون الأساسي ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# اللون الرئيسي الجديد (لبني سماوي متوهج)
MAIN_COLOR = "#00fbff" 
SECONDARY_COLOR = "#0088ff"

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'lang' not in st.session_state: st.session_state.lang = "Arabic"
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 4. الوظائف ---
def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload, timeout=10)
        return response.text == "Success"
    except: return False

def login_user(user_input, pwd_input):
    try:
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=15)
        if response.status_code == 200:
            users_list = response.json()
            user_input = str(user_input).strip().lower()
            pwd_input = str(pwd_input).strip()
            for user_data in users_list:
                name_s = str(user_data.get('Name', user_data.get('name', ''))).strip()
                email_s = str(user_data.get('Email', user_data.get('email', ''))).strip()
                pass_s = str(user_data.get('Password', user_data.get('password', ''))).strip()
                if (user_input == name_s.lower() or user_input == email_s.lower()) and pwd_input == pass_s:
                    return name_s
        return None
    except: return None

@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة."
    except: return "MA3LOMATI PRO 2026"

news_text = get_real_news()

# --- 5. التصميم الجمالي CSS المطور ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    {f'''
    html, body, [data-testid="stAppViewContainer"] {{
        overflow: hidden !important;
        height: 100vh !important;
    }}
    ''' if not st.session_state.auth else ""}

    .block-container {{ padding: 0rem !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background-color: #050505;
        background-image: radial-gradient(circle at center, rgba(0, 251, 255, 0.05) 0%, rgba(0,0,0,0.95) 100%), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {"rtl" if st.session_state.lang == "Arabic" else "ltr"} !important;
        font-family: 'Cairo', sans-serif;
    }}

    /* كارت تسجيل الدخول */
    .auth-top-zone {{ display: flex; flex-direction: column; align-items: center; padding-top: 40px; width: 100%; }}
    .mobile-card {{
        background: rgba(10, 10, 10, 0.9); border: 1px solid {MAIN_COLOR}; border-radius: 25px;
        padding: 30px; width: 90%; max-width: 400px;
        text-align: center; box-shadow: 0 10px 40px rgba(0, 251, 255, 0.2);
        backdrop-filter: blur(10px);
    }}

    /* الحقول والأزرار */
    div.stTextInput input, div.stNumberInput input {{
        background-color: rgba(255,255,255,0.05) !important; color: white !important;
        border: 1px solid {MAIN_COLOR} !important; border-radius: 12px !important;
        height: 45px !important; text-align: center !important;
    }}
    .stButton > button {{
        background: linear-gradient(90deg, {SECONDARY_COLOR}, {MAIN_COLOR}) !important; 
        color: #000 !important; font-weight: 800 !important;
        border-radius: 12px !important; width: 100% !important; border: none !important;
        transition: 0.3s all;
    }}
    .stButton > button:hover {{ transform: scale(1.02); box-shadow: 0 0 15px {MAIN_COLOR}; }}

    /* الهيدر الداخلي */
    .royal-header {{
        background: linear-gradient(180deg, rgba(0,0,0,0.8) 0%, rgba(0,21,25,0.9) 100%);
        border-bottom: 2px solid {MAIN_COLOR};
        padding: 25px 10px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 20px;
    }}
    .royal-header h1 {{ 
        font-size: 32px !important; font-weight: 900 !important;
        background: linear-gradient(to right, #ffffff, {MAIN_COLOR});
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }}

    /* شريط الأخبار */
    .ticker-wrap {{ background: rgba(0,251,255,0.08); padding: 8px 0; border-y: 1px solid rgba(0,251,255,0.2); }}
    .ticker {{ color: {MAIN_COLOR}; font-weight: bold; font-size: 13px; }}
    
    /* كروت البيانات */
    .detail-card {{ 
        background: rgba(20, 20, 20, 0.8); padding: 25px; border-radius: 20px; 
        border: 1px solid rgba(0, 251, 255, 0.3); margin-bottom: 20px;
    }}
    .label-gold {{ color: {MAIN_COLOR}; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; }}
    .val-white {{ color: #e0e0e0; font-size: 18px; font-weight: 600; margin-bottom: 15px; border-bottom: 1px solid #333; }}
    
    /* أزرار القائمة (الكروت المربعة) */
    div.stButton > button[key*="card_"] {{
        background: rgba(255,255,255,0.03) !important; color: white !important;
        border: 1px solid #333 !important; border-right: 4px solid {MAIN_COLOR} !important;
        min-height: 100px !important; border-radius: 12px !important;
        transition: 0.3s;
    }}
    div.stButton > button[key*="card_"]:hover {{
        background: rgba(0, 251, 255, 0.1) !important;
        border-color: {MAIN_COLOR} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 6. واجهة تسجيل الدخول ---
if not st.session_state.auth:
    col_l1, col_l2, col_l3 = st.columns([0.1, 0.75, 0.15])
    with col_l3:
        lang_choice = st.selectbox("🌐", ["العربية", "English"], label_visibility="collapsed")
        st.session_state.lang = "Arabic" if lang_choice == "العربية" else "English"

    st.markdown('<div class="auth-top-zone">', unsafe_allow_html=True)
    with st.container():
        st.markdown(f'<div class="mobile-card"><h2 style="color:{MAIN_COLOR}; margin-bottom:20px;">MA3LOMATI</h2>', unsafe_allow_html=True)
        tab_log, tab_reg = st.tabs(["🔐 دخول", "📝 اشتراك"])
        
        with tab_log:
            u = st.text_input("User", key="u_field", placeholder="الأسم أو الإيميل", label_visibility="collapsed")
            p = st.text_input("Pass", type="password", key="p_field", placeholder="كلمة السر", label_visibility="collapsed")
            if st.button("SIGN IN"):
                if p == "2026": 
                    st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
                else:
                    v = login_user(u, p)
                    if v: st.session_state.auth = True; st.session_state.current_user = v; st.rerun()
                    else: st.error("بيانات غير صحيحة")
        
        with tab_reg:
            r_n = st.text_input("الأسم", placeholder="الاسم الكامل")
            r_p = st.text_input("السر", type="password", placeholder="كلمة السر")
            r_e = st.text_input("البريد", placeholder="الجيميل")
            r_w = st.text_input("واتساب", placeholder="الرقم")
            r_c = st.text_input("الشركة", placeholder="اسم الشركة")
            if st.button("إنشاء حساب"):
                if signup_user(r_n, r_p, r_e, r_w, r_c): st.success("تم بنجاح! يمكنك الدخول الآن")
                else: st.error("فشل في الاشتراك")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
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
            df.columns = [c.strip() for c in df.columns]; df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 8. الهيدر الداخلي ---
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:{MAIN_COLOR}">مرحباً بك، {st.session_state.current_user}</p></div>', unsafe_allow_html=True)
c_t1, c_t2 = st.columns([0.88, 0.12])
with c_t1: st.markdown(f'<div class="ticker-wrap"><div class="ticker">🚀 أخبار العقارات: {news_text}</div></div>', unsafe_allow_html=True)
with c_t2: 
    if st.button("Logout", use_container_width=True): st.session_state.auth = False; st.rerun()

# --- 9. القائمة الرئيسية ---
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["tools", "building", "house", "robot", "stars"], 
    default_index=2, orientation="horizontal", 
    styles={
        "container": {"background-color": "rgba(0,0,0,0.5)", "padding": "0!important"},
        "nav-link": {"font-size": "13px", "text-align": "center", "margin":"0px", "color": "white"},
        "nav-link-selected": {"background-color": MAIN_COLOR, "color": "black", "font-weight": "bold"}
    })

if 'last_menu' not in st.session_state or menu != st.session_state.last_menu: 
    st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu

# --- 10. محتوى الصفحات ---
if menu == "أدوات البروكر":
    st.markdown(f"<h3 style='text-align:center; color:{MAIN_COLOR};'>📊 أدوات الحساب العقاري</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        with st.container():
            st.markdown('<div class="detail-card">', unsafe_allow_html=True)
            st.subheader("💳 حساب القسط")
            v = st.number_input("إجمالي السعر", 1000000, step=50000)
            y = st.slider("مدة التقسيط (سنوات)", 1, 15, 8)
            st.metric("القسط الشهري المتوقع", f"{v/(y*12):,.0f} ج.م")
            st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        with st.container():
            st.markdown('<div class="detail-card">', unsafe_allow_html=True)
            st.subheader("📈 العائد الاستثماري (ROI)")
            buy = st.number_input("سعر الشراء", 1000000, step=50000)
            rent = st.number_input("الإيجار السنوي المتوقع", 100000, step=5000)
            st.metric("نسبة العائد السنوي", f"{(rent/buy)*100:,.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)

elif menu == "المساعد الذكي":
    st.markdown(f"<div class='detail-card'><h3 style='color:{MAIN_COLOR}'>🤖 مساعدك الذكي</h3><p>اطرح أي سؤال حول المشاريع أو الأسعار...</p></div>", unsafe_allow_html=True)
    if pmt := st.chat_input("كيف يمكنني مساعدتك اليوم؟"): 
        st.session_state.messages.append({"role": "user", "content": pmt})
        st.info("خدمة المساعد الذكي قيد التحديث للربط مع قاعدة البيانات...")

else:
    active_df = df_p if menu=="المشاريع" else (df_l if menu=="Launches" else df_d)
    if active_df.empty: st.warning("جاري تحميل البيانات...")
    else:
        col_main = active_df.columns[0]
        if st.session_state.view == "details":
            item = active_df.iloc[st.session_state.current_index]
            if st.button(f"⬅ العودة لـ {menu}", use_container_width=True): 
                st.session_state.view = "grid"; st.rerun()
            
            h = '<div class="detail-card">'
            for k, v in item.items(): 
                h += f'<p class="label-gold">{k}</p><p class="val-white">{v}</p>'
            st.markdown(h+'</div>', unsafe_allow_html=True)
        else:
            search = st.text_input("🔍 ابحث عن مشروع، منطقة، أو مطور...", placeholder="اكتب هنا للبحث...")
            filt = active_df[active_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else active_df
            
            disp = filt.iloc[st.session_state.page_num*ITEMS_PER_PAGE : (st.session_state.page_num+1)*ITEMS_PER_PAGE]
            
            for idx, r in disp.iterrows():
                loc_info = r.get('Location', r.get('الموقع', '---'))
                if st.button(f"🏢 {r[col_main]}  |  📍 {loc_info}", key=f"card_{idx}", use_container_width=True): 
                    st.session_state.current_index, st.session_state.view = idx, "details"
                    st.rerun()
            
            # التنقل بين الصفحات
            st.write("---")
            p1, _, p2 = st.columns([1, 2, 1])
            if st.session_state.page_num > 0: 
                if p1.button("السابق ⬅"): st.session_state.page_num -= 1; st.rerun()
            if (st.session_state.page_num+1)*ITEMS_PER_PAGE < len(filt):
                if p2.button("التالي ➡"): st.session_state.page_num += 1; st.rerun()

st.markdown(f"<p style='text-align:center; color:#555; font-size:12px; margin-top:50px;'>MA3LOMATI PRO © 2026 | Powered by Cyan Logic</p>", unsafe_allow_html=True)

