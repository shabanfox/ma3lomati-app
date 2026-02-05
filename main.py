import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'messages' not in st.session_state: st.session_state.messages = []
if 'search_query' not in st.session_state: st.session_state.search_query = ""

# --- 2. الروابط الأساسية ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 3. وظائف النظام الأساسية ---
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

def logout():
    st.session_state.auth = False
    st.session_state.current_user = None
    st.rerun()

# --- 4. التصميم الجمالي CSS (نسخة الكروت المطورة) ---
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
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: flex-start; width: 100%; padding-top: 50px; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 24px; font-weight: 900;
        text-align: center; z-index: 10; margin-bottom: -30px; min-width: 360px;
    }}
    .auth-card {{ background-color: #ffffff; width: 380px; padding: 55px 35px 30px 35px; border-radius: 30px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 3px solid #f59e0b;
        padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 10px;
    }}
    div.stButton > button[key*="card_"] {{
        background: linear-gradient(145deg, #ffffff, #f9f9f9) !important;
        color: #1a1a1a !important; border-right: 6px solid #f59e0b !important;
        border-radius: 15px !important; padding: 20px !important; text-align: right !important;
        line-height: 1.7 !important; min-height: 180px !important; width: 100% !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important; transition: all 0.3s ease !important;
        white-space: pre-line !important; margin-bottom: 10px !important; font-family: 'Cairo', sans-serif !important;
    }}
    div.stButton > button[key*="card_"]:hover {{
        transform: translateY(-5px) !important; box-shadow: 0 8px 20px rgba(245, 158, 11, 0.4) !important;
    }}
    .detail-card {{ background: rgba(20, 20, 20, 0.9); padding: 25px; border-radius: 20px; border-top: 5px solid #f59e0b; color: white; border: 1px solid #333; margin-bottom:20px; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 14px; margin-top: 5px; }}
    .val-white {{ color: white; font-size: 16px; border-bottom: 1px solid #333; padding-bottom:5px; margin-bottom: 8px; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. منطق الدخول ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>MA3LOMATI PRO</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    col_l, _ = st.columns([0.45, 0.55])
    with col_l: st.button("🌐 EN / AR", key="login_lang", use_container_width=True)
    tab_login, tab_signup = st.tabs(["🔐 دخول", "📝 اشتراك"])
    with tab_login:
        u = st.text_input("User", placeholder="الأسم أو الإيميل", label_visibility="collapsed", key="u")
        p = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="p")
        if st.button("SIGN IN 🚀", use_container_width=True):
            if p == "2026": st.session_state.auth, st.session_state.current_user = True, "Admin"; st.rerun()
            else:
                user = login_user(u, p)
                if user: st.session_state.auth, st.session_state.current_user = True, user; st.rerun()
                else: st.error("خطأ في البيانات")
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 6. جلب البيانات ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]: 
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName', 'Start Price': 'Price'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 7. واجهة المنصة ---
st.markdown(f'<div class="royal-header"><h1 style="color:white; margin:0; font-size:40px;">MA3LOMATI PRO</h1><p style="color:#f59e0b; font-weight:bold;">مرحباً {st.session_state.current_user}</p></div>', unsafe_allow_html=True)
_, c_ex = st.columns([0.88, 0.12])
with c_ex:
    if st.button("🚪 خروج", key="ex", use_container_width=True): logout()

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["briefcase", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.page_num, st.session_state.last_m = "grid", 0, menu

# --- 8. المساعد الذكي المطور ---
if menu == "المساعد الذكي":
    st.markdown("<h2 style='text-align:center; color:#f59e0b;'>🤖 مركز ذكاء معلوماتي برو</h2>", unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["💬 استشارة سريعة", "🔍 فلاتر متقدمة", "📊 مقارنة مشاريع"])

    with t1:
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.write(m["content"])
        if pmt := st.chat_input("اسأل عن أي مشروع أو مطور..."):
            st.session_state.messages.append({"role": "user", "content": pmt})
            with st.chat_message("user"): st.write(pmt)
            with st.chat_message("assistant"):
                res = df_p[df_p.apply(lambda r: r.astype(str).str.contains(pmt.lower(), case=False).any(), axis=1)]
                if not res.empty:
                    r = res.iloc[0]
                    ans = f"✅ **تفاصيل {r.get('ProjectName')}:**\n\n🏗️ **المطور:** {r.get('Developer')}\n📍 **الموقع:** {r.get('Location')}\n💰 **السعر:** {r.get('Price')}\n💳 **السداد:** {r.get('Payment Plan')}\n📝 **معلومات:** {r.get('Detailed Info & Specifics')}"
                else: ans = "عذراً، لم أجد تفاصيل دقيقة. حاول كتابة اسم المشروع بشكل أوضح."
                st.write(ans); st.session_state.messages.append({"role": "assistant", "content": ans})

    with t2:
        c1, c2 = st.columns(2)
        with c1: loc_f = st.multiselect("تصفية بالمنطقة", options=df_p['Location'].unique())
        with c2: dev_f = st.multiselect("تصفية بالمطور", options=df_p['Developer'].unique())
        f_res = df_p
        if loc_f: f_res = f_res[f_res['Location'].isin(loc_f)]
        if dev_f: f_res = f_res[f_res['Developer'].isin(dev_f)]
        st.dataframe(f_res[['ProjectName', 'Developer', 'Location', 'Price', 'Payment Plan']], use_container_width=True)

    with t3:
        col1, col2 = st.columns(2)
        with col1: p1 = st.selectbox("المشروع الأول", df_p['ProjectName'].unique(), key="sel1")
        with col2: p2 = st.selectbox("المشروع الثاني", df_p['ProjectName'].unique(), key="sel2")
        if st.button("تحليل المقارنة 📊"):
            d1, d2 = df_p[df_p['ProjectName']==p1].iloc[0], df_p[df_p['ProjectName']==p2].iloc[0]
            st.table(pd.DataFrame({"الميزة": ["المطور", "السعر", "السداد", "التشطيب"], p1: [d1['Developer'], d1['Price'], d1['Payment Plan'], d1['Finishing']], p2: [d2['Developer'], d2['Price'], d2['Payment Plan'], d2['Finishing']]}))

# --- 9. المشاريع والمطورين ---
elif menu in ["المشاريع", "المطورين", "Launches"]:
    active_df = df_p if menu=="المشاريع" else (df_l if menu=="Launches" else df_d)
    if st.session_state.view == "details":
        if st.button("⬅ عودة", use_container_width=True): st.session_state.view = "grid"; st.rerun()
        item = active_df.iloc[st.session_state.current_index]
        if "Developer" in item and menu != "المطورين":
            if st.button(f"🏢 عرض ملف المطور: {item['Developer']}", use_container_width=True):
                st.session_state.search_query, st.session_state.last_m, st.session_state.view = item['Developer'], "المطورين", "grid"; st.rerun()
        c1, c2, c3 = st.columns(3)
        cols = active_df.columns
        for i, cs in enumerate([cols[:len(cols)//3+1], cols[len(cols)//3+1:2*len(cols)//3+1], cols[2*len(cols)//3+1:]]):
            with [c1, c2, c3][i]:
                h = '<div class="detail-card">'
                for k in cs: h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                st.markdown(h+'</div>', unsafe_allow_html=True)
    else:
        search = st.text_input("🔍 بحث...", value=st.session_state.search_query)
        filt = active_df[active_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else active_df
        start = st.session_state.page_num * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        m_c, s_c = st.columns([0.76, 0.24])
        with m_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    txt = f"🏠 {r.iloc[0]}\n🏗️ {r.get('Developer','---')}\n📍 {r.get('Location','---')}\n💰 {r.get('Price','-')}"
                    if st.button(txt, key=f"card_{idx}"): st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()
            b1, b_inf, b2 = st.columns([1, 2, 1])
            with b1: 
                if st.session_state.page_num > 0 and st.button("⬅ السابق", key="nav_p"): st.session_state.page_num -= 1; st.rerun()
            with b2:
                if (start + ITEMS_PER_PAGE) < len(filt) and st.button("التالي ➡", key="nav_n"): st.session_state.page_num += 1; st.rerun()
        with s_c:
            st.markdown("<p style='color:#f59e0b; font-weight:bold;'>🏆 مقترحات</p>", unsafe_allow_html=True)
            for sid, srow in active_df.head(10).iterrows():
                if st.button(f"📌 {str(srow.iloc[0])[:25]}", key=f"side_{sid}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = sid, "details"; st.rerun()

elif menu == "أدوات البروكر":
    st.subheader("🛠️ حاسبة الاستثمار")
    v = st.number_input("السعر", value=1000000)
    dp = st.number_input("المقدم %", 0, 100, 10)
    y = st.number_input("السنين", 1, 20, 8)
    st.metric("القسط الشهري", f"{(v-(v*dp/100))/(y*12):,.0f}")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px; font-size:12px;'>MA3LOMATI PRO © 2026 | Smart Broker System</p>", unsafe_allow_html=True)
