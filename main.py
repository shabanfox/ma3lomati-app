import streamlit as st
import pandas as pd

# 1. الإعدادات الملكية (أول سطر في الكود)
st.set_page_config(page_title="الموسوعة العقارية", layout="wide")

# 2. كود التصميم CSS الأصلي (اللي أنت متعود عليه)
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
    div.stButton > button {
        background-color: #003366 !important; color: white !important;
        border-radius: 8px !important; width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 3. منع أخطاء الجلسة (الضمان الملكي)
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None

# 4. دالة جلب البيانات (تأكد من وضع الرابط الصحيح)
@st.cache_data
def load_data():
    # حط رابط الشيت المجمع (الـ 100 مطور) هنا
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS-o6G_M6F9YI8Y5D6E7L9k-y9W3H8P0U5L-Yv1K9M-N0V-W3H8P0U5L/pub?output=csv" 
    try:
        return pd.read_csv(csv_url)
    except:
        return pd.DataFrame([{"Developer": "يرجى ربط الشيت", "Area": "-", "Price": "-", "Detailed_Info": "-"}])

df = load_data()

# --- إدارة الصفحات الملكية ---

# الصفحة الرئيسية
if st.session_state.page == 'main':
    st.markdown("<h1 style='color: #003366;'>🏛️ موسوعة المطورين</h1>", unsafe_allow_html=True)
    
    search = st.text_input("🔍 ابحث هنا عن أي مطور أو منطقة...")
    
    filtered = df.copy()
    if search:
        # البحث في الاسم أو الزتونة الفنية
        filtered = filtered[filtered['Developer'].str.contains(search, case=False, na=False) | 
                            filtered['Detailed_Info'].str.contains(search, case=False, na=False)]

    for i, row in filtered.iterrows():
        st.markdown(f"""
            <div class="main-card">
                <span style="color:#003366; font-size:1.2rem; font-weight:bold;">{row['Developer']}</span><br>
                <span>📍 المنطقة: {row.get('Area', '-')}</span> | 
                <span>💰 السعر: {row.get('Price', '-')}</span>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"عرض التفاصيل", key=f"btn_{i}"):
            st.session_state.selected_item = row.to_dict()
            st.session_state.page = 'details'
            st.rerun()

# صفحة التفاصيل (الشكل القديم البسيط اللي مريحك)
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    
    if st.button("🔙 العودة للقائمة"):
        st.session_state.page = 'main'
        st.rerun()
    
    st.header(f"🏢 {item['Developer']}")
    
    # استخدام الـ Blocks العادية الواضحة
    st.info(f"💡 الزتونة الفنية: {item.get('Detailed_Info', 'لا توجد بيانات إضافية')}")
    
    st.write(f"**👤 المالك:** {item.get('Owner', '-')}")
    st.write(f"**🏗️ أهم المشاريع:** {item.get('Projects', '-')}")
    st.write(f"**💰 متوسط السعر:** {item.get('Price', '-')}")
    st.write(f"**⏳ أنظمة التقسيط:** {item.get('Installments', '-')}")
    st.write(f"**📝 وصف عام:** {item.get('Description', '-')}")
