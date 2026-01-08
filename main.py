import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعداد الصفحة (يجب أن يظل أول سطر)
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# 2. روابط البيانات
PROJECTS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

# 3. التنسيق (CSS) - شريط تمرير عريض + تصميم ثابت
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #0d1117; color: white; }
    [data-testid="stSidebar"] { display: none; }
    
    /* شريط التمرير الذهبي العريض */
    ::-webkit-scrollbar { width: 22px !important; }
    ::-webkit-scrollbar-track { background: #161b22 !important; }
    ::-webkit-scrollbar-thumb { background: #d4af37 !important; border-radius: 10px; border: 4px solid #161b22; }
    
    .project-card {
        background: #1c2128; border: 1px solid #30363d; border-radius: 15px;
        padding: 25px; margin-bottom: 20px; position: relative;
    }
    .gold { color: #d4af37 !important; font-weight: 900; }
    .price-badge { 
        background: #d4af37; color: black; padding: 5px 15px; 
        border-radius: 8px; font-weight: bold; float: left;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. دالة جلب البيانات مع معالجة الأخطاء
@st.cache_data(ttl=5)
def load_data():
    try:
        response = requests.get(PROJECTS_URL)
        response.encoding = 'utf-8'
        raw_data = StringIO(response.text)
        df = pd.read_csv(raw_data)
        # تنظيف أسماء الأعمدة من المسافات
        df.columns = [str(c).strip() for c in df.columns]
        # تحويل كل البيانات لنصوص لتجنب أخطاء البحث
        return df.fillna("غير مدرج").astype(str)
    except Exception as e:
        st.error(f"خطأ في جلب البيانات: {e}")
        return pd.DataFrame()

# 5. عرض المحتوى
st.markdown("<h1 style='text-align:center;' class='gold'>🏢 منصة معلوماتي العقارية</h1>", unsafe_allow_html=True)

df = load_data()

if not df.empty:
    # محرك البحث
    col_search_1, col_search_2, col_search_3 = st.columns([1, 2, 1])
    with col_search_2:
        search_query = st.text_input("", placeholder="🔍 ابحث عن مشروع، مطور، أو منطقة...")

    # الفلترة
    if search_query:
        # البحث في كل الأعمدة بدون حساسية لحالة الأحرف
        mask = df.apply(lambda row: row.str.contains(search_query, case=False).any(), axis=1)
        display_df = df[mask]
    else:
        display_df = df

    st.write(f"عدد النتائج: {len(display_df)}")

    # عرض الكروت
    for index, row in display_df.iterrows():
        # استخراج البيانات بأمان باستخدام .get لضمان عدم حدوث خطأ KeyError
        prj_name = row.get('المشروع', '-')
        dev_name = row.get('المطور', '-')
        location = row.get('المنطقة', '-')
        price = row.get('السعر', 'اتصل')
        owner = row.get('المالك', '-')
        payment = row.get('السداد', '-')
        history = row.get('سابقة_الأعمال', 'لا توجد تفاصيل')

        st.markdown(f"""
            <div class="project-card">
                <div class="price-badge">{price}</div>
                <h2 class="gold" style="margin-top:0;">{prj_name}</h2>
                <p style="margin-bottom:10px;">📍 {location} | 🏢 {dev_name}</p>
                <div style="background:rgba(212,175,55,0.05); padding:15px; border-right:4px solid #d4af37; border-radius:5px;">
                    <b class="gold">📜 التفاصيل:</b><br>{history}
                </div>
                <div style="display:flex; gap:30px; margin-top:15px; border-top:1px solid #333; padding-top:10px;">
                    <div><span class="gold">👤 المالك:</span> {owner}</div>
                    <div><span class="gold">💳 السداد:</span> {payment}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("جاري مزامنة قاعدة البيانات... يرجى الانتظار.")
