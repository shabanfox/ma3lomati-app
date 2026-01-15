<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BrokerEdge | مساعد البروكر الذكي</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Cairo', sans-serif; }
    </style>
</head>
<body class="bg-gray-50">

    <nav class="bg-white shadow-sm py-4 px-8 flex justify-between items-center sticky top-0 z-50">
        <div class="text-2xl font-bold text-blue-900">Broker<span class="text-blue-500">Edge</span></div>
        <div class="hidden md:flex space-x-reverse space-x-8 text-gray-600 font-medium">
            <a href="#" class="hover:text-blue-600">المشاريع</a>
            <a href="#" class="hover:text-blue-600">المطورين</a>
            <a href="#" class="hover:text-blue-600">خارطة السوق</a>
            <a href="#" class="hover:text-blue-600 text-red-500 underline">عروض حصرية</a>
        </div>
        <button class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition">دخول البروكر</button>
    </nav>

    <header class="bg-blue-900 py-16 px-4 text-center text-white">
        <h1 class="text-3xl md:text-4xl font-bold mb-4">كل داتا السوق في جيبك</h1>
        <p class="text-blue-200 mb-8">ابحث عن المشاريع، قارن المطورين، واحصل على "الزتونة" فوراً.</p>
        
        <div class="max-w-4xl mx-auto bg-white rounded-xl shadow-2xl p-2 flex flex-wrap md:flex-nowrap gap-2">
            <input type="text" placeholder="اسم المطور أو المشروع..." class="flex-grow p-4 text-gray-800 focus:outline-none rounded-lg">
            <select class="p-4 text-gray-600 border-r border-gray-100 focus:outline-none">
                <option>كل المناطق</option>
                <option>التجمع الخامس</option>
                <option>الشيخ زايد</option>
                <option>العاصمة الإدارية</option>
            </select>
            <button class="bg-blue-600 w-full md:w-auto px-8 py-4 rounded-lg font-bold hover:bg-blue-700 transition">بحث سريع</button>
        </div>
    </header>

    <main class="max-w-7xl mx-auto py-12 px-4">
        
        <section class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
            <div class="bg-white p-6 rounded-xl shadow-sm border-r-4 border-blue-500">
                <h3 class="text-gray-500 text-sm">مشاريع تم تحديثها اليوم</h3>
                <p class="text-2xl font-bold text-gray-800">12 مشروع</p>
            </div>
            <div class="bg-white p-6 rounded-xl shadow-sm border-r-4 border-green-500">
                <h3 class="text-gray-500 text-sm">أفضل عمولة حالية</h3>
                <p class="text-2xl font-bold text-gray-800">8% (مشروع X)</p>
            </div>
            <div class="bg-white p-6 rounded-xl shadow-sm border-r-4 border-orange-500">
                <h3 class="text-gray-500 text-sm">أقل مقدم متاح</h3>
                <p class="text-2xl font-bold text-gray-800">0% مقدم</p>
            </div>
        </section>

        <h2 class="text-2xl font-bold mb-6 text-gray-800">أحدث داتا المشاريع</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div class="bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-md transition">
                <div class="h-48 bg-gray-200 bg-cover bg-center" style="background-image: url('https://via.placeholder.com/400x300')"></div>
                <div class="p-6">
                    <div class="flex justify-between items-start mb-2">
                        <span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">التجمع الخامس</span>
                        <span class="text-green-600 font-bold text-sm">عمولة: 4%</span>
                    </div>
                    <h3 class="text-xl font-bold mb-2">ماونتن فيو آي سيتي</h3>
                    <p class="text-gray-500 text-sm mb-4">المطور: ماونتن فيو (MV)</p>
                    <div class="border-t pt-4 flex justify-between items-center">
                        <span class="font-bold text-blue-600">يبدأ من 7.5M</span>
                        <button class="text-blue-500 hover:underline text-sm font-bold">عرض ملف الـ PDF</button>
                    </div>
                </div>
            </div>
            </div>
    </main>

</body>
</html>
