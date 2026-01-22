import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة الفخمة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. روابط البيانات ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
URL_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'last_menu' not in st.session_state: st.session_state.last_menu = "اللونشات"

# --- 4. التنسيق الجمالي الاحترافي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* خلفية هادئة وفخمة */
    [data-testid="stAppViewContainer"] {
        background-color: #0a0a0a;
        background-image: radial-gradient(circle at 50% 50%, #1a1a1a 0%, #0a0a0a 100%);
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }

    /* هيدر ملكي */
    .royal-header {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(15px);
        border-bottom: 3px solid #f59e0b;
        padding: 40px 20px;
        text-align: center;
        border-radius: 0 0 50px 50px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* كروت الأزرار */
    div.stButton > button[key*="card_"] {
        background: rgba(30, 30, 30, 0.6) !important;
        color: #e0e0e0 !important;
        border: 1px solid #333 !important;
        border-right: 5px solid #f59e0b !important;
        border-radius: 12px !important;
        min-height: 120px !important;
        transition: 0.3s;
        font-weight: bold !important;
    }
    div.stButton > button:hover {
        background: rgba(245, 158, 11, 0.1) !important;
        border-color: #f59e0b !important;
        transform: translateY(-3px);
    }

    /* تفاصيل ذكية */
    .info-card {
        background: rgba(255,255,255,0.03);
        padding: 20px; border-radius: 20px;
        border: 1px solid #222;
    }
    
    .label-gold { color: #f59e0b; font-size: 14px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 5. وظائف الداتا والربط ---
@st.cache_data(ttl=60)
def load_all_data():
    try:
        p = pd.read_csv(URL_P).fillna("---")
        d = pd.read_csv(URL_D).fillna("---")
        l = pd.read_csv(URL_L).fillna("---")
        for df in [p, d, l]: df.columns = df.columns.str.strip()
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d, l
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def login_user(u, p):
    if p == "2026": return "Admin"
    try:
        r = requests.get(f"{SCRIPT_URL}?nocache={time.time()}")
        if r.status_code == 200:
            for user in r.json():
                if (u.lower() == str(user.get('Email','')).lower() or u == str(user.get('Name',''))) and str(p) == str(user.get('Password','')):
                    return user.get('Name','User')
    except: pass
    return None

# --- 6. صفحة الدخول ---
if not st.session_state.auth:
    _, col_login, _ = st.columns([1, 1.2, 1])
    with col_login:
        st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول آمن", use_container_width=True):
            user = login_user(u, p)
            if user: st.session_state.auth = True; st.session_state.current_user = user; st.rerun()
            else: st.error("خطأ في البيانات")
    st.stop()

# --- 7. الواجهة الرئيسية ---
df_p, df_d, df_l = load_all_data()

# الهيدر الفخم
st.markdown(f"""
    <div class="royal-header">
        <h1 style="color: #f59e0b; font-size: 50px; margin: 0; font-weight: 900;">MA3LOMATI</h1>
        <p style="color: #888; letter-spacing: 5px; font-size: 14px;">REAL ESTATE INTELLIGENCE 2026</p>
    </div>
""", unsafe_allow_html=True)

# شريط التحكم (خروج يسار + منيو يمين)
col_menu, col_logout = st.columns([0.85, 0.15])
with col_logout:
    if st.button("🚪 خروج", use_container_width=True): 
        st.session_state.auth = False
        st.rerun()
with col_menu:
    menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], 
        icons=["briefcase", "building", "search", "robot", "rocket"], 
        default_index=4, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

if menu != st.session_state.last_menu:
    st.session_state.selected_item = None
    st.session_state.last_menu = menu

# --- 8. منطق الأقسام بنسبة 70% للمحتوى ---

# الحالة: تفاصيل عنصر
if st.session_state.selected_item is not None:
    it = st.session_state.selected_item
    if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
    
    col_main, col_side = st.columns([0.7, 0.3])
    with col_main:
        st.markdown(f"""<div class="info-card">
            <h1 style="color:#f59e0b;">{it.get('ProjectName', it.get('Project', it.get('Developer')))}</h1>
            <hr style="opacity:0.1">
            <p class="label-gold">📍 الموقع والاستراتيجية</p><h3>{it.get('Location','---')}</h3>
            <p class="label-gold">🏢 الشركة المطورة</p><h3>{it.get('Developer','---')}</h3>
            <p class="label-gold">🌟 نقاط البيع الفريدة (USP)</p>
            <p style="font-size:18px; line-height:1.8;">{it.get('Unique Selling Points (USP)', it.get('Notes','---'))}</p>
        </div>""", unsafe_allow_html=True)
    with col_side:
        st.markdown(f"""<div class="info-card">
            <p class="label-gold">💰 الأسعار وأنظمة السداد</p>
            <p style="font-size:20px;">{it.get('Price & Payment','سيتم التحديد')}</p>
            <hr style="opacity:0.1">
            <p class="label-gold">📏 المساحات المتاحة</p>
            <p>{it.get('Units & Sizes','---')}</p>
        </div>""", unsafe_allow_html=True)

# الحالة: القوائم الرئيسية
else:
    if menu == "اللونشات":
        st.markdown("<h3 style='color:#f59e0b;'>🚀 أحدث الانطلاقات العقارية</h3>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, r in df_l.iterrows():
            with cols[i % 3]:
                if st.button(f"🏢 {r['Developer']}\n{r['Project']}\n📍 {r['Location']}", key=f"card_l_{i}"):
                    st.session_state.selected_item = r; st.rerun()

    elif menu == "المشاريع":
        col_main, col_side = st.columns([0.7, 0.3])
        with col_side:
            st.markdown("<div class='info-card'><h4>🔍 فلترة المشاريع</h4>", unsafe_allow_html=True)
            search = st.text_input("ابحث بالاسم...")
            loc_f = st.selectbox("اختر المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
            st.markdown("</div>", unsafe_allow_html=True)
        with col_main:
            dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
            if loc_f != "الكل": dff = dff[dff['Location'] == loc_f]
            grid = st.columns(2)
            for i, r in dff.head(10).reset_index().iterrows():
                with grid[i % 2]:
                    if st.button(f"🏗️ {r['ProjectName']}\n📍 {r['Location']}\n🏢 {r['Developer']}", key=f"card_p_{i}"):
                        st.session_state.selected_item = r; st.rerun()

    elif menu == "المطورين":
        col_main, col_side = st.columns([0.7, 0.3])
        with col_side:
            st.markdown("<div class='info-card'><h4>🏆 كبار المطورين</h4><p>يتم عرض الشركات حسب التصنيف السوقي A+ لعام 2026</p></div>", unsafe_allow_html=True)
            search_d = st.text_input("بحث عن مطور...")
        with col_main:
            dfd = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
            grid = st.columns(2)
            for i, r in dfd.head(10).reset_index().iterrows():
                with grid[i % 2]:
                    if st.button(f"🏢 {r['Developer']}\n⭐ الفئة: {r.get('Developer Category','A')}", key=f"card_d_{i}"):
                        st.session_state.selected_item = r; st.rerun()

    elif menu == "المساعد الذكي":
        st.markdown("<div class='info-card' style='max-width:800px; margin:auto;'><h2>🤖 المساعد الذكي Pro</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        target_loc = c1.selectbox("📍 المنطقة المطلوبة", sorted(df_p['Location'].unique().tolist()))
        budget = c2.number_input("💰 الميزانية التقريبية للمقدم", 0)
        if st.button("تحليل واقتراح أفضل خيار", use_container_width=True):
            res = df_p[df_p['Location'] == target_loc].head(3)
            for _, r in res.iterrows():
                st.info(f"💡 نرشح لك مشروع {r['ProjectName']} من شركة {r['Developer']}")
        st.markdown("</div>", unsafe_allow_html=True)

    elif menu == "أدوات البروكر":
        st.markdown("<div class='info-card'><h3>🛠️ الحاسبة العقارية المتكاملة</h3>", unsafe_allow_html=True)
        cc1, cc2, cc3 = st.columns(3)
        price = cc1.number_input("سعر الوحدة", 1000000)
        years = cc2.slider("سنوات السداد", 1, 15, 8)
        down_p = cc3.number_input("المقدم", 0)
        
        rem = price - down_p
        st.metric("القسط الشهري", f"{rem/(years*12):,.0f} EGP")
        st.metric("القسط الربع سنوي", f"{rem/(years*4):,.0f} EGP")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة الفخمة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. روابط البيانات ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
URL_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'last_menu' not in st.session_state: st.session_state.last_menu = "اللونشات"

# --- 4. التنسيق الجمالي الاحترافي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* خلفية هادئة وفخمة */
    [data-testid="stAppViewContainer"] {
        background-color: #0a0a0a;
        background-image: radial-gradient(circle at 50% 50%, #1a1a1a 0%, #0a0a0a 100%);
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }

    /* هيدر ملكي */
    .royal-header {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(15px);
        border-bottom: 3px solid #f59e0b;
        padding: 40px 20px;
        text-align: center;
        border-radius: 0 0 50px 50px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* كروت الأزرار */
    div.stButton > button[key*="card_"] {
        background: rgba(30, 30, 30, 0.6) !important;
        color: #e0e0e0 !important;
        border: 1px solid #333 !important;
        border-right: 5px solid #f59e0b !important;
        border-radius: 12px !important;
        min-height: 120px !important;
        transition: 0.3s;
        font-weight: bold !important;
    }
    div.stButton > button:hover {
        background: rgba(245, 158, 11, 0.1) !important;
        border-color: #f59e0b !important;
        transform: translateY(-3px);
    }

    /* تفاصيل ذكية */
    .info-card {
        background: rgba(255,255,255,0.03);
        padding: 20px; border-radius: 20px;
        border: 1px solid #222;
    }
    
    .label-gold { color: #f59e0b; font-size: 14px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 5. وظائف الداتا والربط ---
@st.cache_data(ttl=60)
def load_all_data():
    try:
        p = pd.read_csv(URL_P).fillna("---")
        d = pd.read_csv(URL_D).fillna("---")
        l = pd.read_csv(URL_L).fillna("---")
        for df in [p, d, l]: df.columns = df.columns.str.strip()
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d, l
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def login_user(u, p):
    if p == "2026": return "Admin"
    try:
        r = requests.get(f"{SCRIPT_URL}?nocache={time.time()}")
        if r.status_code == 200:
            for user in r.json():
                if (u.lower() == str(user.get('Email','')).lower() or u == str(user.get('Name',''))) and str(p) == str(user.get('Password','')):
                    return user.get('Name','User')
    except: pass
    return None

# --- 6. صفحة الدخول ---
if not st.session_state.auth:
    _, col_login, _ = st.columns([1, 1.2, 1])
    with col_login:
        st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول آمن", use_container_width=True):
            user = login_user(u, p)
            if user: st.session_state.auth = True; st.session_state.current_user = user; st.rerun()
            else: st.error("خطأ في البيانات")
    st.stop()

# --- 7. الواجهة الرئيسية ---
df_p, df_d, df_l = load_all_data()

# الهيدر الفخم
st.markdown(f"""
    <div class="royal-header">
        <h1 style="color: #f59e0b; font-size: 50px; margin: 0; font-weight: 900;">MA3LOMATI</h1>
        <p style="color: #888; letter-spacing: 5px; font-size: 14px;">REAL ESTATE INTELLIGENCE 2026</p>
    </div>
""", unsafe_allow_html=True)

# شريط التحكم (خروج يسار + منيو يمين)
col_menu, col_logout = st.columns([0.85, 0.15])
with col_logout:
    if st.button("🚪 خروج", use_container_width=True): 
        st.session_state.auth = False
        st.rerun()
with col_menu:
    menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], 
        icons=["briefcase", "building", "search", "robot", "rocket"], 
        default_index=4, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

if menu != st.session_state.last_menu:
    st.session_state.selected_item = None
    st.session_state.last_menu = menu

# --- 8. منطق الأقسام بنسبة 70% للمحتوى ---

# الحالة: تفاصيل عنصر
if st.session_state.selected_item is not None:
    it = st.session_state.selected_item
    if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
    
    col_main, col_side = st.columns([0.7, 0.3])
    with col_main:
        st.markdown(f"""<div class="info-card">
            <h1 style="color:#f59e0b;">{it.get('ProjectName', it.get('Project', it.get('Developer')))}</h1>
            <hr style="opacity:0.1">
            <p class="label-gold">📍 الموقع والاستراتيجية</p><h3>{it.get('Location','---')}</h3>
            <p class="label-gold">🏢 الشركة المطورة</p><h3>{it.get('Developer','---')}</h3>
            <p class="label-gold">🌟 نقاط البيع الفريدة (USP)</p>
            <p style="font-size:18px; line-height:1.8;">{it.get('Unique Selling Points (USP)', it.get('Notes','---'))}</p>
        </div>""", unsafe_allow_html=True)
    with col_side:
        st.markdown(f"""<div class="info-card">
            <p class="label-gold">💰 الأسعار وأنظمة السداد</p>
            <p style="font-size:20px;">{it.get('Price & Payment','سيتم التحديد')}</p>
            <hr style="opacity:0.1">
            <p class="label-gold">📏 المساحات المتاحة</p>
            <p>{it.get('Units & Sizes','---')}</p>
        </div>""", unsafe_allow_html=True)

# الحالة: القوائم الرئيسية
else:
    if menu == "اللونشات":
        st.markdown("<h3 style='color:#f59e0b;'>🚀 أحدث الانطلاقات العقارية</h3>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, r in df_l.iterrows():
            with cols[i % 3]:
                if st.button(f"🏢 {r['Developer']}\n{r['Project']}\n📍 {r['Location']}", key=f"card_l_{i}"):
                    st.session_state.selected_item = r; st.rerun()

    elif menu == "المشاريع":
        col_main, col_side = st.columns([0.7, 0.3])
        with col_side:
            st.markdown("<div class='info-card'><h4>🔍 فلترة المشاريع</h4>", unsafe_allow_html=True)
            search = st.text_input("ابحث بالاسم...")
            loc_f = st.selectbox("اختر المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
            st.markdown("</div>", unsafe_allow_html=True)
        with col_main:
            dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
            if loc_f != "الكل": dff = dff[dff['Location'] == loc_f]
            grid = st.columns(2)
            for i, r in dff.head(10).reset_index().iterrows():
                with grid[i % 2]:
                    if st.button(f"🏗️ {r['ProjectName']}\n📍 {r['Location']}\n🏢 {r['Developer']}", key=f"card_p_{i}"):
                        st.session_state.selected_item = r; st.rerun()

    elif menu == "المطورين":
        col_main, col_side = st.columns([0.7, 0.3])
        with col_side:
            st.markdown("<div class='info-card'><h4>🏆 كبار المطورين</h4><p>يتم عرض الشركات حسب التصنيف السوقي A+ لعام 2026</p></div>", unsafe_allow_html=True)
            search_d = st.text_input("بحث عن مطور...")
        with col_main:
            dfd = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
            grid = st.columns(2)
            for i, r in dfd.head(10).reset_index().iterrows():
                with grid[i % 2]:
                    if st.button(f"🏢 {r['Developer']}\n⭐ الفئة: {r.get('Developer Category','A')}", key=f"card_d_{i}"):
                        st.session_state.selected_item = r; st.rerun()

    elif menu == "المساعد الذكي":
        st.markdown("<div class='info-card' style='max-width:800px; margin:auto;'><h2>🤖 المساعد الذكي Pro</h2>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        target_loc = c1.selectbox("📍 المنطقة المطلوبة", sorted(df_p['Location'].unique().tolist()))
        budget = c2.number_input("💰 الميزانية التقريبية للمقدم", 0)
        if st.button("تحليل واقتراح أفضل خيار", use_container_width=True):
            res = df_p[df_p['Location'] == target_loc].head(3)
            for _, r in res.iterrows():
                st.info(f"💡 نرشح لك مشروع {r['ProjectName']} من شركة {r['Developer']}")
        st.markdown("</div>", unsafe_allow_html=True)

    elif menu == "أدوات البروكر":
        st.markdown("<div class='info-card'><h3>🛠️ الحاسبة العقارية المتكاملة</h3>", unsafe_allow_html=True)
        cc1, cc2, cc3 = st.columns(3)
        price = cc1.number_input("سعر الوحدة", 1000000)
        years = cc2.slider("سنوات السداد", 1, 15, 8)
        down_p = cc3.number_input("المقدم", 0)
        
        rem = price - down_p
        st.metric("القسط الشهري", f"{rem/(years*12):,.0f} EGP")
        st.metric("القسط الربع سنوي", f"{rem/(years*4):,.0f} EGP")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
