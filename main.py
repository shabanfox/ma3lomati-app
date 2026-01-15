import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np

# إعداد الصفحة
st.set_page_config(page_title="BrokerEdge Dashboard", layout="wide")

# 1. تصميم الواجهة (CSS & HTML)
html_header = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Cairo', sans-serif; background-color: #f8fafc; }
        .gradient-bg { background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%); }
    </style>
</head>
<body>
    <nav class="bg-white shadow-sm py-4 px-8 flex justify-between items-center">
        <div class="text-2xl font-bold text-blue-900">Broker<span class="text-blue-500">Edge</span></div>
        <div class="flex gap-4">
            <span class="text-gray-500 text-sm">مرحباً، يا بروكر! 👋</span>
        </div>
    </nav>
    <div class="gradient-bg py-10 px-6 text-white text-center">
        <h1 class="text-3xl font-bold">لوحة تحكم الزتونة 🚀</h1>
        <p class="opacity-80">بيانات السوق اللحظية بين يديك</p>
    </div>
</body>
</html>
"""

# عرض الهيدر
components.html(html_header, height=250)

# 2. قسم الإحصائيات (الرسوم البيانية)
st.subheader("📊 نبض السوق (متوسط سعر المتر 2026)")

# بيانات تجريبية للرسم البياني
chart_data = pd.DataFrame({
    'المنطقة': ['التجمع الخامس', 'الشيخ زايد', 'العاصمة الإدارية', 'المستقبل سيتي', 'الساحل الشمالي'],
    'سعر المتر (جنيه)': [45000, 42000, 35000, 31000, 55000]
})
st.bar_chart(chart_data.set_index('المنطقة'))

# 3. قسم جدول المشاريع الذكي
st.markdown("---")
st.subheader("🏢 قاعدة بيانات المشاريع الحالية")

# بيانات تجريبية للجداول
data = {
    "المشروع": ["Mountain View iCity", "Badya", "The Waterway", "Zed East", "Oia Residence"],
    "المطور": ["Mountain View", "Palm Hills", "Waterway", "Ora Developers", "Edge Stone"],
    "المنطقة": ["التجمع الخامس", "أكتوبر", "التجمع الخامس", "التجمع الخامس", "العاصمة الإدارية"],
    "أقل مقدم": ["10%", "0%", "15%", "5%", "10%"],
    "سنوات القسط": [8, 10, 5, 8, 9],
    "حالة السعر": ["📈 مرتفع", "🟢 ثابت", "📈 مرتفع", "🟡 تذبذب", "🟢 ثابت"]
}

df = pd.DataFrame(data)

# إضافة فلاتر في الجنب (Sidebar)
st.sidebar.header("تصفية البحث")
selected_region = st.sidebar.multiselect("اختر المنطقة", df["المنطقة"].unique(), default=df["المنطقة"].unique())
selected_dev = st.sidebar.selectbox("اختر المطور", ["الكل"] + list(df["المطور"].unique()))

# تصفية البيانات بناءً على الاختيار
filtered_df = df[df["المنطقة"].isin(selected_region)]
if selected_dev != "الالكل":
    filtered_df = filtered_df[filtered_df["المطور"] == selected_dev]

# عرض الجدول بشكل احترافي
st.table(filtered_df)

# 4. ميزة "زرار الزتونة" للبروكر
st.markdown("---")
st.subheader("🛠️ أدوات البروكر السريعة")
col1, col2 = st.columns(2)

with col1:
    if st.button("📄 إنشاء بروشور باسمي (Coming Soon)"):
        st.info("هذه الميزة ستقوم بربط بيانات المشروع بلوجو مكتبك تلقائياً.")

with col2:
    if st.button("💰 حاسبة القسط السريع"):
        st.write("حاسبة مخصصة لأنظمة سداد المطورين المعقدة.")
