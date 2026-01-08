import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="M A S T E R _ R A D A R", layout="wide")

# --- التعديل الجوهري هنا ---
# الرابط المباشر بصيغة CSV لضمان عدم قراءة أكواد HTML من جوجل
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

@st.cache_data(ttl=5)
def load_and_clean_data():
    try:
        response = requests.get(CSV_URL)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            # قراءة البيانات مع تجاهل الأسطر الفارغة
            df = pd.read_csv(StringIO(response.text))
            # تنظيف أسماء الأعمدة من أي مسافات
            df.columns = [str(c).strip() for c in df.columns]
            # تحويل البيانات لنصوص لمنع أخطاء النوع
            df = df.astype(str).replace(['nan', 'NaN', 'None', 'nan '], 'غير مدرج')
            return df
        return pd.DataFrame()
    except Exception as e:
        st.error(f"حدث خطأ أثناء جلب البيانات: {e}")
        return pd.DataFrame()

# 2. تصميم الواجهة الاحترافية (Dark & Gold)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .stApp { background-color: #0b0e14; font-family: 'Cairo', sans-serif; color: white; }
    
    .card {
        background: linear-gradient(145deg, #161b22, #0d1117);
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        direction: rtl;
        text-align: right;
    }
    
    .card:hover { border-color: #d4af37; box-shadow: 0 4px 20px rgba(212, 175, 55, 0.1); }
    .gold { color: #d4af37 !important; font-weight: 900; }
    
    .price-tag { 
        background: #d4af37; color: black; padding: 5px 15px; 
        border-radius: 8px; font-weight: bold; float: left; 
    }
    
    .history-box {
        background: rgba(255, 255, 255, 0.03);
        border-right: 4px solid #d4af37;
        padding: 15px;
        border-radius: 5px 12px 12px 5px;
        margin: 15px 0;
    }
    </style>
    """, unsafe_allow_html=True)

df = load_and_clean_data()

if not df.empty:
    st.markdown("<h1 style='text-align:center;' class='gold'>🏙️ M A S T E R _ R A D A R</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:0.6;'>موسوعة المطورين العقاريين في مصر (200+ شركة)</p>", unsafe_allow_html=True)
    st.divider()

    # القائمة الجانبية
    with st.sidebar:
        st.markdown("<h2 class='gold'>فلترة البيانات</h2>", unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث عن (مطور، مشروع، مالك)")
        
        region_col = next((c for c in df.columns if 'المنطقة' in c), None)
        if region_col:
            regions = ["الكل"] + sorted([r for r in df[region_col].unique() if r != "غير مدرج"])
            sel_region = st.selectbox("📍 اختر المنطقة", regions)
        else: sel_region = "الكل"

    # تطبيق الفلترة
    f_df = df.copy()
    if search:
        f_df = f_df[f_df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if sel_region != "الكل" and region_col:
        f_df = f_df[f_df[region_col] == sel_region]

    st.write(f"المتاح حالياً: **{len(f_df)}** مطور ومشروع")
    
    for _, row in f_df.iterrows():
        # جلب البيانات بأسماء مرنة
        name = row.get('المطور', '-')
        project = row.get('المشروع', '-')
        owner = row.get('المالك', '-')
        history = row.get('سابقة_الأعمال', 'لا توجد بيانات')
        price = row.get('السعر', 'اتصل')
        loc = row.get('المنطقة', '-')
        pay = row.get('السداد', '-')

        st.markdown(f"""
            <div class="card">
                <div class="price-tag">{price}</div>
                <div class="gold" style="font-size: 0.8em; letter-spacing: 2px;">REAL ESTATE PROFILE</div>
                <h2 style="margin: 10px 0;">{project}</h2>
                <p style="opacity: 0.7;">🏢 {name} | 📍 {loc}</p>
                
                <div class="history-box">
                    <b class="gold">📜 سابقة الأعمال والخبرة:</b><br>
                    {history}
                </div>
                
                <div style="display: flex; gap: 30px; font-size: 0.9em; border-top: 1px solid #333; padding-top: 15px;">
                    <div><span class="gold">👤 المالك:</span> {owner}</div>
                    <div><span class="gold">💳 السداد:</span> {pay}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.error("⚠️ لم نتمكن من قراءة البيانات. تأكد أن ملف Google Sheets 'منشور للويب' (Publish to Web) بصيغة CSV وليس رابط HTML عادي.")
