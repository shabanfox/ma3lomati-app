import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. حالة الجلسة (لضمان بقاء الدخول مفعل)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 3. هندسة التناسق (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* ضبط المسافة العلوية الصغيرة جداً */
    .block-container {
        padding-top: 0.6rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }
    
    /* إخفاء عناصر ستريمليت الافتراضية */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background-color: #f4f7fa !important;
    }

    /* الهيدر العلوي النظيف (بدون أي أزرار خروج) */
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
    .nav-links-area { display: flex; gap: 30px; align-items: center; }

    /* منطقة الهيرو (الصورة الخلفية) */
    .hero-outer { padding: 0 8%; margin-top: 10px; }
    .hero-inner {
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80');
        background-size: cover; background-position: center; height: 320px;
        border-radius: 12px; display: flex; flex-direction: column;
        justify-content: center; align-items: center; color: white;
    }

    /* كروت المشاريع العريضة المتناسقة */
    .project-card {
        background: white; border-radius: 10px; border: 1px solid #e2e8f0;
        display: flex; height: 190px; margin-bottom: 15px; overflow: hidden;
    }
    .card-img { 
        width: 260px; 
        background: #eee url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=400&q=80') center/cover; 
    }
    .card-body { padding: 18px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
    .price { color: #0056b3; font-weight: 900; font-size: 1.4rem; }
    </style>
""", unsafe_allow_html=True)

# --- 4. منطق العرض ---

if not st.session_state.logged_in:
    # صفحة تسجيل الدخول
    st.markdown('<div class="header-nav"><div class="logo">معلوماتى <span style="color:#1e293b">العقارية</span></div></div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 1.2, 1])
    with col_b:
        st.markdown("<div style='margin-top:100px;'></div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#1e293b;'>دخول المنصة</h2>", unsafe_allow_html=True)
        user_input = st.text_input("اسم المستخدم", placeholder="admin")
        pass_input = st.text_input("كلمة المرور", type="password", placeholder="123")
        if st.button("دخول", use_container_width=True):
            if user_input == "admin" and pass_input == "123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("البيانات غير صحيحة")
else:
    # --- الموقع الرئيسي (نظيف تماماً من أزرار الخروج) ---
    st.markdown("""
        <div class="header-nav">
            <div class="logo">معلوماتى <span style="color:#1e293b">العقارية</span></div>
            <div class="nav-links-area">
                <a href="#" style="color:#475569; text-decoration:none; font-weight:600; font-size:0.9rem;">الرئيسية</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # قسم الهيرو
    st.markdown("""
        <div class="hero-outer">
            <div class="hero-inner">
                <h1 style="font-weight:900; font-size:2.2rem; margin-bottom:10px;">عالم العقارات في مكان واحد</h1>
                <p style="font-size:1.1rem; opacity:0.9;">أدق المعلومات عن المشاريع والمطورين في مصر</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # المحتوى الرئيسي (Wrapper 8%)
    st.markdown('<div style="padding: 0 8%;">', unsafe_allow_html=True)
    
    # شريط البحث
    st.markdown("<div style='margin-top:25px;'></div>", unsafe_allow_html=True)
    s_col1, s_col2, s_col3, s_col4 = st.columns([2, 1, 1, 0.6])
    with s_col1: st.text_input("📍 المنطقة أو المشروع", placeholder="ابحث هنا...", key="search_main", label_visibility="collapsed")
    with s_col2: st.selectbox("النوع", ["كل الأنواع", "شقة", "فيلا"], key="type_main", label_visibility="collapsed")
    with s_col3: st.selectbox("السعر", ["كل الأسعار"], key="price_main", label_visibility="collapsed")
    with s_col4: st.button("بحث", use_container_width=True)

    st.markdown("<h3 style='margin: 30px 0 20px 0; color:#1e293b; font-size:1.4rem;'>أحدث المشاريع العقارية</h3>", unsafe_allow_html=True)

    # قائمة النتائج
    col_main_list, col_spacer, col_side_info = st.columns([2.8, 0.2, 1])

    with col_main_list:
        def draw_property(price, name, loc):
            st.markdown(f"""
                <div class="project-card">
                    <div class="card-img"></div>
                    <div class="card-body">
                        <div>
                            <div class="price">{price} ج.م</div>
                            <div style="font-weight: 700; font-size: 1.15rem; color: #1e293b;">{name}</div>
                            <div style="color:#64748b; font-size:0.9rem; margin-top:4px;">📍 {loc}</div>
                        </div>
                        <div style="text-align: left;">
                            <button style="background:white; border:1px solid #0056b3; color:#0056b3; padding:6px 16px; border-radius:5px; font-weight:700; cursor:pointer; font-size:0.85rem;">التفاصيل</button>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        draw_property("9,200,000", "كمبوند ايفوري جولي - الشيخ زايد", "الشيخ زايد الجديدة")
        draw_property("6,450,000", "ذا بروكس - التجمع الخامس", "القاهرة الجديدة")

    with col_side_info:
        st.markdown("""
            <div style="background: white; padding: 20px; border-radius: 10px; border: 1px solid #e2e8f0;">
                <h4 style="color:#0056b3; font-size:1.1rem; margin-bottom:15px;">دليل المحترفين</h4>
                <p style="font-size:0.85rem; color:#475569; line-height:1.8;">
                    مرحباً بك في منصتك الخاصة. تصفح المشاريع والأسعار المحدثة لحظة بلحظة.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
