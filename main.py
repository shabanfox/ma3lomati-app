import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. هندسة التصميم (The UI Engine)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* الأساسيات */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background-color: #f8fafc !important;
    }

    /* شريط التنقل العلوي - الأبيض النظيف */
    .nav-bar {
        background: white;
        padding: 15px 60px;
        border-bottom: 1px solid #e2e8f0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky; top: 0; z-index: 1000;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .nav-logo {
        color: #0056b3;
        font-weight: 900;
        font-size: 1.5rem;
    }

    /* شريط البحث المودرن (Aqarmap Style) */
    .search-wrapper {
        background: white;
        padding: 25px 60px;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 30px;
    }

    /* كارت المشروع الاحترافي */
    .property-card {
        background: white;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
        display: flex;
        overflow: hidden;
        transition: 0.3s;
        height: 220px;
    }
    .property-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.06);
        border-color: #0056b3;
    }

    .image-placeholder {
        width: 320px;
        background-image: url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=800&q=80');
        background-size: cover;
        background-position: center;
    }

    .card-info {
        padding: 25px;
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .price-tag {
        color: #0056b3;
        font-weight: 900;
        font-size: 1.6rem;
    }

    .project-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 5px;
    }

    .location-info {
        color: #64748b;
        font-size: 0.95rem;
    }

    /* الأزرار والفلاتر */
    .primary-btn {
        background-color: #0056b3;
        color: white;
        padding: 10px 25px;
        border-radius: 8px;
        border: none;
        font-weight: 700;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# 3. الهيكل (UI Layout)
st.markdown("""
    <div class="nav-bar">
        <div class="nav-logo">معلوماتى <span style="color:#334155">العقارية</span></div>
        <div style="display:flex; gap:25px; font-weight:600; font-size:0.9rem; color:#475569;">
            <span>عقارات للبيع</span>
            <span>دليل المناطق</span>
            <span style="color:#0056b3">تسجيل الدخول</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. منطقة البحث العرضية
st.markdown('<div class="search-wrapper">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([2.5, 1, 1, 0.6])
with c1: st.text_input("📍 ابحث عن منطقة أو مطور أو مشروع...", placeholder="مثلاً: التجمع الخامس، شركة مراكز...")
with c2: st.selectbox("نوع العقار", ["شقة", "فيلا", "مكتب", "محل"])
with c3: st.selectbox("السعر", ["الكل", "3-5 مليون", "5-10 مليون", "+10 مليون"])
with c4: st.markdown('<button class="primary-btn" style="width:100%; margin-top:28px;">بحث</button>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 5. عرض النتائج والسايد بار
col_main, col_side = st.columns([3, 1], gap="large")

with col_main:
    st.markdown("<h3 style='margin-bottom:20px; color:#1e293b;'>أهم المشاريع العقارية</h3>", unsafe_allow_html=True)
    
    def render_card(price, name, loc, dev):
        st.markdown(f"""
            <div class="property-card">
                <div class="image-placeholder"></div>
                <div class="card-info">
                    <div>
                        <div class="price-tag">{price} ج.م</div>
                        <div class="project-title">{name}</div>
                        <div class="location-info">📍 {loc}</div>
                        <div style="margin-top:10px; font-size:0.9rem; color:#475569;">المطور: <b>{dev}</b></div>
                    </div>
                    <div style="text-align: left;">
                        <button class="primary-btn">عرض التفاصيل</button>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    render_card("8,250,000", "ايفوري جولي - Ivoire Zayed", "الشيخ زايد الجديدة", "PRE Developments")
    render_card("6,400,000", "ذا بروكس - The Brooks", "التجمع الخامس - الدائري", "PRE Developments")
    render_card("12,700,000", "بادية - Badya Palm Hills", "أكتوبر - طريق الواحات", "Palm Hills")

with col_side:
    # السايد بار بنفس شكل الصورة
    st.markdown("""
        <div style="background: white; padding: 25px; border-radius: 16px; border: 1px solid #e2e8f0;">
            <h4 style="color:#0056b3; margin-bottom:15px;">المناطق الأكثر بحثاً</h4>
            <div style="display:flex; flex-direction:column; gap:12px; font-size:0.95rem; color:#475569;">
                <div>🔹 التجمع الخامس</div>
                <div>🔹 العاصمة الإدارية</div>
                <div>🔹 مدينة المستقبل</div>
                <div>🔹 الشيخ زايد</div>
                <hr style="opacity:0.1">
                <div style="color:#0056b3; font-weight:700; text-align:center; cursor:pointer;">شاهد المزيد</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
