import streamlit as st
import pandas as pd

# 1. إعدادات المنصة الاحترافية
st.set_page_config(page_title="موسوعة العقارات المصرية", layout="wide", page_icon="🏢")

# رابط الشيت الجديد الخاص بك
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKo71CsiseSakziKDXBVahPV_TJ_JwbTqcJ3832U7kzAHrjM-l4jV1s6rcJPOwRV2mG9WxO8Hhlfex/pub?output=xlsx"

@st.cache_data(ttl=10)
def load_data():
    try:
        df = pd.read_excel(SHEET_URL)
        df.columns = [str(c).strip() for c in df.columns]
        # تنظيف الداتا وتأمينها ضد أي قيم غريبة
        df = df.astype(str).replace(['nan', 'None', 'nan '], 'غير محدد')
        return df
    except Exception as e:
        st.error(f"فشل الاتصال بقاعدة البيانات: {e}")
        return pd.DataFrame()

# 2. هندسة الشكل العام (Premium CSS Design)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, #001524 0%, #000c14 90%);
        font-family: 'Cairo', sans-serif;
    }

    /* كارت المطور المحترف */
    .pro-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 25px;
        direction: rtl;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .pro-card:hover {
        transform: translateY(-10px);
        border-color: #D4AF37;
        box-shadow: 0 15px 40px rgba(0,0,0,0.4);
    }

    /* العناوين والألوان */
    .dev-label { color: #D4AF37; font-weight: 800; font-size: 0.9em; letter-spacing: 1px; margin-bottom: 5px; }
    .project-name { color: #ffffff; font-size: 2em; font-weight: 800; margin: 0; }
    .region-tag { background: rgba(212, 175, 55, 0.15); color: #D4AF37; padding: 4px 15px; border-radius: 50px; font-size: 0.8em; font-weight: 600; }
    .price-tag { 
        background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%); 
        color: #000; padding: 10px 25px; border-radius: 15px; 
        font-weight: 900; font-size: 1.3em; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
    }
    
    /* صندوق سابقة الأعمال */
    .history-section {
        background: rgba(0, 0, 0, 0.2);
        border-radius: 15px;
        padding: 15px;
        margin-top: 20px;
        border-right: 5px solid #D4AF37;
    }

    /* تخصيص السايد بار */
    [data-testid="stSidebar"] { background-color: #000c14 !important; border-right: 1px solid rgba(212, 175, 55, 0.2); }
    h1, h2, h3, p, span, label { color: white !important; }
    
    /* تعديل المدخلات */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        color: white !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

df = load_data()

if not df.empty:
    # --- الهيدر الاحترافي ---
    st.markdown("<h1 style='text-align: center; color: #D4AF37; font-weight: 800; font-size: 3.5em;'>EGYPT REAL ESTATE RADAR</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em; opacity: 0.8;'>المنصة الأذكى لتحليل المطورين والمشاريع العقارية</p>", unsafe_allow_html=True)
    st.write("---")

    # --- القائمة الجانبية المحدثة ---
    with st.sidebar:
        st.markdown("<h2 style='color:#D4AF37'>🧭 لوحة التحكم</h2>", unsafe_allow_html=True)
        search = st.text_input("🔍 بحث ذكي (مطور، مالك، مشروع)")
        
        if 'المنطقة' in df.columns:
            region_list = sorted([r for r in df['المنطقة'].unique() if r != 'غير محدد'])
            sel_region = st.selectbox("📍 فلتر المنطقة", ["الكل"] + region_list)
        else: sel_region = "الكل"

        if 'نوع الوحدة' in df.columns:
            unit_list = sorted([u for u in df['نوع الوحدة'].unique() if u != 'غير محدد'])
            sel_unit = st.selectbox("🏠 نوع الوحدة", ["الكل"] + unit_list)
        else: sel_unit = "الكل"

    # --- منطق الفلترة ---
    f_df = df.copy()
    if search:
        f_df = f_df[f_df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if sel_region != "الكل":
        f_df = f_df[f_df['المنطقة'] == sel_region]
    if sel_unit != "الكل":
        f_df = f_df[f_df['نوع الوحدة'] == sel_unit]

    # --- عرض المحتوى ---
    c1, c2 = st.columns([4, 1])
    with c1: st.write(f"✅ تم العثور على **{len(f_df)}** نتيجة بحث")
    
    for _, row in f_df.iterrows():
        st.markdown(f"""
            <div class="pro-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="text-align: right;">
                        <div class="dev-label">DEVELOPER: {row.get('المطور', 'غير متوفر')}</div>
                        <h2 class="project-name">{row.get('اسم المشروع', 'بدون اسم')}</h2>
                        <div style="margin-top: 10px;">
                            <span class="region-tag">📍 {row.get('المنطقة', '-')}</span>
                            <span style="margin-right: 10px; opacity: 0.7;">👤 المالك: {row.get('المالك / رئيس مجلس الإدارة', '-')}</span>
                        </div>
                    </div>
                    <div style="text-align: left;">
                        <div class="price-tag">{row.get('السعر التقريبي (يبدأ من)', 'اتصل')}</div>
                    </div>
                </div>
                
                <div class="history-section">
                    <div style="color: #D4AF37; font-weight: bold; font-size: 0.9em; margin-bottom: 5px;">📜 سابقة الأعمال والخبرة العقارية:</div>
                    <div style="line-height: 1.6; font-size: 1.05em; color: #e0e0e0;">{row.get('سابقة الأعمال (أهم المشاريع)', 'لم يتم إدراج بيانات سابقة الأعمال')}</div>
                </div>

                <div style="display: flex; gap: 40px; margin-top: 25px; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 20px;">
                    <div>
                        <small style="color: #D4AF37;">🏠 نوع الوحدات</small><br>
                        <span style="font-weight: 600;">{row.get('نوع الوحدة', '-')}</span>
                    </div>
                    <div>
                        <small style="color: #D4AF37;">💳 نظام السداد</small><br>
                        <span style="font-weight: 600;">{row.get('نظام السداد', '-')}</span>
                    </div>
                    <div>
                        <small style="color: #D4AF37;">🏗️ المشروع الحالي</small><br>
                        <span style="font-weight: 600;">{row.get('المشروع الحالي', '-')}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("🔄 جاري تحميل قاعدة بيانات المطورين... تأكد من نشر الشيت بصيغة XLSX.")
