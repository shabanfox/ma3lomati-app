import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعداد الصفحة وإخفاء كل زوائد Streamlit/GitHub
st.set_page_config(page_title="معلوماتي العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الهيدر وأيقونة جيت هب والقوائم تماماً */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important; text-align: right;
        font-family: 'Cairo', sans-serif; background-color: #05070a; color: #ffffff;
    }

    /* هيدر بخلفية متحركة احترافية */
    .hero-section {
        background: linear-gradient(-45deg, #05070a, #1c2128, #2d240a, #05070a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        padding: 60px 20px; text-align: center;
        border-bottom: 2px solid #d4af37; border-radius: 0 0 40px 40px;
        margin-bottom: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    @keyframes gradientBG { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }

    /* كارت المطور الملكي */
    .dev-profile {
        background: #111418; border: 1px solid #d4af37; border-radius: 20px;
        padding: 30px; margin-bottom: 30px; border-right: 10px solid #d4af37;
    }

    /* شبكة المشاريع Grid Style */
    .project-grid {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px; margin-top: 20px;
    }
    .project-card {
        background: #1c2128; border: 1px solid #30363d; border-radius: 15px;
        padding: 20px; position: relative; transition: 0.3s;
    }
    .project-card:hover { border-color: #d4af37; transform: translateY(-5px); }
    .price-tag {
        background: #d4af37; color: #000; padding: 4px 10px;
        border-radius: 6px; font-weight: 900; position: absolute; left: 15px; top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. وظيفة جلب البيانات مع تأمين ضد أخطاء أسماء الأعمدة
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR0vzgtd_E2feFVen6GGR02lYcB7kUASgyLyvqBGA7pAHseUf9KxAyEyDHU935VLFEWQot2p5FBFSwv/pub?output=csv"

@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(SHEET_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns] # تنظيف المسافات
        return df.fillna("-").astype(str)
    except: return pd.DataFrame()

df = load_data()

# الهيدر
st.markdown('<div class="hero-section"><h1>مـعـلـومـاتـي العقارية</h1><p>المرجع الشامل للمطورين والمشاريع في مصر</p></div>', unsafe_allow_html=True)

if not df.empty:
    # دالة ذكية لإيجاد العمود حتى لو اسمه اتغير شوية
    def find_col(possible_names):
        for name in possible_names:
            if name in df.columns: return name
        return df.columns[0] # لو منفعش ياخد أول عمود

    C_DEV = find_col(["المطور", "شركة", "Developer"])
    C_REG = find_col(["المنطقة", "مكان", "Region", "Location"])
    C_PROJ = find_col(["المشروع", "اسم المشروع", "Project"])
    C_OWNER = find_col(["المالك", "رئيس"])
    C_BIO = find_col(["سابقة_الأعمال", "عن الشركة"])

    # الفلاتر
    c1, c2 = st.columns(2)
    with c1: s_dev = st.selectbox("🏢 اختر المطور", ["كل المطورين"] + sorted(df[C_DEV].unique().tolist()))
    with c2: s_reg = st.selectbox("📍 اختر المنطقة", ["كل المناطق"] + sorted(df[C_REG].unique().tolist()))

    if s_dev != "كل المطورين":
        # عرض المطور (مرة واحدة)
        dev_data = df[df[C_DEV] == s_dev]
        first = dev_data.iloc[0]
        st.markdown(f"""
            <div class="dev-profile">
                <h2 style="color:#d4af37;">{s_dev}</h2>
                <p><b>👤 الإدارة:</b> {first.get(C_OWNER, '-')}</p>
                <hr style="opacity:0.1;">
                <p><b>📜 سابقة الأعمال:</b><br>{first.get(C_BIO, '-')}</p>
            </div>
            <h3 style="text-align:center; color:#d4af37; margin:20px 0;">🏗️ مشاريع الشركة</h3>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, row in dev_data.iterrows():
            if row[C_PROJ] != "-":
                st.markdown(f"""
                    <div class="project-card">
                        <div class="price-tag">{row.get('السعر', '-')}</div>
                        <h4 style="margin-top:30px; color:#d4af37;">{row[C_PROJ]}</h4>
                        <p>📍 {row[C_REG]} | 🏗️ {row.get('النوع','-')}</p>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # البحث العام
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df[C_REG] == s_reg]
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, row in f_df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="price-tag">{row.get('السعر', '-')}</div>
                    <h4 style="margin-top:30px; color:#d4af37;">{row[C_PROJ]}</h4>
                    <p>🏢 {row[C_DEV]} | 📍 {row[C_REG]}</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("تأكد من نشر الشيت بصيغة CSV.")
