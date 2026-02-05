import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- إدارة الحالة (Session State) ---
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
                pass_s = str(user_data.get('Password', user_data.get('password', ''))).strip()
                if (user_input == name_s.lower()) and pwd_input == pass_s:
                    return name_s
        return None
    except: return None

def logout():
    st.session_state.auth = False
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
    .auth-card {{ background-color: #ffffff; width: 380px; padding: 50px; border-radius: 30px; text-align: center; margin: auto; margin-top: 50px; }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 3px solid #f59e0b;
        padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 10px;
    }}
    div.stButton > button[key*="card_"] {{
        background: #fff !important; color: #1a1a1a !important; border-right: 6px solid #f59e0b !important;
        border-radius: 15px !important; padding: 20px !important; text-align: right !important;
        min-height: 180px !important; width: 100% !important; box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        white-space: pre-line !important; margin-bottom: 10px !important; font-family: 'Cairo', sans-serif !important;
    }}
    .detail-card {{ background: rgba(20, 20, 20, 0.9); padding: 25px; border-radius: 20px; border-top: 5px solid #f59e0b; color: white; border: 1px solid #333; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. منطق الدخول ---
if not st.session_state.auth:
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.title("MA3LOMATI PRO")
    u = st.text_input("Username", key="u_login")
    p = st.text_input("Password", type="password", key="p_login")
    if st.button("دخول 🚀", use_container_width=True):
        if p == "2026": st.session_state.auth, st.session_state.current_user = True, "Admin"; st.rerun()
        else:
            user = login_user(u, p)
            if user: st.session_state.auth, st.session_state.current_user = True, user; st.rerun()
            else: st.error("خطأ في البيانات")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. جلب وتنظيف البيانات (لتجنب KeyError) ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    try:
        p, d = pd.read_csv(U_P), pd.read_csv(U_D)
        for df in [p, d]:
            df.columns = [c.strip() for c in df.columns] # تنظيف أسماء الأعمدة من المسافات
            df.rename(columns={
                'Project Name': 'ProjectName',
                'Start Price': 'Price',
                'Payment Plan': 'Payment',
                'Area': 'Location',
                'Detailed Info & Specifics': 'Details'
            }, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# --- 7. الهيدر والمنيو ---
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p>مرحباً {st.session_state.current_user}</p></div>', unsafe_allow_html=True)
_, c_ex = st.columns([0.88, 0.12])
with c_ex:
    if st.button("🚪 خروج", key="logout_btn"): logout()

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["briefcase", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

# --- 8. المساعد الذكي المطور (بدون أخطاء) ---
if menu == "المساعد الذكي":
    st.markdown("<h3 style='color:#f59e0b; text-align:center;'>🤖 مركز الاستشارات الذكي</h3>", unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["💬 شات خبير", "🔍 فلاتر ذكية", "📊 مقارنة سريعة"])

    with t1:
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.write(m["content"])
        if pmt := st.chat_input("اسألني عن أي مشروع..."):
            st.session_state.messages.append({"role": "user", "content": pmt})
            with st.chat_message("user"): st.write(pmt)
            with st.chat_message("assistant"):
                res = df_p[df_p.apply(lambda r: r.astype(str).str.contains(pmt.lower(), case=False).any(), axis=1)]
                if not res.empty:
                    r = res.iloc[0]
                    ans = f"✅ **تفاصيل {r.get('ProjectName', 'المشروع')}:**\n\n🏗️ المطور: {r.get('Developer')}\n💰 السعر: {r.get('Price')}\n💳 السداد: {r.get('Payment')}\n📍 الموقع: {r.get('Location')}\n📝 الملاحظات: {r.get('Details')}"
                else: ans = "لم أجد نتائج مطابقة، حاول كتابة اسم المشروع أو المطور."
                st.write(ans); st.session_state.messages.append({"role": "assistant", "content": ans})

    with t2:
        c1, c2 = st.columns(2)
        with c1: 
            loc_list = df_p['Location'].unique() if 'Location' in df_p.columns else []
            sel_loc = st.multiselect("اختر المناطق", loc_list)
        with c2: 
            dev_list = df_p['Developer'].unique() if 'Developer' in df_p.columns else []
            sel_dev = st.multiselect("اختر المطورين", dev_list)
        
        f_df = df_p
        if sel_loc: f_df = f_df[f_df['Location'].isin(sel_loc)]
        if sel_dev: f_df = f_df[f_df['Developer'].isin(sel_dev)]
        
        show_cols = [c for c in ['ProjectName', 'Developer', 'Location', 'Price', 'Payment'] if c in f_df.columns]
        st.dataframe(f_df[show_cols], use_container_width=True)

    with t3:
        if not df_p.empty and 'ProjectName' in df_p.columns:
            cc1, cc2 = st.columns(2)
            p1 = cc1.selectbox("اختر المشروع الأول", df_p['ProjectName'].unique(), key="comp1")
            p2 = cc2.selectbox("اختر المشروع الثاني", df_p['ProjectName'].unique(), key="comp2")
            if st.button("بدء المقارنة 📊"):
                row1, row2 = df_p[df_p['ProjectName']==p1].iloc[0], df_p[df_p['ProjectName']==p2].iloc[0]
                st.table(pd.DataFrame({
                    "الميزة": ["المطور", "الموقع", "السعر", "نظام السداد"],
                    p1: [row1.get('Developer'), row1.get('Location'), row1.get('Price'), row1.get('Payment')],
                    p2: [row2.get('Developer'), row2.get('Location'), row2.get('Price'), row2.get('Payment')]
                }))

# --- 9. المشاريع والمطورين ---
elif menu in ["المشاريع", "المطورين"]:
    active_df = df_p if menu == "المشاريع" else df_d
    if st.session_state.view == "grid":
        search = st.text_input("🔍 بحث سريع في البيانات...")
        filt = active_df[active_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else active_df
        grid = st.columns(2)
        for i, (idx, r) in enumerate(filt.head(10).iterrows()):
            with grid[i%2]:
                card_txt = f"🏠 {r.iloc[0]}\n🏗️ {r.get('Developer','---')}\n💰 {r.get('Price','-')}"
                if st.button(card_txt, key=f"card_{idx}"):
                    st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()
    else:
        if st.button("⬅ عودة"): st.session_state.view = "grid"; st.rerun()
        item = active_df.iloc[st.session_state.current_index]
        st.markdown('<div class="detail-card">', unsafe_allow_html=True)
        for k, v in item.items():
            st.markdown(f"<p><span class='label-gold'>{k}:</span> {v}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "أدوات البروكر":
    st.subheader("🛠️ الحاسبة العقارية")
    v = st.number_input("إجمالي سعر الوحدة", value=1000000)
    dp = st.slider("المقدم (%)", 0, 100, 10)
    y = st.number_input("عدد سنوات التقسيط", 1, 20, 8)
    st.metric("القسط الشهري المتوقع", f"{(v-(v*dp/100))/(y*12):,.0f}")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026 | Powered by AI</p>", unsafe_allow_html=True)
