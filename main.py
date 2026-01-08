import streamlit as st

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. التصميم الملكي (الـ CSS المعتمد بتاعك 100%)
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* إخفاء عناصر ستريمليت الإفتراضية */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    .block-container { padding-top: 0rem !important; padding-bottom: 2rem !important; padding-left: 0rem !important; padding-right: 0rem !important; }
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
        background-color: #f4f7fa !important;
    }

    /* الهيدر الملكي */
    .header-nav {
        background: white; height: 75px; padding: 0 8%; display: flex;
        justify-content: space-between; align-items: center;
        border-bottom: 2px solid #e2e8f0; position: sticky; top: 0; z-index: 1000;
    }
    .logo-container { display: flex; align-items: center; gap: 12px; }
    .logo-main { color: #003366; font-weight: 900; font-size: 1.8rem; }
    .logo-sub { color: #D4AF37; font-weight: 700; font-size: 1.8rem; }

    /* الهيرو */
    .hero-outer { padding: 0 8%; margin-top: 10px; }
    .hero-inner {
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=1200');
        background-size: cover; background-position: center; height: 320px;
        border-radius: 12px; display: flex; flex-direction: column;
        justify-content: center; align-items: center; color: white;
    }

    /* كروت الشركات (تصميم ناوي الفخم) */
    .project-card {
        background: white; border-radius: 12px; border: 1px solid #e2e8f0;
        display: flex; height: 120px; margin-bottom: 15px; overflow: hidden;
        transition: 0.3s; padding: 0 20px; align-items: center;
    }
    .project-card:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    
    .dev-info { flex: 1; margin-right: 20px; }
    .dev-name { color: #003366; font-weight: 900; font-size: 1.4rem; }
    .dev-tag { color: #64748b; font-size: 0.9rem; }
    
    .btn-details {
        background: #003366; color: white; border: none; padding: 10px 25px;
        border-radius: 8px; font-weight: 700; cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة تسجيل الدخول
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # صفحة الدخول
    st.markdown('<div class="header-nav"><div class="logo-container"><div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div></div></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.markdown("<div style='margin-top:80px;'></div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#003366;'>دخول المنصة</h2>", unsafe_allow_html=True)
        user = st.text_input("اسم المستخدم")
        pwd = st.text_input("كلمة المرور", type="password")
        if st.button("دخول الآن", use_container_width=True):
            if user == "admin" and pwd == "123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
else:
    # 4. محتوى المنصة الرئيسي
    st.markdown("""
        <div class="header-nav">
            <div class="logo-container">
                <div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div>
            </div>
            <div style="font-weight:600; color:#475569;">الرئيسية</div>
        </div>
        <div class="hero-outer">
            <div class="hero-inner">
                <h1 style="font-weight:900; font-size:2.5rem;">بوابتك لأدق البيانات العقارية</h1>
                <p style="font-size:1.2rem; opacity:0.9;">قائمة المطورين المعتمدين من موقع ناوي</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # قائمة الشركات (الداتا اللي سحبناها)
    developers = [
        "أورا (Ora Developers)", "سوديك (SODIC)", "إعمار مصر (Emaar)", 
        "طلعت مصطفى (TMG)", "ماونتن فيو (Mountain View)", "بالم هيلز (Palm Hills)", 
        "نيو جيزة (New Giza)", "مصر إيطاليا", "تاج مصر", "الأهلي صبور"
    ]

    st.markdown('<div style="padding: 0 8%; margin-top:30px;">', unsafe_allow_html=True)
    
    for dev in developers:
        st.markdown(f"""
            <div class="project-card">
                <div style="width:60px; height:60px; background:#f0f2f6; border-radius:50%; display:flex; align-items:center; justify-content:center;">
                    <i class="fa-solid fa-building" style="color:#003366; font-size:1.5rem;"></i>
                </div>
                <div class="dev-info">
                    <div class="dev-name">{dev}</div>
                    <div class="dev-tag">مطور عقاري معتمد - السوق المصري</div>
                </div>
                <button class="btn-details">عرض المشاريع</button>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
