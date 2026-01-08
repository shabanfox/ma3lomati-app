import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. تهيئة حالة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# دالة تسجيل الخروج
def logout():
    st.session_state.logged_in = False
    st.rerun()

# 3. التنسيق (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    .block-container { padding-top: 0.5rem !important; padding-left: 0rem !important; padding-right: 0rem !important; }
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
        background-color: #f4f7fa !important;
    }

    /* الهيدر العلوي */
    .header-nav {
        background: white; height: 75px; padding: 0 8%;
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 1px solid #e2e8f0; position: sticky; top: 0; z-index: 1000;
    }
    .logo { color: #0056b3; font-weight: 900; font-size: 1.6rem; text-decoration: none; }
    
    .nav-links { display: flex; gap: 25px; align-items: center; }
    .nav-links a { color: #475569; text-decoration: none; font-weight: 600; font-size: 0.95rem; }
    
    /* ستايل زر تسجيل الخروج في الهيدر */
    .stButton > button {
        background-color: transparent !important;
        color: #ef4444 !important;
        border: 1px solid #ef4444 !important;
        font-weight: 700 !important;
        padding: 5px 15px !important;
        border-radius: 8px !important;
    }
    .stButton > button:hover {
        background-color: #ef4444 !important;
        color: white !important;
    }

    /* منطقة الهيرو والكروت */
    .hero-container {
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80');
        background-size: cover; background-position: center; height: 350px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        color: white; margin-bottom: 40px;
    }
    .main-wrapper { padding: 0 8%; }
    .project-card {
        background: white; border-radius: 12px; border: 1px solid #e2e8f0;
        display: flex; height: 200px; margin-bottom: 20px; overflow: hidden;
    }
    .card-img { width: 280px; background: #eee url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=400&q=80') center/cover; }
    .card-body { padding: 20px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
    </style>
""", unsafe_allow_html=True)

# --- نظام عرض الصفحات ---
if not st.session_state.logged_in:
    # صفحة تسجيل الدخول (كما هي)
    st.markdown('<div class="header-nav"><div class="logo">معلوماتى <span style="color:#1e293b">العقارية</span></div></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.write("")
        st.markdown("<h2 style='text-align:center;'>تسجيل الدخول</h2>", unsafe_allow_html=True)
        user = st.text_input("اسم المستخدم")
        pw = st.text_input("كلمة المرور", type="password")
        if st.button("دخول", use_container_width=True):
            if user == "admin" and pw == "123":
                st.session_state.logged_in = True
                st.rerun()
else:
    # --- الموقع الرئيسي بعد تسجيل الدخول ---
    
    # الهيدر مع زر الخروج بجانب الروابط
    header_col1, header_col2 = st.columns([4, 1])
    
    # عرض الهيدر باستخدام HTML مخصص للجزء الأيمن والـ Button للجزء الأيسر
    with st.container():
        st.markdown("""
            <div class="header-nav">
                <div class="logo">معلوماتى <span style="color:#1e293b">العقارية</span></div>
                <div class="nav-links">
                    <a href="#">الرئيسية</a>
                    <a href="#">المشاريع</a>
                    <a href="#">المطورين</a>
        """, unsafe_allow_html=True)
        
        # وضع زر تسجيل الخروج في نهاية الـ nav-links
        if st.button("تسجيل الخروج"):
            logout()
            
        st.markdown("</div></div>", unsafe_allow_html=True)

    # محتوى الصفحة (Hero)
    st.markdown("""
        <div class="hero-container">
            <h1 style="font-weight:900; font-size:2.5rem;">منصة المحترفين</h1>
            <p style="font-size:1.2rem;">أهلاً بك مرة أخرى في عالم المعلومات العقارية</p>
        </div>
    """, unsafe_allow_html=True)

    # محرك البحث والكروت بمسافة جانبية موحدة
    st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns([2.5, 1, 1, 0.7])
    with c1: st.text_input("📍 ابحث هنا...", label_visibility="collapsed")
    with c2: st.selectbox("النوع", ["شقة", "فيلا"], label_visibility="collapsed")
    with c3: st.selectbox("الميزانية", ["الكل"], label_visibility="collapsed")
    with c4: st.button("ابحث الآن", use_container_width=True)

    st.markdown("<h3 style='margin: 30px 0;'>أحدث المشاريع العقارية</h3>", unsafe_allow_html=True)

    # مثال لكارت
    st.markdown("""
        <div class="project-card">
            <div class="card-img"></div>
            <div class="card-body">
                <div>
                    <div style="color:#0056b3; font-weight:900; font-size:1.5rem;">9,500,000 ج.م</div>
                    <div style="font-weight:700; font-size:1.2rem;">كمبوند ايفوري - الشيخ زايد</div>
                    <div style="color:#64748b;">📍 الشيخ زايد الجديدة</div>
                </div>
                <div style="text-align: left;">
                    <button style="background:#0056b3; color:white; border:none; padding:8px 25px; border-radius:6px; font-weight:700; cursor:pointer;">التفاصيل</button>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
