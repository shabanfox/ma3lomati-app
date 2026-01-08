import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="معلوماتى العقارية", layout="wide")

# 2. كود التصميم الملكي (CSS) - محدث لإضافة ستايل الفلاتر
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    .block-container { padding: 0rem !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f4f7fa; 
    }

    /* الهيدر */
    .header-nav { 
        background: white; height: 75px; padding: 0 8%; display: flex; 
        justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; 
    }
    .logo-main { color: #003366; font-weight: 900; font-size: 1.8rem; }
    .logo-sub { color: #D4AF37; }

    /* شريط البحث والفلاتر */
    .filter-section {
        background: #003366; padding: 30px 8%; margin-bottom: 20px;
        display: flex; gap: 15px; flex-wrap: wrap;
    }
    
    /* تنسيق كروت المطورين */
    .project-card { 
        background: white; border-radius: 12px; border: 1px solid #e2e8f0; 
        display: flex; height: 160px; margin: 15px 8%; overflow: hidden; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .card-img { 
        width: 240px; background-image: url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400');
        background-size: cover; background-position: center; 
    }
    .card-body { padding: 20px; flex: 1; display: flex; flex-direction: column; justify-content: center; }
    .price-tag { color: #003366; font-weight: 900; font-size: 1.4rem; }
    .dev-name { font-weight: 700; font-size: 1.3rem; margin-top: 5px; color: #1e293b; }
    
    .btn-view {
        background: #003366; color: white; border: none; padding: 10px 20px; 
        border-radius: 8px; font-weight: 700; cursor: pointer;
    }

    /* تعديل شكل المدخلات في ستريمليت لتناسب التصميم */
    .stTextInput input, .stSelectbox div {
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. عرض الهيدر
st.markdown('<div class="header-nav"><div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div><div style="font-weight:700; color:#003366;">الرئيسية</div></div>', unsafe_allow_html=True)

# 4. منطقة الفلاتر (البحث)
st.markdown('<div style="padding: 20px 8% 0 8%;"><h3 style="color:#003366;">ابحث عن عقارك المفضل</h3></div>', unsafe_allow_html=True)

# توزيع خانات البحث في أعمدة
col1, col2, col3 = st.columns([1,1,1])
with st.container():
    st.markdown('<div style="padding: 0 8% 20px 8%;">', unsafe_allow_html=True)
    with col1:
        search_dev = st.text_input("🔍 اسم المطور", placeholder="مثلاً: سوديك")
    with col2:
        search_area = st.selectbox("📍 المنطقة", ["كل المناطق", "التجمع الخامس", "الشيخ زايد", "الساحل الشمالي", "العاصمة الإدارية"])
    with col3:
        search_price = st.selectbox("💰 الفئة السعرية", ["الكل", "أقل من 5 مليون", "5 - 10 مليون", "أكثر من 10 مليون"])
    st.markdown('</div>', unsafe_allow_html=True)

# 5. قاعدة بيانات المطورين (بيانات تجريبية للفلترة)
developers_data = [
    {"name": "أورا (Ora Developers)", "area": "الشيخ زايد", "price": "أكثر من 10 مليون"},
    {"name": "سوديك (SODIC)", "area": "الشيخ زايد", "price": "5 - 10 مليون"},
    {"name": "إعمار مصر (Emaar)", "area": "التجمع الخامس", "price": "أكثر من 10 مليون"},
    {"name": "طلعت مصطفى (TMG)", "area": "العاصمة الإدارية", "price": "5 - 10 مليون"},
    {"name": "ماونتن فيو (Mountain View)", "area": "التجمع الخامس", "price": "أقل من 5 مليون"},
    {"name": "بالم هيلز (Palm Hills)", "area": "الساحل الشمالي", "price": "5 - 10 مليون"},
]

# 6. منطق الفلترة (Filtering Logic)
filtered_devs = []
for dev in developers_data:
    # فلترة بالاسم
    if search_dev and search_dev.lower() not in dev['name'].lower():
        continue
    # فلترة بالمنطقة
    if search_area != "كل المناطق" and search_area != dev['area']:
        continue
    # فلترة بالسعر
    if search_price != "الكل" and search_price != dev['price']:
        continue
    filtered_devs.append(dev)

# 7. عرض النتائج
st.markdown(f'<div style="padding: 0 8%;"><p style="color:#64748b;">تم العثور على ({len(filtered_devs)}) مطورين</p></div>', unsafe_allow_html=True)

if filtered_devs:
    for dev in filtered_devs:
        st.markdown(f'''
            <div class="project-card">
                <div class="card-img"></div>
                <div class="card-body">
                    <div class="price-tag">{dev['price']}</div>
                    <div class="dev-name">{dev['name']}</div>
                    <div style="color:#64748b; font-size:0.9rem; margin-top:5px;">📍 {dev['area']} - متاح كامل التفاصيل</div>
                </div>
                <div style="display:flex; align-items:center; padding-left:30px;">
                    <button class="btn-view">عرض التفاصيل</button>
                </div>
            </div>
        ''', unsafe_allow_html=True)
else:
    st.markdown('<div style="text-align:center; padding:50px; color:#64748b;">لا توجد نتائج تطابق بحثك</div>', unsafe_allow_html=True)
