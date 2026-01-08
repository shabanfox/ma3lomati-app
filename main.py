import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. هندسة التصميم (CSS) - دمج الهيدر مع الصورة الخلفية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* إخفاء عناصر ستريمليت الافتراضية */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background-color: #f8fafc !important;
    }

    /* --- 1. الهيدر العلوي الثابت --- */
    .header-nav {
        background: white;
        height: 70px;
        padding: 0 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #e2e8f0;
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    .logo { color: #0056b3; font-weight: 900; font-size: 1.6rem; text-decoration: none; }
    .nav-items a { color: #475569; text-decoration: none; margin-right: 20px; font-weight: 600; font-size: 0.9rem; }
    .nav-items a:hover { color: #0056b3; }

    /* --- 2. منطقة الخلفية (Hero Section) --- */
    .hero-container {
        background-image: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), 
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80');
        background-size: cover;
        background-position: center;
        height: 380px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        position: relative;
    }
    .hero-text h1 { font-size: 2.5rem; font-weight: 900; margin-bottom: 10px; text-shadow: 2px 2px 8px rgba(0,0,0,0.5); }
    .hero-text p { font-size: 1.2rem; opacity: 0.9; }

    /* --- 3. شريط البحث العائم فوق الصورة --- */
    .search-overlay {
        background: white;
        width: 85%;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        position: absolute;
        bottom: -45px; /* لجعل نصف الشريط خارج الصورة */
        display: flex;
        gap: 15px;
        align-items: flex-end;
    }

    /* --- 4. كروت المشاريع (عقارماب ستايل) --- */
    .main-content { margin-top: 80px; padding: 0 60px; }
    
    .project-card {
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        display: flex;
        height: 210px;
        margin-bottom: 20px;
        overflow: hidden;
        transition: 0.3s;
    }
    .project-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
    
    .card-img { width: 300px; background-color: #eee; background-image: url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=400&q=80'); background-size: cover; }
    .card-details { padding: 20px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
    .price { color: #0056b3; font-weight: 900; font-size: 1.5rem; }
    .title { font-weight: 700; font-size: 1.2rem; color: #1e293b; margin: 5px 0; }
    .location { color: #64748b; font-size: 0.9rem; }
    
    .btn-details { background: #0056b3; color: white; border: none; padding: 8px 25px; border-radius: 6px; font-weight: 700; cursor: pointer; }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر
st.markdown("""
    <div class="header-nav">
        <div class="logo">معلوماتى <span style="color:#1e293b">العقارية</span></div>
        <div class="nav-items">
            <a href="#">الرئيسية</a>
            <a href="#">المشاريع</a>
            <a href="#">المطورين</a>
            <a href="#" style="background:#0056b3; color:white; padding:8px 15px; border-radius:5px;">أضف عقارك</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. منطقة الهيرو مع الصورة الخلفية
st.markdown("""
    <div class="hero-container">
        <div class="hero-text" style="text-align:center;">
            <h1>ابحث عن عقارك المفضل في مصر</h1>
            <p>أكثر من 500 مشروع سكني وتجاري في القاهرة الجديدة، زايد، والعاصمة</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# 5. شريط البحث (مدمج مع الصورة)
st.markdown('<div class="main-content">', unsafe_allow_html=True)
with st.container():
    # استخدام أعمدة ستريمليت لمحاكاة شريط البحث العائم
    c1, c2, c3, c4 = st.columns([2.5, 1, 1, 0.6])
    with c1: st.text_input("أين تبحث؟", placeholder="التجمع، الشيخ زايد، العاصمة الإدارية...")
    with c2: st.selectbox("نوع العقار", ["شقة", "فيلا", "تجاري", "إداري"])
    with c3: st.selectbox("السعر من", ["الكل", "2 مليون", "5 مليون", "10 مليون"])
    with c4: st.markdown('<button class="btn-details" style="width:100%; height:45px; margin-top:28px;">بحث</button>', unsafe_allow_html=True)

# 6. قائمة المشاريع (النتائج)
st.markdown("<h3 style='margin: 30px 0 20px 0; color:#1e293b;'>أحدث المشاريع المضافة</h3>", unsafe_allow_html=True)

col_list, col_side = st.columns([3, 1], gap="large")

with col_list:
    def draw_card(price, name, loc, developer):
        st.markdown(f"""
            <div class="project-card">
                <div class="card-img"></div>
                <div class="card-details">
                    <div>
                        <div class="price">{price} ج.م</div>
                        <div class="title">{name}</div>
                        <div class="location">📍 {loc}</div>
                        <div style="margin-top:10px; font-size:0.85rem;">المطور: <b>{developer}</b></div>
                    </div>
                    <div style="text-align: left;">
                        <button class="btn-details">عرض التفاصيل</button>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    draw_card("8,250,000", "كمبوند ايفوري جولي - Ivoire", "الشيخ زايد الجديدة", "PRE Developments")
    draw_card("5,400,000", "ذا بروكس - The Brooks", "القاهرة الجديدة", "PRE Developments")
    draw_card("11,000,000", "بادية - Badya", "مدينة 6 أكتوبر", "Palm Hills")

with col_side:
    st.markdown("""
        <div style="background:white; padding:20px; border-radius:12px; border:1px solid #e2e8f0;">
            <h5 style="color:#0056b3;">دليل البروكر السريع</h5>
            <hr style="opacity:0.1">
            <p style="font-size:0.85rem; color:#64748b;">هذه الأداة تساعدك في الوصول لأسعار المطورين الرسمية بضغطة واحدة.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
