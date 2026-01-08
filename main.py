import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعداد الصفحة لتبدو كمنصة خاصة (Clean & Professional)
st.set_page_config(page_title="معلومات العقار - لوحة البروكر", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* إخفاء تام لأدوات جيت هب وستريمليت */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important; text-align: right;
        font-family: 'Cairo', sans-serif; background-color: #f8f9fb; color: #2d3436;
    }

    /* هيدر المنصة (Nawy UI Style) */
    .broker-header {
        background: #ffffff; padding: 20px 40px; border-bottom: 2px solid #e1e4e8;
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 30px; box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }

    /* كارت معلومات المطور (الموسوعة) */
    .dev-wiki-card {
        background: #ffffff; border-radius: 12px; padding: 30px;
        border: 1px solid #e1e4e8; border-right: 8px solid #c49a6c;
        margin-bottom: 30px;
    }
    .dev-name { color: #1a1a1a; font-weight: 900; font-size: 2.2em; margin-bottom: 15px; }
    
    /* كروت المشاريع (Grid) */
    .project-grid {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
        gap: 20px;
    }
    .broker-card {
        background: #ffffff; border-radius: 12px; padding: 20px;
        border: 1px solid #e1e4e8; transition: 0.3s;
    }
    .broker-card:hover { border-color: #c49a6c; box-shadow: 0 8px 25px rgba(0,0,0,0.05); }
    
    .data-label { color: #888; font-size: 0.85em; margin-bottom: 3px; }
    .data-value { color: #1a1a1a; font-weight: 700; font-size: 1.1em; margin-bottom: 12px; }
    
    .price-tag-gold {
        color: #c49a6c; font-weight: 900; font-size: 1.2em;
        background: #fcf8f3; padding: 5px 12px; border-radius: 6px; display: inline-block;
    }

    /* تنسيق الفلاتر */
    .filter-bar { background: #ffffff; padding: 15px 25px; border-radius: 12px; border: 1px solid #e1e4e8; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات وحل مشكلة KeyError للأبد
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR0vzgtd_E2feFVen6GGR02lYcB7kUASgyLyvqBGA7pAHseUf9KxAyEyDHU935VLFEWQot2p5FBFSwv/pub?output=csv"

@st.cache_data(ttl=2)
def load_data():
    try:
        res = requests.get(SHEET_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns] # تنظيف أسماء الأعمدة من المسافات
        return df.fillna("-").astype(str)
    except: return pd.DataFrame()

df = load_data()

# الهيدر العلوي
st.markdown('<div class="broker-header"><div><h1 style="margin:0; font-size:1.8em; font-weight:900;">معلوماتـي <span style="color:#c49a6c;">العقارية</span></h1><p style="margin:0; font-size:0.9em; color:#888;">أداة البروكر الذكية للمعلومات</p></div></div>', unsafe_allow_html=True)

if not df.empty:
    # دالة صمام الأمان لإيجاد الأعمدة مهما كانت تسميتها في الشيت
    def get_col(options):
        for opt in options:
            if opt in df.columns: return opt
        return df.columns[0]

    C_DEV = get_col(["المطور", "الشركة", "Developer"])
    C_REG = get_col(["المنطقة", "المنطقه", "Location", "Region"])
    C_PROJ = get_col(["المشروع", "اسم المشروع", "Project"])
    C_OWNER = get_col(["المالك", "رئيس", "Owner"])
    C_BIO = get_col(["سابقة_الأعمال", "عن الشركة", "History", "Bio"])

    # شريط الفلاتر
    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: s_dev = st.selectbox("🏗️ ابحث عن مطور عقاري", ["كل المطورين"] + sorted(df[C_DEV].unique().tolist()))
    with c2: s_reg = st.selectbox("📍 فلتر حسب المنطقة", ["كل المناطق"] + sorted(df[C_REG].unique().tolist()))
    st.markdown('</div>', unsafe_allow_html=True)

    if s_dev != "كل المطورين":
        dev_data = df[df[C_DEV] == s_dev]
        first = dev_data.iloc[0]
        
        # بروفايل المطور (Information Sheet)
        st.markdown(f"""
            <div class="dev-wiki-card">
                <div class="dev-name">{s_dev}</div>
                <div style="display:flex; gap:30px; margin-bottom:20px;">
                    <div><div class="data-label">👤 المالك / الإدارة</div><div class="data-value">{first.get(C_OWNER, '-')}</div></div>
                    <div><div class="data-label">📅 تاريخ التأسيس</div><div class="data-value">{first.get('تأسيس', '-')}</div></div>
                </div>
                <div class="data-label">📜 سابقة الأعمال والخبرات</div>
                <div style="line-height:1.7; color:#444;">{first.get(C_BIO, '-')}</div>
            </div>
            <h3 style="margin-bottom:20px; font-weight:700;">🏠 مشاريع {s_dev} المتاحة للبيع</h3>
        """, unsafe_allow_html=True)
        
        # شبكة مشاريع البروكر
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, r in dev_data.iterrows():
            if r[C_PROJ] != "-":
                st.markdown(f"""
                    <div class="broker-card">
                        <div class="data-label">اسم المشروع</div>
                        <div class="data-value" style="color:#c49a6c; font-size:1.3em;">{r[C_PROJ]}</div>
                        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                            <div><div class="data-label">📍 الموقع</div><div class="data-value">{r[C_REG]}</div></div>
                            <div><div class="data-label">🏗️ النوع</div><div class="data-value">{r.get('النوع','-')}</div></div>
                        </div>
                        <div style="margin-top:10px;"><div class="data-label">💳 نظام السداد</div><div class="data-value" style="font-size:0.95em;">{r.get('السداد','-')}</div></div>
                        <div style="margin-top:10px;"><div class="price-tag-gold">{r.get('السعر', '-')}</div></div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # عرض البحث العام (All Inventory)
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df[C_REG] == s_reg]
        
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, r in f_df.iterrows():
            st.markdown(f"""
                <div class="broker-card">
                    <div class="data-label">المشروع</div>
                    <div class="data-value">{r[C_PROJ]}</div>
                    <div class="data-label">المطور</div>
                    <div class="data-value" style="color:#c49a6c;">{r[C_DEV]}</div>
                    <div class="data-label">الموقع</div>
                    <div class="data-value">{r[C_REG]}</div>
                    <div class="price-tag-gold">{r.get('السعر', '-')}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("⚠️ لم نتمكن من الوصول للبيانات. تأكد من نشر الشيت بصيغة CSV.")
