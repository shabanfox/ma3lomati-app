import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="الموسوعة العقارية", layout="wide")

# 2. كود التصميم (CSS) - الشكل الأساسي الأصلي
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

# 3. التأكد من وجود متغيرات الصفحة (لحماية التطبيق من الـ NameError)
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None

# 4. تحميل البيانات (تأكد من وضع الرابط الخاص بك هنا)
@st.cache_data
def load_data():
    # استبدل هذا الرابط برابط الشيت الخاص بك
    csv_url = "https://docs.google.com/spreadsheets/d/e/YOUR_LINK_HERE/pub?output=csv"
    try:
        return pd.read_csv(csv_url)
    except:
        return pd.DataFrame([{"Developer": "يرجى وضع رابط الشيت", "Area": "-", "Price": "-", "Detailed_Info": "-"}])

df = load_data()

# --- إدارة الصفحات (الشكل الأساسي) ---

if st.session_state.page == 'main':
    st.title("🏛️ موسوعة المطورين")
    search = st.text_input("🔍 ابحث هنا...")
    
    filtered = df.copy()
    if search:
        filtered = filtered[filtered['Developer'].str.contains(search, case=False, na=False)]

    for i, row in filtered.iterrows():
        st.markdown(f"""
            <div class="main-card">
                <span style="color:#003366; font-size:1.2rem; font-weight:bold;">{row['Developer']}</span><br>
                <span>📍 المنطقة: {row.get('Area', '-')}</span> | 
                <span>💰 السعر: {row.get('Price', '-')}</span>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"التفاصيل", key=f"btn_{i}"):
            st.session_state.selected_item = row.to_dict()
            st.session_state.page = 'details'
            st.rerun()

elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    
    if st.button("🔙 عودة"):
        st.session_state.page = 'main'
        st.rerun()
    
    # صفحة التفاصيل بالشكل الأساسي البسيط
    st.header(f"🏢 {item['Developer']}")
    
    st.info(f"💡 الزتونة الفنية: {item.get('Detailed_Info', 'لا توجد بيانات')}")
    
    st.write(f"**👤 المالك:** {item.get('Owner', '-')}")
    st.write(f"**🏗️ المشاريع:** {item.get('Projects', '-')}")
    st.write(f"**💰 السعر:** {item.get('Price', '-')}")
    st.write(f"**⏳ التقسيط:** {item.get('Installments', '-')}")
    st.write(f"**📝 وصف المطور:** {item.get('Description', '-')}")
