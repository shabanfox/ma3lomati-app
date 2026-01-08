import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# 2. حماية الموقع
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 3. دالة جلب البيانات (بتجيب الكلام بس، ملهاش دعوة بالتصميم)
def load_data():
    try:
        return pd.read_csv('data.csv')
    except:
        # بيانات احتياطية عشان الموقع ميفضاش لو الإكسيل مش موجود
        return pd.DataFrame({
            'المشروع': ['كمبوند ايفوري جولي', 'مشروع ماونتن فيو'],
            'المنطقة': ['الشيخ زايد الجديدة', 'القاهرة الجديدة'],
            'السعر': ['9,200,000', '12,500,000'],
            'الصورة': ['https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400', 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=400']
        })

# 4. التصميم الفخم (ممنوع اللمس)
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    .block-container { padding-top: 0.6rem !important; padding-left: 0rem !important; padding-right: 0rem !important; }
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
        background-color: #f4f7fa !important;
    }

    /* الهيدر الفخم */
    .header-nav {
        background: white; height: 75px; padding: 0 8%;
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 2px solid #e2e8f0; position: sticky; top: 0; z-index: 1000;
    }
    .logo-container { display: flex; align-items: center; gap: 12px; }
    .logo-main { color: #003366; font-weight: 900; font-size: 1.8rem; }
    .logo-sub { color: #D4AF37; font-weight: 700; }
    
    /* الهيرو */
    .hero-outer { padding: 0 8%; margin-top: 10px; }
    .hero-inner {
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80');
        background-size: cover; background-position: center; height: 320px;
        border-radius: 12px; display: flex; flex-direction: column;
        justify-content: center; align-items: center; color: white;
    }

    /* كروت المشاريع */
    .project-card {
        background: white; border-radius: 12px; border: 1px solid #e2e8f0;
        display: flex; height: 190px; margin-bottom: 15px; overflow: hidden;
    }
    .card-img-box { width: 260px; background-size: cover; background-position: center; }
    .card-body { padding: 20px; flex: 1; display: flex; flex-direction: column; justify-content: space-between; }
    .price { color: #003366; font-weight: 900; font-size: 1.4rem; }
    </style>
""", unsafe_allow_html=True)

# منطق العرض
if not st.session_state.logged_in:
    # صفحة الدخول
    st.markdown('<div class="header-nav"><div class="logo-container"><div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div></div></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<div style='margin-top:100px;'></div>", unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم", placeholder="admin")
        p = st.text_input("كلمة المرور", type="password", placeholder="123")
        if st.button("دخول", use_container_width=True):
            if u == "admin" and p == "123":
                st.session_state.logged_in = True
                st.rerun()
else:
    # الهيدر الفخم
    st.markdown('<div class="header-nav"><div class="logo-container"><i class="fa-solid fa-city" style="color:#003366;font-size:1.6rem;"></i><div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div></div><div style="color:#475569;font-weight:600;">الرئيسية</div></div>', unsafe_allow_html=True)

    # الهيرو
    st.markdown('<div class="hero-outer"><div class="hero-inner"><h1 style="font-weight:900; font-size:2.5rem;">بوابتك لأدق البيانات العقارية</h1><p style="font-size:1.2rem; opacity:0.95;">المرجع الأول للمحترفين في السوق المصري</p></div></div>', unsafe_allow_html=True)

    # تحميل البيانات
    df = load_data()
    st.markdown('<div style="padding: 0 8%; margin-top:25px;">', unsafe_allow_html=True)
    
    # حلقة التكرار (بتعرض المشاريع بنفس التصميم المحفوظ)
    for _, row in df.iterrows():
        st.markdown(f"""
            <div class="project-card">
                <div class="card-img-box" style="background-image: url('{row['الصورة']}')"></div>
                <div class="card-body">
                    <div>
                        <div class="price">{row['السعر']} ج.م</div>
                        <div style="font-weight: 700; font-size: 1.2rem; color: #1e293b; margin-top:5px;">{row['المشروع']}</div>
                        <div style="color:#64748b; font-size:0.95rem; margin-top:5px;">📍 {row['المنطقة']}</div>
                    </div>
                    <div style="text-align: left;">
                        <button style="background:#003366; border:none; color:white; padding:8px 20px; border-radius:6px; font-weight:700; cursor:pointer;">عرض التفاصيل</button>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
