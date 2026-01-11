import streamlit as st
import pandas as pd

# 1. إعدادات أساسية
st.set_page_config(page_title="معلوماتي العقارية PRO", layout="wide")

# 2. لمسة التصميم (فقط للألوان والخطوط بدون تعقيد HTML)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }
    .stMetric { background: #1a1a1a; padding: 15px; border-radius: 10px; border-right: 4px solid #f59e0b; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات (مع معالجة فورية للأخطاء)
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip() # تنظيف أسماء الأعمدة
    return data

try:
    df = load_data()
except Exception as e:
    st.error("فيه مشكلة في سحب الداتا من جوجل شيت.. تأكد إن الرابط منشور (Published)")
    st.stop()

# 4. الملاحة (أزرار واضحة)
st.title("📊 منصة معلوماتي العقارية")
tab_projects, tab_devs, tab_tools = st.tabs(["🏗️ المشاريع", "🏢 المطورين", "🛠️ الأدوات"])

# --- صفحة المشاريع ---
with tab_projects:
    col_search, col_area = st.columns([3, 1])
    with col_search:
        search = st.text_input("🔍 ابحث عن أي كلمة (مشروع، ميزة، استشاري...)", "")
    with col_area:
        areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
        sel_area = st.selectbox("📍 تصفية بالمنطقة", areas)

    # تصفية الداتا
    dff = df.copy()
    if search:
        dff = dff[dff.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if sel_area != "الكل":
        dff = dff[dff['Area'] == sel_area]

    st.info(f"تم العثور على {len(dff)} نتيجة")

    # عرض المشاريع (استخدام Expander لعرض تفاصيل كل مشروع)
    for _, row in dff.iterrows():
        with st.container():
            # السطر الأول: اسم المطور والمشروع
            st.subheader(f"🏢 {row.get('Developer', 'مطور')} | {row.get('Projects', 'مشروع')}")
            
            # السطر الثاني: أهم 4 معلومات (Metrics)
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("💰 السعر", row.get('Min_Val (Start Price)', '-'))
            m2.metric("📍 المنطقة", row.get('Area', '-'))
            m3.metric("💵 المقدم", row.get('Down_Payment', '-'))
            m4.metric("⏳ التقسيط", row.get('Installments', '-'))
            
            # السطر الثالث: التفاصيل الإضافية
            with st.expander("👁️ تفاصيل الميزة التنافسية والاستشاري"):
                st.write(f"**🌟 الميزة:** {row.get('Description', '-')}")
                st.write(f"**🏠 النوع:** {row.get('Type', '-')}")
                st.write(f"**📅 التسليم:** {row.get('Delivery', '-')}")
                st.write(f"**👷 الاستشاري:** {row.get('Consultant', 'غير مسجل')}")
            st.divider()

# --- صفحة المطورين ---
with tab_devs:
    st.header("👨‍💼 سجل المطورين")
    # عرض جدول منظم فيه كل المطورين وسوابق أعمالهم
    dev_display = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates()
    st.table(dev_display)

# --- صفحة الأدوات ---
with tab_tools:
    st.header("🛠️ أدوات مساعدة")
    tool = st.selectbox("اختر الأداة", ["حاسبة الأقساط", "تجهيز رسالة واتساب"])
    
    if tool == "حاسبة الأقساط":
        p = st.number_input("إجمالي المبلغ", value=1000000)
        d = st.number_input("المقدم", value=100000)
        y = st.slider("السنوات", 1, 15, 7)
        st.write(f"### القسط الشهري: {(p-d)/(y*12):,.0f} ج.م")
