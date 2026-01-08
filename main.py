import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعداد الصفحة
st.set_page_config(page_title="منصة معلوماتي - دليل المطورين", layout="wide", page_icon="🏢")

# 2. رابط الشيت (تأكد من نشره بصيغة CSV)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR0vzgtd_E2feFVen6GGR02lYcB7kUASgyLyvqBGA7pAHseUf9KxAyEyDHU935VLFEWQot2p5FBFSwv/pub?output=csv"

# 3. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, header, footer, .stDeployButton {visibility: hidden;}
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important;
        font-family: 'Cairo', sans-serif;
        background-color: #0d1117; color: white; text-align: right;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1c2128; border-radius: 10px; padding: 10px 25px; color: #d4af37;
    }
    .stTabs [aria-selected="true"] { background-color: #d4af37 !important; color: black !important; }
    .dev-card {
        background: linear-gradient(135deg, #1c2128 0%, #0d1117 100%);
        border-right: 5px solid #d4af37; border-radius: 15px; padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-bottom: 20px;
    }
    .project-card {
        background: #1c2128; border: 1px solid #30363d; border-radius: 12px;
        padding: 20px; margin-bottom: 15px; border-right: 4px solid #d4af37;
    }
    .stats-box {
        background: rgba(212, 175, 55, 0.1); border: 1px solid #d4af37;
        border-radius: 15px; padding: 15px; text-align: center;
    }
    label { color: #d4af37 !important; font-size: 1.1em !important; }
    </style>
""", unsafe_allow_html=True)

# 4. دالة جلب البيانات مع تنظيف أسماء الأعمدة
@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(SHEET_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        # تنظيف أسماء الأعمدة من أي مسافات مخفية
        df.columns = df.columns.str.strip()
        df = df.fillna("-").astype(str)
        return df
    except:
        return pd.DataFrame()

df = load_data()

st.markdown("<h1 style='text-align:center; color:#d4af37; font-weight:900;'>🏢 موسوعة المطورين العقاريين</h1>", unsafe_allow_html=True)

if not df.empty:
    # التحقق من وجود الأعمدة قبل تنفيذ الإحصائيات
    dev_col = 'المطور' if 'المطور' in df.columns else df.columns[0]
    proj_col = 'المشروع' if 'المشروع' in df.columns else (df.columns[1] if len(df.columns)>1 else df.columns[0])
    reg_col = 'المنطقة' if 'المنطقة' in df.columns else (df.columns[2] if len(df.columns)>2 else df.columns[0])

    # 5. الإحصائيات (بأسماء الأعمدة المرنة)
    c1, c2, c3 = st.columns(3)
    with c1: 
        st.markdown(f"<div class='stats-box'><h3>{len(df[dev_col].unique())}</h3> مطور عقاري</div>", unsafe_allow_html=True)
    with c2: 
        st.markdown(f"<div class='stats-box'><h3>{len(df[proj_col].unique())}</h3> مشروع مدرج</div>", unsafe_allow_html=True)
    with c3: 
        st.markdown(f"<div class='stats-box'><h3>{len(df[reg_col].unique())}</h3> منطقة</div>", unsafe_allow_html=True)
    
    st.markdown("---")

    # 6. الفلاتر
    col_reg, col_dev = st.columns(2)
    with col_reg:
        s_reg = st.selectbox("📍 فلتر بالمنطقة", ["كل المناطق"] + sorted(df[reg_col].unique().tolist()))
    with col_dev:
        s_dev = st.selectbox("🏢 اختر المطور", ["كل المطورين"] + sorted(df[dev_col].unique().tolist()))

    # 7. منطق العرض
    if s_dev != "كل المطورين":
        dev_data = df[df[dev_col] == s_dev].iloc[0]
        st.markdown(f"<h2 style='color:#d4af37; text-align:center; margin-top:20px;'>📂 شركة: {s_dev}</h2>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["ℹ️ معلومات الشركة", "🏗️ مشاريعها"])
        
        with tab1:
            st.markdown(f"""
                <div class="dev-card">
                    <h3 style="color:#d4af37;">👤 المالك والإدارة</h3>
                    <p style="font-size:1.2em;">{dev_data.get('المالك', 'غير مدرج')}</p>
                    <hr style="opacity:0.2;">
                    <h3 style="color:#d4af37;">📜 النبذة التاريخية</h3>
                    <p style="line-height:1.8;">{dev_data.get('سابقة_الأعمال', 'لا توجد تفاصيل.')}</p>
                </div>
            """, unsafe_allow_html=True)
            
        with tab2:
            projects = df[df[dev_col] == s_dev]
            for _, row in projects.iterrows():
                st.markdown(f"""
                    <div class="project-card">
                        <div style="background:#d4af37; color:black; padding:2px 10px; border-radius:5px; float:left; font-weight:bold;">{row.get('السعر','-')}</div>
                        <h3 style="margin:0;">{row.get(proj_col,'-')}</h3>
                        <p>📍 {row.get(reg_col,'-')} | 💳 {row.get('السداد','-')}</p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        # البحث العام
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df[reg_col] == s_reg]
        
        for _, row in f_df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div style="background:#d4af37; color:black; padding:2px 10px; border-radius:5px; float:left; font-weight:bold;">{row.get('السعر','-')}</div>
                    <h3 style="margin:0;">{row.get(proj_col,'-')}</h3>
                    <p>🏢 {row.get(dev_col,'-')} | 📍 {row.get(reg_col,'-')}</p>
                </div>
            """, unsafe_allow_html=True)
else:
    st.error("⚠️ فشل تحميل البيانات. تأكد من وجود أعمدة: المشروع، المطور، المنطقة.")
