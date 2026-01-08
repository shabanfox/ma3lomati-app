import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعداد الصفحة
st.set_page_config(page_title="منصة معلوماتي - الموسوعة", layout="wide", page_icon="🏢")

# 2. روابط البيانات (تأكد من تحديث روابط الشيتات لو فصلتهم)
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
    .gold-box { border: 2px solid #d4af37; border-radius: 20px; padding: 25px; background: rgba(212,175,55,0.05); }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 50px; }
    .price-badge { background: #d4af37; color: #000; padding: 5px 15px; border-radius: 8px; font-weight: 900; float: left; }
    .project-card { background: #1c2128; border: 1px solid #30363d; border-radius: 15px; padding: 25px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 4. جلب البيانات
@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(PROJECTS_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text)).fillna("غير مدرج").astype(str)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except: return pd.DataFrame()

df = load_data()

if not df.empty:
    st.markdown("<h1 style='text-align:center; color:#d4af37;'>🏢 موسوعة العقارات الذكية</h1>", unsafe_allow_html=True)
    
    # 5. الفلاتر الأساسية
    col1, col2, col3 = st.columns(3)
    with col1:
        regions = ["كل المناطق"] + sorted(df['المنطقة'].unique().tolist())
        s_reg = st.selectbox("📍 المنطقة", regions)
    with col2:
        companies = ["اختر شركة للاستعلام"] + sorted(df['المطور'].unique().tolist())
        s_comp = st.selectbox("🏢 شركة التطوير (المطور)", companies)
    with col3:
        types = ["كل الأنواع"] + sorted(df['النوع'].unique().tolist()) if 'النوع' in df.columns else ["كل الأنواع"]
        s_typ = st.selectbox("🏗️ نوع الوحدة", types)

    # 6. نظام العرض التفاعلي
    if s_comp != "اختر شركة للاستعلام":
        st.markdown(f"---")
        st.markdown(f"<h2 style='text-align:center; color:#d4af37;'>📂 شركة: {s_comp}</h2>", unsafe_allow_html=True)
        
        # اختيار العرض
        tab_info, tab_projects = st.tabs(["ℹ️ معلومات الشركة", "🏗️ مشاريع الشركة"])
        
        with tab_info:
            # هنا بنسحب أول سطر للمطور ده عشان نعرض بياناته العامة
            comp_data = df[df['المطور'] == s_comp].iloc[0]
            st.markdown(f"""
                <div class="gold-box">
                    <h3 style="color:#d4af37;">📜 ملف المطور العقاري</h3>
                    <p><b>👤 اسم المالك:</b> {comp_data.get('المالك', 'غير مدرج')}</p>
                    <p><b>🏗️ سابقة الأعمال:</b><br>{comp_data.get('سابقة_الأعمال', 'غير مدرج')}</p>
                    <p style="font-size:0.9em; opacity:0.8;">سيتم إضافة تفاصيل (سنة التأسيس، حجم الاستثمارات) قريباً من قاعدة البيانات الجديدة.</p>
                </div>
            """, unsafe_allow_html=True)
            
        with tab_projects:
            # هنا بنعرض كل مشاريع الشركة دي بس
            company_projects = df[df['المطور'] == s_comp]
            for _, row in company_projects.iterrows():
                st.markdown(f"""
                    <div class="project-card">
                        <div class="price-badge">{row.get('السعر', '-')}</div>
                        <h3 style="color:#d4af37;">{row.get('المشروع', '-')}</h3>
                        <p>📍 {row.get('المنطقة', '-')} | 💳 {row.get('السداد', '-')}</p>
                    </div>
                """, unsafe_allow_html=True)
    
    else:
        # عرض المشاريع بشكل عام لو مفيش شركة مختارة
        st.markdown("### 🔍 نتائج البحث العامة")
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df['المنطقة'] == s_reg]
        if s_typ != "كل الأنواع": f_df = f_df[f_df['النوع'] == s_typ]
        
        for _, row in f_df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="price-badge">{row.get('السعر', '-')}</div>
                    <h3 style="color:#d4af37; margin-bottom:10px;">{row.get('المشروع', '-')}</h3>
                    <p>📍 {row.get('المنطقة', '-')} | 🏢 {row.get('المطور', '-')}</p>
                </div>
            """, unsafe_allow_html=True)

else:
    st.warning("جاري تحميل البيانات...")
