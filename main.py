import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="Real Estate Elite", layout="wide")

# الرابط بصيغة CSV لضمان أعلى استقرار
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKo71CsiseSakziKDXBVahPV_TJ_JwbTqcJ3832U7kzAHrjM-l4jV1s6rcJPOwRV2mG9WxO8Hhlfex/pub?output=csv"

@st.cache_data(ttl=5)
def load_data():
    try:
        # محاولة جلب البيانات مع تحديد الترميز العربي
        response = requests.get(CSV_URL, timeout=10)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            df = pd.read_csv(StringIO(response.text))
            # تنظيف وتأمين الداتا تماماً
            df.columns = [str(c).strip() for c in df.columns]
            df = df.astype(str).replace(['nan', 'NaN', 'None'], 'غير محدد')
            return df
        else:
            return pd.DataFrame()
    except:
        return pd.DataFrame()

# 2. لغة التصميم (Modern Luxury UI)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .stApp { background-color: #050505; font-family: 'Cairo', sans-serif; }
    
    /* الكروت الاحترافية */
    .premium-card {
        background: linear-gradient(145deg, #121212, #1a1a1a);
        border: 1px solid #222;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        direction: rtl;
        text-align: right;
        transition: 0.3s;
    }
    .premium-card:hover { border-color: #fbbf24; transform: scale(1.01); }
    
    .gold-glow { color: #fbbf24; text-shadow: 0 0 10px rgba(251, 191, 36, 0.3); font-weight: 900; }
    .price-tag { background: #fbbf24; color: #000; padding: 5px 15px; border-radius: 10px; font-weight: 800; font-size: 1.2rem; }
    
    /* تعديل الفلاتر */
    .stTextInput input, .stSelectbox div { background-color: #111 !important; color: white !important; border: 1px solid #333 !important; }
    h1, h2, h3, p, span, label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. محرك جلب البيانات
df = load_data()

# لو الشيت فاضي أو فيه مشكلة، هنعرض رسالة تنبيه واضحة
if df.empty:
    st.error("⚠️ فشل في سحب البيانات من Google Sheets. تأكد أن الشيت 'Public' ومنشور بصيغة CSV.")
    st.info("سأعرض لك نموذجاً تجريبياً للشكل الاحترافي حالياً:")
    # داتا تجريبية عشان الموقع ميبقاش "أبيض" لو فيه عطل في الربط
    df = pd.DataFrame({
        'المطور': ['إعمار مصر', 'ماونتن فيو'],
        'اسم المشروع': ['ميفيدا', 'آي سيتي'],
        'المنطقة': ['التجمع الخامس', 'القاهرة الجديدة'],
        'السعر التقريبي (يبدأ من)': ['15,000,000', '9,000,000'],
        'سابقة الأعمال (أهم المشاريع)': ['مراسي، أب تاون', 'ماونتن فيو 1، 2']
    })

# --- واجهة العرض الرئيسية ---
st.markdown("<h1 style='text-align:center;' class='gold-glow'>EGYPT REAL ESTATE ENCYCLOPEDIA</h1>", unsafe_allow_html=True)

# السايد بار الآمن
with st.sidebar:
    st.markdown("<h2 class='gold-glow'>البحث المتقدم</h2>", unsafe_allow_html=True)
    search = st.text_input("🎯 ابحث عن مطور، مشروع، أو مالك")
    
    # اختيار المنطقة بفلتر آمن جداً
    if 'المنطقة' in df.columns:
        region_list = sorted(list(set([str(x) for x in df['المنطقة'] if str(x).strip() != ""])))
        sel_region = st.selectbox("📍 فلتر المناطق", ["الكل"] + region_list)
    else:
        sel_region = "الكل"

# منطق الفلترة
f_df = df.copy()
if search:
    f_df = f_df[f_df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
if sel_region != "الكل":
    f_df = f_df[f_df['المنطقة'] == sel_region]

# العرض
st.write(f"📊 النتائج المتاحة: {len(f_df)}")

for _, row in f_df.iterrows():
    st.markdown(f"""
        <div class="premium-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <div class="price-tag">{row.get('السعر التقريبي (يبدأ من)', 'اتصل')}</div>
                <div style="text-align: right;">
                    <small class="gold-glow">مطور عقاري محترف</small>
                    <h2 style="margin: 0;">{row.get('اسم المشروع', 'مشروع جديد')}</h2>
                    <p style="color: #888; margin: 0;">🏢 {row.get('المطور', 'شركة غير مدرجة')} | 📍 {row.get('المنطقة', '-')}</p>
                </div>
            </div>
            
            <div style="background: rgba(251, 191, 36, 0.05); padding: 15px; border-radius: 12px; border-right: 4px solid #fbbf24;">
                <b class="gold-glow">📜 سابقة الأعمال والخبرة:</b><br>
                <span style="font-size: 0.95em;">{row.get('سابقة الأعمال (أهم المشاريع)', 'لا توجد بيانات')}</span>
            </div>
            
            <div style="display: flex; gap: 30px; margin-top: 20px; font-size: 0.85em; opacity: 0.7;">
                <div>👤 المالك: {row.get('المالك / رئيس مجلس الإدارة', '-')}</div>
                <div>💳 السداد: {row.get('نظام السداد', '-')}</div>
                <div>🏘️ الموقف: {row.get('المشروع الحالي', '-')}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
