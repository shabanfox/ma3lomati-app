import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="معلوماتى العقارية | أداة البروكر", layout="wide")

# 2. كود التصميم (CSS) - الشكل الرمادي المعتمد
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f1f5f9; 
    }
    .block-container { max-width: 1150px; margin: auto; padding: 1rem 3% !important; }
    .header-nav { text-align: right; padding: 10px 0; margin-bottom: 5px; }

    /* صندوق المقارنة */
    .compare-box { 
        background: #fff; padding: 15px; border-radius: 12px; 
        border: 2px dashed #003366; margin-bottom: 15px; 
    }
    
    .project-card-container { 
        background-color: #edf2f7; border-radius: 10px; 
        margin-bottom: 5px !important; display: flex;
        align-items: center; border: 1px solid #e2e8f0; overflow: hidden;
    }

    div.stButton > button {
        background-color: #003366 !important; color: white !important;
        border-radius: 6px !important; padding: 4px 15px !important;
        font-size: 0.85rem !important; font-weight: 700 !important;
    }
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

# تعريف حالة الجلسة للمقارنة
if 'compare_list' not in st.session_state: st.session_state.compare_list = []
if 'page' not in st.session_state: st.session_state.page = 'main'

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    st.markdown('<div class="header-nav"><div style="color:#003366; font-weight:900; font-size:1.8rem;">منصة معلوماتى <span style="color:#D4AF37;">العقارية</span></div></div>', unsafe_allow_html=True)

    if df is not None:
        # قسم المقارنة (يظهر فقط عند اختيار مطورين)
        if st.session_state.compare_list:
            with st.container():
                st.markdown('<div class="compare-box">', unsafe_allow_html=True)
                st.write(f"📊 مطورين مختارين للمقارنة: {len(st.session_state.compare_list)}")
                col_comp1, col_comp2 = st.columns(2)
                if col_comp1.button("إجراء المقارنة"):
                    st.session_state.page = 'compare'
                    st.rerun()
                if col_comp2.button("مسح القائمة"):
                    st.session_state.compare_list = []
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        # الفلاتر الأساسية
        col1, col2 = st.columns([2, 1])
        with col1: s_dev = st.text_input("🔍 ابحث باسم المطور...")
        with col2: s_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df['Area'].dropna().unique().tolist()))

        f_df = df.copy()
        if s_dev: f_df = f_df[f_df['Developer'].astype(str).str.contains(s_dev, case=False, na=False)]
        if s_area != "الكل": f_df = f_df[f_df['Area'] == s_area]

        # عرض الكروت
        for i, row in f_df.iterrows():
            st.markdown('<div class="project-card-container">', unsafe_allow_html=True)
            col_content, col_img = st.columns([4, 1])
            with col_content:
                txt_c, btn_c = st.columns([3, 1])
                with txt_c:
                    st.markdown(f"""
                        <div style="text-align: right; padding: 15px;">
                            <div style="color: #003366; font-weight: 900; font-size: 1.3rem;">{row.get('Developer')}</div>
                            <div style="color: #D4AF37; font-weight: 700; font-size: 0.85rem;">📍 {row.get('Area')} | {row.get('Price')}</div>
                            <div style="color: #64748b; font-size: 0.8rem;">نظام القسط: {row.get('Installments', '-')} سنوات</div>
                        </div>
                    """, unsafe_allow_html=True)
                with btn_c:
                    st.write("")
                    if st.button("التفاصيل", key=f"det_{i}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'
                        st.rerun()
                    # زر إضافة للمقارنة
                    is_in = row['Developer'] in st.session_state.compare_list
                    label = "✅ مضاف" if is_in else "➕ مقارنة"
                    if st.button(label, key=f"comp_{i}"):
                        if not is_in: st.session_state.compare_list.append(row['Developer'])
                        else: st.session_state.compare_list.remove(row['Developer'])
                        st.rerun()

            with col_img:
                img_url = row.get('Image_URL', 'https://via.placeholder.com/400')
                st.markdown(f'<div style="height: 110px; background-image: url(\'{img_url}\'); background-size: cover; background-position: center;"></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة المقارنة ---
elif st.session_state.page == 'compare':
    st.markdown("### 📊 جدول المقارنة الفني")
    if st.button("⬅️ عودة"):
        st.session_state.page = 'main'
        st.rerun()
    
    compare_df = df[df['Developer'].isin(st.session_state.compare_list)]
    # عرض جدول نظيف للبروكر
    st.table(compare_df[['Developer', 'Area', 'Price', 'Installments', 'Owner']])

# --- صفحة التفاصيل ---
else:
    item = st.session_state.selected_item
    st.markdown('<div style="background:white; padding:30px; border-radius:15px; margin-top:10px; border: 1px solid #e2e8f0;">', unsafe_allow_html=True)
    if st.button("⬅️ عودة"):
        st.session_state.page = 'main'; st.rerun()
    st.markdown(f"<h2>{item.get('Developer')}</h2>", unsafe_allow_html=True)
    st.write(item.get('Description', 'جاري التحديث...'))
    st.markdown('</div>', unsafe_allow_html=True)
