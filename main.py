import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعداد الصفحة
st.set_page_config(page_title="منصة معلوماتي - الموسوعة العقارية", layout="wide", page_icon="🏢")

# 2. رابط الشيت (بصيغة CSV)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR0vzgtd_E2feFVen6GGR02lYcB7kUASgyLyvqBGA7pAHseUf9KxAyEyDHU935VLFEWQot2p5FBFSwv/pub?output=csv"

# 3. تصميم CSS احترافي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, header, footer, .stDeployButton {visibility: hidden;}
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important; font-family: 'Cairo', sans-serif;
        background-color: #0d1117; color: white; text-align: right;
    }
    .stats-box {
        background: rgba(212, 175, 55, 0.1); border: 1px solid #d4af37;
        border-radius: 15px; padding: 15px; text-align: center; margin-bottom: 10px;
    }
    .project-card {
        background: #1c2128; border-right: 5px solid #d4af37;
        border-radius: 10px; padding: 20px; margin-bottom: 15px;
    }
    .dev-profile {
        background: linear-gradient(135deg, #1c2128 0%, #0d1117 100%);
        border: 1px solid #d4af37; border-radius: 15px; padding: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# 4. جلب البيانات وتنظيفها
@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(SHEET_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        # أهم خطوة: تنظيف أسماء الأعمدة من المسافات المخفية
        df.columns = [str(c).strip() for c in df.columns]
        df = df.fillna("-").astype(str)
        return df
    except Exception as e:
        st.error(f"خطأ في الاتصال بالشيت: {e}")
        return pd.DataFrame()

df = load_data()

st.markdown("<h1 style='text-align:center; color:#d4af37;'>🏢 موسوعة المطورين العقاريين</h1>", unsafe_allow_html=True)

if not df.empty:
    # تحديد الأعمدة بذكاء (لو الاسم مش موجود ياخد البديل)
    def get_col(options, default_idx=0):
        for opt in options:
            if opt in df.columns: return opt
        return df.columns[default_idx] if len(df.columns) > default_idx else df.columns[0]

    C_PROJ = get_col(["المشروع", "اسم المشروع", "Project"])
    C_DEV = get_col(["المطور", "الشركة", "Developer"])
    C_REG = get_col(["المنطقة", "Location", "Region"])
    C_OWNER = get_col(["المالك", "Owner"])
    C_BIO = get_col(["سابقة_الأعمال", "سابقة الأعمال", "Bio"])

    # إحصائيات
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='stats-box'><h3>{len(df[C_DEV].unique())}</h3> مطور</div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='stats-box'><h3>{len(df[C_PROJ].unique())}</h3> مشروع</div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='stats-box'><h3>{len(df[C_REG].unique())}</h3> منطقة</div>", unsafe_allow_html=True)

    # الفلاتر
    st.markdown("---")
    f1, f2 = st.columns(2)
    with f1:
        s_reg = st.selectbox("📍 اختر المنطقة", ["كل المناطق"] + sorted(df[C_REG].unique().tolist()))
    with f2:
        s_dev = st.selectbox("🏢 اختر المطور", ["كل المطورين"] + sorted(df[C_DEV].unique().tolist()))

    # عرض النتائج
    if s_dev != "كل المطورين":
        row = df[df[C_DEV] == s_dev].iloc[0]
        st.markdown(f"<div class='dev-profile'>", unsafe_allow_html=True)
        st.subheader(f"📂 ملف شركة: {s_dev}")
        tab_info, tab_projs = st.tabs(["ℹ️ معلومات المطور", "🏗️ المشاريع"])
        
        with tab_info:
            st.write(f"**👤 المالك:** {row.get(C_OWNER, 'غير مدرج')}")
            st.write(f"**📜 سابقة الأعمال:**")
            st.write(row.get(C_BIO, '-'))
            
        with tab_projs:
            dev_projs = df[df[C_DEV] == s_dev]
            for _, p in dev_projs.iterrows():
                st.markdown(f"<div class='project-card'><h3>{p[C_PROJ]}</h3><p>📍 {p[C_REG]}</p></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # عرض البحث العام
        res_df = df.copy()
        if s_reg != "كل المناطق": res_df = res_df[res_df[C_REG] == s_reg]
        for _, r in res_df.iterrows():
            st.markdown(f"<div class='project-card'><h3>{r[C_PROJ]}</h3><p>🏢 {r[C_DEV]} | 📍 {r[C_REG]}</p></div>", unsafe_allow_html=True)
else:
    st.warning("تأكد من نشر الشيت (Publish to web) واختيار صيغة CSV.")
