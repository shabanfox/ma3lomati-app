import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. حالة الجلسة (للتأمين)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 3. هندسة التناسق والجماليات (CSS)
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
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
        background-color: #f4f7fa !important;
    }

    /* الهيدر مع اللوجو الفخم */
    .header-nav {
        background: white;
        height: 75px;
        padding: 0 8%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #e2e8f0;
        position: sticky;
        top: 0;
        z-index: 1000;
        width: 100%;
        box-sizing: border-box;
    }

    /* تصميم اللوجو الجديد الفخم */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .logo-main {
        color: #003366; /* أزرق ملكي غامق */
        font-weight: 900;
        font-size: 1.8rem;
        letter-spacing: -1px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
    }
    .logo-sub {
        color: #D4AF37; /* لون ذهبي فخم */
        font-weight: 700;
        font-size: 1.8rem;
    }
    .logo-icon {
        color: #003366;
        font-size: 1.6rem;
    }

    .nav-links-area {
        display: flex;
        gap: 30px;
        align-items: center;
    }

    /* منطقة الصورة الخلفية (Hero) */
    .hero-outer {
        padding: 0 8%;
        margin-top: 10px;
    }
    .hero-inner {
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80');
        background-size: cover;
        background-position: center;
        height: 320px;
        border-radius: 12px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
    }

    /* كروت المشاريع العريضة */
    .project-card {
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        display: flex;
        height: 190px;
        margin-bottom: 15px;
        overflow: hidden;
        transition: transform 0.3s ease;
    }
    .project-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }
    .card-img { 
        width: 260px; 
        background: #eee url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=400&q=80') center/cover; 
    }
    .card-body { 
        padding: 20px; 
        flex: 1; 
        display: flex; 
        flex-direction: column; 
        justify-content: space-between; 
    }
    .price { color: #003366; font-weight: 900; font-size: 1.4rem; }
    </style>
""", unsafe_allow_html=True)

# --- 4. العرض ---

if not st.session_state.logged_in:
    # صفحة الدخول بنفس اللوجو الفخم
    st.markdown("""
        <div class="header-nav">
            <div class="logo-container">
                <i class="fa-solid fa-city logo-icon"></i>
                <div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    _, login_col, _ = st.columns([1, 1.2, 1])
    with login_col:
        st.markdown("<div style='margin-top:100px;'></div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#003366;'>دخول المنصة الآمن</h2>", unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم", placeholder="admin")
        p = st.text_input("كلمة المرور", type="password", placeholder="123")
        if st.button("دخول", use_container_width=True):
            if u == "admin" and p == "123":
                st.session_state.logged_in = True
                st.rerun()
else:
    # --- الموقع الرئيسي باللوجو الفخم ---
    st.markdown("""
        <div class="header-nav">
            <div class="logo-container">
                <i class="fa-solid fa-city logo-icon"></i>
                <div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div>
            </div>
            <div class="nav-links-area">
                <a href="#" style="color:#475569; text-decoration:none; font-weight:600; font-size:1rem;">الرئيسية</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # قسم الهيرو
    st.markdown("""
        <div class="hero-outer">
            <div class="hero-inner">
                <h1 style="font-weight:900; font-size:2.5rem; margin-bottom:10px;">بوابتك لأدق البيانات العقارية</h1>
                <p style="font-size:1.2rem; opacity:0.95;">المرجع الأول للمحترفين في السوق المصري</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # المحتوى بمسافات 8%
    st.markdown('<div style="padding: 0 8%; margin-top:25px;">', unsafe_allow_html=True)
    
    s1, s2, s3, s4 = st.columns([2, 1, 1, 0.6])
    with s1: st.text_input("📍 ابحث هنا...", label_visibility="collapsed")
    with s2: st.selectbox("النوع", ["كل الأنواع"], label_visibility="collapsed")
    with s3: st.selectbox("السعر", ["الكل"], label_visibility="collapsed")
    with s4: st.button("بحث", use_container_width=True)

    st.markdown("<h3 style='margin: 35px 0 20px 0; color:#003366;'>أحدث المشاريع الحصرية</h3>", unsafe_allow_html=True)

    # كارت المشروع بنفس الروح الفخمة
    st.markdown("""
        <div class="project-card">
            <div class="card-img"></div>
            <div class="card-body">
                <div>
                    <div class="price">9,200,000 ج.م</div>
                    <div style="font-weight: 700; font-size: 1.2rem; color: #1e293b; margin-top:5px;">كمبوند ايفوري جولي - الشيخ زايد</div>
                    <div style="color:#64748b; font-size:0.95rem; margin-top:5px;">📍 الشيخ زايد الجديدة</div>
                </div>
                <div style="text-align: left;">
                    <button style="background:#003366; border:none; color:white; padding:8px 20px; border-radius:6px; font-weight:700; cursor:pointer;">عرض التفاصيل</button>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
