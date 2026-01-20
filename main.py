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

# --- ميزة حماية الموبايل (منع الخروج بزر الرجوع) ---
st.components.v1.html("""
<script>
    window.onbeforeunload = function() { return "هل تريد مغادرة المنصة؟"; };
    history.pushState(null, null, location.href);
    window.onpopstate = function () { history.go(1); };
</script>
""", height=0)

# 2. الرابط الخاص بك
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# 3. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# 4. التنسيق الجمالي (White & Gold Luxury UI)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    /* الخلفية الكحلية الداكنة */
    [data-testid="stAppViewContainer"] {{ 
        background-color: #0a192f; 
        direction: rtl !important; 
        text-align: right !important; 
        font-family: 'Cairo', sans-serif; 
    }}
    
    /* نصوص بيضاء ناصعة وواضحة جداً */
    p, span, label, li, .stWrite, .stMetric div, .stMarkdown, div[data-testid="stExpander"] p {{ 
        color: #ffffff !important; 
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
    }}
    
    /* عناوين ذهبية ملكية */
    h1, h2, h3, h4, .stMetric label {{ 
        color: #f59e0b !important; 
        font-weight: 900 !important;
    }}

    /* أزرار النظام (أبيض داخل ذهبي) */
    div.stButton > button {{ 
        border-radius: 12px !important; 
        background-color: #112240 !important;
        color: #ffffff !important;
        border: 2px solid #f59e0b !important;
        transition: 0.3s !important;
        font-weight: bold !important;
    }}
    
    /* كروت المشاريع (تأثير الفخامة) */
    div.stButton > button[key*="card_"], div.stButton > button[key*="ready_"] {{
        background: linear-gradient(145deg, #112240, #0a192f) !important;
        color: #ffffff !important;
        border-right: 8px solid #f59e0b !important;
        min-height: 120px !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.4) !important;
    }}

    div.stButton > button:hover {{ 
        background-color: #f59e0b !important; 
        color: #000000 !important; 
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.4) !important;
    }}

    /* صناديق المحتوى المحسنة */
    .smart-box {{ 
        background: #112240; 
        border: 2px solid #233554; 
        padding: 20px; 
        border-radius: 20px; 
        border-right: 6px solid #f59e0b;
        color: #ffffff !important;
    }}

    /* تحسين شكل خانات الإدخال */
    input, textarea {{ 
        color: white !important; 
        background-color: #0d1e36 !important; 
        border: 1px solid #f59e0b !important; 
    }}
    
    /* شريط الأخبار */
    .ticker-wrap {{ background: #112240; border-bottom: 2px solid #f59e0b; }}
    .ticker {{ color: #f59e0b !important; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# 5. دوال جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p
    except: return pd.DataFrame()

df_p = load_data()

# 6. نظام الدخول
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; padding-top:50px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1.5,1])
    with c2:
        u_in = st.text_input("الأسم")
        p_in = st.text_input("كلمة السر", type="password")
        if st.button("دخول للمنصة 🚀"):
            if p_in == "2026":
                st.session_state.auth, st.session_state.current_user = True, "Admin"
                st.rerun()
    st.stop()

# 7. واجهة المنصة الرئيسية
st.markdown(f"""<div class='smart-box' style='text-align:center;'>
    <h1 style='margin:0;'>MA3LOMATI PRO</h1>
    <p style='color:#f59e0b !important; font-size:18px;'>مرحباً {st.session_state.current_user} | {egypt_now.strftime('%I:%M %p')}</p>
</div>""", unsafe_allow_html=True)

menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# 8. عرض البيانات
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"<div class='smart-box'><h2>{item['ProjectName']}</h2><p>📍 الموقع: {item['Location']}</p></div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    search = st.text_input("🔍 ابحث عن مشروع...")
    dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
    for i in range(0, len(dff.head(6)), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(dff):
                row = dff.iloc[i+j]
                if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}", key=f"card_p_{i+j}"):
                    st.session_state.selected_item = row; st.rerun()

elif menu == "أدوات البروكر":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    v = st.number_input("سعر الوحدة", 1000000)
    st.metric("القسط الشهري (على 8 سنوات)", f"{v/96:,.0f}")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#555; padding:30px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
