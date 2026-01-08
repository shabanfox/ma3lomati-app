import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. حالة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def logout():
    st.session_state.logged_in = False
    st.rerun()

# 3. هندسة التناسق (CSS) مع إضافة مكتبة الأيقونات
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* تقليل الفراغ الأبيض العلوي */
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

    /* الهيدر المطور */
    .header-nav {
        background: white; height: 65px; padding: 0 8%;
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 1px solid #e2e8f0; position: sticky; top: 0; z-index: 1000;
    }
    .logo { color: #0056b3; font-weight: 900; font-size: 1.5rem; text-decoration: none; }
    
    /* حاوية الأيقونات يسار */
    .icons-container {
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .icon-link {
        color: #475569; font-size: 1.3rem; text-decoration: none; transition: 0.3s;
        cursor: pointer;
    }
    .icon-link:hover { color: #0056b3; }
    .logout-icon { color: #ef4444; }
    .logout-icon:hover { color: #b91c1c; }

    /* تصغير الفراغ فوق الهيرو */
    .hero-outer { padding: 0 8%; margin-top: 5px; }
    .hero-inner {
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80');
        background-size: cover; background-position: center; height: 300px;
        border-radius: 12px; display: flex; flex-direction: column;
        justify-content: center; align-items: center; color: white;
    }

    /* زر الخروج الشفاف (الأيقونة) */
    .stButton > button {
        background: none !important;
        border: none !important;
        padding: 0 !important;
        color: #ef4444 !important;
        font-size: 1.3rem !important;
    }

    .project-card {
        background: white; border-radius: 10px; border: 1px solid #e2e8f0;
        display: flex; height: 190px; margin-bottom: 15px; overflow: hidden;
    }
    .card-img { width: 260px; background: #eee url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=400&q=80') center/cover; }
    .card-body { padding: 18px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
    </style>
""", unsafe_allow_html=True)

if not st.session_state.logged_in:
    # صفحة الدخول
    st.markdown('<div class="header-nav"><div class="logo">معلوماتى العقارية</div></div>', unsafe_allow_html=True)
    _, login_col, _ = st.columns([1, 1.2, 1])
    with login_col:
        st.markdown("<div style='margin-top:100px;'></div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>دخول المنصة</h2>", unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول", key="login_btn", use_container_width=True):
            if u == "admin" and p == "123":
                st.session_state.logged_in = True
                st.rerun()
else:
    # --- الهيدر المنسق بالأيقونات ---
    st.markdown("""
        <div class="header-nav">
            <div class="logo">معلوماتى <span style="color:#1e293b">العقارية</span></div>
            <div class="icons-container">
                <a href="#" class="icon-link" title="الرئيسية"><i class="fa-solid fa-house"></i></a>
    """, unsafe_allow_html=True)
    
    # أيقونة الخروج (باستخدام زر ستريمليت)
    if st.button("󰈆", help="تسجيل خروج"): # استخدمت رمز للخروج داخل الزر
        logout()
        
    st.markdown("</div></div>", unsafe_allow_html=True)

    # --- محتوى الصفحة مع تقليل المسافة العلوية ---
    st.markdown('<div class="hero-outer">', unsafe_allow_html=True)
    st.markdown("""
        <div class="hero-inner">
            <h1 style="font-weight:900; font-size:2.2rem;">عالم العقارات في مكان واحد</h1>
            <p>أدق المعلومات العقارية للمحترفين</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="margin-top:25px;">', unsafe_allow_html=True)
    # شريط البحث والكروت (نفس تصميمك الأصلي)
    s1, s2, s3, s4 = st.columns([2, 1, 1, 0.6])
    with s1: st.text_input("📍 ابحث هنا...", label_visibility="collapsed")
    with s2: st.selectbox("النوع", ["كل الأنواع"], label_visibility="collapsed")
    with s3: st.selectbox("السعر", ["الكل"], label_visibility="collapsed")
    with s4: st.button("بحث")

    st.markdown("<h3 style='margin: 30px 0;'>أحدث المشاريع</h3>", unsafe_allow_html=True)
    
    # مثال للكارت
    st.markdown("""
        <div class="project-card">
            <div class="card-img"></div>
            <div class="card-body">
                <div>
                    <div style="color: #0056b3; font-weight: 900; font-size: 1.4rem;">9,200,000 ج.م</div>
                    <div style="font-weight: 700; font-size: 1.15rem;">كمبوند ايفوري جولي</div>
                    <div style="color:#64748b; font-size:0.9rem;">📍 الشيخ زايد الجديدة</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
