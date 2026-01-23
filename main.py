import streamlit as st

# إعدادات الصفحة
st.set_page_config(page_title="معلوماتي العقارية", layout="centered")

# إضافة تنسيق CSS مخصص لتحسين شكل البطاقات
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .project-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-right: 5px solid #b4912d;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        direction: rtl;
    }
    .label { color: #666; font-size: 0.8rem; }
    .value { color: #111; font-weight: bold; font-size: 1.1rem; }
    .price { color: #27ae60; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("📂 تفاصيل المشروعات")

# البيانات
projects = [
    {"dev": "La Vista", "region": "العاصمة الإدارية", "name": "La Vista City", "price": "17.95M", "pay": "10 Years", "units": "Villas Only", "finish": "Semi Finished"},
    {"dev": "City Edge", "region": "التجمع الخامس", "name": "Lush Valley", "price": "5.67M", "pay": "8 Years", "units": "Apts, Loft", "finish": "Semi Finished"},
    {"dev": "HDP", "region": "التجمع السادس", "name": "Grand Lane", "price": "3.5M", "pay": "Up to 10 Years", "units": "Apts & Villas", "finish": "Semi Finished"}
]

# عرض البيانات بتقسيم احترافي
for p in projects:
    with st.container():
        # كود HTML داخل Streamlit لعرض التقسيم الجديد
        st.markdown(f"""
        <div class="project-card">
            <h2 style='color: #1a237e; margin-bottom: 5px;'>{p['name']}</h2>
            <p style='color: #b4912d; font-weight: bold; margin-bottom: 15px;'>المطور: {p['dev']}</p>
            <hr>
            <table style='width: 100%; border-collapse: collapse;'>
                <tr>
                    <td style='width: 50%; padding: 10px;'>
                        <span class="label">📍 المنطقة</span><br>
                        <span class="value">{p['region']}</span>
                    </td>
                    <td style='padding: 10px;'>
                        <span class="label">🏗️ التشطيب</span><br>
                        <span class="value">{p['finish']}</span>
                    </td>
                </tr>
                <tr>
                    <td style='padding: 10px;'>
                        <span class="label">📏 الوحدات</span><br>
                        <span class="value">{p['units']}</span>
                    </td>
                    <td style='padding: 10px;'>
                        <span class="label">💰 السعر</span><br>
                        <span class="value price">{p['price']}</span>
                    </td>
                </tr>
            </table>
            <div style='background: #f0f9ff; padding: 10px; border-radius: 8px; margin-top: 10px; text-align: center;'>
                <span class="label">💳 نظام السداد:</span> 
                <span class="value">{p['pay']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
