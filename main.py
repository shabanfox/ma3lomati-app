import streamlit as st
import pd as pd

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="Real Estate Wiki", layout="wide")

# 2. كود التصميم (CSS) - الألوان اللي طلبتها
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
        background-color: #f1f5f9; color: #475569; padding: 2px 8px; 
        border-radius: 5px; font-size: 0.8rem; margin-left: 5px;
    }
    div.stButton > button {
        background-color: #003366 !important; color: white !important;
        border-radius: 8px !important; width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 3. منع أخطاء الـ NameError بتعريف الـ Session State
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 4. دالة التحميل (تأكد من وضع رابط الـ CSV الخاص بك)
@st.cache_data
def load_data():
    csv_url = "رابط_شيت_جوجل_هنا"
    try:
        return pd.read_csv(csv_url)
    except:
        return pd.DataFrame([{"Developer": "يرجى ربط الشيت", "Area": "-", "Price": "-", "Detailed_Info": "-"}])

df = load_data()

# --- التنقل بين الصفحات ---

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
                <span class="info-badge">📍 {row['Area']}</span>
                <span class="info-badge">💰 {row['Price']}</span>
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
    
    # صفحة التفاصيل بنفس ألوان الرئيسية
    st.markdown(f"""
        <div style="background-color:#003366; padding:15px; border-radius:10px; color:white; text-align:center;">
            <h2>{item['Developer']}</h2>
        </div>
        <br>
        <div class="main-card">
            <h3 style="color:#003366;">💡 الزتونة الفنية</h3>
            <p style="font-size:1.1rem; line-height:1.6;">{item.get('Detailed_Info', 'لا يوجد بيانات')}</p>
        </div>
        <div class="main-card">
            <p><b>👤 المالك:</b> {item.get('Owner')}</p>
            <p><b>🏢 المشاريع:</b> {item.get('Projects')}</p>
            <p><b>💰 المقدم:</b> {item.get('Down_Payment')}</p>
            <p><b>⏳ التقسيط:</b> {item.get('Installments')}</p>
        </div>
    """, unsafe_allow_html=True)
