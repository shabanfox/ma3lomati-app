import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الأداة
st.set_page_config(page_title="Broker Intelligence Tool", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
    
    /* إخفاء الزوائد لزيادة مساحة العمل */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0f172a !important; /* لون كحلي غامق بروفيشنال */
        font-family: 'Cairo', sans-serif;
        color: #f1f5f9;
        direction: ltr !important;
    }

    /* هيدر الأداة */
    .tool-header {
        background: #1e293b;
        padding: 15px 30px;
        border-bottom: 2px solid #c49a6c;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    /* لوحة المطور الثابتة (يمين) */
    .sidebar-info {
        background: #1e293b;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #334155;
        position: sticky;
        top: 20px;
    }

    /* شبكة المشاريع المكثفة (يسار) */
    .projects-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
        gap: 12px;
    }

    /* الكارت النحيف للبروكر */
    .broker-card {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 12px;
        transition: 0.2s;
        border-left: 4px solid #c49a6c;
    }
    .broker-card:hover {
        background: #1e293b;
        border-color: #c49a6c;
    }

    .price-text {
        color: #c49a6c;
        font-weight: 800;
        font-size: 0.85rem;
    }
    .project-name {
        font-weight: 600;
        font-size: 0.9rem;
        margin: 5px 0;
        color: #f8fafc;
    }
    .area-tag {
        color: #94a3b8;
        font-size: 0.75rem;
    }

    /* تحسين شكل الفلاتر */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 2. تحميل الداتا
@st.cache_data(ttl=5)
def load_data():
    URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8MmnRw6KGRVIKIfp_-o8KyvhJKVhHLIZKpFngWHeN0WTsjupFMILryY7EKv6m0vPCD0jwcBND-pvk/pub?output=csv"
    try:
        res = requests.get(URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("-").astype(str)
    except: return pd.DataFrame()

df = load_data()

# Header
st.markdown('<div class="tool-header"><div><b style="font-size:1.2rem;">MA3LOMATI</b> <small style="color:#c49a6c; margin-left:10px;">BROKER ENGINE v5.0</small></div></div>', unsafe_allow_html=True)

if not df.empty:
    # الفلاتر (أفقية وسريعة)
    f1, f2 = st.columns(2)
    with f1: s_dev = st.selectbox("🏢 Select Developer", sorted(df.iloc[:, 0].unique().tolist()))
    with f2: s_reg = st.selectbox("📍 Filter Area", ["All Areas"] + sorted(df.iloc[:, 4].unique().tolist()))

    st.markdown("---")

    # التقسيم (يمين معلومات | يسار مشاريع)
    col_cards, col_side = st.columns([2.8, 1.2], gap="medium")

    dev_data = df[df.iloc[:, 0] == s_dev]

    with col_side:
        # لوحة معلومات المطور (للبروكر عشان يقرأ سكريبت المبيعات)
        row = dev_data.iloc[0]
        st.markdown(f"""
            <div class="sidebar-info">
                <small style="color:#c49a6c; font-weight:800; letter-spacing:1px;">DEVELOPER BIO</small>
                <h2 style="margin:10px 0; font-size:1.5rem;">{s_dev}</h2>
                <div style="background:#0f172a; padding:10px; border-radius:8px; margin-bottom:15px;">
                    <small style="color:#94a3b8;">Chairman / Owner:</small><br>
                    <span style="color:#fff; font-weight:700;">{row.iloc[1]}</span>
                </div>
                <p style="font-size:0.85rem; line-height:1.6; color:#cbd5e1; text-align:justify;">{row.iloc[2]}</p>
            </div>
        """, unsafe_allow_html=True)

    with col_cards:
        # عرض المشاريع بشكل مكثف (Inventory Grid)
        f_df = dev_data
        if s_reg != "All Areas": f_df = dev_data[dev_data.iloc[:, 4] == s_reg]
        
        st.markdown(f"<p style='color:#94a3b8; font-size:0.8rem; margin-bottom:15px;'>Active Inventory: {len(f_df)} Projects</p>", unsafe_allow_html=True)
        st.markdown('<div class="projects-grid">', unsafe_allow_html=True)
        for _, r in f_df.iterrows():
            if r.iloc[3] != "-":
                st.markdown(f"""
                    <div class="broker-card">
                        <div class="price-text">{r.iloc[5]}</div>
                        <div class="project-name">{r.iloc[3]}</div>
                        <div class="area-tag">📍 {r.iloc[4]}</div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Data Syncing Error...")
