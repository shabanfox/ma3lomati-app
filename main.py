import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="Egypt Real Estate Encyclopedia", layout="wide", page_icon="🏢")

# تحويل رابط pubhtml إلى رابط CSV لضمان استقرار جلب البيانات
RAW_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

@st.cache_data(ttl=10)
def load_data():
    try:
        response = requests.get(RAW_URL)
        response.encoding = 'utf-8'
        df = pd.read_csv(StringIO(response.text))
        # تنظيف أسامي الأعمدة من المسافات
        df.columns = [str(c).strip() for c in df.columns]
        # تأمين البيانات: تحويل كل شيء لنصوص لمنع أخطاء التنسيق
        df = df.astype(str).replace(['nan', 'NaN', 'None', 'nan '], 'غير محدد')
        return df
    except Exception as e:
        st.error(f"خطأ في الاتصال بقاعدة البيانات: {e}")
        return pd.DataFrame()

# 2. هندسة الشكل العام (Premium CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
    
    .stApp {
        background-color: #0d1117;
        font-family: 'Cairo', sans-serif;
    }

    /* تصميم البطاقة الاحترافية */
    .dev-card {
        background: linear-gradient(145deg, #1c2128, #161b22);
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        direction: rtl;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .dev-card:hover {
        border-color: #d4af37;
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.1);
    }

    .gold-label { color: #d4af37; font-weight: 800; font-size: 0.85em; margin-bottom: 5px; }
    .project-name { color: #ffffff; font-size: 1.8em; font-weight: 800; margin-bottom: 10px; }
    .price-badge { 
        background-color: #d4af37; color: #000; padding: 5px 15px; 
        border-radius: 8px; font-weight: 900; font-size: 1.1em;
    }
    
    .info-box {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        padding: 15px;
        margin-top: 15px;
        border-right: 4px solid #d4af37;
    }

    /* تخصيص السايد بار */
    [data-testid="stSidebar"] { background-color: #161b22 !important; border-left: 1px solid #30363d; }
    h1, h2, h3, p, span { color: #f0f6fc !important; }
    
    .stTextInput input, .stSelectbox div {
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

df = load_data()

if not df.empty:
    # الهيدر
    st.markdown("<h1 style='text-align: center; color: #d4af37; font-weight: 800;'>M A S T E R _ R A D A R</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.7;'>أقوى محرك بحث للمطورين العقاريين في مصر (200+ مطور)</p>", unsafe_allow_html=True)
    st.divider()

    # القائمة الجانبية (البحث والفلترة)
    with st.sidebar:
        st.markdown("<h2 style='color:#d4af37'>🧭 لوحة التحكم</h2>", unsafe_allow_html=True)
        search_query = st.text_input("🔍 بحث (مطور، مالك، مشروع)")
        
        # استخراج المناطق الفريدة بأمان
        if 'المنطقة' in df.columns:
            regions = ["الكل"] + sorted([r for r in df['المنطقة'].unique() if r != 'غير محدد'])
            region_filter = st.selectbox("📍 فلترة بالمنطقة", regions)
        else:
            region_filter = "الكل"

    # تطبيق الفلاتر
    filtered_df = df.copy()
    if search_query:
        mask = filtered_df.apply(lambda row: search_query.lower() in str(row.values).lower(), axis=1)
        filtered_df = filtered_df[mask]
    if region_filter != "الكل":
        filtered_df = filtered_df[filtered_df['المنطقة'] == region_filter]

    # عرض النتائج
    st.write(f"✅ تم العثور على **{len(filtered_df)}** نتيجة")

    for index, row in filtered_df.iterrows():
        st.markdown(f"""
            <div class="dev-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="text-align: right;">
                        <div class="gold-label">DEVELOPER: {row.get('المطور', 'غير مدرج')}</div>
                        <div class="project-name">{row.get('المشروع', 'مشروع غير مسمى')}</div>
                        <div style="margin-top: 5px;">
                            <span style="background: rgba(212, 175, 55, 0.1); color: #d4af37; padding: 2px 10px; border-radius: 5px; font-size: 0.9em;">📍 {row.get('المنطقة', 'غير محدد')}</span>
                            <span style="margin-right: 15px; opacity: 0.6; font-size: 0.9em;">👤 المالك: {row.get('المالك', '-')}</span>
                        </div>
                    </div>
                    <div style="text-align: left;">
                        <div class="price-badge">{row.get('السعر', 'اتصل')}</div>
                    </div>
                </div>
                
                <div class="info-box">
                    <div class="gold-label">📜 سابقة الأعمال والخبرة:</div>
                    <div style="line-height: 1.6; font-size: 0.95em;">{row.get('سابقة_الأعمال', 'لا توجد بيانات')}</div>
                </div>

                <div style="display: flex; gap: 40px; margin-top: 20px; font-size: 0.85em; border-top: 1px solid #30363d; padding-top: 15px;">
                    <div><span style="color: #d4af37;">💳 نظام السداد:</span> {row.get('السداد', '-')}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("🔄 جاري مزامنة البيانات من الإكسيل... تأكد من نشر الملف بصيغة CSV.")
