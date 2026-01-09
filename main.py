import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - ضبط الخلفية والمساحات
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    /* جعل الخلفية صورة البرج الأيقوني ثابتة */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(0, 20, 40, 0.7), rgba(0, 20, 40, 0.7)), 
                        url('http://googleusercontent.com/image_collection/image_retrieval/14882722463286650492_0');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        direction: RTL;
        text-align: right;
        font-family: 'Cairo', sans-serif;
    }

    .block-container { 
        max-width: 1100px;
        margin: auto;
        padding-top: 2rem !important;
    }

    /* الهيدر الشفاف */
    .header-nav { 
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        height: 80px; 
        padding: 0 5%; 
        display: flex; 
        align-items: center; 
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        margin-bottom: 30px;
    }

    /* صندوق الفلاتر الشفاف */
    .filter-box { 
        background: rgba(255, 255, 255, 0.95);
        padding: 25px; 
        border-radius: 20px; 
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        margin-bottom: 30px;
    }
    
    /* الكروت بلون أبيض ناصع للتباين مع الخلفية */
    .project-card { 
        background: white; 
        border-radius: 20px; 
        margin-bottom: 20px; 
        overflow: hidden; 
        padding: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }

    /* زرار التفاصيل الأزرق الملكي */
    div.stButton > button {
        background-color: #003366 !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 8px 25px !important;
        font-weight: 700 !important;
        border: none !important;
        transition: 0.3s !important;
    }
    
    div.stButton > button:hover {
        background-color: #D4AF37 !important;
        transform: scale(1.05);
    }
    
    h1, h2, h3, p.hero-text { color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
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
    st.markdown('<div class="header-nav"><div style="color:white; font-weight:900; font-size:2rem;">معلوماتى <span style="color:#D4AF37;">العقارية</span></div></div>', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center; margin-bottom:40px;">عقاراتك العالمية.. برؤية مصرية</h1>', unsafe_allow_html=True)

    if df is not None:
        # الفلاتر
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: search_dev = st.text_input("🔍 اسم المطور")
        with c2: search_area = st.selectbox("📍 المنطقة", ["كل المناطق"] + sorted(list(df['Area'].dropna().unique())))
        with c3: search_price = st.selectbox("💰 السعر", ["الكل", "أقل من 5 مليون", "5 - 10 مليون", "أكثر من 10 مليون"])
        st.markdown('</div>', unsafe_allow_html=True)

        # عرض الكروت
        f_df = df.copy()
        if search_dev: f_df = f_df[f_df['Developer'].str.contains(search_dev, case=False, na=False)]
        if search_area != "كل المناطق": f_df = f_df[f_df['Area'] == search_area]

        for _, row in f_df.iterrows():
            with st.container():
                st.markdown('<div class="project-card">', unsafe_allow_html=True)
                col_info, col_img = st.columns([3, 1])
                
                with col_info:
                    txt_col, btn_col = st.columns([2.5, 1])
                    with txt_col:
                        st.markdown(f"""
                            <div style="text-align: right;">
                                <div style="color: #003366; font-weight: 900; font-size: 1.6rem;">{row.get('Developer')}</div>
                                <div style="color: #D4AF37; font-weight: 700; font-size: 1.1rem; margin-bottom:5px;">المالك: {row.get('Owner')}</div>
                                <div style="color: #64748b; font-size: 1rem;">📍 {row.get('Area')} | {row.get('Price')} ج.م</div>
                            </div>
                        """, unsafe_allow_html=True)
                    with btn_col:
                        st.write("")
                        st.write("")
                        if st.button("التفاصيل", key=f"btn_{row.get('Developer')}"):
                            st.session_state.selected_item = row.to_dict()
                            st.session_state.page = 'details'
                            st.rerun()

                with col_img:
                    img_url = row.get('Image_URL', 'https://via.placeholder.com/400')
                    st.markdown(f"""
                        <div style="height: 120px; border-radius: 15px; background-image: url('{img_url}'); background-size: cover; background-position: center;"></div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التفاصيل ---
else:
    item = st.session_state.selected_item
    st.markdown('<div style="background:rgba(255,255,255,0.95); padding:40px; border-radius:30px; margin-top:20px;">', unsafe_allow_html=True)
    if st.button("⬅️ عودة للقائمة"):
        st.session_state.page = 'main'
        st.rerun()
    
    st.markdown(f"""
        <h1 style="color:#003366;">{item.get('Developer')}</h1>
        <h3 style="color:#D4AF37;">بإدارة: {item.get('Owner')}</h3>
        <hr>
        <div style="font-size:1.2rem; line-height:1.8; color:#333;">
            <p><b>عن الشركة:</b> {item.get('Description', 'جاري تحديث البيانات...')}</p>
            <p><b>أهم المشاريع:</b> {item.get('Projects')}</p>
            <p><b>المنطقة الأساسية:</b> {item.get('Area')}</p>
            <h2 style="color:#003366;">نطاق الأسعار: {item.get('Price')} ج.م</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
