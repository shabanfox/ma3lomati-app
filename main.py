import streamlit as st

# 1. إعداد الصفحة (عشان الموقع يفهم إنه تطبيق مش ملف نصي)
st.set_page_config(page_title="معلوماتى العقارية", layout="wide")

# 2. كود التصميم الملكي الخاص بك (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء عناصر ستريمليت الإفتراضية */
    [data-testid="stHeader"], footer, .stDeployButton {display: none !important;}
    .block-container { padding: 0rem !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f4f7fa; 
    }

    /* تصميم الهيدر (لوجو معلوماتى العقارية) */
    .header-nav { 
        background: white; height: 75px; padding: 0 8%; display: flex; 
        justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; 
    }
    .logo-main { color: #003366; font-weight: 900; font-size: 1.8rem; }
    .logo-sub { color: #D4AF37; }

    /* تصميم الكارت الخاص بك */
    .project-card { 
        background: white; border-radius: 12px; border: 1px solid #e2e8f0; 
        display: flex; height: 160px; margin: 15px 8%; overflow: hidden; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .card-img { 
        width: 240px; 
        background-image: url('https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400');
        background-size: cover; background-position: center; 
    }
    .card-body { padding: 20px; flex: 1; display: flex; flex-direction: column; justify-content: center; }
    .price-tag { color: #003366; font-weight: 900; font-size: 1.4rem; }
    .dev-name { font-weight: 700; font-size: 1.3rem; margin-top: 5px; color: #1e293b; }
    
    .btn-view {
        background: #003366; color: white; border: none; padding: 10px 20px; 
        border-radius: 8px; font-weight: 700; cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# 3. عرض الهيدر (تصميمك)
st.markdown('<div class="header-nav"><div class="logo-main">معلوماتى <span class="logo-sub">العقارية</span></div><div style="font-weight:700;">الرئيسية</div></div>', unsafe_allow_html=True)

# 4. العنوان
st.markdown('<h2 style="padding: 25px 8% 10px 8%; color:#003366;">المطورين المعتمدين</h2>', unsafe_allow_html=True)

# 5. قائمة الأسماء (فقط الأسماء مأخوذة من ناوي)
names_from_nawy = ["أورا (Ora Developers)", "سوديك (SODIC)", "إعمار مصر", "طلعت مصطفى", "ماونتن فيو", "بالم هيلز"]

# 6. عرض البيانات بتصميمك أنت
for name in names_from_nawy:
    st.markdown(f'''
        <div class="project-card">
            <div class="card-img"></div>
            <div class="card-body">
                <div class="price-tag">مطور معتمد</div>
                <div class="dev-name">{name}</div>
                <div style="color:#64748b; font-size:0.9rem; margin-top:5px;">📍 متاح كامل التفاصيل والبيانات المحدثة</div>
            </div>
            <div style="display:flex; align-items:center; padding-left:30px;">
                <div class="btn-view">عرض التفاصيل</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
