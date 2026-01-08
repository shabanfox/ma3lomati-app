import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="موسوعة العقارات المحترفة", layout="wide")

# رابط الشيت بتاعك - تأكد من استخدام صيغة pub?output=xlsx في الكود
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkp73VTBzZ25jYx5Zj-uqYpBgETbZj2Duivdjv8no8btvDQENS6T8OcaAPpSMgqJW0PeCQ-21vJm1V/pub?output=xlsx"

@st.cache_data(ttl=30) # تحديث كل 30 ثانية
def load_data():
    try:
        df = pd.read_excel(SHEET_URL)
        # تنظيف أسامي الأعمدة من المسافات الزائدة
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"فشل في الاتصال بجوجل شيت: {e}")
        return pd.DataFrame()

# 2. التصميم (Modern Dark Glass)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    .stApp { background: #0f172a; font-family: 'Cairo', sans-serif; color: white; }
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 15px;
        direction: rtl;
    }
    .price-tag { background: #38bdf8; color: white; padding: 4px 12px; border-radius: 8px; font-weight: bold; }
    .owner-info { color: #94a3b8; font-size: 0.85em; }
    h1, h2, h3, p, span, label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

df = load_data()

if not df.empty:
    st.markdown("<h1 style='text-align: center;'>🏙️ رادار المطورين العقاريين</h1>", unsafe_allow_html=True)
    
    # 3. الفلاتر الذكية (مع التأكد من وجود الأعمدة)
    with st.sidebar:
        st.title("البحث الذكي")
        search = st.text_input("🔍 بحث عام...")
        
        # التأكد من وجود الأعمدة قبل عمل الفلتر
        cols = df.columns.tolist()
        
        region_opt = ["الكل"] + sorted(df['المنطقة'].unique().tolist()) if 'المنطقة' in cols else ["الكل"]
        sel_region = st.selectbox("المنطقة", region_opt)
        
        unit_opt = ["الكل"] + sorted(df['نوع الوحدة'].unique().tolist()) if 'نوع الوحدة' in cols else ["الكل"]
        sel_unit = st.selectbox("نوع الوحدة", unit_opt)

    # تطبيق الفلترة
    f_df = df.copy()
    if search:
        f_df = f_df[f_df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if 'المنطقة' in cols and sel_region != "الكل":
        f_df = f_df[f_df['المنطقة'] == sel_region]
    if 'نوع الوحدة' in cols and sel_unit != "الكل":
        f_df = f_df[f_df['نوع الوحدة'] == sel_unit]

    # 4. عرض النتائج
    st.write(f"عدد المشاريع المكتشفة: {len(f_df)}")
    
    for _, row in f_df.iterrows():
        with st.container():
            st.markdown(f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <span class="owner-info">المطور: {row.get('المطور', 'غير متوفر')}</span>
                            <h2 style="margin:5px 0;">{row.get('اسم المشروع', 'بدون اسم')}</h2>
                            <p style="color:#38bdf8;">📍 {row.get('المنطقة', '-')}</p>
                        </div>
                        <div>
                            <span class="price-tag">{row.get('السعر التقريبي (يبدأ من)', 'اتصل للسعر')}</span>
                        </div>
                    </div>
                    <div style="background: rgba(0,0,0,0.2); padding: 10px; border-radius: 8px; margin-top: 10px;">
                        <small><b>سابقة الأعمال:</b></small><br>
                        <span style="font-size: 0.9em;">{row.get('سابقة الأعمال (أهم المشاريع)', '-')}</span>
                    </div>
                    <div style="margin-top: 15px; font-size: 0.85em; display: grid; grid-template-columns: 1fr 1fr;">
                        <div>👤 المالك: {row.get('المالك / رئيس مجلس الإدارة', '-')}</div>
                        <div>💳 السداد: {row.get('نظام السداد', '-')}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.warning("لم يتم تحميل بيانات. تأكد من أن الشيت يحتوي على داتا صحيحة.")
