import streamlit as st
import pandas as pd
import urllib.parse
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide")

# 2. التنسيق (ألوان صريحة وخطوط واضحة جداً)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stAppViewContainer"] { background-color: #000000; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    h1, h2, h3 { color: #FFD700 !important; }
    p, span, label { color: #FFFFFF !important; font-size: 18px !important; }
    
    /* شريط الأخبار المتحرك */
    .news-ticker {
        background: #FFD700; color: black; padding: 10px; font-weight: bold;
        white-space: nowrap; overflow: hidden; position: relative; border-radius: 5px; margin-bottom: 20px;
    }
    .news-ticker p { display: inline-block; padding-left: 100%; animation: ticker 20s linear infinite; color: black !important; margin: 0; font-size: 20px !important; }
    @keyframes ticker { 0% { transform: translate(0, 0); } 100% { transform: translate(-100%, 0); } }

    /* كروت اللونشات والأدوات */
    .custom-card { background: #111; border: 2px solid #333; padding: 20px; border-radius: 15px; margin-bottom: 15px; border-right: 10px solid #FFD700; }
    .tool-box { background: #1A1A1A; border: 1px solid #FFD700; padding: 20px; border-radius: 15px; text-align: center; height: 180px; transition: 0.3s; }
    .tool-box:hover { background: #FFD700; }
    .tool-box:hover h3, .tool-box:hover p { color: black !important; }
    
    /* زر الخروج */
    .logout-btn { color: #ff4b4b !important; border: 1px solid #ff4b4b !important; border-radius: 5px; padding: 5px 10px; text-decoration: none; }
    </style>
""", unsafe_allow_html=True)

# 3. شريط الأخبار (تحديثات السوق)
st.markdown("""<div class="news-ticker"><p> 🔥 لونش شركة أورا الجديد في الشيخ زايد يبدأ غداً .. 🚀 ارتفاع أسعار المتر في التجمع الخامس بنسبة 10% .. 🏗️ تسليم المرحلة الأولى من مشروع ميفيدا .. </p></div>""", unsafe_allow_html=True)

# 4. القائمة العلوية وزر الخروج
col_nav, col_out = st.columns([9, 1])
with col_nav:
    selected = option_menu(
        menu_title=None,
        options=["اللونشات 🚀", "المشاريع 🏢", "المطورين 🏗️", "الأدوات 🛠️"],
        icons=["rocket-takeoff", "search", "building", "calculator"],
        orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#FFD700", "color": "black"}}
    )
with col_out:
    if st.button("🚪 خروج"):
        st.session_state.auth = False
        st.rerun()

# --- محتوى الصفحات ---

if selected == "اللونشات 🚀":
    st.markdown("<h1>🚀 رادار اللونشات الحالية</h1>", unsafe_allow_html=True)
    # هنا نضع كود عرض اللونشات من الشيت
    st.markdown('<div class="custom-card"><h2>لونش أورا - زايد الجديدة</h2><p>📍 الموقع: بجوار مطار سفنكس | 💰 الـ EOI: 100,000 ج.م</p></div>', unsafe_allow_html=True)

elif selected == "المشاريع 🏢":
    st.markdown("<h1>🏢 محرك بحث المشاريع الذكي</h1>", unsafe_allow_html=True)
    with st.expander("🔍 فلاتر البحث المتقدمة", expanded=True):
        c1, c2, c3 = st.columns(3)
        c1.selectbox("المنطقة", ["التجمع", "زايد", "العاصمة", "الساحل"])
        c2.selectbox("نوع الاستثمار", ["سكني", "تجاري", "إداري"])
        c3.slider("ميزانية المقدم (ج.م)", 100000, 5000000, 500000)
    st.button("🔍 عرض النتائج المطابقة")

elif selected == "المطورين 🏗️":
    st.markdown("<h1>🏗️ دليل المطورين المعتمدين</h1>", unsafe_allow_html=True)
    # عرض المطورين بشكل Grid
    cols = st.columns(2)
    for i in range(2):
        with cols[i]:
            st.markdown('<div class="custom-card"><h3>شركة إعمار مصر</h3><p>⭐ التقييم: A+ | 🏗️ سابقة الأعمال: ميفيدا، مراسي</p></div>', unsafe_allow_html=True)
            st.button(f"عرض الملف الكامل {i}", key=f"dev_{i}")

elif selected == "الأدوات 🛠️":
    st.markdown("<h1>🛠️ أدوات البروكر المحترف (6 أدوات)</h1>", unsafe_allow_html=True)
    
    t1, t2, t3 = st.columns(3)
    t4, t5, t6 = st.columns(3)
    
    with t1: st.markdown('<div class="tool-box"><h3>🧮</h3><h3>حاسبة القسط</h3><p>احسب الدفعات الشهرية</p></div>', unsafe_allow_html=True)
    with t2: st.markdown('<div class="tool-box"><h3>📈</h3><h3>حاسبة العائد ROI</h3><p>احسب مكسب العميل</p></div>', unsafe_allow_html=True)
    with t3: st.markdown('<div class="tool-box"><h3>📏</h3><h3>مقارنة المساحات</h3><p>صافي ونصف صافي</p></div>', unsafe_allow_html=True)
    with t4: st.markdown('<div class="tool-box"><h3>💱</h3><h3>محول العملات</h3><p>أسعار الذهب والدولار</p></div>', unsafe_allow_html=True)
    with t5: st.markdown('<div class="tool-box"><h3>📉</h3><h3>مقياس التضخم</h3><p>قيمة العقار السنوية</p></div>', unsafe_allow_html=True)
    with t6: st.markdown('<div class="tool-box"><h3>💬</h3><h3>رسائل الواتساب</h3><p>نماذج تسويق جاهزة</p></div>', unsafe_allow_html=True)

    # مثال لتفعيل أداة (تظهر عند الضغط)
    st.write("---")
    with st.expander("🛠️ افتح الأداة المختارة"):
        # هنا تضع كود كل أداة (مثال حاسبة القسط)
        st.number_input("أدخل سعر الوحدة")
        st.button("بدء الحساب")
