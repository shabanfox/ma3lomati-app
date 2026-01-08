import streamlit as st

# 1. إعدادات الصفحة واللغة العربية
st.set_page_config(page_title="منصة البروكر المصري", layout="wide")

# 2. نظام التنسيق (CSS) لدعم اللغة العربية RTL وتصميم مودرن
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء زوائد ستريمليت */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    /* ضبط الاتجاه للعربية */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        direction: RTL;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background-color: #f8f9fa;
    }

    /* الهيدر العلوي */
    .main-header {
        background-color: #1e3a8a;
        color: white;
        padding: 20px;
        text-align: center;
        border-radius: 0 0 20px 20px;
        margin-bottom: 30px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* كارت المطور */
    .dev-card {
        background: white;
        border-radius: 15px;
        padding: 20px;
        border-right: 5px solid #1e3a8a;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* كروت المشاريع */
    .project-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #e2e8f0;
        transition: 0.3s;
        text-align: right;
    }
    .project-card:hover {
        border-color: #1e3a8a;
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
    }

    .price-tag {
        color: #059669;
        font-weight: 900;
        font-size: 1.1rem;
    }
    
    /* تعديل السايد بار ليكون يمين */
    [data-testid="stSidebar"] {
        direction: RTL;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

# 3. واجهة المستخدم (UI)
st.markdown('<div class="main-header"><h1>منصة بروكر مصر 🇪🇬</h1><p>كل داتا العقارات في مكان واحد</p></div>', unsafe_allow_html=True)

# السايد بار للفلاتر
with st.sidebar:
    st.header("تصفية البحث")
    region = st.selectbox("📍 اختر المنطقة", ["كل المناطق", "القاهرة الجديدة", "العاصمة الإدارية", "أكتوبر", "الشيخ زايد", "زايد الجديدة", "المعادي", "مدينة نصر"])
    developer_search = st.text_input("🔍 ابحث عن مطور عقاري...")
    st.write("---")
    st.caption("v1.0 - أداة البروكر المحترف")

# تقسيم الشاشة (يمين للمشاريع | يسار للمطور)
col_info, col_projects = st.columns([1, 2], gap="large")

with col_info:
    st.markdown('<div class="dev-card">', unsafe_allow_html=True)
    st.subheader("شركة التطوير")
    st.write("**اسم الشركة:** سيتم العرض هنا")
    st.write("**رئيس مجلس الإدارة:** سيتم العرض هنا")
    st.write("**نبذة:** معلومات مختصرة عن تاريخ الشركة ومسابقة أعمالها.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_projects:
    st.subheader(f"المشاريع المتاحة في {region}")
    
    # مثال لشكل كارت المشروع
    p_col1, p_col2 = st.columns(2)
    
    with p_col1:
        st.markdown("""
            <div class="project-card">
                <div class="price-tag">يبدأ من 5,000,000 ج.م</div>
                <div style="font-weight:700; margin:10px 0;">اسم المشروع التجريبي</div>
                <div style="color:#64748b; font-size:0.9rem;">📍 التجمع الخامس</div>
            </div>
        """, unsafe_allow_html=True)

    with p_col2:
        st.markdown("""
            <div class="project-card">
                <div class="price-tag">يبدأ من 8,500,000 ج.م</div>
                <div style="font-weight:700; margin:10px 0;">مشروع سكني مميز</div>
                <div style="color:#64748b; font-size:0.9rem;">📍 العاصمة الإدارية</div>
            </div>
        """, unsafe_allow_html=True)
