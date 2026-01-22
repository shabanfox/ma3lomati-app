<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>معلوماتي العقارية - تفاصيل المشروعات</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color: #0f172a;
            --accent-color: #d4af37;
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #1e293b;
        }

        body {
            font-family: 'Cairo', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 20px;
        }

        .container {
            max-width: 1100px;
            margin: 0 auto;
        }

        .main-title {
            text-align: center;
            color: var(--primary-color);
            margin-bottom: 40px;
            border-bottom: 3px solid var(--accent-color);
            display: inline-block;
            padding-bottom: 10px;
        }

        /* حاوية المشاريع */
        #projects-container {
            display: flex;
            flex-direction: column;
            gap: 40px;
        }

        /* بطاقة المشروع الكبيرة */
        .project-section {
            background: var(--card-bg);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
        }

        /* رأس بطاقة المشروع */
        .project-header {
            background: var(--primary-color);
            color: white;
            padding: 20px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .project-header h2 { margin: 0; font-size: 1.5rem; }
        .developer-tag { background: var(--accent-color); color: #000; padding: 5px 15px; border-radius: 8px; font-weight: bold; }

        /* شبكة التفاصيل */
        .details-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1px;
            background: #e2e8f0; /* لون الخطوط الفاصلة */
        }

        .detail-item {
            background: white;
            padding: 20px;
            text-align: center;
        }

        .label {
            display: block;
            color: #64748b;
            font-size: 0.9rem;
            margin-bottom: 8px;
        }

        .value {
            display: block;
            font-weight: bold;
            color: var(--primary-color);
            font-size: 1.1rem;
        }

        /* تمييز السعر ونظام السداد */
        .highlight-price { color: #16a34a !important; }
        .payment-box {
            grid-column: 1 / -1;
            background: #fffbeb;
            border-top: 2px dashed var(--accent-color);
        }

        @media (max-width: 768px) {
            .project-header { flex-direction: column; text-align: center; gap: 10px; }
        }
    </style>
</head>
<body>

<div class="container">
    <center><h1 class="main-title">دليل المشروعات العقارية</h1></center>
    
    <div id="projects-container">
        </div>
</div>

<script>
    // البيانات التي قدمتها أنت
    const projectsData = [
        { dev: "La Vista", region: "العاصمة الإدارية", name: "La Vista City", price: "17.95M", payment: "10 Years (Equal)", units: "Villas Only", finishing: "Semi Finished" },
        { dev: "City Edge", region: "التجمع الخامس", name: "Lush Valley", price: "5.67M", payment: "8 Years (5%+5%)", units: "Apts, Loft, Mansio", finishing: "Semi Finished" },
        { dev: "HDP", region: "التجمع السادس", name: "Grand Lane", price: "3.5M", payment: "Up to 10 Years", units: "Apts & Villas", finishing: "Semi Finished" },
        { dev: "Waterway", region: "التجمع السادس", name: "Waterway East", price: "65k/Meter", payment: "9 Years (10% DP)", units: "Apts (G+7)", finishing: "Flexi Finished" },
        { dev: "Taj Misr", region: "العاصمة (CBD)", name: "Taj Tower 2", price: "4.8M", payment: "Up to 10 Years", units: "Admin (Offices)", finishing: "Fully Finished" },
        { dev: "Orascom", region: "6 أكتوبر", name: "O Views", price: "7.6M", payment: "10 Years (5% DP)", units: "Sky House, Villas", finishing: "High-end" },
        { dev: "People&Places", region: "نيو زايد", name: "Hills of One", price: "17.96M", payment: "10 Years (5% DP)", units: "3BD + Garden", finishing: "Fully Finished" }
    ];

    const container = document.getElementById('projects-container');

    // دالة بناء العناصر
    projectsData.forEach(project => {
        const card = `
            <div class="project-section">
                <div class="project-header">
                    <h2>${project.name}</h2>
                    <span class="developer-tag">${project.dev}</span>
                </div>
                <div class="details-grid">
                    <div class="detail-item">
                        <span class="label">📍 المنطقة</span>
                        <span class="value">${project.region}</span>
                    </div>
                    <div class="detail-item">
                        <span class="label">💰 سعر البداية</span>
                        <span class="value highlight-price">${project.price}</span>
                    </div>
                    <div class="detail-item">
                        <span class="label">🏢 أنواع الوحدات</span>
                        <span class="value">${project.units}</span>
                    </div>
                    <div class="detail-item">
                        <span class="label">🏗️ التشطيب</span>
                        <span class="value">${project.finishing}</span>
                    </div>
                    <div class="detail-item payment-box">
                        <span class="label">💳 نظام السداد</span>
                        <span class="value">${project.payment}</span>
                    </div>
                </div>
            </div>
        `;
        container.innerHTML += card;
    });
</script>

</body>
</html>
