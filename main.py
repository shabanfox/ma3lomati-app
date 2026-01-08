import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات المنصة الاحترافية
st.set_page_config(page_title="موسوعة العقارات المصرية 480+", layout="wide")

# رابط الشيت بتاعك (تأكد إنه بصيغة CSV في النهاية)
# استبدل هذا الرابط برابط الشيت الجديد بعد ما تضيف فيه الـ 480 مطور
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKo71CsiseSakziKDXBVahPV_TJ_JwbTqcJ3832U7kzAHrjM-l4jV1s6rcJPOwRV2mG9WxO8Hhlfex/pub?output=csv"

@st.cache_data(ttl=60) # تحديث كل دقيقة
def load_big_data():
    try:
        response = requests.get(SHEET_URL)
        response.encoding = 'utf-8'
        df = pd.read_csv(StringIO(response.text))
        # تنظيف أسامي الأعمدة
        df.columns = [str(c).strip() for c in df.columns]
        # تحويل كل شيء لنص لمنع الـ Errors
        df = df.astype(str).replace(['nan', 'NaN', 'None'], 'غير مدرج')
        return df
    except Exception as e:
        return pd.DataFrame()

# 2. تصميم الواجهة (Premium Dark Design)
st.markdown("""
<style>
    .stApp { background-color: #0c0f14; font-family: 'Cairo', sans-serif; }
    .card-container {
        background: #1a1f26;
        border: 1px solid #c5a059;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        color: white;
        direction: rtl;
    }
    .gold-text { color: #c5a059; font-weight: bold; }
    .search-box { border-radius: 10px; border: 1px solid #c5a059; }
</style>
""", unsafe_allow_html=True)

# 3. تحميل البيانات
df = load_big_data()

if not df.empty:
    st.markdown("<h1 style='text-align: center; color: #c5a059;'>🏙️ رادار المطورين (480+ مطور)</h1>", unsafe_allow_html=True)
    
    # الفلاتر الذكية
    with st.sidebar:
        st.markdown("<h2 class='gold-text'>لوحة التحكم</h2>", unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث في الـ 480 مطور...")
        
        if 'المنطقة' in df.columns:
            region_list = ["الكل"] + sorted([r for r in df['المنطقة'].unique() if r != "غير مدرج"])
            sel_region = st.selectbox("📍 اختر المنطقة", region_list)
        else: sel_region = "الكل"

    # تطبيق الفلترة
    f_df = df.copy()
    if search:
        f_df = f_df[f_df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if sel_region != "الكل":
        f_df = f_df[f_df['المنطقة'] == sel_region]

    # عرض النتائج مع عداد
    st.markdown(f"<p style='text-align: right;'>تم العثور على: <span class='gold-text'>{len(f_df)}</span> مطور ومشروع</p>", unsafe_allow_html=True)
    st.divider()

    # استخدام نظام الـ "List" السريع للعرض
    for i, row in f_df.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="card-container">
                <div style="display: flex; justify-content: space-between;">
                    <span style="background:#c5a059; color:black; padding:2px 10px; border-radius:5px; font-weight:bold;">#{i+1}</span>
                    <span class="gold-text" style="font-size:1.2em;">{row.get('المطور', '-')}</span>
                </div>
                <h3 style="margin:10px 0;">{row.get('المشروع', 'مشروع غير مسمى')}</h3>
                <p>📍 <b>المنطقة:</b> {row.get('المنطقة', '-')}</p>
                <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px;">
                    <small class="gold-text">📜 سابقة الأعمال:</small><br>
                    {row.get('سابقة_الأعمال', 'لا توجد بيانات')}
                </div>
                <div style="margin-top:10px; display:flex; gap:20px; font-size:0.9em;">
                    <span>👤 <b>المالك:</b> {row.get('المالك', '-')}</span>
                    <span>💰 <b>السعر:</b> {row.get('السعر', '-')}</span>
                    <span>💳 <b>السداد:</b> {row.get('السداد', '-')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.warning("🔄 في انتظار البيانات... تأكد من ملء الإكسيل ونشره بصيغة CSV.")
