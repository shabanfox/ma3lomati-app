import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati Inventory", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق (CSS) لمحاكاة ستايل نوي للوحدات
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right; background-color: #f8f9fa; }
    header, [data-testid="stHeader"] { visibility: hidden; }

    /* تصميم كارت الوحدة (Nawy Unit Style) */
    div.stButton > button[key*="unit_"] {
        background-color: white !important;
        border: 1px solid #eee !important;
        border-radius: 15px !important;
        width: 100% !important;
        min-height: 280px !important;
        padding: 0px !important;
        transition: 0.3s !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02) !important;
    }

    div.stButton > button[key*="unit_"]:hover {
        box-shadow: 0 10px 20px rgba(0,0,0,0.08) !important;
        border-color: #f59e0b !important;
        transform: translateY(-5px) !important;
    }

    /* تنسيق المحتوى داخل الزرار */
    .unit-badge { background: #f3f4f6; color: #666; font-size: 10px; padding: 2px 8px; border-radius: 4px; display: inline-block; margin-bottom: 5px; }
    .unit-ready { background: #ecfdf5; color: #10b981; font-size: 10px; padding: 2px 8px; border-radius: 4px; display: inline-block; }
    .unit-title { color: #003049; font-weight: 700; font-size: 16px; margin: 5px 0; }
    .unit-loc { color: #888; font-size: 12px; margin-bottom: 10px; }
    .unit-info-row { display: flex; justify-content: space-around; border-top: 1px solid #f0f0f0; border-bottom: 1px solid #f0f0f0; padding: 10px 0; margin: 10px 0; }
    .unit-spec { text-align: center; font-size: 11px; color: #444; }
    .unit-price { color: #003049; font-weight: 900; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

# 3. بيانات تجريبية (Inventory Data)
data = [
    {"id": 1, "type": "إعادة بيع", "status": "جاهز للتسليم", "loc": "سيدي عبد الرحمن", "project": "فيدا مراسي مارينا ،شقة", "beds": 2, "baths": 2, "area": 156, "price": "75,000,000"},
    {"id": 2, "type": "إعادة بيع", "status": "جاهز للتسليم", "loc": "سيدي عبد الرحمن", "project": "فيدا مراسي مارينا ،شقة", "beds": 1, "baths": 2, "area": 113, "price": "51,500,000"},
    {"id": 3, "type": "إعادة بيع", "status": "تحت الإنشاء", "loc": "القاهرة الجديدة", "project": "زيد ايست ،شقة", "beds": 3, "baths": 3, "area": 185, "price": "12,000,000"}
]

# 4. العرض (60% يمين)
main_col, _ = st.columns([0.6, 0.4])

with main_col:
    st.markdown("<h2 style='color:#003049;'>المشاريع المتاحة</h2>", unsafe_allow_html=True)
    
    # شبكة العروض (2 في كل صف)
    for i in range(0, len(data), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(data):
                item = data[i+j]
                with cols[j]:
                    # بناء النص داخل الزرار (Label)
                    # بنستخدم HTML بسيط داخل الزرار لو Streamlit سمح أو بنحاكي الشكل بالـ Label
                    content = f"""
                    {item['type']} | {item['status']}
                    {item['loc']}
                    {item['project']}
                    🛏️ {item['beds']} غرف | 🛁 {item['baths']} حمام | 📐 {item['area']}م²
                    {item['price']} جم
                    """
                    
                    # الزرار اللي شايل التصميم
                    if st.button(content, key=f"unit_{item['id']}"):
                        st.session_state.selected_unit = item
                        st.write(f"تم اختيار: {item['project']}")
