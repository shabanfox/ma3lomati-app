import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Configuration
st.set_page_config(page_title="Ma3lomati | Broker Tool", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* Hide Streamlit components */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: ltr !important;
        text-align: left !important;
        font-family: 'Cairo', sans-serif;
        background-color: #f0f2f5;
    }

    /* Minimalist Header */
    .top-header {
        background: #0f172a;
        padding: 20px;
        text-align: center;
        color: white;
        border-bottom: 3px solid #c49a6c;
    }

    /* Main Layout Columns */
    .main-wrapper {
        display: flex;
        gap: 20px;
        padding: 20px;
        flex-direction: row-reverse; /* This puts Info on Right and Cards on Left */
    }

    /* Right Side: Developer Info */
    .info-panel {
        flex: 1;
        background: white;
        border-radius: 15px;
        padding: 25px;
        height: fit-content;
        position: sticky;
        top: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-left: 5px solid #c49a6c;
    }

    /* Left Side: Projects Grid */
    .cards-panel {
        flex: 2.5;
    }

    .project-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 15px;
    }

    /* Slim Luxury Card */
    .premium-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #eef0f2;
        transition: all 0.3s ease;
        min-height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        border-color: #c49a6c;
    }
    
    .price-badge {
        color: #c49a6c;
        font-weight: 800;
        font-size: 0.8em;
        margin-bottom: 5px;
        display: block;
    }

    .project-title {
        font-weight: 700;
        font-size: 0.95em;
        color: #1a1a1a;
        margin-bottom: 5px;
    }
    .project-loc {
        color: #888;
        font-size: 0.8em;
    }

    /* Filter Box */
    .filter-container {
        background: white;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }
    </style>
""", unsafe_allow_html=True)

# 2. Data Loading
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

st.markdown('<div class="top-header"><h1>Ma3lomati</h1></div>', unsafe_allow_html=True)

if not df.empty:
    # Column Finder
    C_DEV = "المطور" if "المطور" in df.columns else df.columns[0]
    C_OWNER = "المالك" if "المالك" in df.columns else df.columns[1]
    C_BIO = "سيرة عن الشركة والاونر" if "سيرة عن الشركة والاونر" in df.columns else df.columns[2]
    C_PROJ = "المشروع" if "المشروع" in df.columns else df.columns[3]
    C_REG = "المنطقة" if "المنطقة" in df.columns else df.columns[4]
    C_PRICE = "السعر" if "السعر" in df.columns else df.columns[5]

    # Filters Area
    with st.container():
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a: s_dev = st.selectbox("Select Developer", sorted(df[C_DEV].unique().tolist()))
        with col_b: s_reg = st.selectbox("Filter Location", ["All Locations"] + sorted(df[C_REG].unique().tolist()))
        st.markdown('</div>', unsafe_allow_html=True)

    # Main Content Columns
    # Left side for cards, Right side for Info
    col_left, col_right = st.columns([2.5, 1])

    dev_data = df[df[C_DEV] == s_dev]
    first_row = dev_data.iloc[0]

    with col_right:
        st.markdown(f"""
            <div class="info-panel">
                <h2 style="color:#c49a6c; margin-top:0;">{s_dev}</h2>
                <p><b>Owner:</b> {first_row[C_OWNER]}</p>
                <hr style="opacity:0.1">
                <p style="font-size:0.9em; line-height:1.6; color:#555;">{first_row[C_BIO]}</p>
            </div>
        """, unsafe_allow_html=True)

    with col_left:
        # Filter projects by location if selected
        display_df = dev_data
        if s_reg != "All Locations":
            display_df = dev_data[dev_data[C_REG] == s_reg]
        
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, r in display_df.iterrows():
            if r[C_PROJ] != "-":
                st.markdown(f"""
                    <div class="premium-card">
                        <div>
                            <span class="price-badge">{r[C_PRICE]}</span>
                            <div class="project-title">{r[C_PROJ]}</div>
                        </div>
                        <div class="project-loc">📍 {r[C_REG]}</div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Check your CSV link.")
