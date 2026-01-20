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

# --- حماية زر الرجوع في الموبايل ---
st.components.v1.html("""
<script>
    window.onbeforeunload = function() { return "هل تريد المغادرة؟"; };
    history.pushState(null, null, location.href);
    window.onpopstate = function () { history.go(1); };
</script>
""", height=0)

# 2. التنسيق الجمالي (CSS) - ألوان سوبر واضحة
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container { padding-top: 1rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    
    /* الخلفية والخطوط */
    [data-testid="stAppViewContainer"] { 
        background-color: #0a192f; 
        direction: rtl !important; 
        text-align: right !important; 
        font-family: 'Cairo', sans-serif; 
    }
    
    /* نصوص بيضاء واضحة جداً */
    p, span, label, .stWrite, .stMetric div { 
        color: #ffffff !important; 
        font-weight: 600 !important; 
    }
    
    /* العناوين الذهبية */
    h1, h2, h3 { 
        color: #f59e0b !important; 
        font-weight: 900 !important; 
    }

    /* كروت المشاريع - كتابة بيضاء Bold */
    div.stButton > button {
        background: linear-gradient(145deg, #112240, #0a192f) !important;
        color: #ffffff !important;
        border: 1px solid #233554 !important;
        border-right: 6px solid #f59e0b !important;
        border-radius: 12px !important;
        min-height: 110px !important;
        width: 100% !important;
        font-size: 16px !important;
        font-weight: bold !important;
        margin-bottom: 15px !important;
    }
    
    div.stButton > button:hover {
        border-color: #f59e0b !important;
        color: #f59e0b !important;
    }

    /* الصناديق والمدخلات */
    .smart-box { 
        background: #112240; 
        border: 1px solid #233554; 
        padding: 25px; 
        border-radius: 20px; 
        border-right: 6px solid #f59e0b; 
    }
    input { color: white !important; background-color: #0d1e36 !important; }
</style>
""", unsafe_allow_html=True)

# 3. جلب البيانات (مع معالجة الأخطاء صح)
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p
    except Exception as e:
        st.error(f"خطأ في جلب البيانات: {e}")
        return pd.DataFrame()

df_p = load_data()

# 4. إدارة الجلسة والدخول
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; padding-top:50px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1.5,1])
    with c2:
        u_in = st.text_input("الأسم")
        p_in = st.text_input("كلمة السر", type="password")
        if st.button("دخول 🚀"):
            if p_in == "2026":
                st.session_state.auth, st.session_state.current_user = True, "Admin"
                st.rerun()
            else: st.error("بيانات غير صحيحة")
    st.stop()

# 5. الواجهة الرئيسية
egypt_now = datetime.now(pytz.timezone('Africa/Cairo'))
st.markdown(f"""<div class='smart-box' style='text-align:center;'>
    <h1 style='margin:0;'>MA3LOMATI PRO</h1>
    <p style='color:#f59e0b !important;'>أهلاً {st.session_state.current_user} | {egypt_now.strftime('%I:%M %p')}</p>
</div>""", unsafe_allow_html=True)

menu = option_menu(None, ["المشاريع", "المساعد الذكي", "أدوات البروكر"], 
    icons=["search", "robot", "calculator"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# 6. منطق العرض
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة"):
        st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"<div class='smart-box'><h2>{item['ProjectName']}</h2><p>الموقع: {item['Location']}</p></div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    search = st.text_input("🔍 ابحث عن اسم المشروع")
    dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
    for i in range(0, len(dff.head(6)), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(dff):
                row = dff.iloc[i+j]
                if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}", key=f"btn_{i+j}"):
                    st.session_state.selected_item = row; st.rerun()

elif menu == "أدوات البروكر":
    st.title("🛠️ حاسبة القسط")
    v = st.number_input("سعر الوحدة", 1000000)
    st.metric("القسط الشهري (على 8 سنوات)", f"{v/96:,.0f}")

st.markdown("<p style='text-align:center; color:#4f5b7d; padding:20px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
