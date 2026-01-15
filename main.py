import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="BrokerEdge Pro", layout="wide")

# 1. نظام التبويبات
tab1, tab2 = st.tabs(["🌐 واجهة البروكر (المعاينة)", "⚙️ إدارة الداتا"])

with tab2:
    st.header("تحديث البيانات")
    uploaded_file = st.file_uploader("ارفع ملف الإكسيل هنا", type=['xlsx'])
    
    if uploaded_file:
        try:
            # قراءة الملف واستخدام أول صف كعناوين
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            # تنظيف البيانات من أي صفوف فاضية
            df = df.dropna(how='all') 
            st.session_state['master_data'] = df
            st.success(f"✅ مبروك! تم قراءة {len(df)} مشروع بنجاح.")
            st.dataframe(df.head(3)) # وريني شكل الداتا
        except Exception as e:
            st.error(f"فيه مشكلة في الملف: {e}")

with tab1:
    if 'master_data' in st.session_state:
        df = st.session_state['master_data']
        
        # --- منطقة البحث الذكي ---
        st.markdown('<h2 style="text-align:right;">🔍 ابحث في مشاريع مصر</h2>', unsafe_allow_html=True)
        search = st.text_input("", placeholder="اكتب اسم المطور أو المنطقة هنا...")

        # --- تحويل الداتا لكروت تفاعلية ---
        st.markdown("---")
        cols = st.columns(3) # عرض 3 كروت في الصف
        
        # فلترة الداتا بناءً على البحث
        mask = df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
        filtered_df = df[mask]

        for index, row in filtered_df.iterrows():
            with cols[index % 3]:
                # هنا بنحاول نخمن أسامي الأعمدة عندك في الإكسيل
                name = row.get('المشروع', row.iloc[0]) # لو ملقاش 'المشروع' هياخد أول عمود
                dev = row.get('المطور', 'مطور غير مسجل')
                price = row.get('السعر', 'اتصل للتفاصيل')
                area = row.get('المنطقة', 'موقع مميز')

                # تصميم الكارت
                st.markdown(f"""
                <div dir="rtl" style="background: white; border-radius: 15px; padding: 20px; border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 20px; transition: 0.3s;">
                    <div style="color: #3b82f6; font-size: 12px; font-weight: bold; margin-bottom: 5px;">📍 {area}</div>
                    <h3 style="margin: 0; color: #1e293b; font-size: 20px;">{name}</h3>
                    <p style="color: #64748b; font-size: 14px; margin: 10px 0;">المطور: <b>{dev}</b></p>
                    <div style="background: #f8fafc; padding: 10px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #1e3a8a; font-weight: bold;">{price}</span>
                        <button style="background: #1e3a8a; color: white; border: none; padding: 5px 10px; border-radius: 5px; font-size: 12px; cursor: pointer;">التفاصيل</button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # إضافة تفاعل بسيط (زرار حقيقي من ستريمليت)
                if st.button(f"احجز وحدة في {name}", key=f"btn_{index}"):
                    st.balloons() # حركة احتفالية لما يدوس
                    st.success(f"تم تسجيل اهتمامك بمشروع {name}. سيتم التواصل معك!")
    else:
        st.warning("⚠️ يا صديقي، روح لتبويب 'إدارة الداتا' وارفع الملف الأول عشان الكروت تظهر هنا.")
