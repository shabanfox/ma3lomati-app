import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. هندسة التناسق (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* تصفير المسافات الافتراضية وضبط المسافة العلوية الصغيرة */
    .block-container {
        padding-top: 0.6rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }
    
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background-color: #f4f7fa !important; /* رمادي أهدى قليلاً */
    }

    /* الحاوية الرئيسية لتوحيد المسافات الجانبية */
    .main-wrapper {
        padding: 0 8%; /* المسافة الجانبية الموحدة لكل الموقع */
    }

    /* --- الهيدر العلوي المتناسق --- */
    .header-nav {
        background: white;
        height: 70px;
        padding: 0 8%; /* نفس المسافة الجانبية */
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #e2e8f0;
        position: sticky;
        top: 0;
        z-index: 1000;
        width: 100%;
        box-sizing: border-box;
    }
    .logo { color: #0056b3; font-weight: 900; font-size: 1.5rem; text-decoration: none; }
    .btn-login {
        background: #0056b3;
        color: white !important;
        padding: 10px 24px;
        border-radius: 6px;
        font-weight: 700;
        text-decoration: none;
        font-size: 0.9rem;
    }

    /* --- منطقة الصورة الخلفية (Hero) --- */
    .hero-outer {
        padding: 0 8%;
        margin-top: 10px;
    }
    .hero-inner {
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
        url('https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80');
        background-size: cover;
        background-position: center;
        height: 320px;
        border-radius: 12px; /* حواف متناسقة مع الكروت */
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
    }

    /* --- كروت المشاريع --- */
    .project-card {
        background: white;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        display: flex;
        height: 190px;
        margin-bottom: 15px;
        overflow: hidden;
        transition: 0.2s ease;
    }
    .project-card:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        border-color: #0056b3;
    }
    .card-img { 
        width: 260px; 
        background: #eee url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=400&q=80') center/cover; 
    }
    .card-body { 
        padding: 18px; 
        flex: 1; 
        display: flex; 
        flex-direction: column; 
        justify-content: space-between; 
    }
    .price { color: #0056b3; font-weight: 900; font-size: 1.4rem; }
    .proj-title { font-weight: 700; font-size: 1.15rem; color: #1e293b; }
    
    /* تنسيق الأعمدة في ستريمليت ليكون داخل الـ Wrapper */
    .stHorizontalBlock {
        padding: 0px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر (Navigation)
st.markdown("""
    <div class="header-nav">
        <div class="logo">معلوماتى <span style="color:#1e293b">العقارية</span></div>
        <div style="display: flex; gap: 25px; align-items: center;">
            <a href="#" style="color:#475569; text-decoration:none; font-weight:600; font-size:0.9rem;">الرئيسية</a>
            <a href="#" class="btn-login">سجل الدخول الآن</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. قسم الصورة الخلفية (Hero Section)
st.markdown("""
    <div class="hero-outer">
        <div class="hero-inner">
            <h1 style="font-weight:900; font-size:2.2rem; margin-bottom:10px;">عالم العقارات في مكان واحد</h1>
            <p style="font-size:1.1rem; opacity:0.9;">أدق المعلومات عن المشاريع والمطورين في مصر</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# 5. محتوى الصفحة الرئيسي (البحث والنتائج) بمسافات موحدة
st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

# شريط البحث (مقسم بأعمدة ستريمليت لكن داخل الـ Wrapper)
st.markdown("<div style='margin-top:25px;'></div>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([2, 1, 1, 0.6])
with c1: st.text_input("📍 المنطقة أو المشروع", placeholder="ابحث هنا...", label_visibility="collapsed")
with c2: st.selectbox("النوع", ["كل الأنواع", "شقة", "فيلا"], label_visibility="collapsed")
with c3: st.selectbox("السعر", ["كل الأسعار", "3-5 مليون", "5-10 مليون"], label_visibility="collapsed")
with c4: st.button("بحث", use_container_width=True)

st.markdown("<h3 style='margin: 30px 0 20px 0; color:#1e293b; font-size:1.4rem;'>أحدث المشاريع العقارية</h3>", unsafe_allow_html=True)

# عرض النتائج في عمودين (النتائج والجانبي)
col_content, col_spacer, col_sidebar = st.columns([2.8, 0.2, 1])

with col_content:
    def create_card(price, name, loc):
        st.markdown(f"""
            <div class="project-card">
                <div class="card-img"></div>
                <div class="card-body">
                    <div>
                        <div class="price">{price} ج.م</div>
                        <div class="proj-title">{name}</div>
                        <div style="color:#64748b; font-size:0.9rem; margin-top:4px;">📍 {loc}</div>
                    </div>
                    <div style="text-align: left;">
                        <button style="background:white; border:1px solid #0056b3; color:#0056b3; padding:6px 16px; border-radius:5px; font-weight:700; cursor:pointer; font-size:0.85rem;">التفاصيل</button>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    create_card("9,200,000", "كمبوند ايفوري جولي - الشيخ زايد", "الشيخ زايد الجديدة")
    create_card("6,450,000", "ذا بروكس - التجمع الخامس", "القاهرة الجديدة")
    create_card("11,300,000", "بادية بالم هيلز - Badya", "مدينة 6 أكتوبر")

with col_sidebar:
    st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 10px; border: 1px solid #e2e8f0;">
            <h4 style="color:#0056b3; font-size:1.1rem; margin-bottom:15px;">دليل المستخدم</h4>
            <ul style="padding-right:15px; font-size:0.85rem; color:#475569; line-height:1.8;">
                <li>ابحث عن طريق اسم المطور</li>
                <li>قارن بين أسعار المتر</li>
                <li>حمل بروشورات المشاريع</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # قفلة الـ main-wrapper
