import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. روابط البيانات
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# 3. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- الوظائف ---
def login_user(user_input, pwd_input):
    try:
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}")
        if response.status_code == 200:
            for u in response.json():
                n = str(u.get('Name',''))
                p = str(u.get('Password',''))
                e = str(u.get('Email',''))
                if (user_input.strip().lower() in [n.lower(), e.lower()]) and str(pwd_input) == p:
                    return n
        return None
    except: return None

@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        p.rename(columns={'Area':'Location','الموقع':'Location','Project Name':'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

# 4. التنسيق (Dark Mode 2026)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] { background-color: #000000; color: #FFFFFF; direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    header { visibility: hidden; }
    h1, h2, h3 { color: #f59e0b !important; }
    p, span, label { color: #FFFFFF !important; font-weight: bold; }
    div.stButton > button[key*="card_"] {
        background-color: #FFFFFF !important; color: #000000 !important;
        min-height: 120px !important; font-weight: 900 !important; font-size: 18px !important;
        border-right: 8px solid #f59e0b !important; margin-bottom: 10px !important; width: 100%;
    }
    .smart-box { background: #111; border: 1px solid #333; padding: 20px; border-radius: 15px; border-right: 6px solid #f59e0b; }
</style>
""", unsafe_allow_html=True)

# 5. نظام الدخول
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    u_in = st.text_input("الأسم أو الجيميل")
    p_in = st.text_input("كلمة السر", type="password")
    if st.button("دخول للنظام 🚀"):
        if p_in == "2026":
            st.session_state.auth, st.session_state.current_user = True, "Admin"
            st.rerun()
        else:
            user = login_user(u_in, p_in)
            if user:
                st.session_state.auth, st.session_state.current_user = True, user
                st.rerun()
            else: st.error("خطأ في البيانات")
    st.stop()

# 6. المنيو والبيانات
df_p, df_d = load_data()
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "calculator"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# 7. العرض
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة"):
        st.session_state.selected_item = None
        st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"""<div class='smart-box'>
        <h2>{item.get('ProjectName', item.get('Developer'))}</h2>
        <p>📍 الموقع: {item.get('Location')}</p>
        <p>🏗️ المطور: {item.get('Developer')}</p>
        <p>💰 السعر: {item.get('Starting Price (EGP)')}</p>
    </div>""", unsafe_allow_html=True)

elif menu == "المساعد الذكي":
    st.title("🤖 المساعد الذكي")
    locs = ["الكل"] + sorted(df_p['Location'].unique().tolist()) if not df_p.empty else ["الكل"]
    loc = st.selectbox("📍 المنطقة", locs)
    wa = st.text_input("واتساب العميل")
    if st.button("🎯 ترشيح"):
        res = df_p[df_p['Location'] == loc] if loc != "الكل" else df_p
        for _, r in res.head(5).iterrows():
            st.write(f"🏢 **{r['ProjectName']}**")
            msg = f"أرشح لك {r['ProjectName']} في {r['Location']}."
            st.markdown(f"[📲 إرسال](https://wa.me/{wa}?text={urllib.parse.quote(msg)})")

elif menu == "المشاريع":
    search = st.text_input("🔍 ابحث عن مشروع")
    dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
    start = st.session_state.p_idx * 6
    for i, r in dff.iloc[start:start+6].iterrows():
        if st.button(f"🏢 {r['ProjectName']}\n📍 {r['Location']}", key=f"card_p_{i}"):
            st.session_state.selected_item = r
            st.rerun()
    c1, _, c2 = st.columns([1,2,1])
    if st.session_state.p_idx > 0:
        if c1.button("السابق"): st.session_state.p_idx -= 1; st.rerun()
    if start + 6 < len(dff):
        if c2.button("التالي"): st.session_state.p_idx += 1; st.rerun()

elif menu == "المطورين":
    search_d = st.text_input("🔍 ابحث عن مطور")
    # ميزة إضافية: فلتر المنطقة للمطورين
    loc_d = st.selectbox("📍 فلتر مطوري منطقة معينة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    
    # ربط المطورين بالمشاريع لإيجاد مطوري المنطقة
    if loc_d != "الكل":
        devs_in_loc = df_p[df_p['Location'] == loc_d]['Developer'].unique()
        dfd_f = df_d[df_d['Developer'].isin(devs_in_loc)]
    else:
        dfd_f = df_d
        
    if search_d:
        dfd_f = dfd_f[dfd_f['Developer'].str.contains(search_d, case=False)]
        
    for i, r in dfd_f.head(10).iterrows():
        if st.button(f"🏗️ {r['Developer']}", key=f"card_d_{i}"):
            st.session_state.selected_item = r
            st.rerun()

elif menu == "أدوات البروكر":
    st.title("🛠️ أدوات مالية")
    v = st.number_input("السعر", value=1000000)
    d = st.number_input("المقدم", value=100000)
    st.metric("القسط الشهري (8 سنين)", f"{(v-d)/(8*12):,.0f}")

st.markdown(f"<p style='text-align:center; color:#555;'>MA3LOMATI PRO © 2026 | {egypt_now.strftime('%I:%M %p')}</p>", unsafe_allow_html=True)
