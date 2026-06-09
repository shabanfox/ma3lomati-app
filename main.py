import streamlit as st

# 1. إعدادات الصفحة (يجب أن تكون أول أمر)
st.set_page_config(
    page_title="Real Invest Mockup",
    layout="wide", # استخدام عرض الصفحة بالكامل
    initial_sidebar_state="collapsed"
)

# 2. تعريف ملفات الـ CSS والخطوط للحصول على التصميم الأنيق
# تم استخراج الأكواد اللونية من الصورة: الكحلي: #0F1A2A، الذهبي: #D19F41
style = """
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
<style>
/* إعدادات الخطوط العامة */
* {
    font-family: 'Cairo', sans-serif;
}

/* إخفاء هوامش Streamlit الافتراضية وجعل الخلفية بيضاء */
[data-testid="stAppViewContainer"] {
    background-color: white;
    padding: 0;
}
[data-testid="stHeader"] {
    display: none;
}
.block-container {
    padding-top: 0rem;
    padding-bottom: 0rem;
    padding-left: 0rem;
    padding-right: 0rem;
}

/* الألوان المتغيرة */
:root {
    --navy: #0F1A2A;
    --gold: #D19F41;
    --text-dark: #333;
}

/* --- الشريط العلوي (Top Bar) --- */
.top-bar {
    background-color: var(--navy);
    color: white;
    padding: 10px 10%;
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    direction: rtl; /* لغة عربية من اليمين لليسار */
}
.top-bar a {
    color: white;
    text-decoration: none;
    margin-right: 15px;
}
.social-icons a {
    color: var(--gold);
    margin-left: 10px;
    font-size: 16px;
}

/* --- شريط التنقل (Navbar) --- */
.navbar {
    background-color: white;
    padding: 15px 10%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    direction: rtl;
}
.logo-area {
    display: flex;
    align-items: center;
}
.logo-icon {
    color: var(--gold);
    font-size: 32px;
    margin-left: 10px;
}
.logo-text {
    color: var(--navy);
    font-weight: 700;
    font-size: 24px;
}
.menu-items {
    display: flex;
}
.menu-items a {
    color: var(--text-dark);
    text-decoration: none;
    margin-right: 25px;
    font-weight: 400;
}
.menu-items a.active {
    font-weight: 700;
    border-bottom: 2px solid var(--navy);
}
.lang-switch {
    border: 1px solid var(--navy);
    padding: 5px 15px;
    border-radius: 5px;
    color: var(--navy);
    cursor: pointer;
}

/* --- قسم الهيرو (Hero Section) --- */
.hero-container {
    padding: 0 10%;
    position: relative;
    overflow: hidden;
}

/* محاكاة الخلفية المائلة الكحلية */
.hero-bg-angled {
    position: absolute;
    top: 0;
    right: 45%; /* تبدأ الكتلة الكحلية من المنتصف تقريباً */
    width: 100%;
    height: 100%;
    background-color: var(--navy);
    transform: skewX(-15deg); /* ميلان */
    z-index: 1;
}

.hero-content-wrapper {
    display: flex;
    position: relative;
    z-index: 2; /* فوق الخلفية المائلة */
    padding: 50px 0;
    direction: rtl;
}

.hero-text {
    width: 50%;
    color: var(--text-dark);
    padding-left: 50px;
}
.hero-text p.sub-title {
    color: var(--gold);
    font-weight: 700;
    font-size: 16px;
    margin-bottom: 5px;
}
.hero-text h1 {
    color: var(--navy);
    font-size: 48px;
    font-weight: 700;
    margin-bottom: 15px;
}
.hero-text p.description {
    font-size: 18px;
    line-height: 1.6;
    margin-bottom: 30px;
    color: #555;
}

.hero-image-area {
    width: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
}
.main-building-img {
    max-width: 90%;
    border-radius: 10px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

/* --- زر الاتصال الأنيق --- */
.cta-button {
    background-color: var(--gold);
    color: white !important;
    padding: 12px 24px;
    border-radius: 5px;
    text-decoration: none;
    font-weight: 700;
    display: inline-flex;
    align-items: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.cta-button:hover {
    background-color: #e2b74f;
}

/* --- قسم العناصر التوضيحية (الترس، الرافعة، إلخ) --- */
.illustrations-container {
    background-color: #f9f9f9;
    padding: 50px 10%;
    direction: rtl;
}
.ill-row {
    display: flex;
    justify-content: space-around;
    align-items: center;
    text-align: center;
}
.ill-item {
    width: 20%;
}
.ill-icon {
    font-size: 60px;
    margin-bottom: 15px;
}
.ill-title {
    font-weight: 700;
    color: var(--navy);
    margin-bottom: 5px;
}
.ill-desc {
    color: #666;
    font-size: 14px;
}

/* ألوان مخصصة للأيقونات التوضيحية */
.icon-navy { color: var(--navy); }
.icon-gold { color: var(--gold); }

</style>
"""

# حقن الـ CSS في التطبيق
st.markdown(style, unsafe_allow_html=True)

# ----------------------------------------
# 3. بناء هيكل الـ HTML في Streamlit
# ----------------------------------------

# أ. الشريط العلوي (Top Bar)
st.markdown("""
<div class="top-bar">
    <div class="social-icons">
        <a href="#">📷</a> <a href="#">📘</a> <a href="#">🐦</a> </div>
    <div>
        <span>info@takwen.net ✉️</span>
        <span style="margin-right: 15px;">0020101852747 📞</span>
        <span style="margin-right: 20px; font-weight:700;">مرحبا بكم في ريل إنفست</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ب. شريط التنقل (Navbar)
st.markdown("""
<div class="navbar">
    <div class="lang-switch">
        العربية ⬇️
    </div>
    <div class="menu-items">
        <a href="#">اتصل بنا</a>
        <a href="#">مشاريعنا</a>
        <a href="#">من نحن</a>
        <a href="#" class="active">الرئيسية</a>
    </div>
    <div class="logo-area">
        <span class="logo-text">Real Invest</span>
        <span class="logo-icon">🏢</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ج. قسم الهيرو (Hero Section)
# نستخدم حاوية واحدة HTML للتعامل مع الخلفية المائلة
hero_html = """
<div class="hero-container">
    <div class="hero-bg-angled"></div>
    <div class="hero-content-wrapper">
        <div class="hero-image-area">
            <img src="https://images.unsplash.com/photo-1570129477492-45c003edd2be?q=80&w=800&auto=format&fit=crop" class="main-building-img">
        </div>
        <div class="hero-text">
            <p class="sub-title">مرحبا بكم في ريل إنفست</p>
            <h1>ريل إنفست</h1>
            <p class="description">تم تأسيس الشركة للنجاح في التسويق والاستثمار العقاري. نحن نقدم حلولاً عقارية متكاملة تلبي احتياجاتكم السكنية والاستثمارية بأعلى معايير الجودة.</p>
            <a href="#" class="cta-button">
                اضغط للاتصال 📞 0020101852747
            </a>
        </div>
    </div>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

# د. محاكاة العناصر التوضيحية (الرسومات المحيطة بالأجهزة)
# بما أننا نستخدم Streamlit، سنقوم بعرض هذه العناصر كقسم سفلي توضيحي
st.markdown('<div class="illustrations-container">', unsafe_allow_html=True)
st.markdown('<h2 style="text-align:center; color: #0F1A2A; margin-bottom:40px;">خدماتنا ومنهجية العمل</h2>', unsafe_allow_html=True)

ill_row_html = """
<div class="ill-row">
    <div class="ill-item">
        <div class="ill-icon icon-navy">🏗️</div>
        <div class="ill-title">تطوير عقاري</div>
        <div class="ill-desc">بناء وتطوير مشاريع سكنية وتجارية حديثة.</div>
    </div>
    <div class="ill-item">
        <div class="ill-icon icon-gold">⚙️</div>
        <div class="ill-title">إدارة أملاك</div>
        <div class="ill-desc">آليات عمل دقيقة لتعظيم عائد استثمارك.</div>
    </div>
    <div class="ill-item">
        <div class="ill-icon icon-navy">💡</div>
        <div class="ill-title">استشارات</div>
        <div class="ill-desc">أفكار وحلول ذكية للسوق العقاري.</div>
    </div>
    <div class="ill-item">
        <div class="ill-icon icon-gold">🌿</div>
        <div class="ill-title">تصميم بيئي</div>
        <div class="ill-desc">لمسة طبيعية في كافة مشاريعنا.</div>
    </div>
</div>
"""
st.markdown(ill_row_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 4. تذييل بسيط
st.markdown("""
<div style="background-color: #0F1A2A; color: #aaa; text-align: center; padding: 20px; font-size: 12px; direction:rtl;">
    تكوين © 2023 | تصميم يحاكي الموكب العقاري
</div>
""", unsafe_allow_html=True)
