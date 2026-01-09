import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    .block-container { padding: 0rem !important; }
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }
    .header-nav { background: white; height: 75px; padding: 0 8%; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; }
    .hero-bg {
        background-image: linear-gradient(rgba(0, 30, 60, 0.4), rgba(0, 30, 60, 0.4)), 
                        url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=2070');
        background-size: cover; background-position: center; height: 250px; 
        display: flex; flex-direction: column; justify-content: center; align-items: center; color: white;
    }
    .filter-box { background: white; margin: -40px 10% 20px 10%; padding: 25px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); position: relative; z-index: 10; }
    
    /* تنسيق الكارت */
    .project-card { 
        background: white; border-radius: 16px; border: 1px solid #e2e8f0; 
        display: flex; margin-bottom: 20px; overflow: hidden; padding: 15px;
        align-items: center; justify-content: space-between;
    }
    
    /* تنسيق زرار التفاصيل الأزرق الصغير */
    div.stButton > button {
        background-color: #003366 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 5px 15px !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        border: none !important;
        transition: 0.3s !important;
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

# --- صفحة التفاصيل ---
if st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("⬅️ عودة للقائمة"):
        st.session_state.page = 'main'
        st.rerun()
    
    st.markdown(f"""
        <div style="background:white; padding:30px; border-radius:20px; margin: 20px 10%; border-right: 8px solid #003366;">
            <h1 style="color:#003366;">{item.get('Developer')}</h1>
            <h4 style="color:#D4AF37;">المالك: {item.get('Owner')}</h4>
            <p><b>نبذة:</b> {item.get('Description', 'لا يوجد وصف.')}</p>
            <p><b>المشاريع:</b> {item.get('Projects')}</p>
            <p><b>المنطقة:</b> {item.get('Area')}</p>
        </div>
    """, unsafe_allow_html=True)

# --- الصفحة الرئيسية ---
else:
    st.markdown('<div class="header-nav"><div style="color:#003366; font-weight:900; font-size:1.8rem;">معلوماتى <span style="color:#D4AF37;">العقارية</span></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-bg"><h1>دليلك العقاري</h1></div>', unsafe_allow_html=True)

    if df is not None:
        # الفلاتر
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: search_dev = st.text_input("🔍 المطور")
        with c2: search_area = st.selectbox("📍 المنطقة", ["كل المناطق"] + sorted(list(df['Area'].dropna().unique())))
        with c3: search_price = st.selectbox("💰 السعر", ["الكل", "أقل من 5 مليون", "أكثر من 10 مليون"])
        st.markdown('</div>', unsafe_allow_html=True)

        f_df = df.copy()
        # عرض الكروت
        st.markdown('<div style="margin: 0 10%;">', unsafe_allow_html=True)
        for _, row in f_df.iterrows():
            # تقسيم الصف: اليمين للكلام والزرار، الشمال للصورة
            col_content, col_img = st.columns([3, 1])
            
            with col_content:
                # هنا بنحط الكلام والزرار جنبه مباشرة باستخدام columns داخلية
                txt_col, btn_col = st.columns([3, 1])
                with txt_col:
                    st.markdown(f"""
                        <div style="text-align: right;">
                            <div style="color: #003366; font-weight: 900; font-size: 1.3rem;">{row.get('Developer')}</div>
                            <div style="color: #D4AF37; font-weight: 700; font-size: 0.9rem;">المالك: {row.get('Owner')}</div>
                            <div style="color: #64748b; font-size: 0.8rem;">📍 {row.get('Area')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with btn_col:
                    st.write("") # موازنة المسافة
                    if st.button("التفاصيل", key=f"btn_{row.get('Developer')}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'
                        st.rerun()

            with col_img:
                img_url = row.get('Image_URL', 'https://via.placeholder.com/400')
                st.markdown(f"""
                    <div style="height: 100px; border-radius: 12px; background-image: url('{img_url}'); background-size: cover; background-position: center;"></div>
                """, unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 10px 0; border: 0.1px solid #f1f1f1;'>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
