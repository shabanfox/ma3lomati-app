import streamlit as st
import pandas as pd
import requests
from io import StringIO

# إعداد الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# رابط الشيت (بصيغة CSV)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR0vzgtd_E2feFVen6GGR02lYcB7kUASgyLyvqBGA7pAHseUf9KxAyEyDHU935VLFEWQot2p5FBFSwv/pub?output=csv"

@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(SHEET_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        # تنظيف شامل لأسماء الأعمدة (إزالة المسافات والحركات)
        df.columns = [str(c).strip() for c in df.columns]
        df = df.fillna("-").astype(str)
        return df
    except:
        return pd.DataFrame()

df = load_data()

# تصميم الهيدر
st.markdown("<h1 style='text-align:center; color:#d4af37;'>🏢 دليل المطورين العقاريين في مصر</h1>", unsafe_allow_html=True)

if not df.empty:
    # ميزة البحث عن العمود (عشان لو الترتيب غلط الكود ميفصلش)
    cols = df.columns.tolist()
    
    # تحديد أسماء الأعمدة المستخدمة
    C_PROJ = "المشروع" if "المشروع" in cols else cols[0]
    C_DEV = "المطور" if "المطور" in cols else (cols[1] if len(cols)>1 else cols[0])
    C_REG = "المنطقة" if "المنطقة" in cols else (cols[2] if len(cols)>2 else cols[0])
    C_OWNER = "المالك" if "المالك" in cols else "غير مدرج"
    C_BIO = "سابقة_الأعمال" if "سابقة_الأعمال" in cols else (cols[7] if len(cols)>7 else "لا توجد تفاصيل")

    # الفلاتر
    st.sidebar.header("🔍 فلاتر البحث")
    s_dev = st.sidebar.selectbox("اختر المطور", ["كل المطورين"] + sorted(df[C_DEV].unique().tolist()))
    s_reg = st.sidebar.selectbox("اختر المنطقة", ["كل المناطق"] + sorted(df[C_REG].unique().tolist()))

    # العرض الموسوعي
    if s_dev != "كل المطورين":
        dev_info = df[df[C_DEV] == s_dev].iloc[0]
        st.markdown(f"### 📂 ملف شركة: {s_dev}")
        
        t1, t2 = st.tabs(["ℹ️ عن الشركة والمالك", "🏗️ المشاريع الحالية"])
        
        with t1:
            st.info(f"👤 **المالك / رئيس مجلس الإدارة:** {dev_info.get(C_OWNER, '-')}")
            st.success(f"📜 **سابقة الأعمال وتاريخ الشركة:**\n\n{dev_info.get(C_BIO, '-')}")
            
        with t2:
            projects = df[df[C_DEV] == s_dev]
            for _, row in projects.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div style="background:#1c2128; padding:15px; border-radius:10px; border-right:5px solid #d4af37; margin-bottom:10px;">
                        <h4 style="margin:0;">{row[C_PROJ]}</h4>
                        <p style="margin:0; opacity:0.8;">📍 {row[C_REG]} | 💳 {row.get('السداد','-')}</p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        # البحث العام
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df[C_REG] == s_reg]
        
        st.write(f"عدد النتائج: {len(f_df)}")
        for _, row in f_df.iterrows():
            st.markdown(f"**{row[C_PROJ]}** - {row[C_DEV]} ({row[C_REG]})")
            st.divider()
else:
    st.warning("جاري تحميل البيانات... تأكد من نشر الشيت بصيغة CSV")
