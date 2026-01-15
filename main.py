import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة
st.set_page_config(page_title="BrokerEdge", layout="wide")

# وضع كود الـ HTML اللي صممناه في متغير (String)
html_code = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Cairo', sans-serif; background-color: #f9fafb; }
    </style>
</head>
<body>
    <nav class="bg-white shadow-sm py-4 px-8 flex justify-between items-center">
        <div class="text-2xl font-bold text-blue-900">Broker<span class="text-blue-500">Edge</span></div>
        <button class="bg-blue-600 text-white px-6 py-2 rounded-lg">دخول البروكر</button>
    </nav>

    <header class="bg-blue-900 py-16 px-4 text-center text-white">
        <h1 class="text-3xl font-bold mb-4">كل داتا السوق في جيبك</h1>
        <p class="text-blue-200 mb-8">ابحث عن المشاريع، قارن المطورين، واحصل على الزتونة فوراً</p>
        
        <div class="max-w-4xl mx-auto bg-white rounded-xl p-2 flex gap-2">
            <input type="text" placeholder="اسم المطور أو المشروع..." class="flex-grow p-4 text-gray-800 outline-none">
            <button class="bg-blue-600 text-white px-8 py-4 rounded-lg font-bold">بحث سريع</button>
        </div>
    </header>

    <main class="max-w-7xl mx-auto py-12 px-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div class="bg-white p-6 rounded-xl shadow-sm border-r-4 border-blue-500 text-right">
                <h3 class="text-gray-500 text-sm">مشاريع تم تحديثها اليوم</h3>
                <p class="text-2xl font-bold">12 مشروع</p>
            </div>
        </div>
    </main>
</body>
</html>
"""

# تشغيل الكود داخل Streamlit
components.html(html_code, height=800, scrolling=True)
