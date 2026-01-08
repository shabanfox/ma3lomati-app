import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="معلوماتى العقارية", layout="wide")

# 2. الحالة الأمنية
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 3. الـ CSS الملكي المطور (نسخة معدلة لضبط المسافات)
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* إخفاء الزوائد */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    .block-container { padding: 0rem !important; }
    
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
    .logo-main { color: #003366; font-weight: 900; font-size: 1.8rem; }
    .logo-sub { color: #D4AF37; font-weight: 700; }

    /* الهيرو */
    .hero-outer { padding: 0 8%; margin-top: 20px; }
    .hero-inner {
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=1200');
        background-size: cover; background-position: center; height: 300px;
        border-radius: 15px; display: flex; flex-direction: column;
        justify-content: center; align-items: center; color: white;
    }

    /* كروت الشركات */
    .project-card {
        background: white; border-radius: 12px; border: 1px solid #e2e8f0;
        display: flex; height: 110px; margin-bottom: 15px; padding: 0 25px;
        align-items: center; transition: 0.3s;
    }
    .project-card:hover { transform: scale(1.01); box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .dev-name { color: #003366; font-weight: 900; font-size: 1.3rem; flex: 1; }
    
    .btn-main {
        background: #003366; color: white; border: none; padding: 8px 20px;
        border-radius: 6px; font-weight: 700; cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# 4. منطق التنفيذ
if not st.session_state.logged_in:
    # --- صفحة الدخول (تظهر وحدها) ---
    st.markdown('<div class="header-nav"><div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div style='margin-top:100px;'></div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#003366;'>دخول المنصة</h2>", unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم", key="user")
        p = st.text_input("كلمة المرور", type="password", key="pass")
        if st.button("دخول", use_container_width=True):
            if u == "admin" and p == "123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("البيانات خطأ")
else:
    # --- الموقع الرئيسي (يظهر بعد الدخول) ---
    st.markdown("""
        <div class="header-nav">
            <div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div>
            <div style="font-weight:600; color:#475569;">الرئيسية</div>
        </div>
        <div class="hero-outer">
            <div class="hero-inner">
                <h1 style="font-weight:900; font-size:2.5rem;">بوابتك لأدق البيانات العقارية</h1>
                <p style="font-size:1.1rem; opacity:0.9;">مطورين عقاريين معتمدين (ناوي)</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # شريط البحث
    st.markdown('<div style="padding: 0 8%; margin-top:25px;">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1: st.text_input("بحث عن شركة...", label_visibility="collapsed")
    with c2: st.selectbox("التصنيف", ["كل الشركات"], label_visibility="collapsed")
    with c3: st.button("تحديث البيانات", use_container_width=True)

    # عرض الشركات (أهم شركات ناوي)
    developers = ["أورا (Ora)", "سوديك (SODIC)", "إعمار مصر", "بالم هيلز", "طلعت مصطفى", "ماونتن فيو", "نيوجيزة", "مصر إيطاليا"]
    
    st.markdown("<h4 style='margin: 25px 0 15px 0; color:#003366;'>قائمة المطورين</h4>", unsafe_allow_html=True)
    
    for dev in developers:
        st.markdown(f"""
            <div class="project-card">
                <div style="width:45px; height:45px; background:#f0f4f8; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-left:20px;">
                    <i class="fa-solid fa-building" style="color:#003366;"></i>
                </div>
                <div class="dev-name">{dev}</div>
                <button class="btn-main">عرض المشاريع</button>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
