import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة الفخمة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- روابط البيانات والروابط الثابتة ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 2. إدارة الحالة والتوقيت ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- 3. الوظائف البرمجية (الربط والبيانات) ---
def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload)
        return response.text == "Success"
    except: return False

def login_user(u_input, pwd_input):
    try:
        response = requests.get(f"{USER_SHEET_URL}?nocache={time.time()}")
        if response.status_code == 200:
            import io
            df = pd.read_csv(io.StringIO(response.text))
            df.columns = df.columns.str.strip()
            # التحقق من الاسم أو الإيميل
            user_row = df[((df['Name'].astype(str).str.lower() == str(u_input).lower().strip()) | 
                           (df['Email'].astype(str).str.lower() == str(u_input).lower().strip())) & 
                          (df['Password'].astype(str) == str(pwd_input).strip())]
            if not user_row.empty:
                return user_row.iloc[0]['Name']
        return None
    except: return None

@st.cache_data(ttl=60)
def load_app_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

# --- 4. التنسيق الجمالي (CSS المدمج) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}

    /* تصميم الدخول البيضاوي */
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: center; padding-top: 80px; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 26px; font-weight: 900;
        text-align: center; z-index: 10; margin-bottom: -35px; min-width: 350px;
        box-shadow: 0 10px 20px rgba(245,158,11,0.3);
    }}
    .auth-card {{ background-color: #ffffff; width: 400px; padding: 60px 30px 30px 30px; border-radius: 40px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.4); }}
    .auth-card input {{ background-color: #f1f1f1 !important; border-radius: 12px !important; text-align: center !important; font-weight: bold; }}

    /* ستايل الهيدر الداخلي */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 4px solid #f59e0b;
        padding: 40px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 20px;
    }}
    
    /* ستايلات البطاقات والأدوات */
    .smart-box {{ background: rgba(15,15,15,0.9); border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; }}
    .tool-card {{ background: rgba(30,30,30,0.8); padding: 20px; border-radius: 15px; border-top: 4px solid #f59e0b; text-align: center; margin-bottom: 10px; }}
    div.stButton > button[key*="card_"] {{
        background: #1a1a1a !important; color: white !important; height: 150px !important; width: 100% !important; border-radius: 15px !important; border-left: 5px solid #f59e0b !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. شاشة الدخول والاشتراك ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>MA3LOMATI PRO</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["🔐 دخول", "📝 اشتراك"])
    with t1:
        u = st.text_input("الأسم أو الإيميل", key="log_u", label_visibility="collapsed", placeholder="Username / Email")
        p = st.text_input("كلمة السر", type="password", key="log_p", label_visibility="collapsed", placeholder="Password")
        if st.button("تسجيل الدخول 🚀", use_container_width=True):
            if p == "2026": # الكود المباشر
                st.session_state.auth, st.session_state.current_user = True, "Admin"
                st.rerun()
            else:
                user = login_user(u, p)
                if user:
                    st.session_state.auth, st.session_state.current_user = True, user
                    st.rerun()
                else: st.error("بيانات غير صحيحة")
    
    with t2:
        reg_n = st.text_input("الاسم", key="rn")
        reg_e = st.text_input("الإيميل", key="re")
        reg_p = st.text_input("كلمة السر", type="password", key="rp")
        if st.button("إنشاء حساب ✅", use_container_width=True):
            if reg_n and reg_e and reg_p:
                if signup_user(reg_n, reg_p, reg_e, "WA", "Comp"):
                    st.success("تم بنجاح! انتقل للدخول")
                else: st.error("فشل الاتصال")
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 6. المنصة من الداخل ---
df_p, df_d = load_app_data()

st.markdown(f"""
    <div class="royal-header">
        <h1 style="color:#f59e0b; font-weight:900; margin:0;">MA3LOMATI PRO</h1>
        <p style="color:white; font-size:18px;">أهلاً بك يا {st.session_state.current_user} في دليلك العقاري لعام 2026</p>
    </div>
""", unsafe_allow_html=True)

# شريط الخروج والتوقيت
c_t1, c_t2 = st.columns([0.8, 0.2])
with c_t2:
    if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()
with c_t1:
    st.markdown(f"<p style='color:#aaa;'>📅 {egypt_now.strftime('%Y-%m-%d')} | 🕒 {egypt_now.strftime('%I:%M %p')}</p>", unsafe_allow_html=True)

menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- منطق الصفحات الداخلي ---
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"""<div class='smart-box'>
        <h2 style='color:#f59e0b;'>{item.get('ProjectName', item.get('Developer'))}</h2>
        <hr>
        <div style='display:grid; grid-template-columns: 1fr 1fr; gap:20px;'>
            <div>
                <p>📍 الموقع: {item.get('Location', '---')}</p>
                <p>🏗️ المطور: {item.get('Developer', '---')}</p>
            </div>
            <div>
                <p>💰 السعر: {item.get('Starting Price (EGP)', 'تواصل للاستفسار')}</p>
                <p>📅 الاستلام: {item.get('Delivery', '---')}</p>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 مساعد الربط العقاري")
    c1, c2 = st.columns(2)
    loc = c1.selectbox("المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    budget = c2.number_input("الميزانية التقريبية", 0)
    if st.button("بحث ذكي"):
        st.write("جاري تحليل البيانات لتقديم أفضل الترشيحات...")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    search = st.text_input("🔍 ابحث عن مشروع...")
    dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
    
    start = st.session_state.p_idx * 6
    page = dff.iloc[start:start+6]
    
    cols = st.columns(2)
    for i, (idx, row) in enumerate(page.iterrows()):
        with cols[i % 2]:
            if st.button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}\n🏗️ {row['Developer']}", key=f"card_p_{idx}"):
                st.session_state.selected_item = row; st.rerun()
    
    st.write("---")
    p1, _, p2 = st.columns([1,2,1])
    if st.session_state.p_idx > 0 and p1.button("السابق"): st.session_state.p_idx -= 1; st.rerun()
    if start + 6 < len(dff) and p2.button("التالي"): st.session_state.p_idx += 1; st.rerun()

elif menu == "أدوات البروكر":
    st.title("🛠️ الأدوات الحسابية")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='tool-card'><h3>💳 القسط</h3>", unsafe_allow_html=True)
        v = st.number_input("السعر", 1000000)
        y = st.slider("السنين", 1, 10, 8)
        st.metric("الشهري", f"{v/(y*12):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='tool-card'><h3>💰 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("الصفقة", 1000000)
        st.metric("العمولة (2.5%)", f"{deal*0.025:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='tool-card'><h3>📈 ROI</h3>", unsafe_allow_html=True)
        rent = st.number_input("الإيجار السنوي", 100000)
        price = st.number_input("سعر الشراء", 1000000)
        st.metric("العائد", f"{(rent/price)*100:.1f}%")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
