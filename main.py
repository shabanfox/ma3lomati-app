import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - العودة للشكل اللي اخترته
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f1f5f9; 
    }

    .block-container { 
        max-width: 1150px; 
        margin: auto; 
        padding: 1rem 2% !important; 
    }

    /* الهيدر: الاسم على اليمين */
    .header-nav { 
        text-align: right; 
        padding: 15px 0; 
        margin-bottom: 5px;
    }

    /* صندوق الفلاتر */
    .filter-box { 
        background: white; 
        padding: 15px; 
        border-radius: 12px; 
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* تنسيق الكارت الأصلي */
    .project-card { 
        background: white; 
        border-radius: 12px; 
        margin-bottom: 5px !important; 
        overflow: hidden;
        display: flex;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* زرار التفاصيل الأزرق بجانب الكلام */
    div.stButton > button {
        background-color: #003366 !important;
        color: white !important;
        border-radius: 6px !important;
        padding: 4px 12px !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        border: none !important;
    }
    
    div.stButton > button:hover {
        background-color: #D4AF37 !important;
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

if 'page' not in st.session_state:
    st.session_state.page = 'main'
    st.session_state.selected_item = None

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    # الهيدر على اليمين
    st.markdown('<div class="header-nav"><div style="color:#003366; font-weight:900; font-size:1.8rem;">منصة معلوماتى <span style="color:#D4AF37;">العقارية</span></div></div>', unsafe_allow_html=True)

    if df is not None:
        # الفلاتر (التطوير الجديد)
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: search_dev = st.text_input("🔍 المطور")
        with c2: 
            area_list = ["كل المناطق"] + sorted(df['Area'].dropna().unique().tolist())
            search_area = st.selectbox("📍 المنطقة", area_list)
        with c3:
            type_list = ["كل الأنواع"] + sorted(df['Type'].dropna().unique().tolist()) if 'Type' in df.columns else ["كل الأنواع"]
            search_type = st.selectbox("🏠 النوع", type_list)
        with c4:
            search_price = st.selectbox("💰 السعر", ["الكل", "أقل من 5 مليون", "10 مليون+"])
        st.markdown('</div>', unsafe_allow_html=True)

        # منطق الفلترة
        f_df = df.copy()
        if search_dev: f_df = f_df[f_df['Developer'].str.contains(search_dev, case=False, na=False)]
        if search_area != "كل المناطق": f_df = f_df[f_df['Area'] == search_area]
        if search_type != "كل الأنواع": f_df = f_df[f_df['Type'] == search_type]

        # عرض الكروت (الشكل الأصلي المظبوط)
        for _, row in f_df.iterrows():
            # صف واحد يحتوي على (المحتوى + الصورة)
            col_content, col_img = st.columns([4, 1])
            
            with col_content:
                # تقسيم داخلي: اليمين للكلام واليسار (بجانبه مباشرة) للزرار
                txt_c, btn_c = st.columns([3, 1])
                with txt_c:
                    st.markdown(f"""
                        <div style="text-align: right; padding: 10px;">
                            <div style="color: #003366; font-weight: 900; font-size: 1.3rem;">{row.get('Developer')}</div>
                            <div style="color: #D4AF37; font-weight: 700; font-size: 0.9rem;">المالك: {row.get('Owner')}</div>
                            <div style="color: #64748b; font-size: 0.8rem;">📍 {row.get('Area')} | النوع: {row.get('Type', '-')} | {row.get('Price')} ج.م</div>
                        </div>
                    """, unsafe_allow_html=True)
                with btn_c:
                    st.write("") # موازنة رأسية للزرار
                    st.write("")
                    if st.button("التفاصيل", key=f"btn_{row.get('Developer')}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'
                        st.rerun()

            with col_img:
                img_url = row.get('Image_URL', 'https://via.placeholder.com/400')
                st.markdown(f"""
                    <div style="height: 100px; border-radius: 12px; background-image: url('{img_url}'); background-size: cover; background-position: center;"></div>
                """, unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 2px 0; opacity: 0.05;'>", unsafe_allow_html=True)

# --- صفحة التفاصيل ---
else:
    item = st.session_state.selected_item
    st.markdown('<div style="background:white; padding:30px; border-radius:15px; margin-top:10px;">', unsafe_allow_html=True)
    if st.button("⬅️ عودة"):
        st.session_state.page = 'main'
        st.rerun()
    st.markdown(f"<h2 style='color:#003366;'>{item.get('Developer')}</h2>", unsafe_allow_html=True)
    st.write(item.get('Description', 'جاري تحديث البيانات...'))
    st.markdown('</div>', unsafe_allow_html=True)
