import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="Egypt Real Estate Encyclopedia", layout="wide")

# تحويل رابط الشيت لنسخة CSV لضمان استقرار الداتا 100%
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKo71CsiseSakziKDXBVahPV_TJ_JwbTqcJ3832U7kzAHrjM-l4jV1s6rcJPOwRV2mG9WxO8Hhlfex/pub?output=csv"

@st.cache_data(ttl=10)
def load_data():
    try:
        response = requests.get(CSV_URL)
        response.encoding = 'utf-8'
        df = pd.read_csv(StringIO(response.text))
        # تنظيف أسامي الأعمدة أوتوماتيكياً
        df.columns = [str(c).strip() for c in df.columns]
        # تحويل كل خلية لنص ومسح أي قيم غريبة
        df = df.applymap(lambda x: str(x).strip() if pd.notnull(x) and str(x).lower() != 'nan' else "غير مدرج")
        return df
    except Exception as e:
        st.error(f"عذراً، واجهنا مشكلة في جلب البيانات: {e}")
        return pd.DataFrame()

# 2. تصميم الواجهة (Luxury Deep UI)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(#1a1a1a 1px, transparent 1px);
        background-size: 30px 30px;
        font-family: 'Cairo', sans-serif;
        color: white;
    }

    .developer-card {
        background: linear-gradient(145deg, #111, #080808);
        border: 1px solid #222;
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        direction: rtl;
        transition: 0.4s;
        box-shadow: 10px 10px 20px #020202, -10px -10px 20px #0a0a0a;
    }
    
    .developer-card:hover {
        border-color: #D4AF37;
        transform: translateY(-5px);
    }

    .gold-text { color: #D4AF37 !important; font-weight: 900; }
    .project-title { font-size: 2.2rem; font-weight: 900; color: #fff; margin-bottom: 10px; }
    .badge { background: #D4AF37; color: #000; padding: 5px 15px; border-radius: 8px; font-weight: bold; }
    
    .history-box {
        background: rgba(212, 175, 55, 0.05);
        border-right: 4px solid #D4AF37;
        padding: 15px;
        margin: 20px 0;
        border-radius: 5px 15px 15px 5px;
    }
    
    /* استايل السايد بار والمدخلات */
    [data-testid="stSidebar"] { background-color: #000 !important; border-left: 1px solid #222; }
    .stTextInput input { background-color: #111 !important; color: white !important; border: 1px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

df = load_data()

if not df.empty:
    st.markdown("<h1 style='text-align:center; font-size: 45px;' class='gold-text'>REAL ESTATE MASTER RADAR</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity: 0.6;'>الإصدار الاحترافي الكامل | 100 مطور عقاري</p>", unsafe_allow_html=True)
    st.write("---")

    # 3. الفلاتر (بدون أخطاء البرمجة السابقة)
    with st.sidebar:
        st.markdown("<h2 class='gold-text'>الفلاتر الذكية</h2>", unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث عن المطور أو المالك أو المنطقة")
        
        # استخراج القوائم بشكل آمن
        regions = ["الكل"] + sorted([r for r in df['المنطقة'].unique() if r != "غير مدرج"]) if 'المنطقة' in df.columns else ["الكل"]
        sel_region = st.selectbox("📍 اختر المنطقة", regions)

    # تطبيق التصفية
    filtered = df.copy()
    if search:
        filtered = filtered[filtered.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if sel_region != "الكل":
        filtered = filtered[filtered['المنطقة'] == sel_region]

    # 4. العرض الملكي للبيانات
    st.write(f"عدد النتائج: {len(filtered)}")

    for _, row in filtered.iterrows():
        st.markdown(f"""
            <div class="developer-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="text-align: right;">
                        <span class="gold-text">DEVELOPER PROFILE</span>
                        <h1 class="project-title">{row.get('اسم المشروع', 'بدون اسم')}</h1>
                        <p style="font-size: 1.2rem; color: #aaa;">🏢 شركة {row.get('المطور', 'غير مدرج')} | 📍 {row.get('المنطقة', '-')}</p>
                    </div>
                    <div class="badge" style="font-size: 1.4rem;">{row.get('السعر التقريبي (يبدأ من)', 'اتصل')}</div>
                </div>

                <div class="history-box">
                    <div class="gold-text" style="margin-bottom: 8px;">📜 سابقة أعمال المطور والمالك:</div>
                    <div style="line-height: 1.8; color: #eee;">{row.get('سابقة الأعمال (أهم المشاريع)', 'لا توجد بيانات')}</div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-top: 20px; opacity: 0.9;">
                    <div><small class="gold-text">رئيس مجلس الإدارة</small><br><b>{row.get('المالك / رئيس مجلس الإدارة', '-')}</b></div>
                    <div><small class="gold-text">المشروع الحالي</small><br><b>{row.get('المشروع الحالي', '-')}</b></div>
                    <div><small class="gold-text">نظام السداد</small><br><b>{row.get('نظام السداد', '-')}</b></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("⚠️ جاري جلب البيانات من السحابة... تأكد من أن ملف جوجل شيت 'منشور للويب'.")
