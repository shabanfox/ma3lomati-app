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

# 2. روابط الهوية
HEADER_BG = "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=2000&auto=format&fit=crop"

# 3. الربط مع جوجل شيت
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# --- التنسيق الجمالي الاحترافي (Advanced CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container {{ padding: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{ background-color: #000000; direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }}
    
    /* الهيدر الزجاجي */
    .hero-section {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('{HEADER_BG}');
        background-size: cover; background-position: center;
        padding: 60px 20px; text-align: center; border-bottom: 5px solid #FFD700;
        border-radius: 0 0 50px 50px;
    }}
    
    /* وضوح الخطوط */
    h1, h2, h3 {{ color: #FFD700 !important; font-weight: 900 !important; text-shadow: 2px 2px 4px rgba(0,0,0,1); }}
    p, span, label {{ color: #ffffff !important; font-size: 16px !important; font-weight: 600 !important; }}
    
    /* الكروت الاحترافية */
    div.stButton > button[key*="card_"] {{
        background: #111111 !important; color: #FFD700 !important;
        border: 2px solid #333 !important; border-radius: 20px !important;
        padding: 25px !important; transition: 0.3s all ease;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.05);
    }}
    div.stButton > button[key*="card_"]:hover {{
        border-color: #FFD700 !important; transform: translateY(-8px);
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.2);
    }}
    
    /* الفلاتر والأدوات */
    .filter-box {{ background: #1a1a1a; padding: 20px; border-radius: 20px; border: 1px solid #FFD700; margin-bottom: 20px; }}
    .tool-card {{ background: #0a0a0a; border: 1px solid #333; padding: 25px; border-radius: 25px; border-top: 5px solid #FFD700; }}
    
    /* شريط الأخبار */
    .ticker-wrap {{ background: #FFD700; color: #000; padding: 8px 0; font-weight: bold; font-size: 15px; }}
    </style>
""", unsafe_allow_html=True)

# 4. وظائف الدخول (مختصرة للربط)
def login_user(u, p):
    try:
        res = requests.get(SCRIPT_URL).json()
        for user in res:
            if (u == user.get('Name') or u == user.get('Email')) and str(p) == str(user.get('Password')): return user.get('Name')
        return None
    except: return None

# --- واجهة تسجيل الدخول ---
if not st.session_state.auth:
    st.markdown("<div class='hero-section'><h1>MA3LOMATI PRO</h1><p>النسخة الاحترافية للوسطاء العقاريين 2026</p></div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔒 دخول", "📝 اشتراك"])
    with tab1:
        u = st.text_input("المستخدم")
        p = st.text_input("الباسورد", type="password")
        if st.button("فتح المنصة 🚀"):
            if p == "2026": st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
            auth_user = login_user(u, p)
            if auth_user: st.session_state.auth = True; st.session_state.current_user = auth_user; st.rerun()
            else: st.error("خطأ في البيانات")
    st.stop()

# --- جلب البيانات ---
@st.cache_data
def get_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    p = pd.read_csv(u_p).fillna("---")
    d = pd.read_csv(u_d).fillna("---")
    p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
    return p, d

df_p, df_d = get_data()

# --- الصفحة الرئيسية بعد الدخول ---
st.markdown(f"<div class='hero-section'><h1>أهلاً بك، {st.session_state.current_user}</h1><p>استكشف أقوى عروض الـ Primary في مصر</p></div>", unsafe_allow_html=True)

menu = option_menu(None, ["المشاريع", "المساعد الذكي", "المطورين", "حاسبة البروكر"], 
    icons=["house-door", "robot", "building", "calculator"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#FFD700", "color": "#000"}})

# 1. صفحة المشاريع (مع الفلاتر القوية)
if menu == "المشاريع":
    with st.container():
        st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        f_loc = c1.multiselect("📍 اختر المناطق", df_p['Location'].unique())
        f_dev = c2.selectbox("🏗️ المطور", ["الكل"] + list(df_p['Developer'].unique()))
        f_search = c3.text_input("🔍 بحث بالاسم")
        st.markdown("</div>", unsafe_allow_html=True)
        
        filtered_df = df_p.copy()
        if f_loc: filtered_df = filtered_df[filtered_df['Location'].isin(f_loc)]
        if f_dev != "الكل": filtered_df = filtered_df[filtered_df['Developer'] == f_dev]
        if f_search: filtered_df = filtered_df[filtered_df['ProjectName'].str.contains(f_search, case=False)]
        
        # عرض المشاريع في كروت واضحة
        rows = len(filtered_df) // 2 + (len(filtered_df) % 2 > 0)
        for i in range(rows):
            cols = st.columns(2)
            for j in range(2):
                idx = i*2 + j
                if idx < len(filtered_df):
                    item = filtered_df.iloc[idx]
                    if cols[j].button(f"🏢 {item['ProjectName']}\n📍 {item['Location']}\n💰 {item.get('Price','تواصل للتفاصيل')}", key=f"card_p_{idx}"):
                        st.session_state.selected_item = item; st.rerun()

# 2. صفحة حاسبة البروكر (الأدوات القوية)
elif menu == "حاسبة البروكر":
    st.title("🛠️ الأدوات الهندسية والمالية")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='tool-card'><h3>💳 حاسبة الأقساط المتقدمة</h3>", unsafe_allow_html=True)
        total = st.number_input("إجمالي سعر الوحدة", value=5000000)
        down = st.number_input("المقدم المدفوع", value=500000)
        years = st.slider("عدد سنوات التقسيط", 1, 15, 8)
        monthly = (total - down) / (years * 12)
        st.metric("القسط الشهري", f"{monthly:,.0f} EGP")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with c2:
        st.markdown("<div class='tool-card'><h3>💰 حاسبة العمولات والضرائب</h3>", unsafe_allow_html=True)
        price = st.number_input("سعر البيع النهائي", value=10000000)
        comm = st.slider("نسبة عمولتك %", 0.0, 5.0, 1.5)
        st.metric("صافي عمولتك", f"{price * (comm/100):,.0f} EGP")
        st.write(f"ضريبة التصرفات (2.5%): {price * 0.025:,.0f} EGP")
        st.markdown("</div>", unsafe_allow_html=True)

# 3. صفحة المساعد الذكي
elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 مساعد الربط الآلي")
    client_req = st.text_area("انسخ هنا طلب العميل (مثال: بدور على شقة في التجمع بـ 5 مليون ومقدم 10%)")
    if st.button("🎯 استخراج أفضل الفرص"):
        st.info("جاري تحليل طلب العميل ومطابقته مع المطورين...")
        # هنا يمكن إضافة منطق الربط الذكي
        st.success("أقوى 3 ترشيحات جاهزة للإرسال على واتساب!")
    st.markdown("</div>", unsafe_allow_html=True)

# عرض التفاصيل عند الضغط على كرت
if st.session_state.selected_item is not None:
    st.markdown("---")
    item = st.session_state.selected_item
    st.markdown(f"""
    <div class='smart-box'>
        <h2>✨ تفاصيل: {item['ProjectName']}</h2>
        <p>🏗️ المطور: {item['Developer']}</p>
        <p>📍 الموقع الدقيق: {item['Location']}</p>
        <p>🛋️ أنواع الوحدات: شقق - فيلات - تجاري</p>
        <button onclick="window.location.reload()">⬅️ عودة للمشاريع</button>
    </div>
    """, unsafe_allow_html=True)
    if st.button("إغلاق التفاصيل"): st.session_state.selected_item = None; st.rerun()

st.markdown("<p style='text-align:center; padding:20px;'>MA3LOMATI PRO © 2026 | القوة في المعلومة</p>", unsafe_allow_html=True)

