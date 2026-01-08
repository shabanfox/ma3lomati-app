import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# رابط البيانات الأساسي
PROJECTS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

# 2. التنسيق (CSS) - شريط التمرير الذهبي وتصميم الكروت الاحترافي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #0d1117; color: white; }
    
    /* شريط التمرير العريض */
    ::-webkit-scrollbar { width: 22px !important; }
    ::-webkit-scrollbar-track { background: #161b22 !important; }
    ::-webkit-scrollbar-thumb { background: #d4af37 !important; border-radius: 10px; border: 4px solid #161b22; }
    
    /* كروت المشاريع المطورة */
    .project-card {
        background: linear-gradient(145deg, #1c2128, #161b22);
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        transition: 0.3s ease;
    }
    .project-card:hover { 
        border-color: #d4af37; 
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(212, 175, 55, 0.1);
    }
    
    .gold-title { color: #d4af37; font-weight: 900; font-size: 1.5em; margin-bottom: 10px; }
    .price-tag { 
        background: #d4af37; color: #000; padding: 5px 15px; 
        border-radius: 8px; font-weight: bold; float: left;
    }
    .location-box { font-size: 0.9em; opacity: 0.8; margin-bottom: 15px; }
    .details-grid { 
        display: grid; grid-template-columns: 1fr 1fr; 
        gap: 15px; border-top: 1px solid #30363d; padding-top: 15px;
    }
    .detail-item { font-size: 0.85em; }
    .detail-label { color: #d4af37; font-weight: bold; }
    
    /* تنسيق البحث */
    .stTextInput > div > div > input {
        background-color: #161b22 !important; color: white !important;
        border: 2px solid #30363d !important; border-radius: 15px !important;
        height: 55px; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=10)
def load_data():
    try:
        res = requests.get(PROJECTS_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.astype(str).replace(['nan', 'NaN'], 'غير مدرج')
    except: return pd.DataFrame()

# --- محتوى الصفحة ---

st.markdown("<h1 style='text-align:center; color:#d4af37;'>🏢 منصة معلوماتي العقارية</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; opacity:0.7;'>دليل المشروعات الذكي لبروكرز مصر</p>", unsafe_allow_html=True)

# 1. قسم البحث والفلاتر
df = load_data()

if not df.empty:
    col_search, col_filter = st.columns([2, 1])
    
    with col_search:
        search = st.text_input("", placeholder="🔍 ابحث باسم المشروع، المطور، أو المنطقة...")
    
    with col_filter:
        # فلاتر سريعة (بناءً على المناطق الموجودة في الشيت)
        regions = ["الكل"] + sorted(df['المنطقة'].unique().tolist())
        selected_region = st.selectbox("تصفية حسب المنطقة:", regions)

    # تطبيق الفلاتر
    filtered_df = df.copy()
    if search:
        filtered_df = filtered_df[filtered_df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if selected_region != "الكل":
        filtered_df = filtered_df[filtered_df['المنطقة'] == selected_region]

    st.markdown(f"---")
    st.markdown(f"**عدد المشاريع المتاحة: {len(filtered_df)}**")

    # 2. عرض المشاريع في كروت
    for _, row in filtered_df.iterrows():
        st.markdown(f"""
            <div class="project-card">
                <div class="price-tag">💰 {row.get('السعر', 'اتصل')}</div>
                <div class="gold-title">{row.get('المشروع', '-')}</div>
                <div class="location-box">📍 {row.get('المنطقة', '-')} | 🏢 المطور: {row.get('المطور', '-')}</div>
                
                <div style="background: rgba(212,175,55,0.03); padding: 15px; border-right: 3px solid #d4af37; border-radius: 5px; margin-bottom: 15px;">
                    <b style="color:#d4af37;">📜 تفاصيل المشروع:</b><br>
                    {row.get('سابقة_الأعمال', 'لا توجد تفاصيل إضافية')}
                </div>
                
                <div class="details-grid">
                    <div class="detail-item"><span class="detail-label">👤 المالك:</span> {row.get('المالك', '-')}</div>
                    <div class="detail-item"><span class="detail-label">💳 السداد:</span> {row.get('السداد', '-')}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("⚠️ جاري تحميل البيانات من جدول جوجل... تأكد من استقرار الإنترنت.")
