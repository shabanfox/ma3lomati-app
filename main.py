import streamlit as st
import pandas as pd

# 1. الإعدادات الأساسية
st.set_page_config(page_title="الموسوعة العقارية", layout="wide")

# 2. كود التصميم (CSS) الموحد
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
    }
    .main-card { 
        background-color: white; border-radius: 10px; padding: 15px; 
        margin-bottom: 10px; border-right: 5px solid #003366;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .info-badge {
        background-color: #f1f5f9; color: #003366; padding: 2px 8px; 
        border-radius: 5px; font-size: 0.8rem; margin-left: 5px; font-weight: bold;
    }
    div.stButton > button {
        background-color: #003366 !important; color: white !important;
        border-radius: 8px !important; width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة الجلسة (عشان الأخطاء اللي ظهرت لك)
if 'page' not in st.session_state:
    st.session_state.page = 'main'

# 4. تحميل البيانات
@st.cache_data
def load_data():
    csv_url = "رابط_شيت_جوجل_هنا"
    try:
        df = pd.read_csv(csv_url)
        return df
    except:
        return pd.DataFrame([{"Developer": "انتظر ربط الشيت", "Area": "-", "Price": "-", "Detailed_Info": "لا توجد بيانات"}])

df = load_data()

# --- بداية المنطق البرمجي (Logic) ---

# الصفحة الرئيسية
if st.session_state.page == 'main':
    st.title("🏛️ موسوعة المطورين العقاريين")
    
    search = st.text_input("🔍 ابحث عن أي مطور أو منطقة...")
    
    filtered = df.copy()
    if search:
        filtered = filtered[filtered['Developer'].str.contains(search, case=False, na=False)]

    for i, row in filtered.iterrows():
        st.markdown(f"""
            <div class="main-card">
                <span style="color:#003366; font-size:1.2rem; font-weight:bold;">{row['Developer']}</span><br>
                <span class="info-badge">📍 {row.get('Area', '-')}</span>
                <span class="info-badge">💰 {row.get('Price', '-')}</span>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"تفاصيل {row['Developer']}", key=f"btn_{i}"):
            st.session_state.selected_item = row.to_dict()
            st.session_state.page = 'details'
            st.rerun()

# صفحة التفاصيل (بنفس ألوان الرئيسية اللي طلبتها)
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    
    if st.button("🔙 عودة للقائمة"):
        st.session_state.page = 'main'
        st.rerun()
    
    st.header(f"🏢 {item['Developer']}")
    
    # تفاصيل واضحة وبسيطة بنفس الوان الموقع
    st.markdown(f"""
        <div class="main-card">
            <h3 style="color:#003366;">💡 الزتونة الفنية</h3>
            <p style="font-size:1.1rem; line-height:1.6;">{item.get('Detailed_Info', 'لا توجد تفاصيل إضافية حالياً')}</p>
        </div>
        
        <div class="main-card">
            <p><b>👤 المالك:</b> {item.get('Owner', '-')}</p>
            <p><b>🏗️ المشاريع:</b> {item.get('Projects', '-')}</p>
            <p><b>💰 السعر:</b> {item.get('Price', '-')}</p>
            <p><b>🕒 الاستلام:</b> {item.get('Delivery', '-')}</p>
            <p><b>📝 الوصف:</b> {item.get('Description', '-')}</p>
        </div>
    """, unsafe_allow_html=True)
