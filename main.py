import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة - تصميم عريض
st.set_page_config(page_title="Ma3lomati | Premium Broker Tool", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* إخفاء هوية ستريمليت تماماً */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: ltr !important;
        text-align: left !important;
        font-family: 'Cairo', sans-serif;
        background-color: #f4f6f9; /* خلفية هادئة */
    }

    /* الهيدر العلوي النحيف */
    .top-nav {
        background: #0f172a; padding: 15px 30px;
        color: white; border-bottom: 3px solid #c49a6c;
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* اللوحة اليمنى: معلومات الشركة */
    .info-panel-right {
        background: white; border-radius: 20px; padding: 30px;
        border-right: 10px solid #c49a6c; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        height: fit-content; position: sticky; top: 20px;
    }

    /* اللوحة اليسرى: شبكة المشاريع */
    .project-grid-left {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 15px;
    }

    /* تصميم الكارت الفاخر المصغر */
    .premium-card-small {
        background: #ffffff; border-radius: 15px; padding: 18px;
        border: 1px solid #eef0f2; transition: all 0.3s ease-in-out;
        display: flex; flex-direction: column; justify-content: space-between;
        min-height: 160px; box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    .premium-card-small:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 30px rgba(196, 154, 108, 0.1);
        border-color: #c49a6c;
    }
    
    .price-tag {
        color: #c49a6c; font-weight: 800; font-size: 0.85em;
        background: #fdfaf5; padding: 4px 10px; border-radius: 8px;
        display: inline-block; margin-bottom: 10px;
    }

    .project-title-text {
        font-weight: 700; font-size: 1em; color: #1e293b;
        margin-bottom: 8px; line-height: 1.4;
    }

    .loc-text { color: #64748b; font-size: 0.8em; font-weight: 600; }

    /* صندوق الفلاتر */
    .filter-wrapper {
        background: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03); margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات
RAW_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8MmnRw6KGRVIKIfp_-o8KyvhJKVhHLIZKpFngWHeN0WTsjupFMILryY7EKv6m0vPCD0jwcBND-pvk/pub?output=csv"

@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(RAW_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("-").astype(str)
    except: return pd.DataFrame()

df = load_data()

# Navigation Bar
st.markdown('<div class="top-nav"><h2 style="margin:0; letter-spacing:1px; font-weight:900;">MA3LOMATI</h2><span style="color:#c49a6c;">Elite Real Estate Hub</span></div>', unsafe_allow_html=True)

if not df.empty:
    # تحديد أسماء الأعمدة بأمان
    def safe_col(names, fallback_idx):
        for n in names:
            if n in df.columns: return n
        return df.columns[fallback_idx] if len(df.columns) > fallback_idx else df.columns[0]

    C_DEV = safe_col(["المطور", "الشركة"], 0)
    C_OWNER = safe_col(["المالك", "الاونر"], 1)
    C_BIO = safe_col(["سيرة عن الشركة والاونر"], 2)
    C_PROJ = safe_col(["المشروع"], 3)
    C_REG = safe_col(["المنطقة"], 4)
    C_PRICE = safe_col(["السعر"], 5)

    # 1. قسم الفلاتر (أعلى الصفحة)
    st.markdown('<div class="filter-wrapper">', unsafe_allow_html=True)
    f1, f2 = st.columns(2)
    with f1: s_dev = st.selectbox("🏢 Select Developer", sorted(df[C_DEV].unique().tolist()))
    with f2: s_reg = st.selectbox("📍 Filter by Region", ["All Regions"] + sorted(df[C_REG].unique().tolist()))
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. التقسيم الرئيسي (يسار للمشاريع | يمين للمعلومات)
    # نستخدم نسبة 2.5 لليسار و 1 لليمن
    col_projects, col_info = st.columns([2.5, 1], gap="large")

    dev_data = df[df[C_DEV] == s_dev]

    # الجانب الأيمن: معلومات الشركة (Company Profile)
    with col_info:
        if not dev_data.empty:
            info = dev_data.iloc[0]
            st.markdown(f"""
                <div class="info-panel-right">
                    <h1 style="color:#0f172a; margin-top:0; font-size:2.2em;">{s_dev}</h1>
                    <p style="font-size:1.1em; color:#c49a6c; font-weight:700;">👤 Owner: <span style="color:#333;">{info[C_OWNER]}</span></p>
                    <hr style="opacity:0.1; margin:20px 0;">
                    <h4 style="color:#0f172a; margin-bottom:10px;">About the Developer:</h4>
                    <p style="line-height:1.7; color:#475569; font-size:0.95em; text-align:justify;">{info[C_BIO]}</p>
                </div>
            """, unsafe_allow_html=True)

    # الجانب الأيسر: المشاريع (Projects Grid)
    with col_projects:
        display_df = dev_data
        if s_reg != "All Regions":
            display_df = dev_data[dev_data[C_REG] == s_reg]
        
        st.markdown(f'<h3 style="margin-bottom:20px; color:#0f172a;">{s_dev} Portfolio</h3>', unsafe_allow_html=True)
        st.markdown('<div class="project-grid-left">', unsafe_allow_html=True)
        for _, row in display_df.iterrows():
            if row[C_PROJ] != "-":
                st.markdown(f"""
                    <div class="premium-card-small">
                        <div>
                            <div class="price-tag">{row[C_PRICE]}</div>
                            <div class="project-title-text">{row[C_PROJ]}</div>
                        </div>
                        <div class="loc-text">📍 {row[C_REG]}</div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Error loading data from Google Sheets.")
