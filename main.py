import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI | Broker Tool", layout="wide")

# 2. CSS منفصل تماماً لتجنب أخطاء Syntax
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;500;700;800&family=Cairo:wght@400;700;900&display=swap');
    
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #fcfcfd !important;
        font-family: 'Plus Jakarta Sans', 'Cairo', sans-serif;
        color: #101828;
    }

    /* الهيدر الرئيسي */
    .main-hero {
        background: #0f172a;
        padding: 30px 40px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
        border-left: 5px solid #c49a6c;
    }

    /* لوحة البروفايل على اليمين */
    .dev-profile {
        background: #ffffff;
        border-radius: 16px;
        padding: 25px;
        border: 1px solid #eaecf0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    /* شبكة الكروت على اليسار */
    .projects-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 15px;
    }

    .card {
        background: #ffffff;
        border: 1px solid #eaecf0;
        border-radius: 12px;
        padding: 15px;
        transition: 0.3s ease;
        min-height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .card:hover {
        transform: translateY(-5px);
        border-color: #c49a6c;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }

    .price {
        color: #c49a6c;
        font-weight: 800;
        font-size: 0.8rem;
        margin-bottom: 8px;
    }
    .title {
        font-weight: 700;
        font-size: 1rem;
        color: #101828;
    }
    .loc {
        color: #667085;
        font-size: 0.8rem;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
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

# 4. Sidebar للبحث والفلاتر
with st.sidebar:
    st.markdown("<h2 style='color:#0f172a;'>MA3LOMATI.</h2>", unsafe_allow_html=True)
    if not df.empty:
        c_dev_name = df.columns[0]
        c_reg_name = df.columns[4] if len(df.columns) > 4 else df.columns[0]
        
        s_dev = st.selectbox("Developer", sorted(df[c_dev_name].unique().tolist()))
        s_reg = st.selectbox("Location", ["All"] + sorted(df[c_reg_name].unique().tolist()))
    st.write("---")
    st.caption("Premium Broker Insight v3.0")

# 5. عرض المحتوى
if not df.empty:
    # تحديد الأعمدة
    c_owner = df.columns[1] if len(df.columns) > 1 else ""
    c_bio = df.columns[2] if len(df.columns) > 2 else ""
    c_proj = df.columns[3] if len(df.columns) > 3 else ""
    c_price = df.columns[5] if len(df.columns) > 5 else ""

    dev_data = df[df[c_dev_name] == s_dev]

    # هيدر الصفحة
    st.markdown(f'<div class="main-hero"><h1>{s_dev}</h1><p>Developer Portfolio & Chairman Insights</p></div>', unsafe_allow_html=True)

    # تقسيم الشاشة (يسار للمشاريع | يمين للمعلومات)
    col_left, col_right = st.columns([2.5, 1], gap="medium")

    with col_right:
        if not dev_data.empty:
            row = dev_data.iloc[0]
            st.markdown('<div class="dev-profile">', unsafe_allow_html=True)
            st.markdown(f"<small style='color:#c49a6c; font-weight:bold;'>CHAIRMAN</small>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='margin:0 0 15px 0;'>{row[c_owner]}</h3>", unsafe_allow_html=True)
            st.markdown("<hr style='opacity:0.1'>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:0.9rem; line-height:1.6; color:#475569;'>{row[c_bio]}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_left:
        filtered_df = dev_data
        if s_reg != "All":
            filtered_df = dev_data[dev_data[c_reg_name] == s_reg]
        
        st.markdown(f"<h4 style='margin-bottom:15px;'>Inventory ({len(filtered_df)})</h4>", unsafe_allow_html=True)
        st.markdown('<div class="projects-grid">', unsafe_allow_html=True)
        for _, r in filtered_df.iterrows():
            if r[c_proj] != "-":
                st.markdown(f"""
                    <div class="card">
                        <div>
                            <div class="price">{r[c_price]}</div>
                            <div class="title">{r[c_proj]}</div>
                        </div>
                        <div class="loc">📍 {r[c_reg_name]}</div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Data Sync Failed.")
