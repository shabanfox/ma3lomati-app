import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. هندسة التصميم (Aqarmap Logic)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* ضبط الاتجاه RTL واللغة */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background-color: #f9fafb !important;
    }

    /* هيدر المنصة */
    .nav-wrapper {
        background: white;
        padding: 15px 50px;
        border-bottom: 2px solid #edeff2;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky; top: 0; z-index: 999;
    }
    .brand-logo {
        color: #0046be; /* أزرق عقارماب الشهير */
        font-weight: 900;
        font-size: 1.6rem;
        letter-spacing: -1px;
    }

    /* شريط البحث العرضي (Horizontal Search Bar) */
    .search-section {
        background: white;
        padding: 30px 50px;
        border-bottom: 1px solid #e5e7eb;
        margin-bottom: 30px;
    }

    /* كارت المشروع (Aqarmap Rectangular Card) */
    .aqar-card-v2 {
        background: white;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 16px;
        display: flex;
        transition: 0.2s;
        height: 200px;
        overflow: hidden;
    }
    .aqar-card-v2:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-color: #0046be;
    }

    .card-photo {
        width: 280px;
        background-color: #f3f4f6;
        background-image: url('https://via.placeholder.com/280x200?text=معلوماتى+العقارية');
        background-size: cover;
    }

    .card-content {
        padding: 20px;
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .price-label {
        color: #0046be;
        font-weight: 900;
        font-size: 1.5rem;
    }

    .proj-name {
        font-size: 1.25rem;
        font-weight: 700;
        color: #111827;
        margin-top: 5px;
    }

    .loc-label {
        color: #6b7280;
        font-size: 0.95rem;
        margin-top: 4px;
    }

    /* زرار التفاصيل */
    .action-btn {
        background: #0046be;
        color: white;
        padding: 8px 25px;
        border-radius: 5px;
        font-weight: 600;
        border: none;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر (Navbar)
st.markdown("""
    <div class="nav-wrapper">
        <div class="brand-logo">معلوماتى <span style="color:#111827">العقارية</span></div>
        <div style="display: flex; gap: 30px; font-weight: 700; font-size: 0.95rem;">
            <div style="cursor:pointer;">عقارات للبيع</div>
            <div style="cursor:pointer;">دليل المطورين</div>
            <div style="cursor:pointer; color:#0046be;">مركز المساعدة</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. شريط البحث (Search Bar - Horizontal)
st.markdown('<div class="search-section">', unsafe_allow_html=True)
sc1, sc2, sc3, sc4 = st.columns([2.5, 1.2, 1.2, 0.6])
with sc1: st.text_input("ابحث عن مدينة، كمبوند، أو مطور...", placeholder="مثلاً: التجمع الخامس، سوديك...")
with sc2: st.selectbox("نوع الوحدة", ["شقق", "فيلات", "تجاري", "إداري", "طبي"])
with sc3: st.selectbox("نطاق السعر", ["الكل", "حتى 3 مليون", "3 - 7 مليون", "7 - 15 مليون", "15 مليون +"])
with sc4: st.markdown('<button style="width:100%; height:45px; margin-top:28px; background:#0046be; color:white; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">بحث</button>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 5. منطقة المحتوى (Results)
col_results, col_ads = st.columns([3, 1], gap="large")

with col_results:
    st.markdown("<h4 style='margin-bottom:20px;'>آخر التحديثات في المشاريع</h4>", unsafe_allow_html=True)
    
    # دالة توليد كروت عقارماب
    def create_aqar_card(price, title, location, developer):
        st.markdown(f"""
            <div class="aqar-card-v2">
                <div class="card-photo"></div>
                <div class="card-content">
                    <div>
                        <div class="price-label">{price} ج.م</div>
                        <div class="proj-name">{title}</div>
                        <div class="loc-label">📍 {location}</div>
                        <div style="margin-top:12px; font-size:0.85rem; color:#4b5563;">بواسطة: <b>{developer}</b></div>
                    </div>
                    <div style="text-align: left;">
                        <button class="action-btn">عرض التفاصيل</button>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # بيانات تجريبية
    create_aqar_card("8,250,000", "كمبوند ايفوري جولي - Ivoire Zayed", "الشيخ زايد الجديدة", "شركة PRE Developments")
    create_aqar_card("5,400,000", "ذا بروكس - The Brooks", "القاهرة الجديدة - التجمع الخامس", "شركة PRE Developments")
    create_aqar_card("12,000,000", "بادية بالم هيلز - Badya", "مدينة 6 أكتوبر - طريق الواحات", "بالم هيلز للتعمير")

with col_ads:
    # السايد بار الجانبي لمعلومات إضافية
    st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0;">
            <h5 style="color:#0046be;">دليل المناطق الأكثر بحثاً</h5>
            <hr style="margin: 10px 0; opacity: 0.1;">
            <p style="font-size: 0.9rem; line-height: 2;">
                • التجمع الخامس<br>
                • العاصمة الإدارية<br>
                • مستقبل سيتي<br>
                • الشيخ زايد
            </p>
        </div>
    """, unsafe_allow_html=True)
