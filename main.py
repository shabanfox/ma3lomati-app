import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Config
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;700;900&display=swap');
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    html, body, [data-testid="stAppViewContainer"] { background-color: #f8fafc !important; font-family: 'Cairo', sans-serif; direction: ltr !important; }
    .nawy-nav { background: white; padding: 15px 40px; border-bottom: 1px solid #e2e8f0; margin-bottom: 30px; }
    .sticky-dev-card { background: white; border-radius: 12px; padding: 24px; border: 1px solid #e2e8f0; position: sticky; top: 20px; }
    .nawy-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; }
    .property-card { background: white; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; min-height: 150px; display: flex; flex-direction: column; justify-content: space-between; }
    .price-nawy { color: #0052cc; font-weight: 800; font-size: 1.15rem; }
    .title-nawy { font-weight: 700; font-size: 1rem; color: #1e293b; margin: 8px 0; }
    .loc-nawy { color: #64748b; font-size: 0.85rem; }
    </style>
""", unsafe_allow_html=True)

# 2. تحميل البيانات مع تسمية الأعمدة يدوياً لضمان عدم الخطأ
@st.cache_data(ttl=5)
def load_data():
    URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8MmnRw6KGRVIKIfp_-o8KyvhJKVhHLIZKpFngWHeN0WTsjupFMILryY7EKv6m0vPCD0jwcBND-pvk/pub?output=csv"
    try:
        res = requests.get(URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        # تنظيف الداتا من المسافات الزايدة
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

df = load_data()

# الهيدر
st.markdown('<div class="nawy-nav"><h2 style="margin:0; color:#0052cc; font-weight:900;">MA3LOMATI PRO</h2></div>', unsafe_allow_html=True)

if not df.empty:
    # ربط الأعمدة بأساميها الحقيقية من الشيت بتاعك
    # تأكد إن الأسامي دي مطابقة للي في أول صف في جوجل شيت
    COL_DEV = "المطور"
    COL_OWNER = "الاونر"
    COL_BIO = "سيرة عن الشركة والاونر"
    COL_PROJ = "المشروع"
    COL_REG = "المنطقة"
    COL_PRICE = "السعر"

    # الفلاتر
    st.markdown('<div style="padding: 0 40px;">', unsafe_allow_html=True)
    f1, f2 = st.columns([2, 1])
    with f1: 
        s_dev = st.selectbox("اختر المطور", sorted(df[COL_DEV].dropna().unique().tolist()))
    with f2: 
        s_reg = st.selectbox("المنطقة", ["الكل"] + sorted(df[COL_REG].dropna().unique().tolist()))
    st.markdown('</div><br>', unsafe_allow_html=True)

    # المحتوى
    col_content, col_sidebar = st.columns([2.8, 1.2], gap="large")
    
    dev_data = df[df[COL_DEV] == s_dev]

    with col_sidebar:
        if not dev_data.empty:
            info = dev_data.iloc[0]
            st.markdown(f"""
                <div class="sticky-dev-card">
                    <h2 style="margin:0 0 15px 0; color:#0f172a;">{s_dev}</h2>
                    <div style="background:#f1f5f9; padding:15px; border-radius:10px; margin-bottom:20px;">
                        <small style="color:#64748b;">الرئيس التنفيذي / المالك</small><br>
                        <b style="color:#1e293b; font-size:1.1rem;">{info[COL_OWNER]}</b>
                    </div>
                    <p style="color:#475569; font-size:0.95rem; line-height:1.7;">{info[COL_BIO]}</p>
                </div>
            """, unsafe_allow_html=True)

    with col_content:
        display_df = dev_data
        if s_reg != "الكل":
            display_df = dev_data[dev_data[COL_REG] == s_reg]
        
        st.markdown(f"<p style='color:#64748b; margin-bottom:15px;'>المشاريع المتاحة ({len(display_df)})</p>", unsafe_allow_html=True)
        st.markdown('<div class="nawy-grid">', unsafe_allow_html=True)
        for _, r in display_df.iterrows():
            st.markdown(f"""
                <div class="property-card">
                    <div>
                        <div class="price-nawy">{r[COL_PRICE]}</div>
                        <div class="title-nawy">{r[COL_PROJ]}</div>
                    </div>
                    <div class="loc-nawy">📍 {r[COL_REG]}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("فشل في قراءة البيانات. تأكد أن رابط جوجل شيت متاح للجميع (Public).")
