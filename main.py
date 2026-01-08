import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="رادار العقارات المحترف", layout="wide")

# الرابط الخاص بك
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRkp73VTBzZ25jYx5Zj-uqYpBgETbZj2Duivdjv8no8btvDQENS6T8OcaAPpSMgqJW0PeCQ-21vJm1V/pub?output=xlsx"

@st.cache_data(ttl=10)
def load_data():
    try:
        df = pd.read_excel(SHEET_URL)
        df.columns = [str(c).strip() for c in df.columns]
        # معالجة شاملة لكل القيم الفارغة في كل الأعمدة
        df = df.fillna("غير محدد")
        return df
    except Exception as e:
        st.error(f"خطأ في الاتصال: {e}")
        return pd.DataFrame()

# 2. التنسيق البصري (Deep Premium Dark)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    .stApp { background: radial-gradient(circle at top right, #0f172a, #020617); font-family: 'Cairo', sans-serif; color: white; }
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        direction: rtl; text-align: right;
    }
    .price-badge { background: linear-gradient(90deg, #38bdf8, #2563eb); color: white; padding: 6px 15px; border-radius: 12px; font-weight: bold; }
    h1, h2, h3, p, span, label, div { color: white !important; }
    .stTextInput input, .stSelectbox div { background-color: rgba(255,255,255,0.05) !important; color: white !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

df = load_data()

if not df.empty:
    st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🏙️ موسوعة المطورين العقاريين</h1>", unsafe_allow_html=True)
    
    # 3.Sidebar Filters (تم تأمينها تماماً من الـ TypeError)
    with st.sidebar:
        st.header("تصفية البحث")
        general_search = st.text_input("🔍 بحث بالاسم أو المالك...")
        
        # تأمين فلتر المنطقة
        if 'المنطقة' in df.columns:
            # تحويل كل القيم لنصوص -> مسح الـ "غير محدد" -> الترتيب
            raw_regions = df['المنطقة'].astype(str).unique().tolist()
            clean_regions = sorted([r for r in raw_regions if r != "غير محدد"])
            sel_region = st.selectbox("📍 المنطقة", ["الكل"] + clean_regions)
        else:
            sel_region = "الكل"

        # تأمين فلتر نوع الوحدة
        if 'نوع الوحدة' in df.columns:
            raw_units = df['نوع الوحدة'].astype(str).unique().tolist()
            clean_units = sorted([u for u in raw_units if u != "غير محدد"])
            sel_unit = st.selectbox("🏠 نوع الوحدة", ["الكل"] + clean_units)
        else:
            sel_unit = "الكل"

    # تطبيق الفلترة
    f_df = df.copy()
    if general_search:
        f_df = f_df[f_df.apply(lambda r: general_search.lower() in str(r).lower(), axis=1)]
    if sel_region != "الكل":
        f_df = f_df[f_df['المنطقة'] == sel_region]
    if sel_unit != "الكل":
        f_df = f_df[f_df['نوع الوحدة'] == sel_unit]

    # 4. عرض النتائج
    st.write(f"المشاريع المتاحة: {len(f_df)}")
    
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
                <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; margin: 20px 0;">
                    <small style="color: #38bdf8; font-weight: bold;">📜 سابقة الأعمال والخبرة:</small><br>
                    <span style="font-size: 0.95em; line-height: 1.6;">{row.get('سابقة الأعمال (أهم المشاريع)', 'لا توجد بيانات متاحة')}</span>
                </div>
                <div style="display: flex; gap: 30px; font-size: 0.9em; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 15px;">
                    <div><span style="color:#94a3b8;">👤 المالك:</span> {row.get('المالك / رئيس مجلس الإدارة', '-')}</div>
                    <div><span style="color:#94a3b8;">💳 السداد:</span> {row.get('نظام السداد', '-')}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("⚠️ لم يتم العثور على بيانات. تأكد من أن ملف الإكسيل يحتوي على البيانات المطلوبة.")
