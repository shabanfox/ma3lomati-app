import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعداد الصفحة وإخفاء زوائد GitHub تماماً
st.set_page_config(page_title="معلوماتي العقارية - Nawy Style", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الهيدر وأيقونة جيت هب */
    [data-testid="stHeader"] {display: none;}
    #MainMenu, footer, .stDeployButton {visibility: hidden;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important; text-align: right;
        font-family: 'Cairo', sans-serif; background-color: #0d1117; color: #ffffff;
    }

    /* هيدر احترافي بخلفية متحركة */
    .hero-section {
        background: linear-gradient(-45deg, #1c2128, #0d1117, #2d240a, #161b22);
        background-size: 400% 400%;
        animation: gradientBG 12s ease infinite;
        padding: 60px 20px; text-align: center;
        border-bottom: 2px solid #d4af37; border-radius: 0 0 40px 40px;
        margin-bottom: 40px;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* تنسيق بروفايل المطور (Nawy Concept) */
    .dev-header {
        background: #1c2128; border: 1px solid #d4af37; border-radius: 20px;
        padding: 30px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .project-card {
        background: #161b22; border: 1px solid #30363d; border-radius: 15px;
        padding: 20px; margin-bottom: 15px; transition: 0.3s;
    }
    .project-card:hover { border-color: #d4af37; transform: translateY(-3px); }
    .price-badge {
        background: #d4af37; color: #000; padding: 4px 12px;
        border-radius: 6px; font-weight: 900; float: left;
    }
    
    /* تنسيق التبويبات */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1c2128; border-radius: 10px; color: #d4af37; padding: 10px 25px;
    }
    .stTabs [aria-selected="true"] { background-color: #d4af37 !important; color: black !important; }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات من رابط الشيت الخاص بك
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

# الهيدر المتحرك
st.markdown("""
    <div class="hero-section">
        <h1 style="font-size: 3.5em; font-weight: 900; color: #d4af37; margin:0;">معلوماتي العقارية</h1>
        <p style="font-size: 1.2em; opacity: 0.8; margin-top:10px;">دليل المطورين والمشاريع الأكثر دقة في مصر</p>
    </div>
""", unsafe_allow_html=True)

if not df.empty:
    # الفلاتر (شكل نظيف)
    col1, col2 = st.columns(2)
    with col1:
        s_dev = st.selectbox("🏢 اختر المطور العقاري", ["كل المطورين"] + sorted(df['المطور'].unique().tolist()))
    with col2:
        s_reg = st.selectbox("📍 ابحث بالمنطقة", ["كل المناطق"] + sorted(df['المنطقة'].unique().tolist()))

    st.markdown("<br>", unsafe_allow_html=True)

    if s_dev != "كل المطورين":
        # منطق "ناوي": عرض المطور كأنه بروفايل واحد
        dev_rows = df[df['المطور'] == s_dev]
        first_row = dev_rows.iloc[0] # ناخد بيانات الشركة من أول سطر
        
        st.markdown(f"""
            <div class="dev-header">
                <h2 style="color:#d4af37; margin:0;">{s_dev}</h2>
                <p style="opacity:0.7;">رئيس مجلس الإدارة: {first_row.get('المالك', '-')}</p>
                <hr style="border-color: rgba(212,175,55,0.2);">
                <h4 style="color:#d4af37;">📜 عن المطور</h4>
                <p style="line-height:1.7;">{first_row.get('سابقة_الأعمال', 'لا توجد بيانات تاريخية متوفرة.')}</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"<h3 style='text-align:center; color:#d4af37;'>🏗️ مشاريع {s_dev}</h3>", unsafe_allow_html=True)
        
        # عرض المشاريع في شبكة (Grid)
        for _, row in dev_rows.iterrows():
            if row['المشروع'] != "-":
                st.markdown(f"""
                    <div class="project-card">
                        <div class="price-badge">{row.get('السعر', '-')}</div>
                        <h3 style="margin:0; color:#d4af37;">{row['المشروع']}</h3>
                        <p style="margin:10px 0;">📍 {row['المنطقة']} | 🏗️ {row.get('النوع','-')}</p>
                        <small style="color:#aaa;">💳 نظام السداد: {row.get('السداد','-')}</small>
                    </div>
                """, unsafe_allow_html=True)
    else:
        # عرض كل المشاريع (البحث العام)
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df['المنطقة'] == s_reg]
        
        for _, row in f_df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="price-badge">{row.get('السعر', '-')}</div>
                    <h3 style="margin:0; color:#d4af37;">{row['المشروع']}</h3>
                    <p style="margin:5px 0;">🏢 {row['المطور']} | 📍 {row['المنطقة']}</p>
                </div>
            """, unsafe_allow_html=True)
else:
    st.error("⚠️ لم نتمكن من سحب البيانات. تأكد من أن ملف الإكسيل 'منشور على الويب' بصيغة CSV.")
