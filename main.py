import streamlit as st
import pandas as pd
import requests
import feedparser
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

# --- 2. الروابط الأساسية ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 3. وظائف الدخول والاشتراك ---
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

# --- 4. التصميم الجمالي CSS ---
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
        padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 20px;
    }}
    .detail-card {{ background: rgba(20, 20, 20, 0.9); padding: 25px; border-radius: 20px; border-top: 5px solid #f59e0b; color: white; border: 1px solid #333; margin-bottom:20px; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 16px; margin-top: 10px; }}
    .val-white {{ color: white; font-size: 18px; border-bottom: 1px solid #333; padding-bottom:5px; margin-bottom: 10px; }}
    
    /* تنسيق أزرار الكروت */
    div.stButton > button[key*="card_"] {{
        background-color: white !important; color: #111 !important;
        min-height: 140px !important; text-align: right !important;
        font-weight: bold !important; font-size: 15px !important;
        border: none !important; margin-bottom: 0px !important;
        display: block !important; width: 100% !important; border-radius: 12px !important;
    }}
    /* تنسيق أزرار التنقل (التالي والسابق) */
    div.stButton > button[key*="nav_"] {{
        background-color: #f59e0b !important; color: black !important;
        font-weight: bold !important; border-radius: 10px !important;
        border: none !important; margin-top: 10px !important;
    }}
    /* تنسيق المقترحات الجانبية */
    div.stButton > button[key*="side_"] {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #eee !important; border: none !important;
        border-right: 3px solid #f59e0b !important;
        text-align: right !important; font-size: 13px !important;
        margin-bottom: 5px !important; border-radius: 8px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. صفحة الدخول ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>MA3LOMATI PRO</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    
    col_lang, _ = st.columns([0.4, 0.6])
    with col_lang: st.button("🌐 EN / AR", key="login_lang", use_container_width=True)
    
    tab_login, tab_signup = st.tabs(["🔐 تسجيل دخول", "📝 اشتراك جديد"])
    with tab_login:
        u_input = st.text_input("User", placeholder="الأسم أو الجيميل", label_visibility="collapsed", key="log_user")
        p_input = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="log_pass")
        if st.button("SIGN IN 🚀", use_container_width=True):
            if p_input == "2026": 
                st.session_state.auth, st.session_state.current_user = True, "Admin"
                st.rerun()
            else:
                user_verified = login_user(u_input, p_input)
                if user_verified:
                    st.session_state.auth, st.session_state.current_user = True, user_verified
                    st.rerun()
                else: st.error("بيانات الدخول غير صحيحة")
    
    with tab_signup:
        reg_name = st.text_input("الأسم", placeholder="الاسم بالكامل")
        reg_pass = st.text_input("كلمة السر", type="password", placeholder="كلمة السر")
        reg_email = st.text_input("الجيميل", placeholder="الإيميل")
        reg_wa = st.text_input("الواتساب", placeholder="رقم الموبايل")
        reg_co = st.text_input("الشركة", placeholder="اسم الشركة")
        if st.button("تأكيد الاشتراك ✅", use_container_width=True):
            if reg_name and reg_pass and reg_email:
                if signup_user(reg_name, reg_pass, reg_email, reg_wa, reg_co): st.success("تم بنجاح!")
                else: st.error("فشل الاتصال")
            else: st.warning("أكمل البيانات")
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
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 7. الهيدر ---
st.markdown(f'<div class="royal-header"><h1 style="color:white; margin:0; font-size:45px;">MA3LOMATI PRO</h1><p style="color:#f59e0b; font-weight:bold;">أهلاً بك يا {st.session_state.current_user}</p></div>', unsafe_allow_html=True)
_, c_exit = st.columns([0.85, 0.15])
with c_exit:
    if st.button("🚪 خروج", key="exit_btn", use_container_width=True): logout()

# --- 8. القائمة ---
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["briefcase", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if 'last_menu' not in st.session_state or menu != st.session_state.last_menu:
    st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu

# --- 9. المحتوى ---
if menu == "أدوات البروكر":
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            v = st.number_input("إجمالي السعر", value=1000000)
            dp = st.number_input("المقدم %", 0, 100, 10)
            y = st.number_input("السنين", 1, 20, 8)
            st.metric("القسط الشهري", f"{(v-(v*dp/100))/(y*12):,.0f}")
    with c2:
        with st.container(border=True):
            val = st.number_input("الصفقة", value=1000000)
            p = st.number_input("العمولة %", 0.0, 10.0, 2.5)
            st.metric("الربح", f"{val*(p/100):,.0f}")
    with c3:
        with st.container(border=True):
            b = st.number_input("الشراء", value=1000000)
            r = st.number_input("الإيجار السنوي", value=100000)
            st.metric("العائد", f"{(r/b)*100:,.1f}%" if b>0 else "0%")

elif menu == "المساعد الذكي":
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    if pmt := st.chat_input("اسألني..."):
        st.session_state.messages.append({"role": "user", "content": pmt})
        st.session_state.messages.append({"role": "assistant", "content": "جاري التحليل..."})
        st.rerun()

else:
    active_df = df_p if menu=="المشاريع" else (df_l if menu=="Launches" else df_d)
    col_main = active_df.columns[0]
    
    if st.session_state.view == "details":
        if st.button("⬅ عودة", use_container_width=True): st.session_state.view = "grid"; st.rerun()
        item = active_df.iloc[st.session_state.current_index]
        c1, c2, c3 = st.columns(3)
        cols = active_df.columns
        for i, cs in enumerate([cols[:len(cols)//3+1], cols[len(cols)//3+1:2*len(cols)//3+1], cols[2*len(cols)//3+1:]]):
            with [c1, c2, c3][i]:
                h = '<div class="detail-card">'
                for k in cs: h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                st.markdown(h+'</div>', unsafe_allow_html=True)
    else:
        search = st.text_input("🔍 بحث...")
        filt = active_df[active_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else active_df
        start = st.session_state.page_num * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        main_c, side_c = st.columns([0.75, 0.25])
        with main_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    if st.button(f"🏢 {r[col_main]}\n📍 {r.get('Location','---')}", key=f"card_{idx}"):
                        st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()
            
            # --- أزرار التنقل تحت الكروت بالظبط ---
            p_col1, p_info, p_col2 = st.columns([1, 2, 1])
            with p_col1:
                if st.session_state.page_num > 0:
                    if st.button("⬅ السابق", key="nav_prev", use_container_width=True):
                        st.session_state.page_num -= 1; st.rerun()
            with p_info:
                st.markdown(f"<p style='text-align:center; color:#888; margin-top:15px;'>{st.session_state.page_num + 1}</p>", unsafe_allow_html=True)
            with p_col2:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالي ➡", key="nav_next", use_container_width=True):
                        st.session_state.page_num += 1; st.rerun()
        
        with side_c:
            st.markdown("<p style='color:#f59e0b; font-weight:bold;'>🏆 مقترحات</p>", unsafe_allow_html=True)
            for s_idx, s_row in active_df.head(8).iterrows():
                if st.button(f"📌 {str(s_row[col_main])[:25]}", key=f"side_{s_idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = s_idx, "details"; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
