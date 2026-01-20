import streamlit as st
import pandas as pd
import requests
import feedparser
import time
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة ودعم الروابط (لزر الرجوع)
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide")

# إدارة التنقل عبر الروابط (Query Params) لدعم زر "الباك" في الهاتف
query_params = st.query_params
if "page" not in query_params:
    st.query_params["page"] = "home"

# 2. البيانات والربط
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None

# --- نظام الألوان (Ultra High Contrast) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    
    /* خلفية سوداء 100% */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #000000 !important;
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }

    /* نصوص بيضاء ناصعة وعناوين صفراء فوسفورية */
    h1, h2, h3, b, strong { color: #FFFF00 !important; font-weight: 900 !important; }
    p, span, label { color: #FFFFFF !important; font-weight: 800 !important; font-size: 18px !important; }
    
    /* الكروت ببرواز أبيض سميك للوضوح */
    div.stButton > button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 3px solid #FFFFFF !important;
        border-radius: 8px !important;
        padding: 20px !important;
        font-size: 18px !important;
        width: 100% !important;
        font-weight: 900 !important;
        margin-bottom: 10px;
    }
    
    /* عند الضغط على الزرار */
    div.stButton > button:active, div.stButton > button:focus {
        background-color: #FFFF00 !important;
        color: #000000 !important;
        border: 3px solid #FFFF00 !important;
    }

    /* تحسين شكل الفلاتر والمدخلات */
    .stTextInput input, .stSelectbox div, .stMultiSelect div {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFF00 !important;
        font-size: 18px !important;
        border-radius: 5px !important;
    }
    
    /* إخفاء شريط الأدوات الافتراضي لزيادة التركيز */
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. وظائف الدخول
def login_user(u, p):
    try:
        res = requests.get(f"{SCRIPT_URL}?nocache={time.time()}").json()
        for user in res:
            if (u.lower() == str(user.get('Name')).lower() or u.lower() == str(user.get('Email')).lower()) and str(p) == str(user.get('Password')):
                return user.get('Name')
        return None
    except: return None

@st.cache_data
def load_data():
    try:
        url_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
        url_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
        p = pd.read_csv(url_p).fillna("---")
        d = pd.read_csv(url_d).fillna("---")
        p.rename(columns={'Area': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

# --- شاشة الدخول ---
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>MA3LOMATI PRO 2026</h1>", unsafe_allow_html=True)
    with st.container():
        u = st.text_input("الأسم أو البريد")
        p = st.text_input("كلمة السر", type="password")
        if st.button("دخول للمنصة 🚀"):
            if p == "2026": 
                st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
            user = login_user(u, p)
            if user:
                st.session_state.auth = True; st.session_state.current_user = user; st.rerun()
            else: st.error("❌ بيانات الدخول غير صحيحة")
    st.stop()

df_p, df_d = load_data()

# --- القائمة الرئيسية ---
# نستخدم Query Params لتغيير الصفحة حتى يعمل زر الباك
current_page = st.query_params.get("page", "المشاريع")

menu = option_menu(None, ["المشاريع", "المساعد الذكي", "المطورين", "الأدوات"], 
    icons=["building", "robot", "people", "calculator"], 
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"background-color": "#000"},
        "nav-link": {"color": "#FFF", "font-size": "14px", "text-align": "center"},
        "nav-link-selected": {"background-color": "#FFFF00", "color": "#000", "font-weight": "bold"}
    })

# تحديث الرابط عند تغيير القائمة
if menu != st.query_params.get("page"):
    st.query_params["page"] = menu

# --- محتوى الصفحات ---

if menu == "المشاريع":
    st.markdown("### 🔍 بحث متقدم")
    c1, c2 = st.columns(2)
    f_loc = c1.multiselect("📍 المناطق", options=df_p['Location'].unique())
    f_search = c2.text_input("🔍 ابحث عن اسم المشروع...")
    
    res = df_p.copy()
    if f_loc: res = res[res['Location'].isin(f_loc)]
    if f_search: res = res[res['ProjectName'].str.contains(f_search, case=False)]
    
    for i, row in res.iterrows():
        with st.container():
            # جعل الكارت كبير وواضح جداً
            if st.button(f"🏢 {row['ProjectName']} | 📍 {row['Location']}\n🏗️ المطور: {row['Developer']}", key=f"p_{i}"):
                st.session_state.selected_item = row
                st.query_params["item"] = row['ProjectName']
                st.rerun()

elif menu == "الأدوات":
    st.markdown("### 🛠️ حواسب البروكر الذكية")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div style='border:2px solid #FFFF00; padding:15px; border-radius:10px;'>", unsafe_allow_html=True)
        st.write("💰 **حاسبة القسط**")
        price = st.number_input("سعر الوحدة", value=1000000, step=100000)
        years = st.slider("السنين", 1, 15, 8)
        st.warning(f"القسط الشهري: {price/(years*12):,.0f} ج.م")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='border:2px solid #FFFF00; padding:15px; border-radius:10px;'>", unsafe_allow_html=True)
        st.write("📈 **حاسبة العمولة**")
        deal = st.number_input("الصفقة", value=2000000)
        pct = st.slider("النسبة %", 1.0, 5.0, 1.5)
        st.success(f"عمولتك: {deal*(pct/100):,.0f} ج.م")
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "المساعد الذكي":
    st.markdown("### 🤖 المساعد الذكي")
    req = st.text_area("أدخل طلب العميل هنا (مثلاً: شقة في التجمع بـ 5 مليون ومقدم 10%)")
    if st.button("🎯 استخراج الترشيحات"):
        st.write("✅ جاري تحليل البيانات ومطابقتها...")
        time.sleep(1)
        st.info("تم العثور على 3 مشاريع مطابقة لطلبك!")

# عرض تفاصيل المشروع (Popup)
if "item" in st.query_params:
    st.markdown("---")
    st.markdown("<div style='border:4px solid #FFFF00; padding:20px; background-color:#111;'>", unsafe_allow_html=True)
    st.header(f"✨ تفاصيل المشروع")
    # البحث عن المشروع المختار في الداتا
    item_details = df_p[df_p['ProjectName'] == st.query_params["item"]].iloc[0]
    st.write(item_details)
    if st.button("⬅️ عودة للمشاريع"):
        del st.query_params["item"]
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

if st.button("🚪 خروج من النظام"):
    st.session_state.auth = False
    st.rerun()
