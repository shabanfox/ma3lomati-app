import streamlit as st
import pandas as pd
import urllib.parse

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide")

# 2. رابط البيانات
PROJECTS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"

@st.cache_data(ttl=5)
def load_and_clean_data():
    try:
        df = pd.read_csv(PROJECTS_URL).fillna("---")
        # تنظيف أسماء الأعمدة من أي مسافات مخفية يمين أو شمال
        df.columns = df.columns.str.strip()
        # حذف التكرار
        if 'Project Name' in df.columns:
            df = df.drop_duplicates(subset=['Project Name'], keep='first')
        return df
    except Exception as e:
        st.error(f"خطأ في التحميل: {e}")
        return pd.DataFrame()

df = load_and_clean_data()

# 3. التنسيق
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo&display=swap');
    body, .stApp { background-color: #0e1117; font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; color: white; }
    .main-card { background: #1a1c24; border-right: 6px solid #f59e0b; padding: 20px; border-radius: 15px; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# 4. واجهة المستخدم
st.title("🤖 المساعد الذكي | إدارة مشاريع التجمع")

if not df.empty:
    st.write(f"مرحباً بك.. لديك الآن **{len(df)}** مشروعاً جاهزاً.")
    
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1: search_q = st.text_input("🔍 بحث باسم المشروع أو المطور")
    with col_f2: 
        s_types = ["الكل"] + sorted(df['Sales Type'].unique().tolist()) if 'Sales Type' in df.columns else ["الكل"]
        selected_sale = st.selectbox("💰 نوع البيع", s_types)
    with col_f3:
        f_types = ["الكل"] + sorted(df['Finishing Status'].unique().tolist()) if 'Finishing Status' in df.columns else ["الكل"]
        selected_finish = st.selectbox("🏗️ التشطيب", f_types)
    with col_f4: client_phone = st.text_input("📞 واتساب العميل")

    # تصفية البيانات (Logic)
    filtered_df = df.copy()
    if search_q:
        filtered_df = filtered_df[filtered_df.apply(lambda row: row.astype(str).str.contains(search_q, case=False).any(), axis=1)]
    if selected_sale != "الكل":
        filtered_df = filtered_df[filtered_df['Sales Type'] == selected_sale]
    if selected_finish != "الكل":
        filtered_df = filtered_df[filtered_df['Finishing Status'] == selected_finish]

    # 5. عرض الكروت (مع حماية ضد الـ KeyError)
    for _, row in filtered_df.iterrows():
        # استخدام .get() بدلاً من القوسين [] يمنع الـ Error لو العمود مش موجود
        p_name = row.get('Project Name', 'غير مسجل')
        dev = row.get('Developer', 'غير مسجل')
        owner = row.get('Owner', 'غير مسجل')
        loc = row.get('Location', 'غير مسجل')
        price = row.get('Starting Price (EGP)', 'اتصل للتفاصيل')
        units = row.get('Available Units (Types)', '---')
        finish = row.get('Finishing Status', '---')
        s_type = row.get('Sales Type', '---')
        payment = row.get('Payment Plan', '---')
        nawy_link = row.get('Nawy Link', '#')

        st.markdown(f"""
        <div class="main-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h2 style="color:#f59e0b; margin:0;">🏢 {p_name}</h2>
                <span style="background:#333; padding:5px 10px; border-radius:5px; font-size:12px;">{s_type}</span>
            </div>
            <p style="color:#aaa; margin:10px 0;">المطور: <b>{dev}</b> | المالك: {owner}</p>
            <p>📍 الموقع: {loc}</p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; background:#25272e; padding:10px; border-radius:10px;">
                <div>🏠 وحدات: {units}</div>
                <div>🏗️ تشطيب: {finish}</div>
                <div style="color:#10b981; font-weight:bold;">💰 {price}</div>
                <div>💳 سداد: {payment}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # أزرار
        c1, c2 = st.columns([1, 4])
        with c1:
            msg = f"تفاصيل {p_name}:\n📍 الموقع: {loc}\n💰 السعر: {price}\n🏗️ التشطيب: {finish}\n💳 السداد: {payment}"
            st.link_button("🚀 إرسال واتساب", f"https://wa.me/{client_phone}?text={urllib.parse.quote(msg)}")
        with c2:
            if nawy_link != "#":
                st.link_button("🔗 فتح في Nawy", nawy_link)
else:
    st.warning("لم يتم العثور على بيانات، تأكد من أن الشيت يحتوي على الأعمدة المطلوبة.")
