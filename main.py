import streamlit as st
import pandas as pd

# 1. إعدادات المتصفح
st.set_page_config(page_title="معلوماتي العقارية PRO", layout="wide")

# 2. تصميم الواجهة (CSS المبسط لضمان عدم تداخل الأكواد)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
        background-color: #0e1117; color: white;
    }
    .stButton>button { width: 100%; background-color: #f59e0b !important; color: black !important; font-weight: bold; }
    .project-header { border-right: 5px solid #f59e0b; padding-right: 15px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات وتنظيفها (تنظيف شامل)
@st.cache_data
def load_and_clean_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    df = pd.read_csv(url)
    # تنظيف أسماء الأعمدة من أي مسافات أو حروف غريبة
    df.columns = df.columns.str.strip()
    return df

df = load_and_clean_data()

# 4. الملاحة بالأزرار (Navigation)
if 'menu' not in st.session_state:
    st.session_state.menu = "🏗️ المشاريع"

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏗️ المشاريع"): st.session_state.menu = "🏗️ المشاريع"
with col2:
    if st.button("🏢 المطورين"): st.session_state.menu = "🏢 المطورين"
with col3:
    if st.button("🛠️ الأدوات"): st.session_state.menu = "🛠️ الأدوات"

st.divider()

# --- صفحة المشاريع ---
if st.session_state.menu == "🏗️ المشاريع":
    st.title("🏗️ دليل المشاريع")
    
    # فلاتر البحث
    f_col1, f_col2 = st.columns([3, 1])
    with f_col1:
        query = st.text_input("🔍 ابحث (اسم المشروع، المطور، الميزة...)", "")
    with f_col2:
        area_filter = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df['Area'].dropna().unique().tolist()))

    # منطق الفلترة
    dff = df.copy()
    if query:
        mask = dff.apply(lambda row: query.lower() in row.astype(str).str.lower().values, axis=1)
        dff = dff[mask]
    if area_filter != "الكل":
        dff = dff[dff['Area'] == area_filter]

    # عرض البيانات باستخدام Container لتجنب أخطاء HTML
    for _, row in dff.iterrows():
        with st.container():
            st.markdown(f"### {row.get('Projects', 'غير مسجل')}")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("💰 يبدأ من", row.get('Min_Val (Start Price)', '-'))
            c2.metric("📍 المنطقة", row.get('Area', '-'))
            c3.metric("💵 المقدم", row.get('Down_Payment', '-'))
            c4.metric("⏳ التقسيط", row.get('Installments', '-'))
            
            with st.expander("🔍 الميزة التنافسية وتفاصيل المشروع"):
                st.write(f"**🏠 النوع:** {row.get('Type', '-')}")
                st.write(f"**📅 التسليم:** {row.get('Delivery', '-')}")
                st.write(f"**🌟 الميزة:** {row.get('Description', '-')}")
                st.info(f"المطور: {row.get('Developer', '-')}")
            st.divider()

# --- صفحة المطورين ---
elif st.session_state.menu == "🏢 المطورين":
    st.title("🏢 سجل المطورين")
    dev_query = st.text_input("🔍 ابحث عن مطور...")
    
    # عرض فريد للمطورين
    dev_df = df.drop_duplicates(subset=['Developer']).copy()
    if dev_query:
        dev_df = dev_df[dev_df['Developer'].str.contains(dev_query, na=False, case=False)]

    for _, row in dev_df.iterrows():
        with st.expander(f"🏢 {row.get('Developer', 'اسم المطور')}"):
            st.subheader(f"المالك: {row.get('Owner', '-')}")
            st.write("**سابقة الأعمال والتفاصيل:**")
            st.write(row.get('Detailed_Info', 'لا توجد تفاصيل إضافية'))

# --- صفحة الأدوات ---
elif st.session_state.menu == "🛠️ الأدوات":
    st.title("🛠️ أدوات البروكر")
    
    tab1, tab2 = st.tabs(["💰 حاسبة القسط", "📱 عروض الواتساب"])
    
    with tab1:
        price = st.number_input("إجمالي السعر", value=1000000)
        dp = st.number_input("المقدم المدفوع", value=100000)
        years = st.slider("عدد السنوات", 1, 15, 7)
        if price > dp:
            monthly = (price - dp) / (years * 12)
            st.metric("القسط الشهري المتوقع", f"{monthly:,.0f} ج.م")

    with tab2:
        target_p = st.selectbox("اختر المشروع لتجهيز الرسالة", df['Projects'].dropna().unique())
        p_row = df[df['Projects'] == target_p].iloc[0]
        msg = f"🏢 *عرض مشروع: {target_p}*\n📍 المنطقة: {p_row['Area']}\n💰 المقدم: {p_row['Down_Payment']}\n⏳ التقسيط: {p_row['Installments']}\n🌟 الميزة: {p_row['Description']}"
        st.text_area("رسالة الواتساب الجاهزة:", msg, height=150)
