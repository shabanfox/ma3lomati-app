import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الفاخرة
st.set_page_config(page_title="موسوعة المطورين العقاريين", layout="wide")

# رابط الشيت بتاعك (تم تحويله للقراءة المباشرة)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkp73VTBzZ25jYx5Zj-uqYpBgETbZj2Duivdjv8no8btvDQENS6T8OcaAPpSMgqJW0PeCQ-21vJm1V/pub?output=xlsx"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_excel(SHEET_URL)
    df.columns = df.columns.str.strip()
    return df

# 2. تصميم UI احترافي جداً (خلفية متدرجة + كروت زجاجية)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at top right, #001e3c, #000814);
        font-family: 'Cairo', sans-serif;
        color: white;
    }

    /* تصميم الكارت الزجاجي */
    .dev-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        direction: rtl;
        transition: 0.3s;
    }
    .dev-card:hover {
        border-color: #c5a059; /* لون ذهبي */
        background: rgba(255, 255, 255, 0.08);
    }

    .owner-tag { color: #c5a059; font-weight: bold; font-size: 0.9em; }
    .project-title { font-size: 1.8em; font-weight: 700; color: #ffffff; margin-bottom: 5px; }
    .price-box { background: #c5a059; color: #000; padding: 5px 15px; border-radius: 10px; font-weight: bold; font-size: 1.2em; }
    .history-box { background: rgba(0,0,0,0.3); padding: 10px; border-radius: 10px; border-right: 4px solid #c5a059; margin-top: 15px; }
    
    /* تعديل الفلاتر لتناسب التصميم الداكن */
    .stTextInput input, .stSelectbox div {
        background-color: rgba(255,255,255,0.05) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    label { color: #c5a059 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

try:
    df = load_data()
    
    st.markdown("<h1 style='text-align: center; color: #c5a059;'>🏙️ دليل المطورين العقاريين في مصر</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #aaa;'>داتا محدثة تشمل الملاك وسابقة الأعمال والأسعار</p>", unsafe_allow_html=True)

    # 3. الفلاتر الاحترافية
    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1:
            search = st.text_input("🔍 ابحث عن (شركة، مالك، أو مشروع)")
        with c2:
            region = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df['المنطقة'].unique().tolist()))
        with c3:
            unit = st.selectbox("🏠 نوع الوحدة", ["الكل"] + sorted(df['نوع الوحدة'].unique().tolist()))

    # تصفية البيانات
    f_df = df.copy()
    if search:
        f_df = f_df[f_df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if region != "الكل":
        f_df = f_df[f_df['المنطقة'] == region]
    if unit != "الكل":
        f_df = f_df[f_df['نوع الوحدة'] == unit]

    st.write(f"---")
    st.write(f"📊 تم العثور على: {len(f_df)} مشروع")

    # 4. عرض النتائج (The Premium Cards)
    for _, row in f_df.iterrows():
        st.markdown(f"""
            <div class="dev-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <span class="owner-tag">رئيس مجلس الإدارة: {row.get('المالك / رئيس مجلس الإدارة', 'غير مدرج')}</span>
                        <div class="project-title">{row.get('اسم المشروع', '-')}</div>
                        <div style="color: #38bdf8; font-weight: bold;">🏢 شركة {row.get('المطور', '-')} | 📍 {row.get('المنطقة', '-')}</div>
                    </div>
                    <div class="price-box">{row.get('السعر التقريبي (يبدأ من)', '-')}</div>
                </div>
                
                <div class="history-box">
                    <small style="color: #aaa;">📜 سابقة أعمال الشركة:</small><br>
                    {row.get('سابقة الأعمال (أهم المشاريع)', '-')}
                </div>

                <div style="display: flex; gap: 40px; margin-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 15px;">
                    <div><small style="color:#aaa">نوع الوحدة</small><br><b>{row.get('نوع الوحدة', '-')}</b></div>
                    <div><small style="color:#aaa">نظام السداد</small><br><b>{row.get('نظام السداد', '-')}</b></div>
                    <div><small style="color:#aaa">المشروع الحالي</small><br><b>{row.get('المشروع الحالي', '-')}</b></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"تأكد من مطابقة أسماء الأعمدة في الشيت للأسامي في الكود. الخطأ: {e}")
