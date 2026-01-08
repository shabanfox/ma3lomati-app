import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة وإخفاء زوائد جيت هب
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء أيقونة جيت هب والقوائم العلوية */
    #MainMenu, header, footer, .stDeployButton {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important; text-align: right;
        font-family: 'Cairo', sans-serif; background-color: #0f1116; color: #ffffff;
    }

    /* هيدر احترافي مع خلفية متحركة بسيطة */
    .hero-section {
        background: linear-gradient(-45deg, #1c2128, #0f1116, #2d240a, #0f1116);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        padding: 50px 20px; text-align: center; border-bottom: 2px solid #d4af37;
        margin-bottom: 30px; border-radius: 0 0 50px 50px;
    }
    @keyframes gradient { 0% {background-position: 0% 50%;} 50% {background-position: 100% 50%;} 100% {background-position: 0% 50%;} }

    /* تنسيق كروت المطورين (Nawy Style) */
    .dev-profile-card {
        background: #1c2128; border: 1px solid #30363d; border-radius: 20px;
        padding: 30px; border-right: 8px solid #d4af37; margin-bottom: 25px;
    }
    .project-card {
        background: #0d1117; border: 1px solid #30363d; border-radius: 15px;
        padding: 20px; transition: 0.3s; margin-bottom: 10px;
    }
    .project-card:hover { border-color: #d4af37; transform: translateY(-5px); }
    
    .price-tag { background: #d4af37; color: #000; padding: 5px 15px; border-radius: 8px; font-weight: 900; float: left; }
    
    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1c2128; border-radius: 10px; color: #d4af37; padding: 12px 30px; font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #d4af37 !important; color: black !important; }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR0vzgtd_E2feFVen6GGR02lYcB7kUASgyLyvqBGA7pAHseUf9KxAyEyDHU935VLFEWQot2p5FBFSwv/pub?output=csv"

@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(SHEET_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("-").astype(str)
    except:
        return pd.DataFrame()

df = load_data()

# الهيدر
st.markdown("""
    <div class="hero-section">
        <h1 style="font-size: 3.5em; font-weight: 900; color: #d4af37; margin-bottom: 10px;">معلوماتي العقارية</h1>
        <p style="font-size: 1.2em; opacity: 0.8;">الموسوعة الأكبر للمطورين العقاريين في مصر</p>
    </div>
""", unsafe_allow_html=True)

if not df.empty:
    # الفلاتر
    col1, col2 = st.columns(2)
    with col1:
        s_dev = st.selectbox("🏢 اختر المطور العقاري", ["كل المطورين"] + sorted(df['المطور'].unique().tolist()))
    with col2:
        s_reg = st.selectbox("📍 فلتر حسب المنطقة", ["كل المناطق"] + sorted(df['المنطقة'].unique().tolist()))

    st.markdown("<br>", unsafe_allow_html=True)

    if s_dev != "كل المطورين":
        # عرض معلومات الشركة (تظهر مرة واحدة فقط)
        dev_info = df[df['المطور'] == s_dev].iloc[0]
        
        st.markdown(f"""
            <div class="dev-profile-card">
                <h2 style="color:#d4af37; margin-bottom:5px;">{s_dev}</h2>
                <p style="color:#aaa;">تاريخ التأسيس: {dev_info.get('تأسيس', '-')}</p>
                <hr style="border-color: rgba(212,175,55,0.2);">
                <div style="display: grid; grid-template-columns: 1fr; gap: 20px;">
                    <div>
                        <h4 style="color:#d4af37;">👤 المالك / الإدارة</h4>
                        <p style="font-size:1.2em;">{dev_info.get('المالك', '-')}</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🏗️ المشاريع المتاحة", "📜 سابقة الأعمال بالتفصيل"])
        
        with tab1:
            projs = df[df['المطور'] == s_dev]
            for _, row in projs.iterrows():
                st.markdown(f"""
                    <div class="project-card">
                        <div class="price-tag">{row.get('السعر', '-')}</div>
                        <h3 style="color:#d4af37;">{row.get('المشروع', '-')}</h3>
                        <p>📍 {row.get('المنطقة', '-')} | 🏗️ {row.get('النوع', '-')} | 💳 {row.get('السداد', '-')}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown(f"""
                <div style="background:#1c2128; padding:20px; border-radius:15px; line-height:1.8;">
                    {dev_info.get('سابقة_الأعمال', 'لا توجد تفاصيل تاريخية حالياً.')}
                </div>
            """, unsafe_allow_html=True)
    else:
        # البحث العام
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df['المنطقة'] == s_reg]
        
        for _, row in f_df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="price-tag">{row.get('السعر', '-')}</div>
                    <h3 style="color:#d4af37;">{row.get('المشروع', '-')}</h3>
                    <p>🏢 {row.get('المطور', '-')} | 📍 {row.get('المنطقة', '-')}</p>
                </div>
            """, unsafe_allow_html=True)
else:
    st.error("فشل تحميل البيانات. تأكد من نشر الشيت بصيغة CSV وترتيب الأعمدة.")
