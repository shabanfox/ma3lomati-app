import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعداد الصفحة (يجب أن يظل أول سطر)
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# 2. روابط البيانات
PROJECTS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

# 3. التنسيق (CSS) - شريط تمرير عريض وتصميم الفلاتر
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #0d1117; color: white; }
    [data-testid="stSidebar"] { display: none; }
    
    /* شريط التمرير الذهبي */
    ::-webkit-scrollbar { width: 22px !important; }
    ::-webkit-scrollbar-track { background: #161b22 !important; }
    ::-webkit-scrollbar-thumb { background: #d4af37 !important; border-radius: 10px; border: 4px solid #161b22; }
    
    .gold { color: #d4af37 !important; font-weight: 900; }
    
    /* تصميم خانات البحث */
    .stTextInput > div > div > input {
        background-color: #1c2128 !important; color: white !important;
        border: 1px solid #d4af37 !important; border-radius: 10px !important;
        text-align: center;
    }

    .project-card {
        background: #1c2128; border: 1px solid #30363d; border-radius: 15px;
        padding: 25px; margin-bottom: 20px;
    }
    .price-badge { 
        background: #d4af37; color: black; padding: 5px 15px; 
        border-radius: 8px; font-weight: bold; float: left;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. دالة جلب البيانات
@st.cache_data(ttl=5)
def load_data():
    try:
        response = requests.get(PROJECTS_URL)
        response.encoding = 'utf-8'
        df = pd.read_csv(StringIO(response.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("غير مدرج").astype(str)
    except:
        return pd.DataFrame()

# العنوان الرئيسي
st.markdown("<h1 style='text-align:center;' class='gold'>🏢 دليل المشاريع الذكي</h1>", unsafe_allow_html=True)

df = load_data()

if not df.empty:
    # 5. الثلاث خانات بحث في صف واحد
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_region = st.text_input("📍 ابحث بالمنطقة", placeholder="مثال: التجمع")
    
    with col2:
        search_price = st.text_input("💰 ابحث بالسعر", placeholder="مثال: 4,000,000")
        
    with col3:
        # تأكد أن اسم العمود في الإكسيل هو "النوع" أو "نوع الوحدة"
        search_type = st.text_input("🏗️ نوع الوحدة", placeholder="مثال: سكني / إداري")

    # 6. منطق الفلترة المتقاطع
    filtered_df = df.copy()

    if search_region:
        filtered_df = filtered_df[filtered_df['المنطقة'].str.contains(search_region, case=False)]
    
    if search_price:
        # البحث في عمود السعر
        filtered_df = filtered_df[filtered_df['السعر'].str.contains(search_price, case=False)]
        
    if search_type:
        # ببحث في عمود "النوع" (تأكد من وجوده في الشيت)
        if 'النوع' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['النوع'].str.contains(search_type, case=False)]
        else:
            # لو العمود مش موجود ببحث في كل البيانات كبديل مؤقت
            filtered_df = filtered_df[filtered_df.apply(lambda r: search_type in str(r), axis=1)]

    st.markdown(f"**النتائج المطابقة: {len(filtered_df)}**")
    st.markdown("---")

    # 7. عرض النتائج
    for _, row in filtered_df.iterrows():
        st.markdown(f"""
            <div class="project-card">
                <div class="price-badge">{row.get('السعر', '-')}</div>
                <h2 class="gold">{row.get('المشروع', '-')}</h2>
                <p>📍 {row.get('المنطقة', '-')} | 🏢 {row.get('المطور', '-')}</p>
                <div style="background:rgba(212,175,55,0.05); padding:15px; border-right:4px solid #d4af37; border-radius:5px;">
                    <b class="gold">📜 سابقة الأعمال والنوع:</b><br>
                    {row.get('النوع', 'غير محدد')} - {row.get('سابقة_الأعمال', '-')}
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("جاري تحميل البيانات...")
