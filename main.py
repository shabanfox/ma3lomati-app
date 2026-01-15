import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لجعلها عريضة وشيك
st.set_page_config(page_title="BrokerEdge | لوحة التحكم", layout="wide")

# 1. تصميم الـ UI الاحترافي باستخدام Tailwind داخل كود بايثون
def local_css():
    st.markdown("""
    <style>
    /* إخفاء عناصر streamlit الافتراضية لزيادة الشياكة */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background-color: #1e3a8a;
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #3b82f6;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# هيدر المنصة بتصميم عصري
html_header = """
<div dir="rtl" style="font-family: 'Cairo', sans-serif; background: linear-gradient(90deg, #0f172a 0%, #1e3a8a 100%); padding: 40px; border-radius: 20px; text-align: center; color: white; margin-bottom: 30px;">
    <h1 style="font-size: 35px; font-weight: bold; margin-bottom: 10px;">BrokerEdge Dashboard</h1>
    <p style="font-size: 18px; opacity: 0.8;">أداة المساعد الذكي للبروكر المحترف - بيانات السوق لحظة بلحظة</p>
</div>
"""
st.markdown(html_header, unsafe_allow_html=True)

# 2. منطقة الفلاتر العلوية (Horizontal Filters)
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.selectbox("📍 المنطقة", ["كل المناطق", "التجمع الخامس", "الشيخ زايد", "العاصمة الإدارية", "الساحل الشمالي"])
with col_f2:
    st.selectbox("🏗️ المطور", ["كل المطورين", "إعمار", "سوديك", "ماونتن فيو", "بالم هيلز"])
with col_f3:
    st.select_slider("💰 نطاق السعر (مليون)", options=[5, 10, 15, 20, 50], value=(5, 20))

st.markdown("---")

# 3. عرض المشاريع بنظام الـ Cards (هنا الزتونة في الشكل)
st.subheader("🏢 أهم المشاريع المتاحة الآن")

# مصفوفة بيانات تجريبية (التي ستستبدلها لاحقاً بالإكسيل)
projects = [
    {"name": "Mountain View iCity", "dev": "MV", "loc": "التجمع الخامس", "price": "7.2M", "comm": "4%", "img": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=400&q=80"},
    {"name": "Marassi", "dev": "Emaar", "loc": "الساحل الشمالي", "price": "15.5M", "comm": "3.5%", "img": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=400&q=80"},
    {"name": "Badya", "dev": "Palm Hills", "loc": "أكتوبر الجديدة", "price": "6.1M", "comm": "5%", "img": "https://images.unsplash.com/photo-1515263487990-61b0082665d1?w=400&q=80"},
    {"name": "Zed East", "dev": "Ora Developers", "loc": "القاهرة الجديدة", "price": "9.8M", "comm": "4%", "img": "https://images.unsplash.com/photo-1574362848149-11496d93a7c7?w=400&q=80"},
]

# تقسيم العرض لـ 2 كروت في كل صف
cols = st.columns(2)

for i, project in enumerate(projects):
    with cols[i % 2]:
        card_html = f"""
        <div dir="rtl" style="background: white; border-radius: 15px; padding: 0px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); overflow: hidden; border: 1px solid #f0f0f0; transition: 0.3s;">
            <img src="{project['img']}" style="width: 100%; height: 200px; object-fit: cover;">
            <div style="padding: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="background: #e0f2fe; color: #0369a1; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;">{project['loc']}</span>
                    <span style="color: #059669; font-weight: bold; font-size: 14px;">عمولة: {project['comm']}</span>
                </div>
                <h3 style="margin: 0; font-size: 20px; color: #1e293b; font-weight: bold;">{project['name']}</h3>
                <p style="color: #64748b; font-size: 14px; margin: 5px 0 15px 0;">المطور: {project['dev']}</p>
                <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #f1f5f9; pt: 15px; padding-top: 10px;">
                    <div style="font-size: 18px; color: #1e3a8a; font-weight: bold;">{project['price']}</div>
                    <a href="#" style="text-decoration: none; background: #f1f5f9; color: #475569; padding: 8px 15px; border-radius: 8px; font-size: 12px; font-weight: bold;">تفاصيل الزتونة ←</a>
                </div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

# 4. زرار "أدوات البروكر" السريع في الجنب
st.sidebar.markdown("### 🛠️ أدوات سريعة")
st.sidebar.button("🖨️ تحميل عرض سعر PDF")
st.sidebar.button("🔗 مشاركة للواتساب")
st.sidebar.button("📉 مقارنة بين مشروعين")
