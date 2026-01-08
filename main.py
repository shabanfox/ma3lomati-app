import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. حالة الجلسة (للتأمين)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 3. الـ CSS الملكي المطور (نسخة 2026)
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    .block-container { padding: 0rem !important; }
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
        background-color: #f8fafc !important;
    }

    /* الهيدر الفخم */
    .header-nav {
        background: white; height: 80px; padding: 0 8%; display: flex;
        justify-content: space-between; align-items: center;
        border-bottom: 3px solid #f1f5f9; position: sticky; top: 0; z-index: 1000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }
    .logo-main { color: #003366; font-weight: 900; font-size: 2rem; }
    .logo-sub { color: #D4AF37; font-weight: 700; }

    /* منطقة الهيرو */
    .hero-outer { padding: 0 8%; margin-top: 20px; }
    .hero-inner {
        background-image: linear-gradient(rgba(0,51,102,0.7), rgba(0,51,102,0.7)), 
        url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=1200');
        background-size: cover; background-position: center; height: 280px;
        border-radius: 20px; display: flex; flex-direction: column;
        justify-content: center; align-items: center; color: white;
        box-shadow: 0 10px 30px rgba(0,51,102,0.1);
    }

    /* كروت الشركات المطورّة */
    .dev-card {
        background: white; border-radius: 15px; border: 1px solid #e2e8f0;
        display: flex; padding: 20px 30px; margin-bottom: 12px;
        align-items: center; transition: all 0.3s ease;
    }
    .dev-card:hover { 
        transform: translateX(-10px); 
        border-right: 5px solid #D4AF37;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    .dev-icon {
        width: 55px; height: 55px; background: #f0f7ff; 
        border-radius: 12px; display: flex; align-items: center; 
        justify-content: center; margin-left: 20px;
    }
    .dev-name { color: #1e293b; font-weight: 700; font-size: 1.4rem; flex: 1; }
    
    .btn-view {
        background: #003366; color: white; border: none; padding: 10px 25px;
        border-radius: 10px; font-weight: 700; cursor: pointer; transition: 0.2s;
    }
    .btn-view:hover { background: #D4AF37; }

    /* تنسيق شريط البحث */
    .stTextInput input {
        border-radius: 12px !important; border: 2px solid #e2e8f0 !important;
        padding: 12px !important; font-family: 'Cairo' !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. قاعدة بيانات المطورين (ناوي المحدثة)
all_developers = [
    "أورا العقارية (Ora Developers)", "سوديك (SODIC)", "إعمار مصر (Emaar)", 
    "مجموعة طلعت مصطفى (TMG)", "ماونتن فيو (Mountain View)", "بالم هيلز (Palm Hills)", 
    "نيو جيزة (New Giza)", "مصر إيطاليا العقارية", "تاج مصر (Taj Misr)", 
    "الأهلي صبور (LMD)", "تطوير مصر (Tatweer Misr)", "لافيردي (La Verde)",
    "هايد بارك (Hyde Park)", "المراسم الدولية", "أوراسكوم للتنمية",
    "سيتي إيدج (City Edge)", "مباني إدريس", "إنرشيا (Inertia)", 
    "رؤية العقارية (Rooya Group)", "سكاي أبوظبي"
]

# 5. منطق البرنامج
if not st.session_state.logged_in:
    # صفحة الدخول
    st.markdown('<div class="header-nav"><div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div style='margin-top:100px;'></div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#003366; font-weight:900;'>دخول المنصة الآمن</h2>", unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم", placeholder="admin")
        p = st.text_input("كلمة المرور", type="password", placeholder="123")
        if st.button("دخول الآن", use_container_width=True):
            if u == "admin" and p == "123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("البيانات التي أدخلتها غير صحيحة.")
else:
    # الصفحة الرئيسية بعد الدخول
    st.markdown("""
        <div class="header-nav">
            <div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div>
            <div style="font-weight:600; color:#475569; border:1px solid #e2e8f0; padding:5px 15px; border-radius:20px;">الرئيسية</div>
        </div>
        <div class="hero-outer">
            <div class="hero-inner">
                <h1 style="font-weight:900; font-size:2.8rem; margin-bottom:5px;">بوابتك لأدق البيانات العقارية</h1>
                <p style="font-size:1.3rem; opacity:0.9;">استعراض كامل لكبار المطورين في السوق المصري</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # منطقة البحث والفلترة
    st.markdown('<div style="padding: 0 8%; margin-top:30px;">', unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 ابحث عن اسم المطور العقاري...", placeholder="مثال: سوديك أو إعمار")
    
    st.markdown(f"<h3 style='color:#003366; margin: 30px 0 20px 0;'>قائمة المطورين ({len(all_developers)} شركة)</h3>", unsafe_allow_html=True)

    # فلترة النتائج بناءً على البحث
    filtered_devs = [d for d in all_developers if search_query.lower() in d.lower()]

    if filtered_devs:
        for dev in filtered_devs:
            st.markdown(f"""
                <div class="dev-card">
                    <div class="dev-icon">
                        <i class="fa-solid fa-city" style="color:#003366; font-size:1.4rem;"></i>
                    </div>
                    <div class="dev-name">{dev}</div>
                    <button class="btn-view">عرض ملف الشركة</button>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("عذراً، لم يتم العثور على شركات تطابق بحثك.")
    
    st.markdown('</div>', unsafe_allow_html=True)
