import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# إعدادات الصفحة
st.set_page_config(page_title="BrokerEdge Admin", layout="wide")

# 1. نظام التبويبات (Tabs) لراحة المستخدم
tab1, tab2 = st.tabs(["🌐 واجهة البروكر", "⚙️ إدارة البيانات (الخلفية)"])

# ---------------------------------------------------------
# Tab 2: إدارة البيانات (دي ليك أنت)
# ---------------------------------------------------------
with tab2:
    st.header("تحديث بيانات المنصة")
    st.info("ارفع ملف الإكسيل اللي سحبته من Nawy أو أي مصدر آخر هنا.")
    
    uploaded_file = st.file_uploader("اختر ملف Excel أو CSV", type=['xlsx', 'csv'])
    
    if uploaded_file:
        # قراءة البيانات
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success("تم تحميل البيانات بنجاح!")
        st.write("معاينة البيانات المرفوعة:")
        st.dataframe(df.head()) # عرض أول 5 سطور للتأكد
        
        # حفظ البيانات في "الجلسة" عشان تظهر في التبويب التاني
        st.session_state['master_data'] = df

# ---------------------------------------------------------
# Tab 1: واجهة البروكر (اللي البروكر بيشوفها)
# ---------------------------------------------------------
with tab1:
    # الهيدر الاحترافي
    header_html = """
    <div dir="rtl" style="background: #0f172a; padding: 30px; border-radius: 20px; text-align: center; color: white;">
        <h1 style="margin: 0; font-size: 28px;">BrokerEdge <span style="color: #3b82f6;">Pro</span></h1>
        <p style="opacity: 0.8;">محرك البحث العقاري الأقوى للبروكر المصري</p>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    # التحقق من وجود بيانات
    if 'master_data' in st.session_state:
        data = st.session_state['master_data']
        
        # فلاتر البحث
        st.markdown("### 🔍 ابحث في السوق")
        col_s1, col_s2 = st.columns([3, 1])
        with col_s1:
            search = st.text_input("ابحث باسم المشروع أو المطور...")
        with col_s2:
            region = st.selectbox("تصفية بالمنطقة", ["الكل"] + list(data['المنطقة'].unique() if 'المنطقة' in data.columns else []))

        # عرض البيانات بنظام الكروت (Cards)
        st.markdown("---")
        
        # تحويل البيانات لكروت
        cols = st.columns(3)
        for index, row in data.iterrows():
            # البحث والتصفية
            if search.lower() in str(row).lower():
                with cols[index % 3]:
                    # تصميم كارت احترافي لكل سطر في الإكسيل
                    st.markdown(f"""
                    <div dir="rtl" style="background: white; border: 1px solid #e2e8f0; border-radius: 15px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                        <h4 style="color: #1e3a8a; margin: 0;">{row.get('المشروع', 'اسم المشروع')}</h4>
                        <p style="color: #64748b; font-size: 14px; margin: 10px 0;">المطور: {row.get('المطور', 'غير معروف')}</p>
                        <hr style="border: 0; border-top: 1px solid #f1f5f9; margin: 15px 0;">
                        <div style="display: flex; justify-content: space-between;">
                            <span style="font-weight: bold; color: #059669;">السعر: {row.get('السعر', 'اتصل بنا')}</span>
                            <span style="font-size: 12px; background: #f1f5f9; padding: 2px 8px; border-radius: 5px;">{row.get('المنطقة', 'مصر')}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ لا توجد بيانات حالياً. يرجى الذهاب لتبويب 'إدارة البيانات' ورفع ملف الإكسيل أولاً.")
