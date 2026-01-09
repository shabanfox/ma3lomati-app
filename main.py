import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - ركزت هنا على الـ Container والـ Margins
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الزوائد */
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    /* ضبط مسافات الصفحة الكلية */
    .block-container { 
        padding-top: 0rem !important; 
        padding-bottom: 0rem !important;
        max-width: 1200px; /* تحديد أقصى عرض للكلام عشان ميسرحش على الشاشات الكبيرة */
        margin: auto; /* توسيط المحتوى */
    }

    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f8fafc; 
    }

    /* الهيدر مع مسافات جانبية داخلية */
    .header-nav { 
        background: white; 
        height: 80px; 
        padding: 0 5%; 
        display: flex; 
        align-items: center; 
        border-bottom: 2px solid #e2e8f0; 
        margin-bottom: 0;
    }

    /* صورة الغلاف */
    .hero-bg {
        background-image: linear-gradient(rgba(0, 30, 60, 0.5), rgba(0, 30, 60, 0.5)), 
                        url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=2070');
        background-size: cover; 
        background-position: center; 
        height: 200px; 
        display: flex; 
        justify-content: center; 
        align-items: center; 
        color: white;
        border-radius: 0 0 20px 20px; /* انحناء بسيط من تحت */
        margin: 0 2%; /* ابعاد خفيفة عن الحواف */
    }

    /* صندوق الفلاتر */
    .filter-box { 
        background: white; 
        margin: -30px 5% 30px 5%; 
        padding: 25px; 
        border-radius: 15px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.08); 
        position: relative; 
        z-index: 10; 
    }
    
    /* الكارت مع مسافات داخلية */
    .project-card-container {
        padding: 0 5%; /* دي اللي بتبعد الكروت عن حافة الشاشة */
    }

    /* زرار التفاصيل الأزرق */
    div.stButton > button {
        background-color: #003366 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 6px 20px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        border: none !important;
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

# إدارة التنقل
if 'page' not in st.session_state:
    st.session_state.page = 'main'
    st.session_state.selected_item = None

# --- صفحة التفاصيل (مع مسافات جانبية) ---
if st.session_state.page == 'details':
    st.markdown('<div style="padding: 20px 5%;">', unsafe_allow_html=True)
    if st.button("⬅️ عودة"):
        st.session_state.page = 'main'
        st.rerun()
    
    item = st.session_state.selected_item
    st.markdown(f"""
        <div style="background:white; padding:40px; border-radius:20px; border-right: 10px solid #003366; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
            <h1 style="color:#003366; margin-bottom:10px;">{item.get('Developer')}</h1>
            <p style="color:#D4AF37; font-size:1.2rem; font-weight:bold;">المالك: {item.get('Owner')}</p>
            <hr>
            <p style="font-size:1.1rem; line-height:1.8;">{item.get('Description', 'نبذة عن المطور قريباً...')}</p>
            <p><b>المشاريع:</b> {item.get('Projects')}</p>
            <p><b>المنطقة:</b> {item.get('Area')}</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- الصفحة الرئيسية ---
else:
    # الهيدر
    st.markdown('<div class="header-nav"><div style="color:#003366; font-weight:900; font-size:1.8rem;">معلوماتى <span style="color:#D4AF37;">العقارية</span></div></div>', unsafe_allow_html=True)
    
    # الغلاف
    st.markdown('<div class="hero-bg"><h1 style="font-weight:900;">دليلك العقاري في مصر</h1></div>', unsafe_allow_html=True)

    if df is not None:
        # الفلاتر
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: search_dev = st.text_input("🔍 اسم المطور")
        with c2: search_area = st.selectbox("📍 المنطقة", ["كل المناطق"] + sorted(list(df['Area'].dropna().unique())))
        with c3: search_price = st.selectbox("💰 السعر", ["الكل", "أقل من 5 مليون", "5 - 10 مليون", "أكثر من 10 مليون"])
        st.markdown('</div>', unsafe_allow_html=True)

        # عرض الكروت داخل حاوية بمسافات
        st.markdown('<div class="project-card-container">', unsafe_allow_html=True)
        
        f_df = df.copy()
        # منطق الفلترة... (نفس القديم)

        for _, row in f_df.iterrows():
            # تصميم الصف: محتوى (كلام + زرار) وصورة
            col_info, col_img = st.columns([3.5, 1])
            
            with col_info:
                # تقسيم داخلي للكلام والزرار بجانبه
                txt_c, btn_c = st.columns([2.5, 1])
                with txt_c:
                    st.markdown(f"""
                        <div style="text-align: right; padding-right: 10px;">
                            <div style="color: #003366; font-weight: 900; font-size: 1.4rem;">{row.get('Developer')}</div>
                            <div style="color: #D4AF37; font-weight: 700;">المالك: {row.get('Owner')}</div>
                            <div style="color: #64748b; font-size: 0.9rem;">📍 {row.get('Area')} | {row.get('Price')} ج.م</div>
                        </div>
                    """, unsafe_allow_html=True)
                with btn_c:
                    st.write("") # موازنة
                    st.write("")
                    if st.button("التفاصيل", key=f"btn_{row.get('Developer')}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'
                        st.rerun()

            with col_img:
                img_url = row.get('Image_URL', 'https://via.placeholder.com/400')
                st.markdown(f"""
                    <div style="height: 110px; border-radius: 15px; background-image: url('{img_url}'); background-size: cover; background-position: center;"></div>
                """, unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 15px 0; opacity: 0.1;'>", unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
