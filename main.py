import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. حالة الجلسة (نظام الحماية)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def logout():
    st.session_state.logged_in = False
    st.rerun()

# 3. التنسيق البرمجي (CSS)
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* إلغاء الفراغات الافتراضية تماماً */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }
    
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
        background-color: #f4f7fa !important;
    }

    /* الهيدر المطور سطر واحد */
    .header-nav {
        background: white; height: 60px; padding: 0 8%;
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 1px solid #e2e8f0; position: sticky; top: 0; z-index: 1000;
    }
    .logo { color: #0056b3; font-weight: 900; font-size: 1.5rem; text-decoration: none; }
    
    /* حاوية الأيقونات جهة اليسار */
    .icons-left-container {
        display: flex;
        align-items: center;
        gap: 25px; /* المسافة بين الأيقونتين */
    }

    /* تنسيق زر الخروج (الأيقونة) ليعمل برمجياً */
    .stButton > button {
        background: none !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        color: #ef4444 !important; /* لون الخروج أحمر */
        font-size: 1.4rem !important;
        cursor: pointer;
        line-height: 1 !important;
    }
    .stButton > button:hover { color: #b91c1c !important; }

    /* أيقونة الرئيسية */
    .home-icon {
        color: #475569; font-size: 1.4rem; text-decoration: none; transition: 0.3s;
    }
    .home-icon:hover { color: #0056b3; }

    /* تصغير الفراغ فوق الهيرو */
    .hero-outer { padding: 0 8%; margin-top: 5px; }
    .hero-inner {
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80');
        background-size: cover; background-position: center; height: 300px;
        border-radius: 12px; display: flex; flex-direction: column;
        justify-content: center; align-items: center; color: white;
    }

    /* كروت المشاريع (عقار ماب ستايل) */
    .main-content { padding: 0 8%; margin-top: 20px; }
    .project-card {
        background: white; border-radius: 10px; border: 1px solid #e2e8f0;
        display: flex; height: 180px; margin-bottom: 15px; overflow: hidden;
    }
    .card-img { width: 250px; background: #eee url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=400&q=80') center/cover; }
    .card-body { padding: 15px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق عرض الصفحات ---

if not st.session_state.logged_in:
    # صفحة تسجيل الدخول
    st.markdown('<div class="header-nav"><div class="logo">معلوماتى العقارية</div></div>', unsafe_allow_html=True)
    _, login_box, _ = st.columns([1, 1, 1])
    with login_box:
        st.markdown("<div style='margin-top:100px;'></div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>دخول المنصة</h2>", unsafe_allow_html=True)
        user = st.text_input("اسم المستخدم")
        pwd = st.text_input("كلمة المرور", type="password")
        if st.button("تسجيل الدخول", use_container_width=True):
            if user == "admin" and pwd == "123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("البيانات غير صحيحة")
else:
    # --- الموقع الرئيسي بعد تسجيل الدخول ---
    
    # الهيدر الموحد: اللوجو يمين، والأيقونات يسار
    st.markdown("""
        <div class="header-nav">
            <div class="logo">معلوماتى <span style="color:#1e293b">العقارية</span></div>
            <div class="icons-left-container">
                <a href="#" class="home-icon" title="الرئيسية"><i class="fa-solid fa-house"></i></a>
    """, unsafe_allow_html=True)
    
    # أيقونة الخروج برمز Font Awesome داخل زر ستريمليت ليعمل برمجياً
    if st.button("", help="خروج"): 
        logout()
        
    st.markdown("</div></div>", unsafe_allow_html=True)

    # قسم الهيرو (تقليل الفراغ العلوي)
    st.markdown('<div class="hero-outer">', unsafe_allow_html=True)
    st.markdown("""
        <div class="hero-inner">
            <h1 style="font-weight:900; font-size:2.2rem; margin-bottom:10px;">عالم العقارات في مكان واحد</h1>
            <p style="font-size:1.1rem; opacity:0.9;">أدق المعلومات العقارية للمحترفين</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # المحتوى الرئيسي (8%)
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # شريط البحث
    s1, s2, s3, s4 = st.columns([2, 1, 1, 0.6])
    with s1: st.text_input("📍 المنطقة", label_visibility="collapsed", placeholder="ابحث عن مشروع...")
    with s2: st.selectbox("النوع", ["كل الأنواع"], label_visibility="collapsed")
    with s3: st.selectbox("السعر", ["الكل"], label_visibility="collapsed")
    with s4: st.button("بحث")

    st.markdown("<h3 style='margin: 25px 0 15px 0;'>أحدث المشاريع</h3>", unsafe_allow_html=True)

    # الكارت العريض
    st.markdown("""
        <div class="project-card">
            <div class="card-img"></div>
            <div class="card-body">
                <div>
                    <div style="color: #0056b3; font-weight: 900; font-size: 1.4rem;">9,200,000 ج.م</div>
                    <div style="font-weight: 700; font-size: 1.15rem;">كمبوند ايفوري جولي</div>
                    <div style="color:#64748b; font-size:0.85rem;">📍 الشيخ زايد الجديدة</div>
                </div>
                <div style="text-align: left;">
                    <button style="background:white; border:1px solid #0056b3; color:#0056b3; padding:5px 15px; border-radius:5px; font-weight:700; font-size:0.8rem;">التفاصيل</button>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
