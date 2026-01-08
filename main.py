import streamlit as st

# التصميم اللي اتفقنا عليه (ممنوع اللمس)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    html, body, [data-testid="stAppViewContainer"] { direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f4f7fa !important; }
    .header-nav { background: white; height: 75px; padding: 0 8%; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; }
    .logo-main { color: #003366; font-weight: 900; font-size: 1.8rem; }
    .logo-sub { color: #D4AF37; font-weight: 700; }
    .project-card { background: white; border-radius: 12px; border: 1px solid #e2e8f0; display: flex; height: 120px; margin-bottom: 15px; padding: 20px; align-items: center; }
    .dev-name { color: #003366; font-weight: 900; font-size: 1.4rem; }
    </style>
""", unsafe_allow_html=True)

# الهيدر
st.markdown('<div class="header-nav"><div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div><div>الرئيسية</div></div>', unsafe_allow_html=True)

st.markdown('<div style="padding: 0 8%; margin-top:30px;">', unsafe_allow_html=True)
st.markdown("<h2 style='color:#003366;'>شركات التطوير العقاري (ناوي)</h2>", unsafe_allow_html=True)

# قائمة الشركات اللي سحبناها
companies = ["أورا (Ora)", "سوديك (SODIC)", "إعمار مصر", "طلعت مصطفى", "ماونتن فيو", "بالم هيلز", "نيو جيزة", "مصر إيطاليا", "تاج مصر"]

for company in companies:
    st.markdown(f"""
        <div class="project-card">
            <div style="width: 50px; height: 50px; background: #f0f2f6; border-radius: 50%; margin-left: 20px;"></div>
            <div class="dev-name">{company}</div>
            <div style="margin-right: auto;">
                <button style="background:#003366; border:none; color:white; padding:8px 15px; border-radius:6px; cursor:pointer;">عرض المشاريع</button>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
