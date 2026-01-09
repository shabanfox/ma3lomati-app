import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - الخلفية والشكل الأصلي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    /* الخلفية: صورة البرج الأيقوني */
    [data-testid="stAppViewContainer"] {
        background-image: linear-gradient(rgba(0, 20, 40, 0.75), rgba(0, 20, 40, 0.75)), 
                        url('https://images.unsplash.com/photo-1570129477492-45c003edd2be?q=80&w=2070');
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
        padding: 1rem 2% !important;
    }

    /* الهيدر */
    .header-nav { 
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 10px 5%; 
        border-radius: 15px;
        margin-bottom: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* صندوق الفلاتر */
    .filter-box { 
        background: rgba(255, 255, 255, 0.95);
        padding: 20px; 
        border-radius: 15px; 
        margin-bottom: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    /* الكروت: العودة للشكل الأصلي مع تقليل الفواصل */
    .project-card { 
        background: white; 
        border-radius: 12px; 
        margin-bottom: 5px !important; /* فواصل صغيرة جداً */
        overflow: hidden; 
        display: flex;
        height: 160px;
        transition: 0.3s;
    }

    /* زرار التفاصيل الأزرق */
    div.stButton > button {
        background-color: #003366 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 5px 15px !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        border: none !important;
    }
    
    div.stButton > button:hover {
        background-color: #D4AF37 !important;
    }

    h1, p.hero-text { color: white; text-align: center; margin: 0; }
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
    st.markdown('<div class="header-nav"><div style="color:white; font-weight:900; font-size:1.8rem;">معلوماتى <span style="color:#D4AF37;">العقارية</span></div></div>', unsafe_allow_html=True)
    st.markdown('<h2 style="color:white; text-align:center; margin-bottom:15px;">عقاراتك العالمية.. برؤية مصرية</h2>', unsafe_allow_html=True)

    if df is not None:
        # الفلاتر
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: search_dev = st.text_input("🔍 اسم المطور")
        with c2: search_area = st.selectbox("📍 المنطقة", ["كل المناطق"] + sorted(list(df['Area'].dropna().unique())))
        with c3: search_price = st.selectbox("💰 السعر", ["الكل", "أقل من 5 مليون", "10 مليون+"])
        st.markdown('</div>', unsafe_allow_html=True)

        f_df = df.copy()
        if search_dev: f_df = f_df[f_df['Developer'].str.contains(search_dev, case=False, na=False)]
        if search_area != "كل المناطق": f_df = f_df[f_df['Area'] == search_area]

        # عرض الكروت بالشكل اللي طلبته
        for _, row in f_df.iterrows():
            # كارت المطور
            col_info_btn, col_img = st.columns([3, 1])
            
            with col_info_btn:
                # حاوية بيضاء تحاكي الكارت
                st.markdown(f"""
                <div style="background:white; height:150px; border-radius:15px 0 0 15px; padding:15px; display:flex; justify-content:space-between; align-items:center; border-left:1px solid #eee;">
                    <div style="text-align:right;">
                        <div style="color:#003366; font-weight:900; font-size:1.4rem; margin:0;">{row.get('Developer')}</div>
                        <div style="color:#D4AF37; font-weight:700; font-size:1rem;">المالك: {row.get('Owner')}</div>
                        <div style="color:#64748b; font-size:0.9rem;">📍 {row.get('Area')} | {row.get('Price')} ج.م</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # وضع الزرار فوق الكارت برفق (بسبب قيود streamlit)
                st.markdown('<div style="margin-top:-60px; margin-right:20px; position:relative; z-index:99;">', unsafe_allow_html=True)
                if st.button("التفاصيل", key=f"btn_{row.get('Developer')}"):
                    st.session_state.selected_item = row.to_dict()
                    st.session_state.page = 'details'
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            with col_img:
                img_url = row.get('Image_URL', 'https://via.placeholder.com/400')
                st.markdown(f"""
                    <div style="height:150px; border-radius:0 15px 15px 0; background-image: url('{img_url}'); background-size: cover; background-position: center;"></div>
                """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-bottom:5px;'></div>", unsafe_allow_html=True)

# --- صفحة التفاصيل ---
else:
    item = st.session_state.selected_item
    st.markdown('<div style="background:rgba(255,255,255,0.95); padding:30px; border-radius:20px; margin-top:10px;">', unsafe_allow_html=True)
    if st.button("⬅️ عودة"):
        st.session_state.page = 'main'
        st.rerun()
    
    st.markdown(f"<h2 style='color:#003366;'>{item.get('Developer')}</h2>", unsafe_allow_html=True)
    st.write(item.get('Description', 'جاري التحديث...'))
    st.markdown('</div>', unsafe_allow_html=True)
