import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="BrokerEdge Pro", layout="wide")

# ستايل "ناوي"
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #f0f2f6; border-radius: 10px; padding: 10px 30px; font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #00416b !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- الهيدر الرئيسي ---
st.markdown("""
    <div style="background:#00416b; color:white; padding:20px; text-align:center; border-radius:0 0 20px 20px; margin-bottom:30px;">
        <h1 style="margin:0;">BrokerEdge | منصة البيانات الذكية</h1>
    </div>
    """, unsafe_allow_html=True)

# --- تقسيم الصفحة لتبويبات واضحة ---
tab_home, tab_admin = st.tabs(["🌐 واجهة المشاريع (للبحث)", "⚙️ لوحة التحكم (لرفع الملف)"])

# --------------------------------
# التبويب الثاني: لوحة التحكم (الرفع هنا)
# --------------------------------
with tab_admin:
    st.header("تحديث بيانات المنصة")
    st.info("ارفع ملف الإكسيل هنا ليتم تحديث المشاريع في الواجهة الرئيسية فوراً.")
    
    # مكان الرفع واضح وصريح
    admin_pass = st.text_input("أدخل كلمة السر للرفع", type="password")
    if admin_pass == "123":
        uploaded_file = st.file_uploader("اختر ملف Excel أو CSV", type=['xlsx', 'csv'])
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file, engine='openpyxl')
                st.session_state['master_data'] = df
                st.success(f"✅ تم الرفع بنجاح! تم العثور على {len(df)} مشروع.")
                st.dataframe(df.head()) # معاينة سريعة للداتا
            except Exception as e:
                st.error(f"خطأ في قراءة الملف: {e}")
    else:
        st.warning("أدخل الباسورد (123) عشان ترفع الملف.")

# --------------------------------
# التبويب الأول: واجهة المشاريع
# --------------------------------
with tab_home:
    if 'master_data' in st.session_state:
        df = st.session_state['master_data']
        
        # محرك البحث
        search = st.text_input("🔍 ابحث عن أي حاجة (اسم، مطور، منطقة)...")
        
        if search:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        
        # عرض الكروت
        cols = st.columns(3)
        for i, (idx, row) in enumerate(df.iterrows()):
            with cols[i % 3]:
                # قراءة الداتا بمرونة
                name = row.get('المشروع', 'مشروع جديد')
                price = row.get('السعر', 'اتصل بنا')
                loc = row.get('المنطقة', 'مصر')
                
                st.markdown(f"""
                    <div style="border:1px solid #ddd; padding:20px; border-radius:15px; background:white; margin-bottom:20px; box-shadow:0 4px 10px rgba(0,0,0,0.05);">
                        <h3 style="color:#00416b; margin-top:0;">{name}</h3>
                        <p style="color:#ed1c24; font-weight:bold;">📍 {loc}</p>
                        <hr>
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:18px; font-weight:bold;">{price}</span>
                            <a href="https://wa.me/?text=تفاصيل {name}" target="_blank" style="background:#25D366; color:white; padding:5px 15px; border-radius:8px; text-decoration:none;">واتساب</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align:center; padding:50px;'><h3>⚠️ لا توجد بيانات حالياً</h3><p>روح لتبويب 'لوحة التحكم' وارفع الملف الأول.</p></div>", unsafe_allow_html=True)
