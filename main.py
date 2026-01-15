import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة - المحافظة على التصميم العريض
st.set_page_config(page_title="EstatePro AI", layout="wide")

# CSS لاستعادة التصميم السابق (الخطوط والألوان)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    /* خلفية الموقع الأصلية */
    .stApp {
        background-color: #0F172A; /* اللون الكحلي الداكن الأصلي */
    }
    
    /* تصميم الكروت (المشاريع) */
    .project-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 20px;
        color: white;
        margin-bottom: 15px;
    }

    /* إخفاء الهوامش الافتراضية لستريمليت */
    header {visibility: hidden;}
    .block-container {padding-top: 2rem;}
</style>
""", unsafe_allow_html=True)

# 1. الهيدر (بنفس شكل المنصة السابق)
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 20px; background: #1E293B; border-radius: 20px; margin-bottom: 30px; border: 1px solid #334155;">
        <h1 style="color: white; font-weight: 900; margin: 0;">ESTATE<span style="color: #3B82F6;">PRO</span></h1>
        <div style="color: #94A3B8;">لوحة التحكم العقارية | 2026</div>
    </div>
""", unsafe_allow_html=True)

# 2. التقسيم (70% محتوى المنصة - 30% قائمة المطورين)
col_main, col_devs = st.columns([0.7, 0.3], gap="large")

with col_main:
    # --- هنا تضع محتوى المنصة السابق (الخرائط، المشاريع، الخ) ---
    st.markdown("<h2 style='color: white;'>🏠 المحتوى الرئيسي</h2>", unsafe_allow_html=True)
    
    # مثال لكروت المشاريع بنفس الستايل القديم
    for i in range(2):
        st.markdown(f"""
        <div class="project-card">
            <h3 style="color: #3B82F6; margin-top:0;">مشروع سكني مميز #{i+1}</h3>
            <p style="color: #CBD5E1; font-size: 14px;">هذا النص يمثل وصف المشروع في المنصة، حيث يتم عرض التفاصيل والموقع والسعر بناءً على التصميم المعتمد.</p>
            <div style
