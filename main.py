import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# إعدادات الصفحة
st.set_page_config(page_title="منصة المستشار العقاري", layout="wide")

# 1. ربط بيانات شيت جوجل (Google Sheets)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pubhtml"

@st.cache_data
def load_data():
    # ملاحظة: سنستخدم القراءة من الرابط وتحويلها لـ DataFrame
    # لمحاكاة الربط المباشر، يفضل دائما استخدام رابط الـ CSV المباشر من الشيت
    try:
        df = pd.read_html(SHEET_URL, header=1)[0]
        # تنظيف البيانات (إزالة الأعمدة غير الضرورية)
        df = df.iloc[:, 1:] 
        return df
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")
        return pd.DataFrame()

df = load_data()

# 2. تصميم الواجهة الجانبية (فلاتر البحث القوية)
st.sidebar.header("🔍 فلاتر البحث الدقيقة")

if not df.empty:
    # فلتر المنطقة
    area_list = df['Area'].unique().tolist() if 'Area' in df.columns else []
    selected_area = st.sidebar.multiselect("اختر المنطقة", options=area_list)

    # فلتر نوع المطور
    type_list = df['Type'].unique().tolist() if 'Type' in df.columns else []
    selected_type = st.sidebar.multiselect("نوع المشروع", options=type_list)

    # فلتر الميزانية (Min_Val)
    if 'Min_Val' in df.columns:
        # تحويل القيم لأرقام لتفعيل السلايدر
        df['Min_Val_Clean'] = pd.to_numeric(df['Min_Val'].astype(str).str.replace(r'[^0-9]', '', regex=True))
        max_budget = int(df['Min_Val_Clean'].max())
        budget_range = st.sidebar.slider("الميزانية (مقدم يبدأ من)", 0, max_budget, (0, max_budget))

    # تطبيق الفلاتر
    filtered_df = df.copy()
    if selected_area:
        filtered_df = filtered_df[filtered_df['Area'].isin(selected_area)]
    if selected_type:
        filtered_df = filtered_df[filtered_df['Type'].isin(selected_type)]
    if 'Min_Val' in df.columns:
        filtered_df = filtered_df[(filtered_df['Min_Val_Clean'] >= budget_range[0]) & (filtered_df['Min_Val_Clean'] <= budget_range[1])]

# 3. قسم حاسبة الأقساط والعائد (الأدوات)
st.title("🏗️ منصة معلومات العقارات الذكية")

col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("🛠️ أدوات البروكر")
    
    # كود HTML للحاسبات
    calc_html = """
    <div dir="rtl" style="font-family: sans-serif; background: #f4f4f9; padding: 15px; border-radius: 10px;">
        <div style="margin-bottom: 20px; border-bottom: 1px solid #ccc; padding-bottom: 10px;">
            <h4>💰 حاسبة القسط</h4>
            <input type="number" id="p" placeholder="سعر الوحدة" style="width:100%; margin:5px 0;">
            <input type="number" id="d" placeholder="المقدم %" style="width:100%; margin:5px 0;">
            <input type="number" id="y" placeholder="السنوات" style="width:100%; margin:5px 0;">
            <button onclick="c1()" style="width:100%; background:#27ae60; color:#fff; border:none; padding:8px; border-radius:5px;">احسب القسط</button>
            <p id="r1" style="color:#27ae60; font-weight:bold; margin-top:10px;"></p>
        </div>
        <div>
            <h4>📈 حاسبة العائد (ROI)</h4>
            <input type="number" id="bp" placeholder="سعر الشراء" style="width:100%; margin:5px 0;">
            <input type="number" id="rt" placeholder="الإيجار الشهري" style="width:100%; margin:5px 0;">
            <button onclick="c2()" style="width:100%; background:#2980b9; color:#fff; border:none; padding:8px; border-radius:5px;">احسب العائد</button>
            <p id="r2" style="color:#2980b9; font-weight:bold; margin-top:10px;"></p>
        </div>
    </div>
    <script>
    function c1(){
        let p=document.getElementById('p').value;
        let d=document.getElementById('d').value;
        let y=document.getElementById('y').value;
        let res = (p - (p*(d/100))) / (y*12);
        document.getElementById('r1').innerText = "القسط: " + Math.round(res).toLocaleString() + " ج.م";
    }
    function c2(){
        let p=document.getElementById('bp').value;
        let r=document.getElementById('rt').value;
        let res = ((r*12)/p)*100;
        document.getElementById('r2').innerText = "العائد السنوي: " + res.toFixed(2) + "%";
    }
    </script>
    """
    components.html(calc_html, height=500)

with col1:
    st.subheader("📊 المطورين المتاحين بناءً على بحثك")
    if not filtered_df.empty:
        # عرض البيانات بشكل كروت أو جدول
        st.dataframe(filtered_df[['Developer', 'Owner', 'Area', 'Price', 'Type', 'Delivery']], use_container_width=True)
        
        # ميزة إضافية: عند الضغط على مطور تظهر تفاصيله
        selected_dev = st.selectbox("اختر مطور لعرض التفاصيل الكاملة", options=filtered_df['Developer'].unique())
        dev_info = filtered_df[filtered_df['Developer'] == selected_dev].iloc[0]
        
        with st.expander(f"ℹ️ تفاصيل {selected_dev}"):
            st.write(f"**المالك:** {dev_info['Owner']}")
            st.write(f"**الوصف:** {dev_info.get('Description', 'لا يوجد وصف')}")
            st.write(f"**أنظمة السداد:** {dev_info.get('Installments', 'غير محدد')}")
    else:
        st.warning("لا توجد نتائج تطابق هذه الفلاتر.")
