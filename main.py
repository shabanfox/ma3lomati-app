import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعداد الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# 2. رابط البيانات (تم تحويله لـ CSV للقراءة البرمجية)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR-Nhmw2xNTG_KMrLykWa6S7EtAW5HAbIvox8rj1HRXFKH6m-TLwOS6ZUBqWykKrhtldnkGSfdD5QVc/pub?output=csv"

# 3. التنسيق (CSS) - تصميم عصري وإخفاء الزوائد
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
    /* شريط التمرير في اليسار */
    ::-webkit-scrollbar { width: 12px !important; }
    ::-webkit-scrollbar-track { background: #0d1117 !important; }
    ::-webkit-scrollbar-thumb { background: #d4af37 !important; border-radius: 10px; }

    /* تنسيق الكروت والتبويبات */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1c2128; border-radius: 10px 10px 0 0; 
        padding: 10px 30px; color: white; border: 1px solid #30363d;
    }
    .stTabs [aria-selected="true"] { background-color: #d4af37 !important; color: black !important; }
    
    .info-box {
        background: rgba(212, 175, 55, 0.05);
        border: 2px solid #d4af37;
        border-radius: 20px;
        padding: 30px;
        margin-top: 20px;
    }
    .project-card {
        background: #1c2128; border: 1px solid #30363d;
        border-radius: 15px; padding: 25px; margin-bottom: 20px;
    }
    .price-badge { background: #d4af37; color: #000; padding: 5px 15px; border-radius: 8px; font-weight: 900; float: left; }
    label { color: #d4af37 !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. جلب البيانات
@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(SHEET_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text)).fillna("-").astype(str)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

df = load_data()

# الهيدر المتحرك البسيط
st.markdown("""
    <div style="text-align:center; padding: 20px; border-bottom: 1px solid #30363d; margin-bottom: 30px;">
        <h1 style="color:#d4af37; font-weight:900; font-size: 3em; margin:0;">منصة معلوماتي</h1>
        <p style="opacity:0.7;">الموسوعة العقارية الشاملة للمطورين والمشاريع</p>
    </div>
""", unsafe_allow_html=True)

if not df.empty:
    # 5. الفلاتر (4 فلاتر احترافية)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        regions = ["كل المناطق"] + sorted(df['المنطقة'].unique().tolist())
        s_reg = st.selectbox("📍 المنطقة", regions)
    with c2:
        companies = ["كل المطورين"] + sorted(df['المطور'].unique().tolist())
        s_comp = st.selectbox("🏢 المطور", companies)
    with c3:
        # البحث عن عمود النوع تلقائياً
        type_col = 'النوع' if 'النوع' in df.columns else df.columns[0]
        types = ["كل الأنواع"] + sorted(df[type_col].unique().tolist())
        s_typ = st.selectbox("🏗️ نوع الوحدة", types)
    with c4:
        s_pri = st.text_input("💰 الميزانية", placeholder="بحث بالسعر...")

    # 6. منطق العرض
    # إذا تم اختيار مطور معين، نعرض نظام "الموسوعة"
    if s_comp != "كل المطورين":
        st.markdown(f"<h2 style='text-align:center; color:#d4af37; margin-top:20px;'>{s_comp}</h2>", unsafe_allow_html=True)
        tab_info, tab_projects = st.tabs(["ℹ️ معلومات الشركة", "🏗️ مشاريع الشركة"])
        
        with tab_info:
            # سحب بيانات المطور من أول ظهور له في الجدول
            comp_info = df[df['المطور'] == s_comp].iloc[0]
            st.markdown(f"""
                <div class="info-box">
                    <h3 style="color:#d4af37; border-bottom: 1px solid rgba(212,175,55,0.3); padding-bottom:10px;">📜 نبذة عن المطور</h3>
                    <p style="font-size:1.2em;"><b>👤 المالك / الإدارة:</b> {comp_info.get('المالك', 'غير مدرج')}</p>
                    <p style="font-size:1.1em; line-height:1.8;"><b>🏗️ سابقة الأعمال والخبرة:</b><br>{comp_info.get('سابقة_الأعمال', 'لا توجد تفاصيل حالياً.')}</p>
                </div>
            """, unsafe_allow_html=True)
            
        with tab_projects:
            p_df = df[df['المطور'] == s_comp]
            for _, row in p_df.iterrows():
                st.markdown(f"""
                    <div class="project-card">
                        <div class="price-badge">{row.get('السعر', '-')}</div>
                        <h3 style="color:#d4af37;">{row.get('المشروع', '-')}</h3>
                        <p>📍 {row.get('المنطقة', '-')} | 🏗️ {row.get(type_col, '-')} | 💳 {row.get('السداد', '-')}</p>
                    </div>
                """, unsafe_allow_html=True)
    
    else:
        # عرض البحث العام
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df['المنطقة'] == s_reg]
        if s_typ != "كل الأنواع": f_df = f_df[f_df[type_col] == s_typ]
        if s_pri: f_df = f_df[f_df['السعر'].str.contains(s_pri, case=False)]
        
        st.markdown(f"**النتائج المتاحة: {len(f_df)}**")
        for _, row in f_df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="price-badge">{row.get('السعر', '-')}</div>
                    <h3 style="color:#d4af37; margin:0;">{row.get('المشروع', '-')}</h3>
                    <p style="margin:5px 0;">📍 {row.get('المنطقة', '-')} | 🏢 {row.get('المطور', '-')}</p>
                    <small style="opacity:0.7;">🏗️ {row.get(type_col, '-')} | 💳 {row.get('السداد', '-')}</small>
                </div>
            """, unsafe_allow_html=True)
else:
    st.error("❌ فشل في قراءة البيانات من الرابط المزود. تأكد من نشر الملف (Publish to Web) بصيغة CSV.")
