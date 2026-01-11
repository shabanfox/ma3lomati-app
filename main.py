import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتنسيق
st.set_page_config(page_title="Ma3lomati PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
        background-color: #050505; color: white;
    }
    /* تنسيق أزرار الملاحة */
    .stButton > button {
        width: 100%; border-radius: 10px; height: 50px; font-weight: bold; font-size: 18px;
        background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #f59e0b !important;
    }
    .stButton > button:hover { background-color: #f59e0b !important; color: black !important; }
    
    /* كروت العرض */
    .data-card {
        background: #111; border: 1px solid #222; border-right: 5px solid #f59e0b;
        border-radius: 12px; padding: 20px; margin-bottom: 20px;
    }
    .price-tag { background: #f59e0b; color: black; padding: 5px 10px; border-radius: 5px; font-weight: 900; }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات وتنظيفها
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip() # تنظيف المسافات من أسماء الأعمدة
    return df

try:
    df = load_data()
except:
    st.error("خطأ في الاتصال بقاعدة البيانات")
    st.stop()

# 3. نظام الأزرار العلوي (Navigation)
if 'page' not in st.session_state:
    st.session_state.page = 'projects'

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏗️ مشاريع"): st.session_state.page = 'projects'
with col2:
    if st.button("🏢 مطورين"): st.session_state.page = 'developers'
with col3:
    if st.button("🛠️ أدوات"): st.session_state.page = 'tools'

st.markdown("---")

# --- قسم المشاريع ---
if st.session_state.page == 'projects':
    st.header("🏢 دليل المشاريع العقارية")
    search = st.text_input("🔍 ابحث عن اسم المشروع أو المنطقة...")
    
    # تصفية البيانات (بفرض أن العمود اسمه Projects أو نستخدم صفوف الجدول)
    dff = df.copy()
    if search:
        dff = dff[dff.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
        
    for _, row in dff.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="data-card">
                <div style="display:flex; justify-content:space-between;">
                    <h3 style="color:#f59e0b; margin:0;">{row.get('Projects', 'اسم المشروع')}</h3>
                    <span class="price-tag">{row.get('Min_Val (Start Price)', '-')}</span>
                </div>
                <p>📍 المنطقة: {row.get('Area', '-')}</p>
                <p>🏠 النوع: {row.get('Type', '-')}</p>
                <div style="background:#1a1a1a; padding:10px; border-radius:5px; margin-top:10px;">
                    <b>🌟 الميزة التنافسية:</b> {row.get('Description', '-')}
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- قسم المطورين ---
elif st.session_state.page == 'developers':
    st.header("👨‍💻 سجل المطورين العقاريين")
    dev_search = st.text_input("🔍 ابحث عن اسم المطور...")
    
    dff = df.copy()
    if dev_search:
        dff = dff[dff['Developer'].str.contains(dev_search, na=False, case=False)]
        
    for _, row in dff.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="data-card">
                <h3 style="color:#f59e0b; margin:0;">{row.get('Developer', 'اسم المطور')}</h3>
                <p>👤 المالك: {row.get('Owner', '-')}</p>
                <p>📝 سابقة الأعمال: {row.get('Detailed_Info', 'لا توجد تفاصيل')}</p>
            </div>
            """, unsafe_allow_html=True)

# --- قسم الأدوات ---
elif st.session_state.page == 'tools':
    st.header("🛠️ أدوات البروكر المحترف")
    
    tool_type = st.radio("اختر الأداة:", ["حاسبة الأقساط", "مولد رسائل واتساب"])
    
    if tool_type == "حاسبة الأقساط":
        price = st.number_input("سعر الوحدة", min_value=0)
        down_payment = st.number_input("المقدم", min_value=0)
        years = st.slider("سنوات التقسيط", 1, 15, 7)
        if price > 0:
            monthly = (price - down_payment) / (years * 12)
            st.success(f"القسط الشهري التقريبي: {monthly:,.0f} ج.م")
            
    elif tool_type == "مولد رسائل واتساب":
        st.info("اختر مشروعاً من صفحة المشاريع لإنشاء رسالة تلقائية (ميزة قيد البرمجة)")
