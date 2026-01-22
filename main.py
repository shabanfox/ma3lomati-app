<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تفاصيل العقارات</t
    <style>
        body {
            font-family: sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 10px;
        }

        .card {
            background: white;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
            border: 1px solid #eee;
        }

        .card-title {
            background: #2c3e50;
            color: white;
            padding: 15px;
            margin: 0;
            font-size: 18px;
            text-align: center;
        }

        .detail-row {
            display: flex;
            justify-content: space-between;
            padding: 12px 15px;
            border-bottom: 1px solid #f9f9f9;
        }

        .label {
            color: #7f8c8d;
            font-weight: bold;
            font-size: 14px;
        }

        .value {
            color: #2c3e50;
            font-weight: bold;
            font-size: 14px;
            text-align: left;
        }

        .price-box {
            background: #eafaf1;
            padding: 10px;
            text-align: center;
            border-top: 1px solid #d5f5e3;
        }

        .price-value {
            color: #27ae60;
            font-size: 18px;
            font-weight: bold;
        }

        .payment-info {
            background: #fef9e7;
            padding: 10px;
            font-size: 13px;
            color: #9c640c;
            text-align: center;
            border-top: 1px solid #fcf3cf;
        }
    </style>
</head>
<body>

<div id="content"></div>

<script>
    // هذه هي بياناتك مقسمة وجاهزة
    const projects = [
        { name: "La Vista City", dev: "La Vista", region: "العاصمة الإدارية", price: "17.95M", payment: "10 Years (Equal)", units: "Villas Only", finish: "Semi Finished" },
        { name: "Lush Valley", dev: "City Edge", region: "التجمع الخامس", price: "5.67M", payment: "8 Years (5%+5%)", units: "Apts, Loft, Mansio", finish: "Semi Finished" },
        { name: "Grand Lane", dev: "HDP", region: "التجمع السادس", price: "3.5M", payment: "Up to 10 Years", units: "Apts & Villas", finish: "Semi Finished" }
    ];

    const container = document.getElementById('content');

    projects.forEach(p => {
        container.innerHTML += `
            <div class="card">
                <h2 class="card-title">${p.name}</h2>
                <div class="detail-row">
                    <span class="label">المطور:</span>
                    <span class="value">${p.dev}</span>
                </div>
                <div class="detail-row">
                    <span class="label">المنطقة:</span>
                    <span class="value">${p.region}</span>
                </div>
                <div class="detail-row">
                    <span class="label">نوع الوحدات:</span>
                    <span class="value">${p.units}</span>
                </div>
                <div class="detail-row">
                    <span class="label">التشطيب:</span>
                    <span class="value">${p.finish}</span>
                </div>
                <div class="price-box">
                    <span class="label">يبدأ من: </span>
                    <span class="price-value">${p.price}</span>
                </div>
                <div class="payment-info">
                    💳 نظام السداد: ${p.payment}
                </div>
            </div>
        `;
    });
</script>

</body>
</html>
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


