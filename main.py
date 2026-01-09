import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }
    .header-box { background: #003366; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
    .project-card {
        background: white; border-radius: 12px; padding: 20px;
        border-right: 8px solid #003366; margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .price-txt { color: #16a34a; font-weight: 900; font-size: 1.2rem; }
    .stTabs [data-baseweb="tab"] { font-weight: bold; font-size: 1.1rem; }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات من رابط الـ CSV المباشر الخاص بك
@st.cache_data
def load_data():
    # تم تحويل الرابط تلقائياً من pubhtml إلى csv ليعمل الكود
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        # تنظيف أسماء الأعمدة من أي رموز أو مسافات خفية
        df.columns = [c.strip().replace('#', '').replace(' ', '_') for c in df.columns]
        return df
    except Exception as e:
        st.error(f"يرجى التأكد من نشر الشيت كـ CSV. الخطأ: {e}")
        return None

df = load_data()

# إدارة التنقل
if 'page' not in st.session_state: st.session_state.page = 'main'

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main' and df is not None:
    st.markdown('<div class="header-box"><h1>منصة معلوماتى العقارية</h1></div>', unsafe_allow_html=True)
    
    # الفلاتر
    col1, col2, col3 = st.columns(3)
    with col1:
        s_area = st.selectbox("📍 اختار المنطقة", ["الكل"] + sorted(df['Area'].dropna().unique().tolist()))
    with col2:
        s_dev = st.text_input("🏢 ابحث باسم المطور")
    with col3:
        s_type = st.selectbox("🏠 النوع", ["الكل"] + sorted(df['Type'].dropna().unique().tolist()))

    # تصفية البيانات
    f_df = df.copy()
    if s_area != "الكل": f_df = f_df[f_df['Area'] == s_area]
    if s_type != "الكل": f_df = f_df[f_df['Type'] == s_type]
    if s_dev: f_df = f_df[f_df['Developer'].str.contains(s_dev, na=False, case=False)]

    # العرض
    grid = st.columns(2)
    for idx, (i, row) in enumerate(f_df.iterrows()):
        with grid[idx % 2]:
            st.markdown(f"""
                <div class="project-card">
                    <h3 style="margin:0; color:#003366;">{row['Project']}</h3>
                    <p style="color:#64748b; margin-bottom:10px;"><b>المطور:</b> {row['Developer']}</p>
                    <div style="display:flex; justify-content:space-between;">
                        <span class="price-txt">{row['Price']}</span>
                        <span>📍 {row['Area']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"عرض التفاصيل والزتونة لـ {row['Project']}", key=f"btn_{i}", use_container_width=True):
                st.session_state.selected_item = row.to_dict()
                st.session_state.page = 'details'
                st.rerun()

# --- صفحة التفاصيل ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 عودة للقائمة الرئيسية"):
        st.session_state.page = 'main'
        st.rerun()

    st.markdown(f"""
        <div style="background:white; padding:30px; border-radius:15px; border-right:12px solid #003366; margin-top:20px;">
            <h1 style="color:#003366; margin:0;">{item['Project']}</h1>
            <p style="font-size:1.3rem;">المطور: <b>{item['Developer']}</b> | المالك: <b>{item['Owner']}</b></p>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📝 معلومات المطور والزتونة", "🏗️ مشاريع الشركة الأخرى"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 📊 بيانات الاستثمار")
            st.success(f"**السعر الإجمالي:** {item['Price']}")
            st.info(f"**أقل مقدم (Min Val):** {item['Min_Val']}")
            st.info(f"**نظام السداد:** مقدم {item['Down_Payment']} / تقسيط {item['Installments']} سنوات")
            st.warning(f"**تاريخ الاستلام:** {item['Delivery']}")
        with c2:
            st.markdown("### 💡 الزتونة الفنية")
            st.write(f"**عن المطور:** {item['Detailed_Info']}")
            st.markdown("---")
            st.write(f"**وصف المشروع:** {item['Description']}")
            st.write(f"**تصنيف المشروع:** {item['Type']}")

    with tab2:
        st.subheader(f"مشاريع أخرى لشركة {item['Developer']}")
        others = df[df['Developer'] == item['Developer']]
        for _, p in others.iterrows():
            if p['Project'] != item['Project']:
                st.markdown(f"- **{p['Project']}** في {p['Area']} (السعر: {p['Price']})")
