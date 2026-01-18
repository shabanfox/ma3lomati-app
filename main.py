import streamlit as st
import pandas as pd
import urllib.parse

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide")

# 2. الروابط المباشرة (تأكد أن الملف "Public" على الإنترنت)
# جربنا هنا الرابط العام للملف مع تحديد الصيغة فقط
u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"

# 3. وظيفة جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    try:
        # سنحاول جلب الورقة الأولى (المشاريع)
        all_data = pd.read_csv(u_p).fillna("---")
        all_data.columns = all_data.columns.str.strip()
        
        # إذا كان شيت المطورين في ورقة ثانية، يفضل حالياً (للتجربة) 
        # وضع المطورين في شيت منفصل تماماً أو التأكد من رابط الـ GID
        # حالياً سنعتبر df_d هي نفسها لضمان عمل الكود
        return all_data, all_data 
    except Exception as e:
        st.error(f"⚠️ مشكلة في الاتصال بجوجل شيت: {e}")
        return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# --- التنسيق وواجهة المستخدم ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    .dev-box { background: #111; border: 1px solid #333; padding: 20px; border-radius: 15px; border-right: 5px solid #f59e0b; margin-bottom: 15px; color: white; }
    .stButton button { width: 100%; border-radius: 10px !important; background-color: #f59e0b !important; color: black !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# 4. إدارة الحالة
if 'view_dev' not in st.session_state: st.session_state.view_dev = None

# 5. عرض البيانات
if st.session_state.view_dev is None:
    st.title("🏗️ دليل المطورين")
    
    if not df_d.empty:
        # عرض المطورين (استناداً لعمود Developer في الشيت)
        if 'Developer' in df_d.columns:
            search = st.text_input("🔍 ابحث عن مطور...")
            unique_devs = df_d[df_d['Developer'].str.contains(search, case=False, na=False)]
            
            for i, row in unique_devs.head(20).iterrows():
                with st.container():
                    st.markdown(f"""<div class="dev-box">
                        <h3>{row['Developer']}</h3>
                        <p>📍 الموقع الأساسي: {row.get('Location', '---')}</p>
                    </div>""", unsafe_allow_html=True)
                    if st.button(f"عرض الملف الكامل لـ {row['Developer']}", key=f"btn_{i}"):
                        st.session_state.view_dev = row.to_dict()
                        st.rerun()
        else:
            st.error("❌ لم يتم العثور على عمود باسم 'Developer' في الشيت. تأكد من تسمية الرأس في جوجل شيت.")
else:
    # صفحة التفاصيل
    dev = st.session_state.view_dev
    if st.button("⬅️ عودة"):
        st.session_state.view_dev = None
        st.rerun()
    
    st.header(f"🏗️ {dev['Developer']}")
    st.info(f"معلومات الشركة: {dev.get('USP', 'مطور عقاري رائد')}")
