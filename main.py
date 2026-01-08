import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="Egypt Real Estate Master", layout="wide")

# الرابط بصيغة CSV لضمان الاستقرار
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKo71CsiseSakziKDXBVahPV_TJ_JwbTqcJ3832U7kzAHrjM-l4jV1s6rcJPOwRV2mG9WxO8Hhlfex/pub?output=csv"

@st.cache_data(ttl=5)
def load_data():
    try:
        response = requests.get(CSV_URL)
        response.encoding = 'utf-8'
        df = pd.read_csv(StringIO(response.text))
        # تحويل كل أسماء الأعمدة لنصوص ومسح المسافات
        df.columns = [str(c).strip() for c in df.columns]
        # تحويل كل الداتا لنصوص عشان مفيش نوع داتا يضرب مع التاني
        df = df.astype(str).replace('nan', '')
        return df
    except Exception as e:
        st.error(f"خطأ في التحميل: {e}")
        return pd.DataFrame()

# 2. تصميم ملكي (Premium Dark Gold)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .stApp { background-color: #0a0a0a; font-family: 'Cairo', sans-serif; color: white; }
    
    .dev-card {
        background: #151515;
        border-radius: 15px;
        padding: 25px;
        border-right: 6px solid #d4af37;
        margin-bottom: 20px;
        direction: rtl;
        text-align: right;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    .gold-title { color: #d4af37; font-weight: 900; }
    .price-badge { background: #d4af37; color: black; padding: 5px 15px; border-radius: 5px; font-weight: bold; float: left; }
    
    /* تصميم الفلاتر */
    .stTextInput input, .stSelectbox div {
        background-color: #222 !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    </style>
    """, unsafe_allow_html=True)

df = load_data()

if not df.empty:
    st.markdown("<h1 style='text-align:center;' class='gold-title'>🏢 رادار المطورين العقاريين</h1>", unsafe_allow_html=True)
    
    # 3. Sidebar (مع معالجة الأخطاء يدوياً)
    with st.sidebar:
        st.header("لوحة التحكم")
        search = st.text_input("🔍 بحث عام...")
        
        # اختيار المنطقة بأمان
        if 'المنطقة' in df.columns:
            # تحويل لنصوص، مسح الفراغات، ثم الترتيب
            regions = sorted(list(set([str(x) for x in df['المنطقة'] if x.strip() != ""])))
            sel_region = st.selectbox("📍 المنطقة", ["الكل"] + regions)
        else:
            sel_region = "الكل"

    # تصفية
    f_df = df.copy()
    if search:
        f_df = f_df[f_df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if sel_region != "الكل":
        f_df = f_df[f_df['المنطقة'] == sel_region]

    # 4. العرض
    st.write(f"متاح حالياً: {len(f_df)} مطور ومشروع")
    
    for _, row in f_df.iterrows():
        st.markdown(f"""
            <div class="dev-card">
                <div class="price-badge">{row.get('السعر التقريبي (يبدأ من)', 'اتصل')}</div>
                <div class="gold-title" style="font-size: 0.9em;">DEVELOPER: {row.get('المطور', '-')}</div>
                <h2 style="margin: 10px 0;">{row.get('اسم المشروع', 'مشروع غير مسمى')}</h2>
                <p style="color: #888;">📍 {row.get('المنطقة', '-')}</p>
                
                <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <b class="gold-title">📜 سابقة الأعمال:</b><br>
                    {row.get('سابقة الأعمال (أهم المشاريع)', 'لا توجد بيانات')}
                </div>
                
                <div style="display: flex; gap: 30px; font-size: 0.9em;">
                    <div><span class="gold-title">👤 المالك:</span> {row.get('المالك / رئيس مجلس الإدارة', '-')}</div>
                    <div><span class="gold-title">💳 السداد:</span> {row.get('نظام السداد', '-')}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("جاري تحميل البيانات...")
