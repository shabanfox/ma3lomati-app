import streamlit as st
import pandas as pd
import urllib.parse
from streamlit_option_menu import option_menu

# 1. إعداد الصفحة الأساسي
st.set_page_config(page_title="MA3LOMATI PRO | منصة العقارات الشاملة", layout="wide")

# 2. روابط البيانات (تأكد أن الرابط ينتهي بـ output=csv)
DATA_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"

@st.cache_data(ttl=10)
def load_data():
    try:
        df = pd.read_csv(DATA_URL).fillna("---")
        # تنظيف العناوين من المسافات المخفية
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"حدث خطأ أثناء الاتصال بالبيانات: {e}")
        return pd.DataFrame()

df = load_data()

# 3. التنسيق الجمالي (CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; background-color: #0e1117; }
    .stApp { background-color: #0e1117; color: white; }
    .card { background: #1a1c24; border-right: 5px solid #f59e0b; padding: 20px; border-radius: 15px; margin-bottom: 20px; border: 1px solid #333; }
    .stat-box { background: #25272e; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #444; }
    .price-tag { color: #10b981; font-weight: bold; font-size: 1.1em; }
</style>
""", unsafe_allow_html=True)

# 4. القائمة الجانبية (Navigation)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/602/602175.png", width=100)
    st.title("لوحة التحكم")
    selected = option_menu(
        menu_title=None,
        options=["المساعد الذكي", "دليل المطورين", "إحصائيات السوق"],
        icons=["robot", "building", "graph-up"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#1a1c24"},
            "nav-link": {"font-size": "16px", "text-align": "right", "margin": "0px", "color": "white"},
            "nav-link-selected": {"background-color": "#f59e0b"},
        }
    )

# --- الصفحة الأولى: المساعد الذكي ---
if selected == "المساعد الذكي":
    st.title("🤖 المساعد الذكي للمشاريع")
    
    # فلاتر البحث
    col1, col2, col3, col4 = st.columns(4)
    with col1: search = st.text_input("🔍 ابحث (مشروع/مطور/منطقة)")
    with col2: 
        s_type = ["الكل"] + sorted(df['Sales Type'].unique().tolist()) if 'Sales Type' in df.columns else ["الكل"]
        sel_sale = st.selectbox("💰 نوع البيع", s_type)
    with col3:
        f_type = ["الكل"] + sorted(df['Finishing Status'].unique().tolist()) if 'Finishing Status' in df.columns else ["الكل"]
        sel_finish = st.selectbox("🏗️ التشطيب", f_type)
    with col4: phone = st.text_input("📞 واتساب العميل")

    # تصفية الداتا
    mask = df.copy()
    if search:
        mask = mask[mask.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
    if sel_sale != "الكل":
        mask = mask[mask['Sales Type'] == sel_sale]
    if sel_finish != "الكل":
        mask = mask[mask['Finishing Status'] == sel_finish]

    st.write(f"تم العثور على **{len(mask)}** نتيجة")

    # عرض الكروت
    for _, row in mask.iterrows():
        # استخدام .get لمنع الـ KeyError
        name = row.get('Project Name', '---')
        dev = row.get('Developer', '---')
        owner = row.get('Owner', '---')
        loc = row.get('Location', '---')
        price = row.get('Starting Price (EGP)', 'اتصل للتفاصيل')
        units = row.get('Available Units (Types)', '---')
        finishing = row.get('Finishing Status', '---')
        stype = row.get('Sales Type', '---')
        pay = row.get('Payment Plan', '---')
        link = row.get('Nawy Link', '#')

        st.markdown(f"""
        <div class="card">
            <div style="display: flex; justify-content: space-between;">
                <h3 style="color:#f59e0b; margin:0;">🏢 {name}</h3>
                <span style="background:#f59e0b; color:black; padding:2px 8px; border-radius:5px; font-size:12px; font-weight:bold;">{stype}</span>
            </div>
            <p style="margin:10px 0;">🏗️ <b>المطور:</b> {dev} ({owner}) | 📍 {loc}</p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; background:#0e1117; padding:15px; border-radius:10px; margin:10px 0;">
                <div>🏠 <b>الوحدات:</b> {units}</div>
                <div>🏗️ <b>التشطيب:</b> {finishing}</div>
                <div class="price-tag">💰 {price}</div>
                <div>💳 <b>السداد:</b> {pay}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns([1, 4])
        with c1:
            wa_msg = f"تفاصيل مشروع {name}:\nالموقع: {loc}\nالسعر: {price}\nالتشطيب: {finishing}\nنظام السداد: {pay}"
            st.link_button("🚀 إرسال واتساب", f"https://wa.me/{phone}?text={urllib.parse.quote(wa_msg)}")
        with c2:
            if link != "#": st.link_button("🔗 فتح صفحة المشروع", link)

# --- الصفحة الثانية: دليل المطورين ---
elif selected == "دليل المطورين":
    st.title("🏢 دليل كبار المطورين العقاريين")
    if 'Developer' in df.columns:
        dev_list = df['Developer'].unique()
        for d in dev_list:
            with st.expander(f"🏗️ شركة {d}"):
                projects = df[df['Developer'] == d]
                st.write(f"عدد المشاريع المسجلة: {len(projects)}")
                st.table(projects[['Project Name', 'Location', 'Starting Price (EGP)']])
    else:
        st.info("لا توجد بيانات مطورين متاحة حالياً.")

# --- الصفحة الثالثة: إحصائيات السوق ---
elif selected == "إحصائيات السوق":
    st.title("📊 تحليل بيانات السوق")
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("إجمالي المشاريع", len(df))
    with c2: 
        if 'Sales Type' in df.columns:
            st.metric("مشاريع المطور", len(df[df['Sales Type'] == 'مطور (Primary)']))
    with c3:
        if 'Sales Type' in df.columns:
            st.metric("مشاريع الريسيل", len(df[df['Sales Type'] == 'ريسيل (Resale)']))
    
    st.divider()
    st.subheader("📍 توزيع المشاريع حسب المنطقة")
    if 'Location' in df.columns:
        st.bar_chart(df['Location'].value_counts())
