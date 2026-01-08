import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة وإخفاء كل زوائد المنصة تماماً
st.set_page_config(page_title="معلوماتي العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الهيدر وأيقونة جيت هب والسهم تماماً */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important; text-align: right;
        font-family: 'Cairo', sans-serif; background-color: #f8f9fa; color: #1a1a1a;
    }

    /* هيدر أبيض نظيف (Nawy Style) */
    .nawy-header {
        background: #ffffff; padding: 25px; text-align: center;
        border-bottom: 2px solid #c49a6c; margin-bottom: 30px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    /* كارت المطور */
    .dev-card {
        background: #ffffff; border-radius: 15px; padding: 30px;
        margin-bottom: 30px; border: 1px solid #e0e0e0;
        border-right: 10px solid #c49a6c;
    }

    /* شبكة المشاريع Grid */
    .project-grid {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
    }
    .project-card {
        background: #ffffff; border-radius: 12px; border: 1px solid #eee;
        padding: 20px; transition: 0.3s;
    }
    .project-card:hover { border-color: #c49a6c; box-shadow: 0 5px 15px rgba(0,0,0,0.08); }
    
    .price-tag {
        color: #c49a6c; font-weight: 900; font-size: 1.1em;
        background: #fcf8f3; padding: 5px 10px; border-radius: 5px;
    }

    /* تنسيق الفلاتر */
    div[data-baseweb="select"] { background-color: white !important; }
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
        df.columns = [str(c).strip() for c in df.columns] # تنظيف أسماء الأعمدة من المسافات
        return df.fillna("-").astype(str)
    except:
        return pd.DataFrame()

df = load_data()

# الهيدر
st.markdown('<div class="nawy-header"><h1>مـعـلـومـاتـي <span style="color:#c49a6c;">الـعـقـاريـة</span></h1></div>', unsafe_allow_html=True)

if not df.empty:
    # الفلاتر
    c1, c2 = st.columns(2)
    with c1:
        s_dev = st.selectbox("🏢 اختر المطور", ["كل المطورين"] + sorted(df['المطور'].unique().tolist()))
    with c2:
        # حل مشكلة KeyError: التأكد من وجود العمود أو استخدام بديل
        reg_col = 'المنطقة' if 'المنطقة' in df.columns else df.columns[4]
        s_reg = st.selectbox("📍 اختر المنطقة", ["كل المناطق"] + sorted(df[reg_col].unique().tolist()))

    if s_dev != "كل المطورين":
        # عرض معلومات المطور مرة واحدة
        dev_info = df[df['المطور'] == s_dev].iloc[0]
        st.markdown(f"""
            <div class="dev-card">
                <h2 style="color:#c49a6c; margin-bottom:10px;">{s_dev}</h2>
                <p><b>👤 المالك:</b> {dev_info.get('المالك', '-')}</p>
                <hr style="opacity:0.1;">
                <p><b>📜 سابقة الأعمال:</b><br>{dev_info.get('سابقة_الأعمال', '-')}</p>
            </div>
            <h3 style="margin-bottom:20px;">🏗️ المشاريع المتاحة</h3>
        """, unsafe_allow_html=True)
        
        # شبكة مشاريع المطور المحدد
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, row in df[df['المطور'] == s_dev].iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="price-tag">{row.get('السعر', '-')}</div>
                    <h4 style="margin: 15px 0 5px 0;">{row['المشروع']}</h4>
                    <p style="color:#666; font-size:0.9em;">📍 {row[reg_col]}</p>
                    <p style="color:#888; font-size:0.8em;">💳 السداد: {row.get('السداد','-')}</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # عرض كل المشاريع في حالة عدم اختيار مطور
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df[reg_col] == s_reg]
        
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, row in f_df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="price-tag">{row.get('السعر', '-')}</div>
                    <h4 style="margin: 15px 0 5px 0;">{row['المشروع']}</h4>
                    <p style="color:#c49a6c; font-weight:bold;">🏢 {row['المطور']}</p>
                    <p style="color:#666; font-size:0.9em;">📍 {row[reg_col]}</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("تأكد من نشر الشيت بصيغة CSV وترتيب الأعمدة.")
