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
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="expanded")

# 2. روابط الصور
HEADER_BG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=2000&auto=format&fit=crop"

# 3. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# --- التنسيق الجمالي (Ultra Contrast CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* الأساسيات: خلفية سوداء وخط أبيض */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: #000000 !important;
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }}
    
    /* الخطوط الفاتحة على الخلفية الغامقة */
    h1, h2, h3, h4, h5, h6 {{ color: #FFD700 !important; font-weight: 900 !important; }}
    p, span, label, div {{ color: #ffffff !important; font-weight: 700 !important; }}
    
    /* تصميم الكروت (خلفية رمادي غامق جداً + حدود ذهبية) */
    div.stButton > button[key*="card_"] {{
        background-color: #111111 !important;
        color: #ffffff !important;
        border: 2px solid #FFD700 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        font-size: 18px !important;
        width: 100% !important;
        text-align: right !important;
    }}
    
    /* العكس: خلفية فاتحة للخط الغامق (في التنبيهات فقط) */
    .stAlert {{
        background-color: #FFD700 !important;
        color: #000000 !important;
        font-weight: 900 !important;
    }}
    
    /* تحسين شكل المدخلات (Inputs) */
    input, select, textarea {{
        background-color: #222222 !important;
        color: #ffffff !important;
        border: 1px solid #FFD700 !important;
    }}
    
    /* الهيدر */
    .main-header {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('{HEADER_BG}');
        background-size: cover;
        padding: 40px;
        border-bottom: 5px solid #FFD700;
        text-align: center;
        border-radius: 0 0 20px 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# 4. جلب البيانات
@st.cache_data
def load_all_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    p = pd.read_csv(u_p).fillna("غير متوفر")
    d = pd.read_csv(u_d).fillna("غير متوفر")
    p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
    return p, d

df_p, df_d = load_all_data()

# --- شاشة الدخول ---
if not st.session_state.auth:
    st.markdown("<div class='main-header'><h1>MA3LOMATI PRO</h1><p>سجل دخول للوصول لأقوى قاعدة بيانات عقارية</p></div>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 2, 1])
    with col:
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة السر", type="password")
        if st.button("دخول ✅"):
            if p == "2026": # كود سريع للتجربة
                st.session_state.auth = True; st.rerun()
            else: st.error("كلمة السر خطأ")
    st.stop()

# --- القائمة الجانبية (فلاتر قوية) ---
with st.sidebar:
    st.image(HEADER_BG, use_container_width=True)
    st.title("🔍 فلاتر البحث")
    f_loc = st.multiselect("📍 المنطقة", options=sorted(df_p['Location'].unique()))
    f_dev = st.selectbox("🏗️ المطور", options=["الكل"] + sorted(df_p['Developer'].unique()))
    f_status = st.radio("🔑 حالة التسليم", ["الكل", "استلام فوري", "تحت الإنشاء"])
    
    st.markdown("---")
    if st.button("🚪 تسجيل خروج"):
        st.session_state.auth = False; st.rerun()

# --- المحتوى الرئيسي ---
st.markdown("<div class='main-header'><h1>معلوماتي العقارية</h1></div>", unsafe_allow_html=True)

menu = option_menu(None, ["المشاريع", "المساعد الذكي", "المطورين", "الأدوات"], 
    icons=["building", "robot", "people", "calculator"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#FFD700", "color": "#000000"}})

# 1. المشاريع
if menu == "المشاريع":
    filtered = df_p.copy()
    if f_loc: filtered = filtered[filtered['Location'].isin(f_loc)]
    if f_dev != "الكل": filtered = filtered[filtered['Developer'] == f_dev]
    
    st.subheader(f"تم إيجاد {len(filtered)} مشروع")
    
    # عرض في صفوف
    for i in range(0, len(filtered), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(filtered):
                item = filtered.iloc[i+j]
                with cols[j]:
                    if st.button(f"🏢 {item['ProjectName']}\n📍 {item['Location']}\n🏗️ {item['Developer']}", key=f"card_p_{i+j}"):
                        st.session_state.selected_item = item; st.rerun()

# 2. المساعد الذكي
elif menu == "المساعد الذكي":
    st.markdown("### 🤖 المساعد الذكي (AI Matcher)")
    req = st.text_area("اكتب طلب العميل هنا...")
    if st.button("🎯 استخراج الترشيحات"):
        st.success("جاري مطابقة الطلب مع المشروعات المتاحة...")

# 3. المطورين
elif menu == "المطورين":
    st.subheader("🏗️ قائمة المطورين المعتمدين")
    for i, r in df_d.head(10).iterrows():
        if st.button(f"🏢 {r['Developer']}\n⭐ الفئة: {r.get('Developer Category','A')}", key=f"card_d_{i}"):
            st.session_state.selected_item = r; st.rerun()

# 4. الأدوات (حواسب البروكر)
elif menu == "الأدوات":
    st.subheader("🛠️ أدوات البروكر الذكية")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div style='border:1px solid #FFD700; padding:20px; border-radius:15px;'>", unsafe_allow_html=True)
        st.write("### 💳 حاسبة القسط")
        price = st.number_input("سعر الوحدة", value=5000000)
        down = st.number_input("المقدم", value=500000)
        years = st.slider("السنين", 1, 15, 8)
        st.metric("القسط الشهري", f"{(price-down)/(years*12):,.0f} ج.م")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div style='border:1px solid #FFD700; padding:20px; border-radius:15px;'>", unsafe_allow_html=True)
        st.write("### 💰 حاسبة العمولة")
        deal = st.number_input("قيمة البيعة", value=1000000)
        pct = st.slider("نسبة العمولة %", 0.5, 5.0, 1.5)
        st.metric("ربحك الصافي", f"{deal*(pct/100):,.0f} ج.م")
        st.markdown("</div>", unsafe_allow_html=True)

# عرض التفاصيل
if st.session_state.selected_item is not None:
    st.markdown("---")
    item = st.session_state.selected_item
    st.success(f"📌 تفاصيل: {item.get('ProjectName', item.get('Developer'))}")
    st.write(item)
    if st.button("❌ إغلاق"): st.session_state.selected_item = None; st.rerun()

st.markdown("<p style='text-align:center; color:#555;'>MA3LOMATI PRO 2026</p>", unsafe_allow_html=True)
