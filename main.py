<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>دليل العقارات المصري</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <style>
        :root {
            --primary-color: #2c3e50;
            --accent-color: #e74c3c;
            --bg-color: #f4f7f6;
            --text-color: #333;
        }

        body {
            font-family: 'Cairo', sans-serif;
            background-color: var(--bg-color);
            margin: 0;
            padding: 20px;
            color: var(--text-color);
        }

        header {
            text-align: center;
            margin-bottom: 40px;
        }

        /* خانة البحث */
        .search-container {
            max-width: 600px;
            margin: 0 auto 30px;
            position: relative;
        }

        .search-container input {
            width: 100%;
            padding: 15px 45px 15px 15px;
            border-radius: 30px;
            border: 2px solid #ddd;
            font-size: 16px;
            outline: none;
            box-sizing: border-box;
        }

        .search-container i {
            position: absolute;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            color: #888;
        }

        /* شبكة الكروت */
        .projects-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
            max-width: 1200px;
            margin: 0 auto;
        }

        /* تصميم الكارت */
        .project-card {
            background: #fff;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            transition: transform 0.3s ease;
            display: flex;
            flex-direction: column;
        }

        .project-card:hover {
            transform: translateY(-10px);
        }

        .project-image {
            width: 100%;
            height: 180px;
            background: #ddd url('https://via.placeholder.com/400x200?text=Project+Image') no-repeat center/cover;
        }

        .project-info {
            padding: 20px;
            flex-grow: 1;
        }

        .project-name {
            font-size: 1.3rem;
            margin: 0 0 10px 0;
            color: var(--primary-color);
        }

        .project-area {
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 5px;
        }

        /* الخانة المطلوبة: Detailed Location */
        .detailed-location {
            background: #fff5f4;
            border-right: 4px solid var(--accent-color);
            padding: 10px;
            font-size: 0.85rem;
            color: #555;
            margin-bottom: 15px;
            line-height: 1.6;
        }

        .detailed-location b {
            display: block;
            color: var(--accent-color);
            margin-bottom: 3px;
        }

        .card-footer {
            padding: 15px 20px;
            background: #fafafa;
            border-top: 1px solid #eee;
            display: flex;
            justify-content: space-between;
        }

        .btn {
            text-decoration: none;
            padding: 8px 15px;
            border-radius: 5px;
            font-size: 0.9rem;
            font-weight: bold;
        }

        .btn-details { background: var(--primary-color); color: white; }
        .btn-call { border: 1px solid var(--primary-color); color: var(--primary-color); }

    </style>
</head>
<body>

<header>
    <h1>منصة المشاريع العقارية</h1>
    <p>استعرض أكثر من 1000 مشروع في كافة أنحاء مصر</p>
</header>

<div class="search-container">
    <i class="fa fa-search"></i>
    <input type="text" id="searchInput" placeholder="ابحث باسم المشروع أو المنطقة..." onkeyup="filterProjects()">
</div>

<div class="projects-grid" id="projectsGrid">
    </div>

<script>
    // هذه هي البيانات التي تأتي من الشيت الخاص بك (مثال لـ 3 مشاريع)
    // يمكنك إضافة الـ 1000 مشروع هنا بنفس التنسيق
    const projects = [
        { name: "SouthMed", area: "الساحل الشمالي", location: "سيدي عبد الرحمن، الكيلو 165 طريق إسكندرية مطروح بجوار الضبعة." },
        { name: "Mivida", area: "القاهرة الجديدة", location: "التجمع الخامس، مباشرة على شارع التسعين الجنوبي بجوار الجامعة الأمريكية." },
        { name: "O West", area: "أكتوبر والشيخ زايد", location: "طريق الواحات، خلف مدينة الإنتاج الإعلامي ومول مصر." },
        { name: "Marassi", area: "الساحل الشمالي", location: "منطقة سيدي عبد الرحمن، الكيلو 125 طريق مطروح." },
        { name: "Il Bosco", area: "العاصمة الإدارية", location: "منطقة المستثمرين، مباشرة على محور بن زايد الجنوبي." }
    ];

    function displayProjects(data) {
        const grid = document.getElementById('projectsGrid');
        grid.innerHTML = ''; // مسح النتائج الحالية

        data.forEach(project => {
            const card = `
                <div class="project-card">
                    <div class="project-image"></div>
                    <div class="project-info">
                        <h2 class="project-name">${project.name}</h2>
                        <div class="project-area">
                            <i class="fa fa-map-marker-alt"></i> ${project.area}
                        </div>
                        <div class="detailed-location">
                            <b>الموقع بالتفصيل:</b>
                            ${project.location}
                        </div>
                    </div>
                    <div class="card-footer">
                        <a href="#" class="btn btn-details">التفاصيل</a>
                        <a href="tel:0123456789" class="btn btn-call">اتصل</a>
                    </div>
                </div>
            `;
            grid.innerHTML += card;
        });
    }

    // وظيفة البحث
    function filterProjects() {
        const term = document.getElementById('searchInput').value.toLowerCase();
        const filtered = projects.filter(p => 
            p.name.toLowerCase().includes(term) || 
            p.area.toLowerCase().includes(term)
        );
        displayProjects(filtered);
    }

    // تشغيل العرض عند فتح الصفحة
    displayProjects(projects);
</script>

</body>
</html>
