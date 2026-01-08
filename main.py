import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة (Nawy Clean UI)
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f0f2f5 !important;
        font-family: 'Cairo', sans-serif;
        direction: ltr !important;
    }

    /* الهيدر الأبيض */
    .header-nawy {
        background: white;
        padding: 15px 40px;
        border-bottom: 1px solid #e1e4e8;
        margin-bottom: 25px;
    }

    /* كارت المطور على اليمين */
    .dev-panel {
        background: white;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #e1e4e8;
        position: sticky; top: 20px;
    }

    /* كروت المشاريع على الشمال */
    .projects-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 15px;
    }

    .project-card {
        background: white;
        border-radius: 12px;
        padding: 18px;
        border: 1px solid #e1e4e8;
        transition: 0.3s;
    }
    .project-card:hover {
        border-color: #0056b3;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    .price-tag { color: #0056b3; font-weight: 800; font-size: 1.1rem; }
    .project-title { font-weight: 700; font-size: 1rem; color: #1c1e21; margin: 8px 0; }
    .location-tag { color: #65676b; font-size: 0.85rem; }
    </style>
""", unsafe_allow_html=True)

# 2. جلب الداتا بأمان
@st.cache_data(ttl=1)
def load_data():
    URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8MmnRw6KGRVIKIfp_-o8KyvhJKVhHLIZKpFngWHeN0WTsjupFMILryY7EKv6m0vPCD0jwcBND-pvk/pub?output=csv"
    try:
        res = requests.get(URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        return df.fillna("-")
    except: return pd.DataFrame()

df = load_data()

# الهيدر
st.markdown('<div class="header-nawy"><h2 style="margin:0; color:#0056b3;">MA3LOMATI <span style="color:#1c1e21">PRO</span></h2></div>', unsafe_allow_html=True)

if not df.empty and len(df.columns) >= 6:
    # إجبار الكود على قراءة الأعمدة بالترتيب (0، 1، 2...) عشان نهرب من الـ KeyError
    dev_col = df.columns[0]   # المطور
    owner_col = df.columns[1] # الاونر
    bio_col = df.columns[2]   # السيرة
    proj_col = df.columns[3]  # المشروع
    reg_col = df.columns[4]   # المنطقة
    price_col = df.columns[5] # السعر

    # الفلاتر
    st.markdown('<div style="padding: 0 40px;">', unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1: s_dev = st.selectbox("Search Developer", sorted(df[dev_col].unique().tolist()))
    with c2: s_reg = st.selectbox("Area", ["All Areas"] + sorted(df[reg_col].unique().tolist()))
    st.markdown('</div><br>', unsafe_allow_html=True)

    # التقسيم (يسار مشاريع | يمين معلومات)
    col_projects, col_info = st.columns([2.5, 1], gap="medium")

    dev_data = df[df[dev_col] == s_dev]

    with col_info:
        # كارت المطور الثابت على اليمين
        first_row = dev_data.iloc[0]
        st.markdown(f"""
            <div class="dev-panel">
                <p style="color:#0056b3; font-size:12px; font-weight:800; margin-bottom:5px;">CORPORATE PROFILE</p>
                <h2 style="margin:0 0 15px 0;">{s_dev}</h2>
                <div style="background:#f0f2f5; padding:12px; border-radius:10px; margin-bottom:15px;">
                    <small style="color:#65676b;">Chairman / Owner</small><br>
                    <b style="color:#1c1e21;">{first_row[owner_col]}</b>
                </div>
                <p style="color:#4b4d50; font-size:14px; line-height:1.6;">{first_row[bio_col]}</p>
            </div>
        """, unsafe_allow_html=True)

    with col_projects:
        # شبكة المشاريع على اليسار
        filt_df = dev_data
        if s_reg != "All Areas": filt_df = dev_data[dev_data[reg_col] == s_reg]
        
        st.markdown(f"<p style='color:#65676b; margin-bottom:15px; padding-left:10px;'>Projects ({len(filt_df)})</p>", unsafe_allow_html=True)
        st.markdown('<div class="projects-grid">', unsafe_allow_html=True)
        for _, r in filt_df.iterrows():
            if str(r[proj_col]) != "-":
                st.markdown(f"""
                    <div class="project-card">
                        <div class="price-tag">EGP {r[price_col]}</div>
                        <div class="project-title">{r[proj_col]}</div>
                        <div class="location-tag">📍 {r[reg_col]}</div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("Data structure mismatch. Ensure you have at least 6 columns in your Sheet.")
