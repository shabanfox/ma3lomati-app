import streamlit as st
import pandas as pd

# 1. إعداد الصفحة (إخفاء كل عناصر ستريمليت)
st.set_page_config(page_title="BrokerEdge | ابحث عن منزلك", layout="wide")

st.markdown("""
    <style>
    /* إخفاء القوائم والماركات الخاصة بـ Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 0rem; padding-bottom: 0rem;}
    
    /* تصميم الخط والخلفية */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        background-color: #ffffff;
    }

    /* تصميم الـ Header */
    .nawy-header {
        background: white;
        padding: 15px 50px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #f0f0f0;
        position: sticky;
        top: 0;
        z-index: 999;
    }

    /* الـ Hero Section */
    .hero {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-position: center;
        height: 450px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        text-align: center;
    }

    /* شريط البحث النظيف */
    .search-container {
        background: white;
        padding: 10px;
        border-radius: 50px;
        display: flex;
        width: 70%;
        margin-top: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الهيدر (Navigation) ---
st.markdown("""
    <div class="nawy-header">
        <div style="font-size: 24px; font-weight: bold; color: #00416b;">Broker<span style="color: #ed1c24;">Edge</span></div>
        <div style="display: flex; gap: 30px; color: #333; font-weight: 600;">
            <span>المشاريع</span>
            <span>المطورين</span>
            <span>الاستلام الفوري</span>
        </div>
        <button style="background: #00416b; color: white; border: none; padding: 10px 25px; border-radius: 5px; cursor: pointer;">دخول</button>
    </div>
    """, unsafe_allow_html=True)

# --- 3. الـ Hero Section ---
st.markdown("""
    <div class="hero">
        <h1 style="font-size: 45px; font-weight: 700;">دليلك الأول لكل مشاريع مصر</h1>
        <p style="font-size: 20px;">احصل على "الزتونة" فوراً وشاركها مع عميلك</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. منطقة البحث الحقيقية (بأدوات ستريمليت لكن داخل حاوية) ---
col_s1, col_s2, col_s3 = st.columns([3, 1, 1])
with col_s1:
    search_q = st.text_input("", placeholder="ابحث عن مشروع، منطقة، أو مطور...")
with col_s2:
    st.selectbox("", ["كل المناطق", "التجمع الخامس", "الشيخ زايد", "العاصمة"])
with col_s3:
    if st.button("ابحث"):
        pass

# --- 5. عرض المشاريع (Nawy Cards) ---
st.markdown('<h2 style="padding: 20px 50px;">أحدث المشاريع</h2>', unsafe_allow_html=True)

# بيانات تجريبية (تستبدلها بملف الإكسيل لاحقاً)
dummy_data = [
    {"title": "Oia Residence", "dev": "Edge Stone", "loc": "New Capital", "price": "6,500,000", "img": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=500&q=80"},
    {"title": "Mountain View", "dev": "MV", "loc": "New Cairo", "price": "8,200,000", "img": "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=500&q=80"},
    {"title": "The Waterway", "dev": "Waterway", "loc": "New Cairo", "price": "12,000,000", "img": "https://images.unsplash.com/photo-1574362848149-11496d93a7c7?w=500&q=80"}
]

c_cols = st.columns(3)
for i, item in enumerate(dummy_data):
    with c_cols[i % 3]:
        st.markdown(f"""
            <div style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border
