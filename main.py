import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Configuration
st.set_page_config(page_title="Ma3lomati | Broker Tool", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: ltr !important;
        text-align: left !important;
        font-family: 'Cairo', sans-serif;
        background-color: #f8f9fb;
    }

    .top-header {
        background: #0f172a; padding: 15px; text-align: center;
        color: white; border-bottom: 3px solid #c49a6c; margin-bottom: 20px;
    }

    /* Right Side: Info Panel */
    .info-panel {
        background: white; border-radius: 15px; padding: 25px;
        border-left: 8px solid #c49a6c; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    /* Left Side: Small Cards */
    .project-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
        gap: 12px;
    }

    .premium-card {
        background: white; border-radius: 12px; padding: 15px;
        border: 1px solid #eee; transition: 0.3s; min-height: 140px;
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .premium-card:hover {
        transform: translateY(-5px); border-color: #c49a6c;
        box-shadow: 0 10px 20px rgba(0,0,0,0.08);
    }
    
    .price-badge { color: #c49a6c; font-weight: 800; font-size: 0.8em; }
    .project-title { font-weight: 700; font-size: 0.9em; color: #1a1a1a; margin: 5px 0; }
    .project-loc { color: #888; font-size: 0.75em; }

    .filter-box {
        background: white; padding: 15px; border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03); margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Data Loading (استخدام رابط الـ CSV المباشر أضمن بكتير)
RAW_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8MmnRw6KGRVIKIfp_-o8KyvhJKVhHLIZKpFngWHeN0WTsjupFMILryY7EKv6m0vPCD0jwcBND-pvk/pub?output=csv"

@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(RAW_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("-").astype(str)
    except:
        return pd.DataFrame()

df = load_data()

st.markdown('<div class="top-header"><h1>Ma3lomati</h1></div>', unsafe_allow_html=True)

if not df.empty:
    # Safe Column Access (حل مشكلة IndexError)
    def get_col(name, index):
        if name in df.columns: return name
        return df.columns[index] if len(df.columns) > index else df.columns[0]

    C_DEV = get_col("المطور", 0)
    C_OWNER = get_col("المالك", 1)
    C_BIO = get_col("سيرة عن الشركة والاونر", 2)
    C_PROJ = get_col("المشروع", 3)
    C_REG = get_col("المنطقة", 4)
    C_PRICE = get_col("السعر", 5)

    # Filters
    st.markdown('<div class="filter-box">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: s_dev = st.selectbox("Select Developer", sorted(df[C_DEV].unique().tolist()))
    with c2: s_reg = st.selectbox("Filter Location", ["All"] + sorted(df[C_REG].unique().tolist()))
    st.markdown('</div>', unsafe_allow_html=True)

    # Layout: Left (Cards) | Right (Info)
    col_cards, col_info = st.columns([2.5, 1])

    dev_data = df[df[C_DEV] == s_dev]
    
    with col_info:
        if not dev_data.empty:
            main = dev_data.iloc[0]
            st.markdown(f"""
                <div class="info-panel">
                    <h2 style="color:#c49a6c; margin-top:0;">{s_dev}</h2>
                    <p style="font-size:0.9em;"><b>Owner:</b> {main[C_OWNER]}</p>
                    <hr style="opacity:0.1">
                    <p style="font-size:0.85em; line-height:1.6; color:#555;">{main[C_BIO]}</p>
                </div>
            """, unsafe_allow_html=True)

    with col_cards:
        display_df = dev_data
        if s_reg != "All":
            display_df = dev_data[dev_data[C_REG] == s_reg]
        
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, r in display_df.iterrows():
            if r[C_PROJ] != "-":
                st.markdown(f"""
                    <div class="premium-card">
                        <div>
                            <div class="price-badge">{r[C_PRICE]}</div>
                            <div class="project-title">{r[C_PROJ]}</div>
                        </div>
                        <div class="project-loc">📍 {r[C_REG]}</div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Data could not be loaded. Please check your Google Sheet 'Publish to Web' settings and ensure CSV format is selected.")
