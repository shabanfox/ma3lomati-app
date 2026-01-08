import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعداد الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# 2. روابط البيانات
PROJECTS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

# 3. التنسيق (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    #MainMenu, header, footer, .stDeployButton {visibility: hidden;}
    html { direction: ltr !important; }
    body, [data-testid="stAppViewContainer"] {
        direction: rtl !important;
        font-family: 'Cairo', sans-serif;
        background-color: #0d1117; color: white;
    }
    ::-webkit-scrollbar { width: 18px !important; }
    ::-webkit-scrollbar-track { background: #0d1117 !important; }
    ::-webkit-scrollbar-thumb { background: #d4af37 !important; border-radius: 10px; }
    
    .hero-section {
        position: relative; height: 160px; border-radius: 20px; margin-bottom: 30px;
        display: flex; align-items: center; justify-content: center; overflow: hidden;
        border: 1px solid rgba(212,175,55,0.3);
    }
    .hero-bg {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-image: url('https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1600&q=80');
        background-size: cover; z-index: 1; filter: brightness(0.3);
    }
    .main-title { color: #d4af37; font-size: 2.5em; font-weight: 900; z-index: 3; position: relative; }
    
    .project-card {
        background: #1c2128; border: 1px solid #30363d;
        border-radius: 15px; padding: 25px; margin-bottom: 20px; text-align: right;
    }
    .price-badge { background: #d4af37; color: #000; padding: 5px 15px; border-radius: 8px; font-weight: 900; float: left; }
    
    /* تحسين شكل الليبل (العناوين فوق الخانات) */
    label { color: #d4af37 !important; font-size: 1.1em !important; font-weight: bold !important; }
    </style>
    
    <div class="hero-section">
        <div class="hero-bg"></div>
        <h1 class="main-title">منصة معلوماتي العقارية</h1>
    </div>
    """, unsafe_allow_html=True)

# 4. جلب البيانات وتحضير القوائم
@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(PROJECTS_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text)).fillna("غير مدرج").astype(str)
        df.columns = [str(c).strip() for c in df.columns]
        
        # تجهيز قوائم الاختيارات
        regions = ["كل المناطق"] + sorted([x for x in df['المنطقة'].unique() if x != "غير مدرج"])
        companies = ["كل الشركات"] + sorted([x for x in df['المطور'].unique() if x != "غير مدرج"])
        
        # تحديد عمود النوع (سكني/تجاري/إداري)
        type_col = ""
        for c in ['النوع', 'نوع الوحدة', 'التصنيف']:
            if c in df.columns:
                type_col = c
                break
        
        if type_col:
            types = ["كل الأنواع"] + sorted([x for x in df[type_col].unique() if x != "غير مدرج"])
        else:
            types = ["كل الأنواع", "سكني", "تجاري", "إداري", "طبي"]
            
        return df, regions, companies, types, type_col
    except:
        return pd.DataFrame(), ["كل المناطق"], ["كل الشركات"], ["كل الأنواع"], ""

df, regions_list, companies_list, types_list, type_col_name = load_data()

if not df.empty:
    # 5. توزيع الفلاتر (4 مربعات بحث)
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    
    with row1_col1:
        s_reg = st.selectbox("📍 اختر المنطقة", options=regions_list)
    with row1_col2:
        s_comp = st.selectbox("🏢 اختر شركة التطوير (المطور)", options=companies_list)
        
    with row2_col1:
        s_typ = st.selectbox("🏗️ نوع الوحدة (سكني/إداري..)", options=types_list)
    with row2_col2:
        s_pri = st.text_input("💰 ميزانية السعر (كتابة)", placeholder="مثال: 7,000,000")

    # 6. منطق الفلترة المتقاطع
    f_df = df.copy()
    if s_reg != "كل المناطق":
        f_df = f_df[f_df['المنطقة'] == s_reg]
    
    if s_comp != "كل الشركات":
        f_df = f_df[f_df['المطور'] == s_comp]
        
    if s_typ != "كل الأنواع" and type_col_name:
        f_df = f_df[f_df[type_col_name] == s_typ]
        
    if s_pri:
        f_df = f_df[f_df['السعر'].str.contains(s_pri, case=False)]

    st.markdown(f"**النتائج المتاحة: {len(f_df)}**")
    st.markdown("---")

    # 7. عرض الكروت
    for _, row in f_df.iterrows():
        st.markdown(f"""
            <div class="project-card">
                <div class="price-badge">{row.get('السعر', '-')}</div>
                <h2 style="color:#d4af37; margin-bottom:10px;">{row.get('المشروع', '-')}</h2>
                <p>📍 {row.get('المنطقة', '-')} | 🏢 {row.get('المطور', '-')} | 🏗️ {row.get('النوع', 'غير محدد')}</p>
                <div style="background:rgba(212,175,55,0.05); padding:15px; border-right:4px solid #d4af37; border-radius:10px; margin-top:10px;">
                    <b>معلومات إضافية:</b> {row.get('سابقة_الأعمال', '-')}
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.error("فشل في تحميل البيانات. تأكد من رابط الشيت.")
