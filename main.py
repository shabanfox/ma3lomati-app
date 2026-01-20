import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide")

# إدارة التنقل لزر الرجوع
if "page" not in st.query_params:
    st.query_params["page"] = "المشاريع"

# 2. روابط البيانات والربط
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

if 'auth' not in st.session_state: st.session_state.auth = False

# --- نظام الألوان الاحترافي (Elite Dark Mode) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* الخلفية الاحترافية */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0E1117 !important;
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }

    /* نصوص هادئة وواضحة */
    h1, h2, h3 { color: #FFFFFF !important; font-weight: 900 !important; }
    p, span, label { color: #E0E0E0 !important; font-weight: 600 !important; font-size: 16px !important; }
    
    /* الكروت: رمادي داكن مع حافة زرقاء رقيقة */
    div.stButton > button {
        background-color: #161B22 !important;
        color: #FFFFFF !important;
        border: 1px solid #30363D !important;
        border-right: 5px solid #1E90FF !important;
        border-radius: 8px !important;
        padding: 15px !important;
        transition: 0.3s all;
        text-align: right !important;
        width: 100% !important;
    }
    
    div.stButton > button:hover {
        border-color: #1E90FF !important;
        background-color: #1C2128 !important;
        transform: translateY(-2px);
    }

    /* تحسين شكل الفلاتر */
    .stTextInput input, .stSelectbox div, .stMultiSelect div {
        background-color: #0D1117 !important;
        color: #FFFFFF !important;
        border: 1px solid #30363D !important;
        border-radius: 5px !important;
    }

    /* زرار الخروج بلون أحمر هادئ */
    button[key="logout_btn"] {
        background-color: #DA3633 !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. وظيفة الدخول
def login_user(u, p):
    try:
        res = requests.get(f"{SCRIPT_URL}?nocache={time.time()}").json()
        for user in res:
            if (u.lower() == str(user.get('Name')).lower()) and str(p) == str(user.get('Password')):
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
    st.markdown("<h1 style='text-align:center;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    with st.container():
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة السر", type="password")
        if st.button("دخول آمن 🔒"):
            if p == "2026": 
                st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
            user = login_user(u, p)
            if user:
                st.session_state.auth = True; st.session_state.current_user = user; st.rerun()
            else: st.error("عفواً، البيانات غير صحيحة")
    st.stop()

df_p, df_d = load_data()

# --- المنيو العلوي ---
menu = option_menu(None, ["المشاريع", "المساعد الذكي", "المطورين", "الأدوات"], 
    icons=["building", "robot", "people", "calculator"], 
    default_index=0, orientation="horizontal",
    styles={
        "container": {"background-color": "#161B22", "border": "1px solid #30363D"},
        "nav-link-selected": {"background-color": "#1E90FF", "color": "white"}
    })

# --- محتوى الصفحات ---
if menu == "المشاريع":
    st.markdown("### 🔍 تصفية النتائج")
    c1, c2 = st.columns(2)
    f_loc = c1.multiselect("📍 المنطقة", options=sorted(df_p['Location'].unique()))
    f_search = c2.text_input("🔍 ابحث عن مشروع...")
    
    res = df_p.copy()
    if f_loc: res = res[res['Location'].isin(f_loc)]
    if f_search: res = res[res['ProjectName'].str.contains(f_search, case=False)]
    
    for i, row in res.iterrows():
        if st.button(f"🏢 {row['ProjectName']} — {row['Location']}\n🏗️ مطور: {row['Developer']}", key=f"p_{i}"):
            st.session_state.selected_item = row
            st.query_params["item"] = row['ProjectName']
            st.rerun()

elif menu == "الأدوات":
    st.markdown("### 🛠️ الحاسبة العقارية")
    col1, col2 = st.columns(2)
    with col1:
        st.write("💰 **حساب القسط**")
        price = st.number_input("السعر الإجمالي", value=1000000)
        years = st.slider("السنين", 1, 15, 8)
        st.info(f"القسط الشهري التقديري: {price/(years*12):,.0f} ج.م")
    with col2:
        st.write("📈 **حساب العمولات**")
        deal = st.number_input("قيمة الصفقة", value=2000000)
        pct = st.slider("النسبة %", 1.0, 5.0, 1.5)
        st.success(f"صافي الربح: {deal*(pct/100):,.0f} ج.م")

# تفاصيل المشروع (تظهر عند الضغط)
if "item" in st.query_params:
    st.markdown("---")
    item_details = df_p[df_p['ProjectName'] == st.query_params["item"]].iloc[0]
    with st.expander("📄 تفاصيل المشروع كاملة", expanded=True):
        st.write(item_details)
        if st.button("اغلاق التفاصيل ❌"):
            del st.query_params["item"]
            st.rerun()

if st.button("تسجيل خروج", key="logout_btn"):
    st.session_state.auth = False
    st.rerun()

