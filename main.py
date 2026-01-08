import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. هندسة التصميم (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* إخفاء عناصر ستريمليت */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background-color: #f8fafc !important;
    }

    /* --- الهيدر العلوي --- */
    .header-nav {
        background: white;
        height: 75px;
        padding: 0 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #e2e8f0;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    .logo { color: #0056b3; font-weight: 900; font-size: 1.6rem; text-decoration: none; }
    
    /* زر سجل الدخول الآن */
    .btn-login-main {
        background: #0056b3;
        color: white !important;
        padding: 10px 25px;
        border-radius: 8px;
        font-weight: 700;
        text-decoration: none;
        font-size: 0.95rem;
        transition: 0.3s;
    }
    .btn-login-main:hover {
        background: #004494;
        box-shadow: 0 4px 12px rgba(0, 86, 179, 0.3);
    }

    /* --- منطقة الخلفية (Hero Section) --- */
    .hero-container {
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80');
        background-size: cover;
        background-position: center;
        height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        position: relative;
    }
    .hero-text h1 { font-size: 2.8rem; font-weight: 900; margin-bottom: 10px; text-shadow: 2px 2px 10px rgba(0,0,0,0.5); }
    .hero-text p { font-size: 1.3rem; opacity: 0.9; font-weight: 600; }

    /* --- كروت المشاريع --- */
    .main-content { margin-top: 50px; padding: 0 60px; }
    
    .project-card {
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        display: flex;
        height: 220px;
        margin-bottom: 20px;
        overflow: hidden;
        transition: 0.3s;
    }
    .project-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.06); }
    
    .card-img { width: 320px; background-color: #eee; background-image: url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=500&q=80'); background-size: cover; }
    .card-details { padding: 25px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
    .price { color: #0056b3; font-weight: 900; font-size: 1.6rem; }
    .title { font-weight: 700; font-size: 1.3rem; color: #1e293b; margin: 5px 0; }
    
    .btn-action { background: #0056b3; color: white; border: none; padding: 10px 30px; border-radius: 6px; font-weight: 700; cursor: pointer; }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر (المكان اللي غيرنا فيه)
st.markdown("""
    <div class="header-nav">
        <div class="logo">معلوماتى <span style="color:#1e293b">العقارية</span></div>
        <div style="display: flex; gap: 30px; align-items: center;">
            <a href="#" style="color:#475569; text-decoration:none; font-weight:600;">الرئيسية</a>
            <a href="#" style="color:#475569; text-decoration:none; font-weight:600;">دليل المطورين</a>
            <a href="#" class="btn-login-main">سجل الدخول الآن</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. منطقة الهيرو مع الصورة الخلفية
st.markdown("""
    <div class="hero-container">
        <div class="hero-text" style="text-align:center;">
            <h1>منصة معلوماتي العقارية للمحترفين</h1>
            <p>كل بيانات المطورين والمشاريع في مكان واحد بضغطة واحدة</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# 5. شريط البحث (مدمج في التصميم)
st.markdown('<div class="main-content">', unsafe_allow_html=True)
with st.container():
    c1, c2, c3, c4 = st.columns([2.5, 1, 1, 0.7])
    with c1: st.text_input("أين تبحث؟", placeholder="التجمع، الشيخ زايد، العاصمة الإدارية...")
    with c2: st.selectbox("نوع العقار", ["شقة", "فيلا", "تجاري", "إداري"])
    with c3: st.selectbox("السعر من", ["الكل", "2 مليون", "5 مليون", "10 مليون"])
    with c4: st.markdown('<button class="btn-action" style="width:100%; height:45px; margin-top:28px;">بحث</button>', unsafe_allow_html=True)

# 6. النتائج
st.markdown("<h3 style='margin: 40px 0 20px 0; color:#1e293b;'>أحدث المشاريع العقارية</h3>", unsafe_allow_html=True)

col_results, col_ads = st.columns([3, 1], gap="large")

with col_results:
    def draw_project(price, name, loc, developer):
        st.markdown(f"""
            <div class="project-card">
                <div class="card-img"></div>
                <div class="card-details">
                    <div>
                        <div class="price">{price} ج.م</div>
                        <div class="title">{name}</div>
                        <div style="color:#64748b; font-size:0.95rem;">📍 {loc}</div>
                        <div style="margin-top:12px; font-size:0.9rem;">المطور: <b style="color:#1e293b;">{developer}</b></div>
                    </div>
                    <div style="text-align: left;">
                        <button class="btn-action">عرض التفاصيل</button>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    draw_project("8,250,000", "ايفوري جولي - Ivoire Zayed", "الشيخ زايد الجديدة", "PRE Developments")
    draw_project("5,400,000", "ذا بروكس - The Brooks", "القاهرة الجديدة", "PRE Developments")
    draw_project("11,000,000", "بادية - Badya", "مدينة 6 أكتوبر", "Palm Hills")

with col_ads:
    st.markdown("""
        <div style="background:white; padding:25px; border-radius:12px; border:1px solid #e2e8f0;">
            <h5 style="color:#0056b3; margin-bottom:15px;">دليل المناطق</h5>
            <div style="line-height:2.2; font-size:0.95rem; color:#475569;">
                • القاهرة الجديدة<br>
                • الشيخ زايد<br>
                • العاصمة الإدارية<br>
                • أكتوبر
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
