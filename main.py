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

# --- 2. الروابط وروابط البيانات ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
URL_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- 4. وظائف الداتا والدخول ---
@st.cache_data(ttl=60)
def load_data():
    try:
        p = pd.read_csv(URL_P).fillna("---")
        d = pd.read_csv(URL_D).fillna("---")
        l = pd.read_csv(URL_L).fillna("---")
        for df in [p, d, l]: df.columns = df.columns.str.strip()
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d, l
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def login_user(u_in, p_in):
    if p_in == "2026": return "Admin"
    try:
        r = requests.get(f"{SCRIPT_URL}?nocache={time.time()}")
        if r.status_code == 200:
            for u in r.json():
                if (u_in.lower() == str(u.get('Email','')).lower() or u_in == str(u.get('Name',''))) and str(p_in) == str(u.get('Password','')):
                    return str(u.get('Name',''))
    except: pass
    return None

# --- 5. التنسيق الجمالي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    div.stButton > button { border-radius: 12px !important; width: 100% !important; font-family: 'Cairo'; transition: 0.3s; }
    div.stButton > button[key*="card_"] { background: #161616 !important; color: white !important; min-height: 120px !important; border: 1px solid #333 !important; border-top: 4px solid #f59e0b !important; white-space: pre-line !important; }
    div.stButton > button:hover { transform: translateY(-5px); border-color: #f59e0b !important; }
    .smart-box { background: #111; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; margin-bottom: 20px; }
    .label { color: #f59e0b; font-weight: bold; font-size: 14px; margin-bottom: 2px; }
    .value { color: #fff; font-size: 18px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- 6. شاشة الدخول ---
if not st.session_state.auth:
    _, col_mid, _ = st.columns([1, 1.5, 1])
    with col_mid:
        st.markdown("<br><br><h1 style='text-align:center; color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم / البريد")
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للمنصة 🚀"):
            user = login_user(u, p)
            if user: st.session_state.auth = True; st.session_state.current_user = user; st.rerun()
            else: st.error("بيانات غير صحيحة")
    st.stop()

# --- 7. الهيدر والمنيو ---
df_p, df_d, df_l = load_data()

st.markdown(f"""<div style="background: #111; padding: 20px; border-radius: 0 0 30px 30px; text-align: center; border-bottom: 4px solid #f59e0b; margin-bottom: 10px;">
    <h1 style="color: white; margin: 0;">MA3LOMATI PRO</h1>
    <p style="color: #f59e0b;">أهلاً بك: {st.session_state.current_user} | {egypt_now.strftime('%I:%M %p')}</p>
</div>""", unsafe_allow_html=True)

if st.button("🚪 خروج", key="exit"): st.session_state.auth = False; st.rerun()

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], 
    icons=["briefcase", "building", "search", "robot", "rocket"], 
    default_index=4, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- 8. المحتوى الرئيسي ---

# 1. صفحة اللونشات
if menu == "اللونشات":
    if st.session_state.selected_item is not None:
        if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
        it = st.session_state.selected_item
        st.markdown(f"""<div class='smart-box'>
            <h1 style='color:#f59e0b;'>{it.get('Project','---')}</h1>
            <p class='label'>🏢 المطور</p><p class='value'>{it.get('Developer','---')}</p>
            <p class='label'>📍 الموقع</p><p class='value'>{it.get('Location','---')}</p>
            <p class='label'>📏 المساحات</p><p class='value'>{it.get('Units & Sizes','---')}</p>
            <p class='label'>💰 السعر والسداد</p><p class='value'>{it.get('Price & Payment','---')}</p>
            <p class='label'>🌟 USP</p><p>{it.get('Unique Selling Points (USP)','---')}</p>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align:center;'>🚀 لانشات حصرية 2026</h2>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, r in df_l.iterrows():
            with cols[i % 3]:
                if st.button(f"🏢 {r['Developer']}\n{r['Project']}\n📍 {r['Location']}", key=f"card_l_{i}"):
                    st.session_state.selected_item = r; st.rerun()

# 2. المساعد الذكي
elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'><h2>🤖 مساعد الربط الذكي</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    loc_s = c1.selectbox("المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    bud_s = c2.number_input("المقدم المتاح", 0, step=100000)
    if st.button("بحث عن أفضل ترشيح"):
        res = df_p[df_p['Location'] == loc_s] if loc_s != "الكل" else df_p
        st.write(f"تم إيجاد {len(res.head(5))} مشاريع مناسبة:")
        for _, r in res.head(5).iterrows():
            st.info(f"🏢 {r['ProjectName']} - المطور: {r['Developer']}")
    st.markdown("</div>", unsafe_allow_html=True)

# 3. المشاريع
elif menu == "المشاريع":
    search = st.text_input("🔍 ابحث عن مشروع...")
    dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
    cols = st.columns(3)
    start = st.session_state.p_idx * 9
    for i, r in dff.iloc[start:start+9].iterrows():
        with cols[i % 3]:
            if st.button(f"🏢 {r['ProjectName']}\n📍 {r['Location']}", key=f"card_p_{i}"):
                st.session_state.selected_item = r; st.rerun()
    # Pagination
    c1, c2 = st.columns(2)
    if start > 0 and c1.button("السابق"): st.session_state.p_idx -= 1; st.rerun()
    if start+9 < len(dff) and c2.button("التالي"): st.session_state.p_idx += 1; st.rerun()

# 4. المطورين
elif menu == "المطورين":
    search_d = st.text_input("🔍 ابحث عن مطور...")
    dfd = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
    for i, r in dfd.head(10).iterrows():
        with st.expander(f"🏗️ {r['Developer']}"):
            st.write(f"⭐ الفئة: {r.get('Developer Category','---')}")
            st.write(f"💼 المالك: {r.get('Owner','---')}")

# 5. أدوات البروكر
elif menu == "أدوات البروكر":
    st.title("🛠️ الحقيبة الحسابية")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='smart-box'><h3>💳 القسط</h3>", unsafe_allow_html=True)
        v = st.number_input("السعر", 1000000)
        d = st.number_input("المقدم", 100000)
        y = st.number_input("السنين", 1, 15, 8)
        st.success(f"القسط الشهري: {(v-d)/(y*12):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='smart-box'><h3>💰 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("الصفقة", 1000000)
        pct = st.slider("%", 1.0, 10.0, 2.5)
        st.success(f"الربح: {deal*(pct/100):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='smart-box'><h3>📏 المساحة</h3>", unsafe_allow_html=True)
        m2 = st.number_input("متر مربع", 100)
        st.info(f"بالقدم: {m2*10.76:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
