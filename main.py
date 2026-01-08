import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات المنصة الاحترافية
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# الرابط المباشر للبيانات (CSV)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

@st.cache_data(ttl=5)
def load_data():
    try:
        response = requests.get(CSV_URL)
        response.encoding = 'utf-8'
        df = pd.read_csv(StringIO(response.text))
        df.columns = [str(c).strip() for c in df.columns]
        df = df.astype(str).replace(['nan', 'NaN', 'None'], 'غير مدرج')
        return df
    except:
        return pd.DataFrame()

# 2. تصميم الواجهة (Premium UI/UX)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .stApp { background-color: #0d1117; font-family: 'Cairo', sans-serif; color: white; }
    
    /* تنسيق اللوجو والعنوان */
    .main-header { text-align: center; padding: 20px; }
    .logo-text { color: #d4af37; font-size: 3em; font-weight: 900; margin-bottom: 0px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
    .sub-text { color: #ffffff; opacity: 0.8; font-size: 1.2em; margin-bottom: 30px; }
    
    /* جعل البحث في المنتصف */
    .search-container {
        display: flex;
        justify-content: center;
        margin-bottom: 40px;
    }
    
    .stTextInput > div > div > input {
        text-align: center;
        background-color: #161b22 !important;
        color: white !important;
        border: 2px solid #d4af37 !important;
        border-radius: 50px !important;
        height: 50px;
        font-size: 1.2em;
    }

    /* تنسيق الكروت */
    .card {
        background: linear-gradient(145deg, #1c2128, #0d1117);
        border: 1px solid #30363d;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        direction: rtl;
        text-align: right;
        transition: 0.3s;
    }
    .card:hover { border-color: #d4af37; transform: translateY(-5px); }
    .gold { color: #d4af37 !important; font-weight: 900; }
    .price-tag { background: #d4af37; color: black; padding: 6px 18px; border-radius: 10px; font-weight: bold; float: left; }
    </style>
    """, unsafe_allow_html=True)

# 3. نظام تسجيل الدخول (في السايد بار)
with st.sidebar:
    st.markdown("<h2 class='gold'>🔐 بوابة البروكرز</h2>", unsafe_allow_html=True)
    menu = st.tabs(["تسجيل دخول", "حساب جديد"])
    
    with menu[0]:
        st.text_input("البريد الإلكتروني", placeholder="example@mail.com")
        st.text_input("كلمة المرور", type="password")
        st.button("دخول المنصة")
    
    with menu[1]:
        st.text_input("الاسم بالكامل")
        st.text_input("رقم الموبايل")
        st.text_input("شركة العقارات")
        st.button("إنشاء حساب مجاني")
    
    st.divider()
    st.markdown("<p style='text-align:center; font-size:0.8em;'>جميع الحقوق محفوظة لمنصة معلوماتي العقارية © 2026</p>", unsafe_allow_html=True)

# 4. محتوى المنصة الرئيسي
# عرض اللوجو والترحيب
st.markdown("""
    <div class="main-header">
        <div class="logo-text">🏠 منصة معلوماتي العقارية</div>
        <div class="sub-text">المرجع الأول والأقوى لكل بروكرز مصر</div>
    </div>
    """, unsafe_allow_html=True)



# البحث في المنتصف
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    search = st.text_input("", placeholder="🔍 ابحث عن المطور، المشروع، أو المالك الآن...")

# جلب البيانات
df = load_data()

if not df.empty:
    # فلترة سريعة بالمنطقة تحت البحث
    region_col = next((c for c in df.columns if 'المنطقة' in c), None)
    if region_col:
        unique_regions = ["كل المناطق"] + sorted(list(df[region_col].unique()))
        sel_region = st.selectbox("", unique_regions, index=0)
    else: sel_region = "كل المناطق"

    # تطبيق التصفية
    f_df = df.copy()
    if search:
        f_df = f_df[f_df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if sel_region != "كل المناطق" and region_col:
        f_df = f_df[f_df[region_col] == sel_region]

    st.markdown(f"<p style='text-align:center;'>عرض <span class='gold'>{len(f_df)}</span> نتيجة من قاعدة البيانات</p>", unsafe_allow_html=True)

    # عرض النتائج
    for _, row in f_df.iterrows():
        st.markdown(f"""
            <div class="card">
                <div class="price-tag">{row.get('السعر', 'اتصل')}</div>
                <div class="gold" style="font-size: 0.9em;">ملف المطور العقاري</div>
                <h2 style="margin: 10px 0;">{row.get('المشروع', '-')}</h2>
                <p style="font-size: 1.1em;">🏢 {row.get('المطور', '-')} | 📍 {row.get('المنطقة', '-')}</p>
                <div style="background: rgba(255,255,255,0.03); border-right: 4px solid #d4af37; padding: 15px; margin: 15px 0; border-radius: 5px;">
                    <b class="gold">📜 سابقة الأعمال والخبرة:</b><br>{row.get('سابقة_الأعمال', 'غير مدرج')}
                </div>
                <div style="display: flex; gap: 40px; font-size: 1em; border-top: 1px solid #333; padding-top: 15px;">
                    <div><span class="gold">👤 المالك:</span> {row.get('المالك', '-')}</div>
                    <div><span class="gold">💳 نظام السداد:</span> {row.get('السداد', '-')}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("🔄 جاري تحميل قاعدة بيانات المطورين... تأكد من استقرار الإنترنت.")
