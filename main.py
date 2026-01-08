import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. التنسيق (CSS) - الهيدر والستايل العام
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* تنظيف الواجهة */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background-color: #f8fafc !important;
    }

    /* --- الهيدر العلوي الجديد --- */
    .top-header {
        background: #ffffff;
        height: 70px;
        padding: 0 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #f1f5f9;
        position: sticky;
        top: 0;
        z-index: 1001;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }

    .header-right {
        display: flex;
        align-items: center;
        gap: 30px;
    }

    .header-left {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .main-logo {
        color: #0056b3;
        font-weight: 900;
        font-size: 1.6rem;
        text-decoration: none;
    }

    .nav-link {
        color: #475569;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.95rem;
        transition: 0.2s;
    }
    .nav-link:hover {
        color: #0056b3;
    }

    .btn-login {
        background: #f1f5f9;
        color: #1e293b;
        padding: 8px 20px;
        border-radius: 8px;
        font-weight: 700;
        text-decoration: none;
        font-size: 0.9rem;
    }

    .btn-add-unit {
        background: #0056b3;
        color: white !important;
        padding: 8px 20px;
        border-radius: 8px;
        font-weight: 700;
        text-decoration: none;
        font-size: 0.9rem;
    }

    /* --- شريط البحث والكروت --- */
    .search-box {
        background: white;
        padding: 30px 60px;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 30px;
    }

    .property-card {
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
        display: flex;
        height: 200px;
        overflow: hidden;
        transition: 0.3s;
    }
    .property-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }

    .img-box {
        width: 280px;
        background-color: #f1f5f9;
        background-image: url('https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80');
        background-size: cover;
    }

    .info-box {
        padding: 20px;
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .price-txt { color: #0056b3; font-weight: 900; font-size: 1.5rem; }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر العلوي (The Header)
st.markdown("""
    <div class="top-header">
        <div class="header-right">
            <a href="#" class="main-logo">معلوماتى <span style="color:#1e293b">العقارية</span></a>
            <a href="#" class="nav-link">عقارات للبيع</a>
            <a href="#" class="nav-link">دليل المطورين</a>
            <a href="#" class="nav-link">أسعار المناطق</a>
        </div>
        <div class="header-left">
            <a href="#" class="btn-login">تسجيل الدخول</a>
            <a href="#" class="btn-add-unit">+ أضف إعلانك</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. شريط البحث (Search Section)
st.markdown('<div class="search-box">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([2.5, 1, 1, 0.6])
with c1: st.text_input("📍 المدينة، المنطقة أو المشروع...", placeholder="ابحث في التجمع، زايد، العاصمة...")
with c2: st.selectbox("نوع العقار", ["الكل", "شقق", "فيلات", "تجاري"])
with c3: st.selectbox("نطاق السعر", ["الكل", "1-3 مليون", "3-7 مليون", "+10 مليون"])
with c4: st.markdown('<button style="width:100%; height:45px; margin-top:28px; background:#0056b3; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">بحث</button>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 5. المحتوى الرئيسي
col_main, col_sidebar = st.columns([3, 1], gap="large")

with col_main:
    def card(price, title, loc):
        st.markdown(f"""
            <div class="property-card">
                <div class="img-box"></div>
                <div class="info-box">
                    <div>
                        <div class="price-txt">{price} ج.م</div>
                        <div style="font-weight:700; font-size:1.2rem; color:#1e293b;">{title}</div>
                        <div style="color:#64748b; font-size:0.9rem; margin-top:5px;">📍 {loc}</div>
                    </div>
                    <div style="text-align: left;">
                        <button style="background:none; border:1px solid #0056b3; color:#0056b3; padding:6px 15px; border-radius:5px; font-weight:600; cursor:pointer;">عرض التفاصيل</button>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    card("9,500,000", "فيلا تاون هاوس في كمبوند ايفوري جولي", "الشيخ زايد الجديدة")
    card("6,200,000", "شقة للبيع في ذا بروكس التجمع الخامس", "القاهرة الجديدة")

with col_sidebar:
    st.markdown("""
        <div style="background:white; padding:20px; border-radius:12px; border:1px solid #e2e8f0;">
            <h5 style="color:#0056b3; margin-bottom:15px;">إحصائيات السوق</h5>
            <p style="font-size:0.85rem; color:#64748b; line-height:1.6;">
                متوسط سعر المتر في التجمع: <b>28,500 ج.م</b><br>
                متوسط سعر المتر في زايد: <b>24,200 ج.م</b>
            </p>
        </div>
    """, unsafe_allow_html=True)
