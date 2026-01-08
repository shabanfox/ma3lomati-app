import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. تهيئة حالة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 3. دالة تسجيل الخروج (ستعمل عند الضغط على الزر في الهيدر)
def logout():
    st.session_state.logged_in = False
    st.rerun()

# 4. التنسيق (CSS) - يجمع كل اللمسات السابقة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    .block-container { padding-top: 0.5rem !important; padding-left: 0rem !important; padding-right: 0rem !important; }
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
        background-color: #f4f7fa !important;
    }

    /* الهيدر العلوي الثابت */
    .header-nav {
        background: white; height: 75px; padding: 0 8%;
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 1px solid #e2e8f0; position: sticky; top: 0; z-index: 1000;
    }
    .logo { color: #0056b3; font-weight: 900; font-size: 1.6rem; text-decoration: none; }
    
    .btn-logout {
        background: #f1f5f9; color: #ef4444 !important; padding: 8px 20px;
        border-radius: 8px; font-weight: 700; text-decoration: none; cursor: pointer; border: none;
    }

    /* منطقة الهيرو (الصورة الخلفية) */
    .hero-container {
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1470&q=80');
        background-size: cover; background-position: center; height: 350px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        color: white; margin-bottom: 40px;
    }

    /* تصميم فورم الدخول */
    .login-box {
        background: white; padding: 40px; border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        max-width: 450px; margin: 80px auto;
    }

    /* كروت المشاريع */
    .main-wrapper { padding: 0 8%; }
    .project-card {
        background: white; border-radius: 12px; border: 1px solid #e2e8f0;
        display: flex; height: 200px; margin-bottom: 20px; overflow: hidden; transition: 0.3s;
    }
    .project-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
    .card-img { width: 280px; background: #eee url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=400&q=80') center/cover; }
    .card-body { padding: 20px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
    .price { color: #0056b3; font-weight: 900; font-size: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

# --- حالة عدم تسجيل الدخول ---
if not st.session_state.logged_in:
    # هيدر بسيط لصفحة الدخول
    st.markdown("""
        <div class="header-nav">
            <div class="logo">معلوماتى <span style="color:#1e293b">العقارية</span></div>
            <div style="font-weight:600; color:#0056b3;">بوابة البروكرز المحترفين</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; color:#1e293b; margin-bottom:25px;'>سجل دخولك</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["تسجيل الدخول", "اشتراك جديد"])
    with tab1:
        email = st.text_input("البريد الإلكتروني", placeholder="admin")
        password = st.text_input("كلمة المرور", type="password", placeholder="123")
        if st.button("دخول للمنصة", use_container_width=True):
            if email == "admin" and password == "123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
    with tab2:
        st.text_input("الاسم")
        st.text_input("رقم الموبايل")
        st.button("إنشاء حساب", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- حالة تسجيل الدخول (عرض الموقع بالكامل) ---
else:
    # 1. الهيدر مع زر تسجيل الخروج الثابت فوق
    col_logo, col_logout = st.columns([5, 1]) # سنستخدم مكونات ستريمليت داخل حاوية CSS
    st.markdown(f"""
        <div class="header-nav">
            <div class="logo">معلوماتى <span style="color:#1e293b">العقارية</span></div>
            <div style="display: flex; gap: 20px; align-items: center;">
                <a href="#" style="color:#475569; text-decoration:none; font-weight:600;">الرئيسية</a>
                <a href="#" style="color:#475569; text-decoration:none; font-weight:600;">المشاريع</a>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # وضع زر الخروج في مكان ثابت (أعلى اليسار)
    with st.sidebar: # سنبقي زر الخروج في مكان واضح جداً أو نستخدم سطر برمجي
         if st.button("🔴 تسجيل خروج"):
             logout()

    # 2. قسم الهيرو (الصورة الخلفية)
    st.markdown("""
        <div class="hero-container">
            <h1 style="font-weight:900; font-size:2.8rem; margin-bottom:10px;">أهلاً بك في "معلوماتى"</h1>
            <p style="font-size:1.3rem; opacity:0.9;">أدق التفاصيل العقارية للمحترفين فقط</p>
        </div>
    """, unsafe_allow_html=True)

    # 3. محرك البحث والنتائج (داخل Wrapper المتناسق)
    st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)
    
    # شريط البحث
    c1, c2, c3, c4 = st.columns([2.5, 1, 1, 0.7])
    with c1: st.text_input("📍 المنطقة أو المشروع", placeholder="ابحث هنا...", key="s1")
    with c2: st.selectbox("النوع", ["كل الأنواع", "شقة", "فيلا"], key="s2")
    with c3: st.selectbox("الميزانية", ["الكل"], key="s3")
    with c4: st.markdown('<button style="width:100%; height:45px; margin-top:28px; background:#0056b3; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">بحث</button>', unsafe_allow_html=True)

    st.markdown("<h3 style='margin: 40px 0 20px 0; color:#1e293b;'>أحدث عروض المشاريع</h3>", unsafe_allow_html=True)

    # النتائج
    col_res, col_side = st.columns([2.8, 1], gap="large")

    with col_res:
        def draw_card(price, name, loc):
            st.markdown(f"""
                <div class="project-card">
                    <div class="card-img"></div>
                    <div class="card-body">
                        <div>
                            <div class="price">{price} ج.م</div>
                            <div style="font-weight:700; font-size:1.2rem; color:#1e293b;">{name}</div>
                            <div style="color:#64748b; font-size:0.9rem; margin-top:5px;">📍 {loc}</div>
                        </div>
                        <div style="text-align: left;">
                            <button style="background:#0056b3; color:white; border:none; padding:8px 25px; border-radius:6px; font-weight:700; cursor:pointer;">التفاصيل</button>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        draw_card("9,500,000", "ايفوري جولي - الشيخ زايد", "الشيخ زايد الجديدة")
        draw_card("6,200,000", "ذا بروكس - التجمع الخامس", "القاهرة الجديدة")
        draw_card("11,000,000", "بادية - 6 أكتوبر", "طريق الواحات")

    with col_side:
        st.markdown("""
            <div style="background:white; padding:25px; border-radius:12px; border:1px solid #e2e8f0;">
                <h5 style="color:#0056b3; margin-bottom:15px;">إحصائيات البروكر</h5>
                <p style="font-size:0.85rem; color:#64748b; line-height:1.8;">
                    • عدد المشاريع المتاحة: 450<br>
                    • تحديث الأسعار: اليوم<br>
                    • تحميلات الدليل: 120
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
