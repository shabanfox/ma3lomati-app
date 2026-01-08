import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="M A S T E R _ R A D A R", layout="wide")

# الرابط الذي يعمل كـ "محرك بيانات" وليس كـ "صفحة ويب"
RAW_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

@st.cache_data(ttl=5)
def get_clean_data():
    try:
        # جلب البيانات الخام
        response = requests.get(RAW_URL)
        response.encoding = 'utf-8'
        # قراءة الـ CSV وتجاهل أي أسطر فارغة أو أعمدة وهمية
        df = pd.read_csv(StringIO(response.text))
        
        # تنظيف الداتا: مسح المسافات من أسماء الأعمدة وتحويل القيم لنصوص
        df.columns = [str(c).strip() for c in df.columns]
        df = df.astype(str).replace(['nan', 'NaN', 'None', 'nan '], 'غير مدرج')
        return df
    except Exception as e:
        st.error(f"خطأ في جلب البيانات: {e}")
        return pd.DataFrame()

# 2. تصميم الواجهة (Premium Dark Design)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .stApp { background-color: #0d1117; font-family: 'Cairo', sans-serif; }
    
    /* تنسيق الكروت الاحترافي */
    .master-card {
        background: linear-gradient(145deg, #1c2128, #111418);
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        direction: rtl;
        text-align: right;
        transition: 0.3s ease;
    }
    .master-card:hover { border-color: #d4af37; box-shadow: 0 4px 20px rgba(212, 175, 55, 0.1); }
    
    .gold { color: #d4af37 !important; font-weight: 900; }
    .price-tag { background: #d4af37; color: black; padding: 4px 12px; border-radius: 6px; font-weight: 800; float: left; }
    
    .history-section {
        background: rgba(255,255,255,0.03);
        border-right: 4px solid #d4af37;
        padding: 12px;
        margin: 15px 0;
        border-radius: 4px 12px 12px 4px;
        font-size: 0.95em;
        line-height: 1.6;
    }
    
    /* إلغاء الروابط والخطوط الزائدة */
    a { text-decoration: none !important; }
    h1, h2, h3, p, span { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

df = get_clean_data()

if not df.empty:
    st.markdown("<h1 style='text-align:center;' class='gold'>🏙️ M A S T E R _ R A D A R</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:0.6;'>الإصدار الاحترافي الكامل - قاعدة بيانات المطورين</p>", unsafe_allow_html=True)
    st.write("---")

    # لوحة التحكم الجانبية
    with st.sidebar:
        st.markdown("<h2 class='gold'>البحث الذكي</h2>", unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث (اسم الشركة، المشروع، المالك)")
        
        # فلتر المنطقة (يتعرف على العمود تلقائياً)
        region_col = next((c for c in df.columns if 'المنطقة' in c), None)
        if region_col:
            unique_regions = ["الكل"] + sorted([r for r in df[region_col].unique() if r != "غير مدرج"])
            sel_region = st.selectbox("📍 اختر المنطقة", unique_regions)
        else:
            sel_region = "الكل"

    # تصفية البيانات
    f_df = df.copy()
    if search:
        f_df = f_df[f_df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if sel_region != "الكل":
        f_df = f_df[f_df[region_col] == sel_region]

    # عرض النتائج
    st.write(f"النتائج المتاحة: **{len(f_df)}**")

    for _, row in f_df.iterrows():
        # تعريف المتغيرات بمرونة (حتى لو تغيرت أسماء الأعمدة في الإكسيل)
        m_dev = row.get('المطور', row.get('مطور', '-'))
        m_proj = row.get('المشروع', row.get('اسم المشروع', '-'))
        m_owner = row.get('المالك', row.get('المالك / رئيس مجلس الإدارة', '-'))
        m_history = row.get('سابقة_الأعمال', row.get('سابقة الأعمال (أهم المشاريع)', 'غير متوفر'))
        m_price = row.get('السعر', row.get('السعر التقريبي (يبدأ من)', 'اتصل للاستعلام'))
        m_region = row.get('المنطقة', '-')
        m_pay = row.get('السداد', row.get('نظام السداد', '-'))

        st.markdown(f"""
            <div class="master-card">
                <div class="price-tag">{m_price}</div>
                <div class="gold" style="font-size: 0.8em; letter-spacing: 1px;">OFFICIAL DEVELOPER</div>
                <h2 style="margin: 5px 0; color: white;">{m_proj}</h2>
                <div style="margin-bottom: 10px;">
                    <span style="color: #d4af37;">🏢 {m_dev}</span> | <span>📍 {m_region}</span>
                </div>
                
                <div class="history-section">
                    <b class="gold">📜 الخبرة وسابقة الأعمال:</b><br>
                    {m_history}
                </div>
                
                <div style="display: flex; gap: 30px; font-size: 0.9em; opacity: 0.8; border-top: 1px solid #30363d; padding-top: 15px;">
                    <div><span class="gold">👤 المالك:</span> {m_owner}</div>
                    <div><span class="gold">💳 نظام السداد:</span> {m_pay}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("🔄 جاري مزامنة البيانات من السحابة... يرجى الانتظار.")
