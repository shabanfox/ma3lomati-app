import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="بروكر هب | Broker Hub", layout="wide")

# 2. التنسيق المتقدم (CSS) - تصميم عصري ونظيف
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;500;700;900&display=swap');
    
    /* ضبط الاتجاه RTL والخط */
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background-color: #f0f2f5 !important;
    }

    /* إخفاء الزوائد */
    [data-testid="stHeader"], .stDeployButton, footer {display: none !important;}

    /* الهيدر الاحترافي */
    .top-nav {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        padding: 25px;
        color: white;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        text-align: center;
    }

    /* كروت المشاريع - تصميم ناي (Flat & Clean) */
    .prop-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }
    .prop-card:hover {
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        border-color: #3b82f6;
    }

    .status-badge {
        background: #dcfce7;
        color: #166534;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
    }

    .price-text {
        color: #1e3a8a;
        font-size: 1.3rem;
        font-weight: 900;
        margin: 10px 0;
    }

    /* قائمة البحث الجانبية */
    [data-testid="stSidebar"] {
        background-color: white !important;
        border-left: 1px solid #e5e7eb;
    }
    </style>
""", unsafe_allow_html=True)

# 3. محرك المنصة
st.markdown('<div class="top-nav"><h1>مركز معلومات البروكر المصري</h1><p>ابحث عن المطور، المشروع، والأسعار في ثواني</p></div>', unsafe_allow_html=True)

# السايد بار (البحث الذكي)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/609/609803.png", width=80)
    st.title("البحث الذكي")
    search_query = st.text_input("🔍 اسم المطور أو المشروع")
    selected_area = st.multiselect("📍 اختر المناطق", 
                                  ["التجمع الخامس", "العاصمة الإدارية", "أكتوبر", "الشيخ زايد", "المعادي", "مدينة نصر"])
    st.write("---")
    st.info("نصيحة: استخدم فلاتر المناطق لتضييق نطاق البحث.")

# تقسيم الصفحة (يمين للمشاريع | يسار لمعلومات المطور)
col_main, col_side = st.columns([2.5, 1], gap="large")

with col_side:
    st.markdown("### 🏢 ملف المطور")
    with st.container():
        st.markdown("""
            <div style="background:white; padding:20px; border-radius:15px; border-right:5px solid #3b82f6;">
                <h4>شركة PRE Developments</h4>
                <p style="font-size:0.9rem; color:#6b7280;">واحدة من أكبر الشركات العقارية في مصر، تشتهر بمشاريعها في التجمع وأكتوبر.</p>
                <hr>
                <b>رئيس مجلس الإدارة:</b> أ/ فلان الفلاني<br>
                <b>تاريخ التأسيس:</b> 2010
            </div>
        """, unsafe_allow_html=True)

with col_main:
    st.markdown("### 🏗️ المشاريع المتاحة")
    
    # تبويبات داخلية للتنظيم
    tab1, tab2 = st.tabs(["المشاريع السكنية", "المشاريع التجارية"])
    
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
                <div class="prop-card">
                    <span class="status-badge">متاح للبيع</span>
                    <div class="price-text">6,200,000 ج.م</div>
                    <h4 style="margin:0;">كمبوند ذا بروكس</h4>
                    <p style="color:#6b7280; font-size:0.9rem;">📍 القاهرة الجديدة - التجمع</p>
                    <button style="width:100%; padding:10px; background:#1e3a8a; color:white; border:none; border-radius:8px;">تفاصيل المشروع</button>
                </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown("""
                <div class="prop-card">
                    <span class="status-badge" style="background:#fee2e2; color:#991b1b;">مباع بالكامل</span>
                    <div class="price-text">4,800,000 ج.م</div>
                    <h4 style="margin:0;">كمبوند ستون ريزيدنس</h4>
                    <p style="color:#6b7280; font-size:0.9rem;">📍 التجمع الخامس</p>
                    <button style="width:100%; padding:10px; background:#e5e7eb; color:#9ca3af; border:none; border-radius:8px;">غير متاح</button>
                </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.info("لا توجد مشاريع تجارية مسجلة لهذا المطور حالياً.")
