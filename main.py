import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS احترافي متوافق مع بياناتك
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f4f7f9; 
    }
    /* تصميم كرت المشروع */
    .project-card {
        background: white; border-radius: 15px; padding: 20px;
        border-right: 8px solid #003366; margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .info-label { color: #64748b; font-size: 0.9rem; font-weight: bold; }
    .info-value { color: #0f172a; font-weight: 900; }
    .price-badge { background: #dcfce7; color: #166534; padding: 5px 12px; border-radius: 8px; font-weight: 900; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    # الرابط الخاص بالشيت بتاعك
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    df = pd.read_csv(url)
    df.columns = [c.strip() for c in df.columns] # تنظيف أسماء الأعمدة
    return df

df = load_data()

# إدارة التنقل
if 'page' not in st.session_state: st.session_state.page = 'main'

# --- الهيدر ---
st.markdown('<h1 style="text-align:center; color:#003366; margin-bottom:30px;">🏠 منصة معلوماتى العقارية</h1>', unsafe_allow_html=True)

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    # الفلاتر بناءً على خانات الشيت
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        s_area = st.selectbox("📍 اختار المنطقة", ["الكل"] + sorted(df['Area'].unique().tolist()))
    with col_f2:
        s_type = st.selectbox("🏗️ نوع الوحدة", ["الكل"] + sorted(df['Type'].unique().tolist()))
    with col_f3:
        s_dev = st.text_input("🏢 ابحث باسم المطور")

    # تطبيق الفلترة
    f_df = df.copy()
    if s_area != "الكل": f_df = f_df[f_df['Area'] == s_area]
    if s_type != "الكل": f_df = f_df[f_df['Type'] == s_type]
    if s_dev: f_df = f_df[f_df['Developer'].str.contains(s_dev, na=False, case=False)]

    # عرض النتائج في شبكة (Grid)
    grid = st.columns(2)
    for idx, (i, row) in enumerate(f_df.iterrows()):
        with grid[idx % 2]:
            st.markdown(f"""
                <div class="project-card">
                    <div style="display:flex; justify-content:space-between;">
                        <span style="font-size:1.3rem; font-weight:900; color:#003366;">{row['Project']}</span>
                        <span class="price-badge">{row['Price']}</span>
                    </div>
                    <p style="color:#64748b; margin-top:5px;">🏢 {row['Developer']} | 📍 {row['Area']}</p>
                    <hr style="margin:10px 0;">
                    <div style="display:flex; justify-content:space-between; font-size:0.85rem;">
                        <span>💰 مقدم: <b>{row['Down_Payment']}</b></span>
                        <span>⏳ تقسيط: <b>{row['Installments']} سنوات</b></span>
                        <span>🔑 استلام: <b>{row['Delivery']}</b></span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"عرض تفاصيل {row['Project']}", key=f"btn_{i}", use_container_width=True):
                st.session_state.selected_item = row.to_dict()
                st.session_state.page = 'details'
                st.rerun()

# --- صفحة التفاصيل (الاستفادة الكاملة من الشيت) ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 العودة للبحث"):
        st.session_state.page = 'main'
        st.rerun()

    # رأس الصفحة
    st.markdown(f"""
        <div style="background:white; padding:25px; border-radius:15px; border-right:10px solid #003366; margin:20px 0;">
            <h1 style="margin:0;">{item['Project']}</h1>
            <p style="font-size:1.2rem; color:#64748b;">بواسطة المطور: <b>{item['Developer']}</b></p>
        </div>
    """, unsafe_allow_html=True)

    # التبويبات المطلوبة
    tab_dev, tab_projs = st.tabs(["👤 معلومات المطور", "🏗️ مشاريع المطور"])

    with tab_dev:
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.markdown(f"### 🖋️ بطاقة المطور")
            st.write(f"**صاحب الشركة:** {item['Owner']}")
            st.write(f"**قوة الشركة (الزتونة):** {item['Detailed_Info']}")
            st.write(f"**الوصف العام:** {item['Description']}")
        
        with col_info2:
            st.markdown(f"### 💳 تفاصيل العرض")
            st.success(f"**سعر الوحدة:** {item['Price']}")
            st.info(f"**أقل قيمة استثمار (Min Val):** {item['Min_Val']}")
            st.warning(f"**نظام السداد:** مقدم {item['Down_Payment']} وتقسيط على {item['Installments']} سنوات")

    with tab_projs:
        st.subheader(f"كل مشاريع {item['Developer']} في السوق")
        # فلترة تلقائية لجلب أي سطر آخر في الشيت لنفس المطور
        all_dev_projs = df[df['Developer'] == item['Developer']]
        for _, p in all_dev_projs.iterrows():
            st.markdown(f"""
                <div style="background:#fff; padding:15px; border-radius:10px; border:1px solid #e2e8f0; margin-bottom:10px;">
                    <b>🏗️ {p['Project']}</b> - {p['Area']} ({p['Type']}) <br>
                    <small>السعر يبدأ من: {p['Price']} | استلام: {p['Delivery']}</small>
                </div>
            """, unsafe_allow_html=True)
