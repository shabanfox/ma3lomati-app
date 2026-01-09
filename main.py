import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="الموسوعة العقارية", layout="wide")

# 2. كود التصميم CSS (الشكل الأساسي اللي بتحبه)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc;
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
        border-radius: 8px !important; width: 100%; font-family: 'Cairo', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# 3. منع أخطاء التشغيل (Session State)
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None

# 4. دالة تحميل البيانات
@st.cache_data
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-o6G_M6F9YI8Y5D6E7L9k-y9W3H8P0U5L-Yv1K9M-N0V-W3H8P0U5L/pub?output=csv" 
    try:
        df = pd.read_csv(csv_url)
        return df
    except:
        # بيانات تجريبية في حالة عدم توفر الرابط
        return pd.DataFrame([{"Developer": "Mountain View", "Area": "التجمع", "Price": "8.5M", "Detailed_Info": "نظام 4D المبتكر"}])

df = load_data()

# --- منطق التنقل بين الصفحات ---

# الصفحة الرئيسية (الشكل الأساسي)
if st.session_state.page == 'main':
    st.markdown("<h1 style='color: #003366; text-align: center;'>🏛️ موسوعة المطورين</h1>", unsafe_allow_html=True)
    
    search = st.text_input("🔍 ابحث عن مطور أو منطقة...")
    
    filtered = df.copy()
    if search:
        filtered = filtered[filtered['Developer'].str.contains(search, case=False, na=False) | 
                            filtered['Detailed_Info'].str.contains(search, case=False, na=False)]

    for i, row in filtered.iterrows():
        st.markdown(f"""
            <div class="main-card">
                <span style="color:#003366; font-size:1.2rem; font-weight:bold;">{row['Developer']}</span><br>
                <span class="info-badge">📍 {row.get('Area', '-')}</span>
                <span class="info-badge">💰 {row.get('Price', '-')}</span>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"عرض التفاصيل الفنية", key=f"btn_{i}"):
            st.session_state.selected_item = row.to_dict()
            st.session_state.page = 'details'
            st.rerun()

# صفحة التفاصيل (بنفس ألوان وتنسيق الصفحة الرئيسية تماماً)
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    
    if st.button("🔙 عودة للقائمة"):
        st.session_state.page = 'main'
        st.rerun()
    
    # الهيدر بنفس اللون الكحلي
    st.markdown(f"""
        <div style="background-color: #003366; padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px;">
            <h1 style="margin:0;">{item['Developer']}</h1>
            <p style="margin:5px 0 0 0; opacity: 0.9;">{item.get('Projects', 'مشاريع متنوعة')}</p>
        </div>
    """, unsafe_allow_html=True)

    # عرض "الزتونة" في كارت بنفس ستايل الرئيسية
    st.markdown(f"""
        <div class="main-card">
            <h3 style="color:#003366; margin-top:0;">💡 الزتونة الفنية (للبـروكـر)</h3>
            <p style="font-size:1.1rem; line-height:1.6; color: #1e293b;">{item.get('Detailed_Info', 'لا توجد بيانات إضافية حالياً')}</p>
        </div>
        
        <div class="main-card">
            <h3 style="color:#003366; margin-top:0;">📊 بيانات المشروع</h3>
            <p><b>👤 المالك:</b> {item.get('Owner', '-')}</p>
            <p><b>💰 المقدم:</b> {item.get('Down_Payment', '-')}</p>
            <p><b>⏳ سنوات القسط:</b> {item.get('Installments', '-')}</p>
            <p><b>🕒 الاستلام:</b> {item.get('Delivery', '-')}</p>
            <hr>
            <p><b>📝 الوصف العام:</b><br>{item.get('Description', '-')}</p>
        </div>
    """, unsafe_allow_html=True)
