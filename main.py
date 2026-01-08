import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Config
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;700;900&family=Inter:wght@400;700&display=swap');
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    html, body, [data-testid="stAppViewContainer"] { background-color: #f8fafc !important; font-family: 'Inter', 'Cairo', sans-serif; direction: ltr !important; }
    .nawy-nav { background: white; padding: 15px 40px; border-bottom: 1px solid #e2e8f0; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center;}
    .dev-profile-card { background: white; border-radius: 12px; padding: 25px; border: 1px solid #e2e8f0; position: sticky; top: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    .nawy-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }
    .prop-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; transition: 0.2s; min-height: 150px; display: flex; flex-direction: column; justify-content: space-between; }
    .prop-card:hover { border-color: #0052cc; transform: translateY(-3px); box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
    .price-text { color: #0052cc; font-weight: 800; font-size: 1.1rem; }
    .title-text { font-weight: 700; font-size: 1rem; color: #1e293b; margin: 8px 0; }
    .loc-text { color: #64748b; font-size: 0.85rem; }
    </style>
""", unsafe_allow_html=True)

# 2. تحميل البيانات وتحديد الأعمدة تلقائياً
@st.cache_data(ttl=2)
def load_data():
    URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8MmnRw6KGRVIKIfp_-o8KyvhJKVhHLIZKpFngWHeN0WTsjupFMILryY7EKv6m0vPCD0jwcBND-pvk/pub?output=csv"
    try:
        res = requests.get(URL); res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns] # تنظيف أسماء الأعمدة
        return df
    except: return pd.DataFrame()

df = load_data()

# Navbar
st.markdown('<div class="nawy-nav"><h2 style="margin:0; color:#0052cc; font-weight:900; font-size:1.5rem;">MA3LOMATI<span style="color:#1e293b">PRO</span></h2></div>', unsafe_allow_html=True)

if not df.empty:
    # دالة ذكية لإيجاد العمود حتى لو اسمه اتغير بسيط
    def find_col(keywords, default_idx):
        for col in df.columns:
            if any(k in col for k in keywords): return col
        return df.columns[default_idx]

    C_DEV = find_col(["المطور", "Developer", "الشركة"], 0)
    C_OWNER = find_col(["الاونر", "Owner", "المالك"], 1)
    C_BIO = find_col(["سيرة", "Bio", "عن"], 2)
    C_PROJ = find_col(["المشروع", "Project"], 3)
    C_REG = find_col(["المنطقة", "Region", "مكان"], 4)
    C_PRICE = find_col(["السعر", "Price"], 5)

    # Filter Bar
    st.markdown('<div style="padding: 0 40px;">', unsafe_allow_html=True)
    f1, f2 = st.columns([2, 1])
    with f1: s_dev = st.selectbox("Search Developer", sorted(df[C_DEV].unique().tolist()))
    with f2: s_reg = st.selectbox("Location", ["All Egypt"] + sorted(df[C_REG].unique().tolist()))
    st.markdown('</div><br>', unsafe_allow_html=True)

    # Main Layout
    col_inv, col_side = st.columns([2.8, 1.2], gap="large")
    
    dev_df = df[df[C_DEV] == s_dev]

    with col_side:
        if not dev_df.empty:
            item = dev_df.iloc[0]
            st.markdown(f"""
                <div class="dev-profile-card">
                    <p style="color:#0052cc; font-size:11px; font-weight:800; margin-bottom:10px;">CORPORATE PROFILE</p>
                    <h2 style="margin:0 0 20px 0; color:#0f172a;">{s_dev}</h2>
                    <div style="background:#f1f5f9; padding:15px; border-radius:10px; margin-bottom:20px;">
                        <small style="color:#64748b;">Chairman</small><br>
                        <b style="color:#1e293b; font-size:1.1rem;">{item[C_OWNER]}</b>
                    </div>
                    <p style="color:#475569; font-size:0.95rem; line-height:1.7;">{item[C_BIO]}</p>
                </div>
            """, unsafe_allow_html=True)

    with col_inv:
        filt_df = dev_df
        if s_reg != "All Egypt": filt_df = dev_df[dev_df[C_REG] == s_reg]
        
        st.markdown(f"<p style='color:#64748b; font-weight:600; margin-bottom:15px; padding-left:10px;'>{len(filt_df)} Results Found</p>", unsafe_allow_html=True)
        st.markdown('<div class="nawy-grid">', unsafe_allow_html=True)
        for _, r in filt_df.iterrows():
            if str(r[C_PROJ]) != "nan" and r[C_PROJ] != "-":
                st.markdown(f"""
                    <div class="prop-card">
                        <div>
                            <div class="price-text">EGP {r[C_PRICE]}</div>
                            <div class="title-text">{r[C_PROJ]}</div>
                        </div>
                        <div class="loc-text">📍 {r[C_REG]}</div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Data source error. Please check your Google Sheet link.")
