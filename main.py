import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. حالة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 3. هندسة التنسيق (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* تصفير المسافات تماماً */
    .block-container {
        padding: 0rem !important;
    }
    
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background-color: #f4f7fa !important;
    }

    /* حاوية الهيدر */
    .custom-header {
        background-color: white;
        border-bottom: 1px solid #e2e8f0;
        padding: 10px 8%;
        position: sticky;
        top: 0;
        z-index: 1000;
    }

    .logo-text { color: #0056b3; font-weight: 900; font-size: 1.6rem; text-decoration: none; }
    
    /* تنسيق الروابط وزر الخروج */
    .nav-item {
        color: #475569;
        text-decoration: none;
        font-weight: 600;
        font-size: 1rem;
        margin-left: 20px;
        display: inline-block;
    }

    /* جعل زر خروج ستريمليت يبدو كنص أحمر */
    .stButton > button {
        background: none !important;
        border: none !important;
        color: #ef4444 !important;
        padding: 0 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        font-family: 'Cairo', sans-serif !important;
        margin: 0 !important;
    }
    
    .hero-section { padding: 0 8%; margin-top: 15px; }
    .hero-box {
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80');
        background-size: cover; background-position: center; height: 300px;
        border-radius: 12px; display: flex; flex-direction: column;
        justify-content: center; align-items: center; color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق العرض ---

if not st.session_state.logged_in:
    # صفحة تسجيل الدخول
    st.markdown('<div class="custom-header"><div class="logo-text">معلوماتى العقارية</div></div>', unsafe_allow_html=True)
    _, login_col, _ = st.columns([1, 1, 1])
    with login_col:
        st.markdown("<div style='margin-top:80px;'></div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>دخول المنصة</h2>", unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة المرور", type="password")
        if st.button("تسجيل الدخول", use_container_width=True):
            if u == "admin" and p == "123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("خطأ في البيانات")
else:
    # --- الهيدر المنسق (سطر واحد حقيقي) ---
    st.markdown('<div class="custom-header">', unsafe_allow_html=True)
    
    # تقسيم الهيدر لعمودين (يمين للوجو، يسار للروابط)
    h_col1, h_col2 = st.columns([2, 1])
    
    with h_col1:
        st.markdown('<div class="logo-text">معلوماتى <span style="color:#1e293b">العقارية</span></div>', unsafe_allow_html=True)
    
    with h_col2:
        # ترتيب العناصر لليسار
        col_link1, col_link2 = st.columns([1, 1])
        with col_link1:
            st.markdown('<div style="text-align: left; margin-top: 8px;"><a href="#" class="nav-item">الرئيسية</a></div>', unsafe_allow_html=True)
        with col_link2:
            st.markdown('<div style="text-align: left; margin-top: 5px;">', unsafe_allow_html=True)
            if st.button("خروج"):
                st.session_state.logged_in = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

    # --- محتوى الصفحة ---
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    st.markdown("""
        <div class="hero-box">
            <h1 style="font-weight:900;">عالم العقارات في مكان واحد</h1>
            <p>أدق المعلومات عن المشاريع والمطورين في مصر</p>
        </div>
    """, unsafe_allow_html=True)
    
    # شريط البحث
    st.markdown("<div style='margin-top:25px;'></div>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns([2, 1, 1, 0.6])
    with s1: st.text_input("📍 ابحث هنا...", label_visibility="collapsed")
    with s2: st.selectbox("النوع", ["شقة", "فيلا"], label_visibility="collapsed")
    with s3: st.selectbox("السعر", ["الكل"], label_visibility="collapsed")
    with s4: st.button("بحث")
    
    st.markdown("<h3 style='margin-top:30px;'>أحدث المشاريع</h3>", unsafe_allow_html=True)
    # كروت بسيطة للتأكد من التناسق
    st.info("تم تسجيل الدخول بنجاح. تصفح المشاريع الآن.")
    st.markdown('</div>', unsafe_allow_html=True)
