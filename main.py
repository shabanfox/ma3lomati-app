import streamlit as st

# 1. إعداد الصفحة
st.set_page_config(page_title="معلوماتى العقارية", layout="wide")

# 2. كود التصميم الملكي (لوجو وكروت)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer {display: none !important;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f4f7fa; 
    }
    .header-nav { 
        background: white; height: 75px; padding: 0 8%; display: flex; 
        justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; 
    }
    .logo-main { color: #003366; font-weight: 900; font-size: 1.8rem; }
    .logo-sub { color: #D4AF37; }
    .project-card { 
        background: white; border-radius: 12px; border: 1px solid #e2e8f0; 
        display: flex; height: 160px; margin: 15px 8%; overflow: hidden;
    }
    .card-img { width: 220px; background: #eee url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400') center/cover; }
    .card-body { padding: 20px; flex: 1; }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر (اللوجو)
st.markdown('<div class="header-nav"><div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div></div>', unsafe_allow_html=True)

# 4. محتوى تجريبي
st.markdown('<h2 style="padding: 20px 8%; color:#003366;">المطورين المعتمدين (ناوي)</h2>', unsafe_allow_html=True)

st.markdown('''
    <div class="project-card">
        <div class="card-img"></div>
        <div class="card-body">
            <div style="color: #003366; font-weight: 900; font-size: 1.4rem;">مطور معتمد</div>
            <div style="font-weight:700; font-size:1.3rem; margin-top:5px;">شركة أورا (Ora Developers)</div>
            <p style="color:#666;">📍 جميع المشاريع محدثة الآن</p>
        </div>
    </div>
''', unsafe_allow_html=True)
