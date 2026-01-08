import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="Professional Real Estate Radar", layout="wide")

# الرابط الخاص بك
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkp73VTBzZ25jYx5Zj-uqYpBgETbZj2Duivdjv8no8btvDQENS6T8OcaAPpSMgqJW0PeCQ-21vJm1V/pub?output=xlsx"

@st.cache_data(ttl=10)
def load_data():
    try:
        df = pd.read_excel(SHEET_URL)
        # تنظيف أسامي الأعمدة من أي مسافات
        df.columns = [str(c).strip() for c in df.columns]
        # تحويل كل الجدول لنصوص لتجنب تضارب الأنواع (نصوص ضد أرقام)
        df = df.astype(str).replace('nan', 'غير محدد')
        return df
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")
        return pd.DataFrame()

# 2. تصميم UI احترافي (Modern Dark Glass)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    .stApp { background: radial-gradient(circle at top right, #0f172a, #020617); font-family: 'Cairo', sans-serif; }
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        direction: rtl; text-align: right;
        transition: 0.3s ease;
    }
    .glass-card:hover { border-color: #38bdf8; background: rgba(255, 255, 255, 0.05); }
    .price-badge { background: linear-gradient(90deg, #38bdf8, #2563eb); color: white; padding: 6px 15px; border-radius: 12px; font-weight: bold; }
    h1, h2, h3, p, span, label, div { color: white !important; }
    .stTextInput input, .stSelectbox div { background-color: rgba(255,255,255,0.05) !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

df = load_data()

if not df.empty:
    st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🏙️ موسوعة المطورين العقاريين</h1>", unsafe_allow_html=True)
    
    # 3. Sidebar (تم معالجة الـ TypeError هنا جذرياً)
    with st.sidebar:
        st.header("تصفية البحث")
        search_query = st.text_input("🔍 ابحث (مطور، مشروع، مالك)...")
        
        # معالجة عمود المنطقة
        if 'المنطقة' in df.columns:
            region_list = sorted([r for r in df['المنطقة'].unique() if r != 'غير محدد'])
            sel_region = st.selectbox("📍 المنطقة", ["الكل"] + region_list)
        else:
            sel_region = "الكل"

        # معالجة عمود نوع الوحدة
        if 'نوع الوحدة' in df.columns:
            unit_list = sorted([u for u in df['نوع الوحدة'].unique() if u != 'غير محدد'])
            sel_unit = st.selectbox("🏠 نوع الوحدة", ["الكل"] + unit_list)
        else:
            sel_unit = "الكل"

    # تطبيق الفلترة
    f_df = df.copy()
    if search_query:
        f_df = f_df[f_df.apply(lambda r: search_query.lower() in str(r).lower(), axis=1)]
    if sel_region != "الكل":
        f_df = f_df[f_df['المنطقة'] == sel_region]
    if sel_unit != "الكل":
        f_df = f_df[f_df['نوع الوحدة'] == sel_unit]

    st.write(f"📊 المشاريع المتاحة: {len(f_df)}")

    # 4. عرض النتائج
    for _, row in f_df.iterrows():
        st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <div style="color: #38bdf8; font-size: 0.9em; font-weight: bold;">🏢 {row.get('المطور', 'مطور غير مسجل')}</div>
                        <h2 style="margin: 5px 0;">{row.get('اسم المشروع', 'بدون اسم')}</h2>
                        <p style="color: #94a3b8; margin: 0;">📍 {row.get('المنطقة', 'غير محدد')}</p>
                    </div>
                    <div class="price-badge">{row.get('السعر التقريبي (يبدأ من)', 'اتصل')}</div>
                </div>
                <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; margin: 20px 0; border-right: 4px solid #38bdf8;">
                    <small style="color: #38bdf8; font-weight: bold;">📜 سابقة الأعمال والخبرة:</small><br>
                    <span style="font-size: 0.95em; line-height: 1.6;">{row.get('سابقة الأعمال (أهم المشاريع)', 'لا توجد بيانات')}</span>
                </div>
                <div style="display: flex; gap: 30px; font-size: 0.9em; opacity: 0.8; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 10px;">
                    <div><span style="color:#94a3b8;">👤 المالك:</span> {row.get('المالك / رئيس مجلس الإدارة', '-')}</div>
                    <div><span style="color:#94a3b8;">💳 السداد:</span> {row.get('نظام السداد', '-')}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("⚠️ تأكد من رفع ملف الإكسيل ومزامنة الرابط بشكل صحيح.")
