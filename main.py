import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. تهيئة حالة الجلسة (نظام الحماية)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# دالة لتنفيذ الخروج
def logout_action():
    st.session_state.logged_in = False
    st.rerun()

# 3. هندسة التناسق والجماليات (CSS)
st.markdown("""
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

    /* الهيدر العلوي */
    .header-nav {
        background: white;
        height: 70px;
        padding: 0 8%;
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
    
    .nav-links-area {
        display: flex;
        gap: 20px;
        align-items: center;
    }

    /* منطقة الهيرو */
    .hero-outer { padding: 0 8%; margin-top: 10px; }
    .hero-inner {
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80');
        background-size: cover; background-position: center; height: 320px;
        border-radius: 12px; display: flex; flex-direction: column;
        justify-content: center; align-items: center; color: white;
    }

    /* كروت المشاريع */
    .project-card {
        background: white; border-radius: 10px; border: 1px solid #e2e8f0;
        display: flex; height: 190px; margin-bottom: 15px; overflow: hidden;
    }
    .card-img { 
        width: 260px; 
        background: #eee url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=400&q=80') center/cover; 
    }
    .card-body { padding: 18px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
    
    /* تصميم زر الخروج ليظهر ككلمة عادية */
    .stButton > button {
        background: none !important;
        border: none !important;
        color: #ef4444 !important;
        padding: 0 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        font-family: 'Cairo', sans-serif !important;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق عرض الصفحات ---

# إذا لم يتم تسجيل الدخول، تظهر فقط صفحة الدخول
if not st.session_state.logged_in:
    st.markdown('<div class="header-nav"><div class="logo">معلوماتى <span style="color:#1e293b">العقارية</span></div></div>', unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 1.2, 1])
    with col_b:
        st.markdown("<div style='margin-top:100px;'></div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center;'>تسجيل دخول المحترفين</h2>", unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم", placeholder="admin")
        p = st.text_input("كلمة المرور", type="password", placeholder="123")
        if st.button("دخول", use_container_width=True):
            if u == "admin" and p == "123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")

else:
    # --- الموقع الرئيسي (المحتوى المحمي) ---
    
    # الهيدر مع "الرئيسية" وكلمة "خروج" بجانبها
    with st.container():
        st.markdown("""
            <div class="header-nav">
                <div class="logo">معلوماتى <span style="color:#1e293b">العقارية</span></div>
                <div class="nav-links-area">
                    <a href="#" style="color:#475569; text-decoration:none; font-weight:600; font-size:0.9rem;">الرئيسية</a>
        """, unsafe_allow_html=True)
        
        # زر "خروج" بجانب "الرئيسية"
        if st.button("خروج"):
            logout_action()
            
        st.markdown("</div></div>", unsafe_allow_html=True)

    # قسم الصورة الخلفية (Hero)
    st.markdown("""
        <div class="hero-outer">
            <div class="hero-inner">
                <h1 style="font-weight:900; font-size:2.2rem; margin-bottom:10px;">عالم العقارات في مكان واحد</h1>
                <p style="font-size:1.1rem; opacity:0.9;">أدق المعلومات عن المشاريع والمطورين في مصر</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # المحتوى الرئيسي بمسافات 8%
    st.markdown('<div style="padding: 0 8%;">', unsafe_allow_html=True)
    
    # شريط البحث
    st.markdown("<div style='margin-top:25px;'></div>", unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns([2, 1, 1, 0.6])
    with s1: st.text_input("📍 المنطقة أو المشروع", placeholder="ابحث هنا...", label_visibility="collapsed")
    with s2: st.selectbox("النوع", ["شقة", "فيلا"], label_visibility="collapsed")
    with s3: st.selectbox("السعر", ["الكل"], label_visibility="collapsed")
    with s4: st.button("بحث 🔍", use_container_width=True)

    st.markdown("<h3 style='margin: 30px 0;'>أحدث المشاريع</h3>", unsafe_allow_html=True)

    # عرض كروت المشاريع
    col_l, col_s, col_r = st.columns([2.8, 0.2, 1])
    with col_l:
        st.markdown(f"""
            <div class="project-card">
                <div class="card-img"></div>
                <div class="card-body">
                    <div>
                        <div style="color: #0056b3; font-weight: 900; font-size: 1.4rem;">9,200,000 ج.م</div>
                        <div style="font-weight: 700; font-size: 1.15rem; color: #1e293b;">كمبوند ايفوري جولي</div>
                        <div style="color:#64748b; font-size:0.9rem; margin-top:4px;">📍 الشيخ زايد الجديدة</div>
                    </div>
                    <div style="text-align: left;">
                        <button style="background:white; border:1px solid #0056b3; color:#0056b3; padding:6px 16px; border-radius:5px; font-weight:700; font-size:0.85rem;">التفاصيل</button>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
