import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="معلوماتى العقارية", layout="wide")

# 2. كود التصميم المحدث (الهيدر العالمي + الفلاتر)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    .block-container { padding: 0rem !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }

    /* الهيدر العلوي */
    .header-nav { 
        background: white; height: 70px; padding: 0 8%; display: flex; 
        justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e8f0; 
    }
    .logo-main { color: #003366; font-weight: 900; font-size: 1.8rem; }
    .logo-sub { color: #D4AF37; }

    /* هيدر الصورة العالمية الحيوية */
    .hero-bg {
        background-image: linear-gradient(rgba(0, 30, 60, 0.4), rgba(0, 30, 60, 0.4)), 
                        url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=2070&auto=format&fit=crop');
        background-size: cover; background-position: center; 
        height: 350px; display: flex; flex-direction: column; justify-content: center; align-items: center; 
        color: white; text-align: center;
    }
    .hero-text h1 { font-weight: 900; font-size: 3rem; margin: 0; text-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    .hero-text p { font-size: 1.2rem; opacity: 0.9; margin-top: 10px; }

    /* حاوية الفلاتر (نفس تصميم الصورة اللي عجبتك) */
    .filter-box {
        background: white; margin: -50px 10% 30px 10%; padding: 30px;
        border-radius: 15px; box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        position: relative; z-index: 10;
        border: 1px solid #edf2f7;
    }

    /* تصميم الكروت */
    .project-card { 
        background: white; border-radius: 16px; border: 1px solid #e2e8f0; 
        display: flex; height: 180px; margin: 20px 10%; overflow: hidden; 
        transition: 0.3s;
    }
    .project-card:hover { transform: translateY(-5px); box-shadow: 0 12px 20px rgba(0,0,0,0.05); }
    
    .card-img { 
        width: 280px; background-image: url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=500');
        background-size: cover; background-position: center; 
    }
    .card-body { padding: 25px; flex: 1; display: flex; flex-direction: column; justify-content: center; }
    .price-tag { color: #003366; font-weight: 900; font-size: 1.5rem; margin-bottom: 5px; }
    .dev-name { font-weight: 700; font-size: 1.3rem; color: #1e293b; }
    
    .btn-view { 
        background: #003366; color: white; border: none; padding: 12px 25px; 
        border-radius: 8px; font-weight: 700; cursor: pointer; transition: 0.2s;
    }
    .btn-view:hover { background: #004488; }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر
st.markdown('<div class="header-nav"><div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div><div style="font-weight:700; color:#003366;">الرئيسية</div></div>', unsafe_allow_html=True)

# 4. الصورة الحيوية العالمية
st.markdown("""
    <div class="hero-bg">
        <div class="hero-text">
            <h1>عقاراتك العالمية.. برؤية مصرية</h1>
            <p>ابحث في أرقى مشاريع المطورين المعتمدين</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# 5. الفلاتر (البحث)
st.markdown('<div class="filter-box">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    search_dev = st.text_input("🔍 اسم المطور", placeholder="مثلاً: سوديك")
with c2:
    search_area = st.selectbox("📍 اختر المنطقة", ["كل المناطق", "التجمع الخامس", "الشيخ زايد", "العاصمة الإدارية", "الساحل الشمالي"])
with c3:
    search_price = st.selectbox("💰 الفئة السعرية", ["الكل", "أقل من 5 مليون", "5 - 10 مليون", "أكثر من 10 مليون"])
st.markdown('</div>', unsafe_allow_html=True)

# 6. قاعدة البيانات (Data)
developers_db = [
    {"name": "أورا (Ora Developers)", "area": "الشيخ زايد", "price": "12,000,000", "min_val": 12},
    {"name": "سوديك (SODIC)", "area": "الشيخ زايد", "price": "8,000,000", "min_val": 8},
    {"name": "إعمار مصر (Emaar)", "area": "التجمع الخامس", "price": "15,000,000", "min_val": 15},
    {"name": "طلعت مصطفى (TMG)", "area": "العاصمة الإدارية", "price": "7,500,000", "min_val": 7.5},
    {"name": "ماونتن فيو (Mountain View)", "area": "التجمع الخامس", "price": "4,800,000", "min_val": 4.8},
    {"name": "بالم هيلز (Palm Hills)", "area": "الساحل الشمالي", "price": "9,200,000", "min_val": 9.2}
]

# 7. الفلترة
filtered = [d for d in developers_db if 
            (not search_dev or search_dev.lower() in d['name'].lower()) and
            (search_area == "كل المناطق" or d['area'] == search_area) and
            (search_price == "الكل" or 
             (search_price == "أقل من 5 مليون" and d['min_val'] < 5) or
             (search_price == "5 - 10 مليون" and 5 <= d['min_val'] < 10) or
             (search_price == "أكثر من 10 مليون" and d['min_val'] >= 10))
           ]

# 8. عرض النتائج
st.markdown(f'<div style="padding: 0 10%;"><p style="color:#64748b;">نتائج البحث: ({len(filtered)}) مطورين</p></div>', unsafe_allow_html=True)

for item in filtered:
    st.markdown(f'''
        <div class="project-card">
            <div class="card-img"></div>
            <div class="card-body">
                <div class="price-tag">يبدأ من {item['price']} ج.م</div>
                <div class="dev-name">{item['name']}</div>
                <div style="color:#64748b; font-size:1rem; margin-top:5px;">📍 {item['area']}</div>
            </div>
            <div style="display:flex; align-items:center; padding-left:40px;">
                <button class="btn-view">عرض المشاريع</button>
            </div>
        </div>
    ''', unsafe_allow_html=True)
