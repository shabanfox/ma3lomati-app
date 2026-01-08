import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة (يجب أن تكون أول سطر)
st.set_page_config(page_title="M A S T E R _ R A D A R", layout="wide")

# الرابط المباشر للبيانات الخام (CSV)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

@st.cache_data(ttl=5)
def load_data():
    try:
        response = requests.get(CSV_URL)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
            df.columns = [str(c).strip() for c in df.columns]
            df = df.astype(str).replace(['nan', 'NaN', 'None'], 'غير مدرج')
            return df
        return pd.DataFrame()
    except:
        return pd.DataFrame()

# 2. التصميم (CSS) - لإخفاء أي عيوب وإظهار الفخامة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .stApp { background-color: #0b0e14; font-family: 'Cairo', sans-serif; color: white; }
    .card {
        background: linear-gradient(145deg, #161b22, #0d1117);
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        direction: rtl;
        text-align: right;
    }
    .gold { color: #d4af37 !important; font-weight: 900; }
    .price-tag { background: #d4af37; color: black; padding: 5px 15px; border-radius: 8px; font-weight: bold; float: left; }
    .history-box { background: rgba(255, 255, 255, 0.03); border-right: 4px solid #d4af37; padding: 10px; margin: 10px 0; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 3. محرك العرض
df = load_data()

if not df.empty:
    st.markdown("<h1 style='text-align:center;' class='gold'>🏙️ M A S T E R _ R A D A R</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:0.6;'>أقوى قاعدة بيانات عقارية في مصر</p>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("<h2 class='gold'>بحث وفلترة</h2>", unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث (مطور، مشروع، مالك)")
        
        region_col = next((c for c in df.columns if 'المنطقة' in c), None)
        if region_col:
            regions = ["الكل"] + sorted(list(df[region_col].unique()))
            sel_region = st.selectbox("📍 المنطقة", regions)
        else: sel_region = "الكل"

    # تصفية
    f_df = df.copy()
    if search:
        f_df = f_df[f_df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if sel_region != "الكل" and region_col:
        f_df = f_df[f_df[region_col] == sel_region]

    # العرض
    for _, row in f_df.iterrows():
        st.markdown(f"""
            <div class="card">
                <div class="price-tag">{row.get('السعر', 'اتصل')}</div>
                <div class="gold" style="font-size: 0.8em;">REAL ESTATE PROFILE</div>
                <h2 style="margin: 5px 0;">{row.get('المشروع', '-')}</h2>
                <p style="opacity: 0.8;">🏢 {row.get('المطور', '-')} | 📍 {row.get('المنطقة', '-')}</p>
                <div class="history-box">
                    <b class="gold">📜 سابقة الأعمال:</b><br>{row.get('سابقة_الأعمال', 'غير مدرج')}
                </div>
                <div style="display: flex; gap: 30px; font-size: 0.9em; border-top: 1px solid #333; padding-top: 10px;">
                    <div><span class="gold">👤 المالك:</span> {row.get('المالك', '-')}</div>
                    <div><span class="gold">💳 السداد:</span> {row.get('السداد', '-')}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.error("⚠️ فشل في تحميل البيانات. تأكد من نشر ملف الإكسيل كـ CSV.")
