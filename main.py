import streamlit as st
import pandas as pd
import urllib.parse
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide")

# 2. هندسة الألوان والتصميم (ألوان صريحة وخطوط واضحة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* الخلفية والنصوص الأساسية */
    [data-testid="stAppViewContainer"] {
        background-color: #000000;
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Cairo', sans-serif;
    }
    
    /* العناوين والخطوط */
    h1, h2, h3 { color: #FFD700 !important; font-weight: 900 !important; }
    p, span, label { color: #FFFFFF !important; font-size: 18px !important; font-weight: 500; }
    
    /* ستايل كروت اللونشات (ألوان نيون واضحة) */
    .launch-card {
        background: #111111;
        border: 2px solid #FFD700;
        border-right: 15px solid #FFD700;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    
    /* صناديق المعلومات */
    .info-box {
        background: #1A1A1A;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 10px;
        color: #00FF00 !important; /* لون أخضر فاقع للمبالغ المادية */
        font-weight: bold;
        font-size: 20px !important;
    }

    /* الأزرار - لون ذهبي واضح */
    .stButton button {
        background-color: #FFD700 !important;
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 20px !important;
        border-radius: 12px !important;
        height: 55px !important;
        border: none !important;
    }

    /* القائمة العلوية */
    .nav-link { font-size: 20px !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# 3. المنيو الرئيسي (الأقسام الأربعة)
selected = option_menu(
    menu_title=None,
    options=["اللونشات 🚀", "المشاريع 🏢", "المطورين 🏗️", "الأدوات 🛠️"],
    icons=["rocket-takeoff", "search", "building", "calculator"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#111"},
        "nav-link": {"color": "white", "font-size": "18px", "text-align": "center", "margin":"0px"},
        "nav-link-selected": {"background-color": "#FFD700", "color": "black"},
    }
)

# --- 4. محتوى الصفحات ---

if selected == "اللونشات 🚀":
    st.markdown("<h1>🚀 أهم اللونشات الحالية</h1>", unsafe_allow_html=True)
    
    # مثال لكارت لونش (كرر هذا الجزء مع الداتا)
    st.markdown("""
        <div class="launch-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h2>مشروع نايل تاور - العاصمة</h2>
                <span style="background:red; color:white; padding:5px 15px; border-radius:8px;">عاجل 🔥</span>
            </div>
            <p>🏗️ <b>المطور:</b> شركة النيل للتطوير العقاري</p>
            <p>📍 <b>الموقع:</b> داون تاون - العاصمة الإدارية</p>
            <div class="info-box">
                💰 مبلغ جدية الحجز (EOI): 50,000 ج.م (مسترد بالكامل)
            </div>
            <p style="color:#FFD700 !important; margin-top:10px;">💡 <b>نصيحة:</b> التركيز على المستثمرين الباحثين عن عائد إيجاري مضمون.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("📲 إرسال تفاصيل اللونش للعميل"):
        pass

elif selected == "المشاريع 🏢":
    st.markdown("<h1>🏢 محرك بحث المشاريع</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("اختر المنطقة", ["التجمع الخامس", "الشيخ زايد", "العاصمة الإدارية", "الساحل"])
    with col2:
        st.selectbox("نوع الوحدة", ["سكني", "تجاري", "إداري", "طبي"])
    st.button("🔍 ابحث الآن")

elif selected == "المطورين 🏗️":
    st.markdown("<h1>🏗️ موسوعة المطورين</h1>", unsafe_allow_html=True)
    st.text_input("🔍 ابحث عن اسم المطور...")
    # هنا يتم عرض كروت المطورين بالصور كما صممنا سابقاً

elif selected == "الأدوات 🛠️":
    st.markdown("<h1>🛠️ أدوات البروكر الذكية</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🧮 حاسبة الأقساط", "📊 مقارنة المطورين"])
    
    with tab1:
        price = st.number_input("سعر الوحدة", value=1000000)
        down_payment = st.slider("المقدم (%)", 0, 50, 10)
        years = st.slider("عدد السنوات", 1, 10, 7)
        calc_btn = st.button("احسب القسط")
        if calc_btn:
            total_dp = price * (down_payment/100)
            monthly = (price - total_dp) / (years * 12)
            st.success(f"المقدم المطلوب: {total_dp:,.0f} ج.م | القسط الشهري: {monthly:,.0f} ج.م")

