import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة (تجربة المستخدم الاحترافية)
st.set_page_config(page_title="MA3LOMATI | Real Estate Intelligence", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;500;700;800&family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء القوائم الافتراضية */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    /* الخلفية العامة للموقع */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #fcfcfd !important;
        font-family: 'Plus Jakarta Sans', 'Cairo', sans-serif;
        color: #101828;
        direction: ltr !important;
    }

    /* تصميم شريط البحث الجانبي */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #eaecf0;
        padding-top: 20px;
    }

    /* الهيدر الرئيسي الفخم */
    .main-hero {
        background: #0f172a;
        padding: 40px;
        border-radius: 24px;
        color: white;
        margin-bottom: 30px;
        border-bottom: 4px solid #c49a6c;
        box-shadow: 0 20px 24px -4px rgba(16, 24, 40, 0.08);
    }

    /* لوحة معلومات المطور (الجهة اليمنى) */
    .dev-profile-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 30px;
        border: 1px solid #eaecf0;
        box-shadow: 0 4px 6px -2px rgba(16, 24, 40, 0.03);
        position: sticky; top: 20px;
    }

    /* شبكة المشاريع (الجهة اليسرى) */
    .projects-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
        gap: 20px;
    }

    /* كارت المشروع "الفخم والمصغر" */
    .project-card-premium {
        background: #ffffff;
        border: 1px solid #eaecf0;
        border-radius: 16px;
        padding: 20px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 140px;
    }
    .project-card-premium:hover {
        transform: translateY(-5px);
        border-color: #c49a6c;
        box-shadow: 0 12px 16px -4px rgba(16, 24, 40, 0.08);
    }

    .badge-price {
        background: #fef6ee;
        color: #c49a6c;
        font-size: 12px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
        width: fit-content;
        margin-bottom: 12px;
    }

    .project-name {
        font-size: 16px;
        font-weight: 700;
        color: #101828;
        margin-bottom: 4px;
    }

    .project-location {
        font-size: 14px;
        color: #667085;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    .owner-label {
        font-size: 12px;
        color: #c49a6c;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 800;
    }
    </style>
""", unsafe_allow_html=True)

# 2. تحميل البيانات
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

# 3. Sidebar (Filters)
with st.sidebar:
    st.markdown("<h1 style='color:#0f172a; font-size:24px;'>MA3LOMATI.</h1>", unsafe_allow_html=True)
    st.markdown("---")
    if not df.empty:
        C_DEV = df.columns[0]; C_REG = df.columns[4]
        s_dev = st.selectbox("Choose Developer", sorted(df[C_DEV].unique().tolist()))
        s_reg = st.selectbox("Select Location", ["All Locations"] + sorted(df[C_REG].unique().tolist()))
    st.markdown("---")
    st.info("v2.5 - Professional Brokerage Tool")

# 4. Main Body Logic
if not df.empty:
    C_OWNER = df.columns[1]; C_BIO = df.columns[2]; C_PROJ = df.columns[3]; C_PRICE = df.columns[5]
    
    dev_data = df[df[C_DEV] == s_dev]
    
    # Header Section
    st.markdown(f"""
        <div class="main-hero">
            <h1 style="margin:0; font-size:32px; font-weight:900;">{s_dev}</h1>
            <p style="opacity:0.8; margin:5px 0 0 0;">Exclusive Insights & Project Portfolio</p>
        </div>
    """, unsafe_
