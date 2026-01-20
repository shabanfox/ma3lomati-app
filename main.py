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
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة والربط
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# --- نظام الألوان عالي التباين (High Contrast CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    /* خلفية سوداء تماماً */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }

    /* نصوص بيضاء صريحة وأصفر فوسفوري */
    h1, h2, h3, b, strong { color: #FFFF00 !important; font-weight: 900 !important; }
    p, span, label, .stMarkdown { color: #FFFFFF !important; font-weight: 700 !important; font-size: 18px !important; }
    
    /* الكروت: خلفية سوداء + برواز أصفر سميك */
    div.stButton > button[key*="card_"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 3px solid #FFFF00 !important;
        border-radius: 10px !important;
        padding: 25px !important;
        font-size: 20px !important;
        width: 100% !important;
        font-weight: 900 !important;
    }
    div.stButton > button[key*="card_"]:hover {
        background-color: #FFFF00 !important;
        color: #000000 !important;
    }

    /* المدخلات والفلاتر: خلفية سوداء وخط أبيض */
    .stTextInput input, .stSelectbox div, .stMultiSelect div {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
        font-size: 16px !important;
    }
    
    /* إخفاء أي بياض ناتج عن Streamlit */
    .stTabs [data-baseweb="tab-list"] { background-color: #000 !important; }
    .stTabs [data-baseweb="tab"] { color: #FFF !important; border: 1px solid #FFFF00 !important; margin: 5px; }
    </style>
""", unsafe_allow_html=True)

# 3. وظائف الدخول والبيانات
def login_user(u, p):
    try:
        res = requests.get(f"{SCRIPT_URL}?nocache={time.time()}").json()
        for user in res:
            if (u.lower() == str(user.get('Name')).lower()) and str(p) == str(user.get('Password')): return user.get('Name')
        return None
    except: return None

@st.cache_data
def load_data():
    url_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    url_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    p = pd.read_csv(url_p).fillna("---")
    d = pd.read_csv(url_d).fillna("---")
    p.rename(columns={'Area': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
    return p, d

# --- شاشة الدخول ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>دخول المحترفين</h1>", unsafe_allow_html=True)
    u = st.text_input("الأسم")
    p = st.text_input("كلمة السر", type="password")
    if st.button("دخول ✅"):
        if p == "2026": st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
        user = login_user(u, p)
        if user: st.session_state.auth = True; st.session_state.current_user = user; st.rerun()
        else: st.error("بياناتك غير صحيحة")
    st.stop()

df_p, df_d = load_data()

# --- المنيو الرئيسي ---
menu = option_menu(None, ["المشاريع", "المساعد الذكي", "المطورين", "الأدوات"], 
    icons=["building", "robot", "people", "calculator"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#FFFF00", "color": "#000"}})

# 1. صفحة المشاريع
if menu == "المشاريع":
    st.markdown("### 🔍 الفلاتر القوية")
    c1, c2 = st.columns(2)
    f_loc = c1.multiselect("📍 المناطق", options=df_p['Location'].unique())
    f_search = c2.text_input("🔍 اسم المشروع")
    
    res = df_p.copy()
    if f_loc: res = res[res['Location'].isin(f_loc)]
    if f_search: res = res[res['ProjectName'].str.contains(f_search, case=False)]
    
    for i in range(0, len(res), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(res):
                item = res.iloc[i+j]
                if cols[j].button(f"🏢 {item['ProjectName']}\n📍 {item['Location']}", key=f"card_p_{i+j}"):
                    st.session_state.selected_item = item; st.rerun()

# 2. الأدوات (حواسب البروكر)
elif menu == "الأدوات":
    st.markdown("### 🛠️ أدوات الحساب")
    c1, c2 = st.columns(2)
    with c1:
        st.write("💰 حاسبة القسط")
        v = st.number_input("سعر الوحدة", value=1000000)
        y = st.slider("السنين", 1, 10, 8)
        st.success(f"القسط: {v/(y*12):,.0f} ج.م")
    with c2:
        st.write("📈 حاسبة العمولة")
        deal = st.number_input("الصفقة", value=1000000)
        pct = st.slider("النسبة", 1.0, 5.0, 1.5)
        st.warning(f"ربحك: {deal*(pct/100):,.0f} ج.م")

# 3. المساعد الذكي
elif menu == "المساعد الذكي":
    st.markdown("### 🤖 المساعد الذكي")
    req = st.text_area("احتياج العميل...")
    if st.button("🎯 استخراج"):
        st.write("أفضل مشاريع تناسب الطلب:")
        for r in df_p.head(3).iterrows(): st.write(f"✅ {r[1]['ProjectName']}")

# تفاصيل المشروع
if st.session_state.selected_item is not None:
    st.markdown("---")
    item = st.session_state.selected_item
    st.markdown(f"<div style='border:5px solid #FFFF00; padding:20px;'>", unsafe_allow_html=True)
    st.header(f"📌 {item.get('ProjectName', item.get('Developer'))}")
    st.write(item)
    if st.button("❌ إغلاق"): st.session_state.selected_item = None; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()
