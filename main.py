import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. هندسة التصميم (CSS) - ضبط المسافة العلوية بدقة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* ضبط المسافة العلوية لتكون "صغيرة خالص" */
    .block-container {
        padding-top: 0.5rem !important; /* المسافة الصغيرة اللي طلبتها */
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }
    
    /* إخفاء الهيدر الافتراضي لستريمليت */
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
        margin: 0 10px; /* مسافة بسيطة من الجوانب ليعطي شكل "عائم" قليلاً */
        border-radius: 8px;
    }
    .logo { color: #0056b3; font-weight: 900; font-size: 1.6rem; text-decoration: none; }
    
    .btn-login-main {
        background: #0056b3;
        color: white !important;
        padding: 10px 25px;
        border-radius: 8px;
        font-weight: 700;
        text-decoration: none;
        font-size: 0.95rem;
    }

    /* --- منطقة الخلفية (Hero Section) --- */
    .hero-container {
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80');
        background-size: cover;
        background-position: center;
        height: 350px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        margin-top: 10px;
    }
    
    .main-content { padding: 0 60px; margin-top: 30px; }
    
    /* كروت المشاريع */
    .project-card {
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        display: flex;
        height: 200px;
        margin-bottom: 20px;
        overflow: hidden;
    }
    .card-img { width: 280px; background: #eee url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=400&q=80') center/cover; }
    .card-details { padding: 20px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
    .price { color: #0056b3; font-weight: 900; font-size: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر (بمسافة علوية 0.5rem)
st.markdown("""
    <div class="header-nav">
        <div class="logo">معلوماتى <span style="color:#1e293b">العقارية</span></div>
        <div style="display: flex; gap: 30px; align-items: center;">
            <a href="#" style="color:#475569; text-decoration:none; font-weight:600;">الرئيسية</a>
            <a href="#" class="btn-login-main">سجل الدخول الآن</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. الصورة الخلفية
st.markdown("""
    <div class="hero-container">
        <h1 style="font-weight:900; font-size:2.5rem; text-shadow: 2px 2px 10px rgba(0,0,0,0.5);">منصة معلوماتي العقارية</h1>
        <p style="font-size:1.2rem; font-weight:600;">بيانات السوق العقاري بين يديك</p>
    </div>
""", unsafe_allow_html=True)

# 5. محرك البحث والنتائج
st.markdown('<div class="main-content">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([2.5, 1, 1, 0.7])
with c1: st.text_input("أين تبحث؟", key="search_input")
with c2: st.selectbox("النوع", ["شقة", "فيلا"], key="type_select")
with c3: st.selectbox("السعر", ["الكل"], key="price_select")
with c4: st.markdown('<button style="width:100%; height:45px; margin-top:28px; background:#0056b3; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">بحث</button>', unsafe_allow_html=True)

st.markdown("<h3 style='margin-top:30px;'>أحدث المشاريع المتاحة</h3>", unsafe_allow_html=True)

# الكارت الاحترافي
st.markdown("""
    <div class="project-card">
        <div class="card-img"></div>
        <div class="card-details">
            <div>
                <div class="price">9,200,000 ج.م</div>
                <div style="font-weight:700; font-size:1.2rem;">كمبوند ايفوري جولي</div>
                <div style="color:#64748b;">📍 التجمع الخامس، القاهرة الجديدة</div>
            </div>
            <div style="text-align: left;">
                <button style="background:#0056b3; color:white; border:none; padding:8px 20px; border-radius:5px; font-weight:700; cursor:pointer;">عرض التفاصيل</button>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
