import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="معلومات البروكر | عقارماب ستايل", layout="wide")

# 2. تصميم عقارماب (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* الأساسيات للعربية */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        direction: RTL;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background-color: #f7f8fa !important; /* خلفية عقارماب */
    }

    /* إخفاء الزوائد */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}

    /* الهيدر الثابت */
    .aqarmap-header {
        background-color: white;
        padding: 15px 40px;
        border-bottom: 1px solid #e0e0e0;
        position: sticky;
        top: 0;
        z-index: 1000;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .aqarmap-logo {
        font-size: 1.8rem;
        font-weight: 900;
        color: #1e3a8a; /* أزرق عقارماب */
    }

    /* فلتر السايد بار */
    [data-testid="stSidebar"] {
        background-color: white !important;
        border-left: 1px solid #e0e0e0;
        box-shadow: -2px 0 8px rgba(0,0,0,0.02);
        padding-top: 20px;
    }
    .sidebar-title {
        color: #1e3a8a;
        font-weight: 700;
        margin-bottom: 20px;
        font-size: 1.3rem;
        text-align: center;
    }

    /* كروت المشاريع (Aqarmap Card) */
    .aqarmap-project-card {
        background: white;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .aqarmap-project-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-5px);
    }

    .project-image {
        width: 100%;
        height: 180px;
        object-fit: cover;
        border-bottom: 1px solid #e0e0e0;
    }
    .project-details {
        padding: 15px;
    }
    .project-price {
        color: #1e3a8a;
        font-weight: 900;
        font-size: 1.2rem;
        margin-bottom: 8px;
    }
    .project-name {
        font-weight: 700;
        font-size: 1rem;
        color: #333;
        margin-bottom: 5px;
    }
    .project-location {
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Tabs Customization (Aqarmap Style) */
    .stTabs [data-testid="stTab"] {
        background-color: #f0f2f5;
        color: #333;
        border-radius: 8px 8px 0 0;
        margin: 0 5px;
        padding: 10px 20px;
        font-weight: 700;
        transition: all 0.2s ease;
    }
    .stTabs [data-testid="stTab"][aria-selected="true"] {
        background-color: white;
        color: #1e3a8a;
        border-bottom: 3px solid #1e3a8a;
    }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر (عقارماب)
st.markdown('<div class="aqarmap-header"><div class="aqarmap-logo">معلومات البروكر</div><small>منصة احترافية</small></div>', unsafe_allow_html=True)

# 4. السايد بار (فلتر عقارماب)
with st.sidebar:
    st.markdown('<div class="sidebar-title">تصفية البحث</div>', unsafe_allow_html=True)
    st.text_input("ابحث عن مطور أو مشروع")
    st.multiselect("المناطق", ["القاهرة الجديدة", "العاصمة الإدارية", "أكتوبر", "الشيخ زايد", "المعادي", "مدينة نصر"])
    st.selectbox("نوع العقار", ["كل الأنواع", "سكني", "تجاري", "إداري"])
    st.slider("نطاق السعر (مليون جنيه)", 1, 30, (3, 15))
    st.button("تطبيق الفلاتر", use_container_width=True)

# 5. المحتوى الرئيسي (كروت المشاريع)
st.markdown('<div style="padding: 20px 40px;">', unsafe_allow_html=True) # padding للمحتوى عشان ميكنش لازق في الأطراف

st.subheader("أحدث المشاريع العقارية")

# التبويبات زي عقارماب (مثلاً: مشاريع سكنية، تجارية)
tab_residential, tab_commercial = st.tabs(["مشاريع سكنية", "مشاريع تجارية"])

with tab_residential:
    # شبكة كروت المشاريع (3 أعمدة)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div class="aqarmap-project-card">
                <img src="https://via.placeholder.com/400x180?text=Project+Image" class="project-image">
                <div class="project-details">
                    <div class="project-price">5,800,000 ج.م</div>
                    <div class="project-name">كمبوند ذا سكوير</div>
                    <div class="project-location">📍 القاهرة الجديدة</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="aqarmap-project-card">
                <img src="https://via.placeholder.com/400x180?text=Project+Image" class="project-image">
                <div class="project-details">
                    <div class="project-price">7,200,000 ج.م</div>
                    <div class="project-name">كمبوند لافيستا سيتي</div>
                    <div class="project-location">📍 العاصمة الإدارية</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="aqarmap-project-card">
                <img src="https://via.placeholder.com/400x180?text=Project+Image" class="project-image">
                <div class="project-details">
                    <div class="project-price">4,500,000 ج.م</div>
                    <div class="project-name">أب فيلاز - Upville</div>
                    <div class="project-location">📍 مدينة 6 أكتوبر</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    # تقدر تضيف المزيد من الكروت بنفس الطريقة

with tab_commercial:
    st.info("لا توجد مشاريع تجارية حالياً.")

st.markdown('</div>', unsafe_allow_html=True) # قفلة الـ padding
