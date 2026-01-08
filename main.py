import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الأداة
st.set_page_config(page_title="Broker Intelligence Tool", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
    
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0f172a !important;
        font-family: 'Cairo', sans-serif;
        color: #f1f5f9;
        direction: ltr !important;
    }

    .tool-header {
        background: #1e293b;
        padding: 15px 30px;
        border-bottom: 2px solid #c49a6c;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    .sidebar-info {
        background: #1e293b;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #334155;
        position: sticky; top: 20px;
    }

    .projects-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 15px;
    }

    .broker-card {
        background: #161e2f;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 15px;
        transition: 0.2s;
        border-top: 3px solid #c49a6c;
    }
    .broker-card:hover {
        background: #1e293b;
        border-color: #c49a6c;
        transform: translateY(-3px);
    }

    .price-text { color: #c49a6c; font-weight: 800; font-size: 0.9rem; }
    .project-name { font-weight: 700; font-size: 1rem; margin: 8px 0; color: #fff; }
    .area-tag { color: #94a3b8; font-size: 0.8rem; }
    </style>
""", unsafe_allow_html=True)

# 2. تحميل البيانات بطريقة آمنة
@st.cache_data(ttl=5)
def load_data():
    URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8MmnRw6KGRVIKIfp_-o8KyvhJKVhHLIZKpFngWHeN0WTsjupFMILryY7EKv6m0vPCD0jwcBND-pvk/pub?output=csv"
    try:
        res = requests.get(URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        # تنظيف أسماء الأعمدة من المسافات
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("-").astype(str)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

st.markdown('<div class="tool-header"><div><b style="font-size:1.2rem; color:white;">MA3LOMATI</b> <small style="color:#c49a6c; margin-left:10px;">BROKER ENGINE v5.1</small></div></div>', unsafe_allow_html=True)

if not df.empty:
    # تحديد الأعمدة ديناميكياً لتجنب الـ IndexError
    def get_col_safe(possible_names, default_idx):
        for name in possible_names:
            if name in df.columns: return name
        return df.columns[default_idx] if len(df.columns) > default_idx else df.columns[0]

    COL_DEV = get_col_safe(["المطور", "الشركة", "Developer"], 0)
    COL_OWNER = get_col_safe(["المالك", "الاونر", "Owner"], 1)
    COL_BIO = get_col_safe(["سيرة عن الشركة والاونر", "Bio"], 2)
    COL_PROJ = get_col_safe(["المشروع", "Project"], 3)
    COL_REG = get_col_safe(["المنطقة", "Region"], 4)
    COL_PRICE = get_col_safe(["السعر", "Price"], 5)

    # الفلاتر
    f1, f2 = st.columns(2)
    with f1: 
        s_dev = st.selectbox("🏢 Select Developer", sorted(df[COL_DEV].unique().tolist()))
    with f2: 
        s_reg = st.selectbox("📍 Filter Area", ["All Areas"] + sorted(df[COL_REG].unique().tolist()))

    st.markdown("<hr style='opacity:0.1'>", unsafe_allow_html=True)

    # التقسيم (يسار مشاريع | يمين معلومات)
    col_left, col_right = st.columns([2.8, 1.2], gap="large")

    dev_data = df[df[COL_DEV] == s_dev]

    with col_right:
        # لوحة معلومات المطور (ثابتة)
        if not dev_data.empty:
            row = dev_data.iloc[0]
            st.markdown(f"""
                <div class="sidebar-info">
                    <small style="color:#c49a6c; font-weight:800; letter-spacing:1px;">DEVELOPER DOSSIER</small>
                    <h2 style="margin:10px 0; color:white;">{s_dev}</h2>
                    <div style="background:#0f172a; padding:12px; border-radius:10px; margin-bottom:20px;">
                        <small style="color:#94a3b8;">Chairman / Owner:</small><br>
                        <span style="color:#fff; font-weight:700; font-size:1.1rem;">{row[COL_OWNER]}</span>
                    </div>
                    <p style="font-size:0.9rem; line-height:1.7; color:#cbd5e1; text-align:justify;">{row[COL_BIO]}</p>
                </div>
            """, unsafe_allow_html=True)

    with col_left:
        # تصفية المشاريع حسب المنطقة
        display_df = dev_data
        if s_reg != "All Areas":
            display_df = dev_data[dev_data[COL_REG] == s_reg]
        
        st.markdown(f"<p style='color:#94a3b8; font-size:0.9rem; margin-bottom:15px;'>Showing {len(display_df)} Active Projects</p>", unsafe_allow_html=True)
        st.markdown('<div class="projects-grid">', unsafe_allow_html=True)
        for _, r in display_df.iterrows():
            if r[COL_PROJ] != "-":
                st.markdown(f"""
                    <div class="broker-card">
                        <div class="price-text">EGP {r[COL_PRICE]}</div>
                        <div class="project-name">{r[COL_PROJ]}</div>
                        <div class="area-tag">📍 {r[COL_REG]}</div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("Please wait, syncing data from Google Sheets...")
