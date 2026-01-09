import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }

    /* تصميم الكروت الرئيسية في الصفحة الأولى */
    .main-gate-card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        transition: 0.3s ease;
        height: 280px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .main-gate-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }
    
    .card-companies { border-top: 10px solid #001a33; }
    .card-tools { border-top: 10px solid #f59e0b; } /* لون ذهبي للأدوات */

    .gate-icon { font-size: 3.5rem; margin-bottom: 15px; }
    .gate-title { font-size: 1.8rem; font-weight: 900; color: #001a33; margin: 0; }
    .gate-desc { color: #64748b; font-size: 0.9rem; margin-top: 10px; }

    /* الهيدر الموحد لصفحة المحتوى */
    .hero-section {
        background: linear-gradient(135deg, #001a33 0%, #1e3a8a 100%);
        padding: 25px; border-radius: 0 0 20px 20px;
        margin-bottom: 20px; color: white;
    }

    /* الكروت الصغيرة (9 كروت) */
    .nano-card {
        background: white; border: 1px solid #cbd5e1; border-right: 6px solid #001a33;
        border-radius: 10px; padding: 12px; margin-bottom: 8px; min-height: 115px;
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .c-dev { color: #000; font-size: 1.1rem; font-weight: 900; }
    .c-price { color: #15803d; font-size: 1.1rem; font-weight: 900; }
    </style>
""", unsafe_allow_html=True)

# دالة تحميل البيانات
@st.cache_data
def get_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        return df
    except: return None

df = get_data()

# إدارة التنقل
if 'view_state' not in st.session_state: st.session_state.view_state = 'landing'

if df is not None:
    # --- الصفحة الرئيسية: البوابة ---
    if st.session_state.view_state == 'landing':
        st.markdown("<h1 style='text-align:center; color:#001a33; margin:40px 0; font-weight:900;'>🏠 منصة معلوماتى العقارية للبروكرز</h1>", unsafe_allow_html=True)
        
        # توزيع الكروت بجانب بعضها
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div class="main-gate-card card-companies">
                    <div class="gate-icon">🏢</div>
                    <div class="gate-title">الشركات</div>
                    <div class="gate-desc">دليل المطورين والمشاريع والتحليلات الفنية</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("فتح قسم الشركات", use_container_width=True):
                st.session_state.view_state = 'browse_companies'
                st.rerun()

        with col2:
            st.markdown("""
                <div class="main-gate-card card-tools">
                    <div class="gate-icon">🛠️</div>
                    <div class="gate-title">أدوات البروكر</div>
                    <div class="gate-desc">الحاسبات المالية، النماذج، وأدوات المساعدة اليومية</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("فتح أدوات البروكر", use_container_width=True):
                st.session_state.view_state = 'broker_tools'
                st.rerun()

    # --- صفحة الشركات (التي صممناها سابقاً) ---
    elif st.session_state.view_state == 'browse_companies':
        st.markdown('<div class="hero-section">', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"):
            st.session_state.view_state = 'landing'; st.rerun()
        st.markdown('<h2 style="text-align:center; margin:0; color:white;">🔍 دليل الشركات والمشاريع</h2>', unsafe_allow_html=True)
        # ... هنا يتم وضع كود الفلاتر والـ 9 كروت الذي اعتمدناه سابقاً ...
        st.info("قسم الشركات قيد العرض الآن (التصميم المعتمد 9 كروت)")

    # --- صفحة أدوات البروكر (القسم الجديد) ---
    elif st.session_state.view_state == 'broker_tools':
        st.markdown('<div class="hero-section" style="background: #f59e0b;">', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"):
            st.session_state.view_state = 'landing'; st.rerun()
        st.markdown('<h2 style="text-align:center; margin:0; color:white;">🛠️ أدوات البروكر المحترف</h2>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # محتوى تجريبي لأدوات البروكر
        t1, t2, t3 = st.columns(3)
        with t1:
            st.success("🧮 حاسبة الأقساط")
        with t2:
            st.warning("📄 نماذج عقود")
        with t3:
            st.info("🔗 روابط التحقق")
