import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide")

# 2. التنسيق (ألوان قوية وواضحة جداً)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* تنظيف الواجهة */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background-color: #f1f5f9 !important; /* رمادي فاتح للخلفية عشان يظهر الكروت */
    }

    /* الهيدر - كحلي غامق واضح */
    .nav-bar {
        background-color: #0f172a; /* كحلي صريح */
        padding: 20px 50px;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 0 0 15px 15px;
        margin-bottom: 30px;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    }

    /* كارت المطور - أبيض بحدود واضحة */
    .info-card {
        background: white;
        border-radius: 12px;
        padding: 25px;
        border: 2px solid #e2e8f0; /* حدود باينة */
        position: sticky;
        top: 20px;
    }

    /* كروت المشاريع - تباين عالي */
    .project-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #cbd5e1;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: 0.2s;
    }
    .project-card:hover {
        border-color: #2563eb;
        background-color: #f8fafc;
    }

    /* السعر - لون أزرق براند قوي */
    .price-box {
        background-color: #2563eb;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 900;
        font-size: 1.3rem;
        min-width: 150px;
        text-align: center;
    }

    .project-name {
        color: #1e293b;
        font-weight: 700;
        font-size: 1.2rem;
        margin: 0;
    }

    .location-text {
        color: #475569;
        font-size: 0.95rem;
        margin-top: 5px;
    }

    /* تعديل الفلاتر */
    .stSelectbox div[data-baseweb="select"] {
        background-color: white !important;
        border: 1px solid #cbd5e1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. محتوى الصفحة
st.markdown("""
    <div class="nav-bar">
        <h2 style="margin:0; color:white;">MA3LOMATI <span style="color:#60a5fa">PRO</span></h2>
        <div style="font-weight:600;">لوحة تحكم البروكر</div>
    </div>
""", unsafe_allow_html=True)

# التقسيم (يمين للمشاريع | يسار للمطور)
col_projects, col_dev = st.columns([2.5, 1], gap="large")

with col_dev:
    st.markdown("""
        <div class="info-card">
            <h3 style="color:#0f172a; border-bottom: 2px solid #60a5fa; padding-bottom:10px;">🏢 بيانات المطور</h3>
            <p style="font-weight:700; color:#2563eb; margin-bottom:5px;">PRE Developments</p>
            <p style="color:#475569; font-size:0.95rem; line-height:1.6;">
                واحدة من أكبر شركات التطوير العقاري في مصر، متخصصة في المشاريع السكنية والتجارية الفاخرة.
            </p>
            <div style="background:#f1f5f9; padding:10px; border-radius:8px; margin-top:15px;">
                <small>رئيس مجلس الإدارة:</small><br>
                <b>أ/ فلان الفلاني</b>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_projects:
    st.markdown("### 🏗️ المشاريع المتاحة")
    
    # دالة لرسم كارت المشروع بتباين عالي
    def draw_luxury_card(title, location, price):
        st.markdown(f"""
            <div class="project-card">
                <div>
                    <h4 class="project-name">{title}</h4>
                    <div class="location-text">📍 {location}</div>
                </div>
                <div class="price-box">
                    {price} ج.م
                </div>
            </div>
        """, unsafe_allow_html=True)

    draw_luxury_card("كمبوند ذا بروكس", "القاهرة الجديدة - التجمع الخامس", "6,500,000")
    draw_luxury_card("ستون ريزيدنس", "التجمع الخامس - الدائري", "5,200,000")
    draw_luxury_card("ايفوري جولي", "الشيخ زايد الجديدة", "9,800,000")

# الفلاتر الجانبية
with st.sidebar:
    st.title("🔍 بحث سريع")
    st.selectbox("اختر المطور", ["PRE Developments", "Sodic", "Hassan Allam"])
    st.multiselect("اختر المنطقة", ["التجمع", "زايد", "العاصمة", "أكتوبر"])
    st.button("بحث الآن", use_container_width=True)
