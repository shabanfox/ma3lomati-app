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

# --- 2. الروابط الأساسية ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 3. وظائف النظام ---
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

# --- 4. التصميم الجمالي المطور للموبايل (Mobile First CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0.5rem !important; padding-bottom: 1rem !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}

    /* تحسين الهيدر للموبايل */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 2px solid #f59e0b;
        padding: 30px 10px; text-align: center; border-radius: 20px; margin-bottom: 10px;
    }}
    .royal-header h1 {{ font-size: 28px !important; margin: 0; color: white; }}
    
    /* تنسيق الكروت وتحسينها للموبايل */
    div.stButton > button[key*="card_"] {{
        background: #ffffff !important;
        color: #111 !important;
        border-right: 5px solid #f59e0b !important;
        border-radius: 12px !important;
        padding: 15px !important;
        text-align: right !important;
        line-height: 1.5 !important;
        min-height: 140px !important;
        width: 100% !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
        white-space: pre-line !important;
        font-size: 14px !important;
        margin-bottom: 5px !important;
    }}

    /* Media Query للشاشات الصغيرة */
    @media (max-width: 768px) {{
        [data-testid="column"] {{ width: 100% !important; flex: 1 1 100% !important; }}
        .royal-header h1 {{ font-size: 22px !important; }}
        div.stButton > button[key*="card_"] {{ min-height: 120px !important; font-size: 13px !important; }}
    }}

    /* زر الخروج العلوي */
    .exit-container {{ display: flex; justify-content: flex-end; padding: 5px; }}
    
    /* استايل المنيو للموبايل */
    .st-emotion-cache-18ni7ap {{ gap: 0.5rem !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. منطق الدخول ---
if not st.session_state.auth:
    # (نفس كود تسجيل الدخول السابق مع تحسين الموبايل)
    st.markdown("<div class='auth-wrapper' style='display:flex; flex-direction:column; align-items:center; padding-top:20px;'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header' style='background:#000; border:2px solid #f59e0b; border-radius:30px; padding:10px 30px; color:#f59e0b; margin-bottom:10px;'>MA3LOMATI PRO</div>", unsafe_allow_html=True)
    with st.container():
        col_lang, _ = st.columns([0.5, 0.5])
        with col_lang: st.button("🌐 EN/AR", key="login_lang")
        u = st.text_input("User", placeholder="الأسم")
        p = st.text_input("Pass", type="password", placeholder="كلمة السر")
        if st.button("دخول 🚀", use_container_width=True):
            if p == "2026": st.session_state.auth, st.session_state.current_user = True, "Admin"; st.rerun()
            else:
                user = login_user(u, p)
                if user: st.session_state.auth, st.session_state.current_user = True, user; st.rerun()
                else: st.error("خطأ")
    st.stop()

# --- 6. واجهة المنصة (بعد الدخول) ---

# زر الخروج في أعلى الصفحة تماماً
c_empty, c_logout = st.columns([0.8, 0.2])
with c_logout:
    if st.button("🚪 خروج", key="top_exit", use_container_width=True): logout()

# الهيدر
st.markdown(f"""
    <div class="royal-header">
        <h1>MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; margin:0;">أهلاً بك، {st.session_state.current_user}</p>
    </div>
""", unsafe_allow_html=True)

# القائمة الرئيسية
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["briefcase", "building", "search", "robot", "megaphone"], 
    default_index=2, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "transparent"},
        "nav-link": {"font-size": "12px", "text-align": "center", "margin":"2px", "color": "white"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"},
    })

if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.page_num, st.session_state.last_m = "grid", 0, menu

# جلب البيانات
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

# --- عرض المحتوى ---
if menu == "أدوات البروكر":
    # (كود الحاسبة مبسط للموبايل)
    with st.expander("💳 حاسبة الأقساط", expanded=True):
        v = st.number_input("السعر", value=1000000)
        dp = st.slider("المقدم %", 0, 100, 10)
        y = st.number_input("السنين", 1, 20, 8)
        st.success(f"القسط الشهري: {(v-(v*dp/100))/(y*12):,.0f}")

elif menu == "المساعد الذكي":
    st.chat_message("assistant").write("أنا مساعدك الذكي، اسألني عن أي تفاصيل عقارية.")
    if p := st.chat_input("سؤالك..."):
        st.chat_message("user").write(p)

else:
    active_df = df_p if menu=="المشاريع" else (df_l if menu=="Launches" else df_d)
    
    if st.session_state.view == "details":
        if st.button("⬅ عودة", use_container_width=True): st.session_state.view = "grid"; st.rerun()
        item = active_df.iloc[st.session_state.current_index]
        for col in active_df.columns:
            st.markdown(f"<p style='color:#f59e0b; margin-bottom:0;'>{col}</p><p style='color:white; border-bottom:1px solid #333; padding-bottom:5px;'>{item[col]}</p>", unsafe_allow_html=True)
    else:
        search = st.text_input("🔍 بحث...")
        filt = active_df[active_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else active_df
        start = st.session_state.page_num * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        # توزيع الأعمدة للموبايل (عمودين على اللابتوب، عمود واحد تلقائياً على الموبايل بفضل الـ CSS)
        main_c, side_c = st.columns([0.7, 0.3])
        with main_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    card_txt = f"🏠 {r.iloc[0]}\n🏗️ {r.get('Developer','-')}\n📍 {r.get('Location','-')}\n💰 {r.get('Price','-')}"
                    if st.button(card_txt, key=f"card_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()
            
            # أزرار التنقل تحت الكروت مباشرة
            st.markdown("<br>", unsafe_allow_html=True)
            n_col1, n_col2 = st.columns(2)
            with n_col1:
                if st.session_state.page_num > 0:
                    if st.button("⬅ السابق", key="nav_p", use_container_width=True):
                        st.session_state.page_num -= 1; st.rerun()
            with n_col2:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالي ➡", key="nav_n", use_container_width=True):
                        st.session_state.page_num += 1; st.rerun()
        
        with side_c:
            st.markdown("<p style='color:#f59e0b;'>🏆 مقترحات</p>", unsafe_allow_html=True)
            for s_idx, s_row in active_df.head(5).iterrows():
                if st.button(f"📌 {str(s_row.iloc[0])[:20]}", key=f"side_{s_idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = s_idx, "details"; st.rerun()

st.markdown("<p style='text-align:center; color:#444; font-size:10px; margin-top:30px;'>MA3LOMATI PRO 2026</p>", unsafe_allow_html=True)
