import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="معلوماتى العقارية | محرك البحث", layout="wide")

# 2. تصميم الواجهة (نظيف واحترافي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }
    .main-header { background: white; padding: 20px 5%; border-bottom: 2px solid #e2e8f0; margin-bottom: 20px; }
    .filter-section { background: #ffffff; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 25px; }
    .card-style { background: white; padding: 20px; border-radius: 12px; margin-bottom: 10px; border-right: 6px solid #003366; box-shadow: 0 2px 5px rgba(0,0,0,0.03); }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except: return None

df = load_data()

# إدارة التنقل
if 'page' not in st.session_state:
    st.session_state.page = 'main'
    st.session_state.selected_item = None

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    st.markdown('<div class="main-header"><h2 style="color:#003366; margin:0;">منصة معلوماتى <span style="color:#D4AF37;">العقارية</span></h2></div>', unsafe_allow_html=True)

    if df is not None:
        # شريط الفلاتر المتقدمة
        with st.container():
            st.markdown('<div class="filter-section">', unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                area_list = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
                sel_area = st.selectbox("📍 المنطقة", area_list)
            
            with col2:
                # فلتر النوع (سكني/تجاري) - يظهر المتاح فقط في المنطقة المختارة
                temp_df = df if sel_area == "الكل" else df[df['Area'] == sel_area]
                type_list = ["الكل"] + sorted(temp_df['Type'].dropna().unique().tolist()) if 'Type' in df.columns else ["الكل"]
                sel_type = st.selectbox("🏠 نوع الوحدة", type_list)
                
            with col3:
                # فلتر سنوات القسط
                inst_list = ["الكل"] + sorted(df['Installments'].dropna().unique().tolist()) if 'Installments' in df.columns else ["الكل"]
                sel_inst = st.selectbox("⏳ سنوات القسط", inst_list)
                
            with col4:
                search_name = st.text_input("🔍 ابحث عن مطور")
            st.markdown('</div>', unsafe_allow_html=True)

        # منطق الفلترة
        filtered_df = df.copy()
        if sel_area != "الكل": filtered_df = filtered_df[filtered_df['Area'] == sel_area]
        if sel_type != "الكل": filtered_df = filtered_df[filtered_df['Type'] == sel_type]
        if sel_inst != "الكل": filtered_df = filtered_df[filtered_df['Installments'] == sel_inst]
        if search_name: filtered_df = filtered_df[filtered_df['Developer'].str.contains(search_name, case=False, na=False)]

        # عرض النتائج
        st.write(f"تم العثور على ({len(filtered_df)}) مطورين")
        
        for _, row in filtered_df.iterrows():
            c_main, c_img = st.columns([4, 1])
            with c_main:
                st.markdown(f"""
                <div class="card-style">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h3 style="margin:0; color:#003366;">{row.get('Developer')}</h3>
                            <p style="margin:5px 0; color:#64748b; font-size:0.9rem;">
                                📍 {row.get('Area')} | 🏢 النوع: {row.get('Type', 'غير محدد')} | 💳 قسط: {row.get('Installments', '-')} سنين
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # زر التفاصيل بجانب الكلام
                st.markdown('<div style="margin-top:-50px; margin-right:20px;">', unsafe_allow_html=True)
                if st.button("التفاصيل", key=f"btn_{row.get('Developer')}"):
                    st.session_state.selected_item = row.to_dict()
                    st.session_state.page = 'details'
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            with c_img:
                img_url = row.get('Image_URL', 'https://via.placeholder.com/400')
                st.markdown(f'<div style="height:100px; border-radius:12px; background-image:url(\'{img_url}\'); background-size:cover; background-position:center; margin-top:5px;"></div>', unsafe_allow_html=True)

# --- صفحة التفاصيل ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    st.markdown('<div style="background:white; padding:40px; border-radius:20px; margin-top:20px;">', unsafe_allow_html=True)
    if st.button("⬅️ العودة للبحث"):
        st.session_state.page = 'main'
        st.rerun()
    
    st.markdown(f"<h1 style='color:#003366;'>{item.get('Developer')}</h1>", unsafe_allow_html=True)
    st.info(f"📍 المنطقة: {item.get('Area')} | 📅 الاستلام: {item.get('Delivery', 'غير محدد')}")
    st.write(f"### عن المطور")
    st.write(item.get('Description', 'لا يوجد وصف متاح حالياً.'))
    st.write(f"### أهم المشاريع")
    st.write(item.get('Projects'))
    st.markdown('</div>', unsafe_allow_html=True)
