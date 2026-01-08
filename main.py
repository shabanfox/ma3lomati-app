import streamlit as st

# 1. الإعدادات الأساسية (ممنوع وضع أي كود قبل هذا السطر)
st.set_page_config(page_title="معلوماتى العقارية", layout="wide")

# 2. حماية الدخول
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 3. الـ CSS (نفس استايلك الملكي بس بتنسيق برمجي صحيح)
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    .block-container { padding: 0rem !important; }
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
        background-color: #f4f7fa !important;
    }

    .header-nav {
        background: white; height: 75px; padding: 0 8%; display: flex;
        justify-content: space-between; align-items: center;
        border-bottom: 2px solid #e2e8f0; position: sticky; top: 0; z-index: 1000;
    }
    .logo-container { display: flex; align-items: center; gap: 12px; }
    .logo-main { color: #003366; font-weight: 900; font-size: 1.8rem; }
    .logo-sub { color: #D4AF37; font-weight: 700; }

    .hero-outer { padding: 0 8%; margin-top: 15px; }
    .hero-inner {
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=1200');
        background-size: cover; background-position: center; height: 320px;
        border-radius: 12px; display: flex; flex-direction: column;
        justify-content: center; align-items: center; color: white;
    }

    .project-card {
        background: white; border-radius: 12px; border: 1px solid #e2e8f0;
        display: flex; height: 190px; margin-bottom: 15px; overflow: hidden;
    }
    .card-img { width: 260px; background-size: cover; background-position: center; }
    .card-body { padding: 20px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
    .price { color: #003366; font-weight: 900; font-size: 1.4rem; }
    .btn-details { background:#003366; border:none; color:white; padding:8px 20px; border-radius:6px; font-weight:700; cursor:pointer; }
    
    /* ستايل فورم الدخول */
    .login-box { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); margin-top: 50px; }
    </style>
""", unsafe_allow_html=True)

# 4. منطق العرض (دخول أم منصة)
if not st.session_state.logged_in:
    # --- صفحة الدخول ---
    st.markdown('<div class="header-nav"><div class="logo-container"><div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div></div></div>', unsafe_allow_html=True)
    
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#003366; font-weight:900;'>دخول المنصة</h2>", unsafe_allow_html=True)
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        if st.button("تسجيل الدخول", use_container_width=True):
            if username == "admin" and password == "123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("البيانات خاطئة، حاول مرة أخرى")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- المنصة الرئيسية ---
    st.markdown("""
        <div class="header-nav">
            <div class="logo-container">
                <div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div>
            </div>
            <div style="color:#475569; font-weight:600;">الرئيسية</div>
        </div>
        <div class="hero-outer">
            <div class="hero-inner">
                <h1 style="font-weight:900; font-size:2.5rem;">بوابتك لأدق البيانات العقارية</h1>
                <p style="font-size:1.2rem; opacity:0.9;">أهلاً بك في المرجع الأول للعقارات في مصر</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="padding: 0 8%; margin-top:30px;">', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#003366; margin-bottom:20px;'>المطورين المعتمدين</h3>", unsafe_allow_html=True)

    # قائمة الشركات
    devs = ["أورا (Ora)", "سوديك (SODIC)", "إعمار مصر", "طلعت مصطفى", "بالم هيلز"]

    for d in devs:
        st.markdown(f"""
            <div class="project-card">
                <div class="card-img" style="background-image: url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400');"></div>
                <div class="card-body">
                    <div>
                        <div class="price">مطور معتمد</div>
                        <div style="font-weight: 700; font-size: 1.2rem; color: #1e293b; margin-top:5px;">{d}</div>
                        <div style="color:#64748b; font-size:0.95rem; margin-top:5px;">📍 متاح كامل المشروعات بموقع ناوي</div>
                    </div>
                    <div style="text-align: left;"><button class="btn-details">عرض المشاريع</button></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
