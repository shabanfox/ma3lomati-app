import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="M A S T E R _ R A D A R", layout="wide")

# الرابط الصحيح (محول ليقرأ البيانات فقط)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

@st.cache_data(ttl=5)
def load_data():
    try:
        response = requests.get(CSV_URL)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
            # تنظيف المسافات من أسماء الأعمدة
            df.columns = [str(c).strip() for c in df.columns]
            # تحويل كل شيء لنص لمنع أخطاء الأرقام
            df = df.astype(str).replace(['nan', 'NaN', 'None'], 'غير مدرج')
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        st.error(f"خطأ في الاتصال: {e}")
        return pd.DataFrame()

# 2. التنسيق البصري (Luxury Dark Mode)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .stApp { background-color: #0d1117; font-family: 'Cairo', sans-serif; }
    
    .dev-card {
        background: linear-gradient(145deg, #161b22, #0d1117);
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        direction: rtl;
        text-align: right;
    }
    .dev-card:hover { border-color: #c5a059; box-shadow: 0 0 15px rgba(197, 160, 89, 0.2); }
    .gold-text { color: #c5a059 !important; font-weight: 900; }
    .price-tag { background: #c5a059; color: black; padding: 5px 15px; border-radius: 8px; font-weight: bold; float: left; }
    .history-box { 
        background: rgba(255,255,255,0.03); 
        padding: 15px; border-radius: 10px; 
        margin: 15px 0; border-right: 4px solid #c5a059; 
    }
    h1, h2, h3, p, span, label { color: white !important; }
    .stTextInput input, .stSelectbox div { background-color: #161b22 !important; color: white !important; border-color: #30363d !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. عرض البيانات
df = load_data()

if not df.empty:
    st.markdown("<h1 style='text-align:center;' class='gold-text'>M A S T E R _ R A D A R</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:0.6;'>دليل الـ 200 مطور العقاري في مصر</p>", unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h2 class='gold-text'>فلترة البحث</h2>", unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث عن مطور أو مشروع...")
        
        # التأكد من وجود عمود المنطقة
        col_region = 'المنطقة' if 'المنطقة' in df.columns else df.columns[4] if len(df.columns) > 4 else None
        if col_region:
            regions = ["الكل"] + sorted(list(df[col_region].unique()))
            sel_region = st.selectbox("📍 المنطقة", regions)
        else:
            sel_region = "الكل"

    # التصفية
    f_df = df.copy()
    if search:
        f_df = f_df[f_df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if col_region and sel_region != "الكل":
        f_df = f_df[f_df[col_region] == sel_region]

    # العرض النهائي للكروت
    for _, row in f_df.iterrows():
        # محاولة قراءة الأعمدة مهما كان مسماها في الإكسيل
        dev_name = row.get('المطور', row.get('مطور', 'غير مدرج'))
        project = row.get('المشروع', row.get('اسم المشروع', 'مشروع جديد'))
        owner = row.get('المالك', row.get('المالك / رئيس مجلس الإدارة', '-'))
        history = row.get('سابقة_الأعمال', row.get('سابقة الأعمال (أهم المشاريع)', 'لا توجد بيانات'))
        price = row.get('السعر', row.get('السعر التقريبي (يبدأ من)', 'اتصل'))
        region = row.get('المنطقة', '-')
        payment = row.get('السداد', row.get('نظام السداد', '-'))

        st.markdown(f"""
            <div class="dev-card">
                <div class="price-tag">{price}</div>
                <div class="gold-text" style="font-size: 0.85em;">DEVELOPER: {dev_name}</div>
                <h2 style="margin: 10px 0;">{project}</h2>
                <p style="opacity: 0.7;">📍 {region}</p>
                
                <div class="history-box">
                    <b class="gold-text">📜 سابقة الأعمال والخبرة:</b><br>
                    {history}
                </div>
                
                <div style="display: flex; gap: 40px; font-size: 0.9em; opacity: 0.8;">
                    <div><span class="gold-text">👤 المالك:</span> {owner}</div>
                    <div><span class="gold-text">💳 السداد:</span> {payment}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.error("⚠️ فشل تحميل البيانات. تأكد من أن ملف الإكسيل يحتوي
