import streamlit as st
import pandas as pd
import urllib.parse

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide")

# 2. الروابط الصحيحة (تعديل صيغة التصدير لـ CSV)
# رابط شيت المشاريع
u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=0&single=true&output=csv"
# رابط شيت المطورين (استناداً إلى اللينك الذي أرسلته)
u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=2031754026&single=true&output=csv"

# 3. وظيفة جلب البيانات مع معالجة الأخطاء
@st.cache_data(ttl=60)
def load_data():
    try:
        # جلب شيت المطورين
        d_df = pd.read_csv(u_d).fillna("---")
        # جلب شيت المشاريع
        p_df = pd.read_csv(u_p).fillna("---")
        
        # تنظيف مسافات العناوين
        d_df.columns = d_df.columns.str.strip()
        p_df.columns = p_df.columns.str.strip()
        
        return p_df, d_df
    except Exception as e:
        st.error(f"حدث خطأ في جلب البيانات: {e}")
        return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 4. إدارة حالة الصفحة (للدخول لصفحة المطور)
if 'view_dev' not in st.session_state:
    st.session_state.view_dev = None

# 5. التنسيق الجمالي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    .dev-box { background: #111; border: 1px solid #333; padding: 20px; border-radius: 15px; border-right: 5px solid #f59e0b; margin-bottom: 15px; color: white; }
    .stButton button { width: 100%; border-radius: 10px !important; font-family: 'Cairo' !important; }
    h1, h2, h3 { color: #f59e0b !important; }
    </style>
""", unsafe_allow_html=True)

# 6. منطق العرض
if st.session_state.view_dev is None:
    st.title("🏗️ دليل المطورين العقاريين")
    
    if df_d.empty:
        st.warning("جاري تحميل البيانات أو الرابط يحتاج لمراجعة...")
    else:
        # البحث
        search = st.text_input("🔍 ابحث عن مطور (مثلاً: Sodic, Emaar...)", placeholder="اكتب اسم الشركة هنا...")
        
        # فلترة النتائج بناءً على البحث
        mask = df_d['Developer'].str.contains(search, case=False, na=False)
        filtered_df = df_d[mask]
        
        # عرض المطورين في مربعات
        for i, row in filtered_df.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="dev-box">
                    <div style="display:flex; justify-content:space-between;">
                        <span style="font-size:20px; font-weight:bold;">{row['Developer']}</span>
                        <span style="background:#f59e0b; color:black; padding:0 10px; border-radius:5px;">{row.get('Category', 'A')}</span>
                    </div>
                    <p style="margin: 10px 0; color:#aaa;">👤 الإدارة: {row.get('Owner / CEO', '---')}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"تفاصيل شركة {row['Developer']} 📖", key=f"btn_{i}"):
                    st.session_state.view_dev = row.to_dict()
                    st.rerun()

else:
    # --- صفحة المطور التفصيلية ---
    dev = st.session_state.view_dev
    if st.button("⬅️ العودة للقائمة الرئيسية"):
        st.session_state.view_dev = None
        st.rerun()
    
    st.markdown(f"""
    <div style="background:#111; padding:30px; border-radius:20px; border-right:10px solid #f59e0b; color:white;">
        <h1>{dev['Developer']}</h1>
        <p style="font-size:20px;">📅 سنة التأسيس: {dev.get('Establishment', '---')}</p>
        <p style="font-size:20px;">👤 رئيس مجلس الإدارة: {dev.get('Owner / CEO', '---')}</p>
        <hr>
        <h3>🌟 نقاط القوة (USP):</h3>
        <p style="font-size:18px; line-height:1.6; color:#ddd;">{dev.get('USP', 'لا توجد تفاصيل مسجلة.')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # ربط المشاريع
    st.write("---")
    st.subheader(f"📂 مشاريع {dev['Developer']} المسجلة")
    
    if not df_p.empty:
        # البحث في شيت المشاريع عن اسم المطور
        rel_projs = df_p[df_p['Developer'].str.contains(dev['Developer'], case=False, na=False)]
        
        if not rel_projs.empty:
            for _, p in rel_projs.iterrows():
                with st.expander(f"🏢 {p['ProjectName']} - {p.get('Location', '---')}"):
                    st.write(f"💳 **نظام السداد:** {p.get('Payment Plan', 'تواصل للتفاصيل')}")
                    st.markdown(f"**[📲 إرسال المقترح للعميل](https://wa.me/?text={urllib.parse.quote('أرشح لك مشروع ' + str(p['ProjectName']) + ' من شركة ' + str(dev['Developer']))})**")
        else:
            st.info("لا توجد مشاريع مضافة لهذا المطور في شيت المشاريع حالياً.")
