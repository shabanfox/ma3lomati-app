import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة (Clean Nawy Look)
st.set_page_config(page_title="معلوماتي العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* إخفاء الهيدر وأيقونة جيت هب والقوائم تماماً */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important; text-align: right;
        font-family: 'Cairo', sans-serif; background-color: #f4f7f6; color: #1a1a1a;
    }

    /* هيدر ناوي الاحترافي */
    .nawy-header {
        background: #ffffff; padding: 25px; text-align: center;
        border-bottom: 2px solid #c49a6c; margin-bottom: 30px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    /* كارت المطور */
    .dev-profile-card {
        background: #ffffff; border-radius: 20px; padding: 35px;
        margin-bottom: 35px; border-right: 12px solid #c49a6c;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    }

    /* شبكة المشاريع Grid */
    .project-grid {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 25px; margin-top: 20px;
    }
    .project-card {
        background: #ffffff; border-radius: 15px; border: 1px solid #eee;
        padding: 25px; transition: 0.4s; position: relative;
    }
    .project-card:hover { transform: translateY(-10px); box-shadow: 0 15px 35px rgba(0,0,0,0.1); border-color: #c49a6c; }
    
    .price-tag {
        background: #c49a6c; color: #fff; padding: 5px 15px;
        border-radius: 8px; font-weight: 900; position: absolute; left: 20px; top: 20px;
    }

    /* الفلاتر */
    .filter-box { background: #fff; padding: 20px; border-radius: 15px; border: 1px solid #eee; margin-bottom: 30px; }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات بمرونة عالية
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR0vzgtd_E2feFVen6GGR02lYcB7kUASgyLyvqBGA7pAHseUf9KxAyEyDHU935VLFEWQot2p5FBFSwv/pub?output=csv"

@st.cache_data(ttl=2)
def load_data():
    try:
        res = requests.get(SHEET_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("-").astype(str)
    except: return pd.DataFrame()

df = load_data()

# الهيدر
st.markdown('<div class="nawy-header"><h1>مـعـلـومـاتـي <span style="color:#c49a6c;">الـعـقـاريـة</span></h1></div>', unsafe_allow_html=True)

if not df.empty:
    # دالة ذكية لإيجاد الأعمدة حتى لو الأسماء غلط في الشيت
    def get_col_safe(search_list):
        for name in search_list:
            if name in df.columns: return name
        return df.columns[0] # البديل الأول

    C_DEV = get_col_safe(["المطور", "شركة", "الشركة", "Developer"])
    C_REG = get_col_safe(["المنطقة", "المنطقه", "مكان", "Location", "Region"])
    C_PROJ = get_col_safe(["المشروع", "اسم المشروع", "Project"])
    C_OWNER = get_col_safe(["المالك", "رئيس مجلس الإدارة", "Owner"])
    C_BIO = get_col_safe(["سابقة_الأعمال", "سابقة الأعمال", "عن الشركة", "Bio"])

    # منطقة الفلاتر
    st.markdown('<div class="filter-box">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: s_dev = st.selectbox("🏢 اختر المطور", ["كل المطورين"] + sorted(df[C_DEV].unique().tolist()))
    with c2: s_reg = st.selectbox("📍 فلتر بالمنطقة", ["كل المناطق"] + sorted(df[C_REG].unique().tolist()))
    st.markdown('</div>', unsafe_allow_html=True)

    if s_dev != "كل المطورين":
        dev_rows = df[df[C_DEV] == s_dev]
        main = dev_rows.iloc[0]
        
        # بروفايل المطور (Nawy Style)
        st.markdown(f"""
            <div class="dev-profile-card">
                <h2 style="color:#c49a6c; margin-bottom:10px;">{s_dev}</h2>
                <p style="font-size:1.1em;">👤 <b>رئيس مجلس الإدارة:</b> {main.get(C_OWNER, '-')}</p>
                <hr style="opacity:0.1; margin:20px 0;">
                <h4 style="color:#c49a6c;">📜 سابقة الأعمال والنبذة التاريخية:</h4>
                <p style="line-height:1.8; color:#444; text-align:justify;">{main.get(C_BIO, '-')}</p>
            </div>
            <h3 style="margin-bottom:20px; font-weight:900;">🏗️ مشاريع {s_dev}</h3>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, r in dev_rows.iterrows():
            if r[C_PROJ] != "-":
                st.markdown(f"""
                    <div class="project-card">
                        <div class="price-tag">{r.get('السعر', 'اتصل بنا')}</div>
                        <h3 style="margin-top:35px; color:#1a1a1a;">{r[C_PROJ]}</h3>
                        <p style="color:#666;">📍 {r[C_REG]} | 🏗️ {r.get('النوع','-')}</p>
                        <div style="background:#fcf8f3; padding:10px; border-radius:8px; font-size:0.85em; color:#888;">
                            💳 نظام السداد: {r.get('السداد','-')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # عرض كل المشاريع
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df[C_REG] == s_reg]
        
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, r in f_df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="price-tag">{r.get('السعر', 'اتصل بنا')}</div>
                    <h3 style="margin-top:35px;">{r[C_PROJ]}</h3>
                    <p style="color:#c49a6c; font-weight:700;">🏢 {r[C_DEV]}</p>
                    <p style="color:#666; font-size:0.9em;">📍 {r[C_REG]}</p>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("⚠️ جاري تحديث البيانات من جوجل شيت... يرجى الانتظار.")
