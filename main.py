import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="معلوماتى العقارية", layout="wide")

# 2. حالة الجلسة (Login)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# 3. التصميم المعتمد (CSS)
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    .block-container { padding: 0rem !important; }
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
        background-color: #f4f7fa !important;
    }
    .header-nav {
        background: white; height: 75px; padding: 0 8%; display: flex;
        justify-content: space-between; align-items: center;
        border-bottom: 2px solid #e2e8f0; position: sticky; top: 0; z-index: 1000;
    }
    .logo-main { color: #003366; font-weight: 900; font-size: 1.8rem; }
    .logo-sub { color: #D4AF37; font-weight: 700; }
    .hero-outer { padding: 0 8%; margin-top: 15px; }
    .hero-inner {
        background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
        url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=1200');
        background-size: cover; background-position: center; height: 320px;
        border-radius: 12px; display: flex; flex-direction: column; justify-content: center; align-items: center; color: white;
    }
    .project-card {
        background: white; border-radius: 12px; border: 1px solid #e2e8f0;
        display: flex; height: 130px; margin-bottom: 15px; overflow: hidden; align-items: center; padding: 0 20px;
    }
    .dev-name { color: #003366; font-weight: 900; font-size: 1.4rem; flex: 1; }
    .btn-details { background:#003366; border:none; color:white; padding:10px 25px; border-radius:6px; font-weight:700; cursor:pointer; }
    </style>
""", unsafe_allow_html=True)

# 4. وظيفة جلب البيانات
def load_data():
    try:
        return pd.read_csv('nawy_developers.csv')
    except:
        return pd.DataFrame({"اسم الشركة": ["أورا (Ora)", "سوديك (SODIC)", "إعمار مصر", "بالم هيلز"]})

# 5. منطق العرض
if not st.session_state.logged_in:
    # صفحة الدخول
    st.markdown('<div class="header-nav"><div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div></div>', unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1, 1])
    with col:
        st.markdown("<div style='margin-top:100px;'></div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#003366; font-weight:900;'>دخول المنصة</h2>", unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول", use_container_width=True):
            if u == "admin" and p == "123":
                st.session_state.logged_in = True
                st.rerun()
else:
    # المنصة الرئيسية
    st.markdown('<div class="header-nav"><div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div><div>الرئيسية</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-outer"><div class="hero-inner"><h1 style="font-weight:900; font-size:2.5rem;">بوابتك لأدق البيانات العقارية</h1></div></div>', unsafe_allow_html=True)
    
    st.markdown('<div style="padding: 0 8%; margin-top:30px;">', unsafe_allow_html=True)
    df = load_data()
    for index, row in df.iterrows():
        st.markdown(f"""
            <div class="project-card">
                <div style="width:50px; height:50px; background:#f0f2f6; border-radius:50%; margin-left:20px; display:flex; align-items:center; justify-content:center;"><i class="fa-solid fa-building" style="color:#003366;"></i></div>
                <div class="dev-name">{row['اسم الشركة']}</div>
                <button class="btn-details">عرض المشاريع</button>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
