import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }
    .header-wrapper {
        display: flex; justify-content: space-between; align-items: center;
        background: white; padding: 15px 30px; border-radius: 15px;
        box-shadow: 0 2px 15px rgba(0,0,0,0.05); margin-bottom: 20px;
    }
    .card {
        background: white; border-radius: 12px; padding: 15px;
        border-right: 6px solid #003366; margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .price-tag { color: #16a34a; font-weight: bold; font-size: 1.1rem; }
    </style>
""", unsafe_allow_html=True)

# 2. دالة تنظيف الأرقام (تحويل 8.5M إلى رقم حقيقي)
def clean_numeric(value):
    if pd.isna(value): return 0.0
    s = str(value).upper().replace(' ', '')
    if 'M' in s:
        res = re.findall(r"[-+]?\d*\.\d+|\d+", s)
        return float(res[0]) * 1000000 if res else 0.0
    if 'K' in s:
        res = re.findall(r"[-+]?\d*\.\d+|\d+", s)
        return float(res[0]) * 1000 if res else 0.0
    res = re.findall(r"[-+]?\d*\.\d+|\d+", s)
    return float(res[0]) if res else 0.0

# 3. جلب البيانات (استبدل الرابط برابط الشيت الخاص بك)
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    df = pd.read_csv(url)
    # تنظيف العناوين من المسافات
    df.columns = [c.strip() for c in df.columns]
    # إضافة أعمدة رقمية للفلترة
    df['Price_Num'] = df['Price'].apply(clean_numeric)
    df['Down_Num'] = df['Min_Val'].apply(clean_numeric)
    return df

df = load_data()

# إدارة التنقل
if 'page' not in st.session_state: st.session_state.page = 'main'

# --- الهيدر ---
st.markdown('<div class="header-wrapper"><div style="color:#003366; font-weight:900; font-size:1.8rem;">منصة معلوماتى العقارية</div></div>', unsafe_allow_html=True)

if st.session_state.page == 'main':
    # --- الفلاتر الذكية ---
    with st.expander("🔍 محرك البحث المتقدم", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            s_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df['Area'].unique().tolist()))
        with c2:
            s_type = st.selectbox("🏠 النوع", ["الكل"] + sorted(df['Type'].unique().tolist()))
        with c3:
            max_p = st.number_input("💵 الحد الأقصى للسعر (مليون)", value=30.0) * 1000000
        with c4:
            s_dev = st.text_input("🏢 اسم المطور")

    # تطبيق الفلترة
    f_df = df.copy()
    if s_area != "الكل": f_df = f_df[f_df['Area'] == s_area]
    if s_type != "الكل": f_df = f_df[f_df['Type'] == s_type]
    if s_dev: f_df = f_df[f_df['Developer'].str.contains(s_dev, na=False, case=False)]
    f_df = f_df[f_df['Price_Num'] <= max_p]

    # --- عرض النتائج (3 صفوف) ---
    items_per_page = 6
    cols = st.columns(2)
    for idx, (i, row) in enumerate(f_df.head(items_per_page).iterrows()):
        with cols[idx % 2]:
            st.markdown(f"""
                <div class="card">
                    <div style="font-weight:900; color:#003366; font-size:1.2rem;">{row['Project']} - {row['Developer']}</div>
                    <div style="color:#64748b;">📍 {row['Area']} | 📅 استلام {row['Delivery']}</div>
                    <div class="price-tag">السعر: {row['Price']} ج.م</div>
                    <div style="font-size:0.9rem; margin-top:5px;">💰 مقدم: {row['Min_Val']} | ⏳ تقسيط {row['Installments']} سنوات</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"تفاصيل {row['Project']}", key=f"btn_{i}", use_container_width=True):
                st.session_state.selected_item = row.to_dict()
                st.session_state.page = 'details'
                st.rerun()

# --- صفحة التفاصيل (التي طلبتها) ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 عودة للرئيسية"):
        st.session_state.page = 'main'
        st.rerun()

    st.markdown(f"""
        <div style="background:white; padding:30px; border-radius:15px; border-right:10px solid #003366; margin-top:20px;">
            <h1 style="color:#003366;">{item['Project']}</h1>
            <h3 style="color:#64748b;">بواسطة: {item['Developer']}</h3>
        </div>
    """, unsafe_allow_html=True)

    # التبويبات المطلوبة
    tab1, tab2 = st.tabs(["👤 معلومات المطور", "🏗️ مشاريع المطور"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.info(f"**المالك:** {item['Owner']}")
            st.write(f"**عن الشركة:** {item['Detailed_Info']}")
        with c2:
            st.success(f"**لماذا هذا المطور؟**\n\n {item['Description']}")
    
    with tab2:
        st.subheader(f"كافة مشاريع {item['Developer']}")
        dev_projects = df[df['Developer'] == item['Developer']]
        for _, p in dev_projects.iterrows():
            st.markdown(f"""
                <div style="padding:10px; border-bottom:1px solid #eee;">
                    <b>{p['Project']}</b> - {p['Area']} ({p['Type']})
                </div>
            """, unsafe_allow_html=True)
