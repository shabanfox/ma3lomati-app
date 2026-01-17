import streamlit as st
import pandas as pd
import urllib.parse

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="MA3LOMATI PRO | التجمع الخامس", layout="wide")

# 2. روابط البيانات (CSV)
# ملاحظة: قمت بتحويل روابط pubhtml إلى روابط CSV ليتمكن الكود من قراءتها
PROJECTS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"

@st.cache_data(ttl=10)
def load_and_merge_data():
    try:
        # قراءة البيانات
        df = pd.read_csv(PROJECTS_URL).fillna("---")
        # تنظيف أسماء الأعمدة من أي مسافات
        df.columns = df.columns.str.strip()
        # منع تكرار المشاريع (بناءً على اسم المشروع)
        df = df.drop_duplicates(subset=['Project Name'], keep='first')
        return df
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")
        return pd.DataFrame()

df = load_and_merge_data()

# 3. التنسيق الجمالي (CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    body, .stApp { background-color: #0e1117; font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; color: white; }
    .main-card { background: #1a1c24; border: 1px solid #333; padding: 20px; border-radius: 15px; border-right: 6px solid #f59e0b; margin-bottom: 15px; }
    .tag { background: #2d2d3a; padding: 4px 10px; border-radius: 6px; font-size: 12px; color: #f59e0b; margin-left: 5px; border: 1px solid #444; }
    .price-style { color: #10b981; font-weight: bold; font-size: 1.2em; }
</style>
""", unsafe_allow_html=True)

# 4. واجهة المساعد الذكي
st.title("🤖 المساعد الذكي | إدارة مشاريع التجمع")
st.write(f"مرحباً بك.. لديك الآن **{len(df)}** مشروعاً محدثاً ومفلطراً.")

# صف الفلاتر الذكية
col_f1, col_f2, col_f3, col_f4 = st.columns(4)

with col_f1:
    search_q = st.text_input("🔍 بحث (مشروع/مطور)", placeholder="اكتب هنا...")
with col_f2:
    # فلترة بنوع البيع (مطور / ريسيل)
    sale_types = ["الكل"] + sorted(df['Sales Type'].unique().tolist()) if 'Sales Type' in df.columns else ["الكل"]
    selected_sale = st.selectbox("💰 نوع البيع", sale_types)
with col_f3:
    # فلترة بحالة التشطيب
    finish_types = ["الكل"] + sorted(df['Finishing Status'].unique().tolist()) if 'Finishing Status' in df.columns else ["الكل"]
    selected_finish = st.selectbox("🏗️ التشطيب", finish_types)
with col_f4:
    client_phone = st.text_input("📞 واتساب العميل", placeholder="01xxxxxxxxx")

st.divider()

# 5. منطق الفلترة
filtered_df = df.copy()

if search_q:
    filtered_df = filtered_df[
        filtered_df['Project Name'].str.contains(search_q, case=False, na=False) | 
        filtered_df['Developer'].str.contains(search_q, case=False, na=False)
    ]

if selected_sale != "الكل":
    filtered_df = filtered_df[filtered_df['Sales Type'] == selected_sale]

if selected_finish != "الكل":
    filtered_df = filtered_df[filtered_df['Finishing Status'] == selected_finish]

# 6. عرض النتائج (الكروت)
if not filtered_df.empty:
    for _, row in filtered_df.iterrows():
        with st.container():
            # تصميم الكارت
            st.markdown(f"""
            <div class="main-card">
                <div style="display: flex; justify-content: space-between;">
                    <h2 style="color:#f59e0b; margin:0;">🏢 {row['Project Name']}</h2>
                    <span class="tag">{row.get('Sales Type', '---')}</span>
                </div>
                <p style="margin:5px 0; color:#aaa;">المطور: <b>{row['Developer']}</b> | المالك: {row['Owner']}</p>
                <p style="margin:5px 0;">📍 الموقع: {row['Location']}</p>
                <hr style="border-color:#333; margin:10px 0;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div>🏠 <b>الوحدات:</b> {row['Available Units (Types)']}</div>
                    <div>🏗️ <b>التشطيب:</b> {row['Finishing Status']}</div>
                    <div class="price-style">💰 {row['Starting Price (EGP)']}</div>
                    <div>💳 <b>السداد:</b> {row['Payment Plan']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # أزرار الإجراءات
            b1, b2 = st.columns([1, 4])
            with b1:
                # زر إرسال العرض
                msg = f"أهلاً بك، أرشح لك مشروع {row['Project Name']}:\n📍 الموقع: {row['Location']}\n💰 السعر: {row['Starting Price (EGP)']}\n🏠 الوحدات: {row['Available Units (Types)']}\n🏗️ التشطيب: {row['Finishing Status']}\n💳 نظام السداد: {row['Payment Plan']}"
                wa_url = f"https://wa.me/{client_phone}?text={urllib.parse.quote(msg)}"
                st.link_button("🚀 إرسال العرض", wa_url, use_container_width=True)
            with b2:
                # زر فتح المصدر
                st.link_button("🔗 تفاصيل المصدر (Nawy)", row.get('Nawy Link', '#'), use_container_width=False)
else:
    st.warning("لا توجد نتائج مطابقة لبحثك. جرب تغيير الفلاتر.")
