import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="موسوعة العقارات المصرية", layout="wide")

# 2. كود التصميم (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f8fafc; 
    }

    .main-card { 
        background-color: white; border-radius: 12px; 
        padding: 15px; margin-bottom: 10px;
        border-right: 5px solid #003366;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .info-badge {
        background-color: #f1f5f9; color: #475569;
        padding: 2px 8px; border-radius: 5px; font-size: 0.8rem;
        margin-left: 5px; border: 1px solid #e2e8f0;
    }

    div.stButton > button {
        background-color: #003366 !important; color: white !important;
        border-radius: 8px !important; width: 100%; font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    csv_url = "رابط_شيت_جوجل_الخاص_بك_هنا"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except: return None

df = load_data()

# إدارة الجلسة
if 'page' not in st.session_state: st.session_state.page = 'main'

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    st.title("🏛️ موسوعة المطورين العقاريين")
    
    if df is not None:
        # محرك البحث الذكي
        search = st.text_input("🔍 ابحث عن مطور، منطقة، أو ميزة (مثلاً: تشطيب، ناطحة سحاب، قسط 10 سنين)")
        
        # الفلاتر السريعة
        c1, c2 = st.columns(2)
        with c1: area_f = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df['Area'].unique().tolist()))
        with c2: type_f = st.selectbox("🏗️ نوع المشروع", ["الكل"] + sorted(df['Type'].unique().tolist()))

        # تصفية البيانات
        filtered = df.copy()
        if search:
            filtered = filtered[
                filtered['Developer'].str.contains(search, case=False, na=False) |
                filtered['Detailed_Info'].str.contains(search, case=False, na=False)
            ]
        if area_f != "الكل": filtered = filtered[filtered['Area'] == area_f]
        if type_f != "الكل": filtered = filtered[filtered['Type'] == type_f]

        st.caption(f"تم العثور على {len(filtered)} مطور")

        # عرض النتائج
        for i, row in filtered.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="main-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <span style="color:#003366; font-size:1.3rem; font-weight:900;">{row['Developer']}</span>
                            <div style="margin-top:5px;">
                                <span class="info-badge">📍 {row['Area']}</span>
                                <span class="info-badge">⏳ {row['Installments']} سنين</span>
                                <span class="info-badge">💰 {row['Price']}</span>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("فتح ملف الشركة الكامل", key=f"btn_{i}"):
                    st.session_state.selected_item = row.to_dict()
                    st.session_state.page = 'details'
                    st.rerun()

# --- صفحة التفاصيل الفنية ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 عودة للموسوعة"): st.session_state.page = 'main'; st.rerun()
    
    st.header(f"🏢 {item['Developer']}")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("💡 الزتونة الفنية (للبـروكـر)")
        st.success(item.get('Detailed_Info', 'لا توجد معلومات إضافية'))
        
        st.subheader("📝 الوصف")
        st.info(item.get('Description'))
        
        st.subheader("📑 بيانات المشروع")
        st.write(f"**المشاريع:** {item.get('Projects')}")
        st.write(f"**المالك:** {item.get('Owner')}")
    
    with col2:
        st.subheader("📊 أرقام تهمك")
        st.write(f"**المقدم:** {item.get('Down_Payment')}")
        st.write(f"**الاستلام:** {item.get('Delivery')}")
        st.write(f"**سنين القسط:** {item.get('Installments')}")
        st.write(f"**أقل قيمة:** {item.get('Min_Val')}")
