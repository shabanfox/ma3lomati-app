import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. حالة الجلسة (نظام الحماية)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def logout():
    st.session_state.logged_in = False
    st.rerun()

# 3. التنسيق (CSS)
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* تصفير الفراغ العلوي تماماً */
    .block-container {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }
    
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
        background-color: #f4f7fa !important;
    }

    /* الهيدر الموحد */
    .header-nav {
        background: white; height: 60px; padding: 0 8%;
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 1px solid #e2e8f0; position: sticky; top: 0; z-index: 1000;
    }
    .logo { color: #0056b3; font-weight: 900; font-size: 1.5rem; text-decoration: none; }
    
    /* حاوية الأيقونات يسار (ملتصقة ببعض) */
    .icons-left-group {
        display: flex;
        align-items: center;
        gap: 15px; /* المسافة بين أيقونة البيت وأيقونة الخروج */
    }

    /* تنسيق أيقونة الرئيسية */
    .nav-icon {
        color: #475569; font-size: 1.25rem; text-decoration: none; transition: 0.3s;
        display: flex; align-items: center;
    }
    .nav-icon:hover { color: #0056b3; }

    /* تنسيق زر الخروج (الأيقونة) ليكون بنفس الحجم والمحاذاة */
    .stButton > button {
        background: none !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        color: #ef4444 !important;
        font-size: 1.25rem !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        cursor: pointer;
    }
    .stButton > button:hover { color: #b91c1c !important; }

    /* الهيرو */
    .hero-outer { padding: 0 8%; margin-top: 5px; }
    .hero-inner {
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80');
        background-size: cover; background-position: center; height: 300px;
        border-radius: 12px; display: flex; flex-direction: column;
        justify-content: center; align-items: center; color: white;
    }
    </style>
""", unsafe_allow_html=True)

if not st.session_state.logged_in:
    # صفحة الدخول
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
    # --- الهيدر (الأيقونات بجانب بعضها تماماً) ---
    st.markdown("""
        <div class="header-nav">
            <div class="logo">معلوماتى <span style="color:#1e293b">العقارية</span></div>
            <div class="icons-left-group">
                <a href="#" class="nav-icon" title="الرئيسية"><i class="fa-solid fa-house"></i></a>
    """, unsafe_allow_html=True)
    
    # أيقونة الخروج داخل زر بجوار أيقونة البيت مباشرة
    if st.button(""): 
        logout()
        
    st.markdown("</div></div>", unsafe_allow_html=True)

    # --- باقي محتوى الصفحة ---
    st.markdown('<div class="hero-outer">', unsafe_allow_html=True)
    st.markdown("""
        <div class="hero-inner">
            <h1 style="font-weight:900; font-size:2.2rem;">عالم العقارات في مكان واحد</h1>
            <p>أدق المعلومات العقارية للمحترفين</p>
        </div>
    """, unsafe_allow_html=True)
    
    # شريط البحث والكروت
    st.markdown('<div style="margin-top:25px;">', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns([2, 1, 1, 0.6])
    with s1: st.text_input("📍 المنطقة", label_visibility="collapsed", placeholder="ابحث هنا...")
    with s2: st.selectbox("النوع", ["كل الأنواع"], label_visibility="collapsed")
    with s3: st.selectbox("السعر", ["الكل"], label_visibility="collapsed")
    with s4: st.button("بحث")
    
    st.markdown("<h3 style='margin: 30px 0;'>أحدث المشاريع</h3>", unsafe_allow_html=True)
    st.info("تم تسجيل الدخول. يمكنك الآن تصفح كافة البيانات.")
    st.markdown('</div></div>', unsafe_allow_html=True)
