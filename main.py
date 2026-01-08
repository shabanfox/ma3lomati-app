import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="معلوماتى العقارية", layout="wide")

# 2. كود التصميم (الصورة، الهيدر، الفلاتر، والكروت)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء إعدادات ستريمليت */
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    .block-container { padding: 0rem !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f4f7fa; 
    }

    /* الهيدر العلوي */
    .header-nav { 
        background: white; height: 75px; padding: 0 8%; display: flex; 
        justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; 
    }
    .logo-main { color: #003366; font-weight: 900; font-size: 1.8rem; }
    .logo-sub { color: #D4AF37; }

    /* صورة الهيدر (Hero) */
    .hero-bg {
        background-image: linear-gradient(rgba(0,51,102,0.5), rgba(0,51,102,0.5)), 
                        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=2070&auto=format&fit=crop');
        background-size: cover; background-position: center; 
        height: 250px; display: flex; justify-content: center; align-items: center; 
        color: white; text-align: center;
    }
    .hero-text h1 { font-weight: 900; font-size: 2.5rem; margin: 0; }

    /* حاوية الفلاتر */
    .filter-box {
        background: white; margin: -40px 8% 20px 8%; padding: 25px;
        border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        position: relative; z-index: 10;
    }

    /* تصميم الكروت */
    .project-card { 
        background: white; border-radius: 12px; border: 1px solid #e2e8f0; 
        display: flex; height: 160px; margin: 15px 8%; overflow: hidden; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .card-img { 
        width: 240px; background-image: url('https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=400');
        background-size: cover; background-position: center; 
    }
    .card-body { padding: 20px; flex: 1; display: flex; flex-direction: column; justify-content: center; }
    .price-tag { color: #003366; font-weight: 900; font-size: 1.3rem; }
    .dev-name { font-weight: 700; font-size: 1.2rem; color: #1e293b; }
    .btn-view { background: #003366; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: 700; cursor: pointer; }
    </style>
""", unsafe_allow_html=True)

# 3. عرض الهيدر واللوجو
st.markdown('<div class="header-nav"><div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div><div style="font-weight:700;">الرئيسية</div></div>', unsafe_allow_html=True)

# 4. عرض صورة الهيدر
st.markdown('<div class="hero-bg"><div class="hero-text"><h1>اكتشف مستقبلك العقاري</h1></div></div>', unsafe_allow_html=True)

# 5. خانات البحث والفلترة (داخل الحاوية البيضاء)
st.markdown('<div class="filter-box">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    search_dev = st.text_input("🔍 اسم المطور", placeholder="مثلاً: سوديك")
with c2:
    search_area = st.selectbox("📍 المنطقة", ["كل المناطق", "التجمع الخامس", "الشيخ زايد", "العاصمة الإدارية", "الساحل الشمالي"])
with c3:
    search_price = st.selectbox("💰 الفئة السعرية", ["الكل", "أقل من 5 مليون", "5 - 10 مليون", "أكثر من 10 مليون"])
st.markdown('</div>', unsafe_allow_html=True)

# 6. قاعدة البيانات (أسماء من ناوي مع تفاصيل للفلترة)
developers_db = [
    {"name": "أورا (Ora Developers)", "area": "الشيخ زايد", "price_range": "أكثر من 10 مليون", "min_val": 12},
    {"name": "سوديك (SODIC)", "area": "الشيخ زايد", "price_range": "5 - 10 مليون", "min_val": 8},
    {"name": "إعمار مصر (Emaar)", "area": "التجمع الخامس", "price_range": "أكثر من 10 مليون", "min_val": 15},
    {"name": "طلعت مصطفى (TMG)", "area": "العاصمة الإدارية", "price_range": "5 - 10 مليون", "min_val": 7},
    {"name": "ماونتن فيو (Mountain View)", "area": "التجمع الخامس", "price_range": "أقل من 5 مليون", "min_val": 4},
    {"name": "بالم هيلز (Palm Hills)", "area": "الساحل الشمالي", "price_range": "5 - 10 مليون", "min_val": 9}
]

# 7. منطق الفلترة
filtered = []
for d in developers_db:
    if search_dev and search_dev.lower() not in d['name'].lower(): continue
    if search_area != "كل المناطق" and d['area'] != search_area: continue
    
    # فلترة السعر
    if search_price == "أقل من 5 مليون" and d['min_val'] >= 5: continue
    if search_price == "5 - 10 مليون" and not (5 <= d['min_val'] < 10): continue
    if search_price == "أكثر من 10 مليون" and d['min_val'] < 10: continue
    
    filtered.append(d)

# 8. عرض النتائج
st.markdown(f'<div style="padding: 10px 8%;"><p>تم العثور على ({len(filtered)}) مطورين</p></div>', unsafe_allow_html=True)

for item in filtered:
    st.markdown(f'''
        <div class="project-card">
            <div class="card-img"></div>
            <div class="card-body">
                <div class="price-tag">{item['price_range']}</div>
                <div class="dev-name">{item['name']}</div>
                <div style="color:#64748b; font-size:0.9rem;">📍 {item['area']} - متاح التفاصيل</div>
            </div>
            <div style="display:flex; align-items:center; padding-left:30px;">
                <button class="btn-view">عرض المشاريع</button>
            </div>
        </div>
    ''', unsafe_allow_html=True)
