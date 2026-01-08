import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعداد الصفحة وتصميمها
st.set_page_config(page_title="منصة معلوماتي - دليل المطورين", layout="wide", page_icon="🏢")

# 2. رابط الشيت الجديد (تم تحويله لصيغة CSV للقراءة)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR0vzgtd_E2feFVen6GGR02lYcB7kUASgyLyvqBGA7pAHseUf9KxAyEyDHU935VLFEWQot2p5FBFSwv/pub?output=csv"

# 3. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, header, footer, .stDeployButton {visibility: hidden;}
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important;
        font-family: 'Cairo', sans-serif;
        background-color: #0d1117; color: white; text-align: right;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1c2128; border-radius: 10px; padding: 10px 25px; color: #d4af37;
    }
    .stTabs [aria-selected="true"] { background-color: #d4af37 !important; color: black !important; }
    
    .dev-card {
        background: linear-gradient(135deg, #1c2128 0%, #0d1117 100%);
        border-right: 5px solid #d4af37; border-radius: 15px; padding: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5); margin-bottom: 20px;
    }
    .project-card {
        background: #1c2128; border: 1px solid #30363d; border-radius: 12px;
        padding: 20px; margin-bottom: 15px; border-right: 4px solid #d4af37;
    }
    .stats-box {
        background: rgba(212, 175, 55, 0.1); border: 1px solid #d4af37;
        border-radius: 15px; padding: 15px; text-align: center;
    }
    label { color: #d4af37 !important; font-size: 1.1em !important; }
    </style>
""", unsafe_allow_html=True)

# 4. دالة جلب البيانات
@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(SHEET_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text)).fillna("-").astype(str)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

# الهيدر
st.markdown("<h1 style='text-align:center; color:#d4af37; font-weight:900;'>🏢 موسوعة المطورين العقاريين</h1>", unsafe_allow_html=True)

if not df.empty:
    # إحصائيات سريعة
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='stats-box'><h3>{len(df['المطور'].unique())}</h3> مطور عقاري</div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='stats-box'><h3>{len(df['المشروع'].unique())}</h3> مشروع مدرج</div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='stats-box'><h3>{len(df['المنطقة'].unique())}</h3> منطقة</div>", unsafe_allow_html=True)
    
    st.markdown("---")

    # 5. الفلاتر
    col_reg, col_dev, col_typ = st.columns(3)
    with col_reg:
        s_reg = st.selectbox("📍 فلتر بالمنطقة", ["كل المناطق"] + sorted(df['المنطقة'].unique().tolist()))
    with col_dev:
        s_dev = st.selectbox("🏢 اختر المطور (للعرض الموسوعي)", ["كل المطورين"] + sorted(df['المطور'].unique().tolist()))
    with col_typ:
        type_col = 'النوع' if 'النوع' in df.columns else df.columns[0]
        s_typ = st.selectbox("🏗️ نوع الوحدة", ["كل الأنواع"] + sorted(df[type_col].unique().tolist()))

    # 6. منطق العرض
    if s_dev != "كل المطورين":
        # عرض معلومات المطور + مشاريع المطور فقط
        dev_data = df[df['المطور'] == s_dev].iloc[0]
        st.markdown(f"<h2 style='color:#d4af37; text-align:center; margin-top:20px;'>📂 ملف شركة: {s_dev}</h2>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["ℹ️ معلومات الشركة والمالك", "🏗️ مشاريع المطور"])
        
        with tab1:
            st.markdown(f"""
                <div class="dev-card">
                    <h3 style="color:#d4af37;">👤 بيانات الإدارة والمالك</h3>
                    <p style="font-size:1.2em;">{dev_data.get('المالك', 'بيان غير مدرج')}</p>
                    <hr style="opacity:0.2;">
                    <h3 style="color:#d4af37;">📜 سابقة الأعمال والنبذة التاريخية</h3>
                    <p style="line-height:1.8; font-size:1.1em;">{dev_data.get('سابقة_الأعمال', 'لا توجد تفاصيل مدرجة.')}</p>
                </div>
            """, unsafe_allow_html=True)
            
        with tab2:
            dev_projects = df[df['المطور'] == s_dev]
            for _, row in dev_projects.iterrows():
                st.markdown(f"""
                    <div class="project-card">
                        <div style="background:#d4af37; color:black; padding:2px 10px; border-radius:5px; float:left; font-weight:bold;">{row.get('السعر','-')}</div>
                        <h3 style="margin:0;">{row.get('المشروع','-')}</h3>
                        <p style="margin:5px 0; opacity:0.8;">📍 {row.get('المنطقة','-')} | 🏗️ {row.get(type_col,'-')}</p>
                        <p style="font-size:0.9em; color:#d4af37;">💳 نظام السداد: {row.get('السداد','-')}</p>
                    </div>
                """, unsafe_allow_html=True)

    else:
        # البحث العام
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df['المنطقة'] == s_reg]
        if s_typ != "كل الأنواع": f_df = f_df[f_df[type_col] == s_typ]
        
        st.markdown(f"### 🔍 نتائج البحث ({len(f_df)} نتيجة)")
        for _, row in f_df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div style="background:#d4af37; color:black; padding:2px 10px; border-radius:5px; float:left; font-weight:bold;">{row.get('السعر','-')}</div>
                    <h3 style="margin:0;">{row.get('المشروع','-')}</h3>
                    <p style="margin:5px 0;">🏢 {row.get('المطور','-')} | 📍 {row.get('المنطقة','-')}</p>
                </div>
            """, unsafe_allow_html=True)
else:
    st.error("⚠️ لم يتم العثور على بيانات. تأكد من أن رابط جوجل شيت 'منشور على الويب' (Published to Web) بصيغة CSV.")
