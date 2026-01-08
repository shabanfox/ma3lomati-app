import streamlit as st

# 1. إعدادات الصفحة
st.set_page_config(page_title="بروكر مصر | عقارماب ستايل", layout="wide")

# 2. تصميم عقارماب الفعلي (Real Aqarmap UX)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* الأساسيات */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background-color: #f2f4f7 !important;
    }

    /* الهيدر الأبيض النظيف */
    .aqar-nav {
        background: white;
        padding: 10px 60px;
        border-bottom: 1px solid #e5e7eb;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky; top: 0; z-index: 999;
    }

    /* بار البحث العريض (زي عقارماب) */
    .search-container {
        background: white;
        padding: 30px 60px;
        margin-bottom: 20px;
        border-bottom: 1px solid #e5e7eb;
    }

    /* كروت المشاريع الاحترافية */
    .aqar-card {
        background: white;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 20px;
        display: flex; /* عرض عرضي للموبايل واللاب */
        transition: 0.3s;
        cursor: pointer;
        overflow: hidden;
    }
    .aqar-card:hover {
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        border-color: #2b59ff;
    }

    .card-img {
        width: 300px;
        background: #e5e7eb;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #9ca3af;
    }

    .card-body {
        padding: 20px;
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .price-style {
        color: #2b59ff;
        font-weight: 900;
        font-size: 1.4rem;
    }

    .project-name {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1f2937;
        margin: 5px 0;
    }

    .location-tag {
        color: #6b7280;
        font-size: 0.9rem;
    }

    /* أزرار الفلترة */
    .filter-btn {
        background: #f3f4f6;
        border: 1px solid #e5e7eb;
        padding: 8px 15px;
        border-radius: 8px;
        font-size: 0.9rem;
        margin-left: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر
st.markdown("""
    <div class="aqar-nav">
        <div style="font-size: 24px; font-weight: 900; color: #2b59ff;">AQAR<span style="color:#1f2937">MAP</span> CLONE</div>
        <div style="display: flex; gap: 20px; font-weight: 600;">
            <span>بحث</span>
            <span>دليل المطورين</span>
            <span>أسعار المناطق</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. منطقة البحث (Horizontal Search)
st.markdown('<div class="search-container">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns([2, 1, 1, 0.5])
with c1: st.text_input("ابحث عن منطقة، مطور، أو مشروع...", placeholder="مثلاً: التجمع الخامس")
with c2: st.selectbox("نوع العقار", ["شقة", "فيلا", "تجاري", "إداري"])
with c3: st.selectbox("السعر من", ["الكل", "1 مليون", "3 مليون", "5 مليون"])
with c4: st.button("بحث", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# 5. عرض النتائج
col_main, col_sidebar = st.columns([3, 1], gap="large")

with col_main:
    st.markdown("### نتائج البحث عن مشاريع")
    
    # دالة كارت عقارماب الحقيقي
    def aqar_card(title, loc, price, dev):
        st.markdown(f"""
            <div class="aqar-card">
                <div class="card-img">صورة المشروع</div>
                <div class="card-body">
                    <div>
                        <div class="price-style">{price} ج.م</div>
                        <h3 class="project-name">{title}</h3>
                        <div class="location-tag">📍 {loc}</div>
                        <div style="margin-top:10px; font-size:0.85rem; color:#4b5563;">المطور: <b>{dev}</b></div>
                    </div>
                    <div style="text-align: left;">
                        <button style="background:#2b59ff; color:white; border:none; padding:8px 20px; border-radius:6px; cursor:pointer;">التفاصيل</button>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    aqar_card("كمبوند نايل بوليفارد", "القاهرة الجديدة - التجمع", "7,500,000", "النيل للتطوير العقاري")
    aqar_card("كمبوند بادية بالم هيلز", "مدينة 6 أكتوبر", "9,200,000", "بالم هيلز")
    aqar_card("تاج سيتي - Taj City", "القاهرة الجديدة - أمام المطار", "5,400,000", "مدينة مصر")

with col_sidebar:
    st.markdown("""
        <div style="background:white; padding:20px; border-radius:12px; border:1px solid #e5e7eb;">
            <h4>لماذا تستخدم هذه الأداة؟</h4>
            <ul style="padding-right:20px; font-size:0.9rem; color:#4b5563;">
                <li>داتا محدثة يومياً</li>
                <li>تواصل مباشر مع المطورين</li>
                <li>تحليل أسعار السوق</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
