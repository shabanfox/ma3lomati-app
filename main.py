import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="بروكر برو | Broker Pro", layout="wide")

# 2. التنسيق الملكي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* الأساسيات وتصفير المسافات */
    [data-testid="stHeader"], .stDeployButton, footer {display: none !important;}
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background-color: #fcfcfc !important;
    }

    /* الهيدر الجديد - فخامة وبساطة */
    .hero-section {
        background-color: #0f172a; /* كحلي ملكي */
        padding: 40px;
        color: #f1f5f9;
        border-bottom: 4px solid #c49a6c; /* خط ذهبي */
        margin-bottom: 30px;
        text-align: center;
    }

    /* كروت المشاريع - عرض كامل واحترافي */
    .property-card-premium {
        background: white;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 15px;
        border: 1px solid #e2e8f0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: 0.3s;
    }
    .property-card-premium:hover {
        border-right: 8px solid #c49a6c;
        transform: scale(1.01);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
    }

    .price-badge {
        background: #f1f5f9;
        color: #0f172a;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 900;
        font-size: 1.2rem;
        border: 1px solid #cbd5e1;
    }

    .developer-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        position: sticky;
        top: 20px;
    }

    /* تخصيص السايد بار */
    [data-testid="stSidebar"] {
        background-color: #f8fafc !important;
        border-left: 1px solid #e2e8f0;
    }
    
    h1, h2, h3 { color: #0f172a; }
    </style>
""", unsafe_allow_html=True)

# 3. الهيكل (UI)
st.markdown("""
    <div class="hero-section">
        <h1 style="color:white; margin-bottom:10px;">MA3LOMATI <span style="color:#c49a6c">PRO</span></h1>
        <p style="font-size:1.1rem; opacity:0.8;">محرك بيانات العقارات للمحترفين في مصر</p>
    </div>
""", unsafe_allow_html=True)

# السايد بار للبحث
with st.sidebar:
    st.markdown("### 🔍 بحث متقدم")
    st.text_input("اسم المطور أو الكمبوند")
    st.selectbox("📍 المنطقة المستهدفة", ["القاهرة الجديدة", "العاصمة الإدارية", "الشيخ زايد", "أكتوبر"])
    st.slider("نطاق السعر (مليون ج.م)", 2, 50, (5, 20))
    st.button("تطبيق الفلاتر", use_container_width=True)

# التقسيم الرئيسي
col_main, col_info = st.columns([2.2, 1], gap="large")

with col_info:
    st.markdown("""
        <div class="developer-box">
            <small style="color:#c49a6c; font-weight:700;">ملف المطور العقاري</small>
            <h2 style="margin-top:5px;">PRE Developments</h2>
            <p style="color:#64748b; font-size:0.9rem; line-height:1.6;">
                شركة رائدة بخبرة تزيد عن 15 عاماً، تمتلك محفظة مشاريع تتجاوز الـ 10 كمبوندات في أرقى مناطق مصر.
            </p>
            <hr style="opacity:0.3">
            <div style="display:flex; justify-content:space-between;">
                <span><b>المشاريع:</b> 12</span>
                <span><b>التقييم:</b> ⭐⭐⭐⭐⭐</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_main:
    st.markdown("### 🏢 قائمة المشاريع الحالية")
    
    # نموذج لكارت مشروع فخم
    def project_card(name, location, price, status):
        st.markdown(f"""
            <div class="property-card-premium">
                <div style="flex: 2;">
                    <div style="display:flex; align-items:center; gap:10px;">
                        <h3 style="margin:0;">{name}</h3>
                        <span style="font-size:0.8rem; background:#0f172a; color:white; padding:2px 8px; border-radius:4px;">{status}</span>
                    </div>
                    <p style="color:#64748b; margin:5px 0;">📍 {location}</p>
                </div>
                <div style="text-align: left;">
                    <div class="price-badge">{price} ج.م</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    project_card("ذا بروكس - The Brooks", "التجمع الخامس - الدائري الأوسطي", "6,500,000", "سكني")
    project_card("ستون ريزيدنس - Stone Residence", "القاهرة الجديدة - مدخل التجمع", "5,200,000", "جاهز للاستلام")
    project_card("ايفوري جولي - Ivoire Zayed", "الشيخ زايد الجديدة", "9,800,000", "تحت الإنشاء")
